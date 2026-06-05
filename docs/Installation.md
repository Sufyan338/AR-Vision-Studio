# Installation

## Prerequisites
- Python 3.11+
- Node.js 20+
- A webcam + a browser that supports `getUserMedia` (Chrome/Edge/Firefox)
- Linux system libs for OpenCV/MediaPipe: `libgl1 libglib2.0-0` (Debian/Ubuntu)

## Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Frontend
```bash
cd frontend
cp .env.example .env        # set VITE_WS_URL if backend not on localhost:8000
npm install
npm run dev
```
Open http://localhost:5173 → **Demo** → **Start Camera**.

## Docker (full stack)
```bash
docker compose -f docker/docker-compose.yml up --build
# frontend :5173  backend :8000
```
