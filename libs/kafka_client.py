from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

import settings


def consumer():
    """
    Consumer configured to listen to the topic on the server configured on settings.py
    :return:
    """
    return KafkaConsumer(settings.KAFKA_TOPIC, bootstrap_servers=settings.KAFKA_SERVER)


def producer():
    """
    Producer configured to write to the server on settings.py
    :return:
    """
    try:
        return KafkaProducer(bootstrap_servers=settings.KAFKA_SERVER)
    except NoBrokersAvailable as e:
        print("Could not connect to kafka, are settings correct?")
        raise e
