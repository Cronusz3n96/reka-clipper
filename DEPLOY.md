# Deployment

## Frontend (Cloudflare Pages) - LIVE
https://reka-clipper.merrittjake65.workers.dev

## Backend Options
1. Render (Docker) - use render.yaml, connect repo
2. Railway - dockerize backend
3. Fly.io - dockerize backend  
4. Replicate/Ollama on separate service + backend
5. Use ngrok/cloudflared to tunnel local backend: cloudflared tunnel --url http://localhost:8000

For full functionality (paste YouTube link -> clips), deploy backend + ensure Ollama is accessible.
