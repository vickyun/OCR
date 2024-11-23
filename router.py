import logging
import shutil
from os import path

import pytesseract
from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pytesseract.pytesseract import TesseractError

ASSETS_DIR = path.abspath("static")
ocr_router = APIRouter(
    tags=["OCR"]
)
logger = logging.getLogger('uvicorn.error')
templates = Jinja2Templates(directory="templates")
print(ASSETS_DIR)


@ocr_router.get("/", response_class=HTMLResponse)
def get_image_upload_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@ocr_router.post('/ocr', response_class=HTMLResponse)
def ocr(request: Request, image: UploadFile = File(...)):
    filePath = path.join(ASSETS_DIR, image.filename)
    api_path = f"/static/{image.filename}"
    with open(filePath, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
        try:
            text = pytesseract.image_to_string(filePath, lang='eng')

        except TesseractError:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    return templates.TemplateResponse("home.html", {"request": request, "message": "File uploaded successfully",
                                                    "text": text,
                                                    "image_path": api_path}, status_code=200)
