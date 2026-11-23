# QLFS employer counts, and the gap that wasn't there

*Copied from the working notes of the session that produced this repo. Internal file paths (`data/sa-entrepreneurship/…`, `notes/2026-11-23-…`) refer to that workspace; the data layout here is documented in `../data/README.md`.*

*2026-11-23. Computed from QLFS 2026 Q3 unit records (`statssa-units/data/QLFS202603.zip`), codebook from the same release's metadata PDF. This closes the "717k vs 283k" discrepancy I raised earlier in the thread — it was my error, not the data's.*

## 1. The numbers (QLFS Q3 2026, weighted)

| | Persons |
|---|---|
| Employed | 17 055 243 |
| — formal sector | 12 482 479 |
| — **informal sector** | **3 535 437** |
| — private households | 1 037 327 |

By status in employment (ICSE-18, `Ste_icse18_authority`):

| | Persons | of which formal sector | of which **informal** |
|---|---|---|---|
| **Employers** | **767 894** | 481 383 | **286 512** |
| Own-account workers | 1 840 184 | 373 850 | 1 466 334 |
| Dependent contractors | 482 589 | — | 389 625 |
| Employees | 13 906 756 | — | 1 354 618 |
| Contributing family workers | 57 820 | — | 38 348 |

The informal sector decomposes as 286 512 employers + 1 466 334 own-account + 389 625 dependent contractors + 1 354 618 employees + 38 348 family workers = 3 535 437. **Half of all employers in South Africa are informal-sector employers.**

## 2. The reconciliation

| Source | Informal-sector employers | Year |
|---|---|---|
| **QLFS 2026 Q3** (ICSE-18 employer, informal sector) | **286 512** | 2026 |
| **SESE 2023** (businesses with any employees) | **283 348** | 2023 |

**1.1% apart, three years and two instruments.** There is no 2.5× discrepancy. What happened: earlier in this thread I read "employer 795k" from the LMIS/QLFS status series as *informal* employers, and carried "717k" into two notes, the hand-off and my summary to Tim as an unreconciled gap on the most important number in the argument. It is the **national total** (767 894 here), of which 481 383 are formal and 286 512 informal. I mistook a total for a subset.

The consistency also survives a mechanical check: among informal-sector self-employed, the number who answer "yes" to hiring (`Q413aHIRE`) is **286 512** — exactly the ICSE employer count, because the classification is derived from that question. Two independent derivations, same number.

## 3. What else the same file settles

- **VAT and owners.** Of 2 608 078 self-employed people (all sectors): **466 552 are VAT-registered (17.9%)**, and **767 894 hire anyone (29.4%)**. VAT-registered owners are **43% of employers** — 329 957 of 767 894 — while 428 493 employers are not VAT-registered.
- **QLFS's informal sector is narrower than SESE's population, not wider.** By construction, informal-sector self-employed are excluded from VAT *and* income-tax registration (the `Sector` derivation uses Q4.13 VAT, Q4.13b registration, Q4.13c incorporation, Q4.14 income tax and Q4.14b bookkeeping). SESE only excludes VAT. So QLFS informal ⊆ SESE — and they still produce the same employer count, which says the income-tax-registered-but-not-VAT group is small.
- **Employees per employer**: informal employers report **2.13** workers (median 2), formal **2.90** (median 2), all **2.61** (`Q416NRWORKERS`). SESE's 1.82 *paid* employees per employing business is lower because SESE counts paid employees only and excludes agriculture and private households; QLFS counts everyone in the establishment. Different denominators, same order of magnitude — worth stating whenever the two are put side by side.

## 4. What is still unreconciled (smaller, and real)

Informal-sector **employees** total **1 354 618**, but informal *employers* × their reported workers is 286 512 × 2.13 ≈ 611 000. The remaining ~740 000 informal employees are attached to establishments whose owner is classified elsewhere — dependent contractors, own-account operators who nonetheless have help, or owners who are registered in a way that keeps them out of the informal sector while their staff's establishment test (fewer than five employees, no income tax deducted) puts the *employees* inside it. The QLFS `Sector` variable is derived per person, so employee and owner can land in different sectors. I have not taken that apart, and it does not affect the employer count.

## 5. Reproduce

```bash
cd data/sa-entrepreneurship/statsa-units/work && unzip -o ../data/QLFS202603.zip
uv run --with pandas python ../../scripts/qlfs_employers.py
```

Codebook: `metadata/QLFS/2026/Qtr03/…metadata.pdf` on iSiBaloweb (fetched to `/tmp/qlfs_meta.txt` while working; the definitions used here are quoted from it — `Sector` 1/2/3 = formal/informal/households, `Ste_icse18_authority` 1–5 = employer/own-account/dependent contractor/employee/family).

## 6. Corrections this forces

- `notes/2026-11-23-sese-2023-microdata-first-analysis.md` §5 said the QLFS/SESE gap was "2.5× on the single number that decides whether informal firms create jobs". **Wrong** — the two agree to 1.1%.
- Addendum 5 of the SA inventory note carries the same wrong claim.
- The hand-off entry for this session carries it too.
- The *substantive* conclusion is unaffected and in fact strengthened: **283–287k informal employers, ~26–30 paid jobs per 100 informal businesses**, and the middle of the turnover distribution does the hiring. The number is now confirmed by two official instruments rather than asserted from one.
