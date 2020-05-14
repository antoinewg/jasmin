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
        parser.add_argument(
            "--from",
            default="",
            dest="from",
            type=str,
            help="Symbol (ex: AAPL) from which to start.",
        )
        parser.add_argument(
            "--exchange",
            default=None,
            dest="exchange",
            type=str,
            help="Exchange (ex: PA, US) from which to check the symbols' gaps",
        )

    def get_exchanges(self):
        exchanges = endpoints.fetch_exchanges()
        return exchanges

    def get_symbols_from_exchange(self, exchange):
        symbols = endpoints.fetch_symbols(exchange)
        return sorted(symbols, key=lambda x: x["symbol"])

    def get_symbols(self):
        path = settings.BASE_DIR + "/equities/management/commands"

        with open(f"{path}/symbols.json") as symbols_file:
            symbols = json.loads(symbols_file.read())
            print(f"Received list of {len(symbols)} symbols to analyse.")

        return sorted([el for el in symbols])

    def get_candle(self, symbol, start, end):
        candles = endpoints.fetch_candles(symbol, start, end)
        return candles

    def handle(self, *args, **options):
        all_symbols = self.get_symbols()

        from_symbol = options["from"]
        if from_symbol:
            all_symbols = [s for s in all_symbols if s > from_symbol]
            print(f"Checking {len(all_symbols)} symbols starting from {from_symbol}.")

        exchange_code = options["exchange"]
        if not exchange_code:
            print("Checking all symbols from the list. Not filtered on the exchange.")
        else:
            exchanges = self.get_exchanges()
            corr_exchanges = [ex for ex in exchanges if ex["code"] == exchange_code]
            if corr_exchanges:
                symbols_from_exchange = self.get_symbols_from_exchange(exchange_code)
                symbols_set = {el["symbol"] for el in symbols_from_exchange}
                all_symbols = list(set(all_symbols) & symbols_set)

                msg = "Checking {} symbols from list. Filtered on exchange {}."
                print(msg.format(len(all_symbols), exchange_code))

        all_symbols = sorted(all_symbols)

        tot_gaps = 0
        for symbol in all_symbols:
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
