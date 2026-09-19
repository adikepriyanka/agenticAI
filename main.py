"""Local development entrypoint: `uvicorn main:app --reload`."""
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.app import create_app

app = create_app()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("index.html")
