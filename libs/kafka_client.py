from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable

import settings


def consumer():
    """
    Consumer configured to listen to the topic on the server configured on settings.py
    :return:
    """
    try:
        return KafkaConsumer(settings.KAFKA_TOPIC,
                             security_protocol="SSL",
                             ssl_cafile=settings.KAFKA_SSL_CA_FILE,
                             ssl_certfile=settings.KAFKA_SSL_CERT_FILE,
                             ssl_keyfile=settings.KAFKA_SSL_KEY_FILE,
                             bootstrap_servers=settings.KAFKA_SERVER)
    except NoBrokersAvailable as e:
        print("Could not connect to kafka, are settings correct?")
        raise e


def producer():
    """
    Producer configured to write to the server on settings.py
    :return:
    """
    try:
        return KafkaProducer(security_protocol="SSL",
                             ssl_cafile=settings.KAFKA_SSL_CA_FILE,
                             ssl_certfile=settings.KAFKA_SSL_CERT_FILE,
                             ssl_keyfile=settings.KAFKA_SSL_KEY_FILE,
                             bootstrap_servers=settings.KAFKA_SERVER)
    except NoBrokersAvailable as e:
        print("Could not connect to kafka, are settings correct?")
        raise e
