from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path


app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")


@app.get("/static/brain.js")
async def brain_js():
    return FileResponse(BASE_DIR / "brain.js", media_type="application/javascript")


@app.get("/static/style.css")
async def style_css():
    return FileResponse(BASE_DIR / "style.css", media_type="text/css")

@app.get("/")
async def landing():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/complete-fit")
async def complete_fit():
    return FileResponse(BASE_DIR / "complete-fit.html")

@app.get("/occasion")
async def occasion():
    return FileResponse(BASE_DIR / "occasion.html")
