"""
amfipy.nfo — New Fund Offers (NFO).

Endpoint (GET, base: https://www.amfiindia.com):
  /api/new-fund-offer

Returns currently open NFOs grouped by AMC.

Response structure:
  {
    "NewFundOffer": [
      {
        "MutualFund": "Axis Mutual Fund",
        "items": [
          {"Scheme_Id": 14475, "MutualFund": "...", "SchemeName": "...", "MF_Id": 53}
        ]
      }
    ],
    "type": "summary"
  }
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_REFERER = "new-fund-offer"
_NFO_PATH = "/api/new-fund-offer"


class NFOClient:
    """Sync client for New Fund Offer data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    def fetch(self, as_df: bool = False) -> Any:
        """Fetch currently open NFOs.

        Args:
            as_df: Return a flat polars DataFrame of all NFO items across AMCs.

        Returns:
            When ``as_df=False``: full API response dict with grouped structure.
            When ``as_df=True``: flat polars DataFrame with one row per NFO scheme.
        """
        with make_client(_REFERER, **self._kw) as c:
            r = c.get(_NFO_PATH)
            r.raise_for_status()
            data = r.json()

        if not as_df:
            return data

        # Flatten for DataFrame
        records = []
        for group in data.get("NewFundOffer", []):
            for item in group.get("items", []):
                records.append(item)
        return maybe_polars(records, as_df)

    def flat(self) -> list[dict]:
        """Return a flat list of NFO scheme dicts (no grouping by AMC)."""
        data = self.fetch()
        records = []
        for group in data.get("NewFundOffer", []):
            for item in group.get("items", []):
                records.append(item)
        return records


class AsyncNFOClient:
    """Async client for New Fund Offer data."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def fetch(self, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER, **self._kw) as c:
            r = await c.get(_NFO_PATH)
            r.raise_for_status()
            data = r.json()

        if not as_df:
            return data

        records = []
        for group in data.get("NewFundOffer", []):
            for item in group.get("items", []):
                records.append(item)
        return maybe_polars(records, as_df)

    async def flat(self) -> list[dict]:
        data = await self.fetch()
        records = []
        for group in data.get("NewFundOffer", []):
            for item in group.get("items", []):
                records.append(item)
        return records
