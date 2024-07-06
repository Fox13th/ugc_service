from kafka import KafkaProducer


def send_to_kafka(ip_srv: str,
                  port_srv: str,
                  topic_data: str,
                  value_data: str,
                  key_data: str):
    producer = KafkaProducer(bootstrap_servers=[f'{ip_srv}:{port_srv}'])

    producer.send(
        topic=topic_data,
        value=bytes(value_data, 'utf-8'),
        key=bytes(key_data, 'utf-8'),
    )
