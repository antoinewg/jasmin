import requests

from django.conf import settings


URLS = {"news": "news?category=general"}


TOKEN = f"&token={settings.API_KEY}"
BASE_URL = "https://finnhub.io/api/v1/"
URLS = {k: BASE_URL + url + TOKEN for k, url in URLS.items()}


def fetch_news():
    response = requests.get(URLS["news"])
    return response.json()
