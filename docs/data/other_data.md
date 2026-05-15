# Other Data Dictionary

> **API reference:** [`client.other_data`](../api/other_data.md)

---

## Investor Complaints

### `investor_complaints_monthly()` — Monthly complaint statistics

Data is split across 4 parts (A–D); call separately with `part=1` through `part=4`.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `Opening_Balance` | `str` | `"2"` | Complaints carried forward from prior month |
| `Received` | `str` | `"45"` | New complaints received in the month |
| `Resolved` | `str` | `"44"` | Complaints resolved in the month |
| `Pending` | `str` | `"3"` | Complaints pending at month end |
| `Part` | `str` | `"A"` | Report part (A = SEBI SCORES, B = Non-SCORES, C = SEBI ODR, D = Non-SEBI) |
| `Month` | `str` | `"March-2026"` | Reporting month |

**Parts explained**

| Part | `part=` | Coverage |
|---|---|---|
| Part A | `1` | SEBI SCORES platform complaints |
| Part B | `2` | Non-SCORES complaints |
| Part C | `3` | SEBI Online Dispute Resolution (ODR) |
| Part D | `4` | Complaints outside SEBI purview |

### `investor_complaints_yearly()` — Annual complaint statistics

Same field structure as monthly. Historical data only — available up to FY 2020-21.

| Parameter | Format | Example |
|---|---|---|
| `year` | `"YYYY-YYYY"` | `"2019-2020"` |

---

## Directors & Trustees

### `amc_directors()` — AMC board directors

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"Axis Mutual Fund"` | AMC name |
| `AMC_Name` | `str` | `"Axis Asset Management Company Ltd."` | Full AMC legal name |
| `Director_Name` | `str` | `"Rajesh Sharma"` | Director's full name |
| `Director_Type` | `str` | `"Independent"` | Type: Independent / Non-Independent / Nominee |
| `DIN` | `str` | `"00123456"` | Director Identification Number |

### `trustees()` — AMC trustees

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"Axis Mutual Fund"` | AMC name |
| `Trustee_Name` | `str` | `"Priya Menon"` | Trustee's full name |
| `Trustee_Type` | `str` | `"Independent"` | Type: Independent / Associate |
| `DIN` | `str` | `"00654321"` | Director Identification Number |

---

## Group Companies

### `group_companies()` / `group_companies_all()` — Group company list

~599 total records across all AMCs.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `AMC_Name` | `str` | `"HDFC Asset Management Company Ltd."` | Full AMC legal name |
| `Company_Name` | `str` | `"HDFC Bank Limited"` | Name of the group company |
| `Relationship` | `str` | `"Sponsor"` | Relationship with the AMC |

Use `group_companies_all()` to retrieve all 599 records automatically (auto-paginated).

---

## Scheme Dividends

### `populate_schemes()` — Scheme list for an AMC

Call this first to get `scheme_id` values for `scheme_dividends()`.

| Field | Type | Example | Description |
|---|---|---|---|
| `scheme_id` | `str` | `"13771"` | Use as `sd_id` in `scheme_dividends()` |
| `scheme_name` | `str` | `"360 ONE Balanced Hybrid Fund"` | Scheme name |

### `scheme_dividends()` — Dividend history

| Field | Type | Example | Description |
|---|---|---|---|
| `Scheme_Name` | `str` | `"360 ONE Balanced Hybrid Fund - IDCW"` | Full scheme/option name |
| `Record_Date` | `str` | `"28-Feb-2026"` | Dividend record date |
| `Dividend_Per_Unit` | `str` | `"0.50"` | Dividend declared per unit (₹) |
| `Face_Value` | `str` | `"10"` | Face value per unit (₹) |

---

## Scheme Data & Details

### `scheme_data()` — NAV variants for a scheme

One row per plan/option (Direct Growth, Regular IDCW, etc.).

| Field | Type | Example | Description |
|---|---|---|---|
| `Scheme_NAV_Name` | `str` | `"360 ONE Balanced Hybrid Fund-Direct Plan-Growth"` | Full NAV option name |
| `ISIN_Div_Payout_ISIN_Growth` | `str` | `"INF200K01VC5"` | Primary ISIN (growth or dividend payout) |
| `ISIN_Div_Reinvestment` | `str` | `"-"` | Dividend reinvestment ISIN; `-` if not applicable |
| `Net_Asset_Value` | `str` | `"13.32"` | Latest NAV (₹) |
| `Repurchase_Price` | `str` | `""` | Repurchase price (₹); often empty — use `Net_Asset_Value` |
| `Sales_Price` | `str` | `""` | Sale price (₹); often empty — use `Net_Asset_Value` |
| `Date` | `str` | `"2026-05-14T00:00:00.000Z"` | NAV date (ISO 8601 datetime string) |
| `strMFId` | `int` | `62` | AMC ID echoed from request |
| `strSDId` | `int` | `13771` | Scheme ID echoed from request |
| `strOption` | `str` | `"NAV"` | Option echoed from request |

### `scheme_details()` — Full scheme profile

Returns a single `dict` (not a list) with the scheme's static profile.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"360 ONE Mutual Fund"` | AMC name |
| `Scheme_Name` | `str` | `"360 ONE Balanced Hybrid Fund"` | Scheme name |
| `Scheme_Objective` | `str` | `"The scheme seeks to generate..."` | Investment objective (long text) |
| `SchemeType_Desc` | `str` | `"Open Ended"` | Open Ended / Close Ended |
| `SchemeCat_Desc` | `str` | `"Hybrid Scheme - Balanced Hybrid Fund"` | SEBI category — includes sub-category |
| `Launch_Date` | `str` | `"2023-09-04T00:00:00+05:30"` | Scheme launch date (ISO 8601) |
| `Scheme_load` | `str` | `"Entry Load: Not Applicable\nExit Load: ..."` | Load structure (multi-line text) |
| `Scheme_min_amt` | `str` | `"1000"` | Minimum investment amount (₹) |
| `AMC_Website` | `str` | `"https://www.360one.in"` | AMC website URL |
| `scheme_Id` | `int` | `13771` | Scheme ID echoed from request |
| `MF_Id` | `int` | `62` | AMC ID echoed from request |

---

## AMC Accounts

### `accounts_annual()` / `accounts_half_yearly()` — Account disclosure links

Returns URL references — not raw financial statements.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `Period` | `str` | `"FY 2024-25"` | Financial period |
| `URL` | `str` | `"https://..."` | Link to the external account statement (PDF) |
