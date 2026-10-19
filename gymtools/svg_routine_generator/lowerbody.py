"""Lower body routine — knee rehab phase. Matches routine_lowerbody.svg."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from svg_routine_generator import (
    Routine, Section, Exercise, Pair, InfoBox, RulesBox,
    SetCountBox, SetCountEntry, render,
)


routine = Routine(
    title="Lower body routine — knee rehab phase",
    subtitle="Knee-sensitive · hypermobility-safe · clean antagonist pairing · 18 working sets · no single-leg eccentric loading",
    legend_muscles=["quads", "hamstrings", "glutes", "calves"],

    pre_workout=InfoBox(
        title="30–60 min before: collagen peptides (10–15g) + vitamin C",
        body_lines=["Supports tendon and cartilage loading during session"],
    ),

    sections=[
        Section(
            header="A — Warmup  (~3 min · straight sets)",
            items=[
                Exercise(number="1", muscle_key="glutes",
                         title="Glute stretch — lying windshield wiper",
                         detail_lines=[
                             "Glutes · hip external rotators",
                             "Move slowly, pain-free range only — wakes up hip rotators before loading",
                         ],
                         sets_reps="10–15 reps", equipment="Bodyweight"),
                Exercise(number="2", muscle_key="quads",
                         title="Banded leg extensions (seated on bench · 80% range)",
                         detail_lines=[
                             "Quadriceps · VMO — light warmup load",
                             "Band anchored behind · stop short of full extension · gets blood into quads and knee joint",
                         ],
                         sets_reps="2 × 15", equipment="Band · very light"),
            ],
        ),
        Section(
            header="B — Superset 1: Hinge + Quad iso  (~8 min · 3 rounds · 90s rest after each pair)",
            items=[Pair(
                a=Exercise(number="3", muscle_key="hamstrings",
                           title="Dumbbell Romanian deadlift (bilateral · soft knee bend throughout)",
                           detail_lines=[
                               "Hamstrings · glutes · erector spinae",
                               "Hip hinge pattern · DBs slide along thighs · stop at mid-shin · 3s eccentric lowering",
                           ],
                           sets_reps="3 × 10–12", equipment="DB · 3s ecc"),
                b=Exercise(number="4", muscle_key="quads",
                           title="Wall sit (isometric)",
                           detail_lines=[
                               "Quadriceps · VMO (glutes/hamstrings as isometric stabilizers only)",
                               "Start shallow · only deepen if pain-free · isometric = no concentric fatigue stacking with RDL",
                           ],
                           sets_reps="3 × 20s", equipment="Bodyweight"),
            )],
        ),
        Section(
            header="C — Superset 2: Hip extension + Knee extension  (~8 min · 3 rounds · 90s rest after each pair)",
            items=[Pair(
                a=Exercise(number="5", muscle_key="glutes",
                           title="Hip thrust (bench-supported)",
                           detail_lines=[
                               "Gluteus maximus · hamstrings",
                               "Stop just short of full hip extension · no hyperextension · drive through heels · squeeze at top",
                           ],
                           sets_reps="3 × 8–12", equipment="Bodyweight / DB"),
                b=Exercise(number="6", muscle_key="quads",
                           title="Sit-to-stand — box squat variation",
                           detail_lines=[
                               "Quadriceps (dominant) · glutes (synergist, modest)",
                               "Bench at 90° knee · bilateral · 3s lowering · replaces step-downs · no single-leg load",
                           ],
                           sets_reps="3 × 10–15", equipment="Bodyweight"),
            )],
        ),
        Section(
            header="D — Superset 3: Knee flexion + Ankle  (~6 min · 3 rounds · 60s rest after each pair)",
            items=[Pair(
                a=Exercise(number="7", muscle_key="hamstrings",
                           title="Prone hamstring curl",
                           detail_lines=[
                               "Biceps femoris · semimembranosus · semitendinosus",
                               "Lying flat · light weight or resistance band · no knee snap at bottom · replaces Nordic curls",
                           ],
                           sets_reps="3 × 12", equipment="Band / light DB"),
                b=Exercise(number="8", muscle_key="calves",
                           title="Standing calf raises",
                           subtitle_line="(hold wall or rack for balance · controlled lowering)",
                           detail_lines=[
                               "Gastrocnemius (primary) · soleus (synergist) · use hand support — hypermobility caution",
                           ],
                           sets_reps="3 × 10–15", equipment="Bodyweight"),
            )],
        ),
        Section(
            header="E — Finisher: Soleus  (~3 min · straight sets)",
            items=[
                Exercise(number="9", muscle_key="calves",
                         title="Seated calf raise",
                         detail_lines=[
                             "Soleus — deeper calf muscle, complements standing raise (gastrocnemius)",
                             "Seated on bench, weight on knees (DB or plate) · controlled raise and lower · soft lockout",
                         ],
                         sets_reps="3 × 12–15", equipment="DB / plate on knees"),
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
            "Never lock out knees — always keep a soft bend at end range",
            "No single-leg eccentric loading during knee rehab phase",
            "Skip session if joints feel unusually loose that day — reschedule, don't push",
            "Stop set early if any joint feels unstable — prioritize joint feel over rep count",
            "No pain rule — stop immediately if any knee pain or swelling",
            "Avoid knee hyperextension on all exercises",
            "Hip abductor/adductor machine: deferred until knee is stable",
        ],
    ),

    timing=InfoBox(
        title="Session timeline",
        body_lines=[
            "Warmup A (3 min) → Superset B (8 min) → Superset C (8 min) → Superset D (6 min) → Finisher E (3 min)",
            "Total working session: ~28 min · 18 working sets · then proceed to post-workout mobility protocol",
        ],
    ),

    set_count=SetCountBox(
        title="Working set count by muscle group",
        entries=[
            SetCountEntry("quads",      "Quads: 6 sets (sit-to-stand 3 + wall sit 3)"),
            SetCountEntry("glutes",     "Glutes: 3 sets direct (hip thrust) + significant synergist work from RDL — effective volume ~5–6 sets"),
            SetCountEntry("hamstrings", "Hamstrings: 6 sets (DB Romanian deadlift 3 + prone hamstring curls 3)"),
            SetCountEntry("calves",     "Calves: 6 sets (standing raises 3 + seated raises 3)"),
        ],
    ),

    version_note="v3 — EMG-verified muscle labels · hip ext (glute-dominant) ↔ knee ext (quad-dominant) pairing confirmed clean",
)


if __name__ == "__main__":
    sys.stdout.write(render(routine))
