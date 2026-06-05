"""Pipeline: glue tracking + gestures + AR window + filters + HUD per frame.

Holds session state (current filter index, frozen, etc). One Pipeline instance
per client/session. Stateless functions live in their own modules."""

from __future__ import annotations

import os
import time
from datetime import datetime

import cv2
import numpy as np

from app.core.ar_window import ARWindow
from app.core.gestures import GestureEngine
from app.core.hand_tracking import HandTracker
from app.core.hud import FPSMeter, draw_hud
from app.filters.filters import FILTER_NAMES, apply_filter

CAPTURE_DIR = os.getenv("CAPTURE_DIR", "captures")
os.makedirs(CAPTURE_DIR, exist_ok=True)


class Pipeline:
    def __init__(self) -> None:
        self.tracker = HandTracker()
        self.gestures = GestureEngine()
        self.window = ARWindow()
        self.fps = FPSMeter()
        self.filter_idx = 0
        self.recording = False
        self._writer: cv2.VideoWriter | None = None

    @property
    def filter_name(self) -> str:
        return FILTER_NAMES[self.filter_idx]

    def _handle_action(self, action: str | None, frame) -> None:
        if action == "create_window":
            self.window.freeze(False)
        elif action == "freeze_window":
            self.window.freeze(True)
        elif action == "next_filter":
            self.filter_idx = (self.filter_idx + 1) % len(FILTER_NAMES)
        elif action == "prev_filter":
            self.filter_idx = (self.filter_idx - 1) % len(FILTER_NAMES)
        elif action == "exit_mode":
            self.window.reset()
        elif action == "screenshot":
            self.screenshot(frame)
        elif action == "toggle_record":
            self.toggle_record(frame)

    def screenshot(self, frame) -> str:
        path = os.path.join(
            CAPTURE_DIR, f"shot_{datetime.now():%Y%m%d_%H%M%S}.png")
        cv2.imwrite(path, frame)
        return path

    def toggle_record(self, frame) -> None:
        if self.recording:
            if self._writer:
                self._writer.release()
                self._writer = None
            self.recording = False
        else:
            h, w = frame.shape[:2]
            path = os.path.join(
                CAPTURE_DIR, f"rec_{datetime.now():%Y%m%d_%H%M%S}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self._writer = cv2.VideoWriter(path, fourcc, 20.0, (w, h))
            self.recording = True

    def process(self, frame: np.ndarray) -> tuple[np.ndarray, dict]:
        hands = self.tracker.process(frame)
        gesture = self.gestures.update(hands)
        action = self.gestures.action()
        self._handle_action(action, frame)

        self.window.update_from_hands(hands, frame.shape)
        self.window.apply_filter(
            frame, lambda roi: apply_filter(self.filter_name, roi))
        frame = self.window.draw(frame)

        fps = self.fps.tick()
        frame = draw_hud(
            frame, fps=fps, filter_name=self.filter_name,
            tracking=bool(hands), gesture=gesture.name,
            confidence=gesture.confidence,
        )
        if self.recording and self._writer:
            self._writer.write(frame)

        meta = {
            "fps": round(fps, 1),
            "filter": self.filter_name,
            "gesture": gesture.name,
            "confidence": gesture.confidence,
            "hands": len(hands),
            "recording": self.recording,
        }
        return frame, meta

    def close(self) -> None:
        self.tracker.close()
        if self._writer:
            self._writer.release()
