# Module Examples

Copy-paste examples for every module.  All examples use the sync `AMFIClient`; prefix calls with `await` and use `AsyncAMFIClient` for the async equivalent.

```python
from amfipy import AMFIClient
client = AMFIClient()
```

---

## NAV

```python
# Latest NAV — all funds
nav = client.nav.latest()
# → {"data": [{type, categories: [{category, nav: [...]}]}], "count": N}

# Latest NAV — single AMC, filtered by fund type
nav = client.nav.latest(mf_id=62, fund_type="Open Ended")

# Category-level summary (no scheme detail)
cat = client.nav.latest_by_category(mf_id="all")

# Scheme list for an AMC — use nav_id as sd_id in history calls
schemes = client.nav.schemes(mf_id=85)
# → [{"nav_id": "154043", "nav_name": "Abakkus Flexi Cap Fund - Direct - Growth", "MF_ID": "85"}, ...]

# All scheme NAVs as of a specific date
all_navs = client.nav.all_navs_for_date(date="2026-03-31")
all_df   = client.nav.all_navs_for_date(date="2026-03-31", as_df=True)

# Historical NAV — raw nested response
hist = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")
# hist["mf_name"], hist["scheme_name"], hist["nav_groups"][0]["nav_name"]

# Historical NAV — flat polars DataFrame (nav_groups auto-flattened)
hist_df = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True)
# columns: mf_name, scheme_name, nav_name, date, nav, repurchase_price, sale_price

# Batch — multiple date ranges
ranges  = [("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28")]
results = client.nav.fetch_range(sd_id=154043, months=ranges)

# High/Low NAV
hl = client.nav.high_low(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")
hl = client.nav.high_low(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31",
                         period_type="Annual", nav_type="high")  # period_type: Month|Annual

# Compare NAV on two dates
cmp    = client.nav.compare(sd_id=154043, date1="2026-01-01", date2="2026-03-31")
cmp_df = client.nav.compare(sd_id=154043, date1="2026-01-01", date2="2026-03-31", as_df=True)

# Full NAV flat file — all schemes for one date, plain-text pipe-delimited, raw bytes
nav_file = client.nav.download_file(date="31-Mar-2026")
open("navs.txt", "wb").write(nav_file)
```

**`fund_type` values:** `""` all · `"Open Ended"` · `"Close Ended"` · `"Interval Fund"`

---

## TER — MF Schemes

```python
# List available months for a financial year (first item = most recent)
months = client.ter.months(year="2025-2026")
# → [{"MonthYear": "March-2026", "MonthNumber": "03-2026"}, ...]

# Fetch TER — list of dicts
data = client.ter.fetch(month="03-2026")
data = client.ter.fetch(month="03-2026", mf_id=62, category="Equity Scheme", fund_type="Open Ended")

# Fetch TER — polars DataFrame
df = client.ter.fetch(month="03-2026", as_df=True)

# Fetch latest month automatically (omit month=)
data = client.ter.fetch(year="2025-2026")

# Batch — multiple months → dict keyed by month string
results = client.ter.fetch_range(months=["03-2026", "02-2026", "01-2026"])

# Download Excel (single-sheet .xlsx) — raw bytes
excel = client.ter.download_excel(month="03-2026")
excel = client.ter.download_excel(month="03-2026", category="Equity Scheme")
open("ter.xlsx", "wb").write(excel)

# Sub-category lookup
subcats = client.ter.sub_categories(fund_type="Open Ended", category="Equity Scheme")
```

**`category` values:** `"-1"` All · `"Equity Scheme"` · `"Debt Scheme"` · `"Hybrid Scheme"` · `"Other Scheme"` · `"Solution Oriented Scheme"`  
**`fund_type` values:** `"-1"` All · `"Open Ended"` · `"Close Ended"` · `"Interval Fund"`

---

## TER — SIF Schemes

Same interface as MF TER; use `sif_id` instead of `mf_id`:

```python
months = client.sif_ter.months(year="2025-2026")
data   = client.sif_ter.fetch(month="03-2026", sif_id="All", as_df=True)
excel  = client.sif_ter.download_excel(month="03-2026")
```

---

## Fund Performance

```python
# All filter options — maturity types, categories, full AMC list with IDs
filters = client.fund_performance.filters()
# → {"maturityTypeList": [...], "investmentTypeList": [...], "mutualFundList": [...]}

# Sub-categories for a category
subcats = client.fund_performance.sub_categories(category=1)  # 1=Equity

# Fetch performance
perf = client.fund_performance.fetch(
    maturity_type=1,           # 1=Open Ended, 2=Close Ended
    category=1,                # 1=Equity, 2=Debt, 3=Hybrid, 4=Solution Oriented, 5=Other
    sub_category=1,            # ID from sub_categories()
    mf_id=0,                   # 0=All, or fund ID from filters()["mutualFundList"]
    report_date="07-May-2026", # DD-Mon-YYYY; omit for last business day
)
```

!!! note
    No server-side Excel download — the AMFI site generates it client-side only.

---

## Tracking Error & Difference

```python
# Tracking Error — lowercase month in date
error    = client.tracking.error(date="31-mar-2026")
error    = client.tracking.error(date="31-mar-2026", mf_id=62)  # single AMC
error_df = client.tracking.error(date="31-mar-2026", as_df=True)

# Batch
errors = client.tracking.error_range(dates=["31-mar-2026", "28-feb-2026", "31-jan-2026"])

# Tracking Difference — title-case month, always day=01
diff    = client.tracking.difference(month="01-Apr-2026")
diff    = client.tracking.difference(month="01-Apr-2026", mf_id="all")
diff_df = client.tracking.difference(month="01-Apr-2026", as_df=True)

# Batch
diffs = client.tracking.difference_range(months=["01-Apr-2026", "01-Mar-2026"])
```

---

## Risk Parameters

```python
# date: "01-Mon-YYYY" — always day=01
# category_id: numeric SEBI category (17 = Mid Cap Fund)
risk    = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17)
risk_df = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17, as_df=True)

# Batch across months
results = client.risk_parameters.fetch_range(
    dates=["01-Mar-2026", "01-Feb-2026", "01-Jan-2026"],
    category_id=17,
)
```

---

## NFO — New Fund Offers

```python
# Full grouped response
nfos = client.nfo.fetch()
# → {"NewFundOffer": [{"MutualFund": "...", "items": [{Scheme_Id, SchemeName, MF_Id}]}]}

# Flat list (no AMC grouping)
items = client.nfo.flat()
# → [{"Scheme_Id": 14475, "MutualFund": "Axis Mutual Fund", "SchemeName": "...", "MF_Id": 53}, ...]

# Polars DataFrame
df = client.nfo.fetch(as_df=True)
```

---

## Publications

These methods return **metadata** (titles + URLs).  Use `download_file(url)` to get the actual bytes.

```python
# Monthly reports — flat list across all financial years
flat = client.publications.monthly_flat()
# → [{"Title": "March 2026", "month": "03", "year": "2026",
#     "pdf_url": "...", "excel_url": "...", "financial_year": "..."}, ...]

# Download the latest month's XLS (multi-sheet workbook)
xls = client.publications.download_file(flat[0]["excel_url"])
open("amfi_monthly.xls", "wb").write(xls)

# Also available grouped by financial year
grouped = client.publications.monthly()

# Quarterly issues
flat_q   = client.publications.quarterly_flat()
grouped_q = client.publications.quarterly()
# → [{"issue_no": "Issue IV", "period": "(Jan - Mar 2026)", "pdf_url": "...", "excel_url": "..."}, ...]

# Annual commission disclosures
commission = client.publications.commission()
# → [{"Period": "FY 2024 - 2025", "URL": "https://..."}, ...]
pdf = client.publications.download_file(commission[0]["URL"])
open("commission_fy24_25.pdf", "wb").write(pdf)
```

---

## CDMDF NAV

```python
# Historical CDMDF NAV — date: "DD-mon-YYYY" lowercase
cdmdf    = client.cdmdf.history(date="31-mar-2026")
cdmdf_df = client.cdmdf.history(date="31-mar-2026", as_df=True)

# Batch → dict keyed by date
results = client.cdmdf.history_range(dates=["31-mar-2026", "28-feb-2026"])
```

---

## AUM — Assets Under Management

=== "Average AUM"

    ```python
    # Step 1 — list financial years
    fys = client.aum.financial_years()
    # → [{"id": 1, "financial_year": "April 2025 - March 2026"}, ...]

    # Step 2 — list quarters for a year
    periods = client.aum.periods(fy_id=1)
    # → {"financial_year": "...", "periods": [{"id": 1, "period": "January - March 2026"}, ...]}

    # Fund-wise average AUM
    data  = client.aum.average_aum_fundwise(fy_id=1, period_id=1)
    df    = client.aum.average_aum_fundwise(fy_id=1, period_id=1, as_df=True)
    excel = client.aum.average_aum_fundwise_excel(fy_id=1, period_id=1)

    # Scheme-wise average AUM  (str_type: "Categorywise" | "Typewise", mf_id: 0=All)
    data  = client.aum.average_aum_schemewise(fy_id=1, period_id=1, str_type="Categorywise", mf_id=62)
    df    = client.aum.average_aum_schemewise(fy_id=1, period_id=1, as_df=True)
    excel = client.aum.average_aum_schemewise_excel(fy_id=1, period_id=1, str_type="Typewise")
    ```

=== "AUM–AAUM Disclosure"

    ```python
    # fyId: "2025-26", "2024-25" (shortened financial year)

    # By fund category
    disc_cat = client.aum.disclosure_by_category(fy_id="2025-26")
    # → [{"Period": "(Oct - Dec 2025)", "pdfURL": "...", "excelURL": "..."}, ...]
    df = client.aum.disclosure_by_category(fy_id="2025-26", as_df=True)

    # By geography
    disc_geo = client.aum.disclosure_by_geography(fy_id="2025-26")
    df       = client.aum.disclosure_by_geography(fy_id="2025-26", as_df=True)
    ```

=== "Age-wise / Folio"

    ```python
    # month: "MonthName-YYYY"
    af    = client.aum.agewise_folio(month="March-2026")
    # raw → {"data": {"investorClassification": [...], "ageWiseAUM": [...]}}

    af_df = client.aum.agewise_folio(month="March-2026", as_df=True)
    # flattens ageWiseAUM → classifications into flat rows
    # columns: schemeTypeName, ageGroup, noOfFolios, AUM

    excel = client.aum.agewise_folio_excel(month="March-2026")
    ```

=== "Classified AUM"

    ```python
    # date: "01-mon-yyyy" — lowercase month, always day=01

    # List available months
    dates = client.aum.classified_dates()
    # → [{"date": "April-2026"}, {"date": "March-2026"}, ...]

    # State-wise classified AUM
    sw    = client.aum.statewise(date="01-apr-2026", mf_id=0)
    sw_df = client.aum.statewise(date="01-apr-2026", as_df=True)
    excel = client.aum.statewise_excel(date="01-apr-2026")

    # Scheme-category-wise classified AUM
    sc    = client.aum.scheme_catwise(date="01-apr-2026", mf_id=0)
    sc_df = client.aum.scheme_catwise(date="01-apr-2026", as_df=True)
    excel = client.aum.scheme_catwise_excel(date="01-apr-2026")
    ```

=== "Bifurcation of AUM"

    ```python
    # date: "DD-Mon-YYYY"
    bif = client.aum.bifurcation(date="31-Mar-2026")
    # → [{"Month_Date": "31-Mar-2026",
    #     "TotalAAUMunderDirectPlan": 3904766.42,
    #     "AAUMunderRegisteredAdvisers": 537599.97,
    #     "AAUMunderPMS": 89942.62,
    #     "AAUMunderDIYclients": 3277223.84}]

    bif_df  = client.aum.bifurcation(date="31-Mar-2026", as_df=True)
    results = client.aum.bifurcation_range(dates=["31-Mar-2026", "28-Feb-2026", "31-Jan-2026"])
    excel   = client.aum.bifurcation_excel(date="31-Mar-2026")
    ```

---

## Other Data

=== "Investor Complaints"

    ```python
    # Monthly — 4 parts (A–D), fetch each separately
    # month: "MonthName-YYYY"  |  part: 1=Part A (SEBI SCORES), 2=B, 3=C (ODR), 4=D
    complaints = client.other_data.investor_complaints_monthly(
        month="March-2026", mf_id=62, part=1   # mf_id=0 for all AMCs
    )
    df = client.other_data.investor_complaints_monthly(
        month="March-2026", mf_id=62, part=1, as_df=True
    )

    # Yearly — "YYYY-YYYY"; historical only (up to FY 2020-21)
    yearly = client.other_data.investor_complaints_yearly(year="2019-2020", mf_id=62)
    df     = client.other_data.investor_complaints_yearly(year="2019-2020", as_df=True)
    ```

=== "Directors & Trustees"

    ```python
    # AMC board directors
    directors    = client.other_data.amc_directors(mf_id=62)   # single AMC
    directors_df = client.other_data.amc_directors(mf_id=0, as_df=True)  # all AMCs

    # Trustees
    trustees    = client.other_data.trustees(mf_id=62)
    trustees_df = client.other_data.trustees(mf_id=0, as_df=True)
    ```

=== "Group Companies"

    ```python
    # One page (default 10 records)
    page = client.other_data.group_companies(page=1, size=10)
    # → {"data": [...], "pagination": {"total": 599, ...}}

    # All ~599 records — auto-paginated
    all_cos = client.other_data.group_companies_all()
    all_df  = client.other_data.group_companies_all(as_df=True)
    ```

=== "Scheme Dividends"

    ```python
    # Step 1 — get scheme list for an AMC
    schemes = client.other_data.populate_schemes(mf_id=62)
    # → [{"scheme_id": "13771", "scheme_name": "360 ONE Balanced Hybrid Fund"}, ...]

    # Step 2 — fetch dividend history
    divs    = client.other_data.scheme_dividends(
                  mf_id=62, sd_id=schemes[0]["scheme_id"], year=2026
              )
    divs_df = client.other_data.scheme_dividends(
                  mf_id=62, sd_id=schemes[0]["scheme_id"], year=2026, as_df=True
              )
    ```

=== "Scheme Data & Details"

    ```python
    schemes = client.other_data.populate_schemes(mf_id=62)
    sd_id   = schemes[0]["scheme_id"]

    # NAV for all plan/option variants (Direct Growth, Regular IDCW, etc.)
    nav_rows = client.other_data.scheme_data(mf_id=62, sd_id=sd_id)
    # → [{"Scheme_NAV_Name": "...", "ISIN_Div_Payout_ISIN_Growth": "INF...",
    #     "Net_Asset_Value": "13.32", "Date": "2026-05-08T00:00:00", ...}, ...]
    nav_df = client.other_data.scheme_data(mf_id=62, sd_id=sd_id, as_df=True)

    # Full scheme profile — returns a single dict, no as_df option
    info = client.other_data.scheme_details(mf_id=62, sd_id=sd_id)
    # → {"Scheme_Name": "...", "Scheme_Objective": "...",
    #    "SchemeType_Desc": "Open Ended", "SchemeCat_Desc": "Hybrid Scheme",
    #    "Scheme_min_amt": "1000", "Launch_Date": "...",
    #    "Scheme_load": "Nil", "AMC_Website": "https://..."}
    ```

=== "AMC Accounts"

    ```python
    # Returns URL references to external PDF statements (not raw financials)
    ann_links  = client.other_data.accounts_annual(mf_id=62)
    half_links = client.other_data.accounts_half_yearly(mf_id=62)
    ```

---

## Research — Categorisation of Stocks

SEBI's average market capitalisation reference list — published bi-annually (Jan–Jun, Jul–Dec) from 2017 onwards.

```python
# Dict keyed by year, each value a list of period entries
data = client.research.categorisation_of_stocks()
# → {"2024": [{"period": "Jul - Dec", "pdfUrl": "...", "excelUrl": "..."}, ...], "2023": [...], ...}

# Flat list sorted oldest → newest
flat = client.research.categorisation_of_stocks_flat()
# → [{"year": "2017", "period": "Jul - Dec", "pdfUrl": "...", "excelUrl": "..."}, ...]

# Polars DataFrame (columns: year, period, pdfUrl, excelUrl)
df = client.research.categorisation_of_stocks(as_df=True)

# Download a file (PDF or Excel) — raw bytes
latest = flat[-1]
excel  = client.research.download_categorisation_file(latest["excelUrl"])
open("categ_latest.xlsx", "wb").write(excel)

pdf = client.research.download_categorisation_file(latest["pdfUrl"])
open("categ_latest.pdf", "wb").write(pdf)
```
