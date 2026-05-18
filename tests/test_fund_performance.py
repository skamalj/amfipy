"""Tests for amfipy.fund_performance."""
import pytest


def test_filters(client):
    pytest.importorskip("httpx")  # ensure httpx available
    try:
        data = client.fund_performance.filters()
        assert isinstance(data, dict)
        assert "mutualFundList" in data or "maturityTypeList" in data
    except Exception as e:
        if "ConnectTimeout" in type(e).__name__ or "Timeout" in type(e).__name__:
            pytest.skip(f"pollingsebi backend timeout: {e}")
        raise


def test_sub_categories(client):
    cats = client.fund_performance.sub_categories(category=1)
    assert isinstance(cats, list)
    assert len(cats) > 0


def test_fetch_open_equity(client):
    data = client.fund_performance.fetch(
        maturity_type=1, category=1, sub_category=1, mf_id=0
    )
    assert data is not None


def test_fetch_specific_amc(client):
    data = client.fund_performance.fetch(
        maturity_type=1, category=1, sub_category=1, mf_id=62
    )
    assert data is not None


def test_fetch_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.fund_performance.fetch(
        maturity_type=1, category=1, sub_category=1, mf_id=0,
        report_date="15-May-2026", as_df=True
    )
    assert isinstance(df, polars.DataFrame)
    assert len(df) > 0
    assert "schemeName" in df.columns


@pytest.mark.asyncio
async def test_async_filters(async_client):
    data = await async_client.fund_performance.filters()
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_async_fetch(async_client):
    data = await async_client.fund_performance.fetch(
        maturity_type=1, category=1, sub_category=1, mf_id=0
    )
    assert data is not None


@pytest.mark.asyncio
async def test_async_fetch_as_df(async_client):
    polars = pytest.importorskip("polars")
    df = await async_client.fund_performance.fetch(
        maturity_type=1, category=1, sub_category=1, mf_id=0,
        report_date="15-May-2026", as_df=True
    )
    assert isinstance(df, polars.DataFrame)
    assert len(df) > 0
