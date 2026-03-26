import logging
import requests
import json
from datetime import datetime
from typing import Dict, List

class Utils:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def make_request(self, url: str, headers: Dict[str, str]) -> Dict[str, str]:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to {url} failed with error {e}")
            return {}

    def parse_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as e:
            logging.error(f"Failed to parse date {date_str} with error {e}")
            return None

    def calculate_diff(self, date1: datetime, date2: datetime) -> int:
        return abs((date1 - date2).days)

    def flatten_dict(self, data: Dict[str, List]) -> Dict[str, List]:
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result.update(self.flatten_dict(value))
            else:
                result[key] = value
        return result

    def sort_dict_by_value(self, data: Dict[str, int]) -> Dict[str, int]:
        return dict(sorted(data.items(), key=lambda item: item[1]))