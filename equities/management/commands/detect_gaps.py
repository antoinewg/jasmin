import json
import time
from datetime import date

from django.core.management.base import BaseCommand
from django.conf import settings

from equities.api import endpoints
from equities import utils
from equities import models


IMPORTANT_SYMBOLS = set(
    (
        ["AAPL", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS", "DOW", "GS", "HD"]
        + ["IBM", "JNJ", "INTC", "JPM", "KO", "MRK", "MSFT", "PFE", "NKE", "PG"]
        + ["TRV", "UNH", "V", "VZ", "WBA", "WMT", "XOM", "MCD"]
    )
)


def get_range():
    ts = time.time()
    day = 60 * 60 * 24
    end = int(day * ts // day)
    start = int(end - 365 * day)
    return start, end


class Command(BaseCommand):
    help = "Check all the symbols OHLC data for gaps."

    def get_exchanges(self):
        # exchanges = endpoints.fetch_exchanges()
        exchanges = [{"code": "US", "currency": "USD", "name": "US exchanges"}]
        print(f"🚀 Found {len(exchanges)} exchanges")
        return exchanges

    def get_symbols(self, exchange):
        symbols = endpoints.fetch_symbols(exchange)
        # symbols = [s for s in symbols if s["symbol"] in IMPORTANT_SYMBOLS]
        print(f"🚀 Found {len(symbols)} symbols")
        return sorted(symbols, key=lambda x: x["symbol"])

    def get_candle(self, symbol, start, end):
        candles = endpoints.fetch_candles(symbol, start, end)
        return candles

    def handle(self, *args, **options):
        all_gaps = []
        exchanges = self.get_exchanges()

        for exchange in exchanges:
            print(f"Looking into exchange {exchange['name']}.")

            symbols = self.get_symbols(exchange["code"])
            for symbol in symbols:
                print("Checking gaps for %s\r" % symbol["symbol"], end="")
                start, end = get_range()
                candles = self.get_candle(symbol["symbol"], start, end)
                all_gaps += utils.detect_gaps_fom_candles(symbol["symbol"], candles)
                time.sleep(1)

        for gap in all_gaps:
            models.Gap.objects.create(
                symbol=gap.s,
                close=gap.c,
                next_open=gap.no,
                percent=gap.p,
                next_volume=gap.nv,
                timestamp=date.fromtimestamp(gap.t).isoformat(),
                next_timestamp=date.fromtimestamp(gap.nt).isoformat(),
            )

        gaps_db = models.Gap.objects.count()
        print(f"🎉 Finished. {gaps_db} gaps found")
