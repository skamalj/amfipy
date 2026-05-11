# Research Data Dictionary

> **API reference:** [`client.research`](../api/research.md)

---

## `categorisation_of_stocks()` — Avg. Market Capitalisation data

SEBI requires mutual funds to classify stocks into Large Cap / Mid Cap / Small Cap buckets based on average market capitalisation.  AMFI publishes the reference list bi-annually.

### Raw response (`as_df=False`)

Returns a `dict` keyed by year string. Each year contains a list of period entries:

```python
{
  "2024": [
    {"period": "Jul - Dec", "pdfUrl": "https://...", "excelUrl": "https://..."},
    {"period": "Jan - Jun", "pdfUrl": "https://...", "excelUrl": "https://..."},
  ],
  "2023": [...],
  ...
}
```

| Field | Type | Example | Description |
|---|---|---|---|
| year key | `str` | `"2024"` | Calendar year of the publication |
| `period` | `str` | `"Jul - Dec"` | Half-year period covered |
| `pdfUrl` | `str` | `"https://portal.amfiindia.com/..."` | Direct URL to the PDF |
| `excelUrl` | `str` | `"https://portal.amfiindia.com/..."` | Direct URL to the Excel file |

Data is published from **2017** onwards, two periods per year (Jan–Jun and Jul–Dec).

### Flat list (`categorisation_of_stocks_flat()`)

Returns a flat list sorted by year, oldest first:

| Field | Type | Example | Description |
|---|---|---|---|
| `year` | `str` | `"2024"` | Calendar year |
| `period` | `str` | `"Jul - Dec"` | Half-year period |
| `pdfUrl` | `str` | `"https://..."` | PDF download URL |
| `excelUrl` | `str` | `"https://..."` | Excel download URL |

### DataFrame (`as_df=True`)

Same four columns as flat list above, as a polars DataFrame.

---

## `download_categorisation_file(url)` — File bytes

Pass any `pdfUrl` or `excelUrl` to download the file:

```python
flat = client.research.categorisation_of_stocks_flat()
latest = flat[-1]   # most recent period

# Download Excel
excel_bytes = client.research.download_categorisation_file(latest["excelUrl"])
Path("categ_latest.xlsx").write_bytes(excel_bytes)
```

The Excel file contains a ranked list of all NSE-listed companies with their average 6-month market capitalisation, which determines their Large/Mid/Small Cap classification.

**Excel file columns (typical)**

| Column | Description |
|---|---|
| Sr. No. | Serial rank by market cap |
| Company Name | Listed company name |
| ISIN | ISIN code |
| Average Market Cap (₹ Crore) | 6-month average market capitalisation |
| Classification | Large Cap / Mid Cap / Small Cap bucket |
