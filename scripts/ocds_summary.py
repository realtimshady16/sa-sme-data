#!/usr/bin/env python3
"""Summarise Treasury eTenders OCDS monthly JSON files.

Reads one or more 0xMMYYYY.json files (as downloaded from
https://data.etenders.gov.za/Home/DownloadFile/?fileName=<0xMMYYYY>.json)
and reports: release counts, how many carry a tender value, how many carry
awards with a value, the value distribution, and the top buyers/suppliers.

The CSV twins of these files do NOT carry values; only the JSON does.
"""
import json
import sys
from collections import Counter, defaultdict

BANDS = [0, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000,
         30_000_000, 100_000_000, float("inf")]


def band(v):
    for lo, hi in zip(BANDS, BANDS[1:]):
        if lo <= v < hi:
            return f"R{lo/1e6:g}m-{'inf' if hi == float('inf') else f'R{hi/1e6:g}m'}"
    return "?"


def main(paths):
    for path in paths:
        d = json.load(open(path))
        rel = d.get("Releases") or []
        print("=" * 78)
        print(f"{path}  published {d.get('PublishedDate')}  releases={len(rel)}")
        print(f"  uri field on file: {d.get('Uri')}")
        tv, av = [], []
        buyers, sup = Counter(), defaultdict(float)
        status = Counter()
        for r in rel:
            status[r.get("tender", {}).get("status")] += 1
            amt = (r.get("tender", {}).get("value") or {}).get("amount")
            if isinstance(amt, (int, float)):
                tv.append(amt)
            for a in r.get("awards") or []:
                aamt = (a.get("value") or {}).get("amount")
                if isinstance(aamt, (int, float)):
                    av.append(aamt)
                    for s in a.get("suppliers") or []:
                        sup[s.get("Name") or "?"] += aamt
                    buyers[r.get("buyer", {}).get("name") or "?"] += aamt
        print(f"  tender.value present: {len(tv)}/{len(rel)}  total R{sum(tv)/1e9:,.2f}bn")
        print(f"  award value present : {len(av)}  total R{sum(av)/1e9:,.2f}bn")
        print(f"  tender status       : {status.most_common()}")
        if av:
            hist = Counter(band(v) for v in av)
            print("  award value bands   :")
            for k in hist:
                print(f"     {k:<22} {hist[k]:>5}  R{sum(v for v in av if band(v) == k)/1e6:,.0f}m")
            av_sorted = sorted(av)
            n = len(av_sorted)
            print(f"  awards: n={n} median=R{av_sorted[n//2]:,.0f} "
                  f"p90=R{av_sorted[int(n*0.9)]:,.0f} max=R{av_sorted[-1]:,.0f}")
            print("  top 10 suppliers by awarded value:")
            for name, v in sorted(sup.items(), key=lambda kv: -kv[1])[:10]:
                print(f"     R{v/1e6:>10,.1f}m  {name[:60]}")


if __name__ == "__main__":
    main(sys.argv[1:])
