"""Perf/stress smoke — skipped if cv2 missing. Targets: filter < 50ms @ VGA."""
import sys, os, time
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
cv2 = pytest.importorskip("cv2")
import numpy as np
from app.filters.filters import FILTER_NAMES, apply_filter


@pytest.mark.parametrize("name", FILTER_NAMES)
def test_filter_latency(name):
    img = (np.random.rand(480, 640, 3) * 255).astype(np.uint8)
    t = time.perf_counter()
    apply_filter(name, img)
    assert (time.perf_counter() - t) < 0.2  # generous CI bound


def test_stress_many_frames():
    img = (np.random.rand(240, 320, 3) * 255).astype(np.uint8)
    for _ in range(200):
        apply_filter("glow", img)
