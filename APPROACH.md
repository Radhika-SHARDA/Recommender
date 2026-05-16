# Approach — SHL Conversational Assessment Recommender

**Candidate:** Radhika Sharda · **Role:** AI Intern, SHL Labs
**Repo:** github.com/Radhika-SHARDA/Recommender · **Endpoint:** recommender-3-ki1j.onrender.com

---

## 1. Design choice and trade-off

I built a **rule-based recommender, not an LLM agent**. Three reasons:

1. **Hallucination is the rubric's most-penalised failure** — every URL must come from the catalog, and one behavior probe is *"% of turns with hallucinations."* A static catalog plus deterministic scoring gives a hallucination rate of zero by construction.
2. **30-second timeout with Render cold starts.** An LLM round-trip plus a JSON-parse retry is risky inside that budget; the rule-based path returns in <50 ms warm.
3. **The catalog is small (41 Individual Test Solutions).** A vector store would add latency and operational surface without measurably improving recall over hand-curated tags at this size.

**The trade-off I made explicit:** I am strong on the **hard evals** (schema, catalog-only URLs, turn cap, hallucination) and **weaker on the conversational behaviors** that benefit from generative language — multi-turn refinement and natural-language comparison. Section 3 lists those gaps without softening them.

## 2. Catalog and retrieval

`catalog_data.py` holds 41 Individual Test Solutions as a list of typed dicts. Each row carries: name, URL, description, `test_type` (single-letter SHL codes — A, B, D, K, P, S are used in this catalog; four products are multi-typed), remote-testing and adaptive-IRT flags, job levels, languages, job families, and a hand-curated **tag list** averaging ~7 tags per product (e.g. `["java","backend","oop","spring"]` for Java 8).

The tags are the workhorse. `search_products(query)` scores each item:

- **+3** for any tag matching a word in the query (or substring match either direction)
- **+2** for a name-word match
- **+1** for description-word match (words >3 chars only, to suppress stopwords)
- Optional `job_levels` / `test_types` / `job_families` filters zero-out or down-rank misses

Sorted descending, top 10 returned. ~30 lines, fully defensible at the deep-dive: I know exactly why a given product ranks where it does, and edits are localised (add a tag → re-rank a product).

## 3. Agent behavior — what works, and what is a known gap

`POST /chat` is stateless. On each call it:

1. Validates schema (role ∈ {user, assistant}, non-empty messages).
2. Enforces the **turn cap** at ≥8 messages → returns `end_of_conversation: true` with empty recommendations.
3. Runs a **keyword refusal** for "legal" / "salary" in the latest message.
4. Runs `search_products` on the **latest user message** and returns the top 5 as recommendations with `end_of_conversation: true`.
5. **Clarify fallback**: if search returns nothing, returns a clarifying question with empty recommendations.

I am being upfront about four known gaps rather than dressing them up:

- **Refinement is single-turn.** Only `messages[-1]` is fed to retrieval. *"Actually, add personality tests"* works only because "personality" matches type-P tags directly; the prior shortlist isn't extended. One-line fix (concatenate user turns with decaying weight), deferred for time.
- **Comparison is not implemented.** *"Difference between OPQ and GSA?"* routes through the same search path. A grounded answer needs either a templated diff over the two products' structured fields, or an LLM with the two records injected. The templated-diff version is the first thing I'd add.
- **Refusal is keyword-based and narrow.** Catches the explicit legal/salary case but paraphrased off-topic queries or prompt-injection can leak through. A score-based gate (zero retrieval signal → refuse) would close most of this.
- **`end_of_conversation: true` on the first shortlist** is intentional — the spec notes the simulated user ends the conversation when given a shortlist — but it forecloses in-conversation refinement.

## 4. Evaluation

`test_agent.py` (160 lines) runs 11 probes against the deployed endpoint: schema compliance, turn cap, vague-query handling, catalog-URL validation, refinement, off-topic refusal, prompt-injection, comparison, and JD parsing.

Honest results on the deployed service:

- **Hard-eval probes pass** — schema, catalog-only URLs, turn cap, JD parsing, basic recommendation.
- **Behavior probes that depend on multi-turn reasoning or generated prose** — refinement edge cases, the comparison reply, robust refusal of injection — **fail or pass-by-accident**. These are real gaps from Section 3, not test bugs.

I did not run the 10 public conversation traces through the harness format end-to-end. The realistic expectation: high Recall@10 on queries whose vocabulary overlaps my tags (Java, sales, customer service, cognitive, personality, IT roles), and lower recall on paraphrased or domain-shifted queries because tag matching does not generalise.

## 5. What didn't work / what I would do next

- **First fix: rule-based retrieval as a pre-filter for an LLM final-write step.** The keyword scorer narrows 41 items to ~10 candidates; the LLM picks the final 1–10 and writes the reply with the candidate list injected as ground truth. This splits the latency budget cleanly, keeps hallucination at zero (URLs only from the pre-filter), and unlocks proper Clarify / Refine / Compare behaviors.
- **Conversation-aware retrieval** — concatenate user turns (skip assistant turns) with decaying weight before scoring. Cheap, no architecture change, immediately fixes the refinement probe.
- **Templated comparison route** — pattern-match *"difference between X and Y"*, resolve X and Y to catalog rows, return a structured diff over `test_type`, `job_levels`, `description`. No LLM required.
- **Score-based refusal gate** replacing keyword refusal — if the top retrieval score is below a threshold and no SHL-specific entities are in the query, refuse instead of clarifying.

## 6. Stack and AI tooling

FastAPI + Uvicorn + Pydantic; Python module catalog; deployed on Render free tier. **No vector DB, no LLM in the runtime path** — both deliberate, both defensible at the deep-dive.

**AI tools used:** Claude assisted with scaffolding the FastAPI boilerplate and Pydantic models, and with expanding the tag vocabulary on individual catalog entries from their SHL descriptions. The retrieval scoring, the routing logic, the trade-off framing above, and the test suite were written by hand.
