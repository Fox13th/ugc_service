import json
from http import HTTPStatus

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sentry_sdk import capture_exception

from core import config
from core.logger import logger
from schemas.events import Event
from service.kafka_s import send_to_kafka

settings = config.get_settings()

router = Blueprint('statistics', __name__, url_prefix='/api/v1/statistics')


@router.route('/send', methods=['POST'])
@jwt_required()
def get_data():
    try:
        current_user = get_jwt_identity()

        input_data = Event(**request.get_json(force=True))
        event_data = {**json.loads(current_user), **input_data.event_data}

        send_to_kafka(
            event_data=event_data
        )

        status = HTTPStatus.OK

    except Exception as error:
        logger.error(error)
        capture_exception(error)
        status = HTTPStatus.BAD_REQUEST

    return jsonify({'status': status.phrase}), status
