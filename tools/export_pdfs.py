"""Export every web talk deck under slides/ to a PDF backup in pdfs/<slug>.pdf.

One page per slide (1920x1080 screenshot, initial state of interactive slides).
Run from the repo root:  python3 tools/export_pdfs.py [slug ...]
Needs: playwright (chromium) and img2pdf.
"""
import functools, html, http.server, pathlib, re, sys, threading

import img2pdf
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "pdfs"
W, H = 1920, 1080


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def export(page, base, slug):
    url = f"{base}/slides/{slug}/index.html"
    page.goto(url)
    n = page.locator("#stage .slide").count()
    shots = []
    for k in range(1, n + 1):
        page.goto(f"{url}#{k}")
        page.reload()  # fresh state per slide
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.add_style_tag(content="#progress,#counter{display:none!important}")
        page.wait_for_timeout(400)
        shots.append(page.screenshot(type="png"))
    OUT.mkdir(exist_ok=True)
    layout = img2pdf.get_fixed_dpi_layout_fun((192, 192))  # 10in x 5.625in pages
    (OUT / f"{slug}.pdf").write_bytes(img2pdf.convert(shots, layout_fun=layout))
    print(f"{slug}: {n} slides -> pdfs/{slug}.pdf")


def write_index():
    """pdfs/index.html: unlinked list of all PDFs, in the homepage's Slides order."""
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    order = list(dict.fromkeys(re.findall(r'href="slides/([^/"]+)/"', home)))
    pdfs = sorted(OUT.glob("*.pdf"),
                  key=lambda p: (order.index(p.stem) if p.stem in order else len(order), p.stem))
    rows = []
    for p in pdfs:
        deck = ROOT / "slides" / p.stem / "index.html"
        m = re.search(r"<title>([^<]*)", deck.read_text(encoding="utf-8")) if deck.exists() else None
        title = html.escape(m.group(1).split(" · ")[0].strip() if m else p.stem)
        web = f' <a class="muted" href="../slides/{p.stem}/">web</a>' if deck.exists() else ""
        size = f"{p.stat().st_size / 1e6:.1f} MB"
        rows.append(f'  <li><a href="{p.name}" dir="auto">{title}</a>'
                    f' <span class="muted">· {size} ·</span>{web}</li>')
    (OUT / "index.html").write_text(INDEX.replace("{rows}", "\n".join(rows)), encoding="utf-8")
    print(f"pdfs/index.html: {len(rows)} PDFs")


INDEX = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Slides (PDF)</title>
<style>
  :root { --bg: #fbfaf7; --fg: #1d1d1b; --muted: #6b6a66; --accent: #b4520f; }
  @media (prefers-color-scheme: dark) {
    :root { --bg: #161615; --fg: #e9e7e2; --muted: #9b9890; --accent: #f08a3e; } }
  body { margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.6 Georgia, serif; }
  main { max-width: 640px; margin: 48px auto; padding: 0 16px; }
  h1 { font-size: 24px; font-weight: normal; margin: 0 0 16px; }
  ul { list-style: none; padding: 0; margin: 0; }
  li { margin: 6px 0; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .muted, a.muted { color: var(--muted); font-size: 14px; }
</style></head>
<body><main>
<h1>Slides (PDF)</h1>
<ul>
{rows}
</ul>
</main></body></html>
"""


def main():
    slugs = sys.argv[1:] or sorted(
        p.parent.name for p in (ROOT / "slides").glob("*/index.html"))
    srv = serve()
    base = f"http://127.0.0.1:{srv.server_port}"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, color_scheme="light")
        for slug in slugs:
            export(page, base, slug)
        browser.close()
    srv.shutdown()
    write_index()


if __name__ == "__main__":
    main()
