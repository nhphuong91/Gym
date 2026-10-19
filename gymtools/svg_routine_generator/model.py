"""
Data model for fitness routines.

A Routine is composed of:
- header (title + subtitle)
- legend (muscle groups present)
- optional pre-workout info box
- one or more Sections, each containing Cards (exercises) optionally paired as supersets
- optional post-workout info box
- rules box, timing summary, set count, alternatives table, version note

The renderer (svg_render.py) takes a Routine and produces SVG. All vertical
positions are computed at render time — never put y-coordinates in the data.
"""
from dataclasses import dataclass, field
from typing import Optional


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
