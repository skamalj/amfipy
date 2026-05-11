# NFO Data Dictionary

> **API reference:** [`client.nfo`](../api/nfo.md)

---

## `fetch()` — Raw grouped response

**Top-level**

| Field | Type | Example | Description |
|---|---|---|---|
| `NewFundOffer` | `list` | `[{...}]` | One entry per AMC that has open NFOs |
| `type` | `str` | `"summary"` | Always `"summary"` |

**Each `NewFundOffer` entry**

| Field | Type | Example | Description |
|---|---|---|---|
| `MutualFund` | `str` | `"Axis Mutual Fund"` | AMC name |
| `items` | `list` | `[{...}]` | NFO schemes for this AMC |

**Each `items` entry**

| Field | Type | Example | Description |
|---|---|---|---|
| `Scheme_Id` | `int` | `14475` | AMFI scheme ID for this NFO |
| `MutualFund` | `str` | `"Axis Mutual Fund"` | AMC name (repeated from parent) |
| `SchemeName` | `str` | `"Axis Innovation Fund - Direct - Growth"` | NFO scheme name |
| `MF_Id` | `int` | `53` | Numeric AMC ID |

---

## `flat()` / `fetch(as_df=True)` — Flat list

Both `flat()` and `fetch(as_df=True)` return the same fields as the `items` entries above, but without grouping:

| Column | Type | Description |
|---|---|---|
| `Scheme_Id` | `int` | AMFI scheme ID |
| `MutualFund` | `str` | AMC name |
| `SchemeName` | `str` | NFO scheme name |
| `MF_Id` | `int` | Numeric AMC ID |

!!! info "Live data"
    NFO data reflects currently open offers only. The list changes daily as new NFOs open and close.
