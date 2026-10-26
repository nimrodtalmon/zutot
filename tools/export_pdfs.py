"""Export every web talk deck under slides/ to a PDF backup in pdfs/<slug>.pdf.

One page per slide (1920x1080 screenshot, initial state of interactive slides).
Run from the repo root:  python3 tools/export_pdfs.py [slug ...]
Needs: playwright (chromium) and img2pdf.
"""
import functools, http.server, io, pathlib, sys, threading

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


if __name__ == "__main__":
    main()
