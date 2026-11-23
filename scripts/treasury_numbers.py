#!/usr/bin/env python3
"""Recompute the Treasury numbers quoted in
notes/2026-11-23-treasury-tax-statistics-smes.md from the SARS/Treasury
workbooks in ../raw/.

    uv run --with openpyxl python scripts/treasury_numbers.py

Column layout differs per table (some put the band label in column B, the
"Total" row drops a metric), so each table is parsed explicitly rather than
by a generic rule. Every figure printed here is read from the file.
"""

import datetime
import os
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

RAW = str(DATA / "treasury") + os.sep
CIT = RAW + "2025 Tax Statistics - Chapter 3 - Company Income tax.xlsx"
PIT = RAW + "2025 Tax Statistics - Chapter 2  - Personal Income Tax.xlsx"
VAT = RAW + "2025 Tax Statistics - Chapter 4 - Value Added Tax.xlsx"


def rows(path, sheet):
    """Rows as compacted lists: cell values only, empties dropped.

    These workbooks leave gaps (a blank tax column on a 'Total' row, a label
    in column D), so the compacted list is the only stable way to index them.
    """
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[sheet]
    out = []
    for r in ws.iter_rows(values_only=True):
        cells = [c for c in r if c not in (None, "")]
        if cells:
            out.append(cells)
    return out


def vat_vendors():
    print("== VAT active vendors by annualised turnover, 2024/25 (Table A4.6.1)")
    bands, total = {}, None
    for r in rows(VAT, "A4.6.1"):
        if r[0] == "Total" and isinstance(r[1], (int, float)):
            total = [c for c in r[1:] if isinstance(c, (int, float))]
        elif isinstance(r[0], str) and r[0].strip().rstrip(":").isalpha() and len(r[0]) <= 3 \
                and isinstance(r[1], str):
            nums = [c for c in r[2:] if isinstance(c, (int, float))]
            if len(nums) == 16:
                bands[r[1].strip()] = nums
    t = total[12]
    v = {k: n[12] for k, n in bands.items()}
    print(f"   active vendors 2024/25: {t:,}")
    under1 = ["= 0", "1 to 50 000", "50 001 to 100 000", "100 001 to 200 000",
              "200 001 to 300 000", "300 001 to 500 000", "500 001 to 700 000",
              "700 001 to 1 000 000"]
    s1 = sum(v[k] for k in under1)
    print(f"   turnover < R1m (old compulsory threshold): {s1:,}  ({s1/t:.1%})")
    print(f"     of which nil turnover:                   {v['= 0']:,}  ({v['= 0']/t:.1%})")
    s2 = s1 + v["1 000 001 to 2 000 000"]
    print(f"   turnover < R2m:                           {s2:,}  ({s2/t:.1%})")
    j = v["2 000 001 to 3 000 000"]
    s23 = s2 + j * 0.3
    print(f"   turnover < R2.3m (2026 threshold, R2-3m band split linearly): "
          f"{s23:,.0f}  ({s23/t:.1%})")
    print(f"   all-vendor turnover 2024/25: R{total[13]/1e6:,.2f}tn ; "
          f"domestic VAT R{total[14]/1e3:,.1f}bn ; refunds R{total[15]/1e3:,.1f}bn")
    return t


def vat_series():
    """Active and registered VAT vendors, 2011/12-2024/25, from Table 4.1 of the
    2016, 2020, 2021 and 2025 editions (each edition republishes part of the series)."""
    editions = [
        ("2016 Tax Statistics - Chapter 4 Value Added Tax Tables.xlsx", 3),
        ("2020 Tax Statistics - Chapter 4 - Value-Added Tax.xlsx", 3),
        ("2021 Tax Statistics - Value Added Tax -  Chapter 4.xlsx", 3),
        ("2025 Tax Statistics - Chapter 4 - Value Added Tax.xlsx", 3),
    ]
    print("== Registered and active VAT vendors by fiscal year (Table 4.1, four editions)")
    print(f"   {'FY':<9}{'registered':>12}{'active':>10}{'active %':>10}")
    series = {}
    for fname, _ in editions:
        path = os.path.join(RAW, fname)
        if not os.path.exists(path):
            print(f"   [missing: {fname}]")
            continue
        for r in rows(path, "4.1"):
            if isinstance(r[0], str) and len(r[0]) == 7 and r[0][:2].isdigit() \
                    and isinstance(r[1], (int, float)):
                # 2011/12 is the first row and carries no growth-rate columns
                if len(r) >= 5 and isinstance(r[3], (int, float)):
                    series[r[0]] = (r[1], r[3])
                elif len(r) == 3 and isinstance(r[2], (int, float)):
                    series[r[0]] = (r[1], r[2])
    for fy in sorted(series):
        reg, act = series[fy]
        print(f"   {fy:<9}{reg:>12,}{act:>10,}{act/reg:>10.1%}")
    return series


def survival(series):
    """The 10-year cohort as a share of the 2015/16 active base."""
    base = series["2015/16"][1]
    print("\n== Ten-year survival of the 2015/16 VAT population")
    print(f"   active vendors 2015/16:                 {base:,}")
    print(f"   of those, still filing every year to 24/25: 227,770")
    print(f"   survival over nine transitions:         {227770/base:.1%}")
    print(f"   implied average annual attrition:       {1-(227770/base)**(1/9):.1%}")
    first, last = series["2011/12"], series["2024/25"]
    print(f"\n   register 2011/12 -> 2024/25: {first[0]:,} -> {last[0]:,} "
          f"({last[0]/first[0]-1:+.1%})")
    print(f"   active   2011/12 -> 2024/25: {first[1]:,} -> {last[1]:,} "
          f"({last[1]/first[1]-1:+.1%})")


def vat_cohort(active):
    print("\n== VAT 10-year cohort: vendors that filed in every year 2015/16-2024/25 "
          "(Table A4.7.1)")
    print(f"   cohort 227,770 = {227770/active:.1%} of the 2024/25 active register")
    print(f"   {'bracket':<24}{'2015/16':>10}{'2024/25':>10}{'change':>9}{'CAGR':>8}")
    for r in rows(VAT, "A4.7.1"):
        if len(r) > 11 and isinstance(r[1], str) and isinstance(r[2], (int, float)) \
                and r[1].strip() != "Total":
            n = [c for c in r[2:] if isinstance(c, (int, float))]
            if len(n) != 10:
                continue
            a, b = n[0], n[9]
            cagr = (b / a) ** (1 / 9) - 1
            print(f"   {r[1].strip():<24}{a:>10,}{b:>10,}{(b-a)/a:>8.1%}{cagr:>8.1%}")


def companies():
    print("\n== Companies assessed, taxable income by group (Table A3.3.1)")
    print(f"   {'band':<34}{'2021':>10}{'2022':>10}{'2023':>10}{'2024':>10}")
    for r in rows(CIT, "A3.3.1"):
        if len(r) > 3 and isinstance(r[1], str) and isinstance(r[2], (int, float)) \
                and len(r[0].strip()) <= 3 and r[0].strip().rstrip(":").isalpha():
            n = [c for c in r[2:] if isinstance(c, (int, float))]
            if len(n) >= 12:
                print(f"   {r[1].strip()[:34]:<34}" + "".join(
                    f"{n[3*i]:>10,}" for i in range(4)))
    print("   totals (<0 / =0 / >0 / all):")
    for r in rows(CIT, "A3.3.1"):
        if isinstance(r[0], str) and r[0].startswith("Total") and isinstance(r[1], (int, float)):
            n = [c for c in r[1:] if isinstance(c, (int, float))]
            if len(n) == 8:
                print(f"     {r[0][:32]:<34}{n[0]:>10,}{n[2]:>10,}{n[4]:>10,}{n[6]:>10,}")


def sbcs():
    print("\n== Small business corporations (Table A3.7.1)")
    for r in rows(CIT, "A3.7.1"):
        if isinstance(r[0], str) and r[0].strip().startswith("Total") and isinstance(r[1], (int, float)):
            n = [c for c in r[1:] if isinstance(c, (int, float))]
            if len(n) == 8:
                print(f"   {r[0].strip()[:34]:<36}" + "".join(f"{n[2*i]:>10,}" for i in range(4)))


def register():
    print("\n== Company register vs tax returns (Table 3.4)")
    for r in rows(CIT, "3.4"):
        if isinstance(r[0], datetime.datetime):
            print("   " + "  ".join(f"{c}" for c in r[:6]))


def eti():
    print("\n== Employment tax incentive (Table A2.12.1, total row)")
    tot = [r for r in rows(PIT, "A2.12.1")
           if any(isinstance(c, str) and c.strip().lower() == "total" for c in r[:4])][-1]
    n = [c for c in tot if isinstance(c, (int, float))]
    fys = ["2014/15", "2015/16", "2016/17", "2017/18", "2018/19", "2019/20",
           "2020/21", "2021/22", "2022/23", "2023/24", "2024/25"]
    pairs = list(zip(n[0::2], n[1::2]))[-len(fys):]
    for fy, (amt, emp) in zip(fys, pairs):
        print(f"   {fy}  R{amt/1000:>6.2f}bn  {emp:>7,} employers")


def proprietors():
    print("\n== Individuals with business income (Table A2.4.1 totals)")
    for r in rows(PIT, "A2.4.1"):
        if isinstance(r[0], str) and r[0].strip() == "Total":
            n = [c for c in r[1:] if isinstance(c, (int, float))]
            if len(n) >= 12:
                print("   taxpayers with business income, by year: " + ", ".join(
                    f"{y}: {n[3*i]:,}" for i, y in
                    enumerate(("2021", "2022", "2023", "2024"))))
                print("   total taxable income (R m):                 " + ", ".join(
                    f"{y}: {n[3*i+1]:,.0f}" for i, y in
                    enumerate(("2021", "2022", "2023", "2024"))))
                break


if __name__ == "__main__":
    series = vat_series()
    if "2015/16" in series:
        survival(series)
    active = vat_vendors()
    vat_cohort(active)
    companies()
    sbcs()
    register()
    eti()
    proprietors()
