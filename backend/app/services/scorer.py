import json
import os
from typing import List, Dict, Any


def build_prompt(transcript: List[Dict[str, Any]], max_clips: int = 5) -> str:
    full_text = "\n".join(
        [f"{t['start']:.2f}-{t['end']:.2f}: {t['text']}" for t in transcript]
    )
    return f"""You are an expert short-form video editor specializing in viral clips for TikTok, YouTube Shorts, and Reels.

Analyze this transcript and identify the {max_clips} best clips based on:
1. Hook potential (first 3 seconds must grab attention)
2. Engagement/value (insightful, surprising, funny, emotional)
3. Self-contained (makes sense standalone)
4. Viral potential (shareable)

Transcript:
{full_text}

Return ONLY a valid JSON array with this exact schema (no explanation):
[
  {{
    "start": float,
    "end": float,
    "title": "short catchy title",
    "hook": "the hook text (first few words/line)",
    "rationale": "why this clip is good",
    "virality_score": int (0-100),
    "category": "educational|entertainment|motivational|other"
  }}
]

Ensure timestamps align with the transcript and each clip is 15-60 seconds ideally. Avoid cutting mid-sentence if possible."""


def _extract_json(text: str) -> List[Dict[str, Any]]:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("no JSON array found")
    return json.loads(text[start : end + 1])


def score_clips(
    transcript: List[Dict[str, Any]], max_clips: int = 5, model: str | None = None
) -> List[Dict[str, Any]]:
    """Score clips using Ollama (local) or any OpenAI-compatible API (env-configured)."""
    prompt = build_prompt(transcript, max_clips)
    raw = _call_llm(prompt, model)
    return _extract_json(raw)[:max_clips]


def _call_llm(prompt: str, model: str | None, timeout: float = 90.0) -> str:
    base_url = os.environ.get("LLM_BASE_URL", "http://localhost:11434")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = model or os.environ.get("LLM_MODEL", "tinyllama")

    if base_url.rstrip("/").endswith("11434"):
        # Ollama native API
        import ollama

        client = ollama.Client(host=base_url, timeout=timeout)
        resp = client.generate(
            model=model,
            prompt=prompt,
            options={"temperature": 0.7, "num_ctx": 4096, "num_predict": 1200},
        )
        return resp["response"]

    # OpenAI-compatible API (OpenAI, Groq, OpenRouter, DeepSeek, etc.)
    import httpx

    resp = httpx.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
        timeout=90,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
