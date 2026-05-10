"""Shared utilities for amfipy."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def maybe_polars(data: list[dict], as_df: bool):
    """Return a polars DataFrame if as_df=True, else the raw list."""
    if not as_df:
        return data
    try:
        import polars as pl
        return pl.DataFrame(data)
    except ImportError as e:
        raise ImportError(
            "polars is required for as_df=True. "
            "Install it with: pip install amfipy[polars]"
        ) from e


def _month_param(month: str) -> str:
    """Normalise month to MM-YYYY format."""
    return month.strip()


def _fin_year(year: str) -> str:
    """Normalise financial year to YYYY-YYYY format."""
    return year.strip()
