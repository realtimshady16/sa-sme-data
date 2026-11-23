# South Africa's LMIS: inventory, download, and reconciliation against QLFS

*Copied from the working notes of the session that produced this repo. Internal file paths (`data/sa-entrepreneurship/…`, `notes/2026-11-23-…`) refer to that workspace; the data layout here is documented in `../data/README.md`.*

**2026-11-23 · research note · data source: Department of Employment and Labour (DEL) Labour Market Information System**

## TL;DR

The LMIS is a real, working **SDMX** data platform. Its front end is a SIS-CC ".Stat Suite" data explorer at `de-lmis.labour.gov.za`, backed by an SDMX REST API at `sdmx-lmis.labour.gov.za/rest`. Of **118 dataflows**, **98 return real data** (downloaded in full as SDMX-CSV into `data/sa-entrepreneurship/lmis/raw/`), **19 return nothing** (15 × "mapping set" 404, 4 × a 422 structure bug), and **1 is a leftover pentest artifact** (not touched).

The reconciliation is decisive but nuanced: **the LMIS's QLFS-derived numbers are bit-for-bit identical to Stats SA's QLFS** (verified on total employed, unemployment, labour force, and status-in-employment for the overlapping quarters) — so it is *real, current QLFS data*, **not** an independent source (the data footnotes read "Source: StatsSA QLFS"). But it **lags Stats SA's own releases** (nothing past **2026-Q2** anywhere; Q3 2026 is absent), and the series Tim most wants — **informal employment levels and any "sector" split — are the empty ones**.

Every dataflow is annotated `NonProductionDataflow=true` and every data message carries the SDMX **`test: true`** flag. So the platform is explicitly marked non-production, even though the data it serves is real.

---

## 1. Jargon (defined once)

- **SDMX** — the international standard (Statistical Data and Metadata eXchange) for publishing statistical data as machine-readable REST APIs. The LMIS speaks SDMX 2.1.
- **Dataflow** — one named dataset (e.g. "Employment by sex and age"). The unit I inventoried. 118 of them.
- **DSD (Data Structure Definition)** — the schema of a dataflow: which dimensions it has (e.g. `SEX`, `AGE`, `REF_AREA` = province, `TIME_PERIOD`) and their code lists. Several dataflows share one DSD.
- **Mapping set / "Mapping Store"** — in this particular server ("NSI Web Service", the .Stat Suite stack), data queries look up a *mapping* from dataflow → underlying dataset. A dataflow with no mapping returns 404 `"does not contain a mapping set"` — i.e. **the structure exists but no data has been loaded for it**.
- **ICSE-93 vs ICSE-18** — two classification standards for "status in employment". ICSE-93 (used by QLFS Table 3.6 and by the LMIS `SIE` dimension): Employee / Employer / Own-account worker / Unpaid household member. ICSE-18 (QLFS Table 3.6b, not in the LMIS) uses a different "type of authority" split.
- **Informal sector vs informal employment** — not the same thing. *Informal sector* = jobs in informal-sector enterprises (narrower). *Informal employment* = jobs lacking formal protection, whether in informal or formal enterprises or households (broader, the 19th ICLS concept). The LMIS only has "informal **employment** (non-agriculture)", never "informal **sector**".

## 2. Access method (how to repeat)

The earlier aborted run's probe files (`data/sa-entrepreneurship/lmis/probe/`) were correct about the base URL but **wrong in its provisional conclusion** that the API might be empty — that came from testing a single dataflow that happens to be one of the empty ones. The working recipe:

```bash
# list all dataflows (structure JSON)
curl -s -H "Accept: application/vnd.sdmx.structure+json;version=1.0" \
  "https://sdmx-lmis.labour.gov.za/rest/dataflow/all/all/latest?references=none"

# full data for one dataflow, all breakdowns, full time span, as CSV
curl -s -H "Accept: application/vnd.sdmx.data+csv;version=1.0" \
  "https://sdmx-lmis.labour.gov.za/rest/data/ZA110,DF_UNE_SEX_PROV,1.0/all?dimensionAtObservation=AllDimensions"
```

- The key segment `all` (one `.` per dimension also works) plus **no** `startPeriod`/`endPeriod` returns the full span.
- Agency is `ZA110`, version `1.0`. SDMX-CSV (`application/vnd.sdmx.data+csv;version=1.0`) worked for every flow that has data; SDMX-JSON (`application/vnd.sdmx.data+json;version=2.0`) also works. Both were exercised.
- **Captcha is not actually gating anything.** The app config has `hasCaptcha: true` but `captchaSiteKey: ""` (empty), so no captcha is configured. I made all requests as ordinary public GETs with `User-Agent: personal-research-script (low-volume, single user)`, one request at a time, ≥4 s apart.
- The front end also has a separate **search/metadata** service at `sfs-lmis.labour.gov.za/api/search` (a Solr/ES-style index) which returns dimension code lists (e.g. `Sex: Total#_T#, Male#M#, Female#F#`) and `indexationDate` per flow. Not needed for data, useful for labels.

Reproducibility: `scripts/sweep.py` does the full 118-flow sweep and writes `manifest.tsv`. `scripts/probe_data.py` is the smaller probe. Run with `python3 -I`.

## 3. Headline numbers

| | count |
|---|---|
| Dataflows registered | 118 |
| Return data (downloaded in full, SDMX-CSV) | **98** |
| Return nothing | 19 (15 × 404 "mapping set", 4 × 422 structure bug) |
| Pentest artifact (not queried) | 1 (`ZZ_PENTEST_I26224`) |

Downloads: `data/sa-entrepreneurship/lmis/raw/` (98 files, one per dataflow, named by id). Provenance (request URL, retrieved-at, rows, sha256, status, period span, notes): `data/sa-entrepreneurship/lmis/manifest.tsv`.

## 4. Is the data non-production / test?

**Yes, the platform is explicitly flagged as non-production — but the data content is real.**

Three independent signals agree:

1. Every one of the 118 dataflows carries the annotation **`NonProductionDataflow=true`** and `isFinal=false` in the structure registry.
2. Every data response (SDMX-JSON) carries **`meta.test: true`** with sender id `LMIS_-_DEL_za`. I checked this on `DF_UNE_SEX_PROV`, `DF_EMP_SEX_AGE`, `DF_LF_SEX_AGE`, `DF_TVET_ENROL_PRG_SEX`, `DF_WAP_SEX_LMS` — all `test=true`.
3. The front-end footer reads **"Copyright 2024. All rights reserved."** with a "Terms & conditions" link that is a **placeholder** pointing at `http://www.example.org/`.

What this *means*: the labels look like a development/launch artifact that was never flipped to production, rather than "the numbers are fake". The numbers are real — see §5. But a "non-production" label is what it is: **treat the LMIS as a preview/beta service, not a citable production source**, until DEL flips those flags. Nothing I found says the *values* are dummy data (they aren't), but the *service* is not declared production-ready.

## 5. Reconciliation against QLFS Q3 2026

Tim's QLFS Q3 2026 figures (thousands): total employed 16 840; informal sector 3 476; formal sector 12 340; household sector 1 024; employers 717; own-account 2 046; unemployment rate 33.7%. (All confirmed present in `data/sa-entrepreneurship/raw/qlfs_q3_2026.txt`, P0211, released 10 Nov 2026.)

**Finding 1 — the QLFS-derived flows are exact copies, and they pass trivially.**

LMIS `DF_EMP_SEX_AGE` (total, both sexes, all ages) vs QLFS "Total employed":

| quarter | LMIS | QLFS | match |
|---|---|---|---|
| 2025-Q4 | 17 099 | 17 099 | ✅ exact |
| 2026-Q1 | 16 754 | 16 754 | ✅ exact |
| 2026-Q2 | 16 739 | 16 739 | ✅ exact |

LMIS unemployment / labour force, 2026-Q2: unemployed **8 481**, labour force **25 220** → rate **8 481 ÷ 25 220 = 33.6%**, which is QLFS Q2 2026's official rate (33.6%) exactly. Status-in-employment, LMIS `DF_EMP_SEX_SIE` 2026-Q2 vs QLFS Table 3.6 (ICSE-93): Employee 13 815, Employer 795, Own-account worker 2 047, Unpaid household member 81 — **all four exact matches** (QLFS Q2 2026: 13 815 / 795 / 2 047 / 81).

**Finding 2 — the LMIS is not an independent source; it mirrors QLFS.** The data footnotes literally read `Source: StatsSA QLFS`. So "does the LMIS confirm QLFS?" is the wrong question — it *is* QLFS, re-served through DEL's API. The one genuinely independent thing about it is the *delivery channel* (SDMX API), not the numbers.

**Finding 3 — Q3 2026 does not exist in the LMIS.** The newest period anywhere in the 98 downloaded flows is **2026-Q2**, and coverage is ragged: most QLFS flows run 2008-Q1 → 2026-Q2, but province-level employment stops at 2025-Q4, the unemployment *rate* flows stop at **2025-Q2**, and the informal-employment *rate* flows stop at **2024-Q4**. The LMIS lags Stats SA by one to several quarters depending on the series. So the reconciliation against **Q3 2026** can only be done by proxy: the latest LMIS quarter (Q2 2026) matches QLFS exactly, which is strong evidence the platform is a faithful mirror — but Q3 2026 itself is simply absent.

**Finding 4 — the "informal sector" split is not in the LMIS at all.** There is no *sector* dimension (formal/informal/households) in any dataflow. The closest concept, "informal employment (non-agriculture)", is (a) a different, broader concept than "informal sector", and (b) broken: all four **level** flows (`DF_IE_SEX_*`) return 404 (no data mapped), and the **rate** flows (`DF_IER_SEX_*`) stop at 2024-Q4. So **Tim's informal-sector figure (3 476) cannot be checked against the LMIS** — the data isn't there. Separately, the QLFS itself notes (P0211 line 177) that formal/informal sector *and* employment definitions "have undergone significant revisions" (move to the 19th ICLS, agriculture now folded into the sector split), which is an extra reason the old "non-agriculture" LMIS informal-employment series won't line up with the new sector figures.

**Verdict (one sentence):** the LMIS is a faithful but lagging mirror of QLFS for the standard labour-market indicators (exact match on everything that overlaps), and it has **no usable informal-sector data** — so for Tim's informal-sector question it is neither an independent cross-check nor a usable source, at least as it stands today.

## 6. Licence / terms

- Footer: **"Copyright 2024. All rights reserved."** (Department of Employment and Labour, with Statistics South Africa as "powered by").
- The **"Terms & conditions"** link resolves to **`http://www.example.org/`** — a placeholder. There is **no real licence or terms-of-use document** published on the site.
- The API returns no licence headers. I found **no open-data licence** (no CC, no "data may be reused" statement). Practical reading: the data is QLFS data (Stats SA's P0211, itself under Stats SA's standard release terms), re-served by DEL with "all rights reserved". **Do not treat these downloads as openly licensed**; the T&C gap is itself a finding.
- Context links on the site: "LMIS Master Plan" → `ee.labour.gov.za/DMISO/Final LMIS Master Plan_South Africa with DEL and StatsSA 2024.pdf`; "Report" → `ee.labour.gov.za/DMISO/South African youth and adults labour market trends 2021 to 2025.pdf`. I did not read either PDF's full text (different host, not needed for the licence question).

## 7. What is / isn't here for "informal sector, small business, entrepreneurship"

**Is here (and downloadable):**
- **Own-account workers and employers** — `DF_EMP_SEX_SIE` (status in employment, ICSE-93), exact QLFS, 2008-Q1 → 2026-Q2, by sex. This is the single best entrepreneurship *proxy* in the LMIS: own-account workers (2 047k, Q2 2026) ≈ self-employed without employees, employers (795k) ≈ business owners with staff. A companion rate `DF_POACFW_SEX_REF_AREA` ("proportion of own-account + contributing family workers in total employment") exists but stops at 2023-Q3.
- **Informal employment *rate*** — `DF_IER_SEX_EDU`, `DF_IER_SEX_MTS`, `DF_IER_SEX_REF_AREA` (by education / marital status / **province**), 2008-Q1 → 2024-Q4. National informal-employment rate (non-agriculture) 2024-Q4: **30.5%**, ranging by province from **21.4% (Northern Cape)** to **43.2% (Mpumalanga)**. *Rate only — no headcount.*
- **Industry (ECO)**, but only via `DF_EMP_INV_ECO` ("Employees involved by economic activity", 2021-Q1 → 2025-Q4), plus GDP, strikes, UIF-claims and job-opportunity flows that carry the ECO dimension. 9 industries + total (Agriculture, Mining, Manufacturing, Utilities, Construction, Trade, Transport, Finance, Community/social services).
- **Workseeker / opportunities** (DEL's own administrative data, genuinely *not* QLFS): `DF_WOKRS_REG_*` (registered workseekers), `DF_WOKRS_CNSL` (counselled), `DF_WORKS_PLC_REF_AREA` (placements), `DF_ESSA_OPP_REF_AREA` (ESSA opportunities registered), `DF_JOI_*` (Job Opportunity Index). These are the LMIS's "native" series.
- **TVET enrolment** — `DF_TVET_ENROL_PRG_SEX`, but it is a single annual snapshot (2022 only), not a series.

**Is *not* here:**
- **No "sector" split** (formal / informal / households) anywhere — so no direct informal-sector counts.
- **No informal-employment *headcounts*** — the `DF_IE_SEX_*` level flows are all empty (404).
- **No metro / municipal geography.** `REF_AREA` is the 9 provinces + national total only. "By province" is the finest spatial breakdown.
- **No informal employment × industry.** There is no informal-employment flow with the ECO dimension.
- **No startup / SMME / business-registration / firm-count data.** The LMIS is a *labour-market* platform (jobs, unemployment, labour relations, UIF, strikes), not an enterprise platform. "Entrepreneurship" is only reachable by proxy (own-account/employer status, informal-employment rate).

## 8. What could not be downloaded, and why

**15 flows → 404 `"does not contain a mapping set"`** (structure registered, no data loaded):
`DF_FOREIGN_EXC_EXC_RT` (foreign exchange), `DF_IER_SEX_AGE` (informal-employment rate by age), **all four `DF_IE_SEX_*` informal-employment level flows**, `DF_OCB_SEX_ECO`, `DF_SENAE_SEX_AGE`, `DF_SENAE_SEX_EDU`, `DF_TRUR_SEX_AGE`, `DF_TRUR_SEX_POPG`, `DF_UIC_AGE`, `DF_UNER_SEX_AGE` (unemployment rate by age), `DF_WORKF_ECO` (workforce by industry). One more, `DF_UIC_AGE_REF_AREA`, returned a *different* 404: `NoRecordsFound` (mapping exists, but no records under the `all` key).

**4 flows → 422** `"Data Structure … does not contain component with id: REF_AREA"` — a server-side bug where the NSI web service tries to attach a province (`REF_AREA`) component to schemas that don't have one (`DSD_ECO_SEX`, `DSD_AGE`): `DF_EMP_SEX_ECO` (employment by sex **and industry** — the one that would matter for entrepreneurship-by-industry), `DF_SENAE_SEX_ECO`, `DF_TRU_SEX_ECO`, `DF_WOKRS_REG_AGE`. I read the exact error body for all four; it is the same message. This looks fixable on DEL's side (the constraint is misconfigured), not something a client can work around with a different key.

Net effect for Tim's interest: the two *industry* breakdowns of employment that a researcher would reach for (`DF_EMP_SEX_ECO` employment-by-sex-by-industry, `DF_WORKF_ECO` workforce-by-industry) are **broken/empty**; the only working employment-by-industry series is the oddly named `DF_EMP_INV_ECO` ("employees involved").

## 9. Full dataflow table

118 rows. `period` is the min–max of `TIME_PERIOD` actually returned (from the CSV, not the registry). "no" = nothing downloadable; reasons in §8. Dimensions come from the CSV header where downloaded, else the DSD name.

| id | name | category | dimensions | period | rows | dl |
|---|---|---|---|---|---|---|
| DF_ARBTR_REF_AREA_ARBTR_STATUS | Arbitration by province and arbitration status | Arbitration (CCMA) | FREQ+INDICATOR+REF_AREA+ARBTR_STATUS+TIME_PERIOD | 2022..2023 | 60 | yes |
| DF_BCEA_INSP_INSP_COMPL | Basic condition of employment act inspection by compliance | Inspection | REF_AREA+FREQ+INDICATOR+INSP_COMPL+TIME_PERIOD | 2022-M01..2025-M12 | 144 | yes |
| DF_BCEA_WORKS_INSP_REF_AREA | Basic condition of employment act workplaces inspection by province | Inspection | FREQ+INDICATOR+REF_AREA+TIME_PERIOD | 2022-M01..2025-M12 | 480 | yes |
| DF_CCMA_AWARD_REF_AREA_AWARD_IN_FAVR | Commission for conciliation mediation and arbitration awards by province and awards in favour | CCMA awards | FREQ+INDICATOR+REF_AREA+AWARD_IN_FAVR+TIME_PERIOD | 2022..2023 | 80 | yes |
| DF_CONCL_REF_AREA_CONCL_STATUS | Conciliations by province and conciliation status | Conciliation (CCMA) | FREQ+INDICATOR+REF_AREA+CONCL_STATUS+TIME_PERIOD | 2022..2023 | 60 | yes |
| DF_EE_INSP_REF_AREA | Employment equity inspections by province | Inspection | FREQ+INDICATOR+REF_AREA+TIME_PERIOD | 2022-M01..2023-M12 | 240 | yes |
| DF_EMP_INV_ECO | Employees invloved by economic activity | Employment | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2021-Q1..2025-Q4 | 192 | yes |
| DF_EMP_SEX_AGE | Employment by sex and age | Employment | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2008-Q1..2026-Q2 | 1332 | yes |
| DF_EMP_SEX_ECO | Employment by sex and economic activity | Employment | DSD_ECO_SEX(1.0) |  | 0 | no |
| DF_EMP_SEX_EDU | Employment by sex and highest level of education | Employment | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2026-Q2 | 1776 | yes |
| DF_EMP_SEX_MTS | Employment  by sex and marital status | Employment | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2026-Q2 | 1314 | yes |
| DF_EMP_SEX_OCU | Employment by sex and occupation | Employment | REF_AREA+FREQ+INDICATOR+SEX+OCU+TIME_PERIOD | 2008-Q1..2026-Q2 | 2658 | yes |
| DF_EMP_SEX_POPG | Employment  by sex and population group | Employment | REF_AREA+FREQ+INDICATOR+SEX+POPG+TIME_PERIOD | 2008-Q1..2026-Q2 | 1095 | yes |
| DF_EMP_SEX_REF_AREA | Employment by sex and province | Employment | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2025-Q4 | 4200 | yes |
| DF_EMP_SEX_SIE | Employment  by sex and status in employment | Employment | REF_AREA+FREQ+INDICATOR+SEX+SIE+TIME_PERIOD | 2008-Q1..2026-Q2 | 1095 | yes |
| DF_EMP_SEX_UHRS | EMPLOYMENT BY SEX AND USUAL HOURS OF WORK | Employment | REF_AREA+FREQ+INDICATOR+SEX+UHRS+TIME_PERIOD | 2008-Q1..2026-Q2 | 1332 | yes |
| DF_EPR_SEX_AGE | Employment-to-population ratio by sex and age | Employment | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2008-Q1..2026-Q2 | 1332 | yes |
| DF_EPR_SEX_EDU | Employment-to-population ratio by sex and highest level of education | Employment | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2025-Q4 | 1728 | yes |
| DF_EPR_SEX_MTS | Employment-to-population ratio by sex and marital status | Employment | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2026-Q2 | 1314 | yes |
| DF_EPR_SEX_POPG | Employment-to-population ratio by sex and population group | Employment | REF_AREA+FREQ+INDICATOR+SEX+POPG+TIME_PERIOD | 2008-Q1..2026-Q2 | 1110 | yes |
| DF_EPR_SEX_REF_AREA | Employment-to-population ratio by sex and province | Employment | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2026-Q2 | 2190 | yes |
| DF_ESSA_OPP_REF_AREA | ESSA opportunities registered by province | Opportunities registered | FREQ+INDICATOR+REF_AREA+TIME_PERIOD | 2021-Q1..2025-Q4 | 200 | yes |
| DF_FOREIGN_EXC_EXC_RT | Foreign exchange by exchange rate | Foreign exchange | DSD_EXC_RT(1.0) |  | 0 | no |
| DF_GDP_ECO | Gross domestic product (Seasonally adjusted and annualised) | GDP (Stats SA) | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2008-Q1..2023-Q4 | 640 | yes |
| DF_IER_SEX_AGE | Informal employment rate by sex and age (non-agriculture) | Informal employment | DSD_AGE_SEX(1.0) |  | 0 | no |
| DF_IER_SEX_EDU | Informal employment rate by sex and highest level of education (non-agriculture) | Informal employment | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2024-Q4 | 1632 | yes |
| DF_IER_SEX_MTS | Informal employment rate by sex and marital status (non-agriculture) | Informal employment | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2024-Q4 | 1206 | yes |
| DF_IER_SEX_REF_AREA | Informal employment rate by sex and province (non-agriculture) | Informal employment | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2024-Q4 | 2010 | yes |
| DF_IE_SEX_AGE | Informal employment by sex and age (non-agriculture) | Informal employment | DSD_AGE_SEX(1.0) |  | 0 | no |
| DF_IE_SEX_EDU | Informal employment by sex and highest level of education (non-agriculture) | Informal employment | DSD_EDU_SEX(1.0) |  | 0 | no |
| DF_IE_SEX_MTS | Informal employment by sex and marital status (non-agriculture) | Informal employment | DSD_MTS_SEX(1.0) |  | 0 | no |
| DF_IE_SEX_REF_AREA | Informal employment by sex and province (non-agriculture) | Informal employment | DSD_SEX(1.0) |  | 0 | no |
| DF_INACTR_SEX_AGE | Inactivity rate by sex and age group | Inactivity | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2008-Q1..2026-Q2 | 1332 | yes |
| DF_INACTR_SEX_EDU | Inactivity rate by sex and highest level of education | Inactivity | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2026-Q2 | 1776 | yes |
| DF_INACTR_SEX_MTS | Inactivity rate by sex and marital status | Inactivity | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2026-Q2 | 1314 | yes |
| DF_INACTR_SEX_POPG | Inactivity rate by sex and population group | Inactivity | REF_AREA+FREQ+INDICATOR+SEX+POPG+TIME_PERIOD | 2008-Q1..2026-Q2 | 962 | yes |
| DF_INACTR_SEX_REF_AREA | Inactivity rate by sex and province | Inactivity | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2026-Q2 | 2190 | yes |
| DF_JOI_ECO | Job opportunity index by economic activity | Job opportunity index | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2021-M01..2025-M12 | 660 | yes |
| DF_JOI_OCU | Job opportunity index by occupation | Job opportunity index | REF_AREA+FREQ+INDICATOR+OCU+TIME_PERIOD | 2021-M01..2025-M12 | 539 | yes |
| DF_JOI_REF_AREA | Job opportunity index by Province | Job opportunity index | FREQ+INDICATOR+REF_AREA+TIME_PERIOD | 2021-Q1..2025-Q4 | 200 | yes |
| DF_LFPR_SEX_AGE | Labour force participation rate by sex and age | LF participation rate | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2008-Q1..2026-Q2 | 1332 | yes |
| DF_LFPR_SEX_EDU | Labour force participation rate by sex and highest level of education | LF participation rate | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2024-Q4 | 1632 | yes |
| DF_LFPR_SEX_MTS | Labour force participation rate by sex and marital status | LF participation rate | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2026-Q2 | 1314 | yes |
| DF_LFPR_SEX_POPG | Labour force participation rate by sex and population group | LF participation rate | REF_AREA+FREQ+INDICATOR+SEX+POPG+TIME_PERIOD | 2008-Q1..2026-Q2 | 1110 | yes |
| DF_LFPR_SEX_REF_AREA | Labour force participation rate by sex and province | LF participation rate | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2026-Q2 | 2190 | yes |
| DF_LF_SEX_AGE | Labour force by sex and age | Labour force | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2008-Q1..2026-Q2 | 1314 | yes |
| DF_LF_SEX_EDU | Labour force by sex and highest level of education | Labour force | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2026-Q2 | 1752 | yes |
| DF_LF_SEX_MTS | Labour force by sex and marital status | Labour force | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2026-Q2 | 1314 | yes |
| DF_LF_SEX_POPG | Labour force by sex and population group | Labour force | REF_AREA+FREQ+INDICATOR+SEX+POPG+TIME_PERIOD | 2008-Q1..2026-Q2 | 1095 | yes |
| DF_LF_SEX_REF_AREA | Labour force by sex and province | Labour force | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2026-Q2 | 2190 | yes |
| DF_NEETR_SEX_REF_AREA | NEET Rate | NEET | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2012-Q4..2024-Q4 | 1440 | yes |
| DF_OCB_SEX_AGE | Ordinary unemployment claim benefits by sex and age | Unemployment claim benefits | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2020-M01..2025-M12 | 1008 | yes |
| DF_OCB_SEX_BNT | Ordinary unemployment claim benefits by sex and benefity type | Unemployment claim benefits | FREQ+INDICATOR+SEX+BNT+TIME_PERIOD | 2020-M01..2025-M12 | 1080 | yes |
| DF_OCB_SEX_ECO | Ordinary unemployment claim benefits by sex and economic activity | Unemployment claim benefits | DSD_ECO_SEX(1.0) |  | 0 | no |
| DF_OCB_SEX_EDUC | Ordinary unemployment claim benefits by sex and education | Unemployment claim benefits | FREQ+INDICATOR+SEX+EDUC+TIME_PERIOD | 2020-M01..2025-M12 | 1152 | yes |
| DF_OCB_SEX_REF_AREA | Ordinary unemployment claim benefits by sex and province | Unemployment claim benefits | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2020-M01..2025-M12 | 1440 | yes |
| DF_OCB_SEX_TERM_RSN | Ordinary unemployment claim benefits by sex and terminiation reason | Unemployment claim benefits | REF_AREA+FREQ+INDICATOR+SEX+TERM_RSN+TIME_PERIOD | 2020-M01..2025-M12 | 864 | yes |
| DF_POACFW_SEX_REF_AREA | Proportion of own-account workers and contributing family workers in total employment by sex and province | Own-account share | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2023-Q3 | 1764 | yes |
| DF_RFRL_REF_AREA_JURISD_STATUS | Referrals by province and jurisdictional status | Referrals (CCMA) | FREQ+INDICATOR+REF_AREA+JURISD_STATUS+TIME_PERIOD | 2021..2023 | 120 | yes |
| DF_SENAE_SEX_AGE | Share of wage employment in non-agricultural employment by sex and age | Employment | DSD_AGE_SEX(1.0) |  | 0 | no |
| DF_SENAE_SEX_ECO | Share of wage employment in non-agricultural employment by sex and economic activity | Employment | DSD_ECO_SEX(1.0) |  | 0 | no |
| DF_SENAE_SEX_EDU | Share of wage employment in non-agricultural employment by sex and highest level of education | Employment | DSD_EDU_SEX(1.0) |  | 0 | no |
| DF_STR_REC_DISP_RESL | Strikes recorded by disputes resolved | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+DISP_RESL+TIME_PERIOD | 2022-Q1..2024-Q4 | 72 | yes |
| DF_STR_REC_DWS | Strikes recorded by duration of work stoppages | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+DWS+TIME_PERIOD | 2022-Q1..2024-Q4 | 60 | yes |
| DF_STR_REC_ECO | Strikes recorded by economic activity | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2021-Q1..2024-Q4 | 160 | yes |
| DF_STR_REC_EMPL_SIZ | Strikes recorded by employment size | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+EMPL_SIZ+TIME_PERIOD | 2022-Q1..2024-Q4 | 84 | yes |
| DF_STR_REC_NOS | Strikes recorded by nature | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+NOS+TIME_PERIOD | 2022-Q1..2024-Q4 | 84 | yes |
| DF_STR_REC_PRNCP_CAUS | Strikes recorded by principal cause | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+PRNCP_CAUS+TIME_PERIOD | 2022-Q1..2024-Q4 | 132 | yes |
| DF_STR_REC_RLUDR | Strikes recorded by replacement labour used during strike | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+RLUDR+TIME_PERIOD | 2022-Q1..2024-Q4 | 36 | yes |
| DF_STR_REC_STR_COMPL | Strikes recorded by compliance | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+STR_COMPL+TIME_PERIOD | 2022-Q1..2024-Q4 | 48 | yes |
| DF_STR_REC_WDL_ORG | Strikes recorded by work days lost by organisation | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+WDL_ORG+TIME_PERIOD | 2022-Q1..2024-Q4 | 72 | yes |
| DF_TRUR_SEX_AGE | Time related underemployment rate by sex and age | Time-related underemployment | DSD_AGE_SEX(1.0) |  | 0 | no |
| DF_TRUR_SEX_POPG | Time-related underemployment rate by sex and population group | Time-related underemployment | DSD_POPG_SEX(1.0) |  | 0 | no |
| DF_TRU_SEX_AGE | Time-related uderemployment by sex and age | Time-related underemployment | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2008-Q1..2025-Q4 | 1278 | yes |
| DF_TRU_SEX_ECO | Time-related underemployment by sex and economic activity | Time-related underemployment | DSD_ECO_SEX(1.0) |  | 0 | no |
| DF_TRU_SEX_EDU | Time-related underemployment by sex and highest level of education | Time-related underemployment | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2025-Q4 | 1704 | yes |
| DF_TRU_SEX_MTS | Time-related underemployment by sex and marital status | Time-related underemployment | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2025-Q4 | 1278 | yes |
| DF_TRU_SEX_OCU | Time-related underemployment by sex and occupation | Time-related underemployment | REF_AREA+FREQ+INDICATOR+SEX+OCU+TIME_PERIOD | 2008-Q1..2025-Q4 | 2583 | yes |
| DF_TRU_SEX_POPG | Time-related underemployment by sex and population group | Time-related underemployment | REF_AREA+FREQ+INDICATOR+SEX+POPG+TIME_PERIOD | 2008-Q1..2025-Q4 | 1062 | yes |
| DF_TRU_SEX_REF_AREA | Time-related underemployment by sex and province | Time-related underemployment | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2025-Q4 | 2160 | yes |
| DF_TUM_COLTV_BARG_MEMB | Trade union membership by collective bargaining membership | Trade union membership | REF_AREA+FREQ+INDICATOR+COLTV_BARG_MEMB+TIME_PERIOD | 2020..2023 | 16 | yes |
| DF_TUM_ECO_REF_AREA | Trade union membership by economic activity and province | Trade union membership | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2022..2024 | 330 | yes |
| DF_TVET_ENROL_PRG_SEX | Enrolment cycle count of students in TVET colleges for NC(V) Level 2-4 programmes by gender | TVET enrolment | FREQ+INDICATOR+PRG+SEX+TIME_PERIOD | 2022..2022 | 40 | yes |
| DF_UIC_AGE | Unemployment insurance claims by age | UIF claims | DSD_AGE(1.0) |  | 0 | no |
| DF_UIC_AGE_ECO | Unemployment insurance claims by age and economic activity | UIF claims | FREQ+INDICATOR+REF_AREA+AGE+ECO+TIME_PERIOD | 2021-M07..2023-M06 | 1440 | yes |
| DF_UIC_AGE_REF_AREA | Unemployment insurance claims by age and province | UIF claims | DSD_AGE(1.0) |  | 0 | no |
| DF_UIC_AGE_TERM_RSN | Unemployment insurance claims by age and reason for termination | UIF claims | REF_AREA+FREQ+INDICATOR+AGE+TERM_RSN+TIME_PERIOD | 2021-07..2023-06 | 840 | yes |
| DF_UIC_BNT | Unemployment insurance claims by benefit type | UIF claims | REF_AREA+FREQ+INDICATOR+BNT+TIME_PERIOD | 2021-M01..2023-M09 | 198 | yes |
| DF_UIC_ECO | Unemployment insurance claims by economic activity | UIF claims | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2021-M01..2023-M12 | 432 | yes |
| DF_UIC_EDUC | Unemployment insurance claims by education | UIF claims | REF_AREA+FREQ+INDICATOR+EDUC+TIME_PERIOD | 2020-M01..2023-M12 | 384 | yes |
| DF_UIC_REF_AREA | Unemployment insurance claims by province | UIF claims | FREQ+INDICATOR+REF_AREA+TIME_PERIOD | 2021-M01..2023-M12 | 360 | yes |
| DF_UIC_REF_AREA_ECO | Unemployment insurance claims by province and economic activity | UIF claims | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2021-M01..2023-M12 | 2562 | yes |
| DF_UIC_TERM_RSN | Unemployment insurance claims by reason for termination | UIF claims | REF_AREA+FREQ+INDICATOR+TERM_RSN+TIME_PERIOD | 2021-M01..2024-M06 | 252 | yes |
| DF_UNER_SEX_AGE | Unemployment rate by sex and age | Unemployment | DSD_AGE_SEX(1.0) |  | 0 | no |
| DF_UNER_SEX_EDU | Unemployment rate by sex and highest level of education | Unemployment | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2025-Q2 | 1680 | yes |
| DF_UNER_SEX_MTS | Unemployment rate by sex and marital status | Unemployment | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2025-Q2 | 1242 | yes |
| DF_UNER_SEX_POPG | Unemployment rate by sex and population group | Unemployment | REF_AREA+FREQ+INDICATOR+SEX+POPG+TIME_PERIOD | 2008-Q1..2025-Q2 | 1050 | yes |
| DF_UNER_SEX_REF_AREA | Unemployment rate by sex and province | Unemployment | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2025-Q2 | 2070 | yes |
| DF_UNE_SEX_AGE | Unemployment by sex and age | Unemployment | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2008-Q1..2026-Q2 | 1332 | yes |
| DF_UNE_SEX_EDU | Unemployment by sex and highest level of education | Unemployment | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2025-Q4 | 1728 | yes |
| DF_UNE_SEX_MTS | Unemployment  by sex and marital status | Unemployment | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2025-Q4 | 1278 | yes |
| DF_UNE_SEX_POPG | Unemployment  by sex and population group | Unemployment | REF_AREA+FREQ+INDICATOR+SEX+POPG+TIME_PERIOD | 2008-Q1..2025-Q4 | 1065 | yes |
| DF_UNE_SEX_PROV | Unemployment by sex and province | Unemployment | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2025-Q4 | 2130 | yes |
| DF_WAP_SEX_AGE | Working age population by sex and age | Working age population | FREQ+INDICATOR+SEX+AGE+TIME_PERIOD+REF_AREA | 2008-Q1..2025-Q4 | 1296 | yes |
| DF_WAP_SEX_EDU | Working age population by sex and highest level of education | Working age population | REF_AREA+FREQ+INDICATOR+SEX+EDU+TIME_PERIOD | 2008-Q1..2025-Q4 | 1704 | yes |
| DF_WAP_SEX_LMS | Working age population by sex and labour market status | Working age population | REF_AREA+FREQ+INDICATOR+SEX+LMS+TIME_PERIOD | 2008-Q1..2025-Q4 | 852 | yes |
| DF_WAP_SEX_MTS | Working age population by sex and marital status | Working age population | REF_AREA+FREQ+INDICATOR+SEX+MTS+TIME_PERIOD | 2008-Q1..2025-Q2 | 1260 | yes |
| DF_WAP_SEX_REF_AREA | Working age population by sex and province | Working age population | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2008-Q1..2025-Q4 | 1988 | yes |
| DF_WD_LST_ECO | Workdays lost during strike by economic activity | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2022-Q1..2023-Q4 | 80 | yes |
| DF_WG_LST_ECO | Wages lost by economic activity | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2022-Q1..2025-Q4 | 152 | yes |
| DF_WH_LST_ECO | Work hours lost during strike by economic activity | Work stoppages/strikes | REF_AREA+FREQ+INDICATOR+ECO+TIME_PERIOD | 2022-Q1..2024-Q4 | 120 | yes |
| DF_WOKRS_CNSL | Workseeker councelled by province | Workseeker | FREQ+INDICATOR+REF_AREA+TIME_PERIOD | 2021-M01..2025-M12 | 600 | yes |
| DF_WOKRS_REG_AGE | Workseeker registered by age | Workseeker | DSD_AGE(1.0) |  | 0 | no |
| DF_WOKRS_REG_REF_AREA | Workseeker registered by Province | Workseeker | FREQ+INDICATOR+REF_AREA+TIME_PERIOD | 2022-M01..2025-M12 | 480 | yes |
| DF_WOKRS_REG_SEX | Workseeker registered by sex | Workseeker | FREQ+INDICATOR+REF_AREA+SEX+TIME_PERIOD | 2022-M01..2025-M12 | 192 | yes |
| DF_WORKF_ECO | Workforce by economic activity | Workseeker | DSD_ECO(1.0) |  | 0 | no |
| DF_WORKS_PLC_REF_AREA | Workseeker placement by province | Workseeker | FREQ+INDICATOR+REF_AREA+TIME_PERIOD | 2021-Q1..2025-Q4 | 200 | yes |
| ZZ_PENTEST_I26224 | pentest | — | — | — | — | skipped |

*(Names/dimensions copied from the registry/CSV headers as returned; spelling errors such as "invloved", "uderemployment", "terminiation", "councelled", "benefity" are the source's own.)*

## 10. Open questions

1. **When will DEL flip the production flags?** `NonProductionDataflow=true`, `isFinal=false`, and `meta.test=true` on every message are the only hard blockers to treating this as a citable source. If they're legacy labels, DEL should remove them; if not, the data should not be relied on.
2. **Why is the data so ragged?** Latest period ranges from 2026-Q2 down to 2023-Q3 across flows, and 19 flows are empty/broken. This looks like an ingestion pipeline that was partially populated and not maintained uniformly.
3. **Will the informal-employment *level* flows (`DF_IE_SEX_*`) ever be loaded?** They're the gap between what the LMIS *claims* (informal employment) and what it *serves* (only 3 of 4 rate flows, through 2024-Q4).
4. **The 422 "does not contain REF_AREA" bug** on the `ECO_SEX`/`AGE` schemas is a server-side constraint misconfiguration — worth reporting to DEL if Tim wants employment-by-industry.
5. **Terms & conditions** are a placeholder (`example.org`). There is no stated reuse licence; who to ask for a data-use agreement is itself open.

## 11. Provenance / artifacts

- Downloads: `data/sa-entrepreneurship/lmis/raw/*.csv` (98 files, one per dataflow).
- Provenance manifest: `data/sa-entrepreneurship/lmis/manifest.tsv` (request URL, retrieved-at, rows, sha256, status, period span, notes).
- Scripts: `data/sa-entrepreneurship/lmis/scripts/sweep.py` (full sweep + manifest), `scripts/probe_data.py` (probe). Run `python3 -I`.
- Prior probe (kept as-is): `data/sa-entrepreneurship/lmis/probe/`.
- QLFS reference: `data/sa-entrepreneurship/raw/qlfs_q3_2026.txt` (P0211, released 10 Nov 2026).

*What I verified: every number in §5 was read directly from the downloaded CSVs and cross-checked against the QLFS text. The `test=true` flag was read from five separate JSON responses. I did not read the "LMIS Master Plan" or "Report" PDFs in full, and I did not attempt the pentest dataflow.*
