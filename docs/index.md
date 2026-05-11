# amfipy

Python client for **AMFI India** — the Association of Mutual Funds in India.  
Clean, typed access to NAV, TER, AUM, Fund Performance, Tracking Error, Risk Parameters, NFOs, Publications, and more.  Both **sync** and **async** interfaces are included.

| Section | Description |
|---|---|
| 🚀 [**Quick Start**](quickstart.md) | Install the library and go from zero to your first data pull in five minutes |
| 📖 [**User Guide**](userguide.md) | Sync vs async, polars DataFrames, Excel downloads, batch fetching, date formats, AMC IDs, Spark / Iceberg |
| 💻 [**Module Examples**](modules.md) | Copy-paste examples for every module — NAV, TER, AUM, Tracking, Risk, NFO, Publications, and more |
| 🔌 [**API Reference**](api/index.md) | Full parameter reference auto-generated from source docstrings |
| 📋 [**Data Dictionary**](data/index.md) | Field-level schema for every dataset, linked back to the API |

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

> **Excel / file** — `✅` means a method returns raw `bytes`; save with `.write_bytes()`.  
> **`as_df=True`** — requires `pip install amfipy[polars]`. Convert to Spark with `.to_arrow()`.
