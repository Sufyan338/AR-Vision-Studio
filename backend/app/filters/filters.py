"""Real-time visual filters (OpenCV + NumPy).

Every filter takes a BGR uint8 frame and returns a BGR uint8 frame of the
same shape. Filters are pure functions so they compose and test easily.
Only the region inside the AR window gets filtered (see ar_window.apply_in_window).
"""

from __future__ import annotations

import cv2
import numpy as np


# --- individual effects ----------------------------------------------------

def f_glow(img: np.ndarray) -> np.ndarray:
    blur = cv2.GaussianBlur(img, (0, 0), sigmaX=9)
    return cv2.addWeighted(img, 1.0, blur, 0.6, 0)


def f_thermal(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.applyColorMap(gray, cv2.COLORMAP_JET)


def f_edge(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 160)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


def f_anime(img: np.ndarray) -> np.ndarray:
    color = cv2.bilateralFilter(img, 9, 200, 200)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
    )
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return cv2.bitwise_and(color, edges)


def f_pencil(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


def f_cyberpunk(img: np.ndarray) -> np.ndarray:
    out = img.astype(np.float32)
    out[..., 0] *= 1.4   # boost blue
    out[..., 2] *= 1.2   # boost red
    out = np.clip(out, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.5, 0, 255)  # saturation pop
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def f_pixel(img: np.ndarray, blocks: int = 48) -> np.ndarray:
    h, w = img.shape[:2]
    small = cv2.resize(img, (blocks, max(1, blocks * h // w)),
                       interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)


def f_rgb_split(img: np.ndarray, shift: int = 6) -> np.ndarray:
    b, g, r = cv2.split(img)
    r = np.roll(r, shift, axis=1)
    b = np.roll(b, -shift, axis=1)
    return cv2.merge([b, g, r])


def f_cartoon(img: np.ndarray) -> np.ndarray:
    color = cv2.pyrMeanShiftFiltering(img, 15, 40)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(
        cv2.medianBlur(gray, 7), 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 5
    )
    return cv2.bitwise_and(color, color, mask=edges)


def f_night_vision(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    green = np.zeros_like(img)
    green[..., 1] = gray            # everything in green channel
    noise = np.random.randint(0, 30, gray.shape, dtype=np.uint8)
    green[..., 1] = cv2.add(green[..., 1], noise)
    return green


def f_matrix(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)[1]
    out = np.zeros_like(img)
    out[..., 1] = cv2.bitwise_and(gray, thresh)
    return out


def f_hologram(img: np.ndarray) -> np.ndarray:
    out = f_rgb_split(img, shift=4)
    # scanlines
    out[::3, :, :] = (out[::3, :, :] * 0.6).astype(np.uint8)
    tint = np.full_like(out, (255, 180, 0))  # cyan-ish in BGR
    return cv2.addWeighted(out, 0.85, tint, 0.15, 0)


# --- registry --------------------------------------------------------------

FILTERS: dict[str, callable] = {
    "glow": f_glow,
    "thermal": f_thermal,
    "edge": f_edge,
    "anime": f_anime,
    "pencil": f_pencil,
    "cyberpunk": f_cyberpunk,
    "pixel": f_pixel,
    "rgb_split": f_rgb_split,
    "cartoon": f_cartoon,
    "night_vision": f_night_vision,
    "matrix": f_matrix,
    "hologram": f_hologram,
}

FILTER_NAMES: list[str] = list(FILTERS.keys())


def apply_filter(name: str, img: np.ndarray) -> np.ndarray:
    fn = FILTERS.get(name)
    if fn is None:
        return img
    return fn(img)
