"""Two-column copy of evaluation_lowerbody v1 — a one-off, not kept in step with v1
(Harry, chat 2026-10-22: P ok · O1 A · O2 B; Stage 2 D-09). Made from a copy of build_2col.py,
which stays unchanged (Stage 2 R55).

Run: python3 -B build_evaluation_lowerbody_2col_v1.py <svg_routine_generator dir> <evaluation_lowerbody.svg (v1)> <out.svg>
The cards, their pictures and links, and the four end boxes are moved from the v1 file as they are.
The header, legend, intro boxes, section headers and version note are drawn again for the
1360 px page with the generator's own functions; the generator is not edited.
v1's sport note ("Day after: no badminton …") is left out: evaluation files carry none (Stage 2 R59 · D-02).
Layout (O2 B): sections start full width, two cards per row, card 5 alone, section D beside card 12.
"""
import html
import re
import sys

sys.path.insert(0, sys.argv[1])
import routine_generator as rg  # noqa: E402
from routine_generator import InfoBox, MuscleColor, Section  # noqa: E402

SRC = open(sys.argv[2], encoding="utf-8").read()
PAGE_W, DX = 1360, 680

rg.MUSCLE_COLORS.update({
    "eval_hip": MuscleColor("eval_hip", "Hip / glutes",
                            "#085041", "#e1f5ee", "#0f6e56", "#085041", "#0f6e56"),
    "eval_knee": MuscleColor("eval_knee", "Knee (quads, hamstrings)",
                             "#26215c", "#eeedfe", "#534ab7", "#26215c", "#3c3489"),
    "eval_ankle": MuscleColor("eval_ankle", "Ankle / calf",
                              "#185fa5", "#e6f1fb", "#378add", "#042c53", "#185fa5"),
})

# ─── split v1 into blocks at its comments (a picture's comment stays with its card) ──
starts = [m.start() for m in re.finditer(r"<!-- ", SRC) if not SRC.startswith("<!-- PIC ", m.start())]
end = SRC.rindex("</svg>")
blocks = {}
order = []
for i, s in enumerate(starts):
    e = starts[i + 1] if i + 1 < len(starts) else end
    text = SRC[s:e].rstrip()
    label = text[5:text.index(" -->")]
    blocks[label] = text
    order.append(label)


def texts(block):
    return [html.unescape(t) for t in re.findall(r"<text [^>]*>([^<]*)</text>", block)]


def first_rect(block, width):
    m = re.search(rf'<rect x="30" y="(\d+)" width="{width}" height="(\d+)"', block)
    return int(m.group(1)), int(m.group(2))


cards = {}
for lab in order:
    m = re.match(r"([A-D])(\d+) — ", lab)
    if m:
        y0, h0 = first_rect(blocks[lab], 8)
        cards[int(m.group(2))] = (blocks[lab], y0, h0)
assert sorted(cards) == list(range(1, 14)), sorted(cards)
sections = {lab[3]: texts(blocks[lab])[0] for lab in order if lab.startswith("── ")}


def move_card(n, dx, y, h):
    block, y0, h0 = cards[n]
    if h != h0:
        block = block.replace(f'width="8" height="{h0}"', f'width="8" height="{h}"', 1)
        block = block.replace(f'width="612" height="{h0}"', f'width="612" height="{h}"', 1)
    return [f'<g transform="translate({dx},{y - y0})">', block, "</g>", ""]


def move_box(label, dx, y, h):
    block = blocks[label]
    y0, h0 = first_rect(block, 620)
    if h != h0:
        block = block.replace(f'<rect x="30" y="{y0}" width="620" height="{h0}"',
                              f'<rect x="30" y="{y0}" width="620" height="{h}"', 1)
    return [f'<g transform="translate({dx},{y - y0})">', block, "</g>", ""]


def section_header(letter, y, width, dx=0):
    rg.CONTENT_WIDTH = width
    lines, y2 = rg._render_section_header(Section(header=sections[letter], items=[],
                                                   comment_label=order_label[letter]), y)
    rg.CONTENT_WIDTH = 620
    if dx:
        lines = [f'<g transform="translate({dx},0)">'] + lines + ["</g>"]
    return lines + [""], y2


order_label = {"A": "A RANGES", "B": "B CONTROL TESTS", "C": "C SYMMETRY TESTS", "D": "D SESSION 2"}
heights = {n: c[2] for n, c in cards.items()}
body = []

# ─── header and legend, full width ────────────────────────────────────────
head = texts(SRC[:SRC.index("<!-- ")])
rg.PAGE_WIDTH = PAGE_W
body += rg._render_header(head[0], head[1] + " · two-column copy") + [""]
rg.CONTENT_WIDTH = 1300
lines, y = rg._render_legend(["eval_hip", "eval_knee", "eval_ankle"], rg.LEGEND_TOP)
rg.CONTENT_WIDTH = 620
body += lines + [""]

# ─── intro: v1's lines less its sport note, as two boxes ─────────────────
intro = [t for t in texts(blocks["PRE-WORKOUT NOTE"])[1:] if not t.startswith("Day after:")]
assert len(intro) == 10 and intro[5].startswith("Angles:"), intro
left = InfoBox("Before you start — what, when and kit", [intro[i] for i in (0, 1, 7, 8, 9)])
right = InfoBox("How the phone is used — camera, beat and angles", [intro[i] for i in (2, 3, 4, 5, 6)])
ll, yl = rg._render_info_box(left, y, comment="PRE-WORKOUT NOTE (1 of 2)")
rl, yr = rg._render_info_box(right, y, comment="PRE-WORKOUT NOTE (2 of 2)")
assert yl == yr
body += ll + [""] + [f'<g transform="translate({DX},0)">'] + rl + ["</g>", ""]
y = yl

# ─── sections: two cards per row, rows share the taller height ───────────
ROWS = {"A": [(1, 2), (3, 4), (5, None)],
        "B": [(6, 7), (8, 9)],
        "C": [(10, 11)]}
for letter in "ABC":
    lines, y = section_header(letter, y, 1300)
    body += lines
    for a, b in ROWS[letter]:
        h = max(heights[a], heights[b]) if b else heights[a]
        body += move_card(a, 0, y, h) + (move_card(b, DX, y, h) if b else [])
        y += h + rg.CARD_GAP
    if letter == "C":
        # card 12 on the left; section D (header + card 13) beside it on the right
        h = max(heights[12], rg.SECTION_HEADER_HEIGHT + 10 + heights[13])
        body += move_card(12, 0, y, h)
        lines, y_d = section_header("D", y, 620, dx=DX)
        body += lines + move_card(13, DX, y_d, h - (y_d - y))
        y += h + rg.CARD_GAP
    y = y - rg.CARD_GAP + rg.SECTION_GAP
y = y - rg.SECTION_GAP + rg.BLOCK_GAP

# ─── the four end boxes, two per column in v1's order; the shorter column's last box stretches ──
COLS = ((0, ["POST-WORKOUT NOTE", "GLOBAL RULES"]), (DX, ["TIMING SUMMARY", "SET COUNT"]))
stack = {dx: sum(first_rect(blocks[lab], 620)[1] for lab in labs) + rg.BLOCK_GAP * (len(labs) - 1)
         for dx, labs in COLS}
bottom = max(stack.values())
for dx, labs in COLS:
    yy = y
    for i, lab in enumerate(labs):
        h = first_rect(blocks[lab], 620)[1] + (bottom - stack[dx] if i == len(labs) - 1 else 0)
        body += move_box(lab, dx, yy, h)
        yy += h + rg.BLOCK_GAP
y += bottom + rg.BLOCK_GAP

note = ("v1 — two-column copy of evaluation_lowerbody v1: the same tests, pictures and links, without v1's "
        "sport note (Stage 2 R59); not updated when v1 changes (Harry, 2026-10-22)")
lines, y = rg._render_version_note(note, y)
body += lines

svg = "\n".join([f'<svg width="100%" viewBox="0 0 {PAGE_W} {y + 10}" xmlns="http://www.w3.org/2000/svg" '
                 f'style="font-family: sans-serif;">', "", *body, "", "</svg>"])
needle = ">" + intro[5] + "</text>"
start = svg.index(needle)
tag = svg.rindex("<text ", 0, start)
stop = start + len(needle)
link = re.search(r'<a href="([^"]+)" target="_blank"><text [^>]*>Angles:', blocks["PRE-WORKOUT NOTE"]).group(1)
svg = svg[:tag] + f'<a href="{link}" target="_blank">' + svg[tag:stop] + "</a>" + svg[stop:]
with open(sys.argv[3], "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print(sys.argv[3], len(svg.encode("utf-8")), "bytes, height", y + 10)
