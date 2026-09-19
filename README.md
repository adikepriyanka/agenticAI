# SkillBridge

## Deploy to Vercel

This repository is ready to deploy as a Vercel project without a custom build command:

1. Import the repository in Vercel.
2. Select **Other** as the framework preset and leave **Build Command** and **Output Directory** empty.
3. Deploy. `index.html` at the repository root is the frontend entrypoint, `/static` contains its assets, and `api/index.py` is the serverless FastAPI entrypoint.

The browser app is available at `/`. Backend examples are available at `/api/profile`, `/api/jobs`, and `POST /api/resumes`.

For local development, install the dependencies and run:

```bash
python -m uvicorn main:app --reload
```

> The serverless SQLite database uses `/tmp` on Vercel, which is ephemeral. Replace it with Postgres or another managed database before production use.
