import csv, requests, pathlib

REG = pathlib.Path(__file__).parents[1] / "registry/registry.csv"

def test_links():
    for row in csv.DictReader(REG.open()):
        url = row["url"]
        if not url:
            continue
        r = requests.head(url, allow_redirects=True, timeout=10)
        assert r.status_code < 400, f"{row['source_id']} broken → {r.status_code}"
