import json
from datetime import datetime
from decimal import Decimal
from typing import Dict, Tuple


class Record(object):
    def __init__(self, url: str, start_time: datetime,
                 elapsed_time: float, status_code: int,
                 regex: str = None, regex_found: bool = None):
        self.url = url
        self.start_time = start_time
        self.elapsed_time = elapsed_time
        self.status_code = status_code
        self.regex = regex
        self.regex_found = regex_found

    def set_regex(self, regex: str, regex_found: bool):
        self.regex = regex
        self.regex_found = regex_found

    def to_json(self) -> str:
        return json.dumps({
            'url': self.url,
            'start': self.start_time.isoformat(),
            'total': self.elapsed_time,
            'code': self.status_code,
            'regex': self.regex,
            'found': self.regex_found
        })

    def to_tuple(self) -> Tuple:
        total_time = round(Decimal.from_float(self.elapsed_time), 2)
        return (self.url, self.start_time,
                total_time,
                self.status_code,
                self.regex, self.regex_found)

    @staticmethod
    def from_json(rec: Dict):
        start_time = datetime.fromisoformat(rec['start'])
        return Record(rec['url'], start_time, rec['total'], rec['code'], rec['regex'], rec['found'])

    def __str__(self):
        return self.to_json()

    def __eq__(self, other):
        return self.url == other.url \
               and self.start_time == other.start_time \
               and self.elapsed_time == other.elapsed_time \
               and self.regex == other.regex \
               and self.status_code == other.status_code \
               and self.regex_found == other.regex_found
