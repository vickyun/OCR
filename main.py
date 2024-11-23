import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from router import ocr_router

app = FastAPI()

app.include_router(ocr_router)

upload_dir = "static"
if not os.path.exists(upload_dir):
    os.mkdir(upload_dir)

app.mount("/static", StaticFiles(directory=upload_dir), name="static")
