# Tracking Data Dictionary

> **API reference:** [`client.tracking`](../api/tracking.md)

---

## `error()` — Tracking Error

Each record represents one index/ETF scheme's tracking error for the requested month-end date.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `Scheme_Name` | `str` | `"HDFC Nifty 50 ETF"` | Scheme name |
| `Scheme_Code` | `str` | `"120716"` | AMFI scheme code |
| `ISIN` | `str` | `"INF179KB1HO1"` | ISIN code |
| `Benchmark` | `str` | `"Nifty 50 TRI"` | Benchmark index the scheme tracks |
| `Tracking_Error` | `str` | `"0.0342"` | Annualised tracking error (decimal; multiply by 100 for %) |
| `Category` | `str` | `"Other Scheme - ETFs"` | SEBI scheme category |
| `Report_Date` | `str` | `"31-Mar-2026"` | Date of the report |

!!! tip "Benchmark column"
    The `Benchmark` field is the only place amfipy exposes benchmark index names.
    Benchmark Indices as a standalone dataset have no accessible API on the AMFI website.

---

## `difference()` — Tracking Difference

Each record represents one index/ETF scheme's tracking difference for the requested month.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `Scheme_Name` | `str` | `"HDFC Nifty 50 ETF"` | Scheme name |
| `Scheme_Code` | `str` | `"120716"` | AMFI scheme code |
| `ISIN` | `str` | `"INF179KB1HO1"` | ISIN code |
| `Benchmark` | `str` | `"Nifty 50 TRI"` | Benchmark index |
| `Scheme_Returns` | `str` | `"14.52"` | Scheme return for the period (%) |
| `Benchmark_Returns` | `str` | `"14.78"` | Benchmark return for the period (%) |
| `Tracking_Difference` | `str` | `-0.26` | Scheme return minus benchmark return (%) |
| `Report_Month` | `str` | `"01-Apr-2026"` | Report month |

---

## Date format reference

| Method | Parameter | Format | Example |
|---|---|---|---|
| `error()` | `date` | `"DD-mon-YYYY"` — **lowercase** month | `"31-mar-2026"` |
| `difference()` | `month` | `"DD-Mon-YYYY"` — **title-case** month, always day=01 | `"01-Apr-2026"` |
