"""Heuristic clip picker used when no LLM is reachable."""
from typing import List, Dict, Any
import re

HOOK_WORDS = [
    "why", "how", "what", "secret", "never", "always", "nobody", "everyone",
    "the best", "the worst", "stop", "listen", "imagine", "here's", "this is",
    "mistake", "truth", "hack", "trick", "crazy", "insane", "warning",
]

SENTENCE_END = re.compile(r"[.!?]$")


def heuristic_clips(transcript: List[Dict[str, Any]], max_clips: int = 5) -> List[Dict[str, Any]]:
    # Score each transcript segment
    scored = []
    for i, seg in enumerate(transcript):
        text = seg["text"].strip()
        low = text.lower()
        score = 40
        score += sum(12 for w in HOOK_WORDS if w in low)
        if SENTENCE_END.search(text):
            score += 8
        words = len(text.split())
        if 5 <= words <= 20:
            score += 10
        scored.append((min(score, 100), i))

    scored.sort(reverse=True)
    chosen: List[Dict[str, Any]] = []
    used = set()
    for score, i in scored:
        if len(chosen) >= max_clips:
            break
        if any(abs(i - j) < 4 for j in used):
            continue
        # build a 15-45s window ending on a sentence boundary if possible
        start = transcript[i]["start"]
        end = transcript[min(i + 5, len(transcript) - 1)]["end"]
        # extend forward slightly for context, cap at 45s
        end = min(end, start + 45)
        if end - start < 10:
            end = min(transcript[-1]["end"], start + 15)
        hook = transcript[i]["text"][:80]
        chosen.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "title": hook or "Clip",
            "hook": hook,
            "rationale": "Strong hook keywords and self-contained moment (heuristic scoring — add an LLM key for AI scoring).",
            "virality_score": int(score),
            "category": "other",
        })
        used.add(i)
    chosen.sort(key=lambda c: c["start"])
    return chosen
