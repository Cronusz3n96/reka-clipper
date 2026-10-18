# reka-clipper

AI YouTube clip generator inspired by Reka Clip. Picks the best viral clips from YouTube videos with:

- Transcript extraction (YouTube auto-captions via `youtube-transcript-api`, fallback to local `faster-whisper`)
- AI clip selection via Ollama (configurable model)
- MiroFish-inspired scoring to pick the best performing clips from candidates
- Auto captions, 9:16 vertical cropping, virality scoring

## Quick Start

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or: pip install -e .
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # runs on http://localhost:5173
```

### Run both with concurrently
```bash
npm install
npm run dev
```

## Requirements
- Python 3.11+
- Node.js 18+
- Ollama installed & running with a model (e.g., `ollama pull llama3.1:8b`)
- FFmpeg (required by moviepy/faster-whisper)
