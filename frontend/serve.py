from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def landing():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/index.html")
async def index_page():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/occasion.html")
async def occasion_page():
    return FileResponse(BASE_DIR / "occasion.html")


@app.get("/complete-fit.html")
async def complete_fit_page():
    return FileResponse(BASE_DIR / "complete-fit.html")


@app.get("/occasion")
async def occasion_alias():
    return FileResponse(BASE_DIR / "occasion.html")


@app.get("/complete-fit")
async def complete_fit_alias():
    return FileResponse(BASE_DIR / "complete-fit.html")


@app.get("/brain.js")
async def brain_js():
    return FileResponse(BASE_DIR / "brain.js", media_type="application/javascript")


@app.get("/style.css")
async def style_css():
    return FileResponse(BASE_DIR / "style.css", media_type="text/css")
