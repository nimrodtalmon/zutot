#!/usr/bin/env python3
"""Refresh the citation count and h-index in cv/index.html from Google Scholar.

Run by .github/workflows/pages.yml before each deploy. Any failure (Scholar
blocking the runner, layout change) leaves the page untouched and exits 0.
"""
import os
import re
import sys
import urllib.request

URL = "https://scholar.google.com/citations?user=dSfOjCQAAAAJ&hl=en"
PAGE = os.path.join(os.path.dirname(__file__), "index.html")


def main():
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept-Language": "en"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        # Stats table: citations all, since; h-index all, since; i10 all, since.
        vals = [int(v) for v in re.findall(r'class="gsc_rsb_std">(\d+)<', html)]
        cites, h = vals[0], vals[2]
    except Exception as e:  # noqa: BLE001
        print(f"Scholar fetch/parse failed, keeping current numbers: {e}")
        return
    if not (1000 <= cites <= 100000 and 10 <= h <= 200):
        print(f"Implausible values {cites=} {h=}, keeping current numbers")
        return
    cites_txt = f"{cites // 100 * 100:,}+"
    page = open(PAGE, encoding="utf-8").read()
    new = re.sub(r'(<span id="cites">)[^<]*(</span>)', rf"\g<1>{cites_txt}\g<2>", page)
    new = re.sub(r'(<span id="hindex">)[^<]*(</span>)', rf"\g<1>{h}\g<2>", new)
    if new != page:
        open(PAGE, "w", encoding="utf-8").write(new)
        print(f"Updated: {cites_txt} citations, h-index {h}")
    else:
        print("No change")


if __name__ == "__main__":
    sys.exit(main())
