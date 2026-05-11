# API Reference

All methods exist on both `AMFIClient` (sync) and `AsyncAMFIClient` (async) with identical signatures — the async versions simply `await` the HTTP calls.

## Client instantiation

```python
from amfipy import AMFIClient, AsyncAMFIClient

# Sync
client = AMFIClient()

# Async
async_client = AsyncAMFIClient()

# Pass any httpx kwargs (proxy, verify, timeout, …)
client = AMFIClient(verify=False, timeout=60)
```

## Modules

| Attribute | Class | Description |
|---|---|---|
| `client.nav` | `NAVClient` | [NAV data](nav.md) — latest, history, download |
| `client.ter` | `TERClient` | [TER for MF schemes](ter.md) |
| `client.sif_ter` | `SIFTERClient` | [TER for SIF schemes](sif_ter.md) |
| `client.fund_performance` | `FundPerformanceClient` | [Fund performance data](fund_performance.md) |
| `client.tracking` | `TrackingClient` | [Tracking error & difference](tracking.md) |
| `client.risk_parameters` | `RiskParametersClient` | [Risk parameters](risk_parameters.md) |
| `client.nfo` | `NFOClient` | [New Fund Offers](nfo.md) |
| `client.publications` | `PublicationsClient` | [Monthly, quarterly & commission publications](publications.md) |
| `client.cdmdf` | `CDMDFClient` | [CDMDF NAV history](cdmdf.md) |
| `client.aum` | `AUMClient` | [AUM — all five sub-modules](aum.md) |
| `client.other_data` | `OtherDataClient` | [Complaints, directors, dividends, scheme details](other_data.md) |
| `client.research` | `ResearchClient` | [Categorisation of stocks](research.md) |
