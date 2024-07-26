import logging
import logstash
from pythonjsonlogger import jsonlogger
from flask import request


class RequestFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        record.host = request.host
        record.http_user_agent = request.headers.get('User-Agent')
        record.method = request.method
        record.path = request.path
        record.query_params = request.query_string.decode('utf-8')
        record.status_code = getattr(record, 'status_code', 'N/A')
        return True


logger = logging.getLogger('ugc_service')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('ugc_service.log')
file_handler.setLevel(logging.INFO)

formatter = jsonlogger.JsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(request_id)s - %(message)s - %(host)s \
                                     - %(method)s - %(path)s - %(query_params)s - %(status_code)s - %(http_user_agent)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logstash_handler = logstash.LogstashHandler('127.0.0.1', 5044, version=1)

logger.addFilter(RequestFilter())
logger.addHandler(logstash_handler)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
