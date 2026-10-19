"""All pictures in figs.py on one sheet, for reviewing or editing them.

Run: python3 picture_grid.py <out_dir> <t1> [t2 ...]   (times in seconds; needs Playwright Chromium)
Writes <out_dir>/grid.svg and <out_dir>/grid_t<t>.png.
"""
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figs  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

COLS = {"shoulder": "#0f6e56", "elbow": "#185fa5", "wrist": "#c97b64", "spine": "#854f0b"}
JOINT = {"shoulder_raise": "shoulder", "shoulder_turnout": "shoulder", "elbow_range": "elbow", "wrist_range": "wrist",
         "lowback_range": "spine", "sidebend": "spine", "hip_hinge": "spine", "pelvic_tuck": "spine",
         "seated_knee": "spine", "rock_forward": "spine", "rock_back": "spine", "prone_knee": "spine",
         "blade_check": "shoulder", "kneeling_pushup": "elbow", "one_arm_hold": "elbow", "wrist_control": "wrist",
         "side_raise": "shoulder", "curl": "elbow", "band_wrist": "wrist", "score": "shoulder"}
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
keys = list(figs.PICTURES)
rows = (len(keys) + 4) // 5
parts = []
for i, k in enumerate(keys):
    x, y = (i % 5) * 170 + 6, (i // 5) * 150 + 16
    parts.append(f'<text x="{x}" y="{y - 4}" font-size="10">{i + 1} {k}</text>')
    parts.append(f'<g transform="translate({x},{y})"><rect width="156" height="132" fill="#fff" stroke="#999"/>'
                 f'{figs.PICTURES[k](COLS[JOINT.get(k, "shoulder")])}</g>')
H = rows * 150 + 20
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{H}" viewBox="0 0 860 {H}" '
       f'style="font-family:Liberation Sans">' + "".join(parts) + "</svg>")
(out / "grid.svg").write_text(svg, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 860, "height": H}, device_scale_factor=1.6)
    pg.set_content("<html><body style='margin:0;background:#fff'>" + svg + "</body></html>")
    pg.wait_for_timeout(100)
    for t in [float(a) for a in sys.argv[2:]]:
        pg.evaluate(f"(()=>{{const s=document.querySelector('svg');s.pauseAnimations();s.setCurrentTime({t});}})()")
        pg.wait_for_timeout(80)
        pg.screenshot(path=str(out / f"grid_t{t}.png"))
    b.close()
print(len(svg), "bytes")
