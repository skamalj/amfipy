"""
amfipy.publications — AMFI Monthly Data, Quarterly Data, and Commission Disclosure.

Endpoints (all GET, base: https://www.amfiindia.com):
  /api/amfi-monthly-data     — list of monthly reports with PDF/XLS URLs
  /api/amfi-quarterly        — list of quarterly issues with PDF/XLS URLs
  /api/commission-disclosure — list of annual commission disclosure PDFs

These APIs return metadata (file URLs), not the file contents themselves.
Use download_file(url) to fetch the actual PDF or XLS bytes.

Static files are hosted at: https://portal.amfiindia.com/spages/
"""
from __future__ import annotations

import httpx

from ._client import make_client, make_async_client

_REFERER_MONTHLY = "research-information/amfi-data"
_REFERER_COMM = "research-information/commission-disclosure"
_MONTHLY_PATH = "/api/amfi-monthly-data"
_QUARTERLY_PATH = "/api/amfi-quarterly"
_COMMISSION_PATH = "/api/commission-disclosure"


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class PublicationsClient:
    """Sync client for AMFI publications (monthly, quarterly, commission disclosure)."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    # -- Monthly ------------------------------------------------------------

    def monthly(self) -> list[dict]:
        """Return all available monthly reports.

        Returns a list of financial-year groups, each containing month entries::

            [
              {
                "Year": "April 2025-March 2026",
                "Pages": [
                  {
                    "Title": "March 2026",
                    "month": "03", "year": "2026",
                    "pdf_url": "https://portal.amfiindia.com/spages/ammar2026repo.pdf",
                    "excel_url": "https://portal.amfiindia.com/spages/ammar2026repo.xls",
                    "financial_year": "April 2025-March 2026"
                  },
                  ...
                ]
              },
              ...
            ]
        """
        with make_client(_REFERER_MONTHLY, **self._kw) as c:
            r = c.get(_MONTHLY_PATH)
            r.raise_for_status()
            data = r.json()
        return data.get("Monthly", data)

    def monthly_flat(self) -> list[dict]:
        """Return a flat list of all monthly report entries (no financial-year grouping)."""
        groups = self.monthly()
        return [page for group in groups for page in group.get("Pages", [])]

    # -- Quarterly ----------------------------------------------------------

    def quarterly(self) -> list[dict]:
        """Return all available quarterly issues.

        Returns a list of financial-year groups, each containing issue entries::

            [
              {
                "financial_year": "April 2025-March 2026",
                "issues": [
                  {
                    "issue_no": "Issue IV",
                    "period": "(Jan - Mar 2026)",
                    "pdf_url": "https://portal.amfiindia.com/spages/aqu-vol25-issueIV.pdf",
                    "excel_url": "https://portal.amfiindia.com/spages/aqu-vol25-issueIV.xls",
                    "financial_year": "..."
                  },
                  ...
                ]
              },
              ...
            ]
        """
        with make_client(_REFERER_MONTHLY, **self._kw) as c:
            r = c.get(_QUARTERLY_PATH)
            r.raise_for_status()
            data = r.json()
        return data.get("Quarterly", data)

    def quarterly_flat(self) -> list[dict]:
        """Return a flat list of all quarterly issue entries."""
        groups = self.quarterly()
        return [issue for group in groups for issue in group.get("issues", [])]

    # -- Commission Disclosure ----------------------------------------------

    def commission(self) -> list[dict]:
        """Return all available annual commission disclosure entries.

        Returns::

            [
              {"Period": "FY 2024 - 2025", "URL": "https://portal.amfiindia.com/spages/ACDVol-2024-2025.pdf"},
              ...
            ]
        """
        with make_client(_REFERER_COMM, **self._kw) as c:
            r = c.get(_COMMISSION_PATH)
            r.raise_for_status()
            data = r.json()
        return data.get("AnnualyCommissionDisclosure", data)

    # -- File download ------------------------------------------------------

    def download_file(self, url: str) -> bytes:
        """Download a publication file (PDF or XLS) by URL.

        Args:
            url: Full URL from pdf_url / excel_url / URL fields in the metadata.

        Returns:
            Raw file bytes.

        Example::

            entries = client.monthly_flat()
            latest = entries[0]
            xls_bytes = client.download_file(latest["excel_url"])
            Path("amfi_monthly.xls").write_bytes(xls_bytes)
        """
        with httpx.Client(timeout=120, follow_redirects=True) as c:
            r = c.get(url)
            r.raise_for_status()
            return r.content


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncPublicationsClient:
    """Async client for AMFI publications."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def monthly(self) -> list[dict]:
        async with make_async_client(_REFERER_MONTHLY, **self._kw) as c:
            r = await c.get(_MONTHLY_PATH)
            r.raise_for_status()
            data = r.json()
        return data.get("Monthly", data)

    async def monthly_flat(self) -> list[dict]:
        groups = await self.monthly()
        return [page for group in groups for page in group.get("Pages", [])]

    async def quarterly(self) -> list[dict]:
        async with make_async_client(_REFERER_MONTHLY, **self._kw) as c:
            r = await c.get(_QUARTERLY_PATH)
            r.raise_for_status()
            data = r.json()
        return data.get("Quarterly", data)

    async def quarterly_flat(self) -> list[dict]:
        groups = await self.quarterly()
        return [issue for group in groups for issue in group.get("issues", [])]

    async def commission(self) -> list[dict]:
        async with make_async_client(_REFERER_COMM, **self._kw) as c:
            r = await c.get(_COMMISSION_PATH)
            r.raise_for_status()
            data = r.json()
        return data.get("AnnualyCommissionDisclosure", data)

    async def download_file(self, url: str) -> bytes:
        async with httpx.AsyncClient(timeout=120, follow_redirects=True) as c:
            r = await c.get(url)
            r.raise_for_status()
            return r.content
