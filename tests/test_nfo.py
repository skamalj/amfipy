"""Tests for amfipy.nfo — New Fund Offers."""
import pytest


def test_fetch(client):
    data = client.nfo.fetch()
    assert isinstance(data, dict) or isinstance(data, list)


def test_flat(client):
    items = client.nfo.flat()
    assert isinstance(items, list)


def test_fetch_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.nfo.fetch(as_df=True)
    assert isinstance(df, polars.DataFrame)


@pytest.mark.asyncio
async def test_async_flat(async_client):
    items = await async_client.nfo.flat()
    assert isinstance(items, list)
