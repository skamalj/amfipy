# Risk Parameters Data Dictionary

> **API reference:** [`client.risk_parameters`](../api/risk_parameters.md)

---

## `fetch()` — Risk parameter records

Each record represents one scheme's monthly risk metrics for the requested category.

| Field | Type | Example | Description |
|---|---|---|---|
| `MF_Name` | `str` | `"HDFC Mutual Fund"` | AMC name |
| `Scheme_Name` | `str` | `"HDFC Mid-Cap Opportunities Fund - Growth"` | Scheme name |
| `Scheme_Code` | `str` | `"118989"` | AMFI scheme code |
| `ISIN` | `str` | `"INF179K01VQ0"` | ISIN code |
| `Standard_Deviation` | `str` | `"14.23"` | Annualised standard deviation of returns (%) |
| `Beta` | `str` | `"0.92"` | Beta vs benchmark — sensitivity to market movements |
| `Sharpe_Ratio` | `str` | `"1.35"` | Sharpe ratio (risk-adjusted return; higher = better) |
| `Treynor_Ratio` | `str` | `"21.05"` | Treynor ratio (return per unit of systematic risk) |
| `Jensens_Alpha` | `str` | `"2.10"` | Jensen's alpha — excess return vs CAPM prediction (%) |
| `Report_Date` | `str` | `"01-Mar-2026"` | First day of the reporting month |

!!! note "Category IDs"
    The `category_id` parameter is numeric and not fully documented by AMFI.
    Known value: `17` = Mid Cap Fund.
    Enumerate empirically or inspect the AMFI risk-parameters page source to find other IDs.

---

## Parameter reference

| Parameter | Values | Description |
|---|---|---|
| `date` | `"01-Mon-YYYY"` — always day=01 | e.g. `"01-Mar-2026"` |
| `category_id` | numeric (e.g. `17`) | SEBI scheme category numeric ID |
