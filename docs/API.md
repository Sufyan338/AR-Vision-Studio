# API Reference

Base URL: `http://localhost:8000`

## `GET /health`
→ `{ "status": "ok" }`

## `GET /api/filters`
→ `{ "filters": ["glow", "thermal", ...] }`

## `POST /api/process`
Single stateless frame (demo / no gesture history).
```json
// request
{ "image": "data:image/jpeg;base64,..." }
// response
{ "image": "data:image/jpeg;base64,...", "meta": { ... } }
```

## `WS /ws/stream`
Realtime. One `Pipeline` per connection (keeps gesture history + window state).

- **Client → server:** binary message = raw JPEG bytes of a webcam frame.
- **Server → client:** alternating messages —
  - binary: processed JPEG frame
  - text: JSON meta `{ fps, filter, gesture, confidence, hands, recording }`

### Meta fields
| field | type | meaning |
|---|---|---|
| fps | number | smoothed server FPS |
| filter | string | active filter name |
| gesture | string | last classified gesture |
| confidence | number | gesture stability 0–1 |
| hands | number | hands detected this frame |
| recording | bool | MP4 recording active |
