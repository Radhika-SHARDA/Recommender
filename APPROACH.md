# Approach Document — SHL Conversational Assessment Recommender
**Candidate:** Radhika Sharda | **Role:** AI Intern, SHL Labs

---

## 1. Problem Decomposition

The core challenge is turning a vague, open-ended hiring intent into a grounded shortlist of SHL assessments — without hallucinating products that do not exist in the catalog. This requires three things to work together: a reliable data layer (the catalog), a reasoning layer (the LLM), and a guardrail layer (output validation).

I decomposed the problem into four sub-problems:
1. **Catalog acquisition** — scrape and structure the SHL Individual Test Solutions catalog.
2. **Agent behavior** — clarify, recommend, refine, compare, and refuse correctly.
3. **Stateless API design** — receive full conversation history, return structured JSON.
4. **Hallucination prevention** — every URL and name must come from the catalog, validated post-generation.

---

## 2. Catalog Strategy

The SHL product catalog renders via JavaScript, making static HTML scraping insufficient. My approach:

- **Primary**: A `catalog_data.py` module containing 35+ manually curated Individual Test Solution entries with names, URLs, descriptions, test types, job levels, languages, job families, and semantic tags.
- **Sourcing**: Product pages accessed via `web_fetch` during development; each entry cross-referenced against the official SHL catalog pages (e.g., `shl.com/solutions/products/product-catalog/view/...`).
- **Deployed enrichment**: The production service includes a background scraper using Playwright that refreshes the catalog daily via the paginated catalog URL (`?start=0&type=1`) — tolerating cold starts gracefully by serving the static catalog if the scrape fails.

The catalog is structured as a Python list of typed dicts, making it easy to search, filter, and inject into prompts without a vector database (appropriate for ~200 products). A simple tag-based scoring function (`search_products`) pre-filters candidates before LLM reasoning.

---

## 3. Agent Design

**Model**: `claude-sonnet-4-20250514` — fast enough for 30-second timeouts, capable enough for multi-turn structured reasoning.

**Context engineering**: The entire catalog (name, URL, type, levels, tags, 200-char description) is injected into the system prompt on every request. This ensures the model always has ground truth and never relies on prior training knowledge about SHL products. At ~35 products × ~80 tokens each, this fits comfortably in the context window and avoids retrieval latency.

**Behavioral instructions** in the system prompt explicitly define four states:
- *Clarify*: ask one focused question when intent is ambiguous (role, level, or skill area is unknown).
- *Recommend*: return 1–10 catalog items once sufficient context exists; include JD parsing.
- *Refine*: treat constraint changes as shortlist updates, not conversation restarts.
- *Compare*: answer from catalog descriptions only — no model priors.

**Turn cap**: A hard check at 8 messages returns `end_of_conversation: true`, preventing runaway conversations.

**Refusal**: The system prompt instructs the model to decline off-topic queries (legal, HR general, prompt injections) and return empty recommendations.

---

## 4. Output Validation & Hallucination Prevention

Claude is instructed to output raw JSON with no markdown fences. A post-generation validator (`_parse_agent_response`):
1. Strips any accidental code fences.
2. Parses JSON, falling back to regex extraction on failure.
3. Checks every recommendation URL and name against the catalog's canonical set.
4. Drops any item not found in the catalog (silent guardrail).
5. Fixes URLs when a correct name is returned with a wrong URL.

This means even if Claude hallucinates an assessment name, it will be silently removed from the response — the evaluator never sees a non-catalog URL.

---

## 5. Evaluation Approach

**Hard evals (local)**: `test_agent.py` runs 11 automated test cases covering schema compliance, turn cap, vague-query behavior, catalog-URL validation, refinement, off-topic refusal, prompt injection, comparison, and JD parsing.

**Recall@10 strategy**: By injecting the full catalog and using rich tags (e.g., `["Java","backend","developer","Spring","OOP"]`) I maximise the model's ability to match queries to the right products. For holdout traces, the tag vocabulary covers common hiring scenarios (IT roles, sales, customer service, management, safety, healthcare).

**What didn't work**:
- *Vector search (FAISS)*: tested sentence-transformer embeddings over the catalog. The catalog is small enough (~35 items) that embedding search added 2–3 seconds of latency with no measurable recall improvement over tag-based scoring + LLM reasoning.
- *Tool-use / function calling*: tried exposing `search_catalog` as a Claude tool. This added a second round-trip (~5–8 seconds) and increased timeout risk. In-prompt catalog injection proved faster and more reliable within the 30-second budget.
- *Streaming*: FastAPI streaming complicated the JSON parsing. Switched to synchronous `messages.create` for schema reliability.

---

## 6. Stack & Deployment

| Layer | Choice | Reason |
|---|---|---|
| LLM | Claude claude-sonnet-4-20250514 (Anthropic) | Assignment used Anthropic SDK; best cost/quality/latency |
| API framework | FastAPI + Uvicorn | Fast, Pydantic schema validation built-in |
| Catalog storage | In-process Python module | No DB latency; small enough catalog |
| Deployment | Render (free web service) | Simple `render.yaml` config; auto-deploy from GitHub |
| Testing | `requests` + custom assertions | Lightweight, no framework overhead |

**AI tools used**: Claude Sonnet assisted with boilerplate generation for the FastAPI models and test stubs. All design decisions, system prompt design, and guardrail logic were written and reasoned through by hand.

---

*Total lines of production code: ~400 (main.py + catalog_data.py). Test file: ~160 lines.*
