# SHL Assessment Recommender

Conversational recommender for SHL Individual Test Solutions, built on a retrieval-augmented generation pipeline with a catalog-URL validator that pins every output to a real product.

**Author:** Radhika Sharda · **Assignment:** SHL Labs – AI Intern Role
**Live endpoint:** https://recommender-3-ki1j.onrender.com
**Approach doc:** [`APPROACH.md`](./APPROACH.md)

---

## Pipeline

```
POST /chat
   │
   ▼
FastAPI handler        ◀── schema validation, 8-turn cap
   │
   ▼
1. RETRIEVE            ◀── search_products() over ALL user turns
   │                       + any product whose name appears in conversation
   │                       → top 15 candidates
   ▼
2. AUGMENT + GENERATE  ◀── Gemini 2.0 Flash, JSON mode, temp 0.2
   │                       5-behavior system prompt
   │                       (Clarify · Recommend · Refine · Compare · Refuse)
   │                       candidates injected as JSON
   ▼
3. VALIDATE            ◀── URL must be in catalog; else drop
   │                       name-match → substitute canonical URL
   │                       normalise test_type to single uppercase letter
   ▼
Response (spec-compliant JSON)

On LLM failure → graceful fallback to retrieval top-5 (still catalog-only).
```

## Why this shape

- **RAG, not just LLM.** Pure LLM would invent products. Pure retrieval can't handle Clarify/Compare/Refine naturally. The pipeline gets both.
- **Validator is the floor, not a backup.** Even if Gemini hallucinates a URL, the validator drops it. Hallucination rate is zero by construction.
- **Retrieval over concatenated user turns.** This is what makes refinement work — *"add personality tests"* gets scored together with the earlier *"Java developer"* query, so the candidate pool reflects both constraints.
- **Fallback path keeps hard evals green during outages.** Render free tier + Gemini availability = real failure modes. On LLM error, top-5 retrieval results are returned — schema-compliant, catalog-only.

## Files

```
main.py             FastAPI service, validator, fallback (~190 lines)
prompts.py          System prompt template + candidate formatter
llm.py              Gemini Flash client (plain httpx, no SDK)
catalog_data.py     41-product catalog + search_products scorer
test_agent.py       11 probes against live /chat
test_helpers.py     10 unit tests for the deterministic parts
requirements.txt    fastapi, uvicorn, pydantic, httpx
APPROACH.md         2-page design doc — read this first
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
    {"role": "assistant", "content": "Sure. What is the seniority level?"},
    {"role": "user", "content": "Mid-level, around 4 years"}
  ]
}
```

**Response:**

```json
{
  "reply": "Got it. Here are 5 assessments that fit a mid-level Java dev with stakeholder needs.",
  "recommendations": [
    {"name": "Java 8 (New)", "url": "https://www.shl.com/...", "test_type": "K"},
    {"name": "OPQ32r", "url": "https://www.shl.com/...", "test_type": "P"}
  ],
  "end_of_conversation": true
}
```

`recommendations` is `[]` when the agent is clarifying, comparing, or refusing. `end_of_conversation` is `true` once a shortlist has been committed or when the 8-turn cap is hit.

## Setup

### 1. Get a Gemini API key (free)

Visit https://aistudio.google.com/app/apikey, sign in with a Google account, click "Create API key". Free tier is 15 requests/minute — more than enough for the evaluator.

### 2. Run locally

```bash
git clone https://github.com/Radhika-SHARDA/Recommender.git
cd Recommender
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here               # Windows: set GEMINI_API_KEY=...
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Test

```bash
# unit tests (no LLM needed)
python test_helpers.py

# integration tests against local server
python test_agent.py

# against the deployed endpoint
BASE_URL=https://recommender-3-ki1j.onrender.com python test_agent.py
```

`test_helpers.py` exercises retrieval, validation, normalisation, and fallback — 10 tests, all passing without the LLM. `test_agent.py` runs 11 probes against the live `/chat`.

## Deployment

Render free tier. Add `GEMINI_API_KEY` under **Settings → Environment**. Render auto-redeploys on every push to `main`.

Cold start adds 20–40s on the first request after idle. The evaluator's 2-minute wake-up window on `/health` covers this.

## Known limitations

Documented honestly in `APPROACH.md` §4. In brief:
- Tag-based retrieval has good recall on queries whose vocabulary overlaps the tags, lower recall on heavily paraphrased queries. An embedding index would close the gap and is the planned next step.
- LLM behaviour has inherent variance. Temperature 0.2 + JSON mode minimises it, but I recommend running `test_agent.py` against the deployed service to verify behavioural probes in your evaluator's exact context.
- Free Gemini tier rate-limits at 15 RPM. The evaluator runs serially well within that, but parallel evaluator runs could hit the cap.
