"""SkillBridge API shared by local FastAPI and Vercel serverless deployments."""
from contextlib import asynccontextmanager
from pathlib import Path
import os
import sqlite3

from fastapi import FastAPI, File, UploadFile

# Vercel's deployed filesystem is read-only, but /tmp is writable for a function
# invocation. Use the project directory during local development.
DB = Path("/tmp/skillbridge.db") if os.getenv("VERCEL") else Path("skillbridge.db")


def connection() -> sqlite3.Connection:
    return sqlite3.connect(DB)


def setup_database() -> None:
    with connection() as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS profiles "
            "(id INTEGER PRIMARY KEY, name TEXT, email TEXT, location TEXT, skills TEXT)"
        )
        db.execute(
            "CREATE TABLE IF NOT EXISTS resumes "
            "(id INTEGER PRIMARY KEY, filename TEXT, uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )
        db.execute(
            "INSERT OR IGNORE INTO profiles VALUES "
            "(1, 'Aarav Sharma', 'aarav.sharma@email.com', "
            "'Bengaluru, Karnataka', 'Python, SQL, Java, Git')"
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_database()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="SkillBridge API", lifespan=lifespan)

    @app.get("/api/profile")
    def profile():
        with connection() as db:
            row = db.execute(
                "SELECT name, email, location, skills FROM profiles WHERE id = 1"
            ).fetchone()
        return dict(zip(["name", "email", "location", "skills"], row))

    @app.post("/api/resumes")
    async def upload_resume(file: UploadFile = File(...)):
        with connection() as db:
            db.execute("INSERT INTO resumes(filename) VALUES (?)", (file.filename,))
        return {"filename": file.filename, "status": "queued"}

    @app.get("/api/jobs")
    def jobs():
        return [
            {"title": "Backend Developer Intern", "company": "Nexora Labs", "location": "Bengaluru", "match": 82},
            {"title": "Python Developer", "company": "BlueHive Systems", "location": "Bengaluru", "match": 76},
            {"title": "Software Engineer Intern", "company": "OrbitStack", "location": "Remote", "match": 71},
        ]

    return app
