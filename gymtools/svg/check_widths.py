"""Width check for routine SVGs: the character-width estimate of reference.md §R4 (Stage2_RoutineFiles.md §2.2).

Run: python3 -B check_widths.py <file.svg> [...]. Each character counts 0.5 px per point of font size, any size
(9 = 4.5 px, 10.5 = 5.25 px, 11 = 5.5 px, 13 = 6.5 px). Flags, per file:
  EDGE      text past x 650 or left of x 30. Lines centred on a page wider than 680 px are flagged against the
            650 px edge and need a look by eye (e.g. the two-column copy's title, subtitle and version note).
  PICTURE   text inside a picture group (x 486) wider than its 154 px.
  TEXT>PIC  in a file with pictures: a card line at x 72 or 136 (size 10-11) past x 480, into the picture.
  TEXT>COL  in a file without pictures: a card line at x 72 or 136 (size 10-11) running into the right column on a
            line where that column has text (sets, RIR, equipment).
  TITLE     a card title at x 72 (size 12) running into the right column.
The right column is found per file: the leftmost bold size-12 text between x 480 and 560 (490 in generator files,
515 in the mobility files); 490 when there is none. Exit code is always 0: it reports, it does not gate.
"""
import html
import re
import sys


def check(path):
    svg = open(path, encoding="utf-8").read()
    pics = [(m.start(), svg.index("</g>", m.start())) for m in re.finditer(r'<g transform="translate\(486,', svg)]

    def inside(pos):
        return any(a <= pos <= b for a, b in pics)

    bad, items = [], []
    for m in re.finditer(r'<text ([^>]*)>([^<]*)</text>', svg):
        a, t = m.group(1), html.unescape(m.group(2))
        fs = re.search(r'font-size="([\d.]+)"', a)
        size = float(fs.group(1)) if fs else 11.0
        x = float(re.search(r' x="([\d.]+)"', a).group(1))
        y = float(re.search(r' y="([\d.]+)"', a).group(1))
        bold = 'font-weight="500"' in a or 'font-weight="bold"' in a
        mid = 'text-anchor="middle"' in a
        w = len(t) * size * 0.5
        l, r = (x - w / 2, x + w / 2) if mid else (x, x + w)
        if inside(m.start()):
            if r > 154 or l < 2:
                bad.append(f"PICTURE {t[:50]} ({l:.0f}–{r:.0f})")
            continue
        items.append((y, x, size, bold, l, r, t))
    col = min((x for y, x, size, bold, l, r, t in items if size == 12 and bold and 480 <= x <= 560), default=490)
    col_ys = {y for y, x, size, bold, l, r, t in items if col <= x < 650}
    for y, x, size, bold, l, r, t in items:
        if r > 650 or l < 30:
            bad.append(f"EDGE y={y:.0f} right={r:.0f}: {t[:70]}")
        if x in (72, 136) and 10 <= size <= 11:
            if pics and r > 480:
                bad.append(f"TEXT>PIC y={y:.0f} right={r:.0f}: {t[:70]}")
            elif not pics and y in col_ys and r > col - 6:
                bad.append(f"TEXT>COL y={y:.0f} right={r:.0f}: {t[:70]}")
        if x == 72 and size == 12 and r > col - 6:
            bad.append(f"TITLE y={y:.0f} right={r:.0f}: {t[:70]}")
    height = re.search(r'viewBox="0 0 \d+ (\d+)"', svg).group(1)
    if len(sys.argv) > 2:
        print(f"== {path}")
    print("\n".join(bad) if bad else "no overflow by heuristic")
    print(len(items), "text elements outside pictures;", len(pics), "pictures; right column at x", f"{col:g};",
          "height", height)


for p in sys.argv[1:]:
    check(p)
