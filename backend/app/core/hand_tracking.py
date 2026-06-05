"""MediaPipe hand tracking engine.

Wraps mp.solutions.hands. Returns normalized + pixel landmarks for up to two
hands plus derived features (fingertips, palm center, openness) used by the
gesture classifier. Designed to degrade gracefully if MediaPipe missing so the
rest of the app (and tests) still import.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

try:
    import mediapipe as mp
    _HAS_MP = True
except Exception:  # pragma: no cover - env without mediapipe
    mp = None
    _HAS_MP = False

# MediaPipe landmark indices
WRIST = 0
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20
TIP_IDS = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
PIP_IDS = [3, 6, 10, 14, 18]  # joint below each tip


@dataclass
class Hand:
    label: str                       # "Left" | "Right"
    landmarks_px: np.ndarray         # (21, 2) pixel coords
    landmarks_norm: np.ndarray       # (21, 3) normalized
    fingers_up: list[bool] = field(default_factory=list)
    palm_center: tuple[int, int] = (0, 0)

    @property
    def index_tip(self) -> tuple[int, int]:
        return tuple(self.landmarks_px[INDEX_TIP])

    @property
    def thumb_tip(self) -> tuple[int, int]:
        return tuple(self.landmarks_px[THUMB_TIP])


class HandTracker:
    def __init__(self, max_hands: int = 2, det_conf: float = 0.6,
                 track_conf: float = 0.6) -> None:
        self.available = _HAS_MP
        if not _HAS_MP:
            self._hands = None
            return
        self._hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=det_conf,
            min_tracking_confidence=track_conf,
        )

    def process(self, frame_bgr: np.ndarray) -> list[Hand]:
        if not self.available:
            return []
        import cv2
        h, w = frame_bgr.shape[:2]
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        res = self._hands.process(rgb)
        hands: list[Hand] = []
        if not res.multi_hand_landmarks:
            return hands
        handed = res.multi_handedness or []
        for i, lm in enumerate(res.multi_hand_landmarks):
            norm = np.array([[p.x, p.y, p.z] for p in lm.landmark])
            px = np.column_stack([norm[:, 0] * w, norm[:, 1] * h]).astype(int)
            label = "Right"
            if i < len(handed):
                label = handed[i].classification[0].label
            hand = Hand(
                label=label,
                landmarks_px=px,
                landmarks_norm=norm,
                fingers_up=self._fingers_up(px, label),
                palm_center=tuple(px[[0, 5, 9, 13, 17]].mean(axis=0).astype(int)),
            )
            hands.append(hand)
        return hands

    @staticmethod
    def _fingers_up(px: np.ndarray, label: str) -> list[bool]:
        up: list[bool] = []
        # thumb: compare x (depends on hand side)
        if label == "Right":
            up.append(px[THUMB_TIP][0] < px[THUMB_TIP - 1][0])
        else:
            up.append(px[THUMB_TIP][0] > px[THUMB_TIP - 1][0])
        # other 4: tip above pip (smaller y = higher)
        for tip, pip in zip(TIP_IDS[1:], PIP_IDS[1:]):
            up.append(px[tip][1] < px[pip][1])
        return up

    def close(self) -> None:
        if self._hands is not None:
            self._hands.close()
