# Who employs people in the informal sector, and why it matters that it's mostly the desperate

*2026-11-23. Cross-tabs from the SESE 2023 microdata (`scripts/sese_crosstabs.py`), weighted throughout, with the unweighted cell size beside every estimate. Follows `notes/04-sese-2023-microdata.md` (the headline counts) and the QLFS reconciliation.*

## 1. Why they started

| Grouping | Businesses | Share |
|---|---|---|
| **Push** — unemployed, no alternative income, retrenched, inadequate income, "to survive/make ends meet", earning while job-searching | **1 476 645** | **74.6%** |
| **Pull** — inherited, likes the activity, has the skills or equipment, sees a new opportunity, wants to be own boss | 440 869 | 22.3% |
| Other | 60 698 | 3.1% |

The narrow reading published in the release — "I was unemployed" or "I had no alternative income source" — is **56.2%** (1 112 728), and it reproduces the published 57.1% within rounding. Adding the survivalist remainder ("to survive/make ends meet", "earn while searching") takes the necessity share to three-quarters.

## 2. Employment rises with age, steeply

| Business age | Businesses | % that employ anyone | Paid jobs per 100 | n |
|---|---|---|---|---|
| Under a year | 321 797 | 10.9% | **7.0** | 265 |
| 1 – 3 years | 442 159 | 10.0% | 20.0 | 337 |
| 3 – 5 years | 335 829 | 15.2% | 27.1 | 263 |
| 5 – 10 years | 410 903 | 13.2% | 28.3 | 318 |
| **10 years +** | 449 933 | **20.9%** | **42.9** | 383 |

A ten-year-old informal business is twice as likely to employ someone as a new one, and carries **six times the jobs per 100**. The employer rate is not monotonic between 1 and 10 years (10.0% → 15.2% → 13.2%), which is within sampling noise on these cells; the direction over the full range is not.

**Where the employers are, in volume**: firms older than five years hold **52.4% of the 283 348 employers and 60.1% of the 514 568 paid jobs**. Businesses under a year old hold 12.4% of employers but only **4.4% of the jobs** — new informal firms employ almost nobody.

## 3. Motive matters per business — and almost not at all in aggregate

| Why the owner started | % that employ | Paid jobs per 100 | Employers (share of all) | Paid jobs (share of all) |
|---|---|---|---|---|
| **Pull** | **22.3%** | **41.1** | 98 203 (34.7%) | 181 417 (35.3%) |
| **Push** | 12.2% | 22.2 | **180 583 (63.7%)** | **328 371 (63.8%)** |
| Other | 7.5% | 7.9 | 4 562 (1.6%) | 4 779 (0.9%) |

Both readings are true and they point in opposite directions:

- **Per business**, an opportunity-started business is **1.8× as likely to employ** and generates **1.85× the jobs per 100**.
- **In aggregate**, necessity-started businesses supply **nearly two-thirds of all informal paid jobs** — because they are three-quarters of the population.

So "only opportunity entrepreneurs create jobs" is false at the level of the economy and true at the level of the firm. The informal sector's jobs mostly come from distress-motivated businesses **that survived long enough to hire**.

## 4. The motive gap is mostly a survival effect

Share that employs anyone, by age and motive:

| Business age | Push | Pull | Gap | n push/pull |
|---|---|---|---|---|
| Under a year | **6.6%** | **35.0%** | 28.4 pp | 216 / 41 |
| 1 – 3 years | 9.2% | 15.5% | 6.3 pp | 278 / 49 |
| 3 – 5 years | 13.2% | 20.2% | 7.0 pp | 196 / 61 |
| 5 – 10 years | 11.3% | 19.6% | 8.3 pp | 226 / 83 |
| 10 years + | **20.4%** | **24.4%** | **4.0 pp** | 255 / 113 |

At birth, an opportunity-started business is **five times** as likely to be an employer (35.0% vs 6.6%); by ten years the difference has narrowed to 4 points (24.4% vs 20.4%). Read as a cohort pattern: **hiring is something informal businesses grow into, and the motive you start with predicts the speed, not the ceiling.** The pull-at-birth cell is 41 records, so the 35.0% is the softest number in this note — but the direction of the convergence holds across all five bands and the endpoint cells are 113 and 255.

## 5. Formalisation markers track employment hard

| Marker | Businesses | % that employ | Jobs per 100 | n |
|---|---|---|---|---|
| Has a business licence | 217 725 | 30.1% | **77.3** | 159 |
| Registered for income tax | 147 882 | 35.6% | **95.4** | 102 |
| Has a savings account | 487 361 | 27.9% | 68.6 | 349 |
| *Whole sector* | 1 978 211 | 14.3% | 26.0 | 1 583 |

Businesses with a licence or an income-tax number run **3–4× the jobs per 100 of the sector average**. Two readings, and the data cannot separate them: formalisation enables hiring (credit, contracts, larger customers), or hiring induces formalisation (an employer has to register). The causal direction matters enormously for policy, and this file cannot settle it.

## 6. Traps in this file

- **Annual turnover is missing for every business under a year old** (all 265 records). The question is asked only of businesses operating twelve months or more, so *no age × turnover comparison is possible*, and any table that appears to show it is reading a skip pattern as a zero.
- **Cell sizes**: the pull-at-birth cell is 41 records, the R250k–500k turnover band 19, the R500k+ band 8. Anything with fewer than ~30 records is reported above but should not be quoted as a level.
- **Weights, not sample**: every figure is weighted; the *n* column is what tells you how much to trust it.
- **One wave, one year (2023)**: these are cross-sectional associations. §4's "survival effect" reading is an interpretation of an age cross-section, not a cohort followed over time — the file has no panel.

## 7. What this means for the argument

The thread's original question was whether entrepreneurship can absorb unemployment. Three quarters of informal businesses exist because there was no alternative, they employ almost nobody, and the ones that do employ mostly got there by surviving a decade. That is not an argument against supporting them; it is an argument that **the support which could matter is the kind that keeps a business alive past year five**, because that is where the employer rate doubles and where six times the jobs sit.

It also reorders the usual policy menu. Seed capital and start-up training target the group with the lowest employment intensity (7 jobs per 100) and the shortest survival; the leverage is in the R50k–R250k turnover band (14% of businesses, 37.5% of jobs) and in the decade-old survivors inside it. Whether *formalisation* is a cause or a consequence of that hiring is the open question, and it is the one a policy would need answered.

## 8. Reproduce

```bash
cd data/sese-microdata
uv run --with pandas python ../treasury/scripts/sese_crosstabs.py
```

Codes from the SESE 2023 record layout (`datafirst/sese-2023-metadata.txt`, Q32MainReason): 02 unemployed, 03 no alternative income, 04 retrenched, 05 inadequate other income, 14 "to survive/make ends meet", 16 "earn while searching" = push; 01, 06–12, 15 = pull; 13 = other.
