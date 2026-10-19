"""Render an SVG to PNG in Chromium with sans-serif = Liberation Sans (reference.md §R4)."""
import sys, pathlib, re
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]).resolve(); dst = sys.argv[2]
svg = src.read_text(encoding="utf-8")
m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg); w, h = int(m.group(1)), int(m.group(2))
html = ("<html><head><style>html,body{margin:0;background:#fff} svg{font-family:'Liberation Sans' !important}"
        " text{font-family:'Liberation Sans' !important}</style></head><body>"
        + svg.replace('width="100%"', f'width="{w}"', 1) + "</body></html>")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1.5)
    pg.set_content(html); pg.wait_for_timeout(200)
    pg.screenshot(path=dst, full_page=True)
    b.close()
print(dst, w, h)
