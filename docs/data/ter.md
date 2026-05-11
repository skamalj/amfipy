# TER Data Dictionary

> **API reference — MF:** [`client.ter`](../api/ter.md)  
> **API reference — SIF:** [`client.sif_ter`](../api/sif_ter.md)

Total Expense Ratio data. The MF and SIF interfaces are identical; SIF uses `sif_id` in place of `mf_id`.

---

## `months()` — Available months

| Field | Type | Example | Description |
|---|---|---|---|
| `MonthYear` | `str` | `"March-2026"` | Human-readable month label |
| `MonthNumber` | `str` | `"03-2026"` | Use this value as the `month` parameter in `fetch()` / `download_excel()` |

---

## `fetch()` — TER records

Each row in the returned list (or DataFrame when `as_df=True`) represents one scheme.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `Scheme_Name` | `str` | `"HDFC Flexi Cap Fund - Direct Plan - Growth"` | Full scheme name |
| `SchemeType` | `str` | `"Open Ended"` | Open Ended / Close Ended / Interval Fund |
| `Category` | `str` | `"Equity Scheme"` | SEBI category |
| `Sub_Category` | `str` | `"Flexi Cap Fund"` | SEBI sub-category |
| `ISIN` | `str` | `"INF179K01ZZ4"` | ISIN code |
| `TER` | `str` | `"0.74"` | Total Expense Ratio as a percentage string |
| `TER_addl_exp` | `str` | `"0.00"` | Additional expense (B30 cities allowance) |
| `TER_total` | `str` | `"0.74"` | Total TER including additional expense |
| `Month` | `str` | `"March-2026"` | Month the TER is applicable for |

!!! note "String numbers"
    TER values are returned as strings. Cast to float for calculations: `float(row["TER"])`.

---

## `sub_categories()` — Sub-category lookup

| Field | Type | Example | Description |
|---|---|---|---|
| `id` | `int` | `1` | Sub-category ID (internal) |
| `name` | `str` | `"Flexi Cap Fund"` | Sub-category label |

---

## `download_excel()` — Excel file

Returns a single-sheet `.xlsx` file.  The sheet contains the same columns as `fetch()` above.

```python
data = client.ter.download_excel(month="03-2026")
Path("ter_march_2026.xlsx").write_bytes(data)
```

---

## Parameter reference

| Parameter | Values | Default |
|---|---|---|
| `month` | `"MM-YYYY"` e.g. `"03-2026"` | Latest available |
| `year` | `"YYYY-YYYY"` e.g. `"2025-2026"` | `"2025-2026"` |
| `mf_id` / `sif_id` | `"All"` or numeric ID | `"All"` |
| `category` | `"-1"` All · `"Equity Scheme"` · `"Debt Scheme"` · `"Hybrid Scheme"` · `"Other Scheme"` · `"Solution Oriented Scheme"` | `"-1"` |
| `fund_type` | `"-1"` All · `"Open Ended"` · `"Close Ended"` · `"Interval Fund"` | `"-1"` |
