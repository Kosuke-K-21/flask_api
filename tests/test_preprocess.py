import pytest
import torch
from api.preprocess import image_to_tensor


def test_image_to_tensor(create_image):
    image_tensor = image_to_tensor(create_image)

    assert isinstance(image_tensor, torch.Tensor)
    assert image_tensor.max().item() == 1.0
    assert image_tensor.min().item() == 0.0
