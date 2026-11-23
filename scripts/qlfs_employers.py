#!/usr/bin/env python3
"""Employer counts from QLFS 2026 Q3, and the SESE comparison.

    make qlfs        # from the repo root; expects data/statsa/qlfs/QLFS202603/QLFS202603.csv

Codebook: metadata/QLFS/2026/Qtr03/…metadata.pdf on iSiBaloweb.
  Sector                  1=formal, 2=informal, 3=households
  Ste_icse18_authority    1=employer, 2=own-account, 3=dependent contractor,
                          4=employee, 5=contributing family worker
  Infempl                 1=formal employment, 2=informal employment, 8=other
  Q413aHIRE               "hiring of employees", asked only of people running a business
  Q416NRWORKERS           number of employees in the establishment
  Q413VAT / Q414TAX       business registered for VAT / income tax

Missing values are 1.79769313486232e+308 (max double), not blank.
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

SENTINEL = 1.79769313486232e+308
CSV = str(DATA / "statsa" / "qlfs" / "QLFS202603" / "QLFS202603.csv")
COLS = ["Status", "Sector", "Ste_icse18_authority", "Q413VAT", "Q414TAX",
        "Q413aHIRE", "Q416NRWORKERS", "Weight"]


def num(s):
    return pd.to_numeric(s, errors="coerce").astype(float).replace({SENTINEL: np.nan})


def main():
    if not os.path.exists(CSV):
        raise SystemExit(f"{CSV} not found — fetch QLFS202603.zip and unzip it into that directory "
                         f"(see data/README.md)")
    df = pd.read_csv(CSV, low_memory=False, usecols=COLS)
    for c in COLS[:-1]:
        df[c] = num(df[c])
    df["w"] = num(df["Weight"])
    emp = df[df.Status == 1]                      # employed
    se = emp[emp.Ste_icse18_authority.isin([1, 2])]
    er = emp[emp.Ste_icse18_authority == 1]

    print(f"employed                {emp.w.sum():>12,.0f}")
    for k, lab in [(1, "formal"), (2, "informal"), (3, "households")]:
        print(f"  {lab:<21} {emp[emp.Sector == k].w.sum():>12,.0f}")

    print(f"\nemployers (all sectors) {er.w.sum():>12,.0f}")
    for k, lab in [(1, "formal"), (2, "informal")]:
        print(f"  {lab:<21} {er[er.Sector == k].w.sum():>12,.0f}")

    inf = se[se.Sector == 2]
    print(f"\ninformal self-employed  {inf.w.sum():>12,.0f}")
    print(f"  say they hire anyone  {inf[inf.Q413aHIRE == 1].w.sum():>12,.0f}")
    print(f"  VAT registered        {inf[inf.Q413VAT == 1].w.sum():>12,.0f}  (zero by construction)")
    print(f"  income tax registered {inf[inf.Q414TAX == 1].w.sum():>12,.0f}  (zero by construction)")

    print(f"\nall self-employed       {se.w.sum():>12,.0f}")
    print(f"  hire anyone           {se[se.Q413aHIRE == 1].w.sum():>12,.0f}")
    print(f"  VAT registered        {se[se.Q413VAT == 1].w.sum():>12,.0f}")

    q = num(er.Q416NRWORKERS)
    for k, lab in [(1, "formal"), (2, "informal")]:
        m = er.Sector == k
        print(f"\n{lab} employers: mean employees {(q[m] * er.w[m]).sum() / er.w[m].sum():.2f}, "
              f"median {q[m].median():.0f}, n={m.sum()}")

    print("\nSESE 2023 for comparison: 283,348 informal businesses with employees; "
          "1.82 paid employees each; 26 paid jobs per 100 businesses.")


if __name__ == "__main__":
    main()
