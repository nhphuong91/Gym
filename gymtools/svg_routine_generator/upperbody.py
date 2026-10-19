"""
Rebuilds routine_upperbody.svg using the generator, applying the two
requested adjustments:
  1. Legend box height reduced by half a line
  2. Timing summary box gains half a line of bottom padding

This file doubles as the reference example for the data format.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from svg_routine_generator import (
    Routine, Section, Exercise, Pair, InfoBox, RulesBox,
    SetCountBox, SetCountEntry, AlternativesTable, AltRow, render,
)


routine = Routine(
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
    out = render(routine)
    sys.stdout.write(out)
