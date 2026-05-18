"""Tests for amfipy.nav — NAV data."""
import pytest
from conftest import MF_ID, NAV_SD_ID


def test_latest_all(client):
    data = client.nav.latest()
    assert isinstance(data, dict)
    assert "data" in data or isinstance(data, dict)


def test_latest_single_amc(client):
    data = client.nav.latest(mf_id=MF_ID, fund_type="Open Ended")
    assert isinstance(data, dict)


def test_latest_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.nav.latest(mf_id=MF_ID, as_df=True)
    assert isinstance(df, polars.DataFrame)
    assert len(df) > 0
    assert "schemeName" in df.columns
    assert "netAssetValue" in df.columns


def test_latest_by_category(client):
    data = client.nav.latest_by_category(mf_id="all")
    assert isinstance(data, (dict, list))


def test_schemes(client):
    schemes = client.nav.schemes(mf_id=MF_ID)
    assert isinstance(schemes, list)
    assert len(schemes) > 0
    assert "nav_id" in schemes[0]
    assert "nav_name" in schemes[0]


def test_all_navs_for_date(client):
    data = client.nav.all_navs_for_date(date="2026-03-31")
    assert isinstance(data, list)
    assert len(data) > 0


def test_history(client):
    data = client.nav.history(sd_id=NAV_SD_ID, from_date="2026-01-01", to_date="2026-03-31")
    assert isinstance(data, dict)
    assert "nav_groups" in data or "mf_name" in data


def test_history_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.nav.history(sd_id=NAV_SD_ID, from_date="2026-01-01", to_date="2026-03-31", as_df=True)
    assert isinstance(df, polars.DataFrame)
    assert len(df) > 0


def test_high_low(client):
    data = client.nav.high_low(
        sd_id=NAV_SD_ID, from_date="2026-01-01", to_date="2026-03-31",
        period_type="Month", nav_type="Both"
    )
    assert isinstance(data, dict)


def test_compare(client):
    data = client.nav.compare(sd_id=NAV_SD_ID, date1="2026-01-01", date2="2026-03-31")
    assert isinstance(data, dict)


def test_fetch_range(client):
    results = client.nav.fetch_range(
        sd_id=NAV_SD_ID,
        months=[("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28")]
    )
    assert isinstance(results, list)
    assert len(results) == 2


def test_download_file(client):
    data = client.nav.download_file(date="31-Mar-2026")
    assert isinstance(data, bytes)
    assert len(data) > 1000


@pytest.mark.asyncio
async def test_async_latest(async_client):
    data = await async_client.nav.latest()
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_async_latest_as_df(async_client):
    polars = pytest.importorskip("polars")
    df = await async_client.nav.latest(mf_id=MF_ID, as_df=True)
    assert isinstance(df, polars.DataFrame)
    assert len(df) > 0


@pytest.mark.asyncio
async def test_async_history(async_client):
    data = await async_client.nav.history(
        sd_id=NAV_SD_ID, from_date="2026-01-01", to_date="2026-01-31"
    )
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_async_fetch_range(async_client):
    results = await async_client.nav.fetch_range(
        sd_id=NAV_SD_ID,
        months=[("2026-01-01", "2026-01-31"), ("2026-02-01", "2026-02-28")]
    )
    assert len(results) == 2
