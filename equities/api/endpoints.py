import requests

from django.conf import settings


URLS = {
    "news": "/news?category=general&",
    "exchange": "/stock/exchange?",
    "symbols": "/stock/symbol?exchange={}&",
    "candle": "/stock/candle?symbol={}&resolution=D&from={}&to={}&",
}


TOKEN = f"token={settings.API_KEY}"
BASE_URL = "https://finnhub.io/api/v1"
URLS = {k: BASE_URL + url + TOKEN for k, url in URLS.items()}


def fetch_news():
    r = requests.get(URLS["news"])
    return r.json()


def fetch_exchanges():
    r = requests.get(URLS["exchange"])
    return r.json()


def fetch_symbols(exchange="US"):
    url = URLS["symbols"].format(exchange)
    r = requests.get(url)
    return r.json()


def fetch_candles(symbol="AAPL", start=1572651390, end=1572910590):
    url = URLS["candle"].format(symbol, start, end)
    r = requests.get(url)
    return r.json()
