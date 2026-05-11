# NAV Data Dictionary

> **API reference:** [`client.nav`](../api/nav.md)

---

## `latest()` — Latest NAV

Returns a nested structure grouped by fund type → category → scheme.

**Top-level response**

| Field | Type | Example | Description |
|---|---|---|---|
| `data` | `list` | `[{...}]` | List of fund-type groups |
| `count` | `int` | `42` | Total number of groups |

**Each fund-type group**

| Field | Type | Example | Description |
|---|---|---|---|
| `type` | `str` | `"Open Ended"` | Fund type — Open Ended, Close Ended, Interval Fund |
| `categories` | `list` | `[{...}]` | List of scheme-category blocks |

**Each category block**

| Field | Type | Example | Description |
|---|---|---|---|
| `category` | `str` | `"Equity Scheme"` | SEBI scheme category |
| `nav` | `list` | `[{...}]` | List of scheme NAV records |

**Each scheme NAV record**

| Field | Type | Example | Description |
|---|---|---|---|
| `Scheme_Code` | `str` | `"120503"` | AMFI scheme code |
| `ISIN_Div_Payout` | `str` | `"INF200K01RN2"` | ISIN for dividend payout option |
| `ISIN_Div_Reinvestment` | `str` | `"-"` | ISIN for dividend reinvestment option; `-` if not applicable |
| `Scheme_Name` | `str` | `"Aditya Birla Sun Life Flexi Cap Fund"` | Full scheme name |
| `Net_Asset_Value` | `str` | `"1109.52"` | Latest NAV (string; parse to float for calculations) |
| `Date` | `str` | `"07-May-2026"` | NAV date in DD-Mon-YYYY format |
| `Repurchase_Price` | `str` | `"1109.52"` | Repurchase / redemption price |
| `Sale_Price` | `str` | `"1109.52"` | Sale price |

---

## `history()` — Historical NAV

### Raw response (no `as_df`)

| Field | Type | Example | Description |
|---|---|---|---|
| `mf_name` | `str` | `"Aditya Birla Sun Life Mutual Fund"` | AMC name |
| `scheme_name` | `str` | `"Aditya Birla Sun Life Flexi Cap Fund"` | Scheme name |
| `date_range` | `str` | `"01-Jan-2026 To 31-Mar-2026"` | Human-readable date range |
| `nav_groups` | `list` | `[{...}]` | One group per NAV option (Direct Growth, Regular IDCW, etc.) |

**Each `nav_groups` entry**

| Field | Type | Example | Description |
|---|---|---|---|
| `nav_name` | `str` | `"Aditya Birla Sun Life Flexi Cap Fund - Direct - Growth"` | Full NAV option name |
| `historical_records` | `list` | `[{...}]` | Daily NAV records |

**Each `historical_records` entry**

| Field | Type | Example | Description |
|---|---|---|---|
| `date` | `str` | `"2026-01-02"` | NAV date (YYYY-MM-DD) |
| `nav` | `str` | `"1056.23"` | NAV value (string — parse to float) |
| `repurchase_price` | `str` | `"1056.23"` | Repurchase price |
| `sale_price` | `str` | `"1056.23"` | Sale price |

### Flattened DataFrame (`as_df=True`)

`as_df=True` collapses the nested `nav_groups → historical_records` structure into a single flat table:

| Column | Type | Description |
|---|---|---|
| `mf_name` | `str` | AMC name (repeated for every row) |
| `scheme_name` | `str` | Scheme name (repeated for every row) |
| `nav_name` | `str` | NAV option name |
| `date` | `str` | NAV date (YYYY-MM-DD) |
| `nav` | `str` | NAV value |
| `repurchase_price` | `str` | Repurchase price |
| `sale_price` | `str` | Sale price |

---

## `high_low()` — High / Low NAV

### Raw response

| Field | Type | Example | Description |
|---|---|---|---|
| `mf_name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `scheme_name` | `str` | `"HDFC Flexi Cap Fund"` | Scheme name |
| `date_range` | `str` | `"01-Jan-2026 To 31-Mar-2026"` | Date range queried |
| `nav_type` | `str` | `"Both"` | high / Low / Both |
| `nav_data` | `list` | `[{...}]` | Period-level high/low records |

**Each `nav_data` entry**

| Field | Type | Example | Description |
|---|---|---|---|
| `period` | `str` | `"Jan-2026"` | Month or year label |
| `high_nav` | `str` | `"1150.45"` | Highest NAV in the period |
| `low_nav` | `str` | `"1080.12"` | Lowest NAV in the period |
| `high_date` | `str` | `"2026-01-28"` | Date of highest NAV |
| `low_date` | `str` | `"2026-01-02"` | Date of lowest NAV |

---

## `compare()` — Compare two dates

### Raw response

| Field | Type | Example | Description |
|---|---|---|---|
| `mf_name` | `str` | — | AMC name |
| `scheme_name` | `str` | — | Scheme name |
| `dates` | `dict` | `{"from_date":"2026-01-01","to_date":"2026-03-31"}` | The two dates compared |
| `nav_comparisons` | `list` | `[{...}]` | One entry per NAV option |

**Each `nav_comparisons` entry**

| Field | Type | Example | Description |
|---|---|---|---|
| `nav_name` | `str` | — | NAV option name |
| `nav_date1` | `str` | `"1056.23"` | NAV on the first date |
| `nav_date2` | `str` | `"1109.52"` | NAV on the second date |
| `change` | `str` | `"53.29"` | Absolute change |
| `change_pct` | `str` | `"5.04"` | Percentage change |

---

## `schemes()` — Scheme list for an AMC

Used to look up scheme IDs for `history()` calls.

| Field | Type | Example | Description |
|---|---|---|---|
| `nav_id` | `str` | `"154043"` | Use this as `sd_id` in history calls |
| `nav_name` | `str` | `"Abakkus Flexi Cap Fund - Direct - Growth"` | Full NAV option name |
| `MF_ID` | `str` | `"85"` | AMC ID |

---

## `download_file()` — NAV flat file

Returns raw **bytes** of the classic plain-text NAV file (equivalent to NAVAll.txt). Contains all schemes for a single date, one scheme per line, pipe-delimited:

```
Scheme Code|ISIN Div Payout/ ISIN Growth|ISIN Div Reinvestment|Scheme Name|Net Asset Value|Date
```

Save with `Path("navs.txt").write_bytes(data)` and parse with `str.split("|")` or `polars.read_csv(io.BytesIO(data), separator="|")`.
