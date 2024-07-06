from flask import Flask

from core import config
from api.v1.statistics import router

settings = config.get_settings()

app = Flask(settings.project_name)

app.debug = settings.debug

app.secret_key = settings.secret_key

app.register_blueprint(router)
