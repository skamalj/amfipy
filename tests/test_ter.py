"""Tests for amfipy.ter and amfipy.sif_ter."""
import pytest
from conftest import MF_ID


# ── TER ────────────────────────────────────────────────────────────────────────

def test_ter_months(client):
    months = client.ter.months(year="2025-2026")
    assert isinstance(months, list)
    assert len(months) > 0
    assert "MonthNumber" in months[0]


def test_ter_fetch(client):
    data = client.ter.fetch(month="03-2026")
    assert isinstance(data, list) or isinstance(data, dict)


def test_ter_fetch_with_filter(client):
    data = client.ter.fetch(month="03-2026", mf_id=MF_ID, category="Equity Scheme")
    assert data is not None


def test_ter_fetch_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.ter.fetch(month="03-2026", as_df=True)
    assert isinstance(df, polars.DataFrame)


def test_ter_fetch_range(client):
    results = client.ter.fetch_range(months=["03-2026", "02-2026"])
    assert isinstance(results, dict)
    assert "03-2026" in results
    assert "02-2026" in results


def test_ter_download_excel(client):
    data = client.ter.download_excel(month="03-2026")
    assert isinstance(data, bytes)
    assert len(data) > 1000


def test_ter_sub_categories(client):
    cats = client.ter.sub_categories(fund_type="Open Ended", category="Equity Scheme")
    assert isinstance(cats, list)


@pytest.mark.asyncio
async def test_async_ter_months(async_client):
    months = await async_client.ter.months(year="2025-2026")
    assert isinstance(months, list)
    assert len(months) > 0


@pytest.mark.asyncio
async def test_async_ter_download_excel(async_client):
    data = await async_client.ter.download_excel(month="03-2026")
    assert isinstance(data, bytes)
    assert len(data) > 1000


# ── SIF TER ────────────────────────────────────────────────────────────────────

def test_sif_ter_months(client):
    months = client.sif_ter.months(year="2025-2026")
    assert isinstance(months, list)


def test_sif_ter_fetch(client):
    data = client.sif_ter.fetch(month="03-2026")
    assert data is not None


def test_sif_ter_download_excel(client):
    data = client.sif_ter.download_excel(month="03-2026")
    assert isinstance(data, bytes)
