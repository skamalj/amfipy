"""Tests for amfipy.publications."""
import pytest


def test_monthly(client):
    data = client.publications.monthly()
    assert isinstance(data, list) or isinstance(data, dict)


def test_monthly_flat(client):
    flat = client.publications.monthly_flat()
    assert isinstance(flat, list)
    assert len(flat) > 0
    first = flat[0]
    assert "pdf_url" in first
    assert "excel_url" in first
    assert "financial_year" in first


def test_quarterly(client):
    data = client.publications.quarterly()
    assert isinstance(data, list) or isinstance(data, dict)


def test_quarterly_flat(client):
    flat = client.publications.quarterly_flat()
    assert isinstance(flat, list)
    assert len(flat) > 0
    assert "pdf_url" in flat[0]


def test_commission(client):
    data = client.publications.commission()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "URL" in data[0]


def test_download_excel(client):
    flat = client.publications.monthly_flat()
    assert flat, "No monthly publications found"
    url = flat[0]["excel_url"]
    data = client.publications.download_file(url)
    assert isinstance(data, bytes)
    assert len(data) > 1000


@pytest.mark.asyncio
async def test_async_monthly_flat(async_client):
    flat = await async_client.publications.monthly_flat()
    assert isinstance(flat, list)
    assert len(flat) > 0


@pytest.mark.asyncio
async def test_async_commission(async_client):
    data = await async_client.publications.commission()
    assert isinstance(data, list)
    assert len(data) > 0
