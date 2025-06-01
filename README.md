# Symphony-Market-Analysis-Template
A reproducible, **audit‑ready** repository scaffold for AI‑assisted market‑analysis projects.


---
## 1 · Prerequisites

| Tool | Why you need it | Quick install |
|------|-----------------|---------------|
| **Git >= 2.35** | version‑control & GitHub sync | macOS: `brew install git` • Windows: <https://git-scm.com/download/win> |
| **GitHub account** | remote repo + issues/wiki | <https://github.com> |
| **Quarto CLI >= 1.6** | single‑source PDF + PPT build | <https://quarto.org/docs/get-started/> |
| **Miniconda ( Python 3.11 )** | isolated env for notebooks & tests | <https://docs.conda.io/en/latest/miniconda.html> |
| **VS Code (+ Quarto ext.)** *(optional)* | friendly editor | <https://code.visualstudio.com/> |

> **Tip**  
> If you prefer a GUI, install **GitHub Desktop** instead of using the command line.

---
## 2 · One‑time setup

```bash
# 1.  Sign in on GitHub and create a **new public repo**
#     Name:  symphony-market-analysis-template

# 2.  Clone it locally (substitute your user):
$ git clone https://github.com/<USERNAME>/symphony-market-analysis-template.git
$ cd symphony-market-analysis-template

# 3.  Create & activate Python env
$ conda create -n symphony_analysis python=3.11 -y
$ conda activate symphony_analysis

# 4.  Install Quarto + deps (once)
$ pip install -r requirements.txt
```

Add your **Perplexity / Scite / Elicit** API keys to a local `.env` (never commit real keys):

```dotenv
# .env.example → copy to .env and fill
PERPLEXITY_API_KEY=""  
SCITE_API_KEY=""  
ELICIT_API_KEY=""
```

---
## 3 · Directory layout

```
├── _quarto.yml          # project config (PDF + slides)
├── README.md            # this file
├── requirements.txt     # Python deps
├── data/
│   ├── raw/             # wget or API pulls (immutable)
│   └── processed/       # cleaned CSV / Parquet
├── registry/
│   └── registry.csv     # Source Registry (one row per citation)
├── analysis/
│   └── notebook.qmd     # Quarto notebook – main analysis
├── reports/             # Auto‑rendered outputs
├── tests/
│   ├── test_links.py    # HTTP 200 checker
│   └── test_numbers.py  # numeric‑diff smoke test
└── .gitignore
```

---
## 4 · Key files

### `_quarto.yml`
```yaml
project:
  type: website      # enables PDF & slides in one build
  output-dir: reports

format:
  pdf:
    toc: true
    number-sections: true
  pptx: default

execute:
  freeze: auto       # caches code unless source changes
```

### `analysis/notebook.qmd` (stub)
```markdown
---
title: "Market Analysis – TEMPLATE"
format: pdf
execute:
  echo: false
---

```{python}
#| label: setup
import pandas as pd
print("hello Symphony 🧠")
```

## 1 Introduction

Text…
```

### `registry/registry.csv`
```csv
source_id,title,outlet,year,url,doi,access_date,content_sha256
```

### `tests/test_links.py`
```python
import csv, requests, pathlib
REG = pathlib.Path(__file__).parents[1] / "registry/registry.csv"
for row in csv.DictReader(REG.open()):
    r = requests.head(row["url"], allow_redirects=True, timeout=10)
    assert r.status_code < 400, f"{row['source_id']} broken → {r.status_code}"
```

---
## 5 · Typical workflow

1. **Scope** ‑ fill out `scoping_sheet.xlsx` (create your own) and commit.
2. **Source** ‑ run retrieval script → writes snapshots into `data/raw/` + updates `registry.csv`.
3. **Synthesize** ‑ write / run code in `analysis/notebook.qmd`; `quarto render` produces PDF & PPTX.
4. **QA** ‑ `pytest` must pass; if it fails, fix links or numbers until green.
5. **Deliver** ‑ commit + push, then share `reports/Market‑Analysis.pdf` with client.

---
## 6 · Zero‑to‑first‑build cheat‑sheet

```bash
# Render report
quarto render analysis/notebook.qmd

# Run QA
pytest

# Add & push
git add .
git commit -m "First skeleton build"
git push origin main
```

---
## 7 · Extending the template

* **Automated builds** – enable *GitHub Actions* with a simple workflow that runs `conda install`, `quarto render`, and `pytest` on each push.
* **Vector search** – add a `scripts/` folder with RAG pipeline using Llama‑Index.
* **Evidence pack** – bundle `data/raw/` + `registry.csv` into a ZIP artifact during CI.

Happy analysing! 🚀
