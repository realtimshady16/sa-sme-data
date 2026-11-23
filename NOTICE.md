# Upstream sources and their terms

Nothing in this repository redistributes source data. Where a figure is derived from
a published table or a unit-record file, the source is named in the note that uses it
and in `data/README.md`. Terms that matter if you reuse or republish anything here:

| Source | Publisher | Terms |
|---|---|---|
| **Tax Statistics** (2025 edition and earlier) | National Treasury / SARS | Joint publication, site footer "all rights reserved". Quote and derive; don't redistribute the tables. |
| **Budget Review** and **Estimates of National Expenditure** | National Treasury | Government publication; attribution expected. |
| **vulekamali** ENE pivot | National Treasury / IMALI YETHU | Open budget data portal; attribute National Treasury and vulekamali. |
| **SESE / QLFS / LMD / IES / GHS** unit records | Statistics South Africa (iSiBaloweb) | Stats SA's own data-use terms apply. Files are published for download without registration; attribute "Statistics South Africa". No raw data is committed here. |
| **eTenders OCDS** packages | National Treasury | ODC-PDDL 1.0 (public domain dedication): https://opendatacommons.org/licenses/pddl/1-0/ |
| **Procurement Dashboard** | National Treasury | A Power BI report with no export. The figures in `notes/09-procurement-dashboard.md` are transcribed from its accessibility layer, with the filter state recorded, and are CC BY 4.0 *as a transcription* — the underlying data is Treasury's. |
| **World Bank CPI** (`FP.CPI.TOTL`, ZAF) | World Bank | CC BY 4.0. Used only for the deflators in `scripts/sese_series.py`. |
| **DEL LMIS** (SDMX) | Department of Employment and Labour | Site footer "all rights reserved"; no open licence. `notes/08-lmis-inventory.md` treats it as personal research use with attribution. |

If you are reusing a *number*: cite the primary publisher, not this repo. If you are
reusing the *analysis*: CC BY 4.0, cite this repo.
