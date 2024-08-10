from pathlib import Path
import io

import numpy as np
import cv2
import torch
from flask import current_app, jsonify
import boto3

from flask_api.api.postprocess import make_color, make_line, draw_lines, draw_texts
from flask_api.api.preparation import load_image
from flask_api.api.preprocess import image_to_tensor

basedir = Path(__file__).parent.parent


def load_model():
    s3 = boto3.client("s3")

    bucket_name = current_app.config["MODEL_BUCKET_NAME"]
    model_name = current_app.config["MODEL_KEY"]
    buffer = io.BytesIO()
    s3.download_fileobj(bucket_name, model_name, buffer)
    buffer.seek(0)

    model = torch.load(buffer)

    return model


def detection(request):
    dict_results = {}

    labels = current_app.config["LABELS"]

    image, filename = load_image(request)
    image_tensor = image_to_tensor(image)

    try:
        model = load_model()
    except Exception as e:
        return jsonify({"message": str(e)}), 404

    model = model.eval()

    output = model([image_tensor])[0]

    result_image = np.array(image.copy())

    for box, label, score in zip(output["boxes"], output["labels"], output["scores"]):
        if score > 0.6 and labels[label] not in dict_results:
            dict_results[labels[label]] = score
            color = make_color(labels)
            line = make_line(result_image)
            c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))

            draw_lines(c1, c2, result_image, line, color)

            draw_texts(result_image, line, c1, color, labels[label])

            dict_results[labels[label]] = round(100 * score.item())

        dir_image = str(basedir / "data" / "output" / filename)

    cv2.imwrite(dir_image, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))

    return jsonify(dict_results)
