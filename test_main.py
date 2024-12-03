import os

import numpy as np
from PIL import Image
from fastapi.testclient import TestClient

from main import app
from router import ocr_router

app.include_router(ocr_router)

client = TestClient(app)


def _gen_random_image(ran_img):
    arr = np.random.randint(0, 256, (250, 250, 3), dtype=np.uint8)

    im = Image.fromarray(arr)
    im.save(ran_img)


def _del_image(ran_img):
    if os.path.exists(ran_img):
        os.remove(ran_img)


def test_get_image_upload_page():
    response = client.get("/")
    assert response.status_code == 200


def test_upload_image():
    ran_img = "test_image.jpeg"
    _gen_random_image(ran_img)

    with open(ran_img, 'rb') as img_file:
        _file = {'image': (ran_img, img_file, 'image/jpeg')}

        response = client.post(
            "/ocr",
            files=_file
        )

    _del_image(ran_img)

    assert response.status_code == 200
