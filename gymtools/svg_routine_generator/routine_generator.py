"""
routine_generator.py — single-file SVG generator for fitness routines.

Self-contained version of the svg_routine_generator package. Drop this file
anywhere on the Python path and import from it directly:

    from routine_generator import (
        Routine, Section, Exercise, Pair, InfoBox, RulesBox,
        SetCountBox, SetCountEntry, AlternativesTable, AltRow, render,
    )

    routine = Routine(...)
    svg = render(routine)

Style baseline: routine_lowerbody.svg (the newer, more polished design).
  - Section headers: neutral gray bg, dark text, left-aligned (matches the
    upper body source — neutral style, no warmup/working distinction)
  - All exercise cards uniform 54px tall (use card_height_override=70 for
    cards with 3 detail lines, or 86 for cards with 2 subtitle lines)
  - Glutes color: dark green (matches Shoulder/cuff)

Output is structured for human readability:
  - Each major block (legend, info box, section, card, summary box) is
    preceded by an `<!-- LABEL -->` comment.
  - Blank lines separate blocks.
  - Cards within sections get letter+number labels (e.g. `<!-- B3 — DB RDL -->`).

This makes the generated SVG easy to navigate and hand-edit.

Two earlier user-requested adjustments are still applied:
  - Legend box uses a 2-line layout: header line, then swatches (LEGEND_HEIGHT = 56)
  - Timing summary box gains half a line of bottom padding (TIMING_BOX_EXTRA = 7)

Both adjustments revertible via constants in this file.

Running this module directly renders the upper-body example to stdout.
"""
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# THEME — colors, dimensions, layout constants
# ═══════════════════════════════════════════════════════════════════════════
# ─── Page / canvas ─────────────────────────────────────────────────────────
PAGE_WIDTH = 680
CONTENT_X = 30          # all boxes start here
CONTENT_WIDTH = 620     # all boxes are this wide
TEXT_PAD_X = 50         # left padding inside boxes for text
STRIPE_WIDTH = 8        # colored left stripe on exercise cards
CARD_TEXT_X = 72        # text x inside exercise card (after stripe + small gap)
CARD_NUM_X = 54         # exercise number x
CARD_RIGHT_X = 490      # right-column (sets/equipment) x

# ─── Vertical rhythm ───────────────────────────────────────────────────────
TOP_MARGIN = 28              # title baseline
SUBTITLE_OFFSET = 16         # subtitle baseline relative to title
LEGEND_TOP = 54
SECTION_HEADER_HEIGHT = 24   # gray header style (matches upper body source)
CARD_HEIGHT = 54             # uniform card height (was 60; reduced by 6px to tighten bottom padding)
CARD_GAP = 6                 # vertical gap between adjacent cards
SECTION_GAP = 14             # gap before a new section header
BLOCK_GAP = 12               # gap between major blocks (rules, timing, etc.)
PAIR_LABEL_HEIGHT = 24       # space taken by "↕ then immediately"

# Card heights are uniform now — the old derive-from-content rules are gone.


# ─── Colors ────────────────────────────────────────────────────────────────
# Neutrals
NEUTRAL_BG = "#f7f7f7"
NEUTRAL_STROKE = "#ccc"
TITLE_FILL = "#1a1a1a"
SUBTITLE_FILL = "#666"
NUMBER_FILL = "#555"
PAIR_LABEL_FILL = "#888"
RULE_TEXT_FILL = "#444"
RULE_BULLET_FILL = "#e8a020"
TABLE_HEADER_FILL = "#666"
TABLE_DIVIDER = "#ccc"
TABLE_CELL_FILL = "#444"
VERSION_NOTE_FILL = "#aaa"

# Section header — neutral gray with dark text (matches upper body source).
# A single style is used for all sections; the warmup/working distinction
# from the lower-body design has been retired.
SECTION_HEADER_BG = "#e8e8e8"
SECTION_HEADER_STROKE = "#bbb"
SECTION_HEADER_TEXT_FILL = TITLE_FILL    # dark text, not white

# Blue info-box (pre/post workout, timing summary)
INFO_BG = "#e8f4fd"
INFO_STROKE = "#5aabf0"
INFO_TITLE_FILL = "#1a5c8a"
INFO_BODY_FILL = "#2272a8"


@dataclass(frozen=True)
class MuscleColor:
    """Color set for one muscle group / card type."""
    key: str           # short id, e.g. "chest"
    label: str         # display label for legend, e.g. "Chest"
    stripe: str        # left stripe + dark accents
    card_fill: str     # card background
    card_stroke: str   # card border
    title_fill: str    # exercise title text
    detail_fill: str   # detail / muscle text


# Palette extracted from routine_upperbody.svg.
# Add new entries here when introducing a new muscle group / card type.
MUSCLE_COLORS = {
    "shoulder":   MuscleColor("shoulder",   "Shoulder / rotator cuff",
                              "#085041", "#e1f5ee", "#0f6e56", "#085041", "#0f6e56"),
    "medial_delt": MuscleColor("medial_delt", "Medial delt",
                              "#085041", "#e1f5ee", "#0f6e56", "#085041", "#0f6e56"),
    "post_delt":  MuscleColor("post_delt",  "Posterior delt",
                              "#085041", "#e1f5ee", "#0f6e56", "#085041", "#0f6e56"),
    "chest":      MuscleColor("chest",      "Chest",
                              "#26215c", "#eeedfe", "#534ab7", "#26215c", "#3c3489"),
    "back":       MuscleColor("back",       "Back",
                              "#633806", "#faeeda", "#854f0b", "#412402", "#633806"),
    "biceps":     MuscleColor("biceps",     "Biceps",
                              "#042c53", "#ddeeff", "#185fa5", "#042c53", "#0c447c"),
    "triceps":    MuscleColor("triceps",    "Triceps",
                              "#185fa5", "#e6f1fb", "#378add", "#042c53", "#185fa5"),
    # ─── Lower body palette (matches routine_lowerbody.pdf legend) ─────────
    "quads":      MuscleColor("quads",      "Quads",
                              "#26215c", "#eeedfe", "#534ab7", "#26215c", "#3c3489"),
    "hamstrings": MuscleColor("hamstrings", "Hamstrings",
                              "#633806", "#faeeda", "#854f0b", "#412402", "#633806"),
    "glutes":     MuscleColor("glutes",     "Glutes",
                              "#085041", "#e1f5ee", "#0f6e56", "#085041", "#0f6e56"),
    "calves":     MuscleColor("calves",     "Calves",
                              "#185fa5", "#e6f1fb", "#378add", "#042c53", "#185fa5"),
}


def color(key: str) -> MuscleColor:
    if key not in MUSCLE_COLORS:
        raise KeyError(
            f"Unknown muscle group '{key}'. Known: {sorted(MUSCLE_COLORS)}"
        )
    return MUSCLE_COLORS[key]


# ═══════════════════════════════════════════════════════════════════════════
# MODEL — dataclasses describing a routine
# ═══════════════════════════════════════════════════════════════════════════
@dataclass
class Exercise:
    """One exercise card.

    Default card height is 54px. Set `card_height_override=70` for cards
    needing a third detail line, or `=86` for cards with two subtitle
    cue lines plus detail lines.

    Title is the main header. `subtitle_line` adds a parenthetical cue
    line below the title (consumes the first detail-line slot).

    The right column shows sets x reps and equipment.

    `comment_label` is an optional short label for the SVG comment
    preceding this card — e.g. "DB RDL" produces `<!-- B3 — DB RDL -->`.
    If omitted, a comment is auto-derived from the first few words of the
    title.
    """
    number: str               # "1", "8a", "8b" — string so split sets work
    muscle_key: str           # key into theme.MUSCLE_COLORS
    title: str
    subtitle_line: Optional[str] = None  # parenthetical cue line
    subtitle_line_2: Optional[str] = None  # optional 2nd cue line (requires card_height_override=86)
    detail_lines: list[str] = field(default_factory=list)  # 1–2 (or 3 with override=70)

    sets_reps: str = ""       # "3 × 8–10"
    equipment: str = ""       # "Cable · 3s ecc"
    equipment_extra: Optional[str] = None  # second equipment line if needed

    card_height_override: Optional[int] = None  # default 54; use 70 for 3-detail cards or 86 for 2-subtitle cards
    comment_label: Optional[str] = None  # short label for SVG comment


@dataclass
class Pair:
    """A superset pair: two Exercises connected by '↕ then immediately'."""
    a: Exercise
    b: Exercise


@dataclass
class Section:
    """A labeled section with a gray header and a list of items.

    items: list of Exercise (straight set) or Pair (superset).
    style: deprecated — kept for backward compatibility. All sections
           now render with the same neutral gray header. Field is ignored.
    comment_label: optional override for the SVG comment preceding the
                   section, e.g. "E SHOULDER DETAIL". If omitted, the
                   comment is auto-derived from the header (letter +
                   pre-colon text, uppercased), e.g. "B SUPERSET 1".
                   The comment is wrapped as ``<!-- ── LABEL ── -->``.
    """
    header: str               # "A — Warmup  (~3 min · straight sets)"
    items: list                # list[Exercise | Pair]
    style: Optional[str] = None  # deprecated; ignored
    comment_label: Optional[str] = None

    def resolved_style(self) -> str:
        # Retained for any callers that may invoke it; always returns
        # "default" now that warmup/working distinction is gone.
        return "default"


@dataclass
class InfoBox:
    """Blue info box (pre/post workout, session timing)."""
    title: str
    body_lines: list[str]


@dataclass
class RulesBox:
    title: str
    bullets: list[str]


@dataclass
class SetCountEntry:
    """One line in the working-set-count box, colored by muscle group."""
    muscle_key: str
    text: str          # "Chest: 5 sets (bench press 3 + chest fly 2)"
    column: int = 0    # 0 = left, 1 = middle, 2 = right (3-column layout)


@dataclass
class SetCountBox:
    title: str
    entries: list[SetCountEntry]


@dataclass
class AltRow:
    number: str
    primary: str
    primary_muscle_key: str   # for color of primary cell
    alt1: str
    alt2: str


@dataclass
class AlternativesTable:
    title: str
    rows: list[AltRow]


@dataclass
class Routine:
    title: str
    subtitle: str
    legend_muscles: list[str]    # ordered keys into MUSCLE_COLORS

    pre_workout: Optional[InfoBox] = None
    sections: list[Section] = field(default_factory=list)
    post_workout: Optional[InfoBox] = None

    rules: Optional[RulesBox] = None
    timing: Optional[InfoBox] = None
    set_count: Optional[SetCountBox] = None
    alternatives: Optional[AlternativesTable] = None
    version_note: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# RENDERER — converts Routine model into SVG string
# ═══════════════════════════════════════════════════════════════════════════
"""
SVG renderer for Routine models — lower-body-style baseline.

Layout is computed top-to-bottom, tracking a running `y` cursor. Each
component knows its own height. Cards are uniform 54px tall by default.

Card layout (h=54, text positions independent of card height):
  - title at +16
  - subtitle at +31 (when present, takes detail0 slot — only 1 detail line then fits)
  - detail0 at +31
  - detail1 at +46
  - right column: sets/reps at +16, equipment at +31

Section header style:
  - Neutral gray bg, dark text, left-aligned at TEXT_PAD_X
  - Matches the upper body source SVG (no warmup/working distinction)
  - Section.comment_label can override the auto-derived SVG comment label
"""


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


# ═══════════════════════════════════════════════════════════════════════════
# SELF-TEST — running this file directly renders the upper-body example
# ═══════════════════════════════════════════════════════════════════════════

def _build_upperbody_example() -> Routine:
    """Reference example. Mirror this structure when authoring new routines."""
    return Routine(
        title="Full upper body routine — final",
        subtitle="Archery + hypertrophy · hypermobility-safe · ~50.5 min · 18 working sets",
        legend_muscles=["shoulder", "chest", "back", "biceps", "triceps"],

        pre_workout=InfoBox(
            title="30–60 min before: collagen peptides (10–15g) + vitamin C",
            body_lines=["Maximizes collagen synthesis in tendons loaded during session"],
        ),

        sections=[
            Section(
                header="A — Warmup  (~3 min · straight sets)",
                items=[
                    Exercise(
                        number="1", muscle_key="shoulder",
                        title="Band pull-aparts (stop 10° short of full extension)",
                        detail_lines=[
                            "Posterior delt · rhomboids",
                            "Shoulder / rotator cuff",
                        ],
                        sets_reps="1 × 15", equipment="Band",
                    ),
                    Exercise(
                        number="2", muscle_key="back",
                        title="Wide grip seated row (elbows flare wide)",
                        detail_lines=[
                            "Posterior delt · upper back · lats",
                            "Back + shoulder · light warmup weight",
                        ],
                        sets_reps="1 × 12", equipment="Cable",
                    ),
                ],
            ),
            Section(
                header="B — Superset 1: Chest + Back  (~9.5 min · 3 rounds · 90s rest after each pair)",
                items=[
                    Pair(
                        a=Exercise(
                            number="3", muscle_key="chest",
                            title="Smith machine flat bench press (soft elbow lockout)",
                            detail_lines=[
                                "Pec major · anterior delt · triceps",
                                "Chest",
                            ],
                            sets_reps="3 × 6–8", equipment="Smith",
                        ),
                        b=Exercise(
                            number="4", muscle_key="back",
                            title="Narrow grip seated cable row (no forward lean on eccentric)",
                            detail_lines=[
                                "Mid-trap · rhomboids · lats · posterior delt",
                                "Back · archery draw power",
                            ],
                            sets_reps="3 × 8–10", equipment="Cable · 3s ecc",
                        ),
                    ),
                ],
            ),
            Section(
                header="C — Superset 2: Back + Chest  (~8 min · 2 rounds · 90s rest after each pair)",
                items=[
                    Pair(
                        a=Exercise(
                            number="5", muscle_key="back",
                            title="Lat pulldown — stretch at top",
                            subtitle_line="(let shoulder elevate at top · pull to upper chest · soft elbow)",
                            detail_lines=[
                                "Lats (upper/stretched portion) · teres major · rhomboids · biceps (synergist)",
                                "Back · lengthened-biased · matches badminton smash setup",
                            ],
                            sets_reps="2 × 10–12", equipment="Cable · 3s ecc",
                        ),
                        b=Exercise(
                            number="6", muscle_key="chest",
                            title="Dumbbell chest fly (flat bench)",
                            subtitle_line="(light weight · slight bend in elbows throughout)",
                            detail_lines=[
                                "Pec major stretch — antagonist balance for archery draw",
                            ],
                            sets_reps="2 × 12–15", equipment="DB · flat bench",
                        ),
                    ),
                ],
            ),
            Section(
                header="D — Superset 3: Biceps + Triceps  (~4.5 min · 2 rounds · 60s rest after each pair)",
                items=[
                    Pair(
                        a=Exercise(
                            number="7", muscle_key="biceps",
                            title="Preacher curl (arm supported on pad)",
                            subtitle_line="(15–20° elbow bend at bottom · never full extension)",
                            detail_lines=[
                                "Biceps brachii · brachialis · lengthened-biased at elbow (shoulder-flexed = not fully biarticular)",
                                "Biceps · shoulder-safe alternative to incline DB curl",
                            ],
                            sets_reps="2 × 10–12", equipment="EZ-bar / DB",
                        ),
                        b=Exercise(
                            number="8", muscle_key="triceps",
                            title="Triceps split — alternate across the 2 rounds",
                            detail_lines=[
                                "R1: Cable pushdown (lateral/medial heads · shortened bias) — 1 × 12–15",
                                "R2: Overhead cable extension (long head · lengthened bias) — 1 × 10–12",
                                "Triceps · regional coverage · overhead = badminton smash carryover",
                            ],
                            sets_reps="2 sets total", equipment="Cable · soft lockout",
                            card_height_override=70,
                        ),
                    ),
                ],
            ),
            Section(
                header="E — Superset 4: Lateral raise + External rotation  (~3.5 min · 2 rounds · 60s rest after each pair)",
                items=[
                    Pair(
                        a=Exercise(
                            number="9", muscle_key="shoulder",
                            title="Dumbbell lateral raise",
                            subtitle_line="(both arms simultaneously · cap at 80° — below shoulder height)",
                            detail_lines=[
                                "Medial delt",
                                "Shoulder / rotator cuff",
                            ],
                            sets_reps="2 × 15", equipment="DB",
                        ),
                        b=Exercise(
                            number="10", muscle_key="shoulder",
                            title="Cable external rotation",
                            subtitle_line="(non-negotiable for hypermobility · very light load)",
                            detail_lines=[
                                "Infraspinatus · teres minor",
                                "Shoulder / rotator cuff · light load protects cuff from lateral raise supraspinatus fatigue",
                            ],
                            sets_reps="2 × 15–20", equipment="Cable",
                        ),
                    ),
                ],
            ),
        ],

        post_workout=InfoBox(
            title="Within 60 min after: protein 30–40g + vitamin C",
            body_lines=["Supports muscle + tendon remodeling · aim 1.6–2g protein/kg/day total"],
        ),

        rules=RulesBox(
            title="Every rep, every set — hypermobility rules",
            bullets=[
                "Never lock out elbows or wrists — always keep a soft bend at end range",
                "3 sec eccentric on all pulling movements — control the return",
                "Skip session if joints feel unusually loose that day — reschedule, don't push",
                "Stop set early if any joint feels unstable — prioritize joint feel over rep count",
                "Hip abductor/adductor machine: deferred until knee is stable",
            ],
        ),

        timing=InfoBox(
            title="Session timeline",
            body_lines=[
                "Warmup A (3 min) → Superset B (9.5 min) → Superset C (8 min) → Superset D (4.5 min) → Superset E (3.5 min)",
                "Total working session: ~50.5 min · 18 working sets · then proceed to post-workout mobility protocol",
            ],
        ),

        set_count=SetCountBox(
            title="Working set count by muscle group",
            entries=[
                SetCountEntry("chest",    "Chest: 5 sets (bench press 3 + chest fly 2)", column=0),
                SetCountEntry("back",     "Back: 5 sets (cable row 3 + lat pulldown 2)", column=0),
                SetCountEntry("biceps",   "Biceps: 2 sets",                              column=1),
                SetCountEntry("triceps",  "Triceps: 2 sets",                             column=1),
                SetCountEntry("shoulder", "Shoulder / cuff: 4 sets",                     column=1),
            ],
        ),

        alternatives=AlternativesTable(
            title="Alternative exercises — if equipment occupied or unavailable",
            rows=[
                AltRow("1",  "Band pull-aparts",            "shoulder", "Prone Y-raise on bench",        "Scapular wall slides"),
                AltRow("2",  "Wide grip seated row (warmup)","back",    "Band face pulls",               "Band pull-apart at chest"),
                AltRow("3",  "Smith flat bench press",      "chest",    "DB flat bench press",           "Push-ups (feet elevated)"),
                AltRow("4",  "Narrow grip cable row",       "back",     "Chest-supported DB row",        "T-bar row"),
                AltRow("5",  "Lat pulldown (stretch top)",  "back",     "Straight-arm cable pullover",   "DB pullover on bench"),
                AltRow("6",  "DB chest fly",                "chest",    "Cable crossover (low to high)", "Pec deck machine"),
                AltRow("7",  "Preacher curl",               "biceps",   "Spider curl (face down incline)","Incline DB curl ⚠ shoulder"),
                AltRow("8a", "Cable pushdown (R1)",         "triceps",  "DB kickback",                   "Diamond push-ups"),
                AltRow("8b", "Overhead cable ext. (R2)",    "triceps",  "Skull crusher to forehead",     "Single-arm overhead DB ext."),
                AltRow("9",  "DB lateral raise",            "shoulder", "Cable lateral raise",           "Leaning lateral raise (DB)"),
                AltRow("10", "Cable external rotation",     "shoulder", "Band external rotation",        "Side-lying DB ext. rotation"),
            ],
        ),

        version_note=(
            "v5 — EMG-verified labels · lat pulldown (biceps synergist) · "
            "preacher curl (elbow lengthened) · cuff fatigue cue added"
        ),
    )


if __name__ == "__main__":
    import sys
    sys.stdout.write(render(_build_upperbody_example()))
