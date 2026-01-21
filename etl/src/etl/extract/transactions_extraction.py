import time
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = logging.getLogger(__name__)

class Transaction:
    def __init__(self, base_url: str, api_key: str= None, rate_limit_per_sec: float=5.0):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'appli'
        })