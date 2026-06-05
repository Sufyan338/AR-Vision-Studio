"""HUD overlay: FPS, active filter, tracking status, gesture, confidence, CPU.

Pure OpenCV drawing. psutil is optional; CPU shows 'n/a' if missing."""

from __future__ import annotations

import time

import cv2
import numpy as np

try:
    import psutil
    _HAS_PSUTIL = True
except Exception:
    _HAS_PSUTIL = False

CYAN = (255, 200, 0)
GREEN = (0, 255, 120)
RED = (60, 60, 255)
FONT = cv2.FONT_HERSHEY_SIMPLEX


class FPSMeter:
    def __init__(self, window: int = 30) -> None:
        self._t = time.time()
        self._fps = 0.0
        self._alpha = 0.9

    def tick(self) -> float:
        now = time.time()
        dt = now - self._t
        self._t = now
        if dt > 0:
            inst = 1.0 / dt
            self._fps = self._alpha * self._fps + (1 - self._alpha) * inst
        return self._fps


def draw_hud(frame: np.ndarray, *, fps: float, filter_name: str,
             tracking: bool, gesture: str, confidence: float) -> np.ndarray:
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 64), (10, 10, 10), -1)
    frame = cv2.addWeighted(overlay, 0.45, frame, 0.55, 0)

    cpu = f"{psutil.cpu_percent():.0f}%" if _HAS_PSUTIL else "n/a"
    track_col = GREEN if tracking else RED
    track_txt = "TRACKING" if tracking else "NO HANDS"

    cv2.putText(frame, "AR VISION STUDIO", (12, 26), FONT, 0.7, CYAN, 2)
    cv2.putText(frame, f"FPS {fps:4.1f}", (12, 52), FONT, 0.5, CYAN, 1)
    cv2.putText(frame, f"FILTER: {filter_name.upper()}", (160, 52),
                FONT, 0.5, CYAN, 1)
    cv2.putText(frame, track_txt, (w - 300, 26), FONT, 0.55, track_col, 2)
    cv2.putText(frame, f"GESTURE: {gesture}", (w - 300, 48), FONT, 0.5, CYAN, 1)
    cv2.putText(frame, f"CONF {confidence:.2f}", (w - 120, 48),
                FONT, 0.5, CYAN, 1)
    cv2.putText(frame, f"CPU {cpu}", (w - 120, 26), FONT, 0.5, CYAN, 1)
    return frame
