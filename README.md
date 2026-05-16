SHL Assessment Recommender

Conversational AI agent for recommending SHL Individual Test Solutions

Author: Radhika Sharda
Assignment: SHL Labs – AI Intern Role

1. Problem Statement

Hiring managers often struggle to identify the correct SHL assessments for a specific role, level, or skill requirement.

The objective of this project is to build a conversational AI system that:

Recommends only valid SHL Individual Test Solutions
Never hallucinates assessment names or URLs
Grounds all recommendations in a structured internal catalog
Produces structured JSON output suitable for automated evaluation
2. System Overview

This is a stateless FastAPI-based conversational agent that uses Claude (Anthropic) as the reasoning engine, with a strictly controlled system prompt and post-validation layer.

Core Design Principles
Strict grounding to in-memory catalog
Zero hallucination tolerance
Structured JSON output enforcement
Turn-cap conversation management
Prompt injection resistance
3. Architecture
Client
   │
   ▼
POST /chat
   │
   ▼
FastAPI Backend
   │
   ├── System Prompt + Catalog Injection
   │
   ▼
Claude (Anthropic API)
   │
   ▼
JSON Parsing + Validation Layer
   │
   ▼
Validated Structured Response
4. Key Technical Decisions
1. Stateless Conversation Design

The /chat endpoint requires full conversation history in every request.

This ensures:

No server-side memory complexity
Easy scaling
Deterministic evaluation behavior
2. Catalog Grounding Strategy

The entire SHL product catalog is:

Loaded in-process (catalog_data.py)
Injected into the system prompt
Validated post-response

Even if the model attempts hallucination, the validation layer drops invalid entries.

3. JSON-Only Response Enforcement

The system prompt strictly mandates:

{
  "reply": "...",
  "recommendations": [...],
  "end_of_conversation": false
}

The backend:

Strips markdown fences
Attempts fallback JSON extraction
Validates URLs and names against catalog
Enforces maximum of 10 recommendations
4. Hallucination Safeguards

Recommendations are accepted only if:

URL matches catalog exactly
OR name matches catalog and canonical URL is substituted

Anything else is dropped.

5. Conversation Turn Cap

Hard cap of 8 total turns (user + assistant).

Prevents:

Infinite loops
Token explosion
Runaway API cost
5. API Endpoints
Health Check
GET /health

Response:

{"status": "ok"}
Chat Endpoint
POST /chat
Content-Type: application/json

Request format:

{
  "messages": [
    {
      "role": "user",
      "content": "Assessment for entry-level data analyst"
    }
  ]
}

Response format:

{
  "reply": "Here are recommended assessments...",
  "recommendations": [
    {
      "name": "Verify Numerical Ability Test",
      "url": "https://...",
      "test_type": "A"
    }
  ],
  "end_of_conversation": false
}
6. Deployment

Hosted on Render (Free Tier).

Base URL:

https://recommender-3-ki1j.onrender.com

Note: First request may take 20–40 seconds due to cold start behavior on free hosting.

7. Local Setup
1. Clone Repository
git clone https://github.com/Radhika-SHARDA/Recommender.git
cd Recommender
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install Dependencies
pip install -r requirements.txt
4. Set Environment Variable

You must set your Anthropic API key:

Mac/Linux:

export ANTHROPIC_API_KEY=your_api_key_here

Windows:

set ANTHROPIC_API_KEY=your_api_key_here
5. Run Server
uvicorn main:app --host 0.0.0.0 --port 8000
8. Security & Robustness Considerations
API key stored in environment variables only
No secrets committed to repository
Input role validation
Strict output schema enforcement
Prompt injection resistance via system prompt constraints
Defensive JSON parsing with fallback
9. Limitations
Relies on external LLM availability
Free-tier hosting introduces cold starts
Large catalog injection increases token usage
No streaming response optimization
10. Future Improvements
Tool-calling instead of prompt-only grounding
Embedding-based semantic retrieval instead of full catalog injection
Rate limiting
Streaming responses
Response caching layer
Observability and metrics logging
