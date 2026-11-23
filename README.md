# sa-sme-data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24467168.svg)](https://doi.org/10.5281/zenodo.24467168)

What South Africa's public data says about small business and entrepreneurship: the inventory, the numbers, and the scripts that re-derive every figure.

The short answer is in **[BRIEF.md](BRIEF.md)** (1,200 words). The working is in [`notes/`](notes/).

## What this is

An evidence base, not an argument. It answers four questions from published South African data and says plainly where the data stops:

1. **How many businesses are there, and how big?** 1.98m non-VAT businesses and 1.4m companies expected to file; the median informal business turns over **R16 000 a year** and **85.7% employ nobody**.
2. **Who employs people?** **26 paid jobs per 100 informal businesses.** Employment is a function of age, not intent: 7 jobs per 100 under a year, **43 at ten years and more**. Firms older than five years hold 52% of employers and 60% of paid jobs.
3. **What happens over time?** Informal-sector businesses grew **64% between 2009 and 2023**, but from 2013 to 2023 employers fell 27% and paid jobs 25%. Ten-year survival of VAT-registered businesses is **53.6%**.
4. **What does the state spend, and on what?** ~R3.0bn through the department, **R8.4bn through the tax code**, and **36% of R328.66bn of procurement** to suppliers under R50m turnover — with the only growing programme aimed at the informal tier.

## Reports

| File | What it is |
|---|---|
| [BRIEF.md](BRIEF.md) | The 1,200-word brief: entrepreneurship as a jobs strategy, tested against the public data |
| [notes/01-data-inventory.md](notes/01-data-inventory.md) | Every source found, what it covers, what is blocked and why |
| [notes/02-treasury-sars-tax-statistics.md](notes/02-treasury-sars-tax-statistics.md) | Company register ladder, size distribution, the 10-year VAT survival cohort |
| [notes/03-statssa-unit-record-archive.md](notes/03-statssa-unit-record-archive.md) | Stats SA's iSiBaloweb: which surveys publish unit records, and how the access works |
| [notes/04-sese-2023-microdata.md](notes/04-sese-2023-microdata.md) | First pass on the SESE 2023 unit-record file, with the validation |
| [notes/05-who-employs.md](notes/05-who-employs.md) | Cross-tabs: employment by business age, motive, turnover and formalisation |
| [notes/06-qlfs-employer-reconciliation.md](notes/06-qlfs-employer-reconciliation.md) | QLFS vs SESE employer counts — they agree to 1.1% |
| [notes/07-informal-sector-series.md](notes/07-informal-sector-series.md) | Four SESE waves harmonised, deflated, 2009 → 2023 |
| [notes/08-lmis-inventory.md](notes/08-lmis-inventory.md) | The DEL Labour Market Information System (SDMX API), and why it adds little |
| [notes/09-procurement-dashboard.md](notes/09-procurement-dashboard.md) | Treasury's procurement dashboard: spend by supplier size and designated group |

## Data you have to fetch yourself

No raw data is committed — most of it is tens of megabytes and all of it is better obtained from source. **[data/README.md](data/README.md)** documents the expected layout; **`scripts/statsa_fetch.py`** and **`scripts/statsa_catalogue.py`** do the fetching and enumeration.

Two quirks worth knowing before you start:

- Stats SA's **iSiBaloweb pages are behind Incapsula** (a plain client gets a 1 KB challenge shell) while **the files under `/data/` download directly**. Enumerate in a browser, fetch with curl.
- The site's navigation is a `<select>`, so survey → year → file lives in `<option value>`, not in anchors.

## Reproducing the numbers

```bash
# informal sector, 2023: counts, turnover, employment
uv run --with pandas python scripts/sese_microdata.py

# who employs people, and why
uv run --with pandas python scripts/sese_crosstabs.py

# the 2009 -> 2023 series (needs the three older waves unzipped into data/statsa/work)
uv run --with pandas python scripts/sese_series.py

# QLFS employer counts (needs QLFS202603 unzipped)
uv run --with pandas python scripts/qlfs_employers.py

# company Register ladder, size distribution, VAT survival cohort
uv run --with openpyxl python scripts/treasury_numbers.py

# programme-level spending (vulekamali ENE pivot)
uv run --with pandas python scripts/ene_pivot.py
```

Every published figure in the notes came out of one of these; where a number could not be re-derived, the note says so.

## Known limits

- **No panel.** There is no public dataset with business identifiers across time, so survival *curves* by entry cohort cannot be computed — only aggregate survival.
- **No formal-firm employment.** The company tax return has no employment field; the Quarterly Employment Survey reports by industry and establishment. Firm-level employment exists for the informal sector only (SESE).
- **A third of procurement spend is unclassifiable.** 32.98% of FY2025/26 spend sits on suppliers with no turnover recorded, so the SME share is 36.05% of all spend or ~53.8% of classified spend, and the data cannot say which.
- **One series is broken by policy**: the VAT registration threshold rises from R1m to R2.3m on 1 April 2026, below which sat 47.8% of active vendors. VAT-based populations are not comparable across 2025/26 → 2026/27.

## Corrections

Four errors found in this work are recorded in place rather than tidied away: a mis-built download URL that made vulekamali look dead; a claim that the procurement dashboard lacked contractor size (it doesn't — it is just not downloadable); reading a national employer total as an informal subset (the "2.5× gap" that does not exist); and describing a de-identified SESE twin file as employee-level data. Each is marked as a correction where it appears.

## Licence

Code MIT, prose and derived tables CC BY 4.0. Upstream sources keep their own terms — see [NOTICE.md](NOTICE.md). Nothing here redistributes source data.

## Citing this

Archived on Zenodo. Use the **concept DOI** to cite "this work, any version", or the
version DOI to cite exactly what you read:

- Concept DOI (always resolves to the latest version): [`10.5281/zenodo.24467168`](https://doi.org/10.5281/zenodo.24467168)
- This version (`v0.1.0`): [`10.5281/zenodo.24467169`](https://doi.org/10.5281/zenodo.24467169)

```bibtex
@software{evertse_sa_sme_data_2026,
  author    = {Evertse, Tim},
  title     = {sa-sme-data: what South Africa's public data says about small business and entrepreneurship},
  year      = {2026},
  version   = {v0.1.0},
  doi       = {10.5281/zenodo.24467169},
  url       = {https://github.com/realtimshady16/sa-sme-data}
}
```

For a *figure*, cite the primary publisher (Stats SA, SARS/National Treasury, National
Treasury) as named in [NOTICE.md](NOTICE.md); for the *analysis*, cite this repository.

## Citation

Metadata in [CITATION.cff](CITATION.cff).
