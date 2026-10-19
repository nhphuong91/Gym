"""Routine definition: upper-body evaluation (loading-gate tests), v3.

Run: python3 -B build_evaluation_upperbody_v3.py <svg_routine_generator dir> <out.svg>
A record of how v3 was built (2026-10-07). The SVG is the source of truth: once its version note
is newer than v3, rebuild from the file just read (reference.md §R4), not from this definition.
Built from v2 (gymplan/evaluation_upperbody.svg, read 2026-10-07) and the plan Harry approved
in chat on 2026-10-07 (Q18 A · Q19 B · Q20 A → Stage 0 D-77 · D-78 · D-79): one test per card in
plain steps, a moving picture on every card, photo and video links, angles read from video.
The generator is not edited: card rendering for picture cards and the new colours are
monkey-patched here (reference.md §R4). figs.py, beside this script, draws the pictures.
"""
import os
import sys
import textwrap
from dataclasses import dataclass, field

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import routine_generator as rg  # noqa: E402
from routine_generator import (  # noqa: E402
    Routine, Section, Exercise, InfoBox, RulesBox, SetCountBox, SetCountEntry, MuscleColor, render,
)
import figs  # noqa: E402

rg.MUSCLE_COLORS.update({
    "eval_shoulder": MuscleColor("eval_shoulder", "Shoulder / rotator cuff",
                                 "#085041", "#e1f5ee", "#0f6e56", "#085041", "#0f6e56"),
    "eval_elbow": MuscleColor("eval_elbow", "Elbow (biceps, triceps)",
                              "#042c53", "#ddeeff", "#185fa5", "#042c53", "#0c447c"),
    "eval_wrist": MuscleColor("eval_wrist", "Wrist / forearm",
                              "#8a3a2e", "#fbeee9", "#c97b64", "#8a3a2e", "#a8503d"),
    "eval_spine": MuscleColor("eval_spine", "Low back / trunk",
                              "#633806", "#faeeda", "#854f0b", "#412402", "#633806"),
    "eval_all": MuscleColor("eval_all", "All joints",
                            "#666666", "#f2f2f2", "#aaaaaa", "#333333", "#555555"),
})

# ─── picture cards ─────────────────────────────────────────────────────────
LABEL_X, TEXT_X, WRAP = 72, 136, 61
FIRST, LINE_H = 34, 14
PIC_X, PIC_TOP = 486, 38
LINK_FILL = "#185fa5"


@dataclass
class TestCard(Exercise):
    steps: list = field(default_factory=list)   # [(label, text)]
    links: list = field(default_factory=list)   # [(label, url)]
    pic: str = ""


def _link_rows(links):
    rows, cur, x = [], [], LABEL_X
    for lab, url in links:
        txt = lab + " ↗"
        w = int(len(txt) * 5.0)
        if cur and x + w > 478:
            rows.append(cur)
            cur, x = [], LABEL_X
        cur.append((x, txt, url))
        x += w + 16
    if cur:
        rows.append(cur)
    return rows


def _render_test_card(ex, y, *, section_letter=""):
    if not isinstance(ex, TestCard):
        return _ORIG_CARD(ex, y, section_letter=section_letter)
    c = rg.color(ex.muscle_key)
    rows = []
    for lab, text in ex.steps:
        parts = textwrap.wrap(text, WRAP, break_on_hyphens=False)
        rows.append((lab, parts[0]))
        rows.extend((None, p) for p in parts[1:])
    link_rows = _link_rows(ex.links)
    text_h = FIRST + (len(rows) - 1) * LINE_H + len(link_rows) * (LINE_H + 1) + 14
    h = max(text_h, PIC_TOP + figs.H + 8)
    label = ex.comment_label or ex.title
    prefix = f"{section_letter}{ex.number}" if section_letter else ex.number
    out = [
        rg._comment(f"{prefix} — {label}"),
        rg._rect(rg.CONTENT_X, y, rg.STRIPE_WIDTH, h, 2, c.stripe),
        rg._rect(rg.CONTENT_X + rg.STRIPE_WIDTH, y, rg.CONTENT_WIDTH - rg.STRIPE_WIDTH, h, 4, c.card_fill, c.card_stroke),
        rg._text(rg.CARD_NUM_X, y + 16, ex.number, size=11, weight=500, fill=rg.NUMBER_FILL),
        rg._text(rg.CARD_TEXT_X, y + 16, ex.title, size=12, weight=500, fill=c.title_fill),
    ]
    for i, (lab, text) in enumerate(rows):
        yy = y + FIRST + i * LINE_H
        if lab:
            out.append(rg._text(LABEL_X, yy, lab, size=11, weight=500, fill=c.title_fill))
        out.append(rg._text(TEXT_X, yy, text, size=11, fill=c.detail_fill))
    ly = y + FIRST + len(rows) * LINE_H + 1
    for row in link_rows:
        for x, txt, url in row:
            out.append(f'<a href="{url}" target="_blank">'
                       + rg._text(x, ly, txt, size=10, fill=LINK_FILL) + "</a>")
        ly += LINE_H + 1
    if ex.sets_reps:
        out.append(rg._text(rg.CARD_RIGHT_X, y + 16, ex.sets_reps, size=12, weight=500, fill=c.title_fill))
    if ex.equipment:
        out.append(rg._text(rg.CARD_RIGHT_X, y + 31, ex.equipment, size=11, fill=c.detail_fill))
    if ex.pic:
        out += [rg._comment(f"PIC {ex.number} — {label}"),
                f'<g transform="translate({PIC_X},{y + PIC_TOP})">',
                f'<rect x="0" y="0" width="{figs.W}" height="{figs.H}" rx="4" fill="#ffffff" '
                f'stroke="{c.card_stroke}" stroke-width="0.8"/>',
                figs.PICTURES[ex.pic]("#0f6e56" if ex.pic == "score" else c.card_stroke),
                "</g>"]
    return out, y + h + rg.CARD_GAP


_ORIG_CARD = rg._render_exercise
rg._render_exercise = _render_test_card

# ─── links ─────────────────────────────────────────────────────────────────
KINOVEA = "https://kinovea.readthedocs.io/en/stable/measurement/angle.html"
LUO = "https://bmcmusculoskeletdisord.biomedcentral.com/articles/10.1186/1471-2474-8-90/figures/"
V_LUO = "https://www.youtube.com/watch?v=ohX94mNFn4Q"
MCCLURE = "https://nata.kglmeridian.com/downloadpdf/view/journals/attr/44/2/article-p160.pdf"
FORD = "https://bura.brunel.ac.uk/bitstream/2438/33074/4/FullText.pdf"
V_PUSH = "https://www.youtube.com/watch?v=utzhPQuXWcA"
V_QUAD = "https://www.youtube.com/watch?v=PSytregUBZY"
V_WEXT = "https://www.youtube.com/watch?v=-TCNPALVqi8"
V_WTURN = "https://www.youtube.com/watch?v=JqkJGiYDAEA"
V_CURL = "https://www.youtube.com/watch?v=tMEGqKuOa-M"
V_BAND = "https://www.youtube.com/watch?v=-cjtWEtilMc"
HOW = ("How to: Kinovea angle tools", KINOVEA)
VLUO = ("Video: IFMK Brest, all six tests (French)", V_LUO)

routine = Routine(
    title="Upper-body evaluation — loading-gate tests",
    subtitle="Shoulder · elbow · wrist · low back — ranges, control and symmetry · 2 sessions (~75 + ~25 min)",
    legend_muscles=["eval_shoulder", "eval_elbow", "eval_wrist", "eval_spine"],
    pre_workout=InfoBox(
        title="Before you start — what this is, and how the phone is used",
        body_lines=[
            "What: tests that decide when each upper-body joint may move up one loading stage. Order: A, B, C, then D.",
            "When: a rested day, no upper-body training or badminton the day before. Warm up 5 min (walk or bike).",
            "Phone = camera only: on the tripod ~2 m away, level, lens at the height the card names; never in your hand.",
            "Beat: a metronome on a second device (PC, tablet or speaker), loud enough for the video to record it.",
            "iPhone (iOS 18 or later): turn on Settings → Camera → Record Sound → Allow Audio Playback.",
            "Angles: later, on the PC, in Kinovea (free): open the video, pause on the frame, pick the card's tool,",
            "drag its centre onto the joint, note the number (over 180°: 360 minus it), snip the frame (Win+Shift+S).",
            "Pictures move when this file opens in Edge or Chrome; elsewhere they show the start (dark) and end (faint).",
            "Kit: dumbbells 2 × 1.5 kg, 2.5 kg, 1 kg, a curl weight · hex dumbbell handles · a band · bench · wall · mat",
            "2 pens · tape · tape measure · tripod and phone · a second device for the beat · Kinovea on the PC",
        ],
    ),
    sections=[
        Section(
            header="A — Session 1: Ranges  (~20 min · no weights · your own effort only, nothing pushes further)",
            comment_label="A RANGES",
            items=[
                TestCard(number="1", muscle_key="eval_shoulder", title="Shoulder raise range — each arm",
                         sets_reps="3 tries per arm", equipment="Tripod · phone", pic="shoulder_raise",
                         comment_label="Shoulder raise range",
                         steps=[("Set-up", "Stand side-on to the camera, 2 m away, lens at shoulder height, "
                                           "the tested arm nearest the camera, thumb up."),
                                ("Do", "Raise the straight arm forward and up as far as it goes by itself; hold 2 s; "
                                       "lower. 3 tries, then turn round for the other arm."),
                                ("Read", "Kinovea, top frame: Angle tool, centre on the shoulder, one leg to the hip, "
                                         "the other to the elbow."),
                                ("Write down", "The best of 3, per arm. Your training limit is ~75% of it.")],
                         links=[HOW]),
                TestCard(number="2", muscle_key="eval_shoulder", title="Shoulder turn-out range, lying — each arm",
                         sets_reps="3 tries per arm", equipment="Mat · tripod · phone", pic="shoulder_turnout",
                         comment_label="Shoulder turn-out range",
                         steps=[("Set-up", "Lie on your back, upper arm against your side, elbow bent 90°, forearm "
                                           "pointing at the ceiling (0°). Camera at your feet, lens at elbow height, "
                                           "looking along the arm."),
                                ("Do", "Turn the forearm out toward the floor as far as it goes by itself, the upper "
                                       "arm still against your side; hold 2 s; back up. 3 tries."),
                                ("Read", "Kinovea, end frame: Angle-to-vertical tool along the forearm, elbow to wrist."),
                                ("Write down", "The best of 3, per arm. Training limit: 45° or ~75% of it, "
                                               "whichever is smaller.")],
                         links=[HOW]),
                TestCard(number="3", muscle_key="eval_elbow", title="Elbow range — each arm",
                         sets_reps="3 tries per arm", equipment="Tripod · phone", pic="elbow_range",
                         comment_label="Elbow range",
                         steps=[("Set-up", "Stand side-on, the tested arm nearest the camera, hanging, palm forward. "
                                           "Lens at elbow height, 2 m away."),
                                ("Do", "Straighten the elbow fully, hold 2 s; then bend it fully, hold 2 s. 3 tries."),
                                ("Read", "Kinovea, both end frames: Angle tool, centre on the elbow, legs to the "
                                         "shoulder and the wrist."),
                                ("Write down", "Both numbers per arm, and whether the elbow bows past straight "
                                               "(yes/no). Training stops 20–30% of the arc short of straight.")],
                         links=[HOW]),
                TestCard(number="4", muscle_key="eval_wrist", title="Wrist range — each hand",
                         sets_reps="3 tries per hand", equipment="Table · tripod · phone", pic="wrist_range",
                         comment_label="Wrist range",
                         steps=[("Set-up", "Forearm flat on a table, palm down, hand past the edge. Camera at the "
                                           "thumb side, lens at table height."),
                                ("Do", "Bend the hand up as far as it goes by itself, hold 2 s; then down, hold 2 s. "
                                       "3 tries."),
                                ("Read", "Kinovea: Angle tool, centre on the wrist, one leg along the forearm, the "
                                         "other to the knuckles."),
                                ("Write down", "The up and the down number, per hand. Training limit: 70–80% of each.")],
                         links=[HOW]),
                TestCard(number="5", muscle_key="eval_spine", title="Low-back bend range — forward and back",
                         sets_reps="3 tries each way", equipment="2 pens · tape · tripod", pic="lowback_range",
                         comment_label="Low-back bend range",
                         steps=[("Set-up", "Tape one pen flat on your spine at the two low-back dimples, a second pen "
                                           "15 cm higher. Stand side-on, knees straight, lens at waist height."),
                                ("Do", "Stand tall 2 s; bend forward as far as is comfortable, hold 2 s; stand up; "
                                       "lean back, hold 2 s. 3 tries each way."),
                                ("Read", "Kinovea, on the standing, forward and back frames: Angle-to-horizontal "
                                         "on each pen."),
                                ("Write down", "Both pen numbers on each frame; Claude works out the range. Limit: "
                                               "70–80% of it, never past ~36–42° forward or ~12–15° back.")],
                         links=[HOW]),
                TestCard(number="6", muscle_key="eval_spine", title="Low-back side-bend — each side",
                         sets_reps="3 tries per side", equipment="Pen · tape measure", pic="sidebend",
                         comment_label="Low-back side-bend",
                         steps=[("Set-up", "Stand tall, arms by your sides, feet hip-width apart. Mark where your "
                                           "middle fingertip touches the thigh."),
                                ("Do", "Slide the hand straight down the side of the thigh as far as is comfortable, "
                                       "without leaning forward or back; mark again. 3 tries per side."),
                                ("Write down", "The gap between the marks (cm), each side. Training limit: 70–80% of "
                                               "it. Twisting has no number: it is judged on the control-test videos.")]),
            ],
        ),
        Section(
            header="B — Session 1: Control tests  (~35 min · each clean or not · film every one)",
            comment_label="B CONTROL TESTS",
            items=[
                TestCard(number="7", muscle_key="eval_spine", title="Hip hinge (waiter's bow)",
                         sets_reps="3 slow reps", equipment="Tripod · phone", pic="hip_hinge",
                         comment_label="Hip hinge",
                         steps=[("Set-up", "Stand side-on, hands on hips, knees soft. Lens at hip height."),
                                ("Do", "Bow forward from the hips to about 60°, back flat, then stand up. 3 slow reps."),
                                ("Fail if", "The low back rounds, or the hips stop bending before 50° without the "
                                            "back moving."),
                                ("Write down", "Failed reps (a test fails at 2 of 3).")],
                         links=[("Photo: Luomajoki 2007, Fig 1", LUO + "1"), VLUO]),
                TestCard(number="8", muscle_key="eval_spine", title="Pelvic tuck (pelvic tilt)",
                         sets_reps="3 slow reps", equipment="Tripod · phone", pic="pelvic_tuck",
                         comment_label="Pelvic tuck",
                         steps=[("Set-up", "Stand side-on, relaxed. Lens at hip height."),
                                ("Do", "Squeeze the glutes and tuck the pelvis under, so the low back flattens, while "
                                       "the upper back stays still; relax. 3 slow reps."),
                                ("Fail if", "The pelvis does not tilt, the low back arches instead, the glutes stay "
                                            "off, or the upper back rounds."),
                                ("Write down", "Failed reps.")],
                         links=[("Photo: Luomajoki 2007, Fig 4", LUO + "4"), VLUO]),
                TestCard(number="9", muscle_key="eval_spine", title="Seated knee straighten — each leg",
                         sets_reps="3 reps per leg", equipment="Bench · tripod", pic="seated_knee",
                         comment_label="Seated knee straighten",
                         steps=[("Set-up", "Sit tall on a high bench, feet off the floor, low back in its normal "
                                           "small arch. Lens at seat height, side-on."),
                                ("Do", "Straighten one knee slowly until it is 30–50° short of straight, then lower. "
                                       "3 reps per leg."),
                                ("Fail if", "The low back rounds (slumps) as the knee straightens."),
                                ("Write down", "Failed reps, per leg.")],
                         links=[("Photo: Luomajoki 2007, Fig 2", LUO + "2"), VLUO]),
                TestCard(number="10", muscle_key="eval_spine", title="Rock forward on all fours",
                         sets_reps="3 slow reps", equipment="Mat · handles · tripod", pic="rock_forward",
                         comment_label="Rock forward",
                         steps=[("Set-up", "On hands and knees, fists or handles under the shoulders, knees under "
                                           "the hips, back flat. Lens ~30 cm up, side-on."),
                                ("Do", "Rock the body forward, shoulders past the hands, and back. 3 slow reps."),
                                ("Fail if", "The low back sags (arches) as you rock forward."),
                                ("Write down", "Failed reps.")],
                         links=[("Photo: Luomajoki 2007, Fig 6", LUO + "6"), VLUO]),
                TestCard(number="11", muscle_key="eval_spine", title="Rock back on all fours",
                         sets_reps="3 slow reps", equipment="Mat · handles · tripod", pic="rock_back",
                         comment_label="Rock back",
                         steps=[("Set-up", "As card 10."),
                                ("Do", "Rock the hips back toward the heels until the hips are bent about 120°, "
                                       "back flat; return. 3 slow reps."),
                                ("Fail if", "The low back rounds before the hips reach about 120°."),
                                ("Write down", "Failed reps.")],
                         links=[("Photo: Luomajoki 2007, Fig 3", LUO + "3"), VLUO]),
                TestCard(number="12", muscle_key="eval_spine", title="Face-down knee bend — each leg",
                         sets_reps="3 reps per leg", equipment="Mat · tripod", pic="prone_knee",
                         comment_label="Face-down knee bend",
                         steps=[("Set-up", "Lie face down, forehead on your hands, legs straight. Lens at floor "
                                           "level, side-on."),
                                ("Do", "Bend one knee until the shin is upright (90°) or more, then lower. "
                                       "3 reps per leg."),
                                ("Fail if", "The pelvis lifts or tips, or the low back arches, as the knee bends."),
                                ("Write down", "Failed reps, per leg. Tests 7–12 are clean with at most 1 failed "
                                               "test and no pain.")],
                         links=[("Photo: Luomajoki 2007, Fig 5", LUO + "5"), VLUO]),
                TestCard(number="13", muscle_key="eval_shoulder", title="Shoulder-blade check",
                         sets_reps="8–10 + 8–10, twice", equipment="2 × 1.5 kg · tripod", pic="blade_check",
                         comment_label="Shoulder-blade check",
                         steps=[("Set-up", "Shirt off, back to the camera 2 m away, lens at shoulder height. "
                                           "Metronome 60: 2 beats up, 2 down."),
                                ("Do", "First without weights, then with 1.5 kg in each hand: raise both straight arms "
                                       "forward, thumbs up, as high as is comfortable, 8–10 times; then out to the "
                                       "sides, 8–10 times."),
                                ("Fail if", "On the video, a blade's inner edge lifts off the ribs (2.5 cm or more), "
                                            "or the blade jerks, hitches up early or drops fast, on 3 of 5 reps or "
                                            "more; worse with weights than without; any slipping or pain."),
                                ("Write down", "Per side and per raise: normal, subtle (mild, not every rep) or "
                                               "obvious.")],
                         links=[("Photo: McClure 2009, Fig 2 (normal vs obvious)", MCCLURE)]),
                TestCard(number="14", muscle_key="eval_elbow", title="Kneeling push-ups on handles",
                         sets_reps="10 reps × 2 sets", equipment="Hex DB handles · tripod", pic="kneeling_pushup",
                         comment_label="Kneeling push-ups",
                         steps=[("Set-up", "Kneel, hands on hex-dumbbell handles under the shoulders, body straight "
                                           "from knees to head. Lens at floor level, side-on; film one set from each "
                                           "side. Metronome 60."),
                                ("Do", "Down for 3 beats until the upper arms are level with the body, up for 2, hold "
                                       "2 at the top with soft elbows. 10 reps."),
                                ("Fail if", "An elbow goes straight (less than ~15° bent on the top frame), snaps, "
                                            "clunks or drifts into lockout; any pain."),
                                ("Write down", "Clean or not, per elbow.")],
                         links=[("Video: Get Exercise Confident, kneeling push-up", V_PUSH)]),
                TestCard(number="15", muscle_key="eval_elbow", title="One-arm hold on all fours — each arm",
                         sets_reps="30 s per arm", equipment="Mat · handles · tripod", pic="one_arm_hold",
                         comment_label="One-arm hold",
                         steps=[("Set-up", "On hands and knees as card 10, lens side-on, the supporting arm nearest "
                                           "the camera."),
                                ("Do", "Lift the other hand off the floor and hold 30 s, the supporting elbow "
                                       "slightly bent. Then switch arms."),
                                ("Fail if", "As card 14: the elbow goes straight, snaps, clunks or drifts into "
                                            "lockout; any pain."),
                                ("Write down", "Clean or not, per elbow.")],
                         links=[("Video: NASM, quadruped arm raise", V_QUAD)]),
                TestCard(number="16", muscle_key="eval_wrist", title="Wrist control set, 1 kg — each hand",
                         sets_reps="10 per direction", equipment="1 kg · bench · tripod", pic="wrist_control",
                         comment_label="Wrist control set",
                         steps=[("Set-up", "Forearm supported on a bench, hand past the edge; a book or block at your "
                                           "card-4 limit stops the hand. Film from the side, then from above. "
                                           "Metronome 60: up on one beat, down on the next."),
                                ("Do", "10 up · 10 down · 10 side to side (palm down, thumb side to little-finger "
                                       "side) · 10 palm-down to palm-up turns. Side to side and turns stay small."),
                                ("Fail if", "A clunk or catch, the wrist gives way, the hand passes the stop, a beat "
                                            "is missed, or any pain."),
                                ("Write down", "Clean or not, per hand.")],
                         links=[("Video: AskDoctorJo, wrist extension", V_WEXT), ("turns", V_WTURN)]),
            ],
        ),
        Section(
            header="C — Session 1: Symmetry tests  (~20 min · each arm to technical failure · ≥3 min between sides)",
            comment_label="C SYMMETRY TESTS",
            items=[
                TestCard(number="17", muscle_key="eval_shoulder", title="Side-raise endurance, 2.5 kg — each arm",
                         sets_reps="1 set per arm", equipment="2.5 kg · wall · tripod", pic="side_raise",
                         comment_label="Side-raise endurance",
                         steps=[("Set-up", "Back and head against a wall, feet shoulder-width. Camera in front, 2 m, "
                                           "lens at shoulder height. Metronome 30: up on one beat, down on the next "
                                           "(2 s each)."),
                                ("Do", "Raise the arm to shoulder height, about 30° in front of straight out to the "
                                       "side, elbow slightly bent, thumb pointing forward and level; lower. Keep going."),
                                ("Stop when", "A rep misses shoulder height, misses the beat or drifts out of line."),
                                ("Write down", "Reps before the first miss, per arm.")],
                         links=[("Photo: Ford 2026, Fig 1 (step by step)", FORD)]),
                TestCard(number="18", muscle_key="eval_elbow", title="Curl endurance, one arm — each arm",
                         sets_reps="1 set per arm", equipment="Curl weight · bench", pic="curl",
                         comment_label="Curl endurance",
                         steps=[("Set-up", "Sit tall, back supported, one dumbbell that gives your stronger arm 12–20 "
                                           "reps; the same weight every time. Camera side-on. Metronome 60: 2 beats "
                                           "up, 2 down."),
                                ("Do", "Curl up and lower; the bottom stops just short of straight; no swinging."),
                                ("Stop when", "A rep misses the beat or the range."),
                                ("Write down", "Reps per arm, and the weight (kg).")],
                         links=[("Video: OPEX, seated one-arm curl", V_CURL)]),
                TestCard(number="19", muscle_key="eval_wrist", title="Band wrist-lift endurance — each hand",
                         sets_reps="1 set per hand", equipment="Band · bench · tripod", pic="band_wrist",
                         comment_label="Band wrist-lift endurance",
                         steps=[("Set-up", "Forearm supported, palm down, hand past the edge, the band from under your "
                                           "foot to the hand; the same band and spot every time. Camera side-on. "
                                           "Metronome 60: 2 beats up, 2 down."),
                                ("Do", "Lift the back of the hand and lower it, inside your card-4 limits."),
                                ("Stop when", "A rep misses the beat or the range."),
                                ("Write down", "Reps per hand, and which band.")],
                         links=[("Video: Baptist Health, band wrist extension", V_BAND)]),
            ],
        ),
        Section(
            header="D — Session 2: 2–7 days later  (~25 min · symmetry tests only)",
            comment_label="D SESSION 2",
            items=[
                TestCard(number="20", muscle_key="eval_all", title="Repeat 17–19 — other side first",
                         sets_reps="1 set per arm", equipment="As session 1", pic="score",
                         comment_label="Repeat symmetry tests",
                         steps=[("Set-up", "2–7 days after session 1: the same warm-up, weights, band, beat and "
                                           "set-up. Start with the other side."),
                                ("Do", "Tests 17, 18 and 19 once more."),
                                ("Score", "Mean of both sessions, weaker ÷ stronger: shoulder ≥80%, elbow and wrist "
                                          "≥85% passes."),
                                ("Example", "Side raise left 18 and 17, right 21 and 22: 17.5 ÷ 21.5 = 81%, a pass.")]),
            ],
        ),
    ],
    post_workout=InfoBox(
        title="Step-gate log — after every training session (exit criterion 1)",
        body_lines=[
            "Per joint: pain ≤5/10 during and after · back to normal the next morning · no swelling or warmth",
            "within 24 h · no “loose joint” feeling that day.",
            "Two clean weeks in a row are needed; a fail is a flare and restarts the count.",
        ],
    ),
    rules=RulesBox(
        title="Every test — rules",
        bullets=[
            "These are tests, not training sets: follow each card's set-up exactly",
            "Stop at pain, a clunk or a slipping feeling — that test is not clean this round",
            "Same weight, band, set-up and beat every time; write down the curl weight and the band",
            "Film every test and judge it on the paused video, not by feel",
            "Ranges: your own effort only — no hand, strap or body weight pushes the joint further",
            "No stretching before the range tests",
        ],
    ),
    timing=InfoBox(
        title="What the results unlock — the same tests at every stage step",
        body_lines=[
            "A joint moves up one loading stage when all three hold: 2 clean step-gate weeks, a clean control test",
            "and a passed symmetry test. Passing now opens stage 2 only.",
            "For 2→3: train ≥2 clean weeks at stage 2, then run this file again; the same for 3→4.",
            "The ranges (A) set your training limits at every stage; redo them after a flare.",
            "The low back has no symmetry test (not a paired joint) · a flare drops a joint back one stage.",
            "Rules behind this file: Stage 0 §2.5–2.6 · R7 · R14 · decisions D-63…D-79 (gymspec folder).",
        ],
    ),
    set_count=SetCountBox(
        title="Send back to Claude — results per joint",
        entries=[
            SetCountEntry("eval_shoulder", "Shoulder: raise ° L/R · turn-out ° L/R · blade rating L/R (forward, side) · side-raise reps L/R ×2"),
            SetCountEntry("eval_elbow", "Elbow: straight and bent ° L/R · past straight? · tests 14–15 clean? · curl reps L/R ×2 · curl kg"),
            SetCountEntry("eval_wrist", "Wrist: up and down ° L/R · test 16 clean? · band reps L/R ×2 · which band"),
            SetCountEntry("eval_spine", "Low back: pen numbers on the 3 frames · side-bend cm L/R · failed tests __ of 6"),
            SetCountEntry("eval_all", "All: the Kinovea snips · step-gate clean weeks so far, per joint"),
        ],
    ),
    version_note="v3 — plain one-test cards with moving pictures and photo/video links; angles from video, phone on the tripod only (D-77…D-79)",
)

svg = render(routine)
# Link the Kinovea line of the first box to Kinovea's guide.
needle = ">Angles: later, on the PC, in Kinovea (free): open the video, pause on the frame, pick the card's tool,</text>"
start = svg.index(needle)
tag_start = svg.rindex("<text ", 0, start)
end = start + len(needle)
svg = svg[:tag_start] + f'<a href="{KINOVEA}" target="_blank">' + svg[tag_start:end] + "</a>" + svg[end:]
with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print(sys.argv[2], len(svg.encode("utf-8")), "bytes")
