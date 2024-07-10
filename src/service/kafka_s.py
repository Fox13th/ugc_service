import json

from kafka import KafkaProducer

from core import config

settings = config.get_settings()


def send_to_kafka(
        event_data: dict,
):
    producer = KafkaProducer(bootstrap_servers=settings.kafka_host)
    print(settings.kafka_host)
    future = producer.send(
        topic=settings.kafka_topic,
        value=bytes(json.dumps(event_data), 'utf-8')
    )
    record_metadata = future.get(timeout=10)
    print(f'Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}')

