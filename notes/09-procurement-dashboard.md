# Procurement dashboard — transcribed figures

Read 2026-11-23 in a browser from National Treasury's **Procurement Dashboard**, a
Power BI *paginated report* (20 pages) embedded at:

```
https://app.powerbi.com/view?r=eyJrIjoiZDExYmQzOTYtZDE0MS00ZjE5LTgxZDctZTBjMGE5YTE3ZWQ0IiwidCI6IjFhNDUzNDhmLTAyYjQtNGY5YS1hN2E4LTc3ODZmNmRkMzI0NSIsImMiOjh9
```

linked from `https://data.etenders.gov.za/Home/SpendData` ("Procurement Data Dashboard"
→ "Procurement Payments Dashboard").

**There is no download.** The embed offers zoom, page navigation and share only — no
export to Excel/CSV/PDF. These figures were transcribed from the report's
accessibility tree, which exposes one `option` per visual element with the exact rand
amount and percentage (e.g. `"SMME Small and Medium Enterprise. Procurement Spend
R118,476,268,976 (36.05%)."`), so they are read values, not estimated from pixels.

**Filter state for every figure below:** `Fiscal_Year` = the four quarters QRT-1…QRT-4
of **2025/26** (a complete year; the slicer displays "Multiple selections"), `Sphere`
All, `Province` All, `Department` All. Page numbers are "n of 20".

Transcribing is the only route: the figures are not in any file Treasury publishes,
and the OCDS packages (which are downloadable) carry no usable award values.

## p.8 — Company and Commodity, FY2025/26

| Supplier size class | Spend | Share |
|---|---|---|
| Small and Medium Enterprise (SME) | R118,476,268,976 | 36.05% |
| Unspecified (no turnover recorded) | R108,390,903,986 | 32.98% |
| Large Business | R101,793,293,344 | 30.97% |
| **Total** | **R328,660,466,307** | 100% |

The same spend by supplier **turnover band** (the classification the type above is
derived from — note the different denominator, because unclassified suppliers drop out):

| Turnover band | Spend | Share of classified spend |
|---|---|---|
| 1: EME (R0 – R10m) | R75,602,779,740 | 33.93% |
| 2: QSE (R10m – R50m) | R42,873,489,237 | 19.24% |
| 3: GE (more than R50m) | R101,793,293,344 | 45.69% |
| 0: Not applicable | R2,526,831,819 | 1.13% |
| **Total classified** | **R222,796,394,140** | 100% |

EME + QSE = R118,476,268,977 = the SME line exactly. GE = the Large Business line
exactly. So SME here means **turnover below R50m**, and the 32.98% "Unspecified" is
spend on suppliers with no turnover on record.

## p.11–12 — Designated groups, FY2025/26

Totals for R328,660,466,307 of spend:

| Designated group | Spend | Share |
|---|---|---|
| Black owned | R134,777,033,021 | 41.01% |
| Women owned | R50,782,632,163 | 15.45% |
| Youth owned | R27,890,667,803 | 8.49% |
| Disabled owned | R1,848,227,271 | 0.56% |
| Rural / township owned (p.10 table) | see p.10, not read to a single total | — |

By quarter (p.12): black-owned share 40.89% / 44.03% / 35.83% / 41.74%;
women 15.59% / 16.45% / 13.57% / 15.59%; youth 8.62% / 9.08% / 7.12% / 8.77%;
disabled 0.59% / 0.61% / 0.51% / 0.50%.

Top ten **black-owned** suppliers (p.11), with each one's share as printed:
BONGANI RAINMAKER R4.61bn (32.19%), LEBONE LITHO PRINTERS R2.29bn (16%),
NOVUS PRINT R1.59bn (11.08%), NEXOR 312 R0.96bn (6.7%),
WORKING ON FIRE R0.95bn (6.63%), MTN PTY LTD R0.83bn (5.76%),
BRILLIANT TELECOMMUNICATIONS R0.74bn (5.16%), plus three unlabelled bars
(R0.89bn/6.19%, R0.75bn/5.25%, and ATLANTIS CORPORATE TRAVEL / TRAVEL WITH FLAIR).
The shares are printed against labels that the text layer interleaves — treat the
*rand amounts* as reliable and the per-supplier percentages as needing a screenshot check.

Top ten suppliers overall (p.9, FY2026/27 view): National Health Laboratory Service
R3bn; Property Management Trading R2bn; Bongani Rainmaker R2bn; SITA R2bn; then five
at R1bn. Spend by supplier type (p.9, FY2026/27): CIPC company 35.73%,
government entity 5.57%, **blank 54.82%** — i.e. more than half of spend is recorded
against a supplier with no type.

## p.10 — Supplier distribution (read with care)

"Value procured from new suppliers per year", by the supplier's **first spend year**:

| First spend year | Total spend | Black owned | Rural/township | Women | Disabled |
|---|---|---|---|---|---|
| 2021 (and earlier) | R1,911,421,302,329 | R445,221,644,471 | R41,912,615,175 | R134,508,725,292 | R5,899,975,827 |
| 2022 | R76,291,832,435 | R32,596,418,947 | R6,424,218,736 | R11,667,504,356 | R243,406,573 |
| 2023 | R56,426,673,812 | R27,509,937,851 | R5,954,832,180 | R11,229,465,571 | R248,633,011 |
| 2024 | R33,273,579,385 | R15,468,845,671 | R4,119,258,359 | R6,987,860,040 | R190,586,325 |
| 2025 | R14,554,381,552 | R9,875,376,832 | R3,203,228,737 | R4,515,843,469 | R119,606,930 |
| 2026 | R4,888,842,288 | R3,999,273,798 | R1,355,117,834 | R1,608,932,326 | R41,363,799 |
| Total | R2,096,856,611,802 | R534,671,497,569 | R62,969,271,020 | R170,518,331,053 | R6,743,572,466 |

**Interpretation, and why it needs care:** the 2021 row is plausibly "first spend in
2021 or earlier" (all incumbents), because R1.91tn over the roughly 5.5 years covered
matches the ~R329bn annual run-rate. On that reading **~91% of cumulative spend went
to suppliers first paid in 2021 or earlier**, and each new cohort's total accumulates
over a shorter window — so the rows are not directly comparable to each other.
"Number of new suppliers per year" on the same page gives 58,154 / 11,873 / 18,341 /
22,750 / 15,078 / 26,529 against an axis labelled 2022, 2024, 2026 with no other
ticks; I have not resolved which bar is which year, so **do not quote those counts**.

## What this measures, and what it does not

- It measures **share of BAS-recorded spend by supplier attribute** — size band,
  designated-group ownership — for national and provincial government.
- It does **not** measure compliance with any set-aside rule, points system or
  threshold: a 36% SME share is an outcome, not a certification that 30% was
  reserved and spent correctly.
- The size band is **turnover**, not headcount, and a third of spend has no band.
- Coverage: BAS (and a separate LOGIS section for the older system); municipalities
  are not in this dashboard. Spend figures are therefore payments, not commitments,
  and the dashboard's own totals (R328.66bn for 2025/26) are below the
  ~R450bn "procurement spend" on its trend page — which I could not reconcile
  without changing the sphere filter, so treat R328.66bn as the figure the
  supplier-size views are computed on.
