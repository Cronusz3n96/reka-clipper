import json
from typing import List, Dict, Any
import ollama

def build_prompt(transcript: List[Dict[str, Any]], max_clips: int = 5) -> str:
    full_text = "\n".join([f"{t['start']:.2f}-{t['end']:.2f}: {t['text']}" for t in transcript])
    return f"""You are an expert short-form video editor specializing in creating viral clips for TikTok, YouTube Shorts, and Reels.

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
