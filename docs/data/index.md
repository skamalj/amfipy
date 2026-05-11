# Data Dictionary

Field-level reference for every dataset returned by amfipy.  Each page documents the exact fields present in API responses, their types, allowed values, and what they mean.  Every page links back to the API method that produces the data.

## Pages

| Dataset | Source method | `as_df` | Excel |
|---|---|:---:|:---:|
| [NAV Data](nav.md) | [`client.nav.*`](../api/nav.md) | ✅ | ✅ |
| [TER Data](ter.md) | [`client.ter.*` / `client.sif_ter.*`](../api/ter.md) | ✅ | ✅ |
| [Fund Performance](fund_performance.md) | [`client.fund_performance.*`](../api/fund_performance.md) | — | — |
| [Tracking](tracking.md) | [`client.tracking.*`](../api/tracking.md) | ✅ | — |
| [Risk Parameters](risk_parameters.md) | [`client.risk_parameters.*`](../api/risk_parameters.md) | ✅ | — |
| [NFO](nfo.md) | [`client.nfo.*`](../api/nfo.md) | ✅ | — |
| [Publications](publications.md) | [`client.publications.*`](../api/publications.md) | — | ✅ |
| [CDMDF NAV](cdmdf.md) | [`client.cdmdf.*`](../api/cdmdf.md) | ✅ | — |
| [AUM](aum.md) | [`client.aum.*`](../api/aum.md) | ✅ | ✅ |
| [Other Data](other_data.md) | [`client.other_data.*`](../api/other_data.md) | ✅ | — |
| [Research](research.md) | [`client.research.*`](../api/research.md) | ✅ | ✅ |

## Reading the field tables

Each field table uses these columns:

| Column | Meaning |
|---|---|
| **Field** | Exact key name as returned by the API |
| **Type** | Python type (`str`, `int`, `float`, `list`, `dict`) |
| **Example** | Representative value |
| **Description** | What the field contains |

!!! tip "as_df=True flattens nested structures"
    Several APIs return nested lists (e.g. `nav_groups → historical_records`).
    Passing `as_df=True` always returns a **flat** polars DataFrame — the nesting is resolved automatically.
