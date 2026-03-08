import time
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url: str, api_key: str = None, rate_limit_per_sec: float = 5.0):
        if not base_url:
            raise ValueError(
                "API_BASE_URL is missing! Check your .env file or environment.")
        self.base_url = base_url.rstrip("/")  
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        if api_key:
            self.session.headers.update({'Authorization': f'Token {api_key}'})

            
        self.min_interval = 1 / rate_limit_per_sec
        self.last_request_time = 0

    def _throttle(self):
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.min_interval:
            sleep_time = self.min_interval - elapsed
            time.sleep(sleep_time)
        self.last_request_time = time.time()  

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException,)),
        reraise=True
    )
    def get(self, path: str, params: dict = None):
        self._throttle()
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = self.session.get(url, params=params or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            log.error(f"HTTP error for {url}: {e}")
            raise


    def paginate(self, endpoint, page_param="page", per_page_param="limit",
                 start_page=1, per_page=50, data_key="results"):
        page = start_page
        while True:
            try:
                payload = self.get(
                    endpoint, {page_param: page, per_page_param: per_page})
                records = payload.get(data_key, [])
                if not records:
                    break
                for rec in records:
                    yield rec
                if not payload.get("next"):
                    break
                page += 1
            except requests.exceptions.HTTPError as e:
                log.error(f"Error fetching page {page} from {endpoint}: {e}")
                raise


# api = ApiClient(base_url="http://127.0.0.1:8000/api/",
#                 api_key="2a222aeeeb844a30dc619918a3eccdd57fbf6b0b")
# users = api.get("accounts", {"page": 1, "per_page": 100})
# print(users)
