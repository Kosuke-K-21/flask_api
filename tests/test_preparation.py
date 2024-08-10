import pytest

from werkzeug.datastructures import FileStorage
from api.preparation import load_image


def test_load_image(create_image_bytes):
    file_storage = FileStorage(
        stream=create_image_bytes, filename="test.jpg", content_type="image/jpeg"
    )

    class MockRequest:
        files = {"image": file_storage}

    mock_request = MockRequest()

    image, filename = load_image(mock_request, reshaped_size=(256, 256))

    assert filename == "test.jpg"
    assert image.size == (256, 256)
    assert image.mode == "RGB"
