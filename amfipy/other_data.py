"""
amfipy.other_data — Miscellaneous AMFI "Other Data" endpoints.

Endpoints (base: https://www.amfiindia.com):
  GET /api/investor-complaints-monthly
      monthly: Part=1-4, Month=March-2026, MF_id=<id>
      yearly:  reportOption=2, MF_id=<id>, Year=<YYYY>

  GET /api/combined-amc-directors?MF_ID=<id>
  GET /api/combined-trustees?MF_ID=<id>

  GET /api/list-of-all-group-companies?page=<n>&size=<n>
      599 total records, page-based (10 per page → 60 pages)

  GET /api/populate-scheme?MF_ID=<id>
      Returns scheme list; use scheme's id as strSDid in scheme-dividend

  GET /api/scheme-dividend?MF_ID=<id>&strSDid=<scheme_id>&strYear=<YYYY>

  GET /api/scheme-data?strMFId=<id>&strSDId=<scheme_id>&strOption=NAV
      NAV details (ISIN, price, date) for all nav options of a scheme.

  GET /api/scheme-details?MF_ID=<id>&scheme_id=<scheme_id>
      Full scheme profile: objective, type, category, load, min amount, website.

  GET /api/accounts-annual?MF_ID=<id>
  GET /api/accounts-half-yearly?MF_ID=<id>
      Both return external URL references, not raw account data.

Investor complaints Part values:
  1 = Part A, 2 = Part B, 3 = Part C, 4 = Part D

Month format for investor-complaints: "March-2026" (MonthName-YYYY)
"""
from __future__ import annotations

from typing import Any

from ._client import make_client, make_async_client
from ._utils import maybe_polars

_REFERER_COMPLAINTS = "otherdata/investor-complaints"
_REFERER_DIRECTORS  = "otherdata/combined-amc-directors"
_REFERER_TRUSTEES   = "otherdata/combined-trustees"
_REFERER_GROUPS     = "otherdata/list-of-all-group-companies"
_REFERER_DIVIDEND   = "otherdata/scheme-wise-dividend-history"
_REFERER_ACCOUNTS   = "otherdata/accounts"

_COMPLAINTS_PATH    = "/api/investor-complaints-monthly"
_DIRECTORS_PATH     = "/api/combined-amc-directors"
_TRUSTEES_PATH      = "/api/combined-trustees"
_GROUP_COS_PATH     = "/api/list-of-all-group-companies"
_POPULATE_PATH      = "/api/populate-scheme"
_DIVIDEND_PATH      = "/api/scheme-dividend"
_ACCOUNTS_ANN_PATH  = "/api/accounts-annual"
_ACCOUNTS_HALF_PATH = "/api/accounts-half-yearly"
_SCHEME_DATA_PATH   = "/api/scheme-data"
_SCHEME_DETAILS_PATH = "/api/scheme-details"


# ---------------------------------------------------------------------------
# Sync
# ---------------------------------------------------------------------------

class OtherDataClient:
    """Sync client for AMFI miscellaneous / other-data endpoints.

    Covers investor complaints, AMC directors & trustees, group companies,
    scheme dividends, and AMC account disclosures.
    """

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    # -- Investor Complaints ------------------------------------------------

    def investor_complaints_monthly(
        self,
        month: str,
        mf_id: int | str = 0,
        part: int = 1,
        as_df: bool = False,
    ) -> Any:
        """Fetch monthly investor complaints report.

        Args:
            month:  Month in "MonthName-YYYY" format, e.g. "March-2026".
            mf_id:  Fund ID. 0 = All AMCs; use a specific numeric ID for one AMC.
            part:   Report part: 1=Part A, 2=Part B, 3=Part C, 4=Part D.
            as_df:  Return polars DataFrame.

        Returns:
            Complaint statistics for the requested month/part.
        """
        with make_client(_REFERER_COMPLAINTS, **self._kw) as c:
            r = c.get(_COMPLAINTS_PATH, params={
                "Part": str(part),
                "Month": month,
                "MF_id": str(mf_id),
            })
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def investor_complaints_yearly(
        self,
        year: int | str,
        mf_id: int | str = 0,
        as_df: bool = False,
    ) -> Any:
        """Fetch annual investor complaints report.

        Args:
            year:   Financial year string "YYYY-YYYY", e.g. "2019-2020".
                    Note: Only covers historical data up to FY 2021.
            mf_id:  Fund ID. 0 = All AMCs.
            as_df:  Return polars DataFrame.
        """
        with make_client(_REFERER_COMPLAINTS, **self._kw) as c:
            r = c.get(_COMPLAINTS_PATH, params={
                "reportOption": "2",
                "MF_id": str(mf_id),
                "Year": str(year),
            })
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    # -- Directors & Trustees -----------------------------------------------

    def amc_directors(self, mf_id: int | str = 0, as_df: bool = False) -> Any:
        """Fetch combined AMC directors list.

        Args:
            mf_id:  Fund ID. 0 = All AMCs.
            as_df:  Return polars DataFrame.

        Returns:
            List of director records for the specified AMC(s).
        """
        with make_client(_REFERER_DIRECTORS, **self._kw) as c:
            r = c.get(_DIRECTORS_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def trustees(self, mf_id: int | str = 0, as_df: bool = False) -> Any:
        """Fetch combined AMC trustees list.

        Args:
            mf_id:  Fund ID. 0 = All AMCs.
            as_df:  Return polars DataFrame.

        Returns:
            List of trustee records for the specified AMC(s).
        """
        with make_client(_REFERER_TRUSTEES, **self._kw) as c:
            r = c.get(_TRUSTEES_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    # -- Group Companies ----------------------------------------------------

    def group_companies(
        self,
        page: int = 1,
        size: int = 10,
        as_df: bool = False,
    ) -> Any:
        """Fetch one page of the group companies list.

        The full dataset has ~599 records. Default page size is 10
        (60 pages total). Use :meth:`group_companies_all` to fetch everything.

        Args:
            page:   1-based page number.
            size:   Records per page (default 10).
            as_df:  Return polars DataFrame.

        Returns:
            Dict with ``data`` (list of company records) and ``totalCount``.
        """
        with make_client(_REFERER_GROUPS, **self._kw) as c:
            r = c.get(_GROUP_COS_PATH, params={"page": str(page), "size": str(size)})
            r.raise_for_status()
            data = r.json()
        if as_df:
            records = data.get("data", data) if isinstance(data, dict) else data
            if not isinstance(records, list):
                records = [records]
            return maybe_polars(records, as_df)
        return data

    def group_companies_all(self, size: int = 100, as_df: bool = False) -> Any:
        """Fetch the full group companies list (auto-paginate).

        Args:
            size:   Records per request (higher = fewer round-trips).
            as_df:  Return polars DataFrame of all records.

        Returns:
            List of all company records (or polars DataFrame).
        """
        all_records: list[dict] = []
        page = 1
        while True:
            with make_client(_REFERER_GROUPS, **self._kw) as c:
                r = c.get(_GROUP_COS_PATH, params={"page": str(page), "size": str(size)})
                r.raise_for_status()
                data = r.json()
            records = data.get("data", []) if isinstance(data, dict) else data
            if not records:
                break
            all_records.extend(records)
            pagination = data.get("pagination", {}) if isinstance(data, dict) else {}
            total = pagination.get("total", 0)
            if total and len(all_records) >= total:
                break
            page += 1
        return maybe_polars(all_records, as_df)

    # -- Scheme Dividends ---------------------------------------------------

    def populate_schemes(self, mf_id: int | str) -> list[dict]:
        """Fetch the list of schemes for an AMC, for use with :meth:`scheme_dividends`.

        Args:
            mf_id:  Numeric AMC ID (required; no "All" option).

        Returns:
            List of scheme dicts. Use the ``scheme_id`` field as ``sd_id`` in
            :meth:`scheme_dividends`.

        Example::

            schemes = client.other_data.populate_schemes(mf_id=62)
            # → [{"scheme_id": "13771", "scheme_name": "..."}, ...]
        """
        with make_client(_REFERER_DIVIDEND, **self._kw) as c:
            r = c.get(_POPULATE_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        return data if isinstance(data, list) else data.get("data", data)

    def scheme_dividends(
        self,
        mf_id: int | str,
        sd_id: int | str,
        year: int | str,
        as_df: bool = False,
    ) -> Any:
        """Fetch dividend history for a specific scheme.

        You must first call :meth:`populate_schemes` to get the ``sd_id``
        (the ``scheme_id`` field from each scheme entry).

        Args:
            mf_id:  Numeric AMC ID.
            sd_id:  Scheme ID from :meth:`populate_schemes` (the ``scheme_id`` field).
            year:   4-digit financial year end, e.g. 2026 for FY 2025-26.
            as_df:  Return polars DataFrame.

        Example::

            schemes = client.other_data.populate_schemes(mf_id=62)
            divs = client.other_data.scheme_dividends(
                mf_id=62, sd_id=schemes[0]["scheme_id"], year=2026
            )
        """
        with make_client(_REFERER_DIVIDEND, **self._kw) as c:
            r = c.get(_DIVIDEND_PATH, params={
                "MF_ID": str(mf_id),
                "strSDid": str(sd_id),
                "strYear": str(year),
            })
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    # -- Scheme Data & Details ----------------------------------------------

    def scheme_data(
        self,
        mf_id: int | str,
        sd_id: int | str,
        as_df: bool = False,
    ) -> Any:
        """Fetch NAV data for all plan/option variants of a scheme.

        Returns one record per NAV option (Direct Growth, Regular IDCW, etc.)
        with ISIN codes, latest NAV price, repurchase/sales price, and date.

        Args:
            mf_id:  Numeric AMC ID.
            sd_id:  Scheme ID from :meth:`populate_schemes` (``scheme_id`` field).
            as_df:  Return polars DataFrame.

        Example::

            schemes = client.other_data.populate_schemes(mf_id=62)
            nav_rows = client.other_data.scheme_data(
                mf_id=62, sd_id=schemes[0]["scheme_id"]
            )
            # → [{"Scheme_NAV_Name": "...", "ISIN_Div_Payout_ISIN_Growth": "...",
            #     "Net_Asset_Value": "13.32", "Date": "2026-05-08T...", ...}, ...]
        """
        with make_client(_REFERER_DIVIDEND, **self._kw) as c:
            r = c.get(_SCHEME_DATA_PATH, params={
                "strMFId": str(mf_id),
                "strSDId": str(sd_id),
                "strOption": "NAV",
            })
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    def scheme_details(
        self,
        mf_id: int | str,
        sd_id: int | str,
    ) -> dict:
        """Fetch full profile for a specific scheme.

        Returns a single dict with scheme objective, type, category, load
        structure, minimum investment amount, and AMC website.

        Args:
            mf_id:  Numeric AMC ID.
            sd_id:  Scheme ID from :meth:`populate_schemes` (``scheme_id`` field).

        Returns:
            Dict with keys: ``MF_Name``, ``Scheme_Name``, ``Scheme_Objective``,
            ``SchemeType_Desc``, ``SchemeCat_Desc``, ``Launch_Date``,
            ``Scheme_load``, ``Scheme_min_amt``, ``AMC_Website``.

        Example::

            schemes = client.other_data.populate_schemes(mf_id=62)
            info = client.other_data.scheme_details(
                mf_id=62, sd_id=schemes[0]["scheme_id"]
            )
            print(info["Scheme_Objective"])
        """
        with make_client(_REFERER_DIVIDEND, **self._kw) as c:
            r = c.get(_SCHEME_DETAILS_PATH, params={
                "MF_ID": str(mf_id),
                "scheme_id": str(sd_id),
            })
            r.raise_for_status()
            data = r.json()
        records = data.get("data", []) if isinstance(data, dict) else data
        return records[0] if records else {}

    # -- AMC Accounts -------------------------------------------------------

    def accounts_annual(self, mf_id: int | str) -> list[dict]:
        """Fetch annual account disclosure links for an AMC.

        Returns a list of dicts with external URL references (not raw financials).

        Args:
            mf_id:  Numeric AMC ID (required).
        """
        with make_client(_REFERER_ACCOUNTS, **self._kw) as c:
            r = c.get(_ACCOUNTS_ANN_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        return data if isinstance(data, list) else data.get("data", data)

    def accounts_half_yearly(self, mf_id: int | str) -> list[dict]:
        """Fetch half-yearly account disclosure links for an AMC.

        Returns a list of dicts with external URL references (not raw financials).

        Args:
            mf_id:  Numeric AMC ID (required).
        """
        with make_client(_REFERER_ACCOUNTS, **self._kw) as c:
            r = c.get(_ACCOUNTS_HALF_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        return data if isinstance(data, list) else data.get("data", data)


# ---------------------------------------------------------------------------
# Async
# ---------------------------------------------------------------------------

class AsyncOtherDataClient:
    """Async client for AMFI miscellaneous / other-data endpoints."""

    def __init__(self, **httpx_kwargs):
        self._kw = httpx_kwargs

    async def investor_complaints_monthly(
        self,
        month: str,
        mf_id: int | str = 0,
        part: int = 1,
        as_df: bool = False,
    ) -> Any:
        async with make_async_client(_REFERER_COMPLAINTS, **self._kw) as c:
            r = await c.get(_COMPLAINTS_PATH, params={
                "Part": str(part),
                "Month": month,
                "MF_id": str(mf_id),
            })
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def investor_complaints_yearly(
        self,
        year: int | str,
        mf_id: int | str = 0,
        as_df: bool = False,
    ) -> Any:
        async with make_async_client(_REFERER_COMPLAINTS, **self._kw) as c:
            r = await c.get(_COMPLAINTS_PATH, params={
                "reportOption": "2",
                "MF_id": str(mf_id),
                "Year": str(year),
            })
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def amc_directors(self, mf_id: int | str = 0, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER_DIRECTORS, **self._kw) as c:
            r = await c.get(_DIRECTORS_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def trustees(self, mf_id: int | str = 0, as_df: bool = False) -> Any:
        async with make_async_client(_REFERER_TRUSTEES, **self._kw) as c:
            r = await c.get(_TRUSTEES_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def group_companies(
        self, page: int = 1, size: int = 10, as_df: bool = False
    ) -> Any:
        async with make_async_client(_REFERER_GROUPS, **self._kw) as c:
            r = await c.get(_GROUP_COS_PATH, params={"page": str(page), "size": str(size)})
            r.raise_for_status()
            data = r.json()
        if as_df:
            records = data.get("data", data) if isinstance(data, dict) else data
            if not isinstance(records, list):
                records = [records]
            return maybe_polars(records, as_df)
        return data

    async def group_companies_all(self, size: int = 100, as_df: bool = False) -> Any:
        import asyncio

        async def _fetch(page: int):
            async with make_async_client(_REFERER_GROUPS, **self._kw) as c:
                r = await c.get(_GROUP_COS_PATH, params={"page": str(page), "size": str(size)})
                r.raise_for_status()
                return r.json()

        first = await _fetch(1)
        pagination = first.get("pagination", {}) if isinstance(first, dict) else {}
        page_count = pagination.get("pageCount", 1)
        records = list(first.get("data", []) if isinstance(first, dict) else first)

        if page_count > 1:
            rest = await asyncio.gather(*[_fetch(p) for p in range(2, page_count + 1)])
            for page_data in rest:
                batch = page_data.get("data", []) if isinstance(page_data, dict) else page_data
                records.extend(batch)

        return maybe_polars(records, as_df)

    async def populate_schemes(self, mf_id: int | str) -> list[dict]:
        async with make_async_client(_REFERER_DIVIDEND, **self._kw) as c:
            r = await c.get(_POPULATE_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        return data if isinstance(data, list) else data.get("data", data)

    async def scheme_dividends(
        self,
        mf_id: int | str,
        sd_id: int | str,
        year: int | str,
        as_df: bool = False,
    ) -> Any:
        async with make_async_client(_REFERER_DIVIDEND, **self._kw) as c:
            r = await c.get(_DIVIDEND_PATH, params={
                "MF_ID": str(mf_id),
                "strSDid": str(sd_id),
                "strYear": str(year),
            })
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def scheme_data(
        self,
        mf_id: int | str,
        sd_id: int | str,
        as_df: bool = False,
    ) -> Any:
        async with make_async_client(_REFERER_DIVIDEND, **self._kw) as c:
            r = await c.get(_SCHEME_DATA_PATH, params={
                "strMFId": str(mf_id),
                "strSDId": str(sd_id),
                "strOption": "NAV",
            })
            r.raise_for_status()
            data = r.json()
        records = data if isinstance(data, list) else data.get("data", data)
        if not isinstance(records, list):
            records = [records]
        return maybe_polars(records, as_df)

    async def scheme_details(self, mf_id: int | str, sd_id: int | str) -> dict:
        async with make_async_client(_REFERER_DIVIDEND, **self._kw) as c:
            r = await c.get(_SCHEME_DETAILS_PATH, params={
                "MF_ID": str(mf_id),
                "scheme_id": str(sd_id),
            })
            r.raise_for_status()
            data = r.json()
        records = data.get("data", []) if isinstance(data, dict) else data
        return records[0] if records else {}

    async def accounts_annual(self, mf_id: int | str) -> list[dict]:
        async with make_async_client(_REFERER_ACCOUNTS, **self._kw) as c:
            r = await c.get(_ACCOUNTS_ANN_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        return data if isinstance(data, list) else data.get("data", data)

    async def accounts_half_yearly(self, mf_id: int | str) -> list[dict]:
        async with make_async_client(_REFERER_ACCOUNTS, **self._kw) as c:
            r = await c.get(_ACCOUNTS_HALF_PATH, params={"MF_ID": str(mf_id)})
            r.raise_for_status()
            data = r.json()
        return data if isinstance(data, list) else data.get("data", data)
