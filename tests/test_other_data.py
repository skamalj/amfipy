"""Tests for amfipy.other_data."""
import pytest
from conftest import MF_ID


def test_investor_complaints_monthly(client):
    data = client.other_data.investor_complaints_monthly(
        month="March-2026", mf_id=MF_ID, part=1
    )
    assert isinstance(data, list)
    assert len(data) > 0


def test_investor_complaints_monthly_all_parts(client):
    for part in [1, 2, 3, 4]:
        data = client.other_data.investor_complaints_monthly(
            month="March-2026", mf_id=MF_ID, part=part
        )
        assert isinstance(data, list), f"Part {part} failed"


def test_investor_complaints_monthly_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.other_data.investor_complaints_monthly(
        month="March-2026", mf_id=MF_ID, part=1, as_df=True
    )
    assert isinstance(df, polars.DataFrame)


def test_investor_complaints_yearly(client):
    data = client.other_data.investor_complaints_yearly(year="2019-2020", mf_id=MF_ID)
    assert isinstance(data, list)
    assert len(data) > 0


def test_amc_directors(client):
    data = client.other_data.amc_directors(mf_id=MF_ID)
    assert isinstance(data, list)
    assert len(data) > 0


def test_amc_directors_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.other_data.amc_directors(mf_id=MF_ID, as_df=True)
    assert isinstance(df, polars.DataFrame)


def test_trustees(client):
    data = client.other_data.trustees(mf_id=MF_ID)
    assert isinstance(data, list)
    assert len(data) > 0


def test_group_companies_page(client):
    result = client.other_data.group_companies(page=1, size=10)
    assert isinstance(result, dict)
    assert "data" in result
    assert len(result["data"]) == 10
    assert result["pagination"]["total"] > 0


def test_group_companies_all(client):
    all_cos = client.other_data.group_companies_all(size=100)
    assert isinstance(all_cos, list)
    assert len(all_cos) >= 500


def test_populate_schemes(client):
    schemes = client.other_data.populate_schemes(mf_id=MF_ID)
    assert isinstance(schemes, list)
    assert len(schemes) > 0
    assert "scheme_id" in schemes[0]
    assert "scheme_name" in schemes[0]


def test_scheme_data(client):
    schemes = client.other_data.populate_schemes(mf_id=MF_ID)
    sd_id = schemes[0]["scheme_id"]
    data = client.other_data.scheme_data(mf_id=MF_ID, sd_id=sd_id)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "Scheme_NAV_Name" in data[0]
    assert "Net_Asset_Value" in data[0]


def test_scheme_data_as_df(client):
    polars = pytest.importorskip("polars")
    schemes = client.other_data.populate_schemes(mf_id=MF_ID)
    sd_id = schemes[0]["scheme_id"]
    df = client.other_data.scheme_data(mf_id=MF_ID, sd_id=sd_id, as_df=True)
    assert isinstance(df, polars.DataFrame)
    assert len(df) > 0


def test_scheme_details(client):
    schemes = client.other_data.populate_schemes(mf_id=MF_ID)
    sd_id = schemes[0]["scheme_id"]
    info = client.other_data.scheme_details(mf_id=MF_ID, sd_id=sd_id)
    assert isinstance(info, dict)
    assert "Scheme_Name" in info
    assert "Scheme_Objective" in info
    assert "SchemeType_Desc" in info
    assert "SchemeCat_Desc" in info
    assert "Scheme_min_amt" in info


def test_scheme_dividends(client):
    schemes = client.other_data.populate_schemes(mf_id=MF_ID)
    sd_id = schemes[0]["scheme_id"]
    data = client.other_data.scheme_dividends(mf_id=MF_ID, sd_id=sd_id, year=2026)
    assert isinstance(data, list)


def test_accounts_annual(client):
    data = client.other_data.accounts_annual(mf_id=MF_ID)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "amcaccountURL" in data[0] or "mfaccountURL" in data[0]


def test_accounts_half_yearly(client):
    data = client.other_data.accounts_half_yearly(mf_id=MF_ID)
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_async_complaints_monthly(async_client):
    data = await async_client.other_data.investor_complaints_monthly(
        month="March-2026", mf_id=MF_ID, part=1
    )
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_async_amc_directors(async_client):
    data = await async_client.other_data.amc_directors(mf_id=MF_ID)
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_async_scheme_details(async_client):
    schemes = await async_client.other_data.populate_schemes(mf_id=MF_ID)
    sd_id = schemes[0]["scheme_id"]
    info = await async_client.other_data.scheme_details(mf_id=MF_ID, sd_id=sd_id)
    assert isinstance(info, dict)
    assert "Scheme_Name" in info


@pytest.mark.asyncio
async def test_async_group_companies_all(async_client):
    all_cos = await async_client.other_data.group_companies_all(size=100)
    assert isinstance(all_cos, list)
    assert len(all_cos) >= 500
