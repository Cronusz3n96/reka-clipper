from typing import List, Dict, Any

def mirofish_score_clip(clip: Dict[str, Any], transcript: List[Dict[str, Any]]) -> float:
    score = 0.0
    text = (clip.get('hook', '') or clip.get('title', '')).lower()
    if any(k in text for k in ['why', 'how', 'what', 'secret', 'hidden', 'never', 'always', 'here']):
        score += 0.1
    vs = clip.get('virality_score', 0)
    if vs:
        score += vs / 1000.0
    duration = clip['end'] - clip['start']
    if 20 <= duration <= 40:
        score += 0.05
    if duration < 10 or duration > 90:
        score -= 0.02
    return max(0.0, min(score, 1.0))
