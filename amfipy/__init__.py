"""
amfipy — Python client for AMFI India.

Provides sync and async access to:
  - NAV (latest, history, download)
  - TER for MF and SIF schemes
  - Fund Performance
  - Tracking Error and Tracking Difference
  - Risk Parameters
  - New Fund Offers (NFO)
  - AMFI Monthly & Quarterly publications
  - Commission Disclosure
  - CDMDF NAV

Quick start (sync)::

    from amfipy import AMFIClient

    client = AMFIClient()
    nav = client.nav.latest()
    ter = client.ter.download_excel(month="03-2026")

Quick start (async)::

    from amfipy import AsyncAMFIClient
    import asyncio

    async def main():
        client = AsyncAMFIClient()
        nav = await client.nav.latest()

    asyncio.run(main())
"""
from __future__ import annotations

from .ter import TERClient, AsyncTERClient
from .sif_ter import SIFTERClient, AsyncSIFTERClient
from .nav import NAVClient, AsyncNAVClient
from .fund_performance import FundPerformanceClient, AsyncFundPerformanceClient
from .tracking import TrackingClient, AsyncTrackingClient
from .risk_parameters import RiskParametersClient, AsyncRiskParametersClient
from .nfo import NFOClient, AsyncNFOClient
from .publications import PublicationsClient, AsyncPublicationsClient
from .cdmdf import CDMDFClient, AsyncCDMDFClient
from .aum import AUMClient, AsyncAUMClient
from .other_data import OtherDataClient, AsyncOtherDataClient
from .research import ResearchClient, AsyncResearchClient

__version__ = "0.3.0"
__all__ = [
    "AMFIClient",
    "AsyncAMFIClient",
    "TERClient",
    "AsyncTERClient",
    "SIFTERClient",
    "AsyncSIFTERClient",
    "NAVClient",
    "AsyncNAVClient",
    "FundPerformanceClient",
    "AsyncFundPerformanceClient",
    "TrackingClient",
    "AsyncTrackingClient",
    "RiskParametersClient",
    "AsyncRiskParametersClient",
    "NFOClient",
    "AsyncNFOClient",
    "PublicationsClient",
    "AsyncPublicationsClient",
    "CDMDFClient",
    "AsyncCDMDFClient",
    "AUMClient",
    "AsyncAUMClient",
    "OtherDataClient",
    "AsyncOtherDataClient",
    "ResearchClient",
    "AsyncResearchClient",
]


class AMFIClient:
    """Unified sync client — convenience wrapper over all modules.

    All sub-clients share the same httpx kwargs (proxies, verify, etc.).

    Example::

        from amfipy import AMFIClient

        client = AMFIClient()

        # NAV
        latest = client.nav.latest()
        history = client.nav.history(sd_id=154043, from_date="2026-01-01", to_date="2026-03-31")

        # TER
        months = client.ter.months(year="2025-2026")
        excel  = client.ter.download_excel(month="03-2026")

        # Fund Performance
        filters = client.fund_performance.filters()
        perf    = client.fund_performance.fetch(category=1, sub_category=1)

        # Tracking
        error = client.tracking.error(date="31-mar-2026")
        diff  = client.tracking.difference(month="01-Apr-2026")

        # Risk Parameters
        risk = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17)

        # NFO
        nfos = client.nfo.flat()

        # Publications
        monthly = client.publications.monthly_flat()
        xls = client.publications.download_file(monthly[0]["excel_url"])

        # CDMDF
        cdmdf = client.cdmdf.history(date="31-mar-2026")

        # Other data (complaints, directors, group companies, dividends, accounts)
        complaints = client.other_data.investor_complaints_monthly(month="March-2026", mf_id=62)
        directors  = client.other_data.amc_directors(mf_id=62)
        companies  = client.other_data.group_companies_all()
    """

    def __init__(self, **httpx_kwargs):
        self.ter = TERClient(**httpx_kwargs)
        self.sif_ter = SIFTERClient(**httpx_kwargs)
        self.nav = NAVClient(**httpx_kwargs)
        self.fund_performance = FundPerformanceClient(**httpx_kwargs)
        self.tracking = TrackingClient(**httpx_kwargs)
        self.risk_parameters = RiskParametersClient(**httpx_kwargs)
        self.nfo = NFOClient(**httpx_kwargs)
        self.publications = PublicationsClient(**httpx_kwargs)
        self.cdmdf = CDMDFClient(**httpx_kwargs)
        self.aum = AUMClient(**httpx_kwargs)
        self.other_data = OtherDataClient(**httpx_kwargs)
        self.research = ResearchClient(**httpx_kwargs)


class AsyncAMFIClient:
    """Unified async client — convenience wrapper over all modules.

    Example::

        import asyncio
        from amfipy import AsyncAMFIClient

        async def main():
            client = AsyncAMFIClient()
            latest = await client.nav.latest()
            excel  = await client.ter.download_excel(month="03-2026")

        asyncio.run(main())
    """

    def __init__(self, **httpx_kwargs):
        self.ter = AsyncTERClient(**httpx_kwargs)
        self.sif_ter = AsyncSIFTERClient(**httpx_kwargs)
        self.nav = AsyncNAVClient(**httpx_kwargs)
        self.fund_performance = AsyncFundPerformanceClient(**httpx_kwargs)
        self.tracking = AsyncTrackingClient(**httpx_kwargs)
        self.risk_parameters = AsyncRiskParametersClient(**httpx_kwargs)
        self.nfo = AsyncNFOClient(**httpx_kwargs)
        self.publications = AsyncPublicationsClient(**httpx_kwargs)
        self.cdmdf = AsyncCDMDFClient(**httpx_kwargs)
        self.aum = AsyncAUMClient(**httpx_kwargs)
        self.other_data = AsyncOtherDataClient(**httpx_kwargs)
        self.research = AsyncResearchClient(**httpx_kwargs)
