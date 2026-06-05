"""AR window: a floating rectangle defined by two hands, with smoothing,
neon border + HUD corners, and masked filter application."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class Rect:
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0

    @property
    def valid(self) -> bool:
        return self.x2 - self.x1 > 10 and self.y2 - self.y1 > 10

    def clamp(self, w: int, h: int) -> "Rect":
        return Rect(
            max(0, min(self.x1, self.x2)),
            max(0, min(self.y1, self.y2)),
            min(w, max(self.x1, self.x2)),
            min(h, max(self.y1, self.y2)),
        )


class ARWindow:
    def __init__(self, smooth: float = 0.4) -> None:
        self.rect = Rect()
        self.frozen = False
        self.smooth = smooth  # EMA factor, lower = smoother/laggier

    def update_from_hands(self, hands, frame_shape) -> None:
        """Build rect from index tips of two hands (opposite corners)."""
        if self.frozen or len(hands) < 2:
            return
        h, w = frame_shape[:2]
        p1 = hands[0].index_tip
        p2 = hands[1].index_tip
        target = Rect(p1[0], p1[1], p2[0], p2[1]).clamp(w, h)
        if not self.rect.valid:
            self.rect = target
            return
        s = self.smooth
        self.rect = Rect(
            int(self.rect.x1 + s * (target.x1 - self.rect.x1)),
            int(self.rect.y1 + s * (target.y1 - self.rect.y1)),
            int(self.rect.x2 + s * (target.x2 - self.rect.x2)),
            int(self.rect.y2 + s * (target.y2 - self.rect.y2)),
        )

    def freeze(self, on: bool = True) -> None:
        self.frozen = on

    def reset(self) -> None:
        self.rect = Rect()
        self.frozen = False

    def apply_filter(self, frame: np.ndarray, filter_fn) -> np.ndarray:
        r = self.rect
        if not r.valid:
            return frame
        roi = frame[r.y1:r.y2, r.x1:r.x2]
        if roi.size == 0:
            return frame
        frame[r.y1:r.y2, r.x1:r.x2] = filter_fn(roi)
        return frame

    def draw(self, frame: np.ndarray, color=(255, 90, 0)) -> np.ndarray:
        r = self.rect
        if not r.valid:
            return frame
        # glow border (draw thick faint then thin bright)
        cv2.rectangle(frame, (r.x1, r.y1), (r.x2, r.y2), color, 6)
        cv2.rectangle(frame, (r.x1, r.y1), (r.x2, r.y2), (255, 255, 255), 1)
        self._corners(frame, r, color)
        return frame

    @staticmethod
    def _corners(frame, r: Rect, color, L: int = 22) -> None:
        for (cx, cy, dx, dy) in [
            (r.x1, r.y1, 1, 1), (r.x2, r.y1, -1, 1),
            (r.x1, r.y2, 1, -1), (r.x2, r.y2, -1, -1),
        ]:
            cv2.line(frame, (cx, cy), (cx + dx * L, cy), color, 3)
            cv2.line(frame, (cx, cy), (cx, cy + dy * L), color, 3)
