#!/usr/bin/env python3
"""Cross-tabs from the SESE 2023 microdata: who employs people, and why.

    cd data/sa-entrepreneurship/sese-microdata
    uv run --with pandas python ../treasury/scripts/sese_crosstabs.py

Weighted throughout; the unweighted cell size is printed beside every estimate
because 1 583 records cannot carry fine cuts (anything under ~30 records is
reported but flagged).

Codes (from the SESE 2023 record layout, metadata PDF):
  Q31BUSSTARTED  1 <1yr, 2 1-3, 3 3-5, 4 5-10, 5 10+, 6 don't know
  Q32MAINREASON  02 unemployed, 03 no alternative income, 04 retrenched,
                 05 inadequate other income, 14 to survive/make ends meet,
                 16 earn while searching for a job  -> PUSH
                 01 inherited, 06 like the activity, 07 have skills,
                 08 have equipment, 09 high income, 10 small investment,
                 11 unhappy with previous work, 12 new opportunity,
                 15 own boss / create employment      -> PULL
                 13 other                            -> OTHER
  Q53EMPLOYER    1 has workers, 2 none
  Q541PDLSTYEAR  number of paid employees
  Q6LICENCE, Q5INCOMETAX, Q25TYPRECORD, Q73SAVACCOUNT  1 = yes
  Q29TURNOVER12MNTH  last 12 months, rand
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CSV = str(DATA / "statsa" / "sese" / "SESE2023.csv")
SENTINEL = 1.79769313486232e+308

AGE = {1: "<1 yr", 2: "1-3", 3: "3-5", 4: "5-10", 5: "10+", 6: "don't know"}
PUSH = {2, 3, 4, 5, 14, 16}
PULL = {1, 6, 7, 8, 9, 10, 11, 12, 15}


def num(s):
    return pd.to_numeric(s, errors="coerce").astype(float).replace({SENTINEL: np.nan})


def load():
    df = pd.read_csv(CSV, encoding="utf-8-sig", low_memory=False)
    df["w"] = df["Weight"]
    df["paid"] = num(df["Q541PDLSTYEAR"]).fillna(0)
    df["has"] = df["Q53EMPLOYER"].eq(1)
    df["age"] = df["Q31BUSSTARTED"].map(AGE)
    df["reason"] = df["Q32MAINREASON"]
    df["group"] = np.where(df.reason.isin(PUSH), "push",
                           np.where(df.reason.isin(PULL), "pull", "other"))
    df["turn"] = num(df["Q29TURNOVER12MNTH"])
    df["turn_band"] = pd.cut(df.turn, [-0.1, 0, 50e3, 250e3, 500e3, 1e15],
                             labels=["nil", "R1-50k", "R50-250k", "R250-500k", "R500k+"])
    return df


def table(df, by, title, order=None):
    W = df.w.sum()
    print(f"\n{title}")
    print(f"  {'':<14}{'businesses':>12}{'% of sector':>12}{'% that employ':>14}"
          f"{'jobs/100':>10}{'n':>6}")
    groups = df.groupby(by, observed=False)
    keys = order if order is not None else [k for k, _ in groups]
    for k in keys:
        g = groups.get_group(k) if k in dict(iter(groups)) else None
        if g is None or len(g) == 0:
            continue
        wb = g.w.sum()
        emp = g.loc[g.has, "w"].sum()
        jobs = (g.paid * g.w).sum()
        flag = "" if len(g) >= 30 else "  *thin"
        print(f"  {str(k):<14}{wb:>12,.0f}{wb/W:>12.1%}{emp/wb:>14.1%}"
              f"{jobs/wb*100:>10.1f}{len(g):>6}{flag}")


def main():
    df = load()
    W = df.w.sum()
    print(f"records {len(df):,}   weighted businesses {W:,.0f}")

    # reason groups
    g = df.groupby("group").agg(n=("w", "size"), w=("w", "sum"))
    print("\nWHY they started (Q32MAINREASON):")
    for k, r in g.iterrows():
        print(f"  {k:<6} {r.w:>12,.0f}  {r.w/W:>6.1%}   (n={int(r.n)})")
    only = df[df.reason.isin([2, 3])]
    print(f"  'unemployed or no alternative income' (02+03) alone: "
          f"{only.w.sum():,.0f} ({only.w.sum()/W:.1%})")

    table(df, "age", "BY BUSINESS AGE", order=["<1 yr", "1-3", "3-5", "5-10", "10+", "don't know"])
    table(df, "group", "BY WHY THE OWNER STARTED", order=["push", "pull", "other"])
    table(df, "turn_band", "BY TURNOVER", order=["nil", "R1-50k", "R50-250k", "R250-500k", "R500k+"])

    # formalisation markers
    print("\nBY FORMALISATION MARKER (share of that group which employs anyone):")
    for col, lab in [("Q6LICENCE", "has a licence"), ("Q5INCOMETAX", "registered for income tax"),
                     ("Q73SAVACCOUNT", "has a savings account")]:
        g = df.groupby(col)
        for k, sub in g:
            if k != 1:
                continue
            print(f"  {lab:<24} {sub.w.sum():>12,.0f} businesses, "
                  f"{sub.loc[sub.has,'w'].sum()/sub.w.sum():>5.1%} employ, "
                  f"jobs/100 {(sub.paid*sub.w).sum()/sub.w.sum()*100:>5.1f}  (n={len(sub)})")

    print("\nAGE x PUSH/PULL: share that employ")
    print(f"  {'':<10}" + "".join(f"{g:>10}" for g in ["push", "pull"]))
    for a in ["<1 yr", "1-3", "3-5", "5-10", "10+"]:
        row = []
        for grp in ["push", "pull"]:
            sub = df[(df.age == a) & (df.group == grp)]
            row.append(f"{sub.loc[sub.has,'w'].sum()/sub.w.sum():>9.1%}" if len(sub) else f"{'-':>9}")
        print(f"  {a:<10}" + "".join(row))

    print("\nAGE x TURNOVER: share of businesses in each age with R50k+ turnover")
    for a in ["<1 yr", "1-3", "3-5", "5-10", "10+"]:
        sub = df[df.age == a]
        big = sub[sub.turn > 50e3]
        print(f"  {a:<10} {big.w.sum()/sub.w.sum():>6.1%} above R50k turnover  (n={len(sub)})")


if __name__ == "__main__":
    main()
