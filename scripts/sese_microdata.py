#!/usr/bin/env python3
"""Every figure in notes/2026-11-23-sese-2023-microdata-first-analysis.md,
from the Stats SA SESE 2023 unit-record file.

    uv run --with pandas python scripts/sese_microdata.py

The file lives in data/sa-entrepreneurship/sese-microdata/SESE2023.csv
(1 583 records x 201 variables, downloaded from Stats SA).

Two traps, both handled here:
  * missing values are stored as 1.79769313486232e+308 (max double), not blank;
  * some numeric columns arrive as strings because of that sentinel.
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CSV = str(DATA / "statsa" / "sese" / "SESE2023.csv")
SENTINEL = 1.79769313486232e+308


def num(s):
    return pd.to_numeric(s, errors="coerce").astype(float).replace({SENTINEL: np.nan})


def wq(x, w, qs=(0.25, 0.5, 0.75, 0.9)):
    m = x.notna()
    x2, w2 = x[m], w[m]
    o = x2.sort_values().index
    cum = w2[o].cumsum() / w2.sum()
    return {f"p{int(q*100)}": float(np.interp(q, cum, x2[o])) for q in qs}


def main():
    df = pd.read_csv(CSV, encoding="utf-8-sig", low_memory=False)
    df["w"] = df["Weight"]
    W = df["w"].sum()
    persons = df.groupby("UQNO")["w"].first().sum()
    print(f"records={len(df):,}  persons={df.UQNO.nunique():,}")
    print(f"weighted businesses={W:,.0f}  weighted persons={persons:,.0f}")

    df["paid"] = num(df["Q541PDLSTYEAR"]).fillna(0)
    df["unpaid"] = num(df["Q541UNPDLSTYEAR"]).fillna(0)
    df["has"] = df["Q53EMPLOYER"].eq(1)

    sex = df.groupby("Q13GENDER")["w"].sum() / W
    print("\nsex of owner (weighted):", {int(k): f"{v:.1%}" for k, v in sex.items()})

    print(f"\nemploying businesses: {df.loc[df.has,'w'].sum():,.0f} "
          f"({df.loc[df.has,'w'].sum()/W:.1%})")
    print(f"own-account:          {df.loc[~df.has,'w'].sum():,.0f} "
          f"({df.loc[~df.has,'w'].sum()/W:.1%})")
    paid_tot = (df.paid * df.w).sum()
    print(f"paid employees:       {paid_tot:,.0f}")
    print(f"unpaid workers:       {(df.unpaid*df.w).sum():,.0f}")
    print(f"paid jobs per 100 businesses: {paid_tot/W*100:.1f} "
          f"(incl. unpaid {(paid_tot+(df.unpaid*df.w).sum())/W*100:.1f})")
    print(f"mean paid employees per employer: "
          f"{paid_tot/df.loc[df.has,'w'].sum():.2f}")

    eo = df[df.has]
    print("\npaid employees per employing business (weighted):")
    for k, g in eo.groupby(eo.paid.clip(upper=6)):
        label = "6+" if k >= 6 else str(int(k))
        print(f"  {label:>3}: {g.w.sum():>10,.0f}  ({g.w.sum()/eo.w.sum():.1%})")

    turn = num(df["Q29TURNOVER12MNTH"])
    print(f"\nturnover: zero {df.loc[turn.fillna(0).eq(0),'w'].sum():,.0f}, "
          f"missing {df.loc[turn.isna(),'w'].sum():,.0f} ({df.loc[turn.isna(),'w'].sum()/W:.1%})")
    print("  quantiles (non-zero):", {k: f"R{v:,.0f}" for k, v in wq(turn.where(turn > 0), df.w).items()})
    print(f"  weighted mean incl. zeros: R{(turn.fillna(0)*df.w).sum()/W:,.0f}")

    prof = num(df["Q63NETPROFIT"])
    print(f"\nmonthly net profit: zero {df.loc[prof.eq(0),'w'].sum():,.0f} "
          f"({df.loc[prof.eq(0),'w'].sum()/W:.1%}); "
          f"mean R{(prof*df.w).sum()/W:,.0f} "
          f"(R{(prof*df.w).sum()/W*12:,.0f}/yr)")
    print("  quantiles (non-zero):", {k: f"R{v:,.0f}" for k, v in wq(prof.where(prof > 0), df.w).items()})

    print("\nemployment gradient by turnover band:")
    bands = [(0, 1, "nil"), (1, 50e3, "R1-50k"), (50e3, 250e3, "R50-250k"),
             (250e3, 500e3, "R250-500k"), (500e3, 1e15, "R500k+")]
    t = turn.fillna(-1)
    for lo, hi, label in bands:
        m = t.ge(lo) & t.lt(hi)
        wb = df.loc[m, "w"].sum()
        if wb == 0:
            continue
        emp = df.loc[m & df.has, "w"].sum()
        jobs = df.loc[m, "paid"].mul(df.loc[m, "w"]).sum()
        print(f"  {label:>10}: businesses {wb:>10,.0f}  employing {emp/wb:>6.1%}  jobs/100 {jobs/wb*100:>6.1f}")

    print("\nage of business (weighted):")
    labels = {1: "<1 yr", 2: "1-3", 3: "3-5", 4: "5-10", 5: "10+", 6: "don't know"}
    for k, g in df.groupby("Q31BUSSTARTED"):
        print(f"  {labels.get(k, k):>11}: {g.w.sum():>10,.0f} ({g.w.sum()/W:.1%})")

    miss = turn.isna()
    for name, m in [("employers", df.has), ("own-account", ~df.has)]:
        print(f"\nturnover missing among {name}: {df.loc[m & miss,'w'].sum()/df.loc[m,'w'].sum():.1%}")


if __name__ == "__main__":
    main()
