# Quick Start

## Installation

```bash
pip install amfipy
```

Add polars DataFrame support (needed for `as_df=True`):

```bash
pip install amfipy[polars]
```

---

## Your first data pull

```python
from amfipy import AMFIClient

client = AMFIClient()

# Latest NAV for all funds
nav = client.nav.latest()

# TER for March 2026 as a polars DataFrame
ter_df = client.ter.fetch(month="03-2026", as_df=True)

# Download TER as Excel (raw bytes — save anywhere)
excel_bytes = client.ter.download_excel(month="03-2026")
open("ter_march_2026.xlsx", "wb").write(excel_bytes)

# Historical NAV — auto-flattens nested nav_groups into a flat DataFrame
hist_df = client.nav.history(
    sd_id=154043, from_date="2026-01-01", to_date="2026-03-31", as_df=True
)

# Tracking error
error_df = client.tracking.error(date="31-mar-2026", as_df=True)

# AUM bifurcation (Direct Plan split)
bif_df = client.aum.bifurcation(date="31-Mar-2026", as_df=True)
```

---

## Async

`AsyncAMFIClient` has an identical API — just `await` the calls.  
Use it in web servers or wherever you want concurrent fetches:

```python
import asyncio
from amfipy import AsyncAMFIClient

async def main():
    client = AsyncAMFIClient()

    # Three datasets fetched concurrently
    ter, nav, nfo = await asyncio.gather(
        client.ter.fetch(month="03-2026", as_df=True),
        client.nav.all_navs_for_date(date="2026-03-31"),
        client.nfo.flat(),
    )
    return ter, nav, nfo

asyncio.run(main())
```

---

## What next?

- [User Guide](userguide.md) — how `as_df=True` works, Excel downloads, batch fetching, date formats, Spark integration
- [Module Examples](modules.md) — copy-paste snippets for every module
- [API Reference](api/index.md) — full parameter docs
- [Data Dictionary](data/index.md) — field-level schema for every dataset
