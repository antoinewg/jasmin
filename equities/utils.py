from collections import namedtuple

Gap = namedtuple("Gap", "s c no p nv t va")


def get_volume_above_average(vols, i, nv):
    vs = vols[max(0, i - 30) : i + 30][:30]
    return int(100 * 100 * (len(vs) * nv - sum(vs)) / sum(vs)) / 100.0


def detect_gaps_fom_candles(symbol, candles):
    gaps = []
    for i, c in enumerate(candles.get("c", [])[:-1]):
        no = candles["o"][i + 1]
        nh = candles["h"][i + 1]
        nl = candles["l"][i + 1]
        nc = candles["c"][i + 1]
        for g in gaps:
            max_day = max([no, nh, nl, nc])
            if g.c < max_day:
                # gap has been filled
                gaps = [el for el in gaps if el != g]

        if c > no:
            nv = candles["v"][i + 1]  # next_volume
            t = candles["t"][i]  # timestamp
            p = int(100 * 100 * (c - no) / no) / 100.0  # percent
            va = get_volume_above_average(candles["v"], i, nv)
            gap = Gap(symbol, c, no, p, nv, t, va)
            if p > 10:  # fall above 10%
                gaps.append(gap)

    return gaps
