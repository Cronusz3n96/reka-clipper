from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.clips import router as clips_router

app = FastAPI(title="Reka Clipper", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clips_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
