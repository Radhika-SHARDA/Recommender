"""
SHL Assessment Recommender — FastAPI Service
Rule-Based Version (No LLM Required)
Author: Radhika Sharda
"""

import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from catalog_data import get_all_products, search_products


# ─── Logging ─────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─── FastAPI App ─────────────────────────────────────
app = FastAPI(
    title="SHL Assessment Recommender",
    description="Rule-based recommender for SHL Individual Test Solutions",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Pydantic Models ─────────────────────────────────
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., min_items=1)


class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation] = Field(default_factory=list)
    end_of_conversation: bool = False


# ─── Catalog ─────────────────────────────────────────
CATALOG = get_all_products()


def _enforce_turn_cap(messages: List[Message]) -> bool:
    return len(messages) >= 8


# ─── Endpoints ───────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.messages:
        raise HTTPException(status_code=400, detail="messages list cannot be empty.")

    for msg in request.messages:
        if msg.role not in ("user", "assistant"):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid role '{msg.role}'. Must be 'user' or 'assistant'."
            )

    if _enforce_turn_cap(request.messages):
        return ChatResponse(
            reply="Maximum conversation length reached. Please start a new conversation.",
            recommendations=[],
            end_of_conversation=True,
        )

    # Get latest user message
    latest_user_message = request.messages[-1].content.strip()

    # Simple guard: decline unrelated questions
    if "salary" in latest_user_message.lower() or "legal" in latest_user_message.lower():
        return ChatResponse(
            reply="I can only assist with SHL Individual Test Solutions recommendations.",
            recommendations=[],
            end_of_conversation=False,
        )

    # Search catalog using your existing retrieval logic
    results = search_products(latest_user_message)

    if not results:
        return ChatResponse(
            reply="Could you clarify the role, job level, or skills required?",
            recommendations=[],
            end_of_conversation=False,
        )

    recommendations = []
    for r in results[:5]:
        recommendations.append(
            Recommendation(
                name=r["name"],
                url=r["url"],
                test_type=",".join(r["test_type"])
            )
        )

    return ChatResponse(
        reply="Here are the most relevant SHL assessments based on your requirements.",
        recommendations=recommendations,
        end_of_conversation=True,
    )


# ─── Entry Point ─────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
