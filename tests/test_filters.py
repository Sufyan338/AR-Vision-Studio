"""Filter tests — skipped automatically if OpenCV not installed."""
import sys, os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

cv2 = pytest.importorskip("cv2")
import numpy as np
from app.filters.filters import FILTER_NAMES, apply_filter


@pytest.mark.parametrize("name", FILTER_NAMES)
def test_filter_shape_and_dtype(name):
    img = (np.random.rand(120, 160, 3) * 255).astype(np.uint8)
    out = apply_filter(name, img)
    assert out.shape == img.shape
    assert out.dtype == np.uint8
