# The informal-sector series, 2009 → 2023: more businesses, fewer employers

*Copied from the working notes of the session that produced this repo. Internal file paths (`data/sa-entrepreneurship/…`, `notes/2026-11-23-…`) refer to that workspace; the data layout here is documented in `../data/README.md`.*

*2026-11-23. Four SESE waves harmonised from Stats SA unit records (2009, 2013, 2017, 2023). Script `scripts/sese_series.py`; deflators from World Bank CPI for ZAF. This is the "series rather than the answer" version of `notes/2026-11-23-brief-entrepreneurship-jobs.md`.*

## 1. Validation first, because harmonising four waves is where errors live

| Wave | Records | Weighted business records | Published (persons) | Diff | Necessity share (mine) | Published |
|---|---|---|---|---|---|---|
| 2009 | 1 944 | 1 205 724 | 1 144 000 | +5.4% | 67.5% | 68.3% |
| 2013 | 2 031 | 1 601 112 | 1 517 000 | +5.5% | 68.2% | 69.2% |
| 2017 | 1 658 | 1 890 452 | 1 793 000 | +5.4% | 62.0% | 63.5% |
| 2023 | 1 583 | 1 978 211 | 1 873 000 | +5.6% | 56.2% | 57.1% |

Two things to read from this. The **+5.5% gap is structural and stable** — a row is a *business*, and the published total counts *persons*, ~5.5% of whom run more than one. It is the same in all four waves, which is what a correct weighting looks like. The **necessity share is 0.8–1.5 points below** the published figure in every wave: a systematic understatement, consistent with the published table being computed on unrounded microdata. Close enough to trust the direction across waves.

Reason codes had to be remapped, and this is the kind of thing that silently ruins a series: **in 2009 code 2 is "unemployed / no alternative income" merged and code 3 is "retrenched"; from 2013 they split into 2 = unemployed and 3 = no alternative income, with retrenched moving to 4.** Codes 14–16 ("to survive/make ends meet", "own boss", "earn while searching") exist only from 2017. So the comparable measure is `{2}` in 2009 and `{2,3}` afterwards, and the broader "push" grouping used in the cross-tab note **cannot** be extended backwards.

## 2. The series

| | 2009 | 2013 | 2017 | 2023 |
|---|---|---|---|---|
| **Businesses** (weighted records) | 1 205 724 | 1 601 112 | 1 890 452 | **1 978 211** |
| **Employers** | 228 388 | **389 966** | 364 652 | 283 348 |
| **Paid employees** | 340 363 | **689 987** | 619 545 | 514 568 |
| % of businesses that employ anyone | 18.9% | 24.4% | 19.3% | **14.3%** |
| Paid jobs per 100 businesses | 28.2 | 43.1 | 32.8 | **26.0** |
| Paid employees per employing business | 1.49 | 1.77 | 1.70 | **1.82** |
| Median annual turnover (nominal) | R9 600 | R12 000 | R18 000 | R16 000 |
| **Median annual turnover (2023 rand)** | **R19 469** | **R19 908** | **R24 012** | **R16 000** |
| Median monthly profit (nominal) | R600 | R1 000 | R1 500 | R2 000 |
| Median monthly profit (2023 rand) | R1 217 | R1 659 | R2 001 | R2 000 |
| % started out of necessity | 67.5% | 68.2% | 62.0% | **56.2%** |
| % in business 10 years or more | 19.4% | 20.1% | 22.2% | 22.7% |
| % in business under a year | 20.9% | 20.2% | 17.8% | 16.3% |
| % with a licence | 12.2% | 12.7% | 8.5% | 11.0% |
| % registered for income tax | 6.6% | 9.6% | 4.7% | 7.5% |

## 3. Three findings that survive the caveats

**(a) The sector grew; its employment did not.** Businesses rose 64% between 2009 and 2023, paid employees 51% — but all of that gain happened by 2013. **From 2013 to 2023 the number of businesses grew 24% while employers fell 27% and paid jobs fell 25%.** The employer rate halved from its 2013 peak (24.4% → 14.3%), and jobs per 100 businesses fell from 43 to 26. Measured this way, the informal sector has been *demerging*: more and smaller units, fewer of them hiring.

**(b) Real earnings per business are flat to falling.** In 2023 rand the median informal business turned over **R19 469 in 2009, R19 908 in 2013, R24 012 in 2017 and R16 000 in 2023** — i.e. a real rise to 2017, then a fall that puts it *below* where it started fourteen years earlier. The nominal numbers doubled; the real ones did not. This is the series' strongest result and it does not depend on any single wave's methodology.

**(c) The one positive trend is motive.** The necessity share fell from 68.2% (2013) to **56.2%** (2023), and the published tables show the same fall (69.2 → 63.5 → 57.1), so it is not an artefact of my coding. Fewer businesses are being started purely because there was nothing else — even as the sector's employment intensity fell.

## 4. What must not be read as a trend

- **2009 → 2013 is a break, not growth.** Employer count up 71% and paid jobs up 103% in four years. SESE rides on QLFS weights and the QLFS was reweighted after a census (last reweighting 2014), so a level shift is the plausible explanation. **Use 2013 → 2023 for change; treat 2009 as a level observation under a different weight regime.**
- **"Share under R50k turnover" rises mechanically** across waves (88.7% → 83.1% → 80.1% → 76.4% *of disposers*): the bracket is nominal and fourteen years of inflation move businesses through it. Only the deflated medians mean anything.
- **The licence and income-tax series are not monotonic** (12.2 → 12.7 → 8.5 → 11.0 and 6.6 → 9.6 → 4.7 → 7.5). Those dips look like questionnaire/fieldwork changes rather than formalisation collapsing and recovering. Do not plot them as a trend.
- **The stock ageing** (10+ years: 19.4% → 22.7%) would normally *raise* the employer rate, since older businesses employ more. It fell instead. So composition is working against the employment trend — the decline in (a) is if anything understated by the age effect, but the interaction is not something these four cross-sections can separate.

## 5. One internal inconsistency worth stating

In 2023 the **median monthly profit is R2 000, i.e. R24 000 a year, against a median annual turnover of R16 000**. The same population cannot have profits exceeding turnover. At least one of the two questions is badly answered — most likely turnover is often reported as a monthly figure, or profit is reported gross — and **the level of either should not be quoted**. That bites on the brief, which quotes both medians: the turnover figure is at least consistent with the employment gradient (the employment question is independent of both), the profit figure is not usable at all.

## 6. What it adds to the brief

The brief says entrepreneurship in South Africa is mostly survival and that jobs come from surviving firms. The series adds three things it could not have known from 2023 alone:

1. **The informal sector's employment intensity is falling, not rising** — a sector that doubled in size while losing a quarter of its paid jobs is not a jobs engine that needs more entrants.
2. **Real turnover per business has not improved in fourteen years.** Any claim that informal enterprise is "growing" has to contend with a median that is lower in real terms than in 2009.
3. **Fewer businesses start from pure necessity** — the policy story is improving on the motive axis while worsening on the employment axis, which suggests entry is not the binding constraint.

## 7. Reproduce

```bash
cd data/sa-entrepreneurship/statsa-units/work
unzip -o ../data/SESE2009.zip -d sese2009 && unzip -o ../data/SESE2013.zip -d sese2013 \
  && unzip -o ../data/SESE2017.zip -d sese2017
uv run --with pandas python ../../scripts/sese_series.py
```

Deflators: World Bank `FP.CPI.TOTL` for ZAF (2010 = 100), ratio to 2023 — 2009 ×2.028, 2013 ×1.659, 2017 ×1.334.

Column crosswalk and the reason-code remap are documented in the script header. `SESE2013WORKER.csv` is the same 2 031 records as `SESE2013.csv` with the `Uqno` identifier replaced by a row number — all 175 other columns identical, same order. It is a de-identified twin, not employee-level data (corrected from my first reading; see the archive note §7).
