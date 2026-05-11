# amfipy

**Python client for AMFI India** — clean, typed access to NAV, TER, AUM, Fund Performance, Tracking Error, Risk Parameters, and more.  Both **sync** and **async** interfaces are included.

## Install

```bash
pip install amfipy            # core (httpx only)
pip install amfipy[polars]    # + polars DataFrame support
```

## Quick start

```python
from amfipy import AMFIClient

client = AMFIClient()

# Latest NAV — all funds
nav = client.nav.latest()

# TER for March 2026 as a polars DataFrame
ter_df = client.ter.fetch(month="03-2026", as_df=True)

# Tracking error for 31-Mar-2026
error_df = client.tracking.error(date="31-mar-2026", as_df=True)
```

## Two ways to use the docs

| Section | What you'll find |
|---|---|
| [**API Reference**](api/index.md) | Every client method — parameters, return types, examples |
| [**Data Dictionary**](data/index.md) | Field-level schema for every dataset returned, linked back to the API |

## Data coverage at a glance

| Module | `as_df=True` | Excel / file |
|---|:---:|:---:|
| [NAV](api/nav.md) | ✅ (history, high/low, compare, all-for-date) | ✅ flat txt file |
| [TER — MF](api/ter.md) | ✅ | ✅ xlsx |
| [TER — SIF](api/sif_ter.md) | ✅ | ✅ xlsx |
| [Fund Performance](api/fund_performance.md) | — | — |
| [Tracking Error / Difference](api/tracking.md) | ✅ | — |
| [Risk Parameters](api/risk_parameters.md) | ✅ | — |
| [NFO](api/nfo.md) | ✅ | — |
| [Publications](api/publications.md) | — | ✅ xls + pdf |
| [CDMDF NAV](api/cdmdf.md) | ✅ | — |
| [AUM](api/aum.md) | ✅ (all sub-modules) | ✅ xlsx (most sub-modules) |
| [Other Data](api/other_data.md) | ✅ (most methods) | — |
| [Research](api/research.md) | ✅ | ✅ xlsx + pdf |

## Polars → Spark

```python
# as_df=True gives a polars DataFrame
df = client.ter.fetch(month="03-2026", as_df=True)

# Convert to Spark via Arrow — no pandas required
spark_df = spark.createDataFrame(df.to_arrow())
spark_df.writeTo("catalog.amfi.ter").createOrReplace()
```
