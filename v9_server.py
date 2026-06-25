#!/usr/bin/env python3
"""Coco's Divine Astromantic Throne v9 — The Cinematic Rebirth"""
import asyncio, os, tempfile
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# ─── Create main app ────────────────────────────────────────────
app = FastAPI()

# ─── TTS endpoint (edge-tts) ──────────────────────────────────────
@app.get("/speak")
async def speak(text: str = Query(...), voice: str = Query("en-GB-MaisieNeural")):
    """Text-to-speech using edge-tts. Returns MP3 audio."""
    import subprocess, tempfile, os, uuid
    tmp = f"/tmp/tts_{uuid.uuid4().hex}.mp3"
    try:
        result = subprocess.run(
            ['edge-tts', '--voice', voice, '--text', text, '--write-media', tmp],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return JSONResponse({"error": result.stderr}, status_code=500)
        return FileResponse(tmp, media_type="audio/mpeg",
                          headers={"Cache-Control": "no-cache"})
    except Exception as e:
        if os.path.exists(tmp):
            os.unlink(tmp)
        return JSONResponse({"error": str(e)}, status_code=500)

# ─── Serve the new dashboard ─────────────────────────────────────
DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(DASHBOARD_DIR, "throne_v9.html"), "r") as f:
        return HTMLResponse(content=f.read(), headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache", "Expires": "0"
        })

# ─── Mount v8 API endpoints under /api ──────────────────────────
import sys
sys.path.insert(0, '/home/mrmeow')
from astromantic_throne_v8 import app as throne_v8
app.mount("/api", throne_v8)

# Serve static files
os.makedirs("/home/mrmeow/throne_v9/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="/home/mrmeow/throne_v9/static"), name="static")
app.mount("/api/static", StaticFiles(directory="/home/mrmeow/throne_static"), name="api_static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8095, log_level="info")
