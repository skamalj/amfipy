# amfipy

Python client for **AMFI India** — the Association of Mutual Funds in India.

Provides clean, typed access to NAV data, TER (Total Expense Ratio), Fund Performance, Tracking Error, Risk Parameters, New Fund Offers, AMFI publications, and more. Both **sync** and **async** interfaces are included.

📖 **[Full documentation → skamalj.github.io/amfipy](https://skamalj.github.io/amfipy/)**  
&nbsp;&nbsp;&nbsp;&nbsp;[Quick Start & User Guide](https://skamalj.github.io/amfipy/) · [API Reference](https://skamalj.github.io/amfipy/api/) · [Data Dictionary](https://skamalj.github.io/amfipy/data/)

## Data Coverage

| Data | Client method | Excel / file | `as_df=True` | Notes |
|---|---|:---:|:---:|---|
| **NAV — Latest** | `client.nav.latest()` | — | ✅ | `as_df` flattens nested type → category → scheme |
| **NAV — Latest by category** | `client.nav.latest_by_category()` | — | — | Category-level summary |
| **NAV — All schemes for date** | `client.nav.all_navs_for_date()` | — | ✅ | One row per scheme |
| **NAV — History** | `client.nav.history()` | — | ✅ | `as_df` auto-flattens nested `nav_groups` |
| **NAV — High / Low** | `client.nav.high_low()` | — | ✅ | `period_type`: Month \| Annual |
| **NAV — Compare two dates** | `client.nav.compare()` | — | ✅ | |
| **NAV — Flat file** | `client.nav.download_file()` | ✅ (txt) | — | Full NAVAll.txt for any date; raw bytes |
| **TER — MF schemes** | `client.ter.fetch()` / `download_excel()` | ✅ xlsx | ✅ | Excel = single sheet; JSON = flat list |
| **TER — SIF schemes** | `client.sif_ter.fetch()` / `download_excel()` | ✅ xlsx | ✅ | Same interface as TER; uses `sif_id` |
| **Fund Performance** | `client.fund_performance.fetch()` | — | ✅ | No server-side Excel (client-side only) |
| **Tracking Error** | `client.tracking.error()` | — | ✅ | Includes Benchmark column per scheme |
| **Tracking Difference** | `client.tracking.difference()` | — | ✅ | |
| **Risk Parameters** | `client.risk_parameters.fetch()` | — | ✅ | Std dev, beta, Sharpe; requires `category_id` |
| **NFO** | `client.nfo.fetch()` | — | ✅ | `as_df` flattens AMC-grouped structure |
| **Publications — Monthly** | `client.publications.monthly_flat()` + `download_file(url)` | ✅ xls | — | Returns metadata + URLs; xls has multiple data sheets |
| **Publications — Quarterly** | `client.publications.quarterly_flat()` + `download_file(url)` | ✅ xls | — | Returns metadata + URLs |
| **Publications — Commission** | `client.publications.commission()` + `download_file(url)` | ✅ pdf | — | Annual commission disclosure PDFs |
| **CDMDF NAV** | `client.cdmdf.history()` | — | ✅ | Corporate Debt Market Dev Fund NAV |
| **AUM — Average (fund-wise)** | `client.aum.average_aum_fundwise()` / `_excel()` | ✅ xlsx | ✅ | Quarterly; one row per AMC |
| **AUM — Average (scheme-wise)** | `client.aum.average_aum_schemewise()` / `_excel()` | ✅ xlsx | ✅ | `str_type`: Categorywise \| Typewise |
| **AUM — Disclosure by category** | `client.aum.disclosure_by_category()` | ✅ (URL in data) | ✅ | Quarterly; each record has `pdfURL`/`excelURL` |
| **AUM — Disclosure by geography** | `client.aum.disclosure_by_geography()` | ✅ (URL in data) | ✅ | Quarterly |
| **AUM — Age-wise / Folio** | `client.aum.agewise_folio()` / `_excel()` | ✅ xlsx | ✅ | `as_df` flattens nested scheme-type + age-band rows |
| **AUM — State-wise classified** | `client.aum.statewise()` / `_excel()` | ✅ xlsx | ✅ | |
| **AUM — Scheme-category-wise** | `client.aum.scheme_catwise()` / `_excel()` | ✅ xlsx | ✅ | |
| **AUM — Bifurcation (Direct Plan)** | `client.aum.bifurcation()` / `_excel()` | ✅ xlsx | ✅ | Direct vs adviser vs PMS vs DIY split |
| **Investor Complaints — Monthly** | `client.other_data.investor_complaints_monthly()` | — | ✅ | 4 parts (A–D); fetch each separately |
| **Investor Complaints — Yearly** | `client.other_data.investor_complaints_yearly()` | — | ✅ | Historical data up to FY 2021 |
| **AMC Directors** | `client.other_data.amc_directors()` | — | ✅ | |
| **Trustees** | `client.other_data.trustees()` | — | ✅ | |
| **Group Companies** | `client.other_data.group_companies_all()` | — | ✅ | ~599 records; auto-paginated |
| **Scheme Dividends** | `client.other_data.scheme_dividends()` | — | ✅ | Call `populate_schemes()` first to get `scheme_id` |
| **Scheme NAV variants** | `client.other_data.scheme_data()` | — | ✅ | One row per plan/option (ISIN, price, date) |
| **Scheme Profile** | `client.other_data.scheme_details()` | — | — | Returns single dict: objective, load, min amt, etc. |
| **Categorisation of Stocks** | `client.research.categorisation_of_stocks()` + `download_categorisation_file(url)` | ✅ xlsx + pdf | ✅ | Bi-annual avg market cap data from 2017; `as_df` = flat year/period rows |

> **Excel / file** — `✅` means raw bytes are returned (save with `.write_bytes()`).  
> **`as_df=True`** — requires `pip install amfipy[polars]`. Convert to Spark with `.to_arrow()`.

## Features

- **Sync + Async** — `AMFIClient` and `AsyncAMFIClient` with identical APIs
- **Typed & documented** — full docstrings, type hints throughout
- **Polars support** — optional `as_df=True` returns a polars DataFrame (`pip install amfipy[polars]`)
- **Raw bytes default** — Excel/file downloads return `bytes`; save wherever you want
- **Historical ranges** — `fetch_range()` on every module for batch multi-period pulls
- **No heavy deps** — only `httpx` required

## Installation

```bash
pip install amfipy
```

With polars DataFrame support:

```bash
pip install amfipy[polars]
```

## Quick Start

```python
from amfipy import AMFIClient

client = AMFIClient()

# Latest NAV for all funds
nav = client.nav.latest()

# Latest NAV as a flat DataFrame
nav_df = client.nav.latest(as_df=True)

# TER Excel for March 2026 (all funds)
excel_bytes = client.ter.download_excel(month="03-2026")
open("ter_march_2026.xlsx", "wb").write(excel_bytes)

# Fund performance — Open Ended Equity, all AMCs
perf = client.fund_performance.fetch(category=1, sub_category=1)

# Tracking error for all funds on 31-Mar-2026
error = client.tracking.error(date="31-mar-2026")
```

### Async

```python
import asyncio
from amfipy import AsyncAMFIClient

async def main():
    client = AsyncAMFIClient()
    nav   = await client.nav.latest()
    excel = await client.ter.download_excel(month="03-2026")

asyncio.run(main())
```

---

## Module Reference

### `client.nav` — NAV Data

```python
# Latest NAV — all funds
nav = client.nav.latest()
# → {"data": [{type, categories: [...]}], "count": N}

# Latest NAV — single AMC (62 = 360 ONE Mutual Fund)
nav = client.nav.latest(mf_id=62, fund_type="Open Ended")

# Latest NAV as flat polars DataFrame (one row per scheme)
nav_df = client.nav.latest(as_df=True)

# Category-level summary
cat = client.nav.latest_by_category(mf_id="all")

# Scheme list for an AMC (needed for history calls)
schemes = client.nav.schemes(mf_id=85)
# → [{"nav_id": "154043", "nav_name": "Abakkus Flexi Cap Fund - Direct - Growth", "MF_ID": "85"}, ...]

# All scheme NAVs for a specific date
all_navs = client.nav.all_navs_for_date(date="2026-03-31")

# Historical NAV for a scheme over a period (use nav_id from schemes() as sd_id)
hist = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")
# → {"mf_name": "...", "scheme_name": "...", "date_range": "...", "nav_groups": [...]}
hist_df = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True)
# → polars DataFrame with columns: mf_name, scheme_name, nav_name, date, nav, ...

# High/Low NAV (period_type: "Month"|"Annual", nav_type: "high"|"Low"|"Both")
hl = client.nav.high_low(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")
hl = client.nav.high_low(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", period_type="Annual", nav_type="high")

# Compare NAV on two dates
cmp = client.nav.compare(sd_id=154043, date1="2026-01-01", date2="2026-03-31")

# Download full NAV flat file (all schemes, one date) — returns bytes
nav_file = client.nav.download_file(date="31-Mar-2026")
open("navs.txt", "wb").write(nav_file)

# Batch historical fetch across multiple ranges
ranges = [("2026-01-01","2026-01-31"), ("2026-02-01","2026-02-28")]
results = client.nav.fetch_range(sd_id=154043, months=ranges)
```

**Fund type values:** `""` (all), `"Open Ended"`, `"Close Ended"`, `"Interval Fund"`

---

### `client.ter` — TER for MF Schemes

```python
# List available months for a financial year
months = client.ter.months(year="2025-2026")
# → [{"MonthYear": "March-2026", "MonthNumber": "03-2026"}, ...]

# Fetch TER data as JSON
data = client.ter.fetch(month="03-2026")
data = client.ter.fetch(month="03-2026", mf_id=62, category="Equity Scheme", fund_type="Open Ended")
data = client.ter.fetch(month="03-2026", as_df=True)  # polars DataFrame

# Fetch latest month automatically
data = client.ter.fetch(year="2025-2026")  # picks months()[0]

# Batch fetch across months
results = client.ter.fetch_range(months=["03-2026", "02-2026", "01-2026"])
# → {"03-2026": <data>, "02-2026": <data>, "01-2026": <data>}

# Download Excel (raw bytes)
excel = client.ter.download_excel(month="03-2026")
excel = client.ter.download_excel(month="03-2026", category="Equity Scheme")
open("ter.xlsx", "wb").write(excel)

# Sub-category lookup
subcats = client.ter.sub_categories(fund_type="Open Ended", category="Equity Scheme")
```

**Category values:** `"-1"` (All), `"Equity Scheme"`, `"Debt Scheme"`, `"Hybrid Scheme"`, `"Other Scheme"`, `"Solution Oriented Scheme"`  
**Fund type values:** `"-1"` (All), `"Open Ended"`, `"Close Ended"`, `"Interval Fund"`

---

### `client.sif_ter` — TER for SIF Schemes

Same interface as `ter`, but uses SIF endpoints and `sif_id` instead of `mf_id`:

```python
months = client.sif_ter.months(year="2025-2026")
data   = client.sif_ter.fetch(month="03-2026", sif_id="All")
excel  = client.sif_ter.download_excel(month="03-2026")
```

---

### `client.fund_performance` — Fund Performance

```python
# Get all filter options (maturity types, categories, fund list)
filters = client.fund_performance.filters()
# → {"maturityTypeList": [...], "investmentTypeList": [...], "mutualFundList": [...]}

# Get sub-categories for Equity (category=1)
subcats = client.fund_performance.sub_categories(category=1)

# Fetch performance data
perf = client.fund_performance.fetch(
    maturity_type=1,   # 1=Open Ended, 2=Close Ended
    category=1,        # 1=Equity, 2=Debt, 3=Hybrid, 4=Solution Oriented, 5=Other
    sub_category=1,    # from sub_categories()
    mf_id=0,           # 0=All, or fund ID from filters()["mutualFundList"]
    report_date="07-May-2026",  # "DD-Mon-YYYY", defaults to last business day
)

# As polars DataFrame
perf_df = client.fund_performance.fetch(category=1, sub_category=1, as_df=True)
```

**Note:** Excel export is client-side only in the AMFI website; no server download endpoint exists.

---

### `client.tracking` — Tracking Error & Difference

```python
# Tracking Error — date format: "DD-mon-YYYY" (lowercase month)
error = client.tracking.error(date="31-mar-2026")
error = client.tracking.error(date="31-mar-2026", mf_id=62)
error = client.tracking.error(date="31-mar-2026", as_df=True)

# Batch tracking error
errors = client.tracking.error_range(dates=["31-mar-2026", "28-feb-2026"])

# Tracking Difference — date format: "01-Mon-YYYY" (title-case month, always day=01)
diff = client.tracking.difference(month="01-Apr-2026")
diff = client.tracking.difference(month="01-Apr-2026", mf_id="all")

# Batch tracking difference
diffs = client.tracking.difference_range(months=["01-Apr-2026", "01-Mar-2026"])
```

---

### `client.risk_parameters` — Risk Parameters

```python
# date format: "01-Mon-YYYY" (always day=01)
# category_id: numeric (e.g. 17 = Mid Cap Fund)
risk = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17)
risk = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17, as_df=True)

# Batch
results = client.risk_parameters.fetch_range(
    dates=["01-Mar-2026", "01-Feb-2026"],
    category_id=17,
)
```

---

### `client.nfo` — New Fund Offers

```python
# Grouped by AMC
nfos = client.nfo.fetch()
# → {"NewFundOffer": [{"MutualFund": "...", "items": [{Scheme_Id, SchemeName, MF_Id}]}], "type": "summary"}

# Flat list
items = client.nfo.flat()
# → [{"Scheme_Id": 14475, "MutualFund": "...", "SchemeName": "...", "MF_Id": 53}, ...]

# As polars DataFrame
df = client.nfo.fetch(as_df=True)
```

---

### `client.publications` — AMFI Monthly, Quarterly & Commission Disclosure

```python
# Monthly reports — grouped by financial year
monthly = client.publications.monthly()

# Flat list of all monthly entries
flat = client.publications.monthly_flat()
# → [{"Title": "March 2026", "month": "03", "year": "2026",
#     "pdf_url": "...", "excel_url": "...", "financial_year": "..."}, ...]

# Quarterly issues — grouped by financial year
quarterly = client.publications.quarterly()
flat_q = client.publications.quarterly_flat()
# → [{"issue_no": "Issue IV", "period": "(Jan - Mar 2026)", "pdf_url": "...", "excel_url": "..."}, ...]

# Commission disclosure — annual PDF list
commission = client.publications.commission()
# → [{"Period": "FY 2024 - 2025", "URL": "https://portal.amfiindia.com/spages/ACDVol-2024-2025.pdf"}, ...]

# Download any file (PDF or XLS) — returns bytes
xls_bytes = client.publications.download_file(flat[0]["excel_url"])
pdf_bytes = client.publications.download_file(commission[0]["URL"])
open("report.xls", "wb").write(xls_bytes)
```

---

### `client.cdmdf` — CDMDF NAV

```python
# Historical CDMDF NAV — date format: "DD-mon-YYYY" (lowercase month)
cdmdf = client.cdmdf.history(date="31-mar-2026")
cdmdf = client.cdmdf.history(date="31-mar-2026", as_df=True)

# Batch
results = client.cdmdf.history_range(dates=["31-mar-2026", "28-feb-2026"])
```

**Note:** Latest CDMDF NAV is server-rendered on the AMFI page — no JSON API exists for it.

---

### `client.aum` — AUM (Assets Under Management)

Five sub-sections covering all AMFI AUM pages.

```python
# ── Average AUM ──────────────────────────────────────────────────────────────

# List financial years (returns id + financial_year label)
fys = client.aum.financial_years()
# → [{"id": 1, "financial_year": "April 2025 - March 2026"}, ...]

# List quarters within a financial year
periods = client.aum.periods(fy_id=1)
# → {"financial_year": "...", "periods": [{"id": 1, "period": "January - March 2026"}, ...]}

# Fund-wise Average AUM for a quarter
data = client.aum.average_aum_fundwise(fy_id=1, period_id=1)
# → [{"Sr_No": "1", "MutualFundName": "...", "averageAUM": {...}}, ...]

# Scheme-wise Average AUM (str_type: "Categorywise" | "Typewise", mf_id: 0=All)
data = client.aum.average_aum_schemewise(fy_id=1, period_id=1, str_type="Categorywise", mf_id=62)

# Excel downloads (raw bytes)
excel = client.aum.average_aum_fundwise_excel(fy_id=1, period_id=1)
excel = client.aum.average_aum_schemewise_excel(fy_id=1, period_id=1, str_type="Typewise")

# ── AUM–AAUM Disclosure ──────────────────────────────────────────────────────

# Quarterly disclosure by fund category — fyId format: "2025-26", "2024-25"
disc_cat  = client.aum.disclosure_by_category(fy_id="2024-25")
# → [{"Period": "(Oct - Dec 2024)", "pdfURL": "...", "excelURL": "..."}, ...]

disc_geo  = client.aum.disclosure_by_geography(fy_id="2024-25")

# ── Age-wise / Folio Data ────────────────────────────────────────────────────

# Month format: "March-2026" (MonthName-YYYY)
af = client.aum.agewise_folio(month="March-2026")
# → {"data": {"investorClassification": [...], "ageWiseAUM": [...]}, "Month": "March-2026"}

af_df = client.aum.agewise_folio(month="March-2026", as_df=True)  # flattens ageWiseAUM
excel  = client.aum.agewise_folio_excel(month="March-2026")

# ── Classified Average AUM ───────────────────────────────────────────────────

# Date format: "01-mon-yyyy" (lowercase month, always day=01)
# e.g. "01-apr-2026", "01-mar-2026"

# List available months
dates = client.aum.classified_dates()
# → [{"date": "April-2026"}, {"date": "March-2026"}, ...]

# State-wise (mf_id: 0=All)
sw    = client.aum.statewise(date="01-apr-2026", mf_id=0)
# → [{"State": "Andaman and Nicobar Islands", "LiquidSchemes": 0.86, ...}, ...]

# Scheme-category-wise
sc    = client.aum.scheme_catwise(date="01-apr-2026", mf_id=0)

# Excel
excel = client.aum.statewise_excel(date="01-apr-2026")
excel = client.aum.scheme_catwise_excel(date="01-apr-2026")

# ── Bifurcation of AAUM ──────────────────────────────────────────────────────

# Date format: "DD-Mon-YYYY" e.g. "31-Mar-2026"
bif   = client.aum.bifurcation(date="31-Mar-2026")
# → [{"Month_Date": "31-Mar-2026", "TotalAAUMunderDirectPlan": 3904766.42,
#     "AAUMunderRegisteredAdvisers": 537599.97, "AAUMunderPMS": 89942.62,
#     "AAUMunderDIYclients": 3277223.84}]

# Batch
results = client.aum.bifurcation_range(dates=["31-Mar-2026", "28-Feb-2026"])

# Excel
excel = client.aum.bifurcation_excel(date="31-Mar-2026")
```

---

## Common Patterns

### Polars DataFrames

Any method with `as_df=True` returns a `polars.DataFrame`. Requires `pip install amfipy[polars]`.

```python
import polars as pl
from amfipy import AMFIClient

client = AMFIClient()
df = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True)
print(df.head())
```

### Async batch fetch

```python
import asyncio
from amfipy import AsyncAMFIClient

async def fetch_all():
    client = AsyncAMFIClient()
    ter, nav, nfo = await asyncio.gather(
        client.ter.download_excel(month="03-2026"),
        client.nav.all_navs_for_date(date="2026-03-31"),
        client.nfo.flat(),
    )
    return ter, nav, nfo

asyncio.run(fetch_all())
```

### Custom httpx settings (proxy, SSL, timeout)

All clients accept `**httpx_kwargs` forwarded to `httpx.Client` / `httpx.AsyncClient`:

```python
from amfipy import AMFIClient

client = AMFIClient(
    proxies={"https://": "http://myproxy:8080"},
    verify=False,
    timeout=120,
)
```

### Using amfipy with Apache Spark and Iceberg

Use `as_df=True` to get a **polars DataFrame** directly from amfipy, then convert
to a Spark DataFrame via Arrow — no pandas, no manual flattening required.

```python
from amfipy import AMFIClient
from pyspark.sql import SparkSession

# ── 1. Spark session with Iceberg catalog ────────────────────────────────────
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

# ── 2. NAV history → Iceberg ─────────────────────────────────────────────────
# as_df=True returns a flat polars DataFrame (no manual nav_groups unwinding needed)
nav_pl = client.nav.history(
    sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True
)
# polars → Arrow → Spark (zero-copy, no pandas)
spark.createDataFrame(nav_pl.to_arrow()).writeTo("local.amfi.nav_history").createOrReplace()

# ── 3. TER data → Iceberg ────────────────────────────────────────────────────
ter_pl = client.ter.fetch(month="03-2026", as_df=True)
spark.createDataFrame(ter_pl.to_arrow()).writeTo("local.amfi.ter_march_2026").createOrReplace()

# ── 4. Tracking error → Iceberg ──────────────────────────────────────────────
tracking_pl = client.tracking.error(date="31-mar-2026", as_df=True)
spark.createDataFrame(tracking_pl.to_arrow()).writeTo("local.amfi.tracking_error").createOrReplace()

# ── 5. AUM bifurcation → Iceberg (append mode) ───────────────────────────────
for date in ["31-Mar-2026", "28-Feb-2026", "31-Jan-2026"]:
    bif_pl = client.aum.bifurcation(date=date, as_df=True)
    spark.createDataFrame(bif_pl.to_arrow()).writeTo("local.amfi.aum_bifurcation").append()

# ── 6. Query the landed data ─────────────────────────────────────────────────
spark.sql("SELECT scheme_name, date, nav FROM local.amfi.nav_history ORDER BY date DESC").show()
spark.sql("SELECT State, LiquidSchemes FROM local.amfi.aum_bifurcation").show()
```

The pattern is always the same: `client.<module>.<method>(as_df=True).to_arrow()` gives
a PyArrow Table that Spark reads natively. Install the polars extra to enable `as_df`:

```bash
pip install amfipy[polars]
```

**Tips for production Iceberg pipelines:**

- Use a Hive metastore or AWS Glue catalog instead of `hadoop` for multi-cluster access.
- Add a `partition_date` column before writing and partition Iceberg tables by it for efficient time-range queries.
- Use `.append()` for incremental daily loads; `.createOrReplace()` for full refreshes.
- For large datasets (all-NAV flat file), fetch `client.nav.download_file()` bytes, write to S3/HDFS, then read with `spark.read.text()`.

---

## Financial Year Reference

AMFI uses financial years in `YYYY-YYYY` format (e.g. `"2025-2026"` = April 2025 – March 2026).

```python
# Available months for the current year
months = client.ter.months(year="2025-2026")
# [{"MonthYear": "March-2026", "MonthNumber": "03-2026"}, ...]
```

## AMC IDs (partial list)

| ID | AMC |
|----|-----|
| 62 | 360 ONE Mutual Fund |
| 85 | Abakkus Mutual Fund |
| 3  | Aditya Birla Sun Life Mutual Fund |
| 0  | All (use `"all"` for NAV, `"All"` for TER) |

Use `client.fund_performance.filters()` to get the full list with IDs.

---

### `client.research` — Categorisation of Stocks

Data published bi-annually (Jan–Jun, Jul–Dec) from 2017 onwards. Served via
the Next.js RSC page — no standalone JSON API exists.

```python
# Dict keyed by year: {year: [{period, pdfUrl, excelUrl}]}
data = client.research.categorisation_of_stocks()
# data["2024"] → [{"period": "Jul - Dec", "pdfUrl": "...", "excelUrl": "..."}, ...]

# Flat list sorted by year
flat = client.research.categorisation_of_stocks_flat()
# → [{"year": "2017", "period": "Jul - Dec", "pdfUrl": "...", "excelUrl": "..."}, ...]

# polars DataFrame (year, period, pdfUrl, excelUrl columns)
df = client.research.categorisation_of_stocks(as_df=True)

# Download a file (PDF or Excel)
pdf = client.research.download_categorisation_file(flat[-1]["pdfUrl"])
open("categ_latest.pdf", "wb").write(pdf)
```

---

### `client.other_data` — Investor Complaints, Directors, Dividends & More

```python
# ── Investor Complaints ──────────────────────────────────────────────────────

# Monthly report (Part 1-4: A, B, C, D)
# month format: "MonthName-YYYY" (e.g. "March-2026")
complaints = client.other_data.investor_complaints_monthly(
    month="March-2026",
    mf_id=62,       # 0 = All AMCs
    part=1,         # 1=Part A, 2=Part B, 3=Part C, 4=Part D
)
complaints_df = client.other_data.investor_complaints_monthly(
    month="March-2026", mf_id=62, part=1, as_df=True
)

# Yearly report — financial year string "YYYY-YYYY", covers up to FY 2021
yearly = client.other_data.investor_complaints_yearly(year="2019-2020", mf_id=62)

# ── AMC Directors & Trustees ─────────────────────────────────────────────────

directors = client.other_data.amc_directors(mf_id=62)   # 0 = All AMCs
trustees  = client.other_data.trustees(mf_id=62)
directors_df = client.other_data.amc_directors(mf_id=0, as_df=True)

# ── Group Companies ──────────────────────────────────────────────────────────

# One page (default size=10)
page = client.other_data.group_companies(page=1, size=10)
# → {"data": [...], "totalCount": 599}

# All records (auto-paginate)
all_cos = client.other_data.group_companies_all()            # list
all_df  = client.other_data.group_companies_all(as_df=True) # polars DataFrame

# ── Scheme Dividends ─────────────────────────────────────────────────────────

# Step 1: get scheme list for an AMC (required to obtain sd_id)
schemes = client.other_data.populate_schemes(mf_id=62)
# → [{"scheme_id": "13771", "scheme_name": "..."}, ...]

# Step 2: fetch dividend history
divs = client.other_data.scheme_dividends(
    mf_id=62,
    sd_id=schemes[0]["scheme_id"],
    year=2026,
)
divs_df = client.other_data.scheme_dividends(
    mf_id=62, sd_id=schemes[0]["scheme_id"], year=2026, as_df=True
)

# ── AMC Account Disclosures ──────────────────────────────────────────────────

# Returns list of dicts with external URL references (not raw financials)
ann_links  = client.other_data.accounts_annual(mf_id=62)
half_links = client.other_data.accounts_half_yearly(mf_id=62)

# ── Scheme Data & Details ─────────────────────────────────────────────────────

# Step 1: get scheme list for an AMC
schemes = client.other_data.populate_schemes(mf_id=62)
sd_id = schemes[0]["scheme_id"]

# NAV details for all plan/option variants (Direct Growth, Regular IDCW, etc.)
nav_rows = client.other_data.scheme_data(mf_id=62, sd_id=sd_id)
# → [{"Scheme_NAV_Name": "...", "ISIN_Div_Payout_ISIN_Growth": "...",
#     "Net_Asset_Value": "13.32", "Date": "2026-05-08T...", ...}, ...]

# Full scheme profile
info = client.other_data.scheme_details(mf_id=62, sd_id=sd_id)
# → {"Scheme_Name": "...", "Scheme_Objective": "...", "SchemeType_Desc": "Open Ended",
#    "SchemeCat_Desc": "Hybrid Scheme - ...", "Scheme_min_amt": 1000,
#    "Launch_Date": "...", "Scheme_load": "...", "AMC_Website": "..."}
```

---

## License

MIT
