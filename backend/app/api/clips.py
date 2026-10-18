from fastapi import APIRouter, HTTPException
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
    use_whisper: bool = True
    ollama_model: str = "tinyllama"
    auto_captions: bool = True
    vertical_9x16: bool = True

class ClipResponse(BaseModel):
    url: str
    clips: List[Clip]
    video_path: Optional[str] = None

@router.post("/clips", response_model=ClipResponse)
async def generate_clips(req: ClipRequest):
    try:
        from ..services.youtube import download_audio, get_video_info
        from ..services.transcribe import transcribe_with_whisper, get_youtube_transcript
        from ..services.scorer import build_prompt
        import ollama
        
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "audio.wav")
            download_audio(req.url, audio_path)
            transcript = get_youtube_transcript(req.url)
            if transcript is None or len(transcript) == 0:
                transcript = transcribe_with_whisper(audio_path, model_size="base")
            if not transcript:
                raise HTTPException(status_code=400, detail="Could not transcribe video")
            prompt = build_prompt(transcript, req.max_clips)
            response = ollama.generate(
                model=req.ollama_model,
                prompt=prompt,
                options={"temperature": 0.7, "num_ctx": 2048, "num_predict": 800}
            )
            try:
                clips_data = json.loads(response['response'])
            except Exception:
                clips_data = []
            from ..services.mirofish import mirofish_score_clip
            clips = []
            for c in clips_data[:req.max_clips]:
                c['score'] = mirofish_score_clip(c, transcript)
                clips.append(Clip(**c))
            return ClipResponse(url=req.url, clips=clips)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
