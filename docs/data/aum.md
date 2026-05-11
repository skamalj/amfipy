# AUM Data Dictionary

> **API reference:** [`client.aum`](../api/aum.md)

Five sub-modules — each section below corresponds to one AMFI AUM page.

---

## 1. Average AUM

### `financial_years()` — Available financial years

| Field | Type | Example | Description |
|---|---|---|---|
| `id` | `int` | `1` | Use as `fy_id` in `periods()` and data calls |
| `financial_year` | `str` | `"April 2025 - March 2026"` | Human-readable label |

### `periods()` — Quarters within a financial year

| Field | Type | Example | Description |
|---|---|---|---|
| `financial_year` | `str` | `"April 2025 - March 2026"` | Financial year label |
| `periods` | `list` | `[{...}]` | List of quarter records |

**Each `periods` entry**

| Field | Type | Example | Description |
|---|---|---|---|
| `id` | `int` | `1` | Use as `period_id` in data calls |
| `period` | `str` | `"January - March 2026"` | Quarter label |

### `average_aum_fundwise()` — Fund-wise Average AUM

One row per AMC.

| Field | Type | Example | Description |
|---|---|---|---|
| `Sr_No` | `str` | `"1"` | Serial number |
| `MutualFundName` | `str` | `"Aditya Birla Sun Life Mutual Fund"` | AMC name |
| `averageAUM` | `dict` | `{"Equity":12345.67,...}` | AUM by scheme category (₹ crore) |

### `average_aum_schemewise()` — Scheme-wise Average AUM

| Field | Type | Example | Description |
|---|---|---|---|
| `Category` | `str` | `"Equity Scheme"` | SEBI scheme category |
| `Sub_Category` | `str` | `"Flexi Cap Fund"` | SEBI sub-category |
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name (when filtered by `mf_id`) |
| `Scheme_Name` | `str` | `"HDFC Flexi Cap Fund - Direct - Growth"` | Scheme name |
| `AAUM` | `str` | `"28456.32"` | Average AUM for the quarter (₹ crore) |

---

## 2. AUM–AAUM Disclosure

### `disclosure_by_category()` / `disclosure_by_geography()` — Quarterly disclosure

Each record provides a quarter's AUM disclosure file links.

| Field | Type | Example | Description |
|---|---|---|---|
| `Period` | `str` | `"October - December 2025"` | Quarter label |
| `pdfURL` | `str` | `"https://..."` | PDF disclosure file URL |
| `excelURL` | `str` | `"https://..."` | Excel disclosure file URL |

Download with `client.publications.download_file(url)` or `httpx.get(url).content`.

---

## 3. Age-wise / Folio Data

### `agewise_folio()` — Flat DataFrame (`as_df=True`)

`as_df=True` flattens the nested `ageWiseAUM → classifications` structure.

| Column | Type | Example | Description |
|---|---|---|---|
| `schemeTypeName` | `str` | `"Open Ended"` | Scheme type (outer grouping) |
| `ageGroup` | `str` | `"18-30"` | Investor age band |
| `noOfFolios` | `str` | `"1234567"` | Number of folios in this age group |
| `AUM` | `str` | `"45678.90"` | AUM for this age group (₹ crore) |

Raw response (`as_df=False`) also contains `investorClassification` — investor type breakdown (Individuals, NRI, HUF, etc.).

---

## 4. Classified Average AUM

### `statewise()` — State-wise AUM

| Field | Type | Example | Description |
|---|---|---|---|
| `State` | `str` | `"Maharashtra"` | State name |
| `B30Cities` | `str` | `"12345.67"` | AUM from Beyond 30 cities (₹ crore) |
| `T30Cities` | `str` | `"98765.43"` | AUM from Top 30 cities (₹ crore) |
| `Total` | `str` | `"111111.10"` | Total AUM for the state (₹ crore) |

### `scheme_catwise()` — Scheme-category-wise AUM

| Field | Type | Example | Description |
|---|---|---|---|
| `Category` | `str` | `"Equity Scheme"` | SEBI scheme category |
| `T30` | `str` | `"456789.12"` | Top 30 cities AUM (₹ crore) |
| `B30` | `str` | `"23456.78"` | Beyond 30 cities AUM (₹ crore) |
| `Total` | `str` | `"480245.90"` | Total AUM (₹ crore) |

**Date format:** `"01-mon-yyyy"` — lowercase month, always day=01. E.g. `"01-apr-2026"`.

---

## 5. Bifurcation of AUM (Direct Plan)

### `bifurcation()` — Direct Plan AUM split

One record per date requested.

| Field | Type | Example | Description |
|---|---|---|---|
| `Month_Date` | `str` | `"31-Mar-2026"` | Month-end date |
| `TotalAAUMunderDirectPlan` | `str` | `"987654.32"` | Total Average AUM under Direct Plans (₹ crore) |
| `AAUMunderRegisteredAdvisers` | `str` | `"456789.10"` | Portion managed via SEBI-registered advisers |
| `AAUMunderPMS` | `str` | `"234567.89"` | Portion managed via Portfolio Management Services |
| `AAUMunderDIYclients` | `str` | `"296297.33"` | Portion invested directly by retail clients (DIY) |
