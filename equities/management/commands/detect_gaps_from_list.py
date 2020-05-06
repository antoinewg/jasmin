import json
import time
from datetime import date

from django.core.management.base import BaseCommand
from django.conf import settings

from equities.api import endpoints
from equities import utils
from equities import models


def get_range():
    ts = time.time()
    day = 60 * 60 * 24
    end = int(day * (1 + ts // day))
    start = int(end - 2 * 365 * day)
    return start, end


class Command(BaseCommand):
    help = "Check all the symbols OHLC data for gaps from the list of symbols provided."

    def add_arguments(self, parser):
        parser.add_argument("--from", default="", dest="from", type=str)

    def get_symbols(self, from_symbol):
        path = settings.BASE_DIR + "/equities/management/commands"

        with open(f"{path}/symbols.json") as symbols_file:
            symbols = json.loads(symbols_file.read())
            print(f"Received list of {len(symbols)} symbols to analyse.")

        return sorted([el for el in symbols if el > from_symbol])

    def get_candle(self, symbol, start, end):
        candles = endpoints.fetch_candles(symbol, start, end)
        time.sleep(1)
        return candles

    def handle(self, *args, **options):
        tot_gaps = 0
        for symbol in self.get_symbols(options["from"]):
            print("Checking gaps for %s\r" % symbol, end="")
            start, end = get_range()
            candles = self.get_candle(symbol, start, end)
            gaps = utils.detect_gaps_fom_candles(symbol, candles)
            if len(gaps):
                print(f"Creating {len(gaps)} gaps for symbol ({symbol})")
                tot_gaps += len(gaps)
                for gap in gaps:
                    models.Gap.objects.get_or_create(
                        symbol=gap.symbol,
                        ascending=gap.ascending,
                        prev_close=gap.prev_close,
                        open=gap.open,
                        percent=gap.percent,
                        volume=gap.volume,
                        volume_above_average=gap.vol_above_avg,
                        timestamp=date.fromtimestamp(gap.time).isoformat(),
                    )

        print(f"🎉 Finished. Total: {tot_gaps} gaps found")
