#!/usr/bin/env python3
"""The informal-sector series: SESE 2009, 2013, 2017, 2023 harmonised.

    make series        # from the repo root; data goes in data/statsa/{work,sese}

Each wave uses different variable names and, in one place, different *codes*:

  Q27BusStarted (2009)      -> Q31BusStarted (2013+)
  Q28MainReason (2009)      -> Q32MainReason (2013+)
  Q48Employer   (2009)      -> Q53Employer   (2013+)
  Q491Pdlstyear (2009)      -> Q541Pdlstyear (2013+)
  Q25Turnover12Mnth (2009)  -> Q29Turnover12Mnth (2013+)
  Q58netprofit (2009)       -> Q63netprofit (2013+)
  weight (2009-2017)        -> Weight (2023)

**Reason codes are not stable.** In 2009 code 2 is "unemployed / have no
alternative income" as a single merged category and code 3 is "retrenched";
from 2013 they split into 2 = unemployed and 3 = no alternative income, and
retrenched moves to 4. So the comparable "necessity" measure is {2} in 2009 and
{2,3} afterwards. Codes 14-16 ("to survive/make ends meet", "own boss",
"earn while searching") exist only from 2017.

Deflators: World Bank FP.CPI.TOTL for ZAF (2010=100), ratio to 2023.
  2009 x2.028, 2013 x1.659, 2017 x1.334, 2023 x1.000
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

WORK = str(DATA / "statsa" / "work")
SENTINEL = 1.79769313486232e+308

WAVES = [
    dict(year=2009, path="sese2009/SESE2009.csv", deflator=2.028,
         weight="weight", emp="Q48Employer", paid="Q491Pdlstyear", unpaid="Q491Unpdlstyear",
         age="Q27BusStarted", rsn="Q28MainReason", turn="Q25Turnover12Mnth",
         prof="Q58netprofit", licence="Q6licence", inctax="Q5incometax",
         necessity={2}, published_pop=1_144_000, published_necessity=68.3),
    dict(year=2013, path="sese2013/SESE2013.csv", deflator=1.659,
         weight="weight", emp="Q53Employer", paid="Q541Pdlstyear", unpaid="Q541Unpdlstyear",
         age="Q31BusStarted", rsn="Q32MainReason", turn="Q29Turnover12Mnth",
         prof="Q63netprofit", licence="Q6licence", inctax="Q5incometax",
         necessity={2, 3}, published_pop=1_517_000, published_necessity=69.2),
    dict(year=2017, path="sese2017/SESE2017.csv", deflator=1.334,
         weight="weight", emp="Q53Employer", paid="Q541Pdlstyear", unpaid="Q541Unpdlstyear",
         age="Q31BusStarted", rsn="Q32MainReason", turn="Q29Turnover12Mnth",
         prof="Q63netprofit", licence="Q6licence", inctax="Q5incometax",
         necessity={2, 3}, published_pop=1_793_000, published_necessity=63.5),
    dict(year=2023, path="../sese/SESE2023.csv", deflator=1.0,
         weight="Weight", emp="Q53EMPLOYER", paid="Q541PDLSTYEAR", unpaid="Q541UNPDLSTYEAR",
         age="Q31BUSSTARTED", rsn="Q32MAINREASON", turn="Q29TURNOVER12MNTH",
         prof="Q63NETPROFIT", licence="Q6LICENCE", inctax="Q5INCOMETAX",
         necessity={2, 3}, published_pop=1_873_000, published_necessity=57.1),
]


def num(s):
    return pd.to_numeric(s, errors="coerce").astype(float).replace({SENTINEL: np.nan})


def wmedian(x, w):
    m = x.notna()
    x2, w2 = x[m], w[m]
    if len(x2) == 0:
        return float("nan")
    o = x2.sort_values().index
    cum = w2[o].cumsum() / w2.sum()
    return float(np.interp(0.5, cum, x2[o]))


def wave_row(m):
    path = m["path"] if os.path.isabs(m["path"]) else os.path.join(WORK, m["path"])
    df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    w = num(df[m["weight"]]).fillna(0)
    total_w = w.sum()

    emp = num(df[m["emp"]])
    paid = num(df[m["paid"]]).fillna(0)
    unpaid = num(df[m["unpaid"]]).fillna(0)
    has = emp.eq(1)
    turn = num(df[m["turn"]])
    prof = num(df[m["prof"]])
    age = num(df[m["age"]])
    rsn = num(df[m["rsn"]])
    lic = num(df[m["licence"]])
    itx = num(df[m["inctax"]])

    paid_jobs = (paid * w).sum()
    bn = df["BUSNSNO"] if "BUSNSNO" in df.columns else pd.Series(1, index=df.index)
    first_biz = num(bn).fillna(1).eq(1)
    employers_w = w[has].sum()
    med_turn = wmedian(turn.where(turn > 0), w)
    med_prof = wmedian(prof.where(prof > 0), w)
    disc = turn.notna()

    return dict(
        year=m["year"], n=len(df), pop=total_w, published_pop=m["published_pop"],
        pct_emp=employers_w / total_w,
        jobs_per100=paid_jobs / total_w * 100,
        paid_per_emp=paid_jobs / employers_w if employers_w else float("nan"),
        unpaid_per100=(unpaid * w).sum() / total_w * 100,
        med_turn=med_turn, med_turn_real=med_turn * m["deflator"],
        pct_under50k=(w[turn.notna() & turn.lt(50e3)].sum() / w[disc].sum()),
        pct_turn_missing=w[turn.isna()].sum() / total_w,
        med_prof=med_prof, med_prof_real=med_prof * m["deflator"],
        pct_10plus=w[age.eq(5)].sum() / total_w,
        pct_under1=w[age.eq(1)].sum() / total_w,
        pct_licence=w[lic.eq(1)].sum() / total_w,
        pct_inctax=w[itx.eq(1)].sum() / total_w,
        necessity=w[rsn.isin(m["necessity"])].sum() / total_w,
        necessity_firstbiz=(w[first_biz & rsn.isin(m["necessity"])].sum()
                            / w[first_biz].sum()),
        employers_n=employers_w, paid_jobs_n=paid_jobs,
        published_necessity=m["published_necessity"],
    )


def main():
    rows = [wave_row(m) for m in WAVES]
    df = pd.DataFrame(rows)

    print("VALIDATION")
    print(f"  {'year':<6}{'records':>9}{'weighted':>12}{'published':>12}{'diff':>8}"
          f"{'necessity':>11}{'published':>11}")
    for r in rows:
        print(f"  {r['year']:<6}{r['n']:>9,}{r['pop']:>12,.0f}{r['published_pop']:>12,.0f}"
              f"{r['pop']/r['published_pop']-1:>8.1%}{r['necessity']:>11.1%}"
              f"{r['published_necessity']/100:>11.1%}")
    print("  (necessity restricted to each person's first business: "
          + ", ".join(f"{r['year']}: {r['necessity_firstbiz']:.1%}" for r in rows) + ")")

    print("\nABSOLUTE COUNTS (weighted business records)")
    print(f"  {'year':<6}{'businesses':>13}{'employers':>12}{'paid jobs':>12}")
    for r in rows:
        print(f"  {r['year']:<6}{r['pop']:>13,.0f}{r['employers_n']:>12,.0f}{r['paid_jobs_n']:>12,.0f}")

    print("\nEMPLOYMENT")
    print(f"  {'year':<6}{'% employers':>13}{'paid jobs/100':>15}{'paid per employer':>19}"
          f"{'unpaid/100':>12}")
    for r in rows:
        print(f"  {r['year']:<6}{r['pct_emp']:>13.1%}{r['jobs_per100']:>15.1f}"
              f"{r['paid_per_emp']:>19.2f}{r['unpaid_per100']:>12.1f}")

    print("\nTURNOVER AND PROFIT (R, median of non-zero)")
    print(f"  {'year':<6}{'turnover':>12}{'in 2023 R':>12}{'% under R50k':>14}"
          f"{'% missing':>11}{'profit/mth':>12}{'in 2023 R':>12}")
    for r in rows:
        print(f"  {r['year']:<6}{r['med_turn']:>12,.0f}{r['med_turn_real']:>12,.0f}"
              f"{r['pct_under50k']:>14.1%}{r['pct_turn_missing']:>11.1%}"
              f"{r['med_prof']:>12,.0f}{r['med_prof_real']:>12,.0f}")

    print("\nSTRUCTURE")
    print(f"  {'year':<6}{'% under 1yr':>13}{'% 10+ yrs':>11}{'% licence':>11}"
          f"{'% income tax':>14}{'% necessity':>13}")
    for r in rows:
        print(f"  {r['year']:<6}{r['pct_under1']:>13.1%}{r['pct_10plus']:>11.1%}"
              f"{r['pct_licence']:>11.1%}{r['pct_inctax']:>14.1%}{r['necessity']:>13.1%}")


if __name__ == "__main__":
    main()
