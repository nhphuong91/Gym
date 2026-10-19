"""
Theme — single source of truth for colors, fonts, and layout constants.

Section header style: neutral gray bg, dark text, left-aligned. Matches
the upper body source SVG.
"""
from dataclasses import dataclass


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
