"""Tests for amfipy.research — Categorisation of Stocks."""
import pytest


def test_categorisation_of_stocks(client):
    data = client.research.categorisation_of_stocks()
    assert isinstance(data, dict)
    assert len(data) >= 8  # 2017 onwards
    for yr, items in data.items():
        assert isinstance(yr, str)
        assert isinstance(items, list)
        for item in items:
            assert "period" in item
            assert "pdfUrl" in item
            assert "excelUrl" in item


def test_categorisation_years_present(client):
    data = client.research.categorisation_of_stocks()
    assert "2024" in data
    assert "2023" in data


def test_categorisation_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.research.categorisation_of_stocks(as_df=True)
    assert isinstance(df, polars.DataFrame)
    assert len(df) > 0
    assert "year" in df.columns
    assert "period" in df.columns
    assert "pdfUrl" in df.columns
    assert "excelUrl" in df.columns


def test_categorisation_flat(client):
    flat = client.research.categorisation_of_stocks_flat()
    assert isinstance(flat, list)
    assert len(flat) > 0
    first = flat[0]
    assert "year" in first
    assert "period" in first
    assert "pdfUrl" in first
    # should be sorted ascending by year
    years = [item["year"] for item in flat]
    assert years == sorted(years)


def test_download_categorisation_file(client):
    flat = client.research.categorisation_of_stocks_flat()
    # pick the most recent excel
    latest = flat[-1]
    data = client.research.download_categorisation_file(latest["excelUrl"])
    assert isinstance(data, bytes)
    assert len(data) > 1000


@pytest.mark.asyncio
async def test_async_categorisation(async_client):
    data = await async_client.research.categorisation_of_stocks()
    assert isinstance(data, dict)
    assert len(data) >= 8


@pytest.mark.asyncio
async def test_async_categorisation_flat(async_client):
    flat = await async_client.research.categorisation_of_stocks_flat()
    assert isinstance(flat, list)
    assert len(flat) > 0


@pytest.mark.asyncio
async def test_async_download_file(async_client):
    flat = await async_client.research.categorisation_of_stocks_flat()
    data = await async_client.research.download_categorisation_file(flat[-1]["excelUrl"])
    assert isinstance(data, bytes)
    assert len(data) > 1000
