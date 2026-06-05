# Hugging Face Spaces Deployment (Backend)

Uses the **Docker** SDK. The root `Dockerfile` + `app.py` serve FastAPI on 7860.

## Steps
1. Create a Space → SDK: **Docker** → Blank.
2. Add the Space as a git remote and push the repo root:
   ```bash
   git remote add space https://huggingface.co/spaces/<user>/ar-vision-studio
   git push space main
   ```
3. The Space builds the root `Dockerfile`, runs `python app.py`, exposes 7860.
4. Backend URL: `https://<user>-ar-vision-studio.hf.space`
   WebSocket: `wss://<user>-ar-vision-studio.hf.space/ws/stream`

## Space README header
Add this YAML front-matter to a `README.md` pushed to the Space:
```yaml
---
title: AR Vision Studio
emoji: 🕶️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
---
```

## Notes
- Free CPU tier is enough (no GPU needed).
- Increase Space sleep timeout to keep the demo warm.
- CORS is `*` by default; restrict via an env-driven origin list for production.

### Gradio alternative
Prefer a self-contained Space with no separate frontend? Use
`deployment/app_gradio.py` (uploads an image, returns a filtered result). Set
the Space `app_file: deployment/app_gradio.py`, sdk `gradio`.
