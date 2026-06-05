# Research Notes

## Gesture classification
Rule-based on MediaPipe 21-landmark finger-extension heuristics + a thumb–index
distance pinch test. Chosen over an ML classifier for zero training data, full
explainability, and CPU speed. A debounce buffer (N identical frames) removes
flicker before an action fires — trades ~N/fps latency for stability.

## AR window stabilization
Exponential moving average on corner coordinates (`smooth=0.4`). Lower = smoother
but laggier. Future: Kalman filter per corner for jitter + velocity prediction.

## Performance
Filters are vectorized NumPy/OpenCV. Targets: 30–60 FPS, <300 MB RAM, CPU-only.
Streaming JPEG over WebSocket trades a little bandwidth for backend portability.

## Future direction
- Replace heuristics with a tiny MLP on landmark vectors for custom gestures.
- MediaPipe Selfie Segmentation for face/background-scoped filters.
- WebRTC/WASM path to move inference fully client-side and cut round-trip latency.
