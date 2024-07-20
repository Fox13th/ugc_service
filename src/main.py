from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from flask import Flask
from flask_jwt_extended import JWTManager
import sentry_sdk

from core import config
from api.v1.statistics import router


settings = config.get_settings()

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Flask(settings.project_name)

app.debug = settings.debug

app.secret_key = settings.secret_key

app.config['JWT_SECRET_KEY'] = settings.jwt_secret
jwt = JWTManager(app)

app.register_blueprint(router)

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
