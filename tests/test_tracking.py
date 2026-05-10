"""Tests for amfipy.tracking — Tracking Error and Tracking Difference."""
import pytest
from conftest import MF_ID


def test_error_all(client):
    data = client.tracking.error(date="31-mar-2026")
    assert isinstance(data, list)
    assert len(data) > 0


def test_error_single_amc(client):
    data = client.tracking.error(date="31-mar-2026", mf_id=MF_ID)
    assert isinstance(data, list)


def test_error_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.tracking.error(date="31-mar-2026", as_df=True)
    assert isinstance(df, polars.DataFrame)


def test_error_range(client):
    results = client.tracking.error_range(dates=["31-mar-2026", "28-feb-2026"])
    assert isinstance(results, dict)
    assert "31-mar-2026" in results
    assert "28-feb-2026" in results


def test_difference(client):
    data = client.tracking.difference(month="01-Apr-2026")
    assert isinstance(data, list)


def test_difference_single_amc(client):
    data = client.tracking.difference(month="01-Apr-2026", mf_id=MF_ID)
    assert isinstance(data, list)


def test_difference_range(client):
    results = client.tracking.difference_range(months=["01-Apr-2026", "01-Mar-2026"])
    assert isinstance(results, dict)
    assert len(results) == 2


@pytest.mark.asyncio
async def test_async_error(async_client):
    data = await async_client.tracking.error(date="31-mar-2026")
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_async_error_range(async_client):
    results = await async_client.tracking.error_range(dates=["31-mar-2026", "28-feb-2026"])
    assert len(results) == 2


@pytest.mark.asyncio
async def test_async_difference(async_client):
    data = await async_client.tracking.difference(month="01-Apr-2026")
    assert isinstance(data, list)
