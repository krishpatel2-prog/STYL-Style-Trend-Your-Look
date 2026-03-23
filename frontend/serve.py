from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

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