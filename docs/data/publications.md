# Publications Data Dictionary

> **API reference:** [`client.publications`](../api/publications.md)

These methods return **metadata** (titles and download URLs).  Use `download_file(url)` to fetch the actual file bytes.

---

## `monthly()` / `monthly_flat()` — Monthly reports

**`monthly()` — grouped response**

| Field | Type | Example | Description |
|---|---|---|---|
| `Year` | `str` | `"April 2025-March 2026"` | Financial year label |
| `Pages` | `list` | `[{...}]` | Monthly entries for this year |

**Each `Pages` entry** (also what `monthly_flat()` returns directly):

| Field | Type | Example | Description |
|---|---|---|---|
| `Title` | `str` | `"March 2026"` | Display title for this month's report |
| `month` | `str` | `"03"` | Two-digit month number |
| `year` | `str` | `"2026"` | Four-digit year |
| `pdf_url` | `str` | `"https://portal.amfiindia.com/spages/ammar2026repo.pdf"` | Direct URL to the PDF report |
| `excel_url` | `str` | `"https://portal.amfiindia.com/spages/ammar2026repo.xls"` | Direct URL to the XLS report |
| `financial_year` | `str` | `"April 2025-March 2026"` | Parent financial year label |

!!! note "XLS file contents"
    The downloaded `.xls` file is a multi-sheet Excel workbook.  Sheets typically cover fund category-wise AUM, folios, new fund mobilisation, and SIP data for the month.

---

## `quarterly()` / `quarterly_flat()` — Quarterly issues

**`quarterly()` — grouped response**

| Field | Type | Example | Description |
|---|---|---|---|
| `financial_year` | `str` | `"April 2025-March 2026"` | Financial year label |
| `issues` | `list` | `[{...}]` | Quarterly issues for this year |

**Each `issues` entry** (also what `quarterly_flat()` returns directly):

| Field | Type | Example | Description |
|---|---|---|---|
| `issue_no` | `str` | `"Issue IV"` | Issue number within the financial year (I–IV) |
| `period` | `str` | `"(Jan - Mar 2026)"` | Calendar quarter covered |
| `pdf_url` | `str` | `"https://portal.amfiindia.com/spages/aqu-vol25-issueIV.pdf"` | Direct URL to the PDF |
| `excel_url` | `str` | `"https://portal.amfiindia.com/spages/aqu-vol25-issueIV.xls"` | Direct URL to the XLS |
| `financial_year` | `str` | `"April 2025-March 2026"` | Parent financial year label |

---

## `commission()` — Annual commission disclosure

| Field | Type | Example | Description |
|---|---|---|---|
| `Period` | `str` | `"FY 2024 - 2025"` | Financial year of the disclosure |
| `URL` | `str` | `"https://portal.amfiindia.com/spages/ACDVol-2024-2025.pdf"` | Direct URL to the PDF |

---

## `download_file(url)` — File bytes

Pass any `pdf_url`, `excel_url`, or `URL` value from the above metadata to download the file:

```python
entries = client.publications.monthly_flat()
xls_bytes = client.publications.download_file(entries[0]["excel_url"])
Path("amfi_march_2026.xls").write_bytes(xls_bytes)
```

Returns raw `bytes`. Save directly; do not parse as JSON.
