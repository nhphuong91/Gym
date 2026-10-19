"""Render a SMIL-animated SVG at chosen times, to check the moving pictures (reference.md §R4, D-78).

Run: python3 render_frames.py <file.svg> <out_dir> <t1> [t2 ...]   (times in seconds; needs Playwright Chromium)
Writes <out_dir>/frame_<t>.png and prints the number of <animate> elements and any console errors.
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', src).groups())
html = ("<html><head><style>html,body{margin:0;background:#fff} text{font-family:'Liberation Sans' !important}</style></head><body>"
        + src.replace('width="100%"', f'width="{w}"', 1) + "</body></html>")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1.0)
    errs = []
    pg.on("console", lambda m: errs.append(m.text))
    pg.set_content(html)
    pg.wait_for_timeout(200)
    for t in [float(a) for a in sys.argv[3:]]:
        pg.evaluate(f"(()=>{{const s=document.querySelector('svg');s.pauseAnimations();s.setCurrentTime({t});}})()")
        pg.wait_for_timeout(60)
        pg.screenshot(path=str(out / f"frame_{t}.png"), full_page=True)
    n = pg.evaluate("document.querySelectorAll('animate').length")
    b.close()
print("animate elements:", n, "console:", errs or "none")
