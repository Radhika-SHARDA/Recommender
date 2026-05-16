# SHL Conversational Assessment Recommender

A conversational AI agent that helps hiring managers find the right SHL Individual Test Solutions through natural dialogue.

## Architecture

```
POST /chat  ──►  Conversation history
                     │
                     ▼
              System prompt with
              full SHL catalog
                     │
                     ▼
           Claude claude-sonnet-4-20250514
                     │
                     ▼
         JSON output validation
         (URL + name guardrail)
                     │
                     ▼
              Structured response
         {reply, recommendations, end_of_conversation}
```

## Endpoints

### `GET /health`
Returns `{"status": "ok"}` — used for readiness checks.

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
  "reply": "Got it. Here are 5 assessments for a mid-level Java developer with stakeholder needs.",
  "recommendations": [
    {"name": "Java 8 (New)", "url": "https://www.shl.com/...", "test_type": "K"},
    {"name": "OPQ32r", "url": "https://www.shl.com/...", "test_type": "P"}
  ],
  "end_of_conversation": false
}
```

## Local Development

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 4. Run tests
python test_agent.py
```

## Deploy to Render

1. Push this folder to a GitHub repository.
2. Go to [render.com](https://render.com) → New → Web Service → Connect repo.
3. Render auto-detects `render.yaml`.
4. Add environment variable `ANTHROPIC_API_KEY` in the Render dashboard.
5. Deploy. The `/health` endpoint will be live within ~2 minutes.

## Agent Behavior

| Scenario | Behavior |
|---|---|
| Vague query ("I need an assessment") | Asks one clarifying question |
| Role + level specified | Returns 1–10 catalog assessments |
| User changes constraints | Updates shortlist, doesn't restart |
| Comparison request | Answers from catalog descriptions only |
| Off-topic / legal / injection | Refuses and redirects |
| 8 turns reached | Sets `end_of_conversation: true` |

## Catalog Coverage

35+ SHL Individual Test Solutions covering:
- **Cognitive / Ability**: Verify Numerical, Verbal, Inductive, Deductive, Mechanical, Checking
- **Personality & Behaviour**: OPQ32r, OPQ32n, MQ, CCQ, SAQ
- **Situational Judgement**: Manager SJT, Graduate SJT, Customer Service SJT
- **Knowledge & Skills (IT)**: Java 8, Core Java, Python, SQL, JavaScript, Spring, .NET, C++, Agile
- **Simulations**: Automata Fix, Automata Pro, Customer Service Simulation
- **Business & Finance**: Financial Awareness, Calculation
- **Leadership & Development**: SHL Leadership Report, UCR, 360 Feedback
- **Safety & Industry**: SafetyAQ, Work Safety Questionnaire
- **Retail & Healthcare**: Retail Sales Associate, Healthcare Reasoning Inventory
