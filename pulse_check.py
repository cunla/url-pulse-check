import argparse
import logging
import re
from datetime import datetime
from time import sleep

import requests
from kafka import KafkaProducer
from requests import ReadTimeout

import settings
from libs import kafka_client
from libs.model import Record

logger = logging.getLogger(__name__)


def check_url_health(url: str, regex_str: str):
    """
    The website checker should perform the checks periodically and collect the
    HTTP response time,
    error code returned,
    as well as optionally checking the returned page contents for a regexp pattern
    that is expected to be found on the page.
    """
    try:
        response = requests.get(url, timeout=10)
        total_time = response.elapsed.total_seconds()
        status_code = response.status_code
    except ReadTimeout as e:
        total_time = -1
        status_code = 404
    result = Record(url, datetime.now(), total_time, status_code)
    if regex_str is not None and total_time != -1:
        # used https://stackoverflow.com/a/15742632/1056460
        result.set_regex(regex_str, bool(re.search(regex_str, response.text)))
    logger.info(f"checked health: {result}")
    return result


def send_update(producer: KafkaProducer, url: str, regex_str: str):
    rec = check_url_health(url, regex_str)
    producer.send(settings.KAFKA_TOPIC, bytes(rec.to_json(), encoding='utf8'))


def check_urls(urls, regex, sleep_time):
    producer = kafka_client.producer()
    while True:
        for url in urls:
            send_update(producer, url, regex)
        logger.info(f'Finished checking URLs, sleeping for {sleep_time}s')
        sleep(sleep_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="pulse check")
    parser.add_argument('--urls', type=str, nargs='+', required=True,
                        help='URLs to check')
    parser.add_argument('--sleep', '-s', type=int, default=settings.SLEEP_BETWEEN_CHECKS,
                        help='Seconds between checks')
    parser.add_argument('--regex', type=str,
                        help='Regular expression to check for in URL')
    args = parser.parse_args()
    print(args)
    check_urls(args.urls, args.regex, args.sleep)
