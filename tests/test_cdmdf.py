"""Tests for amfipy.cdmdf — CDMDF NAV."""
import pytest


def test_history(client):
    data = client.cdmdf.history(date="31-mar-2026")
    assert isinstance(data, list)
    assert len(data) > 0


def test_history_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.cdmdf.history(date="31-mar-2026", as_df=True)
    assert isinstance(df, polars.DataFrame)


def test_history_range(client):
    results = client.cdmdf.history_range(dates=["31-mar-2026", "28-feb-2026"])
    assert isinstance(results, dict)
    assert "31-mar-2026" in results
    assert "28-feb-2026" in results


@pytest.mark.asyncio
async def test_async_history(async_client):
    data = await async_client.cdmdf.history(date="31-mar-2026")
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_async_history_range(async_client):
    results = await async_client.cdmdf.history_range(dates=["31-mar-2026", "28-feb-2026"])
    assert len(results) == 2
