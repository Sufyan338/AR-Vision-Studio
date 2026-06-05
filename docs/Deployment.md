# Deployment

Two pieces deploy separately: **frontend → Netlify**, **backend → Hugging Face
Spaces** (or any container host). Point the frontend at the backend WebSocket.

## 1. Backend → Hugging Face Spaces (Docker SDK)
See [deployment/huggingface.md](../deployment/huggingface.md).

## 2. Frontend → Netlify
See [deployment/netlify.md](../deployment/netlify.md).

## 3. Wire them together
Set Netlify env var `VITE_WS_URL=wss://<your-space>.hf.space/ws/stream`.
HTTPS pages must use `wss://` (secure WebSocket) — HF Spaces serve HTTPS, so this
works out of the box.

## CI/CD
`.github/workflows/ci.yml` runs backend tests, frontend build, and a backend
Docker build on every push/PR to `main`. Add deploy steps or connect Netlify's
Git integration + HF Spaces Git remote for auto-deploy.

```
push → GitHub Actions ──┬─ pytest (backend)
                        ├─ npm build (frontend)
                        └─ docker build (backend)
Netlify  ◀── git push (frontend auto-build)
HF Space ◀── git push to space remote (backend auto-build)
```
