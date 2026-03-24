from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="assets"), name="static")

@app.get("/")
async def landing():
    return FileResponse("index.html")

@app.get("/complete-fit")
async def complete_fit():
    return FileResponse("complete-fit.html")

@app.get("/occasion")
async def occasion():
    return FileResponse("occasion.html")