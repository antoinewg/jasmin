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

    def get_symbols(self):
        path = settings.BASE_DIR + "/equities/management/commands"

        with open(f"{path}/symbols.json") as symbols_file:
            symbols = json.loads(symbols_file.read())
            print(f"Received list of {len(symbols)} symbols to analyse.")

        return sorted(symbols)[::-1]

    def get_candle(self, symbol, start, end):
        candles = endpoints.fetch_candles(symbol, start, end)
        time.sleep(1)
        return candles

    def handle(self, *args, **options):
        models.Gap.objects.all().delete()

        tot_gaps = 0
        for symbol in self.get_symbols():
            print("Checking gaps for %s\r" % symbol, end="")
            start, end = get_range()
            candles = self.get_candle(symbol, start, end)
            gaps = utils.detect_gaps_fom_candles(symbol, candles)
            if len(gaps):
                print(f"Creating {len(gaps)} gaps for symbol ({symbol})")
                tot_gaps += len(gaps)
                for gap in gaps:
                    models.Gap.objects.create(
                        symbol=gap.symbol,
                        ascending=gap.ascending,
                        prev_close=gap.prev_close,
                        open=gap.open,
                        percent=gap.percent,
                        volume=gap.volume,
                        volume_above_average=gap.vol_above_avg,
                        timestamp=date.fromtimestamp(gap.time).isoformat(),
                    )

        print(f"Found {len(all_gaps)} gaps for exchange {exchange['name']}.")

        gaps_db = models.Gap.objects.count()
        print(f"🎉 Finished. Total: {gaps_db} gaps found")
