# User Guide

## Sync vs Async

amfipy ships two client classes with identical APIs:

| | Sync | Async |
|---|---|---|
| Class | `AMFIClient` | `AsyncAMFIClient` |
| Import | `from amfipy import AMFIClient` | `from amfipy import AsyncAMFIClient` |
| Call style | `client.nav.latest()` | `await client.nav.latest()` |
| Best for | Scripts, notebooks, one-off pulls | Web servers, concurrent fetches, pipelines |

Both expose the same sub-modules (`nav`, `ter`, `tracking`, `aum`, …) with identical method signatures — only the `await` keyword differs.

```python
# Sync
from amfipy import AMFIClient
client = AMFIClient()
df = client.ter.fetch(month="03-2026", as_df=True)

# Async — identical call, just awaited
from amfipy import AsyncAMFIClient
import asyncio

async def main():
    client = AsyncAMFIClient()
    df = await client.ter.fetch(month="03-2026", as_df=True)

asyncio.run(main())
```

---

## `as_df=True` — Polars DataFrames

Any method with an `as_df` parameter can return a **polars DataFrame** instead of raw Python objects.
The default always returns plain lists / dicts — `as_df=True` is opt-in.

```python
# Default — plain Python list of dicts
records = client.ter.fetch(month="03-2026")
# → [{"MF_Name": "HDFC...", "TER": "0.74", ...}, ...]

# With as_df=True — polars DataFrame
import polars as pl
df = client.ter.fetch(month="03-2026", as_df=True)
print(df.shape)   # (5423, 10)
print(df.filter(pl.col("Category") == "Equity Scheme"))
```

### Nested structures are flattened automatically

Some APIs return nested data.  `as_df=True` always delivers a flat table — you never need to loop through inner lists.

```python
# Raw — nested: nav_groups → historical_records
raw = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")
# raw["nav_groups"][0]["historical_records"][0]
# → {"date": "2026-01-02", "nav": "1056.23", ...}

# as_df=True — flat DataFrame, ready to use
df = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True)
# columns: mf_name, scheme_name, nav_name, date, nav, repurchase_price, sale_price
```

The same applies to `aum.agewise_folio()` (flattens `ageWiseAUM → classifications`)
and `nfo.fetch()` (flattens `NewFundOffer → items`).

### Polars → Spark via Arrow

Convert any polars DataFrame to a Spark DataFrame with a single call — zero-copy, no pandas:

```python
spark_df = spark.createDataFrame(df.to_arrow())
```

See the [Spark & Iceberg](#polars-apache-spark-and-iceberg) section for a full pipeline example.

---

## Excel & File Downloads

Methods ending in `_excel()`, plus `download_file()` and `download_categorisation_file()`, return raw **bytes**.
Save them directly — no parsing required.

```python
# TER Excel — single-sheet .xlsx
excel = client.ter.download_excel(month="03-2026")
open("ter_march_2026.xlsx", "wb").write(excel)

# AUM bifurcation Excel
excel = client.aum.bifurcation_excel(date="31-Mar-2026")
open("aum_bif.xlsx", "wb").write(excel)

# AMFI monthly report — get URL from metadata first, then download
entries  = client.publications.monthly_flat()
xls_bytes = client.publications.download_file(entries[0]["excel_url"])
open("amfi_monthly.xls", "wb").write(xls_bytes)

# Full NAV flat file — plain-text, pipe-delimited, all schemes for one date
nav_txt = client.nav.download_file(date="31-Mar-2026")
open("navs.txt", "wb").write(nav_txt)
```

!!! note "Publications work differently"
    `client.publications.monthly_flat()` returns metadata (titles + URLs), not file bytes.
    You always need a second call to `download_file(url)` to get the actual content.
    The same applies to `quarterly_flat()`, `commission()`, and `disclosure_by_category()`.

---

## Batch Fetching — `fetch_range()`

Every time-series module has a `fetch_range()` that pulls multiple periods in one call.
The async client runs these concurrently via `asyncio.gather()`.

```python
# TER — multiple months → dict keyed by month
results = client.ter.fetch_range(months=["03-2026", "02-2026", "01-2026"])
# → {"03-2026": [...], "02-2026": [...], "01-2026": [...]}

# NAV history — multiple date ranges for one scheme → list in same order
ranges  = [("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28")]
results = client.nav.fetch_range(sd_id=154043, months=ranges)

# Tracking error — multiple month-end dates
errors = client.tracking.error_range(dates=["31-mar-2026", "28-feb-2026", "31-jan-2026"])

# Tracking difference — multiple months
diffs = client.tracking.difference_range(months=["01-Apr-2026", "01-Mar-2026"])

# Risk parameters — multiple months, same category
risk = client.risk_parameters.fetch_range(
    dates=["01-Mar-2026", "01-Feb-2026", "01-Jan-2026"],
    category_id=17,
)

# CDMDF — multiple dates
cdmdf = client.cdmdf.history_range(dates=["31-mar-2026", "28-feb-2026"])

# AUM bifurcation — multiple month-ends
bifs = client.aum.bifurcation_range(dates=["31-Mar-2026", "28-Feb-2026", "31-Jan-2026"])
```

---

## Custom HTTP Settings

All clients accept any `httpx` keyword arguments forwarded to the underlying `httpx.Client` / `httpx.AsyncClient`:

```python
from amfipy import AMFIClient

client = AMFIClient(
    proxies={"https://": "http://myproxy:8080"},
    verify=False,   # disable SSL verification (e.g. corporate proxy with custom cert)
    timeout=120,    # seconds — default is 30
)
```

---

## Date Format Reference

AMFI uses several date formats across endpoints — get these wrong and you'll get a 404 or empty response.

| Module / method | Parameter | Format | Example |
|---|---|---|---|
| `nav.history`, `nav.all_navs_for_date` | `from_date`, `to_date`, `date` | `YYYY-MM-DD` | `"2026-03-31"` |
| `nav.download_file` | `date` | `DD-Mon-YYYY` | `"31-Mar-2026"` |
| `tracking.error`, `cdmdf.history` | `date` | `DD-mon-YYYY` **lowercase** month | `"31-mar-2026"` |
| `tracking.difference` | `month` | `DD-Mon-YYYY` title-case, **always day=01** | `"01-Apr-2026"` |
| `risk_parameters.fetch` | `date` | `DD-Mon-YYYY` title-case, **always day=01** | `"01-Mar-2026"` |
| `ter.fetch`, `ter.download_excel` | `month` | `MM-YYYY` | `"03-2026"` |
| `aum.agewise_folio` | `month` | `MonthName-YYYY` | `"March-2026"` |
| `aum.statewise`, `aum.scheme_catwise` | `date` | `DD-mon-yyyy` **lowercase**, always day=01 | `"01-apr-2026"` |
| `aum.bifurcation` | `date` | `DD-Mon-YYYY` | `"31-Mar-2026"` |
| `other_data.investor_complaints_monthly` | `month` | `MonthName-YYYY` | `"March-2026"` |

---

## Financial Year Format

AMFI financial years run **April – March**.

```python
# Full format — used by ter.months(), aum.financial_years(), etc.
months = client.ter.months(year="2025-2026")
# → [{"MonthYear": "March-2026", "MonthNumber": "03-2026"}, ...]
# First item is always the most recent available month.

# Shortened format — used by aum.disclosure_by_category/geography()
disc = client.aum.disclosure_by_category(fy_id="2025-26")

# Yearly complaints — "YYYY-YYYY"
yearly = client.other_data.investor_complaints_yearly(year="2019-2020")
```

---

## AMC IDs

Numeric AMC IDs are used across NAV, TER, AUM, and Other Data endpoints.

| ID | AMC |
|---|---|
| `0` / `"all"` / `"All"` | All AMCs (exact value varies by endpoint) |
| `3` | Aditya Birla Sun Life Mutual Fund |
| `53` | Axis Mutual Fund |
| `62` | 360 ONE Mutual Fund |
| `85` | Abakkus Mutual Fund |

Get the full list programmatically:

```python
filters  = client.fund_performance.filters()
amc_list = filters["mutualFundList"]
# → [{"id": 3, "name": "Aditya Birla Sun Life Mutual Fund"}, ...]
```

---

## Polars, Apache Spark, and Iceberg

`as_df=True` returns a polars DataFrame.  Convert it to a Spark DataFrame via Arrow — **zero-copy, no pandas required**.

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

# The pattern — works for any method that supports as_df=True
#   polars DataFrame  →  PyArrow Table  →  Spark DataFrame
nav_pl = client.nav.history(
    sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True
)
spark.createDataFrame(nav_pl.to_arrow()).writeTo("local.amfi.nav_history").createOrReplace()

ter_pl = client.ter.fetch(month="03-2026", as_df=True)
spark.createDataFrame(ter_pl.to_arrow()).writeTo("local.amfi.ter").createOrReplace()

tracking_pl = client.tracking.error(date="31-mar-2026", as_df=True)
spark.createDataFrame(tracking_pl.to_arrow()).writeTo("local.amfi.tracking_error").createOrReplace()

# Incremental append — loop over dates
for date in ["31-Mar-2026", "28-Feb-2026", "31-Jan-2026"]:
    bif_pl = client.aum.bifurcation(date=date, as_df=True)
    spark.createDataFrame(bif_pl.to_arrow()).writeTo("local.amfi.aum_bifurcation").append()

# Query
spark.sql("SELECT scheme_name, date, nav FROM local.amfi.nav_history ORDER BY date DESC").show()
```

**Production tips:**

- Replace `hadoop` catalog with Hive metastore or AWS Glue for multi-cluster access
- Add a `partition_date` column and partition Iceberg tables by it for fast time-range queries
- Use `.append()` for daily incremental loads; `.createOrReplace()` for full refreshes
- For the full NAV flat file, write `client.nav.download_file()` bytes to S3/HDFS and read with `spark.read.text()`
