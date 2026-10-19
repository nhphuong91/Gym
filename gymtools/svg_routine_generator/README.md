# SVG Routine Generator

Reusable system for producing fitness-routine SVGs that match the style of
your hand-authored upper/lower body source files.

## Layout

```
svg_routine_generator/
├── __init__.py          # re-exports the public API
├── theme.py             # colors, dimensions, layout constants
├── model.py             # dataclasses: Routine, Section, Exercise, Pair, ...
├── svg_render.py        # render(routine) -> SVG string
├── upperbody.py         # example: an older upper-body routine (data-format reference)
├── lowerbody.py         # example: an older lower-body routine (data-format reference)
├── routine_generator.py # single-file bundle of the modules above
└── README.md
```

A single-file bundled equivalent (`routine_generator.py`) is also provided
for projects where copying one file is easier than maintaining a package.
The bundle and package produce byte-for-byte identical output.

## Quick start

```python
from svg_routine_generator import (
    Routine, Section, Exercise, Pair, InfoBox, RulesBox,
    SetCountBox, SetCountEntry, AlternativesTable, AltRow, render,
)

routine = Routine(
    title="My routine",
    subtitle="hypermobility-safe · ~50 min",
    legend_muscles=["chest", "back", "shoulder"],
    pre_workout=InfoBox(title="Before", body_lines=["..."]),
    sections=[
        Section(header="A — Warmup  (~3 min · straight sets)", items=[
            Exercise(number="1", muscle_key="shoulder",
                     title="Band pull-aparts",
                     detail_lines=["Posterior delt", "Shoulder"],
                     sets_reps="1 × 15", equipment="Band"),
        ]),
        Section(header="B — Superset", items=[
            Pair(
                a=Exercise(number="2", muscle_key="chest", ...),
                b=Exercise(number="3", muscle_key="back", ...),
            ),
        ]),
    ],
    # post_workout, rules, timing, set_count, alternatives, version_note...
)

svg = render(routine)
open("out.svg", "w").write(svg)
```

## Section headers

All sections render with the same neutral gray header (matches the upper
body source SVG): `#e8e8e8` background, dark text, left-aligned at
`TEXT_PAD_X`, height 24px, rounded corners with rx=4.

The corresponding SVG comment is wrapped as `<!-- ── LABEL ── -->`. The
label is auto-derived from the section header (letter + pre-colon text,
uppercased — e.g., "B — Superset 1: Hinge + Quad iso (~8 min · …)" → `── B
SUPERSET 1 ──`). To override, set `comment_label` on the Section:

```python
Section(
    header="E — Superset 4: Lateral raise + External rotation (~3.5 min ...)",
    comment_label="E SHOULDER DETAIL",
    items=[...]
)
# emits <!-- ── E SHOULDER DETAIL ── -->
```

The deprecated `style` field on Section is ignored — kept only for
backward compatibility with older code.

## Card heights

Exercise cards default to **54px** tall. Three layout slots:

- **No subtitle** — title at +16, detail0 at +31, detail1 at +46
- **One subtitle** — title at +16, subtitle at +31, detail0 at +46
- **Two subtitles** — needs `card_height_override=86`. Title at +16,
  subtitle at +31, subtitle_line_2 at +46, detail0 at +60, detail1 at +75
- **Three detail lines, no subtitle** — set `card_height_override=70`. Title at
  +16, detail0 at +31, detail1 at +46, detail2 at +60

Text positions are independent of card height — only the bottom padding
shrinks/grows with `h`. So `card_height_override=80` would give the
3-detail layout with extra bottom whitespace; the layout slots are
selected by passing the threshold (>= 70 for 3-detail, >= 86 for two
subtitles).

Use `subtitle_line_2` (with `card_height_override=86`) when you need two
parenthetical cue lines below the title:

```python
Exercise(
    title="Long exercise name",
    subtitle_line="(first cue line · constraint or setup info)",
    subtitle_line_2="(second cue line · safety reminder)",
    detail_lines=["Muscles", "Emphasis line"],
    card_height_override=86,
    ...
)
```

## Set count layout (1, 2, or 3 columns)

`SetCountBox` supports up to a 3-column layout via the `column` field on
`SetCountEntry`:

- `column=0` (default) — left column at `TEXT_PAD_X` (x=50)
- `column=1` — middle column at `SETCOUNT_COL2_X` (x=360)
- `column=2` — right column at `SETCOUNT_COL3_X` (x=530)

Within each column, entries appear in input order at 18px line spacing.
Box height is sized to the tallest column. If all entries use the
default `column=0`, the box renders as a single column.

For 3-column use, prefer short entries in column 2 (right) — the column
starts at x=530 and the content right edge is x=650, leaving only ~120px
before overflow.

```python
SetCountBox(
    title="Working set count by muscle group",
    entries=[
        SetCountEntry("chest",   "Chest: 5 sets (bench 3 + fly 2)", column=0),
        SetCountEntry("back",    "Back: 5 sets (row 3 + pulldown 2)", column=0),
        SetCountEntry("biceps",  "Biceps: 2 sets",                  column=1),
        SetCountEntry("triceps", "Triceps: 2 sets",                 column=1),
        SetCountEntry("shoulder","Shoulder: 4 sets",                column=2),
    ],
)
```

## SVG comments and source-code readability

The generator emits SVG with comments and blank lines so the source is
navigable and hand-editable, mirroring your authoring conventions:

```xml
<!-- LEGEND -->
<rect ...
<text ...

<!-- PRE-WORKOUT NOTE -->
<rect ...

<!-- ── A WARMUP ── -->
<rect ...

<!-- A1 — Band pull-aparts -->
<rect ...
...

<!-- A2 — Wide grip seated row -->
...

<!-- ── B SUPERSET 1 ── -->
...
```

Card comments use `<!-- {section_letter}{number} — {label} -->`. The label
defaults to the first 40 chars of the title (parenthetical stripped). To
specify a shorter label, set `comment_label` on Exercise:

```python
Exercise(
    number="3", muscle_key="hamstrings",
    title="Dumbbell Romanian deadlift (bilateral · soft knee bend throughout)",
    comment_label="DB RDL",  # → <!-- B3 — DB RDL -->
    ...
)
```

The alternatives-table renders one blank line between rows for easier
hand-editing, regardless of whether you provide one in the data.

## Adding a new muscle group

Add a `MuscleColor` entry to `MUSCLE_COLORS` in `theme.py`:

```python
"new_group": MuscleColor("new_group", "Display Label",
                         stripe="#hex", card_fill="#hex",
                         card_stroke="#hex", title_fill="#hex",
                         detail_fill="#hex"),
```

Then reference it by key (`muscle_key="new_group"`) in any Exercise / AltRow.

## Adjustments applied vs source

Two visual changes baked into the generator (per earlier user requests):

1. **Legend box** uses a 2-line layout (LEGEND_HEIGHT = 56). Top line:
   "Muscle group" header. Bottom line: swatches + labels. The original
   single-line layout (header beside the swatches) is no longer used.
2. **Timing summary box** gains 7px of bottom padding (TIMING_BOX_EXTRA = 7)
   so the last line isn't cramped against the box border.

Both revertible via constants in `theme.py`:
- `LEGEND_HEIGHT` — affects vertical sizing of the legend box
- `TIMING_BOX_EXTRA = 0` — restore original timing box size

## Content-length constraints

The renderer doesn't auto-wrap text. Long content can overlap with
adjacent elements:

**Exercise title length.** The right-column (sets/equipment) starts at
x=490. A title past x≈480 will collide with the sets/reps text. Move the
parenthetical cue to `subtitle_line`:

```python
# Bad — title too long
Exercise(title="Standing calf raises (hold wall or rack for balance · controlled lowering)", ...)

# Good
Exercise(
    title="Standing calf raises",
    subtitle_line="(hold wall or rack for balance · controlled lowering)",
    ...
)
```

**Section header length.** Auto-shrinks from size 12 to size 11 when
needed. Very long headers shrink but won't overflow.

**Detail lines.** Extend across the full card width (x=72 to x≈640).
Lines >95 chars may run past the right column.

When in doubt, render and visually check — overflow is obvious.

## Color palette

| Muscle group | Stripe |
|---|---|
| `shoulder` / `medial_delt` / `post_delt` / `glutes` | `#085041` (dark green) |
| `chest` / `quads` | `#26215c` (purple) |
| `back` / `hamstrings` | `#633806` (brown) |
| `biceps` | `#042c53` (dark blue) |
| `triceps` / `calves` | `#185fa5` / `#042c53` |

Lower and upper body share hues by design. Don't render a mixed routine
where same-hue groups appear in the same legend.

## Testing changes

Run from inside `svg_routine_generator/`; `-B` keeps `__pycache__` out of the folder.

```bash
python3 -B upperbody.py > /tmp/upper.svg
python3 -B lowerbody.py > /tmp/lower.svg

# Verify bundle == package (the bundle's built-in example is the upper-body one)
python3 -B routine_generator.py > /tmp/bundle.svg
diff /tmp/bundle.svg /tmp/upper.svg
```
