"""Self-contained Gradio Space: upload an image, pick a filter, get result.

A lighter HF demo that needs no separate frontend. Gesture/AR-window features
require the WebSocket + browser webcam path (FastAPI app.py)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import gradio as gr
from app.filters.filters import FILTER_NAMES, apply_filter
import cv2


def run(image, filter_name):
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    out = apply_filter(filter_name, bgr)
    return cv2.cvtColor(out, cv2.COLOR_BGR2RGB)


demo = gr.Interface(
    fn=run,
    inputs=[gr.Image(label="Input"),
            gr.Dropdown(FILTER_NAMES, value="glow", label="Filter")],
    outputs=gr.Image(label="Filtered"),
    title="AR Vision Studio — Filter Playground",
    description="Apply any of the 12 OpenCV filters to an image.",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))
