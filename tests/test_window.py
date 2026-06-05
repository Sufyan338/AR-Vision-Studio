import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from app.core.ar_window import Rect


def test_rect_validity():
    assert Rect(0, 0, 100, 100).valid
    assert not Rect(0, 0, 5, 5).valid


def test_rect_clamp_orders_and_bounds():
    r = Rect(120, 90, 10, 5).clamp(100, 80)
    assert r.x1 <= r.x2 and r.y1 <= r.y2
    assert r.x2 <= 100 and r.y2 <= 80
