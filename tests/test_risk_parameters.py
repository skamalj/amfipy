"""Tests for amfipy.risk_parameters."""
import pytest


def test_fetch(client):
    data = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17)
    assert isinstance(data, list)
    assert len(data) > 0


def test_fetch_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.risk_parameters.fetch(date="01-Mar-2026", category_id=17, as_df=True)
    assert isinstance(df, polars.DataFrame)


def test_fetch_range(client):
    results = client.risk_parameters.fetch_range(
        dates=["01-Mar-2026", "01-Feb-2026"],
        category_id=17,
    )
    assert isinstance(results, dict)
    assert "01-Mar-2026" in results
    assert "01-Feb-2026" in results


@pytest.mark.asyncio
async def test_async_fetch(async_client):
    data = await async_client.risk_parameters.fetch(date="01-Mar-2026", category_id=17)
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_async_fetch_range(async_client):
    results = await async_client.risk_parameters.fetch_range(
        dates=["01-Mar-2026", "01-Feb-2026"],
        category_id=17,
    )
    assert len(results) == 2
