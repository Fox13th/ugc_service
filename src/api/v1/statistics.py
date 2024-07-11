from http import HTTPStatus

import sentry_sdk
from flask import request, jsonify, Blueprint
from sentry_sdk import capture_exception

from core import config
from schemas.events import Event
from service.kafka_s import send_to_kafka

settings = config.get_settings()

router = Blueprint('statistics', __name__, url_prefix='/api/v1/statistics')

sentry_sdk.init(
    dsn="https://0687df3d7eef5995ed6b59377692711f@o4507584677478400.ingest.de.sentry.io/4507584685342800",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@router.route('/send', methods=['POST'])
def get_data():
    try:
        input_data = Event(**request.get_json(force=True))

        send_to_kafka(
            event_data=input_data.event_data
        )

        status = HTTPStatus.OK

    except Exception as error:
        capture_exception(error)

        status = HTTPStatus.BAD_REQUEST

    return jsonify({'status': status.phrase}), status
