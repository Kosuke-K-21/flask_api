import pytest
import torch
from flask import Flask, jsonify
from api.calculation import detection


def test_detection(app):
    app.config["LABELS"] = ["cat", "dog"]
    app.config["MODEL"] = torch.nn.Linear(100, 2)

    class MockRequest:
        json = {"image": "dummy"}

    mock_request = MockRequest()

    response = detection(mock_request)

    assert response.status_code == 200
    assert response.json == {"label": "cat", "score": 0.5}
