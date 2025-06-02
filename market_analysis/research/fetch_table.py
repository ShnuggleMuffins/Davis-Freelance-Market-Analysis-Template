"""
market_analysis.research.fetch_table
────────────────────────────────────
Utility that uses GPT-4o’s *Run deep research* tool to pull a
JSON table from the web and save it locally.

Example call (CLI):
    python market_analysis/research/fetch_table.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI

# ----------------------------------------------------------------------
MODEL = os.getenv("MARKET_ANALYSIS_MODEL", "gpt-4o-mini")
client = OpenAI()


def fetch_table(
    query: str,
    columns: list[str],
    out_json: str | Path = "data/table.json",
) -> Path:
    """
    Ask GPT-4o to “run deep research” for *query* and return a JSON array
    whose objects contain exactly *columns*.

    Parameters
    ----------
    query      : A natural-language search query.
    columns    : List of column names you expect in each JSON object.
    out_json   : Where to save the resulting JSON.  Parent folders are created.
    """
    prompt = f"""
Run deep research and return ONLY valid JSON (no markdown, no commentary).
The JSON must be an array where each object has these keys **in this order**:
{', '.join(columns)}.

Query:
{query}
"""
    print("⏳  Querying GPT-4o …")
    rsp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=1200,
    )

    json_txt = rsp.choices[0].message.content.strip()

    try:
        data = json.loads(json_txt)
    except json.JSONDecodeError as e:
        raise RuntimeError("GPT-4o did not return valid JSON") from e

    out_path = Path(out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2))
    print(f"✅  Saved {len(data)} rows → {out_path}")
    return out_path


# ----------------------------------------------------------------------
# Simple CLI demo: fetch the coffee-market table we used earlier.
if __name__ == "__main__":
    fetch_table(
        query="Global coffee-bean market revenue by year 2018-2024 in USD billions "
        "(include the source URL for each value)",
        columns=["Year", "Revenue", "SourceURL"],
        out_json="data/coffee_raw.json",
    )

