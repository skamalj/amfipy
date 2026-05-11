# Fund Performance Data Dictionary

> **API reference:** [`client.fund_performance`](../api/fund_performance.md)

---

## `filters()` — Filter options

| Field | Type | Description |
|---|---|---|
| `maturityTypeList` | `list` | Available maturity types (Open Ended, Close Ended) |
| `investmentTypeList` | `list` | Category list with IDs |
| `mutualFundList` | `list` | AMC list with IDs — use `id` as `mf_id` in `fetch()` |

**Each `mutualFundList` entry**

| Field | Type | Example | Description |
|---|---|---|---|
| `id` | `int` | `62` | AMC numeric ID |
| `name` | `str` | `"360 ONE Mutual Fund"` | AMC name |

---

## `sub_categories()` — Sub-categories for a category

| Field | Type | Example | Description |
|---|---|---|---|
| `id` | `int` | `1` | Sub-category ID — use as `sub_category` in `fetch()` |
| `name` | `str` | `"Flexi Cap Fund"` | Sub-category label |

---

## `fetch()` — Performance data

Each record represents one scheme's performance metrics.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `Scheme_Name` | `str` | `"HDFC Flexi Cap Fund - Growth"` | Scheme name |
| `Scheme_Code` | `str` | `"100033"` | AMFI scheme code |
| `Category` | `str` | `"Equity Scheme"` | SEBI category |
| `Sub_Category` | `str` | `"Flexi Cap Fund"` | SEBI sub-category |
| `Launch_Date` | `str` | `"01-Jan-1995"` | Scheme launch date |
| `NAV` | `str` | `"1109.52"` | NAV as of report date |
| `Returns_1yr` | `str` | `"12.45"` | 1-year return (%) |
| `Returns_3yr` | `str` | `"18.32"` | 3-year CAGR (%) |
| `Returns_5yr` | `str` | `"22.10"` | 5-year CAGR (%) |
| `Benchmark_Returns_1yr` | `str` | `"11.80"` | Benchmark 1-year return (%) |
| `Benchmark_Returns_3yr` | `str` | `"16.90"` | Benchmark 3-year CAGR (%) |
| `Benchmark_Returns_5yr` | `str` | `"20.50"` | Benchmark 5-year CAGR (%) |
| `Additional_Benchmark_Returns_1yr` | `str` | `"13.10"` | Additional benchmark 1-year return (%) |
| `Report_Date` | `str` | `"07-May-2026"` | Date of the performance report |

---

## Parameter reference

| Parameter | Values | Default |
|---|---|---|
| `maturity_type` | `1` = Open Ended, `2` = Close Ended | `1` |
| `category` | `1`=Equity · `2`=Debt · `3`=Hybrid · `4`=Solution Oriented · `5`=Other | required |
| `sub_category` | Numeric ID from `sub_categories()` | required |
| `mf_id` | `0`=All, or numeric ID from `filters()["mutualFundList"]` | `0` |
| `report_date` | `"DD-Mon-YYYY"` e.g. `"07-May-2026"` | Last business day |
