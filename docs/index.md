# amfipy

Python client for **AMFI India** — the Association of Mutual Funds in India.  
Clean, typed access to NAV, TER, AUM, Fund Performance, Tracking Error, Risk Parameters, NFOs, Publications, and more.  Both **sync** and **async** interfaces are included.

---

## Installation

```bash
pip install amfipy
```

Add polars DataFrame support (needed for `as_df=True`):

```bash
pip install amfipy[polars]
```

---

## Quick Start

Five minutes to your first data pull.

```python
from amfipy import AMFIClient

client = AMFIClient()

# ── NAV ──────────────────────────────────────────────────────────────────────
# Latest NAV for all funds
nav = client.nav.latest()

# Historical NAV as a polars DataFrame (auto-flattens nested structure)
df = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True)

# ── TER ──────────────────────────────────────────────────────────────────────
# Download March 2026 TER Excel (raw bytes — save anywhere)
excel_bytes = client.ter.download_excel(month="03-2026")
open("ter_march_2026.xlsx", "wb").write(excel_bytes)

# Or fetch as a polars DataFrame
ter_df = client.ter.fetch(month="03-2026", as_df=True)

# ── Tracking ─────────────────────────────────────────────────────────────────
error_df = client.tracking.error(date="31-mar-2026", as_df=True)

# ── AUM ──────────────────────────────────────────────────────────────────────
bif_df = client.aum.bifurcation(date="31-Mar-2026", as_df=True)
```

### Async

Every method is also available on `AsyncAMFIClient` with an identical signature — just `await` the calls:

```python
import asyncio
from amfipy import AsyncAMFIClient

async def main():
    client = AsyncAMFIClient()

    # Fetch three datasets concurrently
    ter, nav, nfo = await asyncio.gather(
        client.ter.fetch(month="03-2026", as_df=True),
        client.nav.all_navs_for_date(date="2026-03-31"),
        client.nfo.flat(),
    )
    return ter, nav, nfo

asyncio.run(main())
```

---

## User Guide

### Sync vs Async

| | Sync | Async |
|---|---|---|
| Client | `AMFIClient` | `AsyncAMFIClient` |
| Import | `from amfipy import AMFIClient` | `from amfipy import AsyncAMFIClient` |
| Call style | `client.nav.latest()` | `await client.nav.latest()` |
| Use when | Scripts, notebooks, one-off pulls | Web servers, concurrent fetches, high throughput |

Both clients share the same sub-module attributes (`nav`, `ter`, `tracking`, …) and identical method signatures — only the `await` keyword differs.

---

### `as_df=True` — Polars DataFrames

Any method with an `as_df` parameter can return a **polars DataFrame** instead of a raw Python list or dict.  This is optional — the default always returns plain Python objects.

```python
# Default — plain Python list of dicts
records = client.ter.fetch(month="03-2026")
# → [{"MF_Name": "HDFC...", "TER": "0.74", ...}, ...]

# With as_df=True — polars DataFrame
df = client.ter.fetch(month="03-2026", as_df=True)
# → shape: (5000, 10)  [5000 rows × 10 columns]

print(df.head(3))
print(df.filter(pl.col("Category") == "Equity Scheme").shape)
```

!!! tip "Nested structures are flattened automatically"
    Some APIs return nested data (e.g. NAV history has `nav_groups → historical_records`).
    Passing `as_df=True` always resolves the nesting into a flat table — you never need to
    loop through inner lists yourself.

    ```python
    # Raw — nested dict with nav_groups list inside
    raw = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")
    # raw["nav_groups"][0]["historical_records"][0] → {"date": "2026-01-02", "nav": "..."}

    # as_df=True — flat DataFrame, ready to use
    df = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True)
    # df columns: mf_name, scheme_name, nav_name, date, nav, repurchase_price, sale_price
    ```

---

### Excel & File Downloads

Methods that end in `_excel()` (or `download_file()` / `download_categorisation_file()`) return raw **bytes**.  Save them directly — no parsing needed.

```python
# TER Excel (single-sheet .xlsx)
excel = client.ter.download_excel(month="03-2026")
open("ter_march_2026.xlsx", "wb").write(excel)

# AUM bifurcation Excel
excel = client.aum.bifurcation_excel(date="31-Mar-2026")
open("aum_bif.xlsx", "wb").write(excel)

# AMFI monthly report — first get the URL from metadata, then download
entries = client.publications.monthly_flat()
xls_bytes = client.publications.download_file(entries[0]["excel_url"])
open("amfi_monthly.xls", "wb").write(xls_bytes)

# Full NAV flat file — plain-text, all schemes for one date
nav_txt = client.nav.download_file(date="31-Mar-2026")
open("navs.txt", "wb").write(nav_txt)
```

---

### Batch Fetching — `fetch_range()`

Every module that has time-series data includes a `fetch_range()` method for pulling multiple periods in one call.

```python
# TER — multiple months
results = client.ter.fetch_range(months=["03-2026", "02-2026", "01-2026"])
# → {"03-2026": [...], "02-2026": [...], "01-2026": [...]}

# NAV history — multiple date ranges for one scheme
ranges = [("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28")]
results = client.nav.fetch_range(sd_id=154043, months=ranges)
# → [<Jan data>, <Feb data>]

# Tracking error — multiple month-end dates
errors = client.tracking.error_range(dates=["31-mar-2026", "28-feb-2026", "31-jan-2026"])

# Risk parameters — multiple months
risk = client.risk_parameters.fetch_range(
    dates=["01-Mar-2026", "01-Feb-2026", "01-Jan-2026"],
    category_id=17,
)
```

The async client runs range fetches concurrently (`asyncio.gather`) for much better throughput.

---

### Custom HTTP Settings

All clients accept any `httpx` kwargs (proxy, SSL, timeout, headers):

```python
from amfipy import AMFIClient

client = AMFIClient(
    proxies={"https://": "http://myproxy:8080"},
    verify=False,   # disable SSL verification
    timeout=120,    # seconds
)
```

---

### Date Format Reference

AMFI uses several date formats across different endpoints.

| Module / method | Parameter | Format | Example |
|---|---|---|---|
| `nav.history`, `nav.all_navs_for_date` | `from_date`, `to_date`, `date` | `YYYY-MM-DD` | `"2026-03-31"` |
| `nav.download_file` | `date` | `DD-Mon-YYYY` | `"31-Mar-2026"` |
| `tracking.error`, `cdmdf.history` | `date` | `DD-mon-YYYY` **lowercase** | `"31-mar-2026"` |
| `tracking.difference` | `month` | `DD-Mon-YYYY` title-case, **always day=01** | `"01-Apr-2026"` |
| `risk_parameters.fetch` | `date` | `DD-Mon-YYYY` title-case, **always day=01** | `"01-Mar-2026"` |
| `ter.fetch`, `ter.download_excel` | `month` | `MM-YYYY` | `"03-2026"` |
| `aum.agewise_folio` | `month` | `MonthName-YYYY` | `"March-2026"` |
| `aum.statewise`, `aum.scheme_catwise` | `date` | `DD-mon-yyyy` **lowercase**, always day=01 | `"01-apr-2026"` |
| `aum.bifurcation` | `date` | `DD-Mon-YYYY` | `"31-Mar-2026"` |
| `other_data.investor_complaints_monthly` | `month` | `MonthName-YYYY` | `"March-2026"` |

---

### Financial Year Format

AMFI financial years run **April – March** and are written as `YYYY-YYYY`:

```python
months = client.ter.months(year="2025-2026")
# → [{"MonthYear": "March-2026", "MonthNumber": "03-2026"},
#    {"MonthYear": "February-2026", "MonthNumber": "02-2026"}, ...]
# First item is always the most recent available month.

# AUM–AAUM Disclosure uses a shortened format: "2025-26"
disc = client.aum.disclosure_by_category(fy_id="2025-26")
```

---

### AMC IDs

Numeric AMC IDs are used across NAV, TER, AUM, and Other Data endpoints.

| ID | AMC |
|---|---|
| `0` / `"all"` / `"All"` | All AMCs (varies by endpoint — check parameter docs) |
| `3` | Aditya Birla Sun Life Mutual Fund |
| `53` | Axis Mutual Fund |
| `62` | 360 ONE Mutual Fund |
| `85` | Abakkus Mutual Fund |

Get the full list with IDs from:

```python
filters = client.fund_performance.filters()
amc_list = filters["mutualFundList"]
# → [{"id": 3, "name": "Aditya Birla Sun Life Mutual Fund"}, ...]
```

---

## Module Examples

### NAV

```python
# Latest NAV — all funds
nav = client.nav.latest()

# Latest NAV — single AMC, Open Ended only
nav = client.nav.latest(mf_id=62, fund_type="Open Ended")

# Category-level summary
cat = client.nav.latest_by_category(mf_id="all")

# Scheme list for an AMC (use nav_id as sd_id in history calls)
schemes = client.nav.schemes(mf_id=85)
# → [{"nav_id": "154043", "nav_name": "Abakkus Flexi Cap Fund - Direct - Growth", "MF_ID": "85"}, ...]

# All scheme NAVs for a specific date
all_navs = client.nav.all_navs_for_date(date="2026-03-31")

# Historical NAV — raw nested dict
hist = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")
# hist["nav_groups"][0]["nav_name"] → "Abakkus Flexi Cap Fund - Direct - Growth"

# Historical NAV — flat polars DataFrame
hist_df = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True)
# columns: mf_name, scheme_name, nav_name, date, nav, repurchase_price, sale_price

# High/Low NAV
hl = client.nav.high_low(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")
hl = client.nav.high_low(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31",
                         period_type="Annual", nav_type="high")

# Compare NAV on two dates
cmp = client.nav.compare(sd_id=154043, date1="2026-01-01", date2="2026-03-31")

# Full NAV flat file (all schemes, one date) — returns bytes
nav_file = client.nav.download_file(date="31-Mar-2026")
open("navs.txt", "wb").write(nav_file)
```

**`fund_type` values:** `""` (all), `"Open Ended"`, `"Close Ended"`, `"Interval Fund"`

---

### TER (MF Schemes)

```python
# List available months for a financial year
months = client.ter.months(year="2025-2026")
# → [{"MonthYear": "March-2026", "MonthNumber": "03-2026"}, ...]

# Fetch TER as a list of dicts
data = client.ter.fetch(month="03-2026")
data = client.ter.fetch(month="03-2026", mf_id=62, category="Equity Scheme", fund_type="Open Ended")

# Fetch as polars DataFrame
df = client.ter.fetch(month="03-2026", as_df=True)

# Fetch latest month automatically (no month= needed)
data = client.ter.fetch(year="2025-2026")

# Batch fetch across multiple months
results = client.ter.fetch_range(months=["03-2026", "02-2026", "01-2026"])
# → {"03-2026": [...], "02-2026": [...], "01-2026": [...]}

# Download Excel (raw bytes)
excel = client.ter.download_excel(month="03-2026")
excel = client.ter.download_excel(month="03-2026", category="Equity Scheme")
open("ter.xlsx", "wb").write(excel)

# Sub-category lookup
subcats = client.ter.sub_categories(fund_type="Open Ended", category="Equity Scheme")
```

**`category` values:** `"-1"` All, `"Equity Scheme"`, `"Debt Scheme"`, `"Hybrid Scheme"`, `"Other Scheme"`, `"Solution Oriented Scheme"`

### TER (SIF Schemes)

Same interface as MF TER — use `sif_id` instead of `mf_id`:

```python
months = client.sif_ter.months(year="2025-2026")
data   = client.sif_ter.fetch(month="03-2026", sif_id="All")
excel  = client.sif_ter.download_excel(month="03-2026")
```

---

### Fund Performance

```python
# All filter options (maturity types, categories, AMC list)
filters = client.fund_performance.filters()
# → {"maturityTypeList": [...], "investmentTypeList": [...], "mutualFundList": [...]}

# Sub-categories for a category
subcats = client.fund_performance.sub_categories(category=1)  # 1=Equity

# Fetch performance data
perf = client.fund_performance.fetch(
    maturity_type=1,          # 1=Open Ended, 2=Close Ended
    category=1,               # 1=Equity, 2=Debt, 3=Hybrid, 4=Solution Oriented, 5=Other
    sub_category=1,           # from sub_categories()
    mf_id=0,                  # 0=All, or fund ID from filters()["mutualFundList"]
    report_date="07-May-2026",# "DD-Mon-YYYY"; omit for last business day
)
```

!!! note
    The AMFI website generates the Excel export client-side only. There is no server-side download endpoint.

---

### Tracking Error & Difference

```python
# Tracking Error — one record per index/ETF scheme
error    = client.tracking.error(date="31-mar-2026")           # lowercase month
error    = client.tracking.error(date="31-mar-2026", mf_id=62) # single AMC
error_df = client.tracking.error(date="31-mar-2026", as_df=True)

# Batch
errors = client.tracking.error_range(dates=["31-mar-2026", "28-feb-2026"])

# Tracking Difference — title-case month, always day=01
diff    = client.tracking.difference(month="01-Apr-2026")
diff    = client.tracking.difference(month="01-Apr-2026", mf_id="all")

# Batch
diffs = client.tracking.difference_range(months=["01-Apr-2026", "01-Mar-2026"])
```

---

### Risk Parameters

```python
# date format: "01-Mon-YYYY" — always day=01
# category_id: numeric SEBI category (e.g. 17 = Mid Cap Fund)
risk    = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17)
risk_df = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17, as_df=True)

# Batch across months
results = client.risk_parameters.fetch_range(
    dates=["01-Mar-2026", "01-Feb-2026", "01-Jan-2026"],
    category_id=17,
)
```

---

### New Fund Offers (NFO)

```python
# Full response — grouped by AMC
nfos = client.nfo.fetch()
# → {"NewFundOffer": [{"MutualFund": "...", "items": [{Scheme_Id, SchemeName, MF_Id}]}]}

# Flat list (no AMC grouping)
items = client.nfo.flat()
# → [{"Scheme_Id": 14475, "MutualFund": "...", "SchemeName": "...", "MF_Id": 53}, ...]

# Polars DataFrame
df = client.nfo.fetch(as_df=True)
```

---

### Publications (Monthly, Quarterly, Commission)

These methods return **metadata** (titles + URLs). Use `download_file(url)` to get the actual bytes.

```python
# Monthly reports — flat list across all financial years
flat = client.publications.monthly_flat()
# → [{"Title": "March 2026", "month": "03", "year": "2026",
#     "pdf_url": "...", "excel_url": "...", "financial_year": "..."}, ...]

# Download the latest month's XLS (multi-sheet workbook)
xls = client.publications.download_file(flat[0]["excel_url"])
open("amfi_monthly.xls", "wb").write(xls)

# Quarterly issues
flat_q = client.publications.quarterly_flat()
# → [{"issue_no": "Issue IV", "period": "(Jan - Mar 2026)", "pdf_url": "...", "excel_url": "..."}, ...]

# Annual commission disclosures (PDF list)
commission = client.publications.commission()
# → [{"Period": "FY 2024 - 2025", "URL": "https://..."}, ...]
pdf = client.publications.download_file(commission[0]["URL"])
```

---

### CDMDF NAV

```python
# Historical CDMDF NAV — lowercase month
cdmdf    = client.cdmdf.history(date="31-mar-2026")
cdmdf_df = client.cdmdf.history(date="31-mar-2026", as_df=True)

# Batch
results = client.cdmdf.history_range(dates=["31-mar-2026", "28-feb-2026"])
```

---

### AUM (Assets Under Management)

Five sub-sections — all under `client.aum`.

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
    excel = client.aum.average_aum_fundwise_excel(fy_id=1, period_id=1)

    # Scheme-wise average AUM (str_type: "Categorywise" | "Typewise")
    data  = client.aum.average_aum_schemewise(fy_id=1, period_id=1, str_type="Categorywise", mf_id=62)
    excel = client.aum.average_aum_schemewise_excel(fy_id=1, period_id=1, str_type="Typewise")
    ```

=== "Disclosure"

    ```python
    # fyId format: "2025-26", "2024-25" (shortened financial year)
    disc_cat = client.aum.disclosure_by_category(fy_id="2025-26")
    # → [{"Period": "(Oct - Dec 2025)", "pdfURL": "...", "excelURL": "..."}, ...]

    disc_geo = client.aum.disclosure_by_geography(fy_id="2025-26")
    ```

=== "Age-wise / Folio"

    ```python
    # month format: "MonthName-YYYY"
    af    = client.aum.agewise_folio(month="March-2026")
    af_df = client.aum.agewise_folio(month="March-2026", as_df=True)  # flattens age bands
    excel = client.aum.agewise_folio_excel(month="March-2026")
    ```

=== "Classified AUM"

    ```python
    # date format: "01-mon-yyyy" — lowercase month, always day=01
    dates = client.aum.classified_dates()
    # → [{"date": "April-2026"}, {"date": "March-2026"}, ...]

    # State-wise
    sw    = client.aum.statewise(date="01-apr-2026", mf_id=0)
    excel = client.aum.statewise_excel(date="01-apr-2026")

    # Scheme-category-wise
    sc    = client.aum.scheme_catwise(date="01-apr-2026", mf_id=0)
    excel = client.aum.scheme_catwise_excel(date="01-apr-2026")
    ```

=== "Bifurcation"

    ```python
    # date format: "DD-Mon-YYYY"
    bif = client.aum.bifurcation(date="31-Mar-2026")
    # → [{"Month_Date": "31-Mar-2026",
    #     "TotalAAUMunderDirectPlan": 3904766.42,
    #     "AAUMunderRegisteredAdvisers": 537599.97,
    #     "AAUMunderPMS": 89942.62,
    #     "AAUMunderDIYclients": 3277223.84}]

    bif_df  = client.aum.bifurcation(date="31-Mar-2026", as_df=True)
    results = client.aum.bifurcation_range(dates=["31-Mar-2026", "28-Feb-2026"])
    excel   = client.aum.bifurcation_excel(date="31-Mar-2026")
    ```

---

### Other Data

```python
# ── Investor Complaints ───────────────────────────────────────────────────────
# Monthly report — 4 parts (A–D); fetch each separately
# month format: "MonthName-YYYY"
complaints = client.other_data.investor_complaints_monthly(
    month="March-2026",
    mf_id=62,   # 0 = All AMCs
    part=1,     # 1=Part A (SEBI SCORES), 2=B, 3=C (SEBI ODR), 4=D
)
complaints_df = client.other_data.investor_complaints_monthly(
    month="March-2026", mf_id=62, part=1, as_df=True
)

# Yearly — "YYYY-YYYY" format; historical data only (up to FY 2021)
yearly = client.other_data.investor_complaints_yearly(year="2019-2020", mf_id=62)

# ── AMC Directors & Trustees ──────────────────────────────────────────────────
directors    = client.other_data.amc_directors(mf_id=62)
directors_df = client.other_data.amc_directors(mf_id=0, as_df=True)  # all AMCs
trustees     = client.other_data.trustees(mf_id=62)

# ── Group Companies (~599 total records) ──────────────────────────────────────
page    = client.other_data.group_companies(page=1, size=10)   # one page
all_cos = client.other_data.group_companies_all()              # all, auto-paginated
all_df  = client.other_data.group_companies_all(as_df=True)

# ── Scheme Dividends ──────────────────────────────────────────────────────────
# Step 1: get scheme list for an AMC
schemes = client.other_data.populate_schemes(mf_id=62)
# → [{"scheme_id": "13771", "scheme_name": "360 ONE Balanced Hybrid Fund"}, ...]

# Step 2: fetch dividend history
divs    = client.other_data.scheme_dividends(mf_id=62, sd_id=schemes[0]["scheme_id"], year=2026)
divs_df = client.other_data.scheme_dividends(mf_id=62, sd_id=schemes[0]["scheme_id"],
                                             year=2026, as_df=True)

# ── Scheme Data & Details ─────────────────────────────────────────────────────
sd_id = schemes[0]["scheme_id"]

# NAV for all plan/option variants (Direct Growth, Regular IDCW, etc.)
nav_rows = client.other_data.scheme_data(mf_id=62, sd_id=sd_id)
# → [{"Scheme_NAV_Name": "...", "ISIN_Div_Payout_ISIN_Growth": "INF...",
#     "Net_Asset_Value": "13.32", "Date": "2026-05-08T00:00:00", ...}, ...]

# Full scheme profile (objective, load, min amount, AMC website)
info = client.other_data.scheme_details(mf_id=62, sd_id=sd_id)
# → {"Scheme_Name": "...", "Scheme_Objective": "...",
#    "SchemeType_Desc": "Open Ended", "SchemeCat_Desc": "Hybrid Scheme",
#    "Scheme_min_amt": "1000", "Launch_Date": "...",
#    "Scheme_load": "Nil", "AMC_Website": "https://..."}

# ── AMC Account Disclosures ───────────────────────────────────────────────────
# Returns lists of dicts with external URL references (not raw financials)
ann_links  = client.other_data.accounts_annual(mf_id=62)
half_links = client.other_data.accounts_half_yearly(mf_id=62)
```

---

### Research — Categorisation of Stocks

SEBI's average market capitalisation reference list — published bi-annually from 2017.

```python
# Dict keyed by year, each value a list of period entries
data = client.research.categorisation_of_stocks()
# → {"2024": [{"period": "Jul - Dec", "pdfUrl": "...", "excelUrl": "..."}, ...], ...}

# Flat list sorted oldest → newest
flat = client.research.categorisation_of_stocks_flat()
# → [{"year": "2017", "period": "Jul - Dec", "pdfUrl": "...", "excelUrl": "..."}, ...]

# Polars DataFrame (year, period, pdfUrl, excelUrl)
df = client.research.categorisation_of_stocks(as_df=True)

# Download the latest Excel file (ranked company list with market cap and classification)
latest = client.research.categorisation_of_stocks_flat()[-1]
excel  = client.research.download_categorisation_file(latest["excelUrl"])
open("categ_latest.xlsx", "wb").write(excel)
```

---

## Polars → Apache Spark (Iceberg)

`as_df=True` returns a polars DataFrame. Convert to a Spark DataFrame via Arrow — **zero-copy, no pandas required**.

```python
from amfipy import AMFIClient
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("amfi-iceberg-ingest")
    .config("spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.local.type", "hadoop")
    .config("spark.sql.catalog.local.warehouse", "/tmp/iceberg-warehouse")
    .getOrCreate()
)

client = AMFIClient()

# The pattern: polars → Arrow → Spark (works for any as_df=True method)
nav_pl = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True)
spark.createDataFrame(nav_pl.to_arrow()).writeTo("local.amfi.nav_history").createOrReplace()

ter_pl = client.ter.fetch(month="03-2026", as_df=True)
spark.createDataFrame(ter_pl.to_arrow()).writeTo("local.amfi.ter").createOrReplace()

tracking_pl = client.tracking.error(date="31-mar-2026", as_df=True)
spark.createDataFrame(tracking_pl.to_arrow()).writeTo("local.amfi.tracking_error").createOrReplace()

# Append mode for incremental daily loads
for date in ["31-Mar-2026", "28-Feb-2026", "31-Jan-2026"]:
    bif_pl = client.aum.bifurcation(date=date, as_df=True)
    spark.createDataFrame(bif_pl.to_arrow()).writeTo("local.amfi.aum_bifurcation").append()

# Query
spark.sql("SELECT scheme_name, date, nav FROM local.amfi.nav_history ORDER BY date DESC").show()
```

**Production tips:**

- Use a Hive metastore or AWS Glue catalog instead of `hadoop` for multi-cluster access
- Partition Iceberg tables by date for efficient time-range queries
- Use `.append()` for daily loads; `.createOrReplace()` for full refreshes
- For the full NAV flat file, write `client.nav.download_file()` bytes to S3/HDFS and read with `spark.read.text()`

---

## Data Coverage

| Data | Client method | Excel / file | `as_df=True` |
|---|---|:---:|:---:|
| NAV — Latest | `client.nav.latest()` | — | — |
| NAV — History | `client.nav.history()` | — | ✅ |
| NAV — High/Low | `client.nav.high_low()` | — | ✅ |
| NAV — Compare | `client.nav.compare()` | — | ✅ |
| NAV — All for date | `client.nav.all_navs_for_date()` | — | ✅ |
| NAV — Flat file | `client.nav.download_file()` | ✅ txt | — |
| TER — MF schemes | `client.ter.fetch()` / `download_excel()` | ✅ xlsx | ✅ |
| TER — SIF schemes | `client.sif_ter.fetch()` / `download_excel()` | ✅ xlsx | ✅ |
| Fund Performance | `client.fund_performance.fetch()` | — | — |
| Tracking Error | `client.tracking.error()` | — | ✅ |
| Tracking Difference | `client.tracking.difference()` | — | ✅ |
| Risk Parameters | `client.risk_parameters.fetch()` | — | ✅ |
| NFO | `client.nfo.fetch()` | — | ✅ |
| Publications — Monthly | `client.publications.monthly_flat()` + `download_file()` | ✅ xls | — |
| Publications — Quarterly | `client.publications.quarterly_flat()` + `download_file()` | ✅ xls | — |
| Publications — Commission | `client.publications.commission()` + `download_file()` | ✅ pdf | — |
| CDMDF NAV | `client.cdmdf.history()` | — | ✅ |
| AUM — Average (fund-wise) | `client.aum.average_aum_fundwise()` / `_excel()` | ✅ xlsx | ✅ |
| AUM — Average (scheme-wise) | `client.aum.average_aum_schemewise()` / `_excel()` | ✅ xlsx | ✅ |
| AUM — Disclosure by category | `client.aum.disclosure_by_category()` | ✅ (URL) | ✅ |
| AUM — Disclosure by geography | `client.aum.disclosure_by_geography()` | ✅ (URL) | ✅ |
| AUM — Age-wise / Folio | `client.aum.agewise_folio()` / `_excel()` | ✅ xlsx | ✅ |
| AUM — State-wise classified | `client.aum.statewise()` / `_excel()` | ✅ xlsx | ✅ |
| AUM — Scheme-category-wise | `client.aum.scheme_catwise()` / `_excel()` | ✅ xlsx | ✅ |
| AUM — Bifurcation | `client.aum.bifurcation()` / `_excel()` | ✅ xlsx | ✅ |
| Investor Complaints | `client.other_data.investor_complaints_monthly()` | — | ✅ |
| AMC Directors | `client.other_data.amc_directors()` | — | ✅ |
| Trustees | `client.other_data.trustees()` | — | ✅ |
| Group Companies | `client.other_data.group_companies_all()` | — | ✅ |
| Scheme Dividends | `client.other_data.scheme_dividends()` | — | ✅ |
| Scheme NAV variants | `client.other_data.scheme_data()` | — | ✅ |
| Scheme Profile | `client.other_data.scheme_details()` | — | — |
| Categorisation of Stocks | `client.research.categorisation_of_stocks()` | ✅ xlsx/pdf | ✅ |

> **Full field-level schema** for each dataset → [Data Dictionary](data/index.md)  
> **Full parameter reference** for each method → [API Reference](api/index.md)
