"""
SVG renderer for Routine models.

Layout is computed top-to-bottom, tracking a running `y` cursor. Each
component knows its own height. Cards are uniform 54px tall by default
(use card_height_override=70 for cards with 3 detail lines, or 86 for
cards with 2 subtitle lines).

Card layout (h=54, text positions independent of card height):
  - title at +16
  - subtitle at +31 (when present, takes detail0 slot)
  - detail0 at +31
  - detail1 at +46
  - right column: sets/reps at +16, equipment at +31

Section header style:
  - Neutral gray bg, dark text, left-aligned at TEXT_PAD_X
  - Matches the upper body source SVG
  - Section.comment_label can override the auto-derived SVG comment label
"""
from .theme import (
    PAGE_WIDTH, CONTENT_X, CONTENT_WIDTH, TEXT_PAD_X, STRIPE_WIDTH,
    CARD_TEXT_X, CARD_NUM_X, CARD_RIGHT_X,
    TOP_MARGIN, SUBTITLE_OFFSET, LEGEND_TOP, SECTION_HEADER_HEIGHT,
    CARD_HEIGHT, CARD_GAP, SECTION_GAP, BLOCK_GAP, PAIR_LABEL_HEIGHT,
    NEUTRAL_BG, NEUTRAL_STROKE,
    SECTION_HEADER_BG, SECTION_HEADER_STROKE, SECTION_HEADER_TEXT_FILL,
    TITLE_FILL, SUBTITLE_FILL, NUMBER_FILL, PAIR_LABEL_FILL,
    RULE_TEXT_FILL, RULE_BULLET_FILL,
    TABLE_HEADER_FILL, TABLE_DIVIDER, TABLE_CELL_FILL, VERSION_NOTE_FILL,
    INFO_BG, INFO_STROKE, INFO_TITLE_FILL, INFO_BODY_FILL,
    color,
)
from .model import (
    Routine, Section, Exercise, Pair, InfoBox, RulesBox,
    SetCountBox, AlternativesTable,
)


# ─── Component dimensions ─────────────────────────────────────────────────

INFO_BOX_HEIGHT = 36
INFO_TITLE_OFFSET = 17
INFO_BODY_FIRST_OFFSET = 30
INFO_BODY_LINE_HEIGHT = 13

RULES_LINE_HEIGHT = 20
RULES_TOP_PAD = 22
RULES_FIRST_BULLET_OFFSET = 10
RULES_LAST_BULLET_BOTTOM_PAD = 20

TIMING_HEIGHT_BASE = 60
TIMING_TITLE_OFFSET = 20
TIMING_LINE_HEIGHT = 17
TIMING_BODY_FIRST_OFFSET = 37
TIMING_BOX_EXTRA = 7

SETCOUNT_TITLE_OFFSET = 22
SETCOUNT_LINE_HEIGHT = 18
SETCOUNT_FIRST_OFFSET = 42
SETCOUNT_BOTTOM_PAD = 14
SETCOUNT_COL2_X = 360       # x position of 2nd column (when entry.column == 1)
SETCOUNT_COL3_X = 530       # x position of 3rd column (when entry.column == 2)

TABLE_TITLE_OFFSET = 20
TABLE_HEADER_OFFSET = 42
TABLE_DIVIDER_TOP = 29
TABLE_DIVIDER_BOTTOM = 47
TABLE_FIRST_ROW_OFFSET = 62
TABLE_ROW_HEIGHT = 16
TABLE_BOTTOM_PAD = 12

LEGEND_HEIGHT = 56


# ─── Drawing helpers ───────────────────────────────────────────────────────

def _comment(text: str) -> str:
    """SVG comment for human navigation. Always emitted on its own line."""
    return f"<!-- {text} -->"


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _rect(x, y, w, h, rx, fill, stroke=None, sw=0.8):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    return s + "/>"


def _text(x, y, content, *, size=11, weight=None, fill="#000",
          anchor=None):
    attrs = [f'font-size="{size}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    attrs.append(f'fill="{fill}"')
    attrs.append(f'x="{x}"')
    attrs.append(f'y="{y}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    return f'<text {" ".join(attrs)}>{_esc(content)}</text>'


# ─── Component renderers — each returns (svg_lines, new_y) ────────────────

def _render_header(title: str, subtitle: str) -> list[str]:
    return [
        _text(PAGE_WIDTH // 2, TOP_MARGIN, title,
              size=15, weight=500, fill=TITLE_FILL, anchor="middle"),
        _text(PAGE_WIDTH // 2, TOP_MARGIN + SUBTITLE_OFFSET, subtitle,
              size=11, fill=SUBTITLE_FILL, anchor="middle"),
    ]


def _render_legend(muscles: list[str], y: int) -> tuple[list[str], int]:
    out = [
        _comment("LEGEND"),
        _rect(CONTENT_X, y, CONTENT_WIDTH, LEGEND_HEIGHT, 6,
              NEUTRAL_BG, NEUTRAL_STROKE),
        _text(TEXT_PAD_X, y + 18, "Muscle group",
              size=11, weight=500, fill=TITLE_FILL),
    ]
    swatch_y = y + 35
    text_y = y + 44

    def text_w(s: str) -> int:
        return int(len(s) * 5.5) + 4

    cur_x = 50
    slot_gap = 12
    # swatch_y/text_y recomputed: header on top line, swatches on bottom line
    # LEGEND_HEIGHT must be tall enough for both lines
    for key in muscles:
        c = color(key)
        out.append(_rect(cur_x, swatch_y, 10, 10, 2, c.stripe))
        out.append(_text(cur_x + 16, text_y, c.label, size=11, fill="#333"))
        cur_x += 16 + text_w(c.label) + slot_gap
    return out, y + LEGEND_HEIGHT + BLOCK_GAP


def _render_info_box(box: InfoBox, y: int, *, comment: str = "INFO BOX") -> tuple[list[str], int]:
    """Pre/post-workout info boxes — compact 36px height."""
    n = len(box.body_lines)
    h = INFO_BOX_HEIGHT + max(0, n - 1) * INFO_BODY_LINE_HEIGHT
    out = [
        _comment(comment),
        _rect(CONTENT_X, y, CONTENT_WIDTH, h, 8, INFO_BG, INFO_STROKE, sw=1),
        _text(TEXT_PAD_X, y + INFO_TITLE_OFFSET, box.title,
              size=12, weight=500, fill=INFO_TITLE_FILL),
    ]
    for i, line in enumerate(box.body_lines):
        out.append(_text(TEXT_PAD_X,
                         y + INFO_BODY_FIRST_OFFSET + i * INFO_BODY_LINE_HEIGHT,
                         line, size=11, fill=INFO_BODY_FILL))
    return out, y + h + BLOCK_GAP


def _section_letter(header: str) -> str:
    """Extract section letter from header like 'A — Warmup ...' -> 'A'."""
    h = header.strip()
    if h and h[0].isalpha() and (len(h) == 1 or not h[1].isalpha()):
        return h[0].upper()
    return ""


def _render_section_header(sec: Section, y: int) -> tuple[list[str], int]:
    """Section header — neutral gray background with dark text.

    Matches the upper body source style: 24px tall, rx=4, gray bg with
    dark text left-aligned at TEXT_PAD_X. Header text auto-shrinks from
    size 12 to size 11 if estimated width exceeds the box.

    Comment is wrapped as `<!-- ── LABEL ── -->`. Label is the user-
    provided `sec.comment_label` if set, else auto-derived from the
    header (letter + pre-colon text, uppercased).
    """
    # Comment label: prefer explicit override, else auto-derive from header.
    if sec.comment_label:
        label = sec.comment_label.upper().strip()
    else:
        # Take the part of the header before the first ':' (drops
        # superset descriptions). Strip trailing parenthetical (time/round
        # info). Replace the em-dash separator between letter and name
        # with a single space so "A — Warmup" becomes "A WARMUP".
        head = sec.header.split(":")[0]
        head = head.split("(")[0].strip().rstrip("·").strip()
        # Normalize the letter-name separator: " — " or " - " → " "
        head = head.replace(" — ", " ").replace(" - ", " ")
        label = head.upper()

    comment_text = f"── {label} ──"

    # Width estimate at size 12 (sans-serif, weight 500): ~6.0 px/char
    est_w = len(sec.header) * 6.0
    available_w = CONTENT_WIDTH - 2 * (TEXT_PAD_X - CONTENT_X)
    if est_w > available_w:
        font_size = 11
        weight = 500
    else:
        font_size = 12
        weight = 500

    out = [
        _comment(comment_text),
        _rect(CONTENT_X, y, CONTENT_WIDTH, SECTION_HEADER_HEIGHT, 4,
              SECTION_HEADER_BG, SECTION_HEADER_STROKE, sw=0.5),
        _text(TEXT_PAD_X, y + 16, sec.header,
              size=font_size, weight=weight, fill=SECTION_HEADER_TEXT_FILL),
        "",  # blank line before first card
    ]
    return out, y + SECTION_HEADER_HEIGHT + 10


def _short_title(title: str, max_chars: int = 40) -> str:
    """Take the first chunk of a title, stripping parentheticals."""
    # Drop everything from first '(' onward
    base = title.split("(")[0].strip()
    if len(base) <= max_chars:
        return base
    # Truncate on word boundary
    truncated = base[:max_chars].rsplit(" ", 1)[0]
    return truncated


def _render_exercise(ex: Exercise, y: int, *, section_letter: str = "") -> tuple[list[str], int]:
    """Render one exercise card.

    Default height 54px. If card_height_override is set (typically 70 for
    3-detail cards, 86 for cards with two subtitle lines), use that and
    add a third detail slot at +60.

    section_letter is prepended to the exercise number in the SVG comment
    (e.g. "B" + "3" -> "B3 — DB RDL").
    """
    h = ex.card_height_override if ex.card_height_override else CARD_HEIGHT
    c = color(ex.muscle_key)

    # Build card comment: "{letter}{number} — {label}"
    label = ex.comment_label if ex.comment_label else _short_title(ex.title)
    prefix = f"{section_letter}{ex.number}" if section_letter else ex.number
    card_comment = f"{prefix} — {label}" if label else prefix

    out = [
        _comment(card_comment),
        _rect(CONTENT_X, y, STRIPE_WIDTH, h, 2, c.stripe),
        _rect(CONTENT_X + STRIPE_WIDTH, y, CONTENT_WIDTH - STRIPE_WIDTH, h,
              4, c.card_fill, c.card_stroke),
        _text(CARD_NUM_X, y + 16, ex.number,
              size=11, weight=500, fill=NUMBER_FILL),
        _text(CARD_TEXT_X, y + 16, ex.title,
              size=12, weight=500, fill=c.title_fill),
    ]

    # Detail line slots (text positions are independent of card height —
    # only the bottom padding shrinks/grows with h):
    #   - h=54, no subtitle: detail0 at +31, detail1 at +46
    #   - h=54, subtitle:    subtitle at +31, detail0 at +46 (only 1 detail fits)
    #   - h=70, no subtitle: detail0 at +31, detail1 at +46, detail2 at +60
    #   - h=70, subtitle:    subtitle at +31, detail0 at +46, detail1 at +60
    #   - h=86, subtitle+sub2: subtitle at +31, sub2 at +46, detail0 at +60, detail1 at +75
    if ex.subtitle_line:
        out.append(_text(CARD_TEXT_X, y + 31, ex.subtitle_line,
                         size=12, weight=500, fill=c.title_fill))
        if ex.subtitle_line_2:
            out.append(_text(CARD_TEXT_X, y + 46, ex.subtitle_line_2,
                             size=12, weight=500, fill=c.title_fill))
            detail_offsets = [60, 75] if h >= 86 else [60]
        else:
            detail_offsets = [46, 60] if h >= 70 else [46]
    else:
        detail_offsets = [31, 46, 60] if h >= 70 else [31, 46]

    for line, dy_off in zip(ex.detail_lines, detail_offsets):
        out.append(_text(CARD_TEXT_X, y + dy_off, line,
                         size=11, fill=c.detail_fill))

    if ex.sets_reps:
        out.append(_text(CARD_RIGHT_X, y + 16, ex.sets_reps,
                         size=12, weight=500, fill=c.title_fill))
    if ex.equipment:
        out.append(_text(CARD_RIGHT_X, y + 31, ex.equipment,
                         size=11, fill=c.detail_fill))
    if ex.equipment_extra:
        out.append(_text(CARD_RIGHT_X, y + 45, ex.equipment_extra,
                         size=11, fill=c.detail_fill))
    return out, y + h + CARD_GAP


def _render_pair_label(y: int) -> tuple[list[str], int]:
    """Pair label '↕ then immediately' — size 12.

    Wrapped in blank lines for visual separation from cards above/below.
    """
    out = [
        "",
        _text(PAGE_WIDTH // 2, y + 14, "↕ then immediately",
              size=12, fill=PAIR_LABEL_FILL, anchor="middle"),
        "",
    ]
    return out, y + PAIR_LABEL_HEIGHT


def _render_section(sec: Section, y: int) -> tuple[list[str], int]:
    out, y = _render_section_header(sec, y)
    items = sec.items
    for idx, item in enumerate(items):
        if isinstance(item, Pair):
            lines, y = _render_exercise(item.a, y, section_letter=_section_letter(sec.header))
            out.extend(lines)
            y -= CARD_GAP
            lines, y = _render_pair_label(y)
            out.extend(lines)
            lines, y = _render_exercise(item.b, y, section_letter=_section_letter(sec.header))
            out.extend(lines)
        else:  # Exercise
            lines, y = _render_exercise(item, y, section_letter=_section_letter(sec.header))
            out.extend(lines)
        # Blank line between items within a section (but not after the last)
        if idx < len(items) - 1:
            out.append("")
    y = y - CARD_GAP + SECTION_GAP
    return out, y


def _render_rules(box: RulesBox, y: int) -> tuple[list[str], int]:
    """Rules box — 20px bullet spacing, 22px title pad."""
    n = len(box.bullets)
    first_rect_offset = RULES_TOP_PAD + RULES_FIRST_BULLET_OFFSET  # 32
    h = (first_rect_offset
         + (n - 1) * RULES_LINE_HEIGHT
         + RULES_LAST_BULLET_BOTTOM_PAD)
    out = [
        _comment("GLOBAL RULES"),
        _rect(CONTENT_X, y, CONTENT_WIDTH, h, 6, NEUTRAL_BG, NEUTRAL_STROKE),
        _text(TEXT_PAD_X, y + RULES_TOP_PAD, box.title,
              size=12, weight=500, fill=TITLE_FILL),
    ]
    by = y + first_rect_offset
    for bullet in box.bullets:
        out.append(_rect(TEXT_PAD_X, by, 7, 7, 1, RULE_BULLET_FILL))
        out.append(_text(TEXT_PAD_X + 14, by + 8, bullet,
                         size=11, fill=RULE_TEXT_FILL))
        by += RULES_LINE_HEIGHT
    return out, y + h + BLOCK_GAP


def _render_timing(box: InfoBox, y: int) -> tuple[list[str], int]:
    """Timing summary — base 60px (for 2 body lines) + half-line bottom pad."""
    n = len(box.body_lines)
    extra_lines = max(0, n - 2)
    h = TIMING_HEIGHT_BASE + extra_lines * TIMING_LINE_HEIGHT + TIMING_BOX_EXTRA
    out = [
        _comment("TIMING SUMMARY"),
        _rect(CONTENT_X, y, CONTENT_WIDTH, h, 8, INFO_BG, INFO_STROKE, sw=1),
        _text(TEXT_PAD_X, y + TIMING_TITLE_OFFSET, box.title,
              size=12, weight=500, fill=INFO_TITLE_FILL),
    ]
    for i, line in enumerate(box.body_lines):
        out.append(_text(TEXT_PAD_X,
                         y + TIMING_BODY_FIRST_OFFSET + i * TIMING_LINE_HEIGHT,
                         line, size=11, fill=INFO_BODY_FILL))
    return out, y + h + BLOCK_GAP


def _render_setcount(box: SetCountBox, y: int) -> tuple[list[str], int]:
    """Set count box — supports up to 3-column layout via the entry.column field.

    Entries with column == 0 render in the left column starting at TEXT_PAD_X.
    Entries with column == 1 render in the middle column at SETCOUNT_COL2_X.
    Entries with column == 2 render in the right column at SETCOUNT_COL3_X.
    Within each column, entries appear in input order at SETCOUNT_LINE_HEIGHT
    intervals. Box height is sized to the tallest column.

    For 3-column use, prefer short entries in column 2 (right) since the
    column starts at x=530 and content right edge is x=650 — only ~120px
    of horizontal room before overflow.
    """
    col0 = [e for e in box.entries if e.column == 0]
    col1 = [e for e in box.entries if e.column == 1]
    col2 = [e for e in box.entries if e.column == 2]
    rows_used = max(len(col0), len(col1), len(col2), 1)
    h = (SETCOUNT_FIRST_OFFSET
         + (rows_used - 1) * SETCOUNT_LINE_HEIGHT + SETCOUNT_BOTTOM_PAD)
    out = [
        _comment("SET COUNT"),
        _rect(CONTENT_X, y, CONTENT_WIDTH, h, 6, NEUTRAL_BG, NEUTRAL_STROKE),
        _text(TEXT_PAD_X, y + SETCOUNT_TITLE_OFFSET, box.title,
              size=12, weight=500, fill=TITLE_FILL),
    ]
    for i, entry in enumerate(col0):
        c = color(entry.muscle_key)
        out.append(_text(
            TEXT_PAD_X,
            y + SETCOUNT_FIRST_OFFSET + i * SETCOUNT_LINE_HEIGHT,
            entry.text, size=11, fill=c.stripe,
        ))
    for i, entry in enumerate(col1):
        c = color(entry.muscle_key)
        out.append(_text(
            SETCOUNT_COL2_X,
            y + SETCOUNT_FIRST_OFFSET + i * SETCOUNT_LINE_HEIGHT,
            entry.text, size=11, fill=c.stripe,
        ))
    for i, entry in enumerate(col2):
        c = color(entry.muscle_key)
        out.append(_text(
            SETCOUNT_COL3_X,
            y + SETCOUNT_FIRST_OFFSET + i * SETCOUNT_LINE_HEIGHT,
            entry.text, size=11, fill=c.stripe,
        ))
    return out, y + h + BLOCK_GAP


def _render_alternatives(table: AlternativesTable, y: int) -> tuple[list[str], int]:
    n = len(table.rows)
    h = (TABLE_FIRST_ROW_OFFSET
         + (n - 1) * TABLE_ROW_HEIGHT + TABLE_BOTTOM_PAD)
    out = [
        _comment("ALTERNATIVES TABLE"),
        _rect(CONTENT_X, y, CONTENT_WIDTH, h, 6, NEUTRAL_BG, NEUTRAL_STROKE),
        _text(TEXT_PAD_X, y + TABLE_TITLE_OFFSET, table.title,
              size=12, weight=500, fill=TITLE_FILL),
        f'<line x1="40" y1="{y + TABLE_DIVIDER_TOP}" '
        f'x2="640" y2="{y + TABLE_DIVIDER_TOP}" '
        f'stroke="{TABLE_DIVIDER}" stroke-width="0.5"/>',
        _text(TEXT_PAD_X, y + TABLE_HEADER_OFFSET, "#  Primary exercise",
              size=10, weight=500, fill=TABLE_HEADER_FILL),
        _text(280, y + TABLE_HEADER_OFFSET, "Alternative 1",
              size=10, weight=500, fill=TABLE_HEADER_FILL),
        _text(470, y + TABLE_HEADER_OFFSET, "Alternative 2",
              size=10, weight=500, fill=TABLE_HEADER_FILL),
        f'<line x1="40" y1="{y + TABLE_DIVIDER_BOTTOM}" '
        f'x2="640" y2="{y + TABLE_DIVIDER_BOTTOM}" '
        f'stroke="{TABLE_DIVIDER}" stroke-width="0.5"/>',
    ]
    ry = y + TABLE_FIRST_ROW_OFFSET
    for idx, row in enumerate(table.rows):
        c = color(row.primary_muscle_key)
        num_label = f"{row.number}{'  ' if len(row.number) < 2 else ' '}{row.primary}"
        if idx > 0:
            out.append("")  # blank line between rows for easy hand-editing
        out.append(_text(TEXT_PAD_X, ry, num_label, size=10, fill=c.stripe))
        out.append(_text(280, ry, row.alt1, size=10, fill=TABLE_CELL_FILL))
        out.append(_text(470, ry, row.alt2, size=10, fill=TABLE_CELL_FILL))
        ry += TABLE_ROW_HEIGHT
    return out, y + h + BLOCK_GAP


def _render_version_note(text: str, y: int) -> tuple[list[str], int]:
    out = [
        _comment("VERSION NOTE"),
        _text(PAGE_WIDTH // 2, y + 8, text,
              size=9, fill=VERSION_NOTE_FILL, anchor="middle"),
    ]
    return out, y + 30


# ─── Public entry point ────────────────────────────────────────────────────

def render(routine: Routine) -> str:
    """Render a Routine to an SVG document string.

    Output is structured for human readability:
      - Each major block (legend, info box, section, card, summary box)
        is preceded by an `<!-- LABEL -->` comment.
      - Blank lines separate blocks.
      - Sections include a top-level comment; cards within a section
        get their own letter+number label (e.g. `<!-- B3 — DB RDL -->`).

    This makes the generated SVG straightforward to navigate and
    hand-edit when needed (e.g. tweaking a single coordinate value).
    """
    body = []
    body.extend(_render_header(routine.title, routine.subtitle))
    body.append("")  # blank line after header

    y = LEGEND_TOP
    lines, y = _render_legend(routine.legend_muscles, y)
    body.extend(lines)
    body.append("")

    if routine.pre_workout:
        lines, y = _render_info_box(routine.pre_workout, y,
                                    comment="PRE-WORKOUT NOTE")
        body.extend(lines)
        body.append("")

    for sec in routine.sections:
        lines, y = _render_section(sec, y)
        body.extend(lines)
        body.append("")  # blank line between sections

    if routine.sections:
        y = y - SECTION_GAP + BLOCK_GAP

    if routine.post_workout:
        lines, y = _render_info_box(routine.post_workout, y,
                                    comment="POST-WORKOUT NOTE")
        body.extend(lines)
        body.append("")

    if routine.rules:
        lines, y = _render_rules(routine.rules, y)
        body.extend(lines)
        body.append("")

    if routine.timing:
        lines, y = _render_timing(routine.timing, y)
        body.extend(lines)
        body.append("")

    if routine.set_count:
        lines, y = _render_setcount(routine.set_count, y)
        body.extend(lines)
        body.append("")

    if routine.alternatives:
        lines, y = _render_alternatives(routine.alternatives, y)
        body.extend(lines)
        body.append("")

    if routine.version_note:
        lines, y = _render_version_note(routine.version_note, y)
        body.extend(lines)

    total_height = y + 10
    header = (
        f'<svg width="100%" viewBox="0 0 {PAGE_WIDTH} {total_height}" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'style="font-family: sans-serif;">'
    )
    # Strip any trailing blank lines so the closing </svg> sits cleanly.
    while body and body[-1] == "":
        body.pop()
    return "\n".join([header, "", *body, "", "</svg>"])
