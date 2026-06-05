"""Unit + gesture-accuracy tests (no camera/cv2 needed)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.gestures import (
    GestureEngine, classify_hand, detect_cross_hands, GESTURE_ACTIONS)


class FakeHand:
    def __init__(self, fingers, label="Right", palm=(0, 0)):
        self.fingers_up = fingers
        self.label = label
        self.palm_center = palm
        self.landmarks_px = None


def test_open_palm_fires_create_window():
    e = GestureEngine(hold_frames=3)
    for _ in range(3):
        st = e.update([FakeHand([True] * 5)])
    assert st.name == "open_palm"
    assert e.action() == "create_window"


def test_fist_freezes():
    e = GestureEngine(hold_frames=3)
    for _ in range(3):
        e.update([FakeHand([False] * 5)])
    assert e.action() == "freeze_window"


def test_debounce_blocks_unstable():
    e = GestureEngine(hold_frames=4)
    e.update([FakeHand([True] * 5)])
    e.update([FakeHand([False] * 5)])
    st = e.update([FakeHand([True] * 5)])
    assert st.confidence < 0.99
    assert e.action() is None


def test_classify_victory():
    assert classify_hand([False, True, True, False, False], None) == "victory"


def test_classify_three_fingers():
    assert classify_hand([False, True, True, True, False], None) == "three_fingers"


def test_cross_hands():
    left = FakeHand([True] * 5, label="Left", palm=(400, 200))
    right = FakeHand([True] * 5, label="Right", palm=(100, 200))
    assert detect_cross_hands([left, right]) is True


def test_action_map_complete():
    for g in ["open_palm", "fist", "thumb_up", "thumb_down", "victory",
              "pinch", "cross_hands", "three_fingers", "ok_sign"]:
        assert g in GESTURE_ACTIONS


# gesture accuracy: synthetic labelled set -> expect >= 90%
ACCURACY_SET = [
    ([True, True, True, True, True], "open_palm"),
    ([False, False, False, False, False], "fist"),
    ([False, True, True, False, False], "victory"),
    ([False, True, True, True, False], "three_fingers"),
]


def test_gesture_accuracy_threshold():
    correct = sum(classify_hand(f, None) == lbl for f, lbl in ACCURACY_SET)
    assert correct / len(ACCURACY_SET) >= 0.9
