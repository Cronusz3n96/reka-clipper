from typing import List, Dict, Any
from faster_whisper import WhisperModel

def transcribe_with_whisper(audio_path: str, model_size: str = "base") -> List[Dict[str, Any]]:
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, word_timestamps=True)
    result = []
    for segment in segments:
        result.append({
            "start": float(segment.start),
            "end": float(segment.end),
            "text": segment.text.strip(),
            "words": [
                {
                    "start": float(w.start),
                    "end": float(w.end),
                    "word": w.word
                } for w in (segment.words or [])
            ] if segment.words else []
        })
    return result

def get_youtube_transcript(url: str):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        if parsed.hostname == 'youtu.be':
            video_id = parsed.path[1:]
        else:
            video_id = parse_qs(parsed.query).get('v', [parsed.path.split('/')[-1]])[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return [{"start": t['start'], "end": t['start'] + t['duration'], "text": t['text']} for t in transcript]
    except Exception as e:
        return None
