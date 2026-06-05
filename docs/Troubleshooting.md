# Troubleshooting

**`ImportError: libGL.so.1`** — install system libs:
`apt-get install -y libgl1 libglib2.0-0`.

**MediaPipe won't install** — pin Python 3.11 and use
`opencv-python-headless` (not `opencv-python`) on servers.

**Demo says "backend offline"** — backend not running or `VITE_WS_URL` wrong.
Confirm `GET /health` returns ok; check CORS / mixed-content (HTTPS page can't
open `ws://`; use `wss://` in production).

**Low FPS** — lower capture resolution in `Demo.tsx` (e.g. 480×360), raise the
`setTimeout` interval, or reduce JPEG quality. Heavy filters (cartoon,
pyrMeanShift) cost more; switch filter with Thumb Up/Down.

**Black output image** — first frame can arrive before video is ready; click
Start Camera again after permission is granted.

**Recording file empty** — ensure the container has `ffmpeg` and the
`captures/` volume is writable.
