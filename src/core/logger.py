import logging
import logstash
from pythonjsonlogger import jsonlogger
from flask import request


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


logger = logging.getLogger('ugc_service')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('ugc_service.log')
file_handler.setLevel(logging.INFO)

formatter = jsonlogger.JsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(request_id)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logstash_handler = logstash.LogstashHandler('127.0.0.1', 5044, version=1)

logger.addHandler(logstash_handler)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addFilter(RequestIdFilter())
