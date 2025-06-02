"""
market_analysis.metrics
-----------------------
Numeric helpers that operate on a DataFrame returned by data.load_market_data().
"""

import pandas as pd


def yoy_growth(df: pd.DataFrame, value_col: str, date_col: str) -> float:
    """
    Year-over-year growth for the most recent period in `date_col`.

    Example
    -------
    >>> yoy_growth(df, "Revenue", "Year")
    0.12     # == 12 %
    """
    latest_year = df[date_col].max()
    prev_year   = latest_year - 1
    latest_val  = df.loc[df[date_col] == latest_year, value_col].sum()
    prev_val    = df.loc[df[date_col] == prev_year,   value_col].sum()
    return (latest_val - prev_val) / prev_val

