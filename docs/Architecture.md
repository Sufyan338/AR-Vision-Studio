# Architecture

## High-level

```
┌──────────────┐   webcam frames (JPEG)   ┌──────────────────────────────┐
│   Browser    │ ───────────────────────▶ │  FastAPI  /ws/stream         │
│ React + Vite │      WebSocket            │                              │
│  getUserMedia│ ◀─────────────────────── │  Pipeline (per connection)   │
└──────────────┘   processed frame + meta  └──────────────────────────────┘
                                                     │
                          ┌──────────────┬───────────┴──────────┬───────────┐
                          ▼              ▼                      ▼           ▼
                    HandTracker     GestureEngine           ARWindow     Filters
                    (MediaPipe)     (debounced FSM)        (EMA smooth)  (OpenCV)
                                                     │
                                                     ▼
                                                  HUD overlay
```

## Components

- **HandTracker** (`core/hand_tracking.py`) — MediaPipe Hands → up to 2 `Hand`
  objects with pixel/normalized landmarks, fingertip flags, palm center.
- **GestureEngine** (`core/gestures.py`) — pure FSM. Classifies per-frame
  gesture, debounces over N frames, emits an action only when stable
  (confidence ≥ 0.99).
- **ARWindow** (`core/ar_window.py`) — builds a rectangle from two index tips,
  EMA-smooths it, supports freeze, draws neon border + corner anchors, applies a
  filter only inside the ROI.
- **Filters** (`filters/filters.py`) — 12 pure `np.ndarray → np.ndarray`
  functions in a name→fn registry.
- **HUD** (`core/hud.py`) — FPS meter + Iron-Man overlay (FPS, filter, tracking,
  gesture, confidence, CPU via psutil).
- **Pipeline** (`core/pipeline.py`) — per-session orchestration + screenshot /
  recording state.

## Data flow (per frame)

`frame → tracker → gestures → action handler → ar_window update → filter ROI →
draw window → HUD → encode → send back (+ JSON meta)`

## Deployment view

- Frontend → **Netlify** (static SPA).
- Backend → **Hugging Face Spaces** (Docker SDK) or any container host.
- Frontend `VITE_WS_URL` points at the deployed backend WebSocket.

## Why browser-captures-camera

HF Spaces / cloud containers have no webcam and are headless. Capturing in the
browser and streaming frames keeps the backend portable and GPU-free.
