from contextlib import asynccontextmanager
import sqlite3
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


DB = Path("skillbridge.db")


def conn():
    return sqlite3.connect(DB)


def setup():
    with conn() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                location TEXT,
                skills TEXT
            )
            """
        )

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        c.execute(
            """
            INSERT OR IGNORE INTO profiles
            VALUES (
                1,
                "Aarav Sharma",
                "aarav.sharma@email.com",
                "Bengaluru, Karnataka",
                "Python, SQL, Java, Git"
            )
            """
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup()
    yield


app = FastAPI(
    title="SkillBridge API",
    lifespan=lifespan
)


# Serve frontend static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Home page
@app.get("/")
def home():
    return FileResponse("static/index.html")


# Get profile
@app.get("/api/profile")
def profile():

    with conn() as c:

        row = c.execute(
            """
            SELECT name, email, location, skills
            FROM profiles
            WHERE id = 1
            """
        ).fetchone()

    return dict(
        zip(
            ["name", "email", "location", "skills"],
            row
        )
    )


# Upload resume
@app.post("/api/resumes")
async def upload_resume(
    file: UploadFile = File(...)
):

    with conn() as c:

        c.execute(
            """
            INSERT INTO resumes(filename)
            VALUES (?)
            """,
            (file.filename,)
        )

    return {
        "filename": file.filename,
        "status": "queued"
    }


# Get jobs
@app.get("/api/jobs")
def jobs():

    return [
        {
            "title": "Backend Developer Intern",
            "company": "Nexora Labs",
            "location": "Bengaluru",
            "match": 82
        },
        {
            "title": "Python Developer",
            "company": "BlueHive Systems",
            "location": "Bengaluru",
            "match": 76
        },
        {
            "title": "Software Engineer Intern",
            "company": "OrbitStack",
            "location": "Remote",
            "match": 71
        }
    ]