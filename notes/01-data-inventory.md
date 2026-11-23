# SA entrepreneurship data: what exists, what's reachable, what first emerges

*2026-11-23. Triggered by: government points at entrepreneurship as the answer to unemployment — what does the public data say about market conditions, product, location, funding, and the informal sector?*

Raw files (PDF + extracted text) are in `data/raw/`. Everything below that is a number was read from those files unless marked **[search only]**.

## 1. The core finding about the data itself

There are **two populations, measured by different instruments, that almost never meet**:

| | Venture-backed "startups" | Everyone else running a business |
|---|---|---|
| Size | 85 equity rounds, 94 deals incl. debt, in 2025 (Partech), 200+ rounds incl. small ones (SAVCA, **[search only]**) | ~3.0m owners (FinScope 2024); ~1.9m informal (SESE 2023); 515,892 company registrations in 2025/26 (CIPC) |
| Measured by | Industry trackers, from press/investor disclosure | Household surveys + the company register |
| Questions it answers | Funding, sector, investors | Location, reasons, turnover, formality, gender |
| Questions it can't answer | Anything about informal/survivalist business | Anything about growth, product, or funding rounds |

Rough scale: **~6,000 new company registrations per equity VC deal** (515,892 ÷ 85). Registrations are not operating businesses (see §4), so read it as an order of magnitude, not a ratio.

## 2. Inventory (reachable and read)

| Source | Latest | What it gives | Unit / caveat | File |
|---|---|---|---|---|
| **Stats SA QLFS** (P0211) | Q3 2026, released 10 Nov 2026 | Employed by formal / informal / household sector; by industry; by **province and metro**; by status (employer / own-account); unemployment | Quarterly, sample-based, jobs not businesses. **Informal definition changed Q3 2025** (21st ICLS): only 5 comparable quarters | `qlfs_q3_2026.pdf` (+ Q1 2026, Q4 2025) |
| **Stats SA SESE** (P0276) | **2023** (released Mar 2025); 2017 also pulled | Persons running non-VAT-registered ("informal") businesses: sex, age, province, industry, licence, start-up reason, money source, debt, bank account, record-keeping, employees, turnover, profit. Series 2001–2023 | ~4-yearly. **Turnover bands are nominal rand** across 22 years, so "fewer in the lowest band" is partly inflation | `sese_2023.pdf`, `sese_2017.pdf` |
| **FinMark FinScope MSME** | 2024 (fieldwork); 2020 also | Owners 3.03m; formal / semi-formal / informal split; sectors; township and rural; record-keeping; digital use; market access; who they sell to; formalisation barriers | n=4,027, 300 enumeration areas. Slide deck only, not microdata or full report | `finscope_msme_2024.pdf`, `_2020.pdf` |
| **CIPC annual report** | 2025/26 | Company registrations per year; name reservations; deregistration/reinstatement | Registrations ≠ trading. No total-register size or active-company count found in the text | `cipc_ar_2025_26.pdf` |
| **Stats SA liquidations** (P0043.1) | Apr 2026 | Monthly formal liquidations by industry (companies, CCs) | Only formal insolvency; says nothing about informal closure | `statssa_liquidations_apr2026.pdf` |
| **Stats SA QES** (P0277) | Mar 2026 | Formal non-agricultural employment by industry | Formal employers only; downloaded, **not read** | `qes_mar2026.pdf` |
| **Partech Africa VC report** | 2025 | Equity + debt by country, sector, deal count, investors, gender | Aggregates only, no deal-level data. Excludes M&A, grants, securitisation | `partech_2025.html` |
| **SAVCA/EY Private Capital Survey** | 2026 (2025 data), highlights only | Southern Africa PE+VC: fundraising R22.0bn, deployment R22.4bn, 186 deals, FUM R226.4bn | Full report member-only. Mostly infrastructure/energy, not startups | `ey_savca_2026_highlights.pdf` |
| **UNDP "Meet the Toshikas"** | 2024 | Annex mapping SA ecosystem players | Actually an Angola-focused report; SA is the comparator. Weak | `undp_startup_map.pdf` |

## 3. Reachable but not yet used, or blocked

- **DataFirst (UCT)**: catalogue reachable; carries QLFS and SESE microdata. Access terms (registration) not tested. **This is how to get unit-level data.**
- **World Bank Enterprise Surveys, SA 2020**: page reachable; downloads not tried. Formal firms with 5+ employees only, so not startups.
- **Treasury tax statistics page**: reachable, not read. Likely the best public formal-SME tax data (SARS itself isn't public).
- **GEM**: `gemconsortium.org/data` reachable; SA profile page returned 500 and the Stellenbosch PDF returned 403. Only second-hand figures so far (established-business ownership 1.8% in 2022/23). **[search only]**
- **Blocked / broken**: SEDA site (certificate error), DSBD (cert not verifiable), SEFA (cert expired), Africa: The Big Deal (timed out), Shoprite SMME report (403). The SEDA failure matters because its SMME Quarterly was the official SMME count and I found nothing after 2021 **[search only]**.
- **Paywalled by nature, not tested**: Crunchbase, Tracxn, Briter, SAVCA full reports.

## 4. What emerges (first pass; each is a hypothesis to test, not a conclusion)

**A. Two independent surveys agree on the informal owner count.** SESE 2023: **1.9m** informal-business operators. FinScope 2024: **1.70m** informal owners (of 3.03m; 56%). Different instruments, different years, within ~10%. That's a useful anchor. The *formal* count does not agree (§F).

**B. Most informal business is push, not pull.** SESE 2023: **57.1%** started because of unemployment or no alternative income (>60% in 2017). Also: 89.3% have no licence, 74.4% no bank account, 72% keep no financial records, >80% started with their own money, >90% have no business debt. Trade is 48.2% of informal businesses (62.7% of women's in 2017). This is what the "entrepreneurship fixes unemployment" claim is up against.

**C. The informal sector shrank sharply on Stats SA's new definition.** Informal sector employment 3,961k (Q3 2025) → 3,476k (Q3 2026): **−485k, −12.2%**. The path: −294k (Q3→Q4 2025), −127k, +34k, −98k. So most of the drop landed in one quarter. Employers: 717k, down 78k q/q (−9.9%) and 59k y/y. Own-account workers flat at ~2.05m. Formal sector +357k y/y, but total employment −215k y/y. **Caveat**: only five quarters on the new definition; Q3→Q4 2025 may include methodology or sample effects. I haven't checked sampling variability tables.

**D. Location is documented, and uneven.** Informal share of employment by area, Q3 2026:
- Highest: Eastern Cape non-metro 32.2%, Limpopo 32.1%, Mpumalanga 27.2%, Free State 24.2%
- Lowest: Northern Cape 10.5%, Nelson Mandela Bay 10.7%, Tshwane 11.4%, Gauteng non-metro 13.4%
- Cities differ a lot: Johannesburg 23.1% vs Cape Town 14.5% vs Tshwane 11.4%
- Largest absolute pools: Gauteng 887k, KZN 566k, Limpopo 485k
- SESE 2023 owner shares: Gauteng 28.9%, KZN 16.8%, Limpopo 15.8%

**Don't trust the metro-level y/y changes** (Buffalo City −50%, Tshwane −38%): those cells are small samples. Levels are safer than changes.

**E. Funding totals disagree, including on debt vs equity.** Disrupt Africa **[search only]**: $336m, 41% debt, early-stage only ~$9m. Partech: $715m, **90% equity ($643m), 10% debt ($72m)**, 85 equity rounds + 9 debt deals. Those can't both describe the same thing; the composition gap is the real signal that methods differ. Partech's sector mix for SA: cleantech 21%, healthtech 17%, fintech 14%. VC is not fintech-led here, unlike Nigeria.

**F. The formal-SME count is the least settled number.** FinScope 2024: 838k formal (CIPC+SARS-registered). Small Business Institute (tax data): 262k. TIPS: 710k **[search only]**. Probably a definition difference (what counts as "small", VAT/tax-active vs registered), but it means any "formal small business" statistic needs its source stated.

**G. Failure is nearly invisible in the formal data.** Formal liquidations: 233 in April 2026, 891 in Jan–Apr 2026. Against 515k registrations and ~3m owners, that's a rounding error: businesses mostly stop trading or get struck off, not liquidated. CIPC mentions deregistering **500,000+** non-compliant entities **(vaguely worded, not a verified figure)**. So the "70–80% fail" claim has no clean data behind it; the only honest survival evidence is cohort data, which would need microdata.

**H. Registrations are at a five-year high while name reservations fell.** Registrations 515,892 in 2025/26 (vs 402,517 in 2023/24). Name reservations 649,353 → 532,843. CIPC reads both as confidence; I'd read registrations as partly compliance and cheap online registration (R175, ~1 day **[search only]**), not necessarily new businesses.

## 5. Numbers that don't reconcile (don't use without a note)

- **FinScope "MSMEs employ 13.4m people, ~80% of the workforce"** vs QLFS total employment of **16.8m**, of which 3.3m formal community/social services (largely government) and 12.3m formal overall. Employee counts include part-time and seasonal, probably double-counting people with several jobs.
- **FinScope "R5.29 trillion estimated turnover"** is revenue, not GDP contribution. Not comparable to GDP.
- **"Informal sector" vs "informal employment"** (QLFS): 3.5–3.7m vs 5.7m. The second includes informal jobs inside formal firms. Using one number for the other is the easiest mistake in this whole area.

## 6. What this data cannot answer (so far)

- **Product**: nothing beyond industry. No data on what is sold or whether it's novel.
- **Growth**: no panel data on businesses over time. Only repeated cross-sections (SESE) and one 2026 survey claim that established firms don't develop into bigger employers **[search only]**.
- **Market conditions** at the business level: FinScope has who they sell to (57% other MSMEs, 34% bigger business, 26% government), but not demand or competition.
- **Job creation per business**: FinScope gives "potential new jobs per job" ratios by sector, which I treat as unverified.

## 7. Open questions

1. Is the Q3→Q4 2025 informal drop real, or an artefact of the definition change? Test: sampling-variability tables (QLFS 3.4A/B) and the Stats SA explanation.
2. Can DataFirst microdata give owners' start year and survival, to estimate real failure rates from SESE cross-sections?
3. What explains Disrupt Africa vs Partech on debt share? Needs both methodology notes.
4. Does SEDA still publish an SMME count? Any official successor?
5. Is any of the formal-count discrepancy (262k / 710k / 838k) resolvable from Treasury's tax statistics?

## Glossary and assumptions

- **MSME/SMME**: micro, small and medium enterprise. FinScope: micro 0–10 employees (84% of owners), small 11–50, medium 51–250.
- **Non-VAT-registered business** (SESE): Stats SA's definition of informal. Registration, not size, is the test.
- **Own-account worker**: self-employed with no employees. **Employer**: self-employed with employees.
- **Survivalist**: running a business because there's no job. FinScope's 2010 survey put ~60% of owners there, but on a different definition.
- **ICLS**: International Conference of Labour Statisticians, which sets the standard definitions Stats SA follows.
- **Equity vs debt** in funding data: equity buys a stake; debt is a loan. Trackers disagree about including debt.
- This note assumes the PDFs' text extraction was accurate. FinScope's deck tables extract messily; its headline figures reconcile arithmetically (micro + small + medium = 3,027,298; formal + semi + informal ≈ 3.01m).

## Addendum: DataFirst (checked 2026-11-23, public pages only)

Read the public catalogue pages for SESE 2005, 2013, 2017 and 2023 (a handful of requests, spaced a few seconds apart, robots.txt checked). The browser session was not used, and I have no tool here that can reach it.

- **SESE microdata exists for every wave**: 2005, 2013, 2017, **2023 (v1, released Aug 2026)**. The 2023 study carries a **CC-BY** access condition (the file itself sits behind DataFirst's "Get Microdata" page, which I haven't opened). Lowest geography: **province and metro**.
- **SESE is a two-stage follow-up to QLFS Q3**, not a business survey. Stats SA says there is "no sampling frame" for unregistered businesses. Stage 1: people who say they're self-employed in QLFS. Stage 2: they're re-interviewed about the business. So SESE counts **owners**, and anyone not reached through a household is missed.
- **Inclusion rule**: businesses *not registered for VAT*. That is wider than "informal" (it includes income-tax-paying businesses), which is why Stats SA's published "informal" count and SESE's definition aren't the same population.
- **Survival limits**: waves are repeated cross-sections, not a panel. "Length of time operated" lets you build age profiles, not true survival rates.
- **Not yet done**: variable list (the data-dictionary page returned no content to a plain fetch, probably JavaScript-rendered), actual downloads.
- **Size, from the data-dictionary page**: the SESE 2023 file has **1,583 cases and 201 variables**. That's a small sample for a population of ~1.9m owners, so the provincial and industry cuts in the Stats SA report will have wide error bars, and anything finer (province × industry × sex) will be mostly noise. Weights come with the release PDF.
- **Correction to §6 ("product: nothing beyond industry")**: that holds for the *published tables*, not the microdata. The 2023 questionnaire (in `data/datafirst/q-sese-2023.pdf`) asks what goods or services the business provides (Q8), where it operates and why there (Q18–24), when the business and the owner started (Q43–44), start-up difficulties and grants (Q59–61), who it sells to and where (Q76–77), turnover and other income (Q79–80), difficulties affecting operation (Q81), assistance needed (Q83) and employment/wages (Q89–95). Whether each is in the public file at usable detail is not yet checked.
- **Documentation downloaded 2026-11-23 09:54–09:57**: questionnaires (2001, 2009, 2013, 2017, 2023), release reports (all five), metadata/record layouts (2001, 2013, 2023). No data files yet.

## Addendum 2: Department of Employment and Labour (DEL), public releases (checked 2026-11-23)

Files in `data/del/`: DEL, UIF and Compensation Fund annual reports 2025/26, CEE 23rd report.

- **DEL is not the owner of small-business or startup data.** Its publications folders (labour.gov.za → Resource Centre → Publications) are organised by Act (BCEA, COIDA, Employment Equity, Labour Relations, OHS, UIF) plus Public Employment Services and Operations. Nothing on enterprise births, size or survival.
- **Public Employment Services (ESSA), 2025/26 annual report**: 1,129,464 work-seekers registered (56% women, 62% youth 15–35, 0.1% disabled); 116,044 placed (~10% of registrations, though placements and registrations aren't the same cohort); 357,843 counselled. This is a *supply-side jobseeker register*, not a labour-force measure.
- **Inspections (employer compliance)**: 309,659 inspections vs target 298,104; 233,462 compliant (75%); 76,197 non-compliant employers served notices. By province in the report. Counts inspected workplaces, not all employers.
- **Employment equity**: reports only from designated employers (50+ employees). LabourGuide (secondary, **[search only]**) says reports received fell from 29,269 (2024) to 15,090 (2025) because small employers were exempted. So it can't say anything about small businesses by design.
- **LMIS portal** (`de-lmis.labour.gov.za`, launched Sept 2024 by DEL, ILO and Stats SA): a JavaScript "data explorer"; it returned only an empty app shell to a plain fetch, so contents unknown. **Needs a real browser to inspect.** It's the single most likely place for DEL-hosted tables.
- **Registered-employer counts (UIF, COIDA)**: not found in the UIF or Compensation Fund annual reports. UIF contributions are collected by SARS, so the employer base effectively sits with SARS.
- **Old**: the Annual Labour Market Bulletin (last one I could find: 2012/13).

## Addendum 3: LMIS (de-lmis.labour.gov.za), downloaded 2026-11-23

Full detail in `notes/08-lmis-inventory.md` (written by a DeepSeek V4 Pro Pi thread); files in `data/lmis/raw/` (98 SDMX-CSV files, 8.5 MB, provenance in `manifest.tsv`).

- **It is a public SDMX API** (`sdmx-lmis.labour.gov.za/rest`), no captcha or token needed. 118 dataflows listed (117 real + one `ZZ_PENTEST_I26224` leftover that was not queried). 98 returned data; 15 are registered but empty (404 "no mapping set", including all four informal-employment *level* flows); 4 fail with a server bug (422), including employment by sex *and industry*.
- **The QLFS-derived series are Stats SA's QLFS republished, not independent data.** Spot-checked by me: national employed 17,055k (2025-Q3) and 17,099k (2025-Q4) match the Stats SA release exactly; informal employment rate 30.5% national, 21.4% Northern Cape, 43.2% Mpumalanga (2024-Q4) reproduce from the CSV. The thread reports the same match for status in employment (employer 795k, own-account 2,047k, 2026-Q2). Series lag: nothing for 2026-Q3.
- **Every dataflow is tagged `NonProductionDataflow=true` and every message `meta.test: true`**, yet the values are real QLFS numbers. The thread's reading, which I haven't independently tested beyond the spot checks: a real platform still carrying development flags.
- **Licence**: the "Terms & conditions" link is a placeholder (`example.org`), footer "All rights reserved". No open licence, so treat as personal-research use with attribution to DEL; don't republish.
- **What's genuinely new vs the Stats SA PDFs**: (1) clean 2008→2026 time series for employers and own-account workers by sex (`DF_EMP_SEX_SIE`), saving PDF parsing; (2) informal employment *rate* by province, 2008→2024-Q4 (old definition, before Stats SA's Q3 2025 change, so don't splice it with the new informal-sector shares); (3) DEL's own admin series: work-seekers registered/counselled/placed, opportunities, Job Opportunity Index, inspections, CCMA arbitration and conciliation, UIF claims, work stoppages.
- **Still missing from every source so far**: informal sector headcounts by industry or metro beyond the QLFS tables, anything on firm births, size or survival, and any product-level data.

## Addendum 4: National Treasury / SARS (checked 2026-11-23)

Full detail in **`notes/02-treasury-sars-tax-statistics.md`**; files and recomputation scripts in `data/treasury/`. This addendum records only what changes *this* note.

- **Tax Statistics 2025 is the richest formal-sector source found so far, and it is published as `.xlsx`, not PDF.** SARS hosts it (not Treasury — Treasury's tax-statistics page stops at 2015). Chapters 2, 3 and 4 gave: companies assessed by taxable income band, **small business corporations by turnover band**, **active VAT vendors by turnover band**, a **10-year VAT survivor cohort**, individuals with business income by sector, and ETI by SETA.
- **Open question 5 is answered (§2 of the new note).** The 262k / 710k / 838k formal-SME estimates are different rungs of one ladder: 4.14m on the register → 1.38m "expected to submit" (SARS's active-and-not-dormant count) → 1.23m assessed → **266k with a positive taxable income** → 186k on the s12E regime. 262k sits within 2% of the 266k figure; that is almost certainly what it is measuring.
- **§4G is fixed, for one segment.** The 10-year VAT cohort (227,770 vendors that filed in every year 2015/16–2024/25) against the **425,225 active vendors in 2015/16** (Table 4.1 of the *2016* edition) gives a **ten-year survival rate of 53.6%**, = **6.7% a year leaving the VAT register**. It also shows a barbell migration pattern with a thinning R1m–R5m middle, and a quiet-death measure: cohort members declaring **nil turnover rose from 1.4% to 3.2%**. Caveats: exit ≠ death (deregistration, sub-threshold decline, re-registration under a new number), it is a floor because the cohort must file every year, and it is a ten-year endpoint rather than a curve. *(Correction to this addendum's first draft, which said the 2015/16 denominator wasn't published: it is not in the 2025 edition, but the 2016 edition carries it.)*
- **§4H is qualified.** 64% of the 4.14m company register is not expected to submit a return at all, and the active base *fell* 6.5% over the step in which the register rose 13.7% (register clean-up, per a Table 3.4 footnote). Registrations are not business formation; the active-company count is the number to watch.
- **A structural break is coming that will break every VAT-based count.** Budget 2026 raises the **VAT compulsory registration threshold from R1m to R2.3m** (1 April 2026) and the turnover-tax limit to match. **47.8% of active vendors had annualised turnover below R2.3m** in 2024/25, so the measured formal population roughly halves by definition. Don't splice 2025/26 with 2026/27.
- **What the state spends, for comparison with the funding trackers**: SBC tax relief R3.9bn + ETI R4.5bn (2023/24) against a DSBD vote of R2.8–3.0bn; s12J venture-capital relief cost R1.0–1.3bn a year before its estimate disappears. Programme detail (vulekamali ENE pivot + the 2026 ENE): DSBD's only fast-growing line is **Programme 3, Integrated Cooperatives and Micro Enterprise Development — R142.7m (2024/25) → R532.2m (2026/27), a 3.7× rise aimed at informal and micro businesses**, while Programme 4 (SEDFA and the growth-facing work) fell 5.1%/yr nominal to 2025/26. **SEDFA is mostly a payroll**: 40.7% compensation and 49.7% goods and services over the MTEF, 7.6% transfers, with ~R1.1–1.9bn a year of *lending* (repaid) alongside it. dtic (vote 39, R11.7bn) spends four times DSBD on **incentives for existing manufacturers** (R5.4bn), not startup finance. Nothing in either vote funds equity for new firms.
- **vulekamali is alive; my first pass said otherwise.** Resource files sit at `/datasets/<dataset>/resources/<file>` (dataset-level, one level above the per-year page that links them) — the CSV is 4.7MB and reproduces the published ENE to the rand. The dead part is `data.vulekamali.gov.za`, the "Data Portal API" in the footer (no DNS).
- **Procurement is countable after all — but only in a browser.** The eTenders OCDS packages (ODC-PDDL, downloadable) carry award values that fail spot checks and no contractor size; the **Procurement Dashboard** (Power BI paginated report, no export, no API) carries exactly the dimension I said was missing. For **FY2025/26**: R328.66bn of spend, **SME (turnover < R50m) 36.05% (R118.48bn)**, large business 30.97%, and **32.98% (R108.39bn) on suppliers with no turnover recorded**. Designated groups: black-owned 41.01% (R134.78bn), women 15.45%, youth 8.49%, disabled 0.56%. Both readings of the SME share (36.05% of all spend, ~53.8% of classified spend) exceed the 30% target — but this measures **share of spend by supplier size**, not compliance with any set-aside. Full transcript with page numbers and filter state: `data/treasury/procurement-dashboard-2025-26.md`. **My earlier "not countable / one-field fix" verdict was wrong on the facts and right on the friction: the field exists, it just isn't in any file.**
- **The older OCDS position stands for the downloadables.** eTenders OCDS monthly JSON (ODC-PDDL) carries award values, but they fail spot checks (R5.32bn "Eskom", R4.20bn "National Metrology Institute", R2.18bn "Artscape"), the documented API returns 500, the CSV twins drop all value fields, and `SupplierID` is 0 everywhere — so no join to the CSD's enterprise-size class. The 30%-set-aside claim cannot be tested from public data yet; the missing field is contractor size, not money.
- **Still missing after this**: any firm-level employment, any birth rate, any cohort survival *rate*, and anything at all on the informal sector. Tax data begins where SESE ends.

## Addendum 5: SESE 2023 microdata obtained (2026-11-23)

**The SESE 2023 zip was downloaded from Stats SA directly** — 3 532 700-byte CSV, 1 583 records × 201 variables, with weights. This is the unit-record file the earlier addendum listed as "no data files yet"; it is not DataFirst and not behind an application. Full first-pass analysis: **`notes/04-sese-2023-microdata.md`**.

It verifies against the published report (weighted population 1.84m persons vs 1.87m published; sex split 57.6/42.4 vs 57.7/42.3) and it changes four things in this note:

- **§6 "product: nothing beyond industry" is now answerable for the informal sector** — the file has turnover, profit, employee counts, business age and start reasons at unit level.
- **§4B ("most informal business is push, not pull") survives, and gets its economic content**: median annual turnover **R16 000**, median monthly profit **R2 000**, 76.4% of businesses that disclose turnover take under R50 000 a year.
- **§4C/§4G**: still no panel, so no survival rate from this file — but employment is now measurable per business: **85.7% employ nobody; 26 paid jobs per 100 businesses; the R50k–R250k band supplies 37.5% of all paid jobs.**
- **The "new gap" was mine, and it is closed**: I first read QLFS as counting **717k** informal-sector employers against SESE's **283k**. Computed from the QLFS Q3 2026 unit records, informal-sector employers are **286 512** — **1.1% from SESE's 283 348**. 717k/768k is the *national total* of employers (481 383 formal + 286 512 informal). **Correction (same day): there is no 2.5× gap — QLFS Q3 2026 puts informal-sector employers at 286 512 against SESE's 283 348, a 1.1% difference; the 717k I quoted was the national total of employers, not the informal subset.** See `notes/06-qlfs-employer-reconciliation.md`.

## Addendum 6: Stats SA's unit-record archive (2026-11-23)

**`notes/03-statssa-unit-record-archive.md`.** The trail started at `isibaloweb.statssa.gov.za`; it is Stats SA's **ungated unit-record archive**, not a PDF portal — nearly every household/establishment survey from 2000 as CSV/SPSS/SAS/STATA, no registration.

- **Access**: the HTML pages sit behind Incapsula (1.1KB challenge to a plain client), but the files under `/data/` download directly. Enumerate in a browser, fetch with curl.
- **What exists that matters here**: SESE **2009/2013/2017/2023** (2013 additionally has a **worker-level file**), QLFS **2008Q1–2026Q3**, LMD **2008–2024** (four quarters stacked, *with earnings*), LFS **2000–2007**, IES **1995–2023**, GHS 2002–2025, Census 1970–2022, vital registration, plus 17 monthly ETS series including **liquidations from 2000**.
- **Pulled** (11 files, 77MB, manifest with hashes): the three older SESE waves, LMD 2024, QLFS 2026Q3 + 2008Q1, IES 2023, two LFS waves, liquidations (xlsx + txt).
- **This changes the "missing" list**: the informal series can now be a *trend* rather than a snapshot; the **717k vs 283k employer gap** can be computed from QLFS/LMD person records instead of quoted; and **liquidations 2000→** is a real formal-exit series behind the "70–80% fail" claim. It does **not** deliver a business-level panel, so cohort survival curves remain out of reach.
## Addendum 7: who employs people in the informal sector (2026-11-23)

**`notes/05-who-employs.md`** — cross-tabs from the SESE 2023 microdata, weighted, with cell counts.

- **74.6% of informal businesses were started out of necessity** (unemployed, no alternative income, retrenched, "to survive/make ends meet", earning while searching); 22.3% from opportunity. The narrow published reading ("unemployed" or "no alternative income") is 56.2%, reproducing the reported 57.1%.
- **Employment rises with age**: 10.9% of under-a-year businesses employ anyone against **20.9% at ten years+**, and jobs per 100 rise from **7.0 to 42.9**. Firms older than five years hold **52% of employers and 60% of paid jobs**; under-a-year firms hold 12.4% of employers but **4.4% of the jobs**.
- **Motive cuts both ways, and the two readings are both true**: opportunity-started businesses are **1.8× as likely to employ** (22.3% vs 12.2%) and generate **1.85× the jobs per 100** (41.1 vs 22.2) — yet necessity-started businesses supply **64% of all informal paid jobs**, because they are three-quarters of the population.
- **The motive gap is mostly a survival effect**: 35.0% vs 6.6% at under a year, converging to 24.4% vs 20.4% at ten years+. Hiring is something informal businesses grow into; motive predicts the speed, not the ceiling.
- **Formalisation markers track employment**: a licence → 30.1% employ / 77.3 jobs per 100; income-tax registration → 35.6% / 95.4; savings account → 27.9% / 68.6, against 14.3% / 26.0 for the sector. **Causality cannot be settled in this file and it is the question a policy would need answered.**
- **Trap recorded**: annual turnover is missing for **all 265** under-a-year businesses (the question is only asked of businesses operating 12 months+), so no age × turnover comparison exists — a first draft showed "0.0% above R50k" which was a skip pattern, not a finding.
## Addendum 8: the informal-sector series, 2009 → 2023 (2026-11-23)

**`notes/07-informal-sector-series.md`** — four SESE waves harmonised (`scripts/sese_series.py`), deflated with World Bank CPI. Validated in every wave: weighted population within 5.4–5.6% of the published person count (the gap is structural — a row is a business, the published total counts persons), and the necessity share within 0.8–1.5 points of the published figure.

- **More businesses, fewer employers.** Businesses +64% (2009→2023), but from **2013 to 2023 businesses rose 24% while employers fell 27% and paid jobs fell 25%**. The employer rate peaked at 24.4% in 2013 and is 14.3% in 2023; paid jobs per 100 businesses fell from 43.1 to 26.0.
- **Real turnover has not improved in fourteen years.** Median annual turnover in 2023 rand: **R19 469 (2009) → R19 908 (2013) → R24 012 (2017) → R16 000 (2023)**. The nominal series doubles; the real one ends below where it began.
- **The one improving trend is motive**: necessity starts fell from 68.2% (2013) to **56.2%** (2023), matching the published series (69.2 → 63.5 → 57.1).
- **2009→2013 is a break, not growth** (employers +71%, paid jobs +103% in four years) — SESE rides on QLFS weights and the QLFS was reweighted after a census (last reweighting 2014), so a level shift is the plausible explanation. Use 2013→2023 for change.
- **Comparability trap**: reason codes are not stable. 2009 has code 2 = "unemployed/no alternative income" *merged* and 3 = retrenched; 2013+ splits them (2 unemployed, 3 no alternative) and moves retrenched to 4. Codes 14–16 exist only from 2017. The cross-tab note's broader "push" grouping **cannot** be extended backwards.
- **Internal inconsistency to respect**: 2023's median monthly profit (R2 000) exceeds its median annual turnover (R16 000), so at least one question is badly answered. Neither level is quoted in the brief; the employment numbers do not depend on either.
- **Correction**: `SESE2013WORKER.csv` is *not* employee-level data (see the archive note §7) — it is the same 2 031 records with `Uqno` replaced by a serial.

