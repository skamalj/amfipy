# CDMDF NAV Data Dictionary

> **API reference:** [`client.cdmdf`](../api/cdmdf.md)

The Corporate Debt Market Development Fund (CDMDF) was set up by SEBI as a backstop facility for the debt mutual fund segment.

---

## `history()` — CDMDF NAV records

Each record represents the NAV of one CDMDF plan for the requested date.

| Field | Type | Example | Description |
|---|---|---|---|
| `Scheme_Code` | `str` | `"149001"` | AMFI scheme code |
| `Scheme_Name` | `str` | `"CDMDF - Plan A - Growth"` | CDMDF plan name |
| `ISIN` | `str` | `"INF200X01234"` | ISIN code |
| `Net_Asset_Value` | `str` | `"10.3412"` | NAV as of the requested date |
| `Date` | `str` | `"31-Mar-2026"` | NAV date (DD-Mon-YYYY) |
| `Repurchase_Price` | `str` | `"10.3412"` | Repurchase price |
| `Sale_Price` | `str` | `"10.3412"` | Sale price |

---

## Date format

| Parameter | Format | Example |
|---|---|---|
| `date` | `"DD-mon-YYYY"` — **lowercase** month | `"31-mar-2026"` |

!!! warning "Latest NAV not available"
    The current-day CDMDF NAV is server-rendered on the AMFI page and has no JSON API.
    Only historical date queries (via `history()`) are supported.
