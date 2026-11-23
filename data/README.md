# data/

Not committed. Everything here is public and should be fetched from source; this file documents
the layout the scripts expect so a re-fetch lands in the right place.

```
data/
├── statsa/
│   ├── sese/SESE2023.csv            # SESE 2023 unit records (1 583 × 201, 3.5 MB)
│   ├── qlfs/QLFS202603/QLFS202603.csv   # QLFS 2026 Q3 unit records (202 MB unpacked)
│   └── work/                        # scratch: unzipped waves, fetch manifests
│       ├── sese2009/SESE2009.csv
│       ├── sese2013/SESE2013.csv
│       ├── sese2017/SESE2017.csv
│       └── manifest.tsv             # url, status, bytes, sha256, path
└── treasury/
    ├── 2025 Tax Statistics - Chapter {2,3,4}*.xlsx
    ├── 2025_Tax_Statistics_main.pdf
    ├── budget2026_FullBR.pdf
    ├── budget2026_FullENE.pdf
    ├── vulekamali-ENE-2026-pivot.csv
    └── 0xMMYYYY.json                # eTenders OCDS packages
```

## Where each file comes from

| File | Source |
|---|---|
| SESE 2009 / 2013 / 2017 / 2023 | `https://isibaloweb.statssa.gov.za/data/PSS/HSS/SESE/SESE<year>.zip` — the plain zips are CSV; SPSS/SAS/STATA are separate |
| QLFS | `https://isibaloweb.statssa.gov.za/data/PSS/HSS/QLFS/<year>/QLFS<year><quarter>.zip` — every quarter 2008 Q1 → 2026 Q3 |
| Labour Market Dynamics (annual, with earnings) | `https://isibaloweb.statssa.gov.za/data/PSS/HSS/LMD/LMD<year>.zip` |
| Tax Statistics chapters | `https://www.sars.gov.za/about/sars-tax-and-customs-system/tax-statistics/` → chapter zips (`.xlsx` inside) |
| Budget Review 2026 | `https://www.treasury.gov.za/documents/National%20Budget/2026/review/FullBR.pdf` |
| Estimates of National Expenditure 2026 | `https://www.treasury.gov.za/documents/National%20Budget/2026/ene/FullENE.pdf` |
| ENE pivot (vote × programme × subprogramme) | `https://vulekamali.gov.za/datasets/estimates-of-national-expenditure/resources/Budget_2026_-_ENE_and_Appropriation_Pivot.csv` |
| eTenders OCDS packages | `https://data.etenders.gov.za/Home/DownloadFile/?fileName=0xMMYYYY.json` (JSON carries values; the CSVs do not) |
| Older SESE waves, IES, GHS, census | same iSiBaloweb pattern; `scripts/statsa_catalogue.py` enumerates the whole tree |

## Fetching

```bash
# a file list, one request at a time with a manifest and hashes
python3 scripts/statsa_fetch.py data/urls.txt --out data/statsa/work

# enumerate the whole unit-record archive (run the pages through a browser first —
# the HTML is Incapsula-protected, see the repo README)
python3 scripts/statsa_catalogue.py > data/catalogue.tsv
```

## Traps

- **Extraction is the surprise**: a 16 MB LMD zip unpacks to 741 MB; a 4 MB QLFS zip to 202 MB. Extract on demand.
- **Missing values are `1.79769313486232e+308`** (max double) in the 2023 SESE file, not blank or `-9`. Every script strips it.
- **Reason codes are not stable across SESE waves**: 2009 code 2 merges "unemployed" with "no alternative income" and code 3 is "retrenched"; from 2013 they split (2, 3) and retrenched moves to 4. Codes 14–16 only exist from 2017.
- **Annual turnover is missing for all under-a-year businesses** in SESE 2023 (asked only of 12-month+ operations), so no age × turnover comparison exists.
