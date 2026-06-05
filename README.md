<div align="center">

# 🕶️ AR Vision Studio

**Gesture-controlled augmented reality. Draw a floating window with your hands; everything inside gets real-time AI visual effects.**

![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![React](https://img.shields.io/badge/React-18-61dafb)
![MediaPipe](https://img.shields.io/badge/MediaPipe-hands-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/your-user/AR-Vision-Studio/actions/workflows/ci.yml/badge.svg)

[Live Demo](#) · [Hugging Face Space](#) · [Docs](docs/)

</div>

---

## ✨ What it does

Hold up two hands → your index fingertips become opposite corners of a floating
**AR window**. Whatever is inside that window gets a live filter (glow, thermal,
anime, cyberpunk, matrix…). The rest of the camera feed stays normal. Control
everything with gestures — no keyboard, no mouse.

> **Architecture note:** the browser captures the webcam and streams JPEG frames
> over WebSocket to a FastAPI backend that runs MediaPipe + OpenCV, then streams
> processed frames back. The backend stays **headless** → runs on Hugging Face
> Spaces and any CPU-only container. No GPU required.

## 🖐️ Gesture controls

| Gesture | Action | Gesture | Action |
|---|---|---|---|
| Open Palm | Create window | Pinch | Resize window |
| Closed Fist | Freeze window | Victory | Filter selection |
| Thumb Up | Next filter | Cross Hands | Exit mode |
| Thumb Down | Prev filter | Three Fingers | Screenshot |
| OK Sign | Start/stop recording | | |

## 🎨 Filters (12)

`glow` · `thermal` · `edge` · `anime` · `pencil` · `cyberpunk` · `pixel` ·
`rgb_split` · `cartoon` · `night_vision` · `matrix` · `hologram`

## 🧱 Tech stack

**Backend** Python 3.11 · FastAPI · OpenCV · MediaPipe · NumPy · Uvicorn
**Frontend** React · Vite · TypeScript · TailwindCSS · Framer Motion
**Deploy** Docker · Hugging Face Spaces · Netlify · GitHub Actions

## 🚀 Quick start

```bash
# backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# frontend (new terminal)
cd frontend
cp .env.example .env
npm install
npm run dev   # http://localhost:5173 → /demo
```

Or full stack via Docker:

```bash
docker compose -f docker/docker-compose.yml up --build
```

## 📁 Structure

```
AR-Vision-Studio/
├── backend/          FastAPI + CV core
│   └── app/
│       ├── core/     hand_tracking · gestures · ar_window · hud · pipeline
│       ├── filters/  12 OpenCV filters
│       └── main.py   REST + WebSocket
├── frontend/         React + Vite + Tailwind (Home · Demo · Docs)
├── docs/             Architecture · API · Installation · Deployment · ...
├── docker/           Dockerfiles + compose
├── deployment/       HF Spaces + Netlify guides
├── tests/            unit · perf · gesture-accuracy
├── .github/          CI workflow
├── app.py            Hugging Face Spaces entrypoint
├── Dockerfile        HF Spaces image
└── netlify.toml      Netlify frontend config
```

## 🧪 Tests

```bash
pip install -r backend/requirements-dev.txt
pytest -q
```

Covers gesture classification, debounce, AR-window geometry, filter shape/dtype,
latency, stress, and a gesture-accuracy threshold.

## 🗺️ Roadmap

- [ ] YOLO object-detection mode (filter only detected objects)
- [ ] Face/eyes/hair/background segmentation filters
- [ ] Voice commands (Web Speech API)
- [ ] AI background removal / virtual green screen
- [ ] AR stickers + 3D HUD elements
- [ ] Custom filter creator UI
- [ ] Multi-user mode · cloud sync · accounts · filter marketplace

## 🤝 Contributing

See [docs/Contributing.md](docs/Contributing.md). PRs welcome.

## 📄 License

MIT — see [LICENSE](LICENSE).
