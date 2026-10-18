#!/bin/bash
export PATH="/home/portchud/.local/bin:$PATH"
source ~/reka-clipper/backend/.venv/bin/activate
cd ~/reka-clipper
python -m uvicorn backend.app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd frontend && npm run dev -- --host &
FRONTEND_PID=$!
wait
