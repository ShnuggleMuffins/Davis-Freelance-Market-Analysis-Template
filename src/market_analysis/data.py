"""
market_analysis.data
--------------------
Thin wrapper around pandas so downstream code never touches paths or URLs.
"""

from __future__ import annotations
import pathlib, io, requests
import pandas as pd


def _read_csv(buffer: io.BytesIO | str, *, date_cols: list[str] | None = None) -> pd.DataFrame:
    """Internal helper – always use UTF-8 and low-memory-off to avoid dtype issues."""
    return pd.read_csv(buffer, parse_dates=date_cols, low_memory=False)


def load_market_data(source: str | pathlib.Path, *, date_cols: list[str] | None = None) -> pd.DataFrame:
    """
    Load a CSV either from disk or HTTP(S) and return a clean DataFrame.

    Parameters
    ----------
    source      path/to/file.csv **or** https://example.com/file.csv
    date_cols   column names to parse as datetime64[ns]
    """
    src = str(source)
    if src.startswith("http"):
        resp = requests.get(src, timeout=30)
        resp.raise_for_status()
        return _read_csv(io.BytesIO(resp.content), date_cols=date_cols)
    return _read_csv(src, date_cols=date_cols)

