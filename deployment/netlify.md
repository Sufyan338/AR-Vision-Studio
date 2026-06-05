# Netlify Deployment (Frontend)

`netlify.toml` (repo root) sets base=`frontend`, build=`npm run build`,
publish=`frontend/dist`, plus SPA redirect so react-router refreshes work.

## Steps
1. Push repo to GitHub.
2. Netlify → Add new site → Import from Git → pick the repo.
3. Build settings are auto-read from `netlify.toml`. Confirm Node 20.
4. **Environment variables** (Site settings → Build & deploy → Environment):
   - `VITE_API_URL = https://<backend-host>`
   - `VITE_WS_URL  = wss://<backend-host>/ws/stream`
5. Deploy. Every push to `main` auto-rebuilds.

## Custom domain
1. Netlify → Domain management → Add custom domain → `arvisionstudio.com`.
2. Point DNS: either Netlify DNS (change nameservers) or add a `CNAME`
   (`www`) + `ALIAS/ANAME` (apex) to Netlify's load balancer.
3. HTTPS cert (Let's Encrypt) provisions automatically — wait for "secured".
4. Force HTTPS so the page can open `wss://` to the backend.
