from flask import request, jsonify, Blueprint

from core import config
from service.kafka_s import send_to_kafka

settings = config.get_settings()

router = Blueprint('statistics', __name__, url_prefix='/api/v1/statistics')


@router.route('/send', methods=['POST'])
def get_data():
    try:
        input_data = request.get_json(force=True)

        send_to_kafka(ip_srv=settings.kafka_host,
                      port_srv=settings.kafka_port,
                      topic_data=input_data['topic'],
                      value_data=input_data['value'],
                      key_data=input_data['key'])

        return jsonify({'status': 'OK'}), 200

    except Exception:
        return jsonify({'status': 'Bad Request'}), 400
