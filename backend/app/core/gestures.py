"""Gesture recognition.

Maps Hand finger-state (and two-hand relations) to named gestures. Uses a small
debounce so a gesture must hold N frames before firing an action, killing
flicker. Pure logic; no OpenCV/MediaPipe import needed -> trivially testable.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass

# gesture -> action mapping from the spec
GESTURE_ACTIONS = {
    "open_palm": "create_window",
    "fist": "freeze_window",
    "thumb_up": "next_filter",
    "thumb_down": "prev_filter",
    "victory": "filter_select",
    "pinch": "resize_window",
    "cross_hands": "exit_mode",
    "three_fingers": "screenshot",
    "ok_sign": "toggle_record",
}


def _dist(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def classify_hand(fingers_up: list[bool], landmarks_px) -> str:
    """Single-hand gesture from finger booleans [thumb,index,mid,ring,pinky]."""
    thumb, index, mid, ring, pinky = fingers_up
    n = sum(fingers_up)

    # pinch: thumb tip close to index tip
    if landmarks_px is not None:
        if _dist(landmarks_px[4], landmarks_px[8]) < 0.06 * \
                max(1, _dist(landmarks_px[0], landmarks_px[9])) * 10:
            # scale-invariant-ish pinch check
            if _dist(landmarks_px[4], landmarks_px[8]) < 40:
                return "pinch"

    if n == 0:
        return "fist"
    if n == 5:
        return "open_palm"
    if index and mid and not ring and not pinky and not thumb:
        return "victory"
    if thumb and not any([index, mid, ring, pinky]):
        # up vs down decided by caller via orientation; default thumb_up
        return "thumb_up"
    if index and mid and ring and not pinky and not thumb:
        return "three_fingers"
    # ok sign: thumb+index circle, others up
    if landmarks_px is not None and mid and ring and pinky:
        if _dist(landmarks_px[4], landmarks_px[8]) < 45:
            return "ok_sign"
    return "none"


def thumb_direction(landmarks_px) -> str:
    """Decide thumb_up vs thumb_down by thumb tip vs wrist y."""
    if landmarks_px is None:
        return "thumb_up"
    return "thumb_up" if landmarks_px[4][1] < landmarks_px[0][1] else "thumb_down"


def detect_cross_hands(hands) -> bool:
    """Two hands crossed: right hand's center left of left hand's center."""
    if len(hands) < 2:
        return False
    a, b = hands[0], hands[1]
    if a.label == b.label:
        return False
    left = a if a.label == "Left" else b
    right = b if a.label == "Left" else a
    return right.palm_center[0] < left.palm_center[0]


@dataclass
class GestureState:
    name: str = "none"
    confidence: float = 0.0


class GestureEngine:
    def __init__(self, hold_frames: int = 4) -> None:
        self.hold = hold_frames
        self._hist: deque[str] = deque(maxlen=hold_frames)
        self.current = GestureState()

    def update(self, hands) -> GestureState:
        g = "none"
        if detect_cross_hands(hands):
            g = "cross_hands"
        elif hands:
            h = hands[0]
            g = classify_hand(h.fingers_up, h.landmarks_px)
            if g == "thumb_up":
                g = thumb_direction(h.landmarks_px)
        self._hist.append(g)
        # stable only if same gesture fills the buffer
        if len(self._hist) == self.hold and len(set(self._hist)) == 1:
            conf = 1.0
        else:
            conf = self._hist.count(g) / max(1, len(self._hist))
        self.current = GestureState(name=g, confidence=round(conf, 2))
        return self.current

    def action(self) -> str | None:
        if self.current.confidence >= 0.99:
            return GESTURE_ACTIONS.get(self.current.name)
        return None
