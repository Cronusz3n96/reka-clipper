from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs


def _extract_video_id(url: str) -> Optional[str]:
    parsed = urlparse(url)
    host = (parsed.hostname or "").replace("www.", "")
    if host == "youtu.be":
        return parsed.path.lstrip("/").split("/")[0] or None
    if host in ("youtube.com", "m.youtube.com", "music.youtube.com"):
        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) >= 2 and parts[0] in ("shorts", "embed", "live", "v"):
            return parts[1]
    if len(url) == 11 and url.isalnum():
        return url
    return None


def get_youtube_transcript(url: str) -> Optional[List[Dict[str, Any]]]:
    """Fetch YouTube captions (fast, free). Returns None if unavailable."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        video_id = _extract_video_id(url)
        if not video_id:
            return None
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id)
        return [
            {"start": float(s.start), "end": float(s.start + s.duration), "text": s.text}
            for s in fetched
        ]
    except Exception:
        return None


def transcribe_with_whisper(audio_path: str, model_size: str = "base") -> List[Dict[str, Any]]:
    """Local Whisper fallback when no YouTube captions exist."""
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(audio_path, word_timestamps=True)
    result = []
    for segment in segments:
        result.append(
            {
                "start": float(segment.start),
                "end": float(segment.end),
                "text": segment.text.strip(),
                "words": [
                    {"start": float(w.start), "end": float(w.end), "word": w.word}
                    for w in (segment.words or [])
                ]
                if segment.words
                else [],
            }
        )
    return result
