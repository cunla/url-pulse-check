import json
import logging

from libs import database
from libs import kafka_client
from libs.model import Record

logger = logging.getLogger(__name__)


def get_msgs():
    msgs = kafka_client.consumer()
    for message in msgs:
        logger.debug(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}")
        msg_dict = json.loads(message.value)
        record = Record.from_json(msg_dict)
        logger.info(f"Got record {record}")
        database.write_record(record)


if __name__ == '__main__':
    database.initialize_connections()
    get_msgs()
