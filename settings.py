import logging

logging.basicConfig(level=logging.INFO,
                    format="%(lineno)d in %(filename)s at %(asctime)s: %(message)s")

# Kafka connection settings
KAFKA_SERVER = 'localhost:9092'
KAFKA_TOPIC = 'website_health'

# Databases settings
DATABASES = [
    {
        'name': 'default',
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'password',
        'database': 'postgres',
        'schema': 'public',
        'table': 'url_check',
    },
]

# Healthcheck period
SLEEP_BETWEEN_CHECKS = 10
