# SESE 2023 microdata: the first firm-level employment numbers for the informal sector

*Copied from the working notes of the session that produced this repo. Internal file paths (`data/sa-entrepreneurship/…`, `notes/2026-11-23-…`) refer to that workspace; the data layout here is documented in `../data/README.md`.*

*2026-11-23. Tim downloaded `SESE2023.zip` from Stats SA directly (3 stall 532 700-byte CSV, 25 April 2025 inside the zip, 1 583 records × 201 variables, `Weight` included). It is the unit-record file, not the documentation — which is what the earlier thread had and what the inventory note said was missing. This note is the first pass at it, and it overturns one of my own claims.*

File: `data/sa-entrepreneurship/sese-microdata/SESE2023.csv`. Reproduce with `scripts/sese_microdata.py`. Weighted throughout (`Weight`); unweighted n = 1 583 business records for 1 482 persons.

## 1. It checks out

Before trusting a file I didn't download, three checks:

| Check | Microdata | Published (SESE 2023 report) |
|---|---|---|
| Weighted population | 1 842 709 persons / **1 978 211 business records** | **1 873 000** persons running a business |
| Sex of owner | men **57.6%**, women **42.4%** | men 57.7%, women 42.3% |
| Businesses per person | 6.2% of persons run more than one | 1.6% run more than one (98.4% run one) |

Two stronger checks, because counts and a sex split could pass on the wrong file:

**(a) The turnover distribution reproduces Table 17 band for band.** Weighted `Q48TURNOVERLSTMNTH` against the report's published monthly-turnover counts:

| Band (last calendar month) | Report | Microdata | Diff |
|---|---|---|---|
| R0–100 | 11.4% | 11.2% | −0.1 |
| R101–350 | 5.8% | 6.0% | +0.2 |
| R351–750 | 11.6% | 11.6% | −0.0 |
| R751–1 500 | 15.4% | 15.5% | +0.1 |
| R1 501–3 000 | 20.0% | 19.8% | −0.2 |
| R3 001–6 000 | 15.3% | 15.2% | −0.2 |
| R6 001–15 000 | 12.4% | 12.6% | +0.2 |
| R15 001+ | 8.0% | 8.0% | −0.0 |

Every band within 0.2 points on eight cells. That validates the weights *and* the variable interpretation together — if either were wrong, this would not line up.

**(b) The paid/unpaid split reconciles once the base is aligned.** Among the 283k businesses with workers: 81.7% have paid employees only or with unpaid help, 10.1% have unpaid help only, and 8.3% record neither (a data artefact). Excluding that 8.3%, the paid share is **89.0%** against the report's Figure 26 figure of **88.7%** for 2023.

**The one discrepancy** is businesses-per-person: the file carries 101 second/third businesses (6.2% of persons run more than one) against the report's 1.6%, which is why the weighted row total is 1.98m businesses but the weighted person total is 1.87m and matches the report. So the file has more multi-business records than the tabulation reflects. Use **1.98m businesses** for per-business arithmetic and **1.87m owners** for per-person claims — the 26 jobs per 100 businesses becomes 27.5 per 100 if you divide by persons instead.

*(Also verified: record and variable counts — 1 583 × 201 — are exactly what the DataFirst catalogue states for this study, so this is the same file the catalogue distributes, obtained without the registration step.)*

No names, addresses, ID numbers or coordinates in the file — only `Geo_Type_Code` (urban/rural) and province/metro. Safe to handle; kept local and untracked anyway.

## 2. The finding: 26 paid jobs per 100 informal businesses, and it is not evenly spread

| | Estimate | Share |
|---|---|---|
| Businesses with **no employees at all** (owner working alone) | **1 694 863** | **85.7%** |
| Businesses with any paid or unpaid workers | 283 348 | 14.3% |
| **Paid employees** across all informal businesses | **514 568** | — |
| Unpaid (family) workers | 90 008 | — |

- **26 paid jobs per 100 informal businesses**, 30.6 including unpaid help.
- The 283k employing businesses carry **1.82 paid employees each** — 37.8% of them have exactly one, another 22.5% have two, and 5.8% have six or more.
- So the informal sector is, overwhelmingly, **one person selling to stay alive**. 1.69m businesses produce no wage at all.

**Employment rises steeply with turnover** — but the jobs themselves come from the middle of the distribution, not from the micro tail and not from the handful at the top:

| Annual turnover | Businesses | % of sector | Share that employ anyone | Paid jobs per 100 businesses | Paid jobs | % of all paid jobs | records |
|---|---|---|---|---|---|---|---|
| Reported zero | 63 822 | 3.2% | 19.0% | 32.7 | 20 874 | 4.1% | 43 |
| R1 – R50k | 996 718 | 50.4% | 9.8% | 15.4 | 153 555 | 29.8% | 832 |
| **R50k – R250k** | **277 169** | **14.0%** | **32.6%** | **69.6** | **192 785** | **37.5%** | 205 |
| R250k – R500k | 29 374 | 1.5% | 16.9% | 36.0 | 10 563 | 2.1% | 17 |
| R500k + | 21 260 | 1.1% | 59.4% | 156.5 | 33 280 | 6.5% | 14 |
| Not disclosed | 589 869 | 29.8% | 11.2% | 17.5 | 103 512 | 20.1% | 472 |
| **Total** | **1 978 211** | 100% | 14.3% | **26.0** | **514 568** | 100% | 1 583 |

Read three ways:

- **Per business**, the gradient is stark: 9.8% of sub-R50k businesses employ anyone, against 32.6% in the R50k–R250k band and 59.4% above R500k. Intensity rises ~10× from the bottom band to the top.
- **In volume**, it is the **R50k–R250k band** that carries the jobs — 14% of the sector supplying 37.5% of paid employment. The sub-R50k half supplies 29.8%; the 1.1% above R500k supplies 6.5%. *I first wrote that "job creation is in the top 1.1%", which is true per business and false in total; the middle does the work.*
- **Counts get thin fast.** The two top bands rest on 17 and 14 records, so treat their levels (36 and 156 per 100) as noisy even though the direction is clear. The R50k–R250k band rests on 205 records and is the one worth quoting.

The shape is the same one the VAT cohort showed from the other side (§5 of the Treasury note) — a thin middle doing the hiring. It also explains why the "85% are survivalist" framing was doing too much work: 50% of the sector turns over under R50k and hires almost nobody, but that is *not* where the informal jobs are.

## 3. What they earn, and what they turn over

| | Estimate |
|---|---|
| Median annual turnover (non-zero) | **R16 000** (p25 R6 000, p75 R48 000, p90 R120 000) |
| Turnover **not disclosed** | **29.8%** (589 869) |
| Businesses reporting **zero turnover** for the last 12 months | 3.2% (63 822) |
| Share of *all* businesses turning over under R50 000 a year | **53.6%** |
| Share of *disclosing* businesses turning over under R50 000 | **76.4%** |
| Median monthly **net profit** (non-zero) | **R2 000** |
| Businesses reporting **zero profit** last month | 25.2% (498 989) |
| Weighted mean monthly profit | R3 350 (**R40 200 a year**) |

*(Corrected after a first pass: my table had lumped the 29.8% who did not disclose turnover in with the 3.2% who reported zero, which inflated "zero turnover" from 3.2% to 33% and pushed the under-R50k share to 83.4%. The disclosing and non-disclosing groups behave differently — 11.2% of non-disclosers employ someone, against 14.3% overall — so conflating them biases the distribution. The bands in §2 are now computed on disclosed turnover only.)*

Median turnover of R16k a year is about **R1 300 a month**. These are not micro-enterprises waiting to grow; they are income supplements and last-resort work. That is consistent with the 57.1% "unemployment or no alternative income" start reason already in the inventory note, and it is what "entrepreneurship fixes unemployment" has to contend with — not because the businesses are unserious but because at this turnover none of them can pay a wage.

## 4. Age profile (with a caveat that kills the naive reading)

| Age of business | Weighted | Share |
|---|---|---|
| Less than a year | 321 797 | 16.3% |
| 1 but less than 3 years | 442 159 | 22.4% |
| 3 but less than 5 years | 335 829 | 17.0% |
| 5 but less than 10 years | 410 903 | 20.8% |
| 10 years or more | 449 933 | 22.7% |
| Don't know | 17 590 | 0.9% |

**Don't read "10+ is the biggest bucket" as longevity**: the buckets are unequal widths (1 year, 2, 2, 5, unbounded). Per year of age, the density is 16.3% in year one, 11.2%/yr in 1–3, 8.5%/yr in 3–5, 4.2%/yr in 5–10 and ≤2.3%/yr at 10+. So the hazard is highest at the start and falls with age, which is the ordinary shape. This is a *cross-section*, so it cannot separate births from deaths — the identification problem from the Treasury note is not solved by having the microdata, only made better-specified.

## 5. What this changes

- **It kills my own claim.** I wrote in the Treasury note (§11) and said in the session that "nothing public links a business to the number of people it employs". That is false for the informal sector and was false the whole time: SESE has asked for employee counts since 2001, and the microdata has them at unit level with weights. The correct statement is narrower: **there is no firm-level employment data for the *formal* segment** (nothing in the company tax return, QES is by establishment and industry, ETI is claimant-only), and **no panel** anywhere.
- **It converts the "informal sector" from a count into a distribution.** The inventory note could say 1.9m owners existed; it can now say what they turn over, earn, and employ, and that 85.7% employ nobody.
- **It sharpens the jobs argument.** The earlier framing was "85% of informal businesses are survivalist". The defensible version is: **83.4% turn over under R50k and employ 15–19 paid workers per 100 businesses, while the 1.1% above R500k employ 157 per 100.** Concentration, not average, is the story.
- **The apparent QLFS gap closed, and it closed in SESE's favour.** I wrote that QLFS counts 717k informal-sector employers against SESE's 283k — a 2.5× gap. Computing it from the QLFS Q3 2026 unit records instead of quoting a table gives **286 512 informal-sector employers**, against SESE's **283 348**: a **1.1% difference across three years and two instruments**. The 717k figure was the *national total* of employers (767 894, of which 481 383 formal), which I had read as the informal subset. **Correction (same day): there is no 2.5× gap — QLFS Q3 2026 puts informal-sector employers at 286 512 against SESE's 283 348, a 1.1% difference; the 717k I quoted was the national total of employers, not the informal subset.** See `notes/2026-11-23-qlfs-employer-count-reconciliation.md`.

## 6. Caveats

- **Small sample, heavy tails.** 1 583 records for 1.98m businesses. The R250k–R500k band rests on 29k weighted businesses; anything finer than the cuts above (province × industry × employees) will be noise. Cell counts are reported above so they can be judged.
- **Missingness is not random in the direction that matters.** 29.8% don't disclose turnover, and non-disclosure is *higher among own-account businesses* (30.9%) than employers (23.3%), so the turnover distribution is biased toward larger businesses. The employment numbers don't depend on this, the turnover ones do.
- **Sentinels.** Missing values are stored as `1.79769313486232e+308` (max double), not blank or `-9`. Anyone re-using this file must strip it or every mean is wrong.
- **No panel.** One wave, self-reported, no business identifiers across time. Survival still can't be measured here.
- **There is no codebook in the zip**, and the CSV's variable names do not match the 2023 questionnaire (`Q53EMPLOYER` is an employment question here but Q53 on the paper form is "how much did you pay off"; the age band lives in `Q31BUSSTARTED` though the form asks it at Q43). So variable meanings were **inferred from value distributions and then validated against published tables** — solid for turnover, sex and the employee counts, and only plausible for the age bands, `Q10BINDUSCODE` industry codes, and start reasons. Anything quoted from those three should be checked against the release report first.
- **Scope.** Non-VAT-registered businesses, excluding agriculture and private households — so 1.98m is a subset of all informal activity, and the smallest businesses (subsistence farming, domestic work) are outside it.
- **Licence**: Stats SA publishes SESE under its own data-use terms; this is personal research use with attribution to Stats SA, and the raw file is not committed.

## 7. Reproduce

```
cd data/sa-entrepreneurship/sese-microdata
uv run --with pandas python ../treasury/scripts/sese_microdata.py
```

Source: `SESE2023.csv` (3 532 700 bytes, from `SESE2023.zip`, downloaded from Stats SA 2026-11-23). Questionnaire, release report and record layout are in `data/sa-entrepreneurship/datafirst/`.

## Glossary

- **Weight**: inverse selection probability, so weighted sums estimate the population. Every number in §2–§4 is weighted.
- **Own-account worker**: self-employed with no employees — the international definition of the self-employed-without-workers category, and 85.7% of this population.
- **Paid vs unpaid employee**: `Q541PDLSTYEAR` / `Q541UNPDLSTYEAR` are counts of employees paid in cash or kind vs not paid (family labour).
- **Non-VAT-registered**: the SESE inclusion rule. Wider than "informal", narrower than "all business".
