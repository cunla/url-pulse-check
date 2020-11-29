import logging
import os

logging.basicConfig(level=logging.INFO,
                    format="%(lineno)d in %(filename)s at %(asctime)s: %(message)s")

# Kafka connection settings, if connection does not require SSL, the KAFKA_SSL_* can be set to None
KAFKA_SSL_CA_FILE = '/Users/style/PycharmProjects/kafka2postgres/ca.pem'
KAFKA_SSL_CERT_FILE = '/Users/style/PycharmProjects/kafka2postgres/cert.pem'
KAFKA_SSL_KEY_FILE = '/Users/style/PycharmProjects/kafka2postgres/service.key'
KAFKA_SERVER = 'kafka-1e6aebe0-daniel-e9f0.aivencloud.com:29100'
KAFKA_TOPIC = 'website_health'

# Databases settings
DATABASES = [
    {
        'name': 'default',
        'host': 'pg-96edce5-daniel-e9f0.aivencloud.com',
        'port': 29098,
        'user': 'avnadmin',
        'password': os.getenv('POSTGRES_PASSWORD', 'password'),
        'database': 'defaultdb',
        'schema': 'public',
        'table': 'url_check',
    },
]

# Healthcheck period
SLEEP_BETWEEN_CHECKS = 10
