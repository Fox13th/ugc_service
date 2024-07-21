from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from flask import Flask, request
from flask_jwt_extended import JWTManager
import sentry_sdk

from core import config
from core.logger import logger
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


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        logger.error('request id is requred')
        raise RuntimeError('request id is requred')


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
