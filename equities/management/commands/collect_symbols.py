import json
import time
from datetime import date

from django.core.management.base import BaseCommand
from django.conf import settings

from equities.api import endpoints
from equities import utils
from equities import models


class Command(BaseCommand):
    help = "Collect list of important symbols."

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
