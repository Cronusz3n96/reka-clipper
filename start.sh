#!/bin/bash
export PATH="/home/portchud/.local/bin:$PATH"
cd ~/reka-clipper/backend && source .venv/bin/activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
cd ~/reka-clipper/frontend && npx vite --host 0.0.0.0 --port 5173 &
wait
