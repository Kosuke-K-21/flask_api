from pathlib import Path
from werkzeug.utils import secure_filename

import PIL
import PIL.Image


def load_image(request, reshaped_size=(256, 256)):
    file = request.files["image"]
    filename = secure_filename(file.filename)

    image_obj = PIL.Image.open(file.stream).convert("RGB")

    image = image_obj.resize(reshaped_size)
    return image, filename
