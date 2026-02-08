import requests
import json
from config import settings
def extra_customers():
    url = f"{settings['api']['base']}"