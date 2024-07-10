from flask import request, jsonify, Blueprint

from core import config
from schemas.events import Event
from service.kafka_s import send_to_kafka

settings = config.get_settings()

router = Blueprint('statistics', __name__, url_prefix='/api/v1/statistics')


@router.route('/send', methods=['POST'])
def get_data():
    try:
        input_data = Event(**request.get_json(force=True))

        send_to_kafka(
            event_data=input_data.event_data
        )

        return jsonify({'status': 'OK'}), 200

    except Exception as error:
        print(error)
        return jsonify({'status': 'Bad Request'}), 400
