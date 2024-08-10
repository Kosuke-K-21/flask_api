import pytest
from flask import Flask
from io import BytesIO
from PIL import Image


@pytest.fixture
def create_image():
    # テスト用のイメージを生成
    img = Image.new("RGB", (100, 100), color="red")
    return img


@pytest.fixture
def create_image_bytes(create_image):
    byte_io = BytesIO()
    img = create_image
    img.save(byte_io, "JPEG")
    byte_io.seek(0)
    return byte_io


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["LABELS"] = ["cat", "dog"]
    return app


@pytest.fixture
def client(app):
    return app.test_client()
