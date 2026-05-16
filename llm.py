"""
Gemini Flash client for the SHL Assessment Recommender.

We use plain HTTP via httpx rather than the google-generativeai SDK so we
don't bloat dependencies. responseMimeType: application/json gives us
near-guaranteed valid JSON, with Python-side fallback parsing for safety.

Environment variables:
    GEMINI_API_KEY   required, free key from https://aistudio.google.com/app/apikey
    GEMINI_MODEL     optional, defaults to gemini-2.0-flash
"""

import json
import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

LLM_TIMEOUT_SECONDS = 20.0
MAX_OUTPUT_TOKENS = 1024


class LLMError(Exception):
    """Raised when the LLM call fails for any reason. main.py catches this
    and falls back to a rule-based response so the user never sees a 500."""


def _to_gemini_contents(messages: list[dict]) -> list[dict]:
    """Convert OpenAI-style {role, content} messages → Gemini 'contents' format.

    Gemini uses 'user' and 'model' roles. We map assistant → model.
    """
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    return contents


def _extract_json_text(data: dict) -> str:
    """Pull the text body out of Gemini's response envelope."""
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as e:
        raise LLMError(f"unexpected response shape: {str(data)[:300]}") from e


def _parse_json_loose(text: str) -> dict[str, Any]:
    """Parse JSON, tolerating accidental markdown fences or leading prose."""
    text = text.strip()
    if text.startswith("```"):
        # strip ```json ... ``` or ``` ... ```
        text = text.split("```", 2)[1] if "```" in text[3:] else text[3:]
        if text.startswith("json"):
            text = text[4:]
        text = text.rsplit("```", 1)[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # last-ditch: try to slice from first '{' to last '}'
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e != -1 and e > s:
            return json.loads(text[s : e + 1])
        raise


def call_gemini(system_prompt: str, messages: list[dict]) -> dict[str, Any]:
    """Call Gemini Flash with system prompt + conversation. Return parsed JSON.

    Raises LLMError on any failure (network, HTTP, parse).
    """
    if not GEMINI_API_KEY:
        raise LLMError("GEMINI_API_KEY environment variable is not set")

    body = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": _to_gemini_contents(messages),
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2,
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
        },
        # Permissive safety: we filter content ourselves; we don't want
        # the model refusing on a benign hiring query.
        "safetySettings": [
            {"category": c, "threshold": "BLOCK_ONLY_HIGH"}
            for c in (
                "HARM_CATEGORY_HARASSMENT",
                "HARM_CATEGORY_HATE_SPEECH",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "HARM_CATEGORY_DANGEROUS_CONTENT",
            )
        ],
    }

    try:
        with httpx.Client(timeout=LLM_TIMEOUT_SECONDS) as client:
            r = client.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=body)
        r.raise_for_status()
        data = r.json()
    except httpx.TimeoutException as e:
        raise LLMError(f"timeout after {LLM_TIMEOUT_SECONDS}s: {e}") from e
    except httpx.HTTPStatusError as e:
        raise LLMError(
            f"HTTP {e.response.status_code}: {e.response.text[:200]}"
        ) from e
    except httpx.RequestError as e:
        raise LLMError(f"request failed: {e}") from e

    raw = _extract_json_text(data)
    try:
        return _parse_json_loose(raw)
    except json.JSONDecodeError as e:
        raise LLMError(f"could not parse JSON: {e}; raw={raw[:300]}") from e
