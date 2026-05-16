# SHL Assessment Recommender

Conversational recommender for SHL Individual Test Solutions.

**Author:** Radhika Sharda · **Assignment:** SHL Labs – AI Intern Role
**Live endpoint:** https://recommender-3-ki1j.onrender.com

---

## What this is

A FastAPI service that exposes two endpoints — `GET /health` and `POST /chat` — and returns a grounded shortlist of SHL Individual Test Solutions in the schema required by the assignment evaluator.

The recommender is **rule-based**: no LLM is in the runtime path. Retrieval is a hand-curated, tag-scored lookup over a static catalog. The design rationale and trade-offs are in [`APPROACH.md`](./APPROACH.md).

## Why rule-based

- **Zero hallucination by construction** — every URL returned comes from the static catalog. The rubric's *"% of turns with hallucinations"* probe is zero by design.
- **Predictable latency** — <50ms warm, no LLM round-trip risk inside the 30s evaluator timeout.
- **Catalog is small (41 products)** — vector retrieval would add latency without measurably improving recall over hand-curated tags at this size.

The trade-off — weaker conversational behaviors on refinement, comparison, and robust refusal — is documented honestly in `APPROACH.md` §3.

## Architecture

```
POST /chat
   │
   ▼
FastAPI handler (main.py)
   │   • role validation
   │   • turn cap (≥8 messages → end_of_conversation: true)
   │   • keyword refusal (legal / salary)
   │
   ▼
search_products(latest_user_message)   ← catalog_data.py
   │   • tag-word match  +3
   │   • name-word match +2
   │   • description-word match (>3 chars) +1
   │   • optional job_levels / test_types / job_families filters
   │
   ▼
Top-5 recommendations + reply + end_of_conversation
```

## API

### `GET /health`

```json
{ "status": "ok" }
```

### `POST /chat`

**Request:**

```json
{
  "messages": [
    {"role": "user", "content": "Hiring a Java developer who works with stakeholders"},
    {"role": "assistant", "content": "Sure. What is seniority level?"},
    {"role": "user", "content": "Mid-level, around 4 years"}
  ]
}
```

**Response:**

```json
{
  "reply": "Here are the most relevant SHL assessments based on your requirements.",
  "recommendations": [
    {"name": "Java 8 (New)", "url": "https://www.shl.com/...", "test_type": "K"}
  ],
  "end_of_conversation": true
}
```

`recommendations` is `[]` when the agent is clarifying or refusing. `end_of_conversation` is `true` once a shortlist has been committed (matches the evaluator's note that the simulated user ends the conversation when given a shortlist) or when the 8-turn cap is hit.

## Local setup

```bash
git clone https://github.com/Radhika-SHARDA/Recommender.git
cd Recommender
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

No API keys, no environment variables. The catalog ships in `catalog_data.py`.

## Tests

```bash
# against local server
python test_agent.py

# against the deployed endpoint
BASE_URL=https://recommender-3-ki1j.onrender.com python test_agent.py
```

`test_agent.py` runs 11 probes covering schema, turn cap, vague-query handling, catalog-URL validation, refinement, off-topic refusal, prompt-injection, comparison, and JD parsing. See `APPROACH.md` §4 for which probes pass and which surface known design gaps.

`test_agent.py` requires the `requests` library (`pip install requests`); it's not in `requirements.txt` because the deployed service doesn't need it.

## Deployment

Render free tier. Cold start adds 20–40s on the first request after idle; subsequent requests are fast. The `/health` endpoint is intentionally trivial so the evaluator can warm the dyno before scoring.

## Repo layout

```
main.py              FastAPI service (2 endpoints, ~130 lines)
catalog_data.py      41-product catalog + search_products scorer
test_agent.py        11 local probes against /chat
requirements.txt     fastapi, uvicorn, pydantic, httpx
APPROACH.md          2-page design doc — read this first
```

## Honest limitations

These are real, known, and not hidden in the approach doc:

- **Refinement is single-turn.** Only the latest user message is fed to retrieval.
- **Comparison is not implemented.** *"Difference between OPQ and GSA?"* routes through the same search path.
- **Refusal is keyword-only** (`legal` / `salary`). Paraphrased off-topic queries and prompt-injection can leak through.

The next-step architecture (rule-based pre-filter + small LLM final-write step) is sketched in `APPROACH.md` §5.
