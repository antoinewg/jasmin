from collections import namedtuple

Gap = namedtuple(
    "Gap", "symbol ascending prev_close open percent time volume vol_above_avg",
)


def get_volume_above_average(prev_volumes, volume):
    total = sum(prev_volumes)
    return (
        int(100 * (len(prev_volumes) * volume - total) / total) / 100.0 if total else 0
    )


def detect_gaps_fom_candles(symbol, candles):
    if not candles.get("o", []):
        return []

    try:
        # Get candles and first for each day
        prev_open, *opens = candles.get("o", [])
        prev_high, *highs = candles.get("h", [])
        prev_low, *lows = candles.get("l", [])
        prev_close, *closes = candles.get("c", [])
        prev_time, *times = candles.get("t", [])
        prev_volume, *volumes = candles.get("v", [])

        min_j_1 = min([prev_open, prev_high, prev_low, prev_close])
        max_j_1 = max([prev_open, prev_high, prev_low, prev_close])

        gaps = []
        day = 1
        for open, high, low, close, time, volume in zip(
            opens, highs, lows, closes, times, volumes
        ):
            # get min and max of day J.
            min_j = min([open, high, low, close])
            max_j = max([open, high, low, close])

            # Check if any gaps we've found previously has been filled
            # We compare the close before the gap with any value that day.
            for gap in gaps:
                if gap.ascending and gap.prev_close > min_j:
                    # ascending gap has been filled
                    gaps = [el for el in gaps if el != gap]
                if not gap.ascending and gap.prev_close < max_j:
                    # descending gap has been filled
                    gaps = [el for el in gaps if el != gap]

            # detect if there is a gap
            gap_present = False
            # ascending gap: ouverture > maximimum of day before
            if open > max_j_1 and min_j > max_j_1:
                gap_present = True
                ascending = True
                diff = (open - max_j_1) / max_j_1
            # descending gap:  ouverture < minimum of day before
            if open < min_j_1 and max_j < min_j_1:
                gap_present = True
                ascending = False
                diff = (min_j_1 - open) / open

            if gap_present:
                percent = int(100 * 100 * diff) / 100.0
                volumes = candles.get("v", [])
                prev_volumes = volumes[day - 5 : day + 5][:5]
                vol_above_avg = get_volume_above_average(prev_volumes, volume)

                if percent > 10 and sum(prev_volumes) / 5 > 1000 and vol_above_avg > 2:
                    gap = Gap(
                        symbol,
                        ascending,
                        prev_close,
                        open,
                        percent,
                        time,
                        volume,
                        vol_above_avg,
                    )
                    gaps.append(gap)

            # At the end of the loop, save the previous OHLC
            prev_open, prev_close = open, close
            prev_high, prev_low = high, low
            min_j_1, max_j_1 = min_j, max_j
            day += 1

        # After the loop, we return the gaps we've found for this symbol.
        return gaps
    except Exception as e:
        print(e)
        return []
