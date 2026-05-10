"""Tests for amfipy.aum — Assets Under Management."""
import pytest
from conftest import MF_ID


# ── Average AUM ────────────────────────────────────────────────────────────────

def test_financial_years(client):
    fys = client.aum.financial_years()
    assert isinstance(fys, list)
    assert len(fys) > 0
    assert "id" in fys[0]
    assert "financial_year" in fys[0]


def test_periods(client):
    fys = client.aum.financial_years()
    fy_id = fys[0]["id"]
    result = client.aum.periods(fy_id=fy_id)
    assert isinstance(result, dict)
    assert "periods" in result


def test_average_aum_fundwise(client):
    fys = client.aum.financial_years()
    periods = client.aum.periods(fy_id=fys[0]["id"])
    period_id = periods["periods"][0]["id"]
    data = client.aum.average_aum_fundwise(fy_id=fys[0]["id"], period_id=period_id)
    assert isinstance(data, list)
    assert len(data) > 0


def test_average_aum_schemewise(client):
    fys = client.aum.financial_years()
    periods = client.aum.periods(fy_id=fys[0]["id"])
    fy_id = fys[0]["id"]
    period_id = periods["periods"][0]["id"]
    data = client.aum.average_aum_schemewise(
        fy_id=fy_id, period_id=period_id, str_type="Categorywise", mf_id=MF_ID
    )
    assert data is not None


def test_average_aum_fundwise_excel(client):
    fys = client.aum.financial_years()
    periods = client.aum.periods(fy_id=fys[0]["id"])
    excel = client.aum.average_aum_fundwise_excel(
        fy_id=fys[0]["id"], period_id=periods["periods"][0]["id"]
    )
    assert isinstance(excel, bytes)
    assert len(excel) > 1000


# ── AUM Disclosure ─────────────────────────────────────────────────────────────

def test_disclosure_by_category(client):
    data = client.aum.disclosure_by_category(fy_id="2024-25")
    assert isinstance(data, list)
    assert len(data) > 0


def test_disclosure_by_geography(client):
    data = client.aum.disclosure_by_geography(fy_id="2024-25")
    assert isinstance(data, list)


# ── Age-wise Folio ─────────────────────────────────────────────────────────────

def test_agewise_folio(client):
    data = client.aum.agewise_folio(month="March-2026")
    assert isinstance(data, dict) or isinstance(data, list)


def test_agewise_folio_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.aum.agewise_folio(month="March-2026", as_df=True)
    assert isinstance(df, polars.DataFrame)


def test_agewise_folio_excel(client):
    data = client.aum.agewise_folio_excel(month="March-2026")
    assert isinstance(data, bytes)


# ── Classified AUM ─────────────────────────────────────────────────────────────

def test_classified_dates(client):
    dates = client.aum.classified_dates()
    assert isinstance(dates, list)
    assert len(dates) > 0


def test_statewise(client):
    data = client.aum.statewise(date="01-apr-2026", mf_id=0)
    assert isinstance(data, list)
    assert len(data) > 0


def test_scheme_catwise(client):
    data = client.aum.scheme_catwise(date="01-apr-2026", mf_id=0)
    assert isinstance(data, list)


def test_statewise_excel(client):
    data = client.aum.statewise_excel(date="01-apr-2026")
    assert isinstance(data, bytes)


# ── Bifurcation ────────────────────────────────────────────────────────────────

def test_bifurcation(client):
    data = client.aum.bifurcation(date="31-Mar-2026")
    assert isinstance(data, list)
    assert len(data) > 0


def test_bifurcation_as_df(client):
    polars = pytest.importorskip("polars")
    df = client.aum.bifurcation(date="31-Mar-2026", as_df=True)
    assert isinstance(df, polars.DataFrame)


def test_bifurcation_range(client):
    results = client.aum.bifurcation_range(dates=["31-Mar-2026", "28-Feb-2026"])
    assert isinstance(results, dict)
    assert len(results) == 2


def test_bifurcation_excel(client):
    data = client.aum.bifurcation_excel(date="31-Mar-2026")
    assert isinstance(data, bytes)


@pytest.mark.asyncio
async def test_async_financial_years(async_client):
    fys = await async_client.aum.financial_years()
    assert isinstance(fys, list)
    assert len(fys) > 0


@pytest.mark.asyncio
async def test_async_bifurcation_range(async_client):
    results = await async_client.aum.bifurcation_range(dates=["31-Mar-2026", "28-Feb-2026"])
    assert len(results) == 2
