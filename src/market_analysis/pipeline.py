"""
market_analysis.pipeline
------------------------
End-to-end helper that glues data → metric → LLM insight → chart.
"""

from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd

from .data import load_market_data
from .metrics import yoy_growth
from .llm import ask


def run_slice(source: str) -> tuple[str, plt.Figure]:
    """
    Return (insight_text, chart_figure) for a single dataset.
    """
    df = load_market_data(source, date_cols=["Year"])
    growth = yoy_growth(df, "Revenue", "Year") * 100

    # --- draft executive insight with GPT-4o ---
    insight = ask(
        f"The CSV shows revenue from {df['Year'].min()}-{df['Year'].max()}. "
        f"The latest YoY growth is {growth:.1f} %. "
        f"Write a crisp, 2-sentence insight laser-focused on the growth number."
    )

    # --- quick chart ---
    fig, ax = plt.subplots()
    df.groupby("Year")["Revenue"].sum().plot(ax=ax)
    ax.set_title("Revenue by Year")
    ax.set_ylabel("USD (millions)")
    ax.grid(True)

    return insight, fig

