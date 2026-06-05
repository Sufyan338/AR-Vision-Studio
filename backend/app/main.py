"""FastAPI backend for AR Vision Studio.

Endpoints
---------
GET  /health            -> liveness
GET  /api/filters       -> list filter names
POST /api/process       -> single base64 JPEG frame in/out (stateless demo)
WS   /ws/stream         -> realtime: client sends JPEG bytes, gets processed
                           JPEG + JSON meta back. One Pipeline per connection.

Frontend captures webcam in-browser and streams frames here; backend never
touches a physical camera, so it runs fine in headless containers / HF Spaces.
"""

from __future__ import annotations

import base64
import json

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.pipeline import Pipeline
from app.filters.filters import FILTER_NAMES

app = FastAPI(title="AR Vision Studio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in prod via env
    allow_methods=["*"],
    allow_headers=["*"],
)


def _decode(b64: str) -> np.ndarray:
    raw = base64.b64decode(b64.split(",")[-1])
    arr = np.frombuffer(raw, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def _encode(img: np.ndarray) -> str:
    ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return base64.b64encode(buf).decode() if ok else ""


class FrameIn(BaseModel):
    image: str  # base64 data URL or raw base64 JPEG


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/filters")
def list_filters() -> dict:
    return {"filters": FILTER_NAMES}


@app.post("/api/process")
def process_frame(payload: FrameIn) -> dict:
    """Stateless single-frame demo (no gesture history persistence)."""
    pipe = Pipeline()
    frame = _decode(payload.image)
    out, meta = pipe.process(frame)
    pipe.close()
    return {"image": "data:image/jpeg;base64," + _encode(out), "meta": meta}


@app.websocket("/ws/stream")
async def ws_stream(ws: WebSocket) -> None:
    await ws.accept()
    pipe = Pipeline()
    try:
        while True:
            msg = await ws.receive_bytes()
            arr = np.frombuffer(msg, np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if frame is None:
                continue
            out, meta = pipe.process(frame)
            ok, buf = cv2.imencode(".jpg", out,
                                   [cv2.IMWRITE_JPEG_QUALITY, 75])
            await ws.send_bytes(buf.tobytes())
            await ws.send_text(json.dumps(meta))
    except WebSocketDisconnect:
        pass
    finally:
        pipe.close()
