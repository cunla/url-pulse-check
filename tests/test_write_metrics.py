import unittest
from datetime import datetime
from unittest.mock import Mock

from kafka.consumer.fetcher import ConsumerRecord

from libs import kafka_client, database
from libs.model import Record
from write_metrics import get_msgs


class TestWriteMetrics(unittest.TestCase):

    def test_get_msgs(self):
        # arrange
        rec = Record("http://www.google.com", datetime.now(), 1.1, 200, 'itemtype', True)
        msgs = [ConsumerRecord(topic='website_health',
                               partition=0,
                               offset=172,
                               timestamp=1606615336458,
                               timestamp_type=0,
                               key=None,
                               value=bytes(rec.to_json(), encoding='utf8'), headers=[],
                               checksum=None,
                               serialized_key_size=-1,
                               serialized_value_size=140,
                               serialized_header_size=-1),
                ]
        kafka_client.consumer = Mock(return_value=msgs)
        database.write_record = Mock()
        # act
        get_msgs()

        # assert
        database.write_record.assert_called_with(rec)

