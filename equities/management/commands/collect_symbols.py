import json
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.core.management.base import BaseCommand
from django.conf import settings

from equities.api import endpoints


class Command(BaseCommand):
    help = "Collect list of important symbols."

    def get_most_volatile_stock(self):
        driver = webdriver.Chrome()
        url = "https://www.tradingview.com/markets/stocks-usa/market-movers-most-volatile/"
        driver.get(url)
        elems = driver.find_elements_by_css_selector("a.tv-screener__symbol")
        symbols = [e.text for i, e in enumerate(elems) if not i % 2]
        driver.close()
        return symbols

    def get_peers(self, symbol):
        peers = endpoints.fetch_peers(symbol)
        time.sleep(1)
        print(f"🚀 Found {len(peers)} peers for symbol {symbol}")
        return peers

    def handle(self, *args, **options):
        path = settings.BASE_DIR + "/equities/management/commands"

        with open(f"{path}/CAC_40.json") as cac40_file:
            cac40 = json.loads(cac40_file.read())
            print(f"Received {len(cac40)} symbols from cac40")

        with open(f"{path}/NASDAQ.json") as nasdaq_file:
            nasdaq = json.loads(nasdaq_file.read())
            print(f"Received {len(nasdaq)} symbols from nasdaq")

        with open(f"{path}/S_P_500.json") as sp500_file:
            sp500 = json.loads(sp500_file.read())
            print(f"Received {len(sp500)} symbols from sp500")

        unique_symbols = set(cac40) | set(nasdaq) | set(sp500)
        with open(f"{path}/symbols.json", "w") as outfile:
            json.dump(list(unique_symbols), outfile)
            print(f"Saved {len(unique_symbols)} unique symbols.")

        most_volatile = self.get_most_volatile_stock()
        for symbol in most_volatile:
            unique_symbols |= set(self.get_peers(symbol))

        with open(f"{path}/symbols.json", "w") as outfile:
            json.dump(list(unique_symbols), outfile)

        print(f"✅ Finished. {len(unique_symbols)} unique symbols.")
