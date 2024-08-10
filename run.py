import os

from flask import Flask

from flask_api.api import api
from flask_api.api.config import config

config_name = os.environ.get("CONFIG", "local")

app = Flask(__name__)
app.config.from_object(config[config_name])

app.register_blueprint(api)
