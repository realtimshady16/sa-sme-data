# Treasury + SARS tax data: the formal-business denominator, and the first public "what happens next" series

*2026-11-23. Follows `notes/01-data-inventory.md` (which lists the sources and the first-pass findings) and the LMIS note. Trigger: after SESE/QLFS/FinScope/DEL/LMIS, the open question was whether Treasury's public releases could supply what the household surveys can't — a count of **formal** businesses by size, and any evidence on **what happens to them over time**. They can, for one segment, better than expected.*

Raw files, scripts and extracted text: `data/treasury/`. Every number below is recomputed from the published workbook by `scripts/treasury_numbers.py` (see §13), not typed in from a summary. Prose quotes come from `raw/2025_Tax_Statistics_main.txt` (the 2025 edition, released 5 December 2025) and `raw/budget2026_FullBR.txt` (Budget Review 2026).

## 1. What was actually reachable

| Source | Access | What it gives |
|---|---|---|
| **Tax Statistics 2025** (National Treasury + SARS, 18th edition) | Full **`.xlsx` tables** per chapter, zipped, no login | Companies assessed by taxable income band, by turnover band, by age; small business corporations; VAT vendors by turnover band, 10-year cohort; individuals with business income; ETI |
| **Budget Review 2026** (Annexure B, Tax Expenditure Statement) | Single PDF | Revenue forgone per incentive: SBC rate, s12E depreciation, ETI, VCC, SEZ |
| **Budget Review 2026** (Ch. 4, Table 4.6–4.7) | As above | The 2026 threshold changes, including the **VAT registration threshold** |
| **eTenders OCDS** (`data.etenders.gov.za`) | Monthly JSON/CSV, ODC-PDDL | Tender and award records with values (see §9 — the values are not usable) |
| **CSD** (`secure.csd.gov.za`) | Headline counter only | 1,465,721 verified suppliers to the state |
| **Procurement Dashboard** (Power BI, via `data.etenders.gov.za`) | **Browser only — no download, no API** | FY2025/26 spend by supplier size band and by designated group (§9) |
| Treasury's own tax-statistics page | **Dead ends at 2015** — SARS took the publication over | n/a |
| **Earlier Tax Statistics editions** (2016, 2020, 2021) | Same SARS page, same `.xlsx` format | The historical register/active-vendor series, and the 2015/16 base that turns the cohort into a survival rate |
| `ocds-api.etenders.gov.za` | Public Swagger; **every dated request returns 500** | n/a |
| Procurement Payments Dashboard | **Power BI report**, no bulk download | Payments from BAS, by supplier (not used) |
| **vulekamali** (`vulekamali.gov.za`) | Renders fine; the **resource files** are at `/datasets/<dataset>/resources/…`, not the guessed per-year path. `data.vulekamali.gov.za` (the "Data Portal API" link) has **no DNS** | ENE as a semicolon-delimited pivot (vote × programme × subprogramme × economic class), 2020/21→2026/27 |

## 2. The register ladder — and it does resolve the "formal business count" question

The published estimates of formal small business in SA disagree wildly (262k, 710k, 838k, 3.0m). The tax data explains why: **"formal business" has at least six different counts, each defensible**, and they differ by a factor of 60.

All at 31 March 2025 unless marked (Tax Statistics 2025, front summary and Table 3.4):

| Definition | Count |
|---|---|
| Entities on the CIPC/SARS **company register** | **4,144,492** |
| Companies **"expected to submit returns"** — SARS's own "active and not dormant" measure | **1,377,809** (tax year 2024) |
| Companies **assessed**, tax year 2023 (83.3% of those expected) | **1,228,437** |
| Companies with **positive taxable income**, tax year 2023 | **266,391** |
| Companies using the **small-business-corporation regime** (s12E), tax year 2023 | **185,022** |
| **Active VAT vendors** (2024/25) | **496,858** of 900,285 registered |
| **Employers on the PAYE register** | **648,500** |
| Individuals declaring **business income** (2024, 84.3% assessed) | **208,111** |

Read it as a funnel, and the survey numbers stop contradicting each other:

- **262k** (Small Business Institute, via tax data) sits within 2% of the **266,391 companies with a positive taxable income**. That looks like a "profitable company" count, which is a sensible definition and a very small one.
- **710k**–**838k** (TIPS; FinScope's "formal, CIPC+SARS registered") sit between the SBC count and the active-register count. 838k is close to the 867,337 companies assessed for the *partly assessed* 2024 year, so it may be a tax-year-scoping artefact rather than a different population.
- **1.38m** is the widest defensible "active formal company" number, and **4.14m** is what people mean when they quote "companies registered in SA" — two-thirds of which are dormant.

That last ratio is the headline: **2.77 million of the 4.14 million entities on the register (66.8%) are not expected to submit a return at all.** CIPC's 515,892 registrations in 2025/26 (inventory note §H) are therefore not 515,892 businesses entering the economy; they are entries on a register whose active fraction is two-thirds smaller.

**Caveat on the register series.** The register falls 7.2% in 2024 and rises 13.7% in 2025, while "expected to submit" *falls* 6.5% (1,474,309 → 1,377,809) across the same step. Table 3.4 carries a footnote saying a "comparative data analysis of the CIT register against internal and third party data sets was conducted" — i.e. the register is being cleaned, and both moves are more likely maintenance than business dynamics. Don't read the year-on-year register change as entrepreneurship.

## 3. Size distribution: where the tax is

Tax year 2023, all 1,228,437 assessed companies (Table 3.6; band detail in Table A3.3.1):

| Taxable income | Companies | Share | Tax assessed | Share |
|---|---|---|---|---|
| Loss | 298,865 | 24.3% | R67m | — |
| **Nil** | **663,181** | **54.0%** | R31m | — |
| R1 – R1m | 217,516 | 17.7% | R8,168m | 2.6% |
| R1m – R100m | 47,680 | 3.9% | R95,374m | 30.9% |
| R100m + | **1,195** | **0.1%** | **R205,223m** | **66.4%** |

So: **of every 100 companies that file, 54 declare nothing, 24 declare a loss, and 22 declare a profit.** The 1,195 companies with taxable income above R100m pay two-thirds of company tax. Any story about company tax that doesn't start with that concentration is wrong.

The 54% nil group is doing a lot of work and is the least clean number in the table: it mixes dormant-but-filing entities, companies exactly breaking even, and companies whose assessed loss wiped out the year. It is *not* 663,181 failed businesses.

## 4. Small business corporations: the closest thing to a size profile of formal small firms

Section 12E lets a company with gross income up to R20m opt into graduated rates. 185,022 companies did in 2023. Their **turnover** distribution (Table A3.7.7) is the closest public substitute for "how big are SA's formal small firms":

| Turnover | 2021 | 2022 | 2023 | 2024* |
|---|---|---|---|---|
| R1 – 100k | 23,324 | 22,247 | 25,583 | 35,704 |
| R100k – 250k | 16,819 | 15,029 | 13,247 | 9,000 |
| R250k – 500k | 22,045 | 20,597 | 18,496 | 12,874 |
| R500k – 750k | 17,982 | 17,357 | 16,215 | 11,079 |
| R750k – 1m | 18,505 | 19,965 | 18,778 | 13,796 |
| R1m – 2.5m | 35,603 | 37,867 | 37,684 | 28,460 |
| R2.5m – 5m | 22,596 | 24,729 | 25,163 | 19,888 |
| R5m – 7.5m | 10,004 | 11,408 | 11,795 | 9,678 |
| R7.5m – 10m | 5,713 | 6,570 | 7,074 | 6,002 |
| R10m – 14m | 4,688 | 5,755 | 6,124 | 5,232 |
| R14m – 20m | 3,522 | 4,415 | 4,847 | 4,187 |
| Above R20m | 31 | 27 | 16 | 4 |
| **Total** | **180,832** | **185,966** | **185,022** | **155,904** |

\* 2024 is only 63% assessed; treat its column as a floor, and don't read the shifts inside it.

- **Half of the companies in the small-business regime turn over less than R1m a year** (92,319 of 185,022 in 2023, 49.9%) — and those sub-R1m companies pay R318m of tax between them, about **R3,450 each**.
- The mode is R1m–R2.5m (37,684), not the bottom band.
- The top of the regime is thin: 4,847 companies in the R14m–20m band and only **16** above R20m. The population is dominated by genuinely small firms.
- **The regime is not a subsidy for innovation or growth**: 39.6% of SBCs report an assessed loss in 2024 (61,683 of 155,904), and 40.5% in 2023. It is a compliance-simplification regime for small, mostly marginal companies.

## 5. The 10-year VAT cohort — a real survival rate, and the first public "what happens over time" series

This is the find. Tax Statistics publishes a cohort of **227,770 VAT vendors that filed returns and paid or reclaimed VAT in every one of the ten years from 2015/16 to 2024/25**, tracked by turnover bracket each year (Tables A4.7.1–A4.7.11). SARS describes the population explicitly (2025 main PDF p. 257).

**The denominator is not in the 2025 edition, but it is in the earlier ones.** Table 4.1 of the 2016 edition gives **425,225 active VAT vendors in 2015/16**.

- **Ten-year survival: 227,770 / 425,225 = 53.6%.** Roughly **half of VAT-registered businesses are gone from the register within ten years**, and the implied average attrition is **6.7% a year** (1 − 0.536^(1/9)). This is the number the inventory note said didn't exist for any SA business population. It holds for one segment — businesses above the R1m threshold, filing VAT — and it is a **floor on survival**, because the cohort requires filing *every* year, while the denominator only requires activity in the base year.
- **The other side of the same arithmetic: 269,088 of today's 496,858 active vendors (54.2%) were not on the register as active in 2015/16.** Nine years, ~30,000 net new entrants a year that are still trading — a business population that turns over by more than half every decade, in the segment where the firms are big enough to matter for jobs.
- **Exit is not death.** A vendor leaves this count by deregistering, dropping below the threshold, being struck off, being absorbed, or re-registering under a new VAT number. So 53.6% is "still the same VAT entity and still filing", not "still trading". The direction is right; the magnitude is a lower bound on continuity and an upper bound on nothing.

The register history says the same thing more slowly (Table 4.1 across the 2016, 2020, 2021 and 2025 editions):

| Fiscal year | Registered | Active | Active share |
|---|---|---|---|
| 2011/12 | 652,349 | 441,820 | 67.7% |
| 2012/13 | 650,540 | 431,572 | 66.3% |
| 2013/14 | 662,194 | 424,562 | 64.1% |
| 2014/15 | 679,274 | 420,940 | 62.0% |
| 2015/16 | 706,874 | 425,225 | 60.2% |
| 2016/17 | 742,388 | 432,072 | 58.2% |
| 2017/18 | 773,783 | 434,981 | 56.2% |
| 2018/19 | 802,957 | 448,710 | 55.9% |
| 2019/20 | 831,821 | 449,597 | 54.0% |
| 2020/21 | 880,553 | 448,361 | 50.9% |
| 2021/22 | 941,406 | 470,239 | 50.0% |
| 2022/23 | 953,665 | 477,775 | 50.1% |
| 2023/24 | 959,000 | 488,124 | 50.9% |
| 2024/25 | 900,285 | 496,858 | 55.2% |

Over thirteen years the **register grew 38% while the active base grew 12.5%**. Every percentage point of that gap is an accumulated dead entity that has to be carried, cleaned or deregistered — and two of the steps show the cleaning: the register falls 6.1% in 2024/25 (959,000 → 900,285) exactly as the active share jumps 50.9% → 55.2%, the same pattern as the company register (§2). **Neither register series is a business-population series; the active line is.**

What the cohort adds beyond the survival number:
- **Survivors' nominal turnover grew 6.7% a year** (R9.5tn → R17.1tn), and their Domestic VAT payments also 6.7% (R234.8bn → R422.2bn), refunds 7.8%. SARS's own reading: *"This confirms that real growth in the economy has remained subdued over the decade."* For a set of businesses that by construction survived a decade, nominal turnover tracking inflation **is** the finding.
- **Movement between brackets is a barbell**, and it is partly an artefact:

| Turnover bracket | 2015/16 | 2024/25 | Change | CAGR |
|---|---|---|---|---|
| Nil | 3,273 | 7,282 | **+122.5%** | 9.3% |
| R1 – 50k | 3,116 | 3,694 | +18.5% | 1.9% |
| R50k – 100k | 4,584 | 3,942 | −14.0% | −1.7% |
| R100k – 200k | 8,335 | 7,131 | −14.4% | −1.7% |
| R200k – 300k | 7,550 | 6,537 | −13.4% | −1.6% |
| R300k – 500k | 12,734 | 11,199 | −12.1% | −1.4% |
| R500k – 700k | 10,450 | 9,336 | −10.7% | −1.2% |
| R700k – 1m | 13,652 | 11,615 | −14.9% | −1.8% |
| R1m – 2m | 33,475 | 27,729 | **−17.2%** | −2.1% |
| R2m – 3m | 21,673 | 18,299 | −15.6% | −1.9% |
| R3m – 5m | 25,795 | 23,421 | −9.2% | −1.1% |
| R5m – 10m | 28,853 | 28,940 | +0.3% | 0.0% |
| R10m – 14m | 11,128 | 11,977 | +7.6% | 0.8% |
| R14m – 20m | 9,559 | 10,772 | +12.7% | 1.3% |
| R20m – 30m | 8,589 | 10,201 | +18.8% | 1.9% |
| R30m – 50m | 8,326 | 10,600 | +27.3% | 2.7% |
| R50m – 100m | 7,679 | 10,613 | +38.2% | 3.7% |
| R100m + | 8,999 | 14,482 | **+60.9%** | 5.4% |

Two readings, one safe and one not:

1. **Safe:** the decline is concentrated in the **R50k–R5m middle** (every bracket there lost 9–17% of its members) while the top gained 61%. Even allowing for growth, a decade-surviving cohort lost 40,000 vendors out of the R1m–R5m range and gained 5,500 above R100m. Middle-sized firms are the ones that disappear.
2. **Not safe:** the rightward drift is **mostly inflation**, because the brackets are fixed in nominal rand over ten years. A vendor whose real turnover was flat would move up roughly one bracket. So the top-bracket growth cannot be read as "survivors grew"; only the *shape* (barbell, thin middle) and the nil group are inflation-robust.
3. **The nil group is a real finding and a real warning:** 3,273 → 7,282 vendors that filed every year and then declared **zero turnover** — 1.4% → 3.2% of the cohort. These are registered, compliant, ten-year-old "zombie" vendors: not liquidated, not deregistered, just not trading. If you want a public measure of quiet business death, **this is the closest thing that exists**, and it says deaths are counted late, as nil returns rather than as failures.

**Selection bias to state out loud:** the cohort is defined by filing every year, so it describes survivors exactly and says nothing about when anyone exited. It cannot give a survival *curve* (five-year vs ten-year), only the ten-year endpoint. Its turnover brackets are VAT-exclusive and cover only businesses above the registration threshold.

## 6. Sole proprietors and the rest of the VAT register

- **Individuals with business income** (Table A2.4.1): 208,111 in tax year 2024, down from 248,498 in 2021 — **−16.3%**, while their *total* taxable income rose from R81.7bn to R108.9bn (+33%). Fewer declarers, more income per declarer. Treat the count as a floor (84.3% assessed).
- **VAT register composition, 2024/25** (main PDF p. 246): 82.5% companies and close corporations, 10.4% individuals (~51,700 VAT-registered individuals), 5.2% estates/trusts, 1.1% partnerships.
- **Concentration inside VAT**: the 17.4% of vendors that file monthly pay **83.5%** of Domestic VAT and receive 93.2% of refunds. The 81.1% that file bi-monthly contribute 16.4%.
- **31.8% of active vendors have annualised turnover at or below the R1m threshold** — SARS states this directly, and it is what my recomputation of Table A4.6.1 gives: **158,157 of 496,858** (38,254 of them nil). These are vendors registered but below the compulsory threshold — which is either voluntary registration, decline, or threshold lags. It also means "VAT vendor" has never been a clean proxy for "above R1m turnover", and §9 makes that worse.

## 7. What the state actually spends on small business

Budget Review 2026, Annexure B (tax expenditure, R million):

| Incentive | 2020/21 | 2021/22 | 2022/23 | 2023/24 |
|---|---|---|---|---|
| Small business corporation tax savings | 3,403 | 3,880 | 4,387 | **3,937** |
| — of which reduced headline rate | 3,285 | 3,746 | 3,707 | 3,463 |
| — of which s12E depreciation | 118 | 134 | 680 | 474 |
| Employment tax incentive (ETI) | 7,165 | 6,617 | 4,791 | **4,462** |
| Venture capital companies (s12J) | 1,001 | 1,328 | – | – |
| Special economic zones | 26 | 37 | 65 | 38 |

**Where it goes, in programme detail** (vulekamali's ENE pivot, which reproduces Table 36.2 of the 2026 ENE exactly; `scripts/ene_pivot.py`):

| Vote 36 — Small Business Development, 2026/27 | R million |
|---|---|
| 1. Administration | 217.1 |
| 2. Sector Policy and Research | 83.6 |
| 3. Integrated Cooperatives and Micro Enterprise Development | **532.2** |
| 4. Enterprise Development, Innovation and Entrepreneurship | **2,203.6** |
| — of programme 4: Entrepreneurship and Enterprise Development | 1,198.6 |
| — of programme 4: Funding Support and Coordination (the SEDFA transfer) | 984.5 |
| **Total** | **3,036.5** |
| Transfers and subsidies (71% of the vote) | 2,154.4 |
| Current payments (own operations) | 874.3 |

- **Programme 3 grew 3.7× in two years** — R142.7m (2024/25 audited) → R482.7m (2025/26) → R532.2m — and it is the only fast-growing line in the vote. It is aimed at **informal and micro enterprises**: 9,000 informal businesses to be supported over three years, 30 SMME hubs, R424.5m for equipment/tools/machinery across 150 firms, R204.6m for 600 firms' market access. Meanwhile programme 4, which funds SEDFA and the growth-facing work, **fell 5.1% a year in nominal terms** from 2022/23 to 2025/26 and is projected to grow 3.4% a year over the MTEF — below inflation, after three years of real cuts. Whatever the policy says about entrepreneurship creating jobs, the budget's growth is in survivalist support.
- **SEDFA is mostly a payroll.** It has R2,566.9m of expenditure in 2026/27, of which **40.7% compensation of employees and 49.7% goods and services** across the MTEF; **transfers and subsidies are 7.6%**. Its lending to small enterprises (R1.9bn disbursed 2024/25, R1.1bn 2025/26, R1.8bn targeted 2026/27; R1.4–1.9bn of credit guarantees) is a balance-sheet activity funded largely from interest, fees and loan recoveries, not from the budget line above. Read carefully: the R2.6bn of expenditure is mostly the cost of administering support, and the R1.8bn of disbursements is money that has to come back.
- **The support targets are large relative to the budget and small relative to the population.** SEDFA targets **100,500 firms receiving business development services in 2026/27** (2,400 incubated, 240 graduating) against 1.9m informal owners and 266k profitable companies. The whole apparatus — DSBD's R3.0bn vote, of which R2.15bn is transferred to SEDFA, plus SEDFA's own ~R1.8bn of lending — is roughly **R5bn a year gross** (the two overlap: the transfer funds SEDFA's operations, and the lending is repaid). Spread evenly over the 1.9m informal owners it would be about **R2,500 each per year**, which is the right order of magnitude for what the state could ever deliver through a department, and the wrong order of magnitude for a jobs strategy.
- **dtic spends four times as much, on firms that already exist.** Vote 39 is **R11,698.5m** (2026/27), of which **Incentives R5,437.5m** (Manufacturing Incentives R3,116.8m; Services Investment Incentives R1,057.7m) and Transformation and Competition R2,198.6m. Those are investment incentives and competitiveness support for established manufacturers and service exporters, not startup finance. There is **no line in either vote that funds equity for new firms**, and the only tax instrument that did (s12J, above) no longer carries a tax-expenditure estimate.

Three things worth saying:

1. **The tax code spends roughly three times what the department does.** Direct SBC + ETI relief in 2023/24 was **R8.4bn**, against a DSBD appropriation of **R2.8bn** — which is itself 0.26% of the R1.08tn total appropriation.
2. **The ETI is shrinking and is used by very few employers.** Claimed by **28,926 employers** in 2024/25 (R4.13bn), down from a 49,205-employer peak in 2020/21 (−41%). Against 648,500 employers on the PAYE register, that is ~4.5% of employers using the youth wage subsidy.
3. **SA's only VC-specific tax incentive was small and is gone.** s12J venture capital companies cost R1.0–1.3bn a year and has no estimate from 2022/23 onward. That is the same order as the entire SBC relief, against a private-capital market deploying R22.4bn a year (SAVCA). *(The sunset of s12J is not stated in this document — treat the cause as unverified here.)*

## 8. Budget 2026 breaks the series: the VAT threshold doubles

Table 4.6 of Budget Review 2026 (effective 1 April 2026 for VAT, 1 March 2026 otherwise):

| Measure | Current | From 2026 |
|---|---|---|
| **VAT compulsory registration threshold** | R1,000,000 | **R2,300,000** |
| **Turnover-tax (micro business) limit** | R1,000,000 | **R2,300,000** |
| Voluntary VAT registration threshold | R50,000 | R120,000 |
| Turnover tax, zero-rate band | R0–335,000 | **R0–600,000** |
| CGT exclusion, small business asset disposal | R10,000,000 | R15,000,000 |

This matters more for this project than the policy merits do:

- **47.8% of the 496,858 active vendors had annualised turnover below R2.3m** in 2024/25 (my estimate: 224,342 below R2m, plus a linear 30% of the R2–3m band = 237,353). The compulsory-VAT population is going to be **roughly halved in definition overnight**, and the register will drain slowly as below-threshold vendors deregister or new ones never register.
- Every "formal small business" count built on the VAT register (including FinScope's and any cohort I'd build) becomes **non-comparable across 2025/26 → 2026/27**. This is a bigger break than the QLFS informal-definition change flagged in the inventory note (§C), because it moves ~237k businesses out of the measured population at once.
- The turnover-tax regime now zero-rates up to R600k with a top rate of 3% above R1.4m. Combined with the R2.3m limit, the state has effectively said: below R2.3m turnover, you may stay outside VAT. If you want to study formalisation, **2026/27 is a natural experiment** and the 2027 edition of Tax Statistics is the measurement.

**What the change does to the economics, not just the accounting.** A business in the R1m–R2.3m band gets a choice it never had. If it sells to consumers, leaving VAT is close to free money: the VAT was passed on to the customer anyway, and it saves the returns and the accounting. If it sells to other VAT-registered firms, leaving is expensive — it can no longer issue a tax invoice, so its customers cannot claim input VAT, and its price has to fall by roughly the standard rate to stay competitive. **So the take-up will be uneven by sector, and it will select for businesses selling to households** — which is most informal-adjacent trade. That makes the growth effect genuinely ambiguous rather than obviously positive: less compliance cost, but for the B2B half of the band, a real loss of commercial standing. Anyone modelling this as "small firms get a tax cut" is modelling the wrong half.

**The companion regime barely exists.** Turnover tax raised **R12.1m in 2022/23**, projected at **R14.3m for 2028/29** (Budget Review 2026, revenue by type) — against R3.9bn of relief through the small-business-corporation regime. A revenue of R12m at a 1–3% rate on turnover under R1m implies something like a thousand-odd users, not the ~1.9m informal businesses the regime was built for. **The "stay small, file one simple tax" path has never attracted uptake**, which is the main reason to be sceptical that the 2026 sweetening moves many firms into the formal net — and the main reason the natural experiment is worth watching rather than predicting.

**It also invalidates the survival number in §5 for future use.** The 53.6% was measured on vendors above the R1m threshold. If ~237k of them leave the register in 2026/27, the next cohort will be dominated by larger firms, which survive better, so a naive re-run will show survival *improving* for purely definitional reasons. Any 2027-onward reuse of §5 has to state that the population changed.

## 9. Procurement: the money is published, and the size dimension exists — but only inside a Power BI report

Government is the largest customer in the economy (R1.08tn appropriated). What Treasury publishes, and in what state:

- **CSD**: 1,465,721 verified suppliers. A register, not an award record.
- **eTenders OCDS**: monthly packages from Jan 2024 to Jul 2026, ODC-**PDDL** licensed, at `data.etenders.gov.za/Home/DownloadFile/?fileName=0xMMYYYY.{json,csv,xlsx}`. The JSON carries `tender.value.amount` and `awards[].value.amount`; the CSVs **drop all value fields**.
- **OCDS API**: documented, `dateFrom`/`dateTo` required — returns **HTTP 500** on every dated request I tried (four formats and ranges). The packages leak `https://localhost:7249/api/...` in their `Uri` field.
- **Procurement Dashboard**: a 20-page Power BI *paginated report* over BAS payments. **Readable in a browser, not downloadable** — no export in the embed. This is where the size class lives.

The downloadable values don't survive a spot check. Feb 2026 has 44 award records totalling R20.9bn, with 16 awards above R100m — including **R5.32bn from Eskom**, **R4.20bn from the National Metrology Institute**, **R2.18bn from Artscape** (a publicly funded theatre) and R2.10bn from Justice. A single RFQ from a metrology institute or an opera house is not worth billions. `SupplierID` is `0` on every supplier record, so there's no key back to the CSD. **Do not total those fields.**

**The dashboard, for FY2025/26** (all four quarters, all spheres/provinces/departments; transcribed from the report's accessibility text layer, which states exact rand and percent per visual — full transcript in `data/treasury/procurement-dashboard-2025-26.md`):

| | Spend | Share of total |
|---|---|---|
| **SME (turnover under R50m)** | **R118.48bn** | **36.05%** |
| — of which EME (R0–R10m) | R75.60bn | 22.99% |
| — of which QSE (R10m–R50m) | R42.87bn | 13.04% |
| **Large business (over R50m)** | **R101.79bn** | **30.97%** |
| **Unspecified — no turnover on the supplier record** | **R108.39bn** | **32.98%** |
| Total | **R328.66bn** | 100% |
| Black owned | R134.78bn | 41.01% |
| Women owned | R50.78bn | 15.45% |
| Youth owned | R27.89bn | 8.49% |
| Disabled owned | R1.85bn | 0.56% |

Four things this settles, and three it doesn't:

- **The size dimension I said was missing does exist** — it is the supplier's turnover band (EME ≤ R10m, QSE R10m–50m, GE > R50m), and EME + QSE reproduces the SME line to the rand. I was wrong to write it off as a one-field fix on Treasury's side; the field is there, it just isn't in any file.
- **A third of the money is unclassifiable.** R108.4bn of spend sits on suppliers with no turnover recorded, and 54.82% of spend sits on suppliers with no type recorded at all. So the SME share of procurement is **36.05% of all spend** or **~53.8% of the spend that can be classified** — the policy-relevant answer lies between those and the report does not say which.
- **Both readings exceed the 30% target**, which is the trap: this is *share of spend by supplier size*, not evidence that a set-aside was applied. A 36% SME share can coexist with zero reserved contracts.
- **Designated-group shares are real, and concentrated.** Women-owned 15.45%, youth 8.49%, disabled 0.56% of spend. Black-owned 41.01%, and **one supplier takes R4.61bn of that — 3.4% of all black-owned spend, and more than the entire disabled-owned share by a factor of 2.5.**
- **Coverage and scope**: BAS payments (a separate LOGIS section covers the older system); municipalities are not here; the supplier-size views are computed on R328.66bn, while the report's own trend page shows ~R0.45tn of procurement spend for the same year — unreconciled, so don't mix the two.
- **Not measurable at all**: whether a *particular* 30% reservation was applied, and what any of this looks like below national/provincial level.

Practical note for whoever re-reads this: open the URL in a browser and use the report's accessibility output (the `.option` text in its a11y tree) — it states `"SMME Small and Medium Enterprise. Procurement Spend R118,476,268,976 (36.05%)."` per visual, which is far more reliable than reading a screenshot, and is how the table above was produced.

## 10. What this changes in the inventory note

- **Open question 5** ("is the 262k/710k/838k formal-count split resolvable from Treasury's tax statistics?") — **yes, structurally.** §2. They measure different rungs of one ladder, and the ladder is 4.14m registered → 1.38m active → 1.23m assessed → 266k profitable → 186k on the small-business regime.
- **§4G ("failure is nearly invisible")** — **partly fixed, for one segment.** The 10-year VAT cohort (§5) gives a survival floor (45.8%) and a quiet-death measure (nil-turnover survivors, 3.2% of the cohort). Nothing yet gives cohort survival *rates*.
- **§4H ("registrations at a five-year high")** — **strengthened and qualified.** Registrations are cheap and the register is 64% dormant, and the active base fell 6.5% in the same step the register rose 13.7%. Registrations are not entrepreneurship; the active-company count is the number to watch.
- **§6 ("product: nothing beyond industry")** — unchanged. Tax data has no product detail. It does add one thing the surveys lack: **size**, in turnover and taxable income, for the formal segment.

## 11. What this still cannot answer

- **A survival curve.** §5 now gives the ten-year point (53.6%). Five-year survival, and survival by size at entry, would need the cohort run for shorter windows or entry/exit counts — SARS has both, and publishes neither.
- **Job creation per business, for *formal* firms.** Tax data has no employment field at all for companies; QES is by establishment and industry; ETI is claimant-only. **Correction:** I first wrote that nothing public links a business to its employee count — that is false for the informal sector, where the SESE 2023 microdata does exactly that (see `notes/04-sese-2023-microdata.md`: 85.7% of informal businesses employ nobody, 26 paid jobs per 100 businesses, and jobs concentrate in the R50k–R250k turnover band). The gap is the formal segment and the panel, not employment as such.
- **Startup rates.** Registration dates on the CIT register would give company *age* (Table 3.8 has age bands, 2014 and 2023 only), but nothing here is a birth rate per year.
- **Informal business, at all.** Everything in this note is above the VAT or CIT threshold; the 1.9m SESE owners are invisible here, as they are in every administrative dataset.
- **Procurement below national/provincial level**, and the audit trail from reservation to award. §9 gives the shares; it cannot say whether any given set-aside was applied.
- **The informal-to-formal transition**, which is the question that actually matters for "entrepreneurship fixes unemployment" — and which a threshold change (§8) is about to make measurable, retrospectively, from the 2027 edition.

## 12. Caveats and assumptions

- **Assessment completeness.** Tax year 2024 is only **63.0%** assessed as at 31 August 2025; every 2024 column in this note is a floor, and its internal shifts (e.g. SBCs in the R1–100k turnover band rising while every other band falls) are an artefact of which returns have been processed. **Use 2023 for structure, 2024 only for direction.**
- **"Expected to submit" is derived, not a register subset** (SARS's own definition: assessed this year, plus active companies assessed in either of the two prior years but not yet assessed for this one). It is not "companies that exist".
- **Brackets are nominal.** Both the company taxable-income bands and the VAT turnover bands are fixed in rand, so ten years of inflation moves everything right. Never compare a bracket count across years without saying so.
- **Two populations still don't meet.** Nothing here measures the ~1.9m informal owners: the tax data starts above the VAT/CIT thresholds, which is precisely where SESE stops.
- **The ETI appears twice with different values**: R4,462m in the Tax Expenditure Statement (2023/24, estimated cost) and R4,204.9m in Table A2.12.1 (amount utilised). They are different measurements; don't mix them or subtract one from the other.
- **Register series are contaminated by clean-up** (§2). Don't use register growth as a business-formation series.
- **Licence.** Tax Statistics is a joint National Treasury/SARS publication, © SARS, all rights reserved on the site; the OCDS packages are ODC-PDDL. This note quotes and derives for personal research; don't republish the tables.
- **The dashboard figures are transcribed, not downloaded.** A Power BI paginated report has no export in the embed, so §9's numbers come from reading its accessibility text layer. They are exact to the rand as stated by the report, but they are a single point-in-time read of a filterable report whose filter state (2025/26, all spheres) I have recorded — if Treasury republishes or changes the model, they cannot be re-derived from a file.
- **Not read:** the Power BI payments dashboard, QES (downloaded in earlier work, still unread), and the Forecast/Budget Facility material.
- **vulekamali correction.** My first pass recorded its downloads as dead — that was my own URL construction, not the site: the resource files sit at `/datasets/<dataset>/resources/<file>`, one level *above* the per-year page that links them. The CSV is alive (4.7MB) and matches the published ENE to the rand. The genuinely dead part is `data.vulekamali.gov.za`, the "Data Portal API" the footer links to (NXDOMAIN).

## 13. Reproduce

```
cd data/treasury
uv run --with openpyxl python scripts/treasury_numbers.py     # every figure in §2-§7
python3 scripts/ocds_summary.py raw/01012026.json raw/01022026.json   # §9
uv run --with pandas python scripts/ene_pivot.py                      # §7, programme detail
```

Sources: `raw/vulekamali-ENE-2026-pivot.csv`, `raw/budget2026_FullENE.pdf` (vote 36 narrative, targets, SEDFA tables 36.14–36.16), `raw/2025 Tax Statistics - Chapter {2,3,4}*.xlsx` (unzipped from the SARS chapter zips), `raw/2016`, `raw/2020` and `raw/2021` Chapter-4 editions (the VAT vendor series and the 2015/16 base), `raw/2025_Tax_Statistics_main.pdf` (prose and the front summary), `raw/budget2026_FullBR.pdf` (Annexure B, Tables 4.6–4.7), `raw/0xMMYYYY.json` (OCDS).

## Glossary

- **Assessed**: SARS has finalised the return and issued an assessment. "Expected to submit" is larger; the gap is processing lag.
- **Tax year (companies)**: the company's own financial year, so "tax year 2023" is not a calendar year.
- **Taxable income vs turnover**: taxable income is after deductions and assessed losses, which is why 54% of companies show nil and half of all SBCs show turnover under R1m while still filing.
- **SBC / s12E**: "small business corporation" — a company with gross income ≤ R20m, all shareholders individuals, not a personal-service provider. Graduated rates instead of 27%.
- **Turnover tax (s48)**: a single simplified tax for micro businesses, replacing VAT/PAYE/provisional tax, for turnover below the limit.
- **VAT vendor, registered vs active**: registered is the register (900,285); active means returns filed in the year (496,858).
- **Annualised turnover**: declared turnover scaled to a full year, so a six-month filer isn't understated.
- **Cohort (SARS sense)**: a fixed population that met a criterion in the base year and is followed afterwards — here, vendors that filed in all ten years, so it is survivors only by construction.
- **Tax expenditure**: revenue the state forgoes through a relief, estimated against a baseline — not money spent, and not cash received by anyone.
- **OCDS**: Open Contracting Data Standard, a JSON schema for publishing tender/award/contract records.
