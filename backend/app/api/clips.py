from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
import json

router = APIRouter()

class Clip(BaseModel):
    start: float
    end: float
    title: str
    hook: str
    rationale: str
    virality_score: int
    category: str
    score: Optional[float] = None

class ClipRequest(BaseModel):
    url: str
    max_clips: int = 5
    use_whisper: bool = False
    ollama_model: Optional[str] = None
    auto_captions: bool = True
    vertical_9x16: bool = True

class ClipResponse(BaseModel):
    url: str
    clips: List[Clip]
    video_path: Optional[str] = None

@router.get("/health")
def health():
    return {"status": "ok", "service": "reka-clipper-api"}

@router.post("/clips", response_model=ClipResponse)
async def generate_clips(req: ClipRequest):
    try:
        from ..services.youtube import download_audio
        from ..services.transcribe import transcribe_with_whisper, get_youtube_transcript
        from ..services.scorer import score_clips
        from ..services.mirofish import mirofish_score_clip

        transcript = get_youtube_transcript(req.url)
        if not transcript and req.use_whisper:
            # guard: whisper on 512MB instances is risky for long audio
            import os as _os
            if _os.environ.get("RENDER") and _os.environ.get("ENABLE_WHISPER") != "true":
                raise HTTPException(status_code=400, detail="No captions on this video. Whisper fallback is disabled on this instance (set ENABLE_WHISPER=true to enable).")
            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = os.path.join(tmpdir, "audio.wav")
                download_audio(req.url, audio_path)
                transcript = transcribe_with_whisper(audio_path, model_size="base")
        if not transcript:
            raise HTTPException(status_code=400, detail="Could not transcribe video (no captions found and Whisper unavailable)")

        try:
            clips_data = score_clips(transcript, req.max_clips, req.ollama_model)
        except Exception:
            from ..services.fallback import heuristic_clips
            clips_data = heuristic_clips(transcript, req.max_clips)
        clips = []
        for c in clips_data:
            c["score"] = mirofish_score_clip(c, transcript)
            clips.append(Clip(**c))
        return ClipResponse(url=req.url, clips=clips)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
