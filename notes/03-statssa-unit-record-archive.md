# Stats SA's iSiBaloweb: the unit-record archive we should have started with

*Copied from the working notes of the session that produced this repo. Internal file paths (`data/sa-entrepreneurship/…`, `notes/2026-11-23-…`) refer to that workspace; the data layout here is documented in `../data/README.md`.*

*2026-11-23. Tim pointed at the iSiBaloweb domain and its Product Access accordions. It is not a PDF portal — it is Stats SA's ungated **unit-record archive**: nearly every household and establishment survey, back to 2000, as CSV/SPSS/SAS/STATA, with no registration and no application. This note is the map plus what we pulled.*

## 1. The access finding (this is the practical bit)

Two different things on the same host:

- **The HTML pages are behind Incapsula bot protection.** A plain client gets a 1 158-byte challenge shell — the same wall that blocked Stats SA from a headless fetch earlier in this thread. So the navigation cannot be crawled with curl.
- **The files download directly.** `GET /data/PSS/HSS/SESE/SESE2023.zip` returns 200 with `Content-Length` and no challenge at all. Same for `/metadata/...` PDFs.

So the workflow is: **enumerate in a real browser, fetch the files with curl.** That is what `scripts/statsa_fetch.py` does — it never touches the pages, only the file list it is handed.

Two more properties worth knowing:

- Navigation is a `<select>`, not links. The survey → year → file tree lives in `<option value="…">`, so an anchor-only extractor finds nothing (mine did, and returned zero surveys until I parsed options).
- File naming is regular: `/data/PSS/HSS/<SURVEY>/[<YEAR>/]<SURVEY><YEAR>[<QUARTER>].zip`, with `SPSS`/`SAS`/`STATA` suffixes for those formats.

## 2. The map (what exists)

| Survey | Years available | Notes |
|---|---|---|
| **SESE** (informal businesses) | **2009, 2013, 2017, 2023** | CSV. 2013 also ships `SESE2013WORKER.csv`, which is **the same 2 031 records with the `Uqno` identifier replaced by a row number** (all 175 other columns identical, same order) — a de-identified twin, **not** employee-level records. Corrected below |
| **QLFS** | **2008 Q1 – 2026 Q3**, every quarter | the labour series in full |
| **LMD** (Labour Market Dynamics) | **2008 – 2024**, annually | four QLFS quarters stacked, **plus earnings variables not in the quarterly releases** |
| **LFS** (pre-QLFS labour force) | **2000 – 2007**, twice a year | the pre-2008 history |
| **GHS** | 2002 – 2025 | household access to services, informal activity |
| **IES** (Income & Expenditure) | 1995, 2000, 2006, 2011, **2023** | household **and business** income |
| **LCS** | 2009, 2015 | living conditions/poverty |
| **Census** | 1970, 1980, 1985, 1991, 1996, 2001, 2011, **2022** | metadata pages here; products via `census.statssa.gov.za` |
| **Community Survey** | 2007, 2016 | mid-census estimates |
| DTS / NHTS / GPSJS / VCS | 2008–2024 / periodic / 2019–2026 / periodic | tourism, travel, governance & safety, crime |
| **Vital registration** | RLB, **Causes of Death 2024**, marriages & divorces | from Home Affairs records |
| SAYP, VAS, TUS | periodic | child work, volunteering, time use |

**Separately, the ETS pages are *aggregate time series*, not unit records** — monthly, quarterly and annual, as Excel/ASCII/JSON. Seventeen monthly series, including **Liquidations and Insolvencies (P0043.1) from 2000**. Useful, different kind of object.

## 3. What we pulled (11 files, 77 MB)

`data/sa-entrepreneurship/statsa-units/`, hashes and status in `manifest.tsv`:

| File | Zip | Unpacks to | Why this one |
|---|---|---|---|
| `SESE2017.zip` | 119 KB | 629 KB CSV | informal sector, wave 3 |
| `SESE2013.zip` | 255 KB | 692 KB + 667 KB de-identified twin | wave 2. The second file is the same records with `Uqno` stripped — no extra information |
| `SESE2009.zip` | 123 KB | 594 KB CSV | wave 1 — extends the 2023 analysis back 14 years |
| `LMD2024.zip` | 16.2 MB | **741 MB CSV** | 4 quarters stacked + earnings; the employer-count and informal-earnings source |
| `QLFS202603.zip` | 4.1 MB | **202 MB CSV** | latest quarter |
| `QLFS200801.zip` | 3.3 MB | — | first quarter of the series (2008 definition, pre-2014 reweighting) |
| `IES2023.zip` | 31.4 MB | — | household and business income |
| `LFS200003.zip`, `LFS200709.zip` | 1.4 / 3.4 MB | — | the pre-QLFS labour series, oldest and newest |
| `Excel Table from 2000 onwards.xlsx` | 58 KB | 331 date columns | **monthly liquidations by industry, 2000 →** |
| `ASCII Liquidations.txt` | 60 KB | — | same series, flat |

Extraction is the trap: two small zips become **almost 1 GB** of CSV. Extracted on demand, not kept.

## 4. What this changes for the thread

Three of the four things the thread kept describing as missing now have a route:

- **Informal series** — SESE 2009/2013/2017 against 2023 gives five waves (2001 and 2005 are not on this portal; the release PDFs are). That turns the informal numbers from a snapshot into a trend, with the caveat that variable names drift between waves.
- **The 717k vs 283k employer gap** — QLFS 2026 Q3 and LMD 2024 both carry employment status on the person record, so the QLFS side can be computed directly rather than quoted from a table. That is the single most valuable check available now.
- **Business deaths** — liquidations from 2000 monthly by industry is a real formal-failure series, and it is the closest thing to the "70–80% fail" number anyone cites. (It measures *liquidations*, which is the small tail of exits, but over 26 years it is a genuine series rather than a claim.)

What it does **not** fix: there is still no panel with business identifiers, so survival curves by entry cohort remain out of reach. LMD's stacked quarters and QLFS's rotating panel design get close on the *labour* side (the same individuals appear in consecutive quarters), not the *business* side.

## 5. Traps, recorded

- **Incapsula on pages, open files.** Enumerate in a browser; never expect curl to read the navigation.
- **`<select>` navigation** — parse `option` values, not anchors.
- **CSV vs SPSS vs SAS vs STATA** are separate zips; the plain `.zip` is the CSV.
- **Unpacked size ≠ zip size** (16 MB → 741 MB).
- **Census microdata** is not in this archive; the census pages here only carry metadata, with products on `census.statssa.gov.za`.
- **2001 and 2005 SESE waves and 1996/2001 census products** are not on iSiBaloweb — those genuinely require the main site or DataFirst.
- The ETS Excel layout is a **wide matrix** (terms in rows, dates across 331 columns), not tidy data — it needs transposing before use.

## 6. Reproduce

```bash
cd data/sa-entrepreneurship
python3 scripts/statsa_fetch.py statsa-units/priority-urls.txt   --out statsa-units
python3 scripts/statsa_fetch.py statsa-units/priority-urls-2.txt --out statsa-units
```
The manifest merges across runs (two runs writing one path truncated each other once — fixed).

Enumeration was done in the browser through the Product Access accordion:
`/pages/labour.php`, `/pages/social.php`, `/pages/povertyinquality.php`,
`/pages/vital.php`, `/pages/dataapps.php`, plus
`/pages/surveys/ets/{monthly,quarterly,annual}/`.

## 7. Correction: `SESE2013WORKER.csv` is not employee-level data

I described it as "the only wave with employee-level records" when I found the file. It isn't. Every one of the 175 non-key columns matches `SESE2013.csv` row for row, and the row order is the same; the only difference is that `Uqno` — a long record identifier (`101000220000002801`) — is replaced by a serial number (`1`, `2`, …). It is a de-identified twin of the same 2 031 business records. There is no employee-level SESE file in any wave, so any question about the employees *of* informal businesses (as opposed to how many there are) remains unanswerable from this source.
