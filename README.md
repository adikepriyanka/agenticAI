# SkillBridge

SkillBridge is a static-first career-platform demo with an optional FastAPI API. The frontend does **not** depend on a framework build step: any static host can serve `index.html` and the `static/` folder.

## Deploy anywhere

### Static hosting (GitHub Pages, Netlify, Cloudflare Pages, S3, shared hosting)

Publish the repository root. The entrypoint is `index.html`, and its asset URLs are relative (`./static/...`), so it also works when hosted under a project subpath. Resume processing continues in demo mode if the optional API is not available.

### Vercel

Import the repository, choose **Other**, and leave **Build Command** and **Output Directory** empty. Vercel serves the root `index.html`; `vercel.json` routes all `/api/*` calls to the FastAPI serverless function in `api/index.py`.

### Render, Railway, Fly.io, Docker, or another container host

The included `Dockerfile` launches the complete app (frontend + API). Configure the service with a `PORT` environment variable; the container command already uses it.

```bash
docker build -t skillbridge .
docker run --rm -p 8000:8000 -e PORT=8000 skillbridge
```

### Local development

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open `http://localhost:8000`. The health endpoint is `GET /health`; API examples are `GET /api/profile`, `GET /api/jobs`, and `POST /api/resumes`.

## Database note

SQLite is for the demo only. On Vercel the database uses `/tmp/skillbridge.db`, which is ephemeral. Use Postgres or another managed database before production use.
