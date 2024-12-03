import logging
import re
import shutil
from os import path
from typing import Annotated

import pytesseract
from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pytesseract.pytesseract import TesseractError

ocr_router = APIRouter(
    tags=["OCR"]
)

ASSETS_DIR = path.abspath("static")
logger = logging.getLogger('uvicorn.error')

templates = Jinja2Templates(directory="templates")


@ocr_router.get("/", response_class=HTMLResponse)
def get_image_upload_page(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)


@ocr_router.post('/ocr', response_class=HTMLResponse)
def upload_image(request: Request, image: Annotated[UploadFile, File()]):
    print(f"Received file: {image.filename, image.read}")
    file_path = path.join(ASSETS_DIR, image.filename)
    api_path = f"/static/{image.filename}"

    with open(file_path, "w+b") as buffer:
        if re.search(pattern="(?:jpg|jpeg|png|bmp|webp)", string=image.filename) is not None:
            shutil.copyfileobj(image.file, buffer)
        try:
            text = pytesseract.image_to_string(file_path, lang='eng')

        except TesseractError:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    return templates.TemplateResponse(name="home.html",
                                      request=request,
                                      context={"message": "File uploaded successfully",
                                               "text": text,
                                               "image_path": api_path}, status_code=200)
