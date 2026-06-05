"""Hugging Face Spaces entrypoint.

HF Spaces (SDK: docker) runs this. Serves the FastAPI app on $PORT (7860).
Browser streams webcam frames to /ws/stream — Space stays headless.
"""
import os
import uvicorn

# reuse the real backend app
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
from app.main import app  # noqa: E402

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "7860")))
