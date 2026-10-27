"""Build the two region-wide mobility files from the data below (Stage 2 §2.1 · R55; register: build script).

Run from the Gym folder:  python3 -B gymtools/svg/build_mobility_v1.py <out_dir>
Writes <out_dir>/stretching_upper_hEDS.svg (v5) and <out_dir>/stretching_lower_hEDS.svg (v3). Copy each into gymplan/
and cp it to gymtxt/<stem>.txt (Stage 2 R57); never write straight into gymplan/.

Form, kept from the hand-laid files: 680 px page; legend; a principle box; a PRE and a POST section, each a core list
plus add-ons picked by target (add-on cards dashed); each card has its ID centred at x 54 (size 11, bold), its title at x 72
(size 12, bold), three lines below it and a dose column at x 510 (upper) or 515 (lower); then the breathing note,
target index, self-check, rules and timeline boxes; the version note last (size 9, centred). Card IDs and titles are
what catalogue/verify.py check 6 reads, so each title keeps the words of its catalogue row (ExerciseCatalogue rev 13).

Copied from build_mobility_v1.py (upper v4, lower v3) on 2026-10-27 for upper v5: S6, the biceps hold, back as a post
add-on (catalogue rev 14); the lower data is unchanged and rebuilds v3 byte-identical.
The drills follow the catalogue rows screened at the Current state of 2026-10-26: shoulder, elbow and wrist at loading
stage 2; spine, hip, knee and ankle at 1. When a joint changes stage, re-screen the rows, edit the data in a copy of
this script, raise the version, rebuild and run the checks in gymtools/README.md (Stage 2 R55 · R66).
"""
import os
import sys

PAL = {  # bar, card fill, card stroke, title, text: the five target colours of the hand-laid files
    "teal": ("#085041", "#e1f5ee", "#0f6e56", "#085041", "#0f6e56"),
    "red": ("#8b1a1a", "#fce8e8", "#c44040", "#8b1a1a", "#a83030"),
    "purple": ("#26215c", "#eeedfe", "#534ab7", "#26215c", "#3c3489"),
    "brown": ("#633806", "#faeeda", "#854f0b", "#412402", "#633806"),
    "navy": ("#042c53", "#ddeeff", "#185fa5", "#042c53", "#0c447c"),
}

PRINCIPLE = [
    "⚠ Why active drills only — hEDS / HSD",
    "Your joints have range to spare; what they lack is control. Muscles guard loose joints with",
    "protective tension, and passive stretching switches that guard off. Every drill here is made by",
    "your own muscles, inside the range they control, with nothing pushing further (R7).",
]
POST_GOAL = "Compare each joint with the pre half · log any change with the step gate (§2.6) · tightness → foam rolling (R7)"
BREATH = ("Holds: breathe in before, breathe out slowly during — never hold your breath",
          "A slow exhale under tension keeps trunk pressure steady")
BREATHING_CARD = ["Diaphragm · deep core — winding down",
                  "On your back, hips and knees at 90°, feet resting on the bench",
                  "Breathe in 4 s through the nose, ribs widen · out 8 s, ribs drop; easy, unforced"]
RULE_ACTIVE = "Active only: your own muscles move and hold; nothing pushes a joint further, no bounce (R7)"
RULE_RANGE = "~70–80% of your range, never end range; a soft bend at every joint, no lockout (R1 · R2)"
RULE_LIGHT = "Light: holds at ~20–30% of a max push, moves slow and smooth — drills are not working sets (§2.3 · R19)"
RULE_CARS = "CARs: a spot catches or clicks → slow down there, never force through it (R7)"
RULE_ABORT = "A joint feels loose or unstable → stop that drill; loose joints that day → skip the session (R9)"
TIMELINE_2 = "Add-ons only when your session's targets call for them; tightness after a session → foam rolling (R7)"

# Card: (ID, colour, catalogue row, title, [3 lines], [dose column, up to 3 lines])
UPPER = {
    "stem": "stretching_upper_hEDS", "version": 5, "col": 510,
    "title": "Mobility protocol — upper body (hEDS / HSD safe)",
    "subtitle": "Pre: joint control before warm-up sets · Post: joint check · active drills only (R7) · add-ons by target",
    "legend": [("teal", "Shoulder / cuff"), ("brown", "Scapula / upper back"), ("navy", "Elbow / arms"),
               ("red", "Wrist / spine"), ("purple", "Breathing")],
    "pre_head": "PRE-WORKOUT — joint control  (core ~10 min · before warm-up sets)",
    "pre_goal": "Core: every upper-body joint, every session · Add-ons: pick by your session's targets · light effort, slow breathing",
    "pre_core": [
        ("P1", "teal", "C097", "Shoulder CARs, both arms together",
         ["Shoulder capsule · rotator cuff · scapular stabilisers",
          "Arms circle together, mirrored: the biggest circle you control (R12)",
          "Steady tension, short of end range; ribs down, low back still (R1 · R3)"],
         ["2 each direction", "~30 s per circle", "standing"]),
        ("P2", "teal", "C100", "Band external-rotation hold, 3 angles, both hands on one band",
         ["Infraspinatus · teres minor · back of the cuff",
          "Elbows pinned to your sides; turn both forearms out against the band",
          "Hold near neutral, mid-way, then at ~70–80% of your turn-out — 90° only if it's inside (R1)"],
         ["8 s × 3 angles", "× 2 rounds", "light band"]),
        ("P3", "teal", "C143", "Internal-rotation hold, both arms, palms pressed together",
         ["Subscapularis · front of the cuff (front-of-shoulder stability)",
          "Elbows pinned to your sides, bent 90°; hands meet in front of the belly",
          "Press palm into palm ~20–30%: both shoulders turn in against each other, nothing moves"],
         ["8 s hold", "× 3", "no kit"]),
        ("P4", "brown", "C103", "Band pull-apart hold at chest height",
         ["Rear delts · rhomboids · mid-trap; the chest lengthens actively",
          "Hands stop in line with the shoulders, never behind the torso (R1)",
          "Elbows soft (R2); shoulder blades come together without a shrug (R8)"],
         ["2 × 8 reps", "3 s hold each rep", "light band"]),
        ("P5", "red", "C098", "Wrist CARs, both wrists together + palm press in 4 directions",
         ["Wrist capsule · forearm flexors and extensors",
          "Forearms on your thighs; both wrists circle slowly, ~70–80% of range",
          "Then palm into palm: bend up · bend down · thumb side · little-finger side, ~20–30% each"],
         ["5 circles each way", "+ 5 s × 4 directions", "seated"]),
        ("P6", "brown", "C099", "Scapular push-up hold (on fists or DB handles)",
         ["Serratus anterior · lower trap · elbow control",
          "Wrists straight on fists or hex DB handles, never bent back (R2)",
          "Push the shoulder blades apart to ~80% and hold; elbows soft, ~15° short of straight (R1 · R2)"],
         ["3 × 10 s hold", "knees down if needed"]),
        ("P7", "red", "C102", "Wrist weight shifts on fists, 4 directions (hands and knees)",
         ["Wrist stabilisers in neutral · forearm co-contraction",
          "On fists or DB handles, knees down; wrists stay straight throughout",
          "Shift a little forward · back · left · right and hold each; no bend at the wrist (R1 · R2)"],
         ["5 s × 4 directions", "× 2 rounds"]),
        ("P8", "red", "C101", "Cat-cow with pauses (on fists or DB handles)",
         ["Thoracic spine · serratus · rhomboids · deep core",
          "Low back moves only part-way: your stage-1 range, short of each end (R3)",
          "Pause 3 s near each end: cat = push the floor away · cow = blades together, no sag"],
         ["1 × 6 reps", "3 s pause each end"]),
    ],
    "pre_add": [
        ("P9", "brown", "C108", "Prone Y-T-W holds",
         ["Lower and mid trap · rhomboids · back of the cuff — overhead days",
          "Face down, chest on the floor, thumbs up; no shrug (R8)",
          "Y short of end range · T at the shoulder line · W with the arms angled, not spread wide (R1)"],
         ["1 round", "8 s each letter", "body weight"]),
        ("P10", "navy", "C106", "Overhead triceps hold, both arms (band under both feet)",
         ["Triceps long head · overhead control — before overhead extensions",
          "Shoulder blades braced overhead, arms short of end range (R6 · R1)",
          "Elbows bend to ~70–80% and hold; nothing pulls the arms deeper (R7)"],
         ["2 × 12 s hold", "light band"]),
        ("P11", "red", "C135", "Seated thoracic rotation, arms crossed",
         ["Upper-back rotation · obliques",
          "Sit tall on the bench, arms crossed on the chest, pelvis still",
          "Turn the upper back to ~70–80% of the range and pause 2 s; no bounce (R1 · R7)"],
         ["5 each side", "slow"]),
        ("P12", "red", "C109", "Neck rotation holds, both hands resisting",
         ["Neck stabilisers — when the neck feels stiff",
          "Both hands stacked on the side of the head; turn into them ~20%",
          "The head stays still; the hands only resist, never push the head further (R7)"],
         ["5 s each way", "× 2 rounds"]),
    ],
    "post_head": "POST-WORKOUT — joint check and wind-down  (core ~4 min · after the last set)",
    "post_core": [
        ("S1", "teal", "C097", "Shoulder CARs, slow scan, both arms together",
         ["Joint check: compare with P1",
          "One slow circle each way; note any new catch, click or looseness",
          "Worse than in P1 → note it in the step-gate log; a loose shoulder ends the drill (§2.6 · R9)"],
         ["1 each direction", "~45 s per circle"]),
        ("S2", "red", "C098", "Wrist CARs, slow scan, both wrists together",
         ["Joint check: compare with P5",
          "Forearms on your thighs; 3 slow circles each way, ~70–80% of range",
          "New catching or pain compared with P5 → note it in the step-gate log (§2.6)"],
         ["3 each direction", "seated"]),
        ("S3", "purple", "C110", "90/90 breathing (feet on the bench or wall)", BREATHING_CARD,
         ["5 breaths", "4 s in / 8 s out", "~1 min"]),
    ],
    "post_add": [
        ("S4", "brown", "C108", "Prone Y-T-W holds",
         ["Lower and mid trap · back of the cuff — after a session without the Y raise",
          "As P9: chest on the floor, thumbs up, no shrug (R8)",
          "Y short of end range · T at the shoulder line · W with the arms angled, not spread wide (R1)"],
         ["1 round", "8 s each letter", "body weight"]),
        ("S5", "navy", "C106", "Overhead triceps hold, both arms (band under both feet)",
         ["Triceps long head — if they feel tight; foam rolling first (R7)",
          "As P10: shoulder blades braced overhead, arms short of end range (R6)",
          "Elbows bend to ~70–80% and hold; nothing pulls the arms deeper (R7)"],
         ["2 × 12 s hold", "light band"]),
        ("S6", "navy", "C105", "Biceps hold, both palms pressing forward (uprights or doorway)",
         ["Biceps · brachialis — if tight after curls; foam rolling first (R7)",
          "Facing the rack uprights or a doorway: palms forward against them, arms at your sides (R5)",
          "Elbows at ~140–150°; press forward ~30% and hold, both arms together (R1 · R12)"],
         ["2 × 15 s hold", "uprights or doorway"]),
    ],
    "index": [
        ("teal", "Shoulder capsule / cuff", "P1 · P2 · P3 · post S1"),
        ("brown", "Scapula / upper back", "P4 · P6 · P8 · add-on P9 · post S4"),
        ("teal", "Chest / front of shoulder", "P3 · P4 (chest lengthens) · P6"),
        ("brown", "Lats / overhead work", "P1 · add-ons P9 · P10"),
        ("navy", "Elbow · biceps · triceps", "P6 (soft elbow) · add-on P10 · post S5 · S6 · your warm-up sets"),
        ("red", "Wrist · forearm · grip", "P5 · P7 · post S2"),
        ("red", "Upper and lower back", "P8 · add-on P11"),
        ("red", "Neck", "add-on P12"),
        ("purple", "Ribcage / winding down", "post S3"),
    ],
    "check_head": "Before vs after — log any change with the step gate (§2.6)",
    "check": [
        ("teal", "Shoulders: S1 vs P1 — any new click, catch or looseness?"),
        ("red", "Wrists: S2 vs P5 — any new catching or pain?"),
        ("brown", "Worse after a drill → log it and leave that drill out next session"),
    ],
    "rules": [RULE_ACTIVE, RULE_RANGE, RULE_CARS,
              "Both arms together on every drill: one-arm work waits for loading stage 3 (R12)",
              "Spine at stage 1: the low back moves only part-way, ribs down (R3)",
              RULE_LIGHT, RULE_ABORT],
    "timeline": ["Pre core (~10 min) → add-ons by target → 1–2 warm-up sets → your session → post core (~4 min)",
                 TIMELINE_2],
    "note": "v5 — S6, the biceps hold, back as a post add-on: palms pressing forward on the rack uprights or a doorway (catalogue rev 14)",
}

LOWER = {
    "stem": "stretching_lower_hEDS", "version": 3, "col": 515,
    "title": "Mobility protocol — lower body (hEDS / HSD safe)",
    "subtitle": "Pre: joint control before warm-up sets · Post: joint check · active drills only (R7) · add-ons by target",
    "legend": [("teal", "Glutes"), ("purple", "Quads / knee"), ("brown", "Hamstrings / adductors"),
               ("navy", "Ankles / calves"), ("red", "Hips / balance / breath")],
    "pre_head": "PRE-WORKOUT — joint control  (core ~11 min · before warm-up sets)",
    "pre_goal": "Core: every lower-body joint, every session · Add-ons: pick by your session's targets · light effort, slow breathing",
    "pre_core": [
        ("P1", "navy", "C112", "Ankle CARs, both feet together (seated)",
         ["Ankle capsule · calves · shin muscles",
          "Seated, both feet lifted; both ankles circle slowly together (R12)",
          "The biggest circle you control, short of end range; note any catching (R1 · R7)"],
         ["5 each direction", "~10 s per circle", "seated"]),
        ("P2", "red", "C142", "Supine windshield wipers, both knees together",
         ["Hip rotators, in and out · hip capsule",
          "On your back, knees bent, feet flat and wider than your hips",
          "Both knees drop to one side to ~70–80% of the range, then the other; low back quiet (R1 · R3)"],
         ["5 each side", "slow, no bounce"]),
        ("P3", "red", "C137", "Supine bent-knee leg lift to tabletop, both legs",
         ["Hip flexors · deep core",
          "On your back, knees bent ~90°; lift both feet until the thighs are upright",
          "Low back stays flat; lower slowly and stop where it starts to arch (R1 · R2)"],
         ["2 × 6 reps", "2–3 s down"]),
        ("P4", "teal", "C131", "Supine banded butterfly (short band above the knees)",
         ["Glute med · hip abductors · side-of-hip control",
          "On your back, knees bent, feet flat hip-width; both knees open together",
          "Open to ~70–80% of the range, not to the floor; pelvis and low back still (R1)"],
         ["2 × 10 reps", "short band"]),
        ("P5", "teal", "C075", "Glute bridge, band above the knees, 3 s squeeze",
         ["Glute max · hamstrings",
          "Knees pressed out against the band; ribs down, no arch in the low back (R3)",
          "⚠ The load peaks at the top: stop just short of full hip extension — that's your margin (R2)"],
         ["2 × 8 reps", "3 s squeeze at the top", "short band"]),
        ("P6", "purple", "C132", "Short-band squat hold, knees pressed out (above parallel)",
         ["Quads · glute med · knee tracking",
          "Short band just above the knees; press both knees out over the toes",
          "Thighs stay above parallel at the deepest point; easy effort, no caving (R3 · R11)"],
         ["2 × 20 s hold", "short band"]),
        ("P7", "navy", "C117", "Calf-raise hold just short of the top, both legs",
         ["Calves · ankle control",
          "Hand on the wall or rack; rise on both feet together (R12)",
          "⚠ Hold just below your highest point: full height under body weight is end range (R2)"],
         ["2 × 8 reps", "3 s hold each rep", "wall support"]),
        ("P8", "red", "C130", "Tandem stance, heel to toe (eyes open, then closed)",
         ["Ankle and hip stabilisers · balance",
          "Front heel against the back toes; knees soft; beside the rack, a hand ready",
          "Eyes closed only once 30 s with eyes open is steady; swap the front foot (R23)"],
         ["2 × 30 s", "one per front foot"]),
    ],
    "pre_add": [
        ("P9", "purple", "C115", "Banded knee extension, both legs (one band behind both knees)",
         ["Quads — before squat or knee-dominant work",
          "Band from the rack behind both knees; both knees work together (R12)",
          "⚠ Straighten to just short of straight: the load peaks there, so never lock (R2)"],
         ["2 × 12 reps", "light band"]),
        ("P10", "brown", "C119", "Hamstring hold, both heels pressing into the wall",
         ["Hamstrings — before hinge work",
          "On your back, both feet on the wall at ~45°, knees slightly bent (R2)",
          "Press both heels into the wall ~30% and hold; both legs together (R12)"],
         ["2 × 15 s hold"]),
        ("P11", "brown", "C133", "Supine banded hip adduction, both legs (two long bands)",
         ["Adductors — before the hip machine or wide-stance work",
          "A long band round each knee from the frame, same pull both sides (R23)",
          "Start with the knees open to ~70–80% and bring both together slowly (R1)"],
         ["2 × 10 reps", "2 long bands", "frame"]),
    ],
    "post_head": "POST-WORKOUT — joint check and wind-down  (core ~3 min · after the last set)",
    "post_core": [
        ("S1", "navy", "C112", "Ankle CARs, slow scan, both feet together",
         ["Joint check: compare with P1",
          "Seated; 3 slow circles each way; note any new catching or stiffness",
          "Worse than in P1 → note it in the step-gate log (§2.6)"],
         ["3 each direction", "seated"]),
        ("S2", "red", "C142", "Supine windshield wipers, slow scan",
         ["Joint check: compare with P2",
          "3 slow sweeps each side to ~70–80%; note any pinch, click or looseness",
          "A loose or painful hip ends the drill; note it in the step-gate log (R9 · §2.6)"],
         ["3 each side"]),
        ("S3", "red", "C110", "90/90 breathing (feet on the bench or wall)", BREATHING_CARD,
         ["5 breaths", "4 s in / 8 s out", "~1 min"]),
    ],
    "post_add": [
        ("S4", "brown", "C119", "Hamstring hold, both heels pressing into the wall",
         ["Hamstrings — if they feel tight; foam rolling first (R7)",
          "As P10: feet on the wall at ~45°, knees slightly bent (R2)",
          "Press both heels ~30% and hold; both legs together (R12)"],
         ["2 × 15 s hold"]),
    ],
    "index": [
        ("navy", "Ankle · calves · Achilles", "P1 · P7 · post S1"),
        ("red", "Hip rotation / capsule", "P2 · post S2"),
        ("red", "Hip flexors / deep core", "P3"),
        ("teal", "Glute med / abductors", "P4 · P6"),
        ("teal", "Glute max", "P5"),
        ("purple", "Quads / knee tracking", "P6 · add-on P9"),
        ("brown", "Hamstrings", "add-on P10 · post S4"),
        ("brown", "Adductors", "add-on P11"),
        ("red", "Balance", "P8"),
        ("red", "Ribcage / winding down", "post S3"),
    ],
    "check_head": "Before vs after — log any change with the step gate (§2.6)",
    "check": [
        ("navy", "Ankles: S1 vs P1 — any new catching or stiffness?"),
        ("red", "Hips: S2 vs P2 — any new pinch, click or looseness?"),
        ("purple", "Knees: any pain, swelling or instability during or after the session?"),
    ],
    "rules": [RULE_ACTIVE, RULE_RANGE, RULE_CARS,
              "Both legs together, or both feet loaded: one-leg drills wait for loading stage 3 (R12)",
              "Stage 1: knees above parallel; the low back moves only part-way, ribs down (R3 · R11)",
              RULE_LIGHT, RULE_ABORT],
    "timeline": ["Pre core (~11 min) → add-ons by target → 1–2 warm-up sets → your session → post core (~3 min)",
                 TIMELINE_2],
    "note": "v3 — rebuilt from catalogue rev 13 at the current stages: core + add-ons by target, both legs together (R12), post half as a check",
}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def width(t, size):
    return len(t) * size * 0.5  # reference.md §R4 estimate


class Page:
    def __init__(self, col):
        self.out, self.col, self.texts, self.labels = [], col, [], set()

    def a(self, s=""):
        self.out.append(s)

    def text(self, size, fill, x, y, t, bold=None, middle=False):
        attrs = f'font-size="{size}"' + (f' font-weight="{bold}"' if bold else "") + f' fill="{fill}" x="{x}" y="{y}"'
        if middle:
            attrs += ' text-anchor="middle"'
        self.a(f"<text {attrs}>{esc(t)}</text>")
        w = width(t, size)
        left, right = (x - w / 2, x + w / 2) if middle else (x, x + w)
        self.texts.append((y, x, size, bold, left, right, t))

    def check(self):
        """The width estimate of check_widths.py, run before writing (Stage 2 §2.2 · R64)."""
        bad = []
        col_ys = {y for y, x, *_ in self.texts if self.col <= x < 650}
        for y, x, size, bold, left, right, t in self.texts:
            if right > 650 or left < 30:
                bad.append(f"EDGE y={y} {right:.0f}: {t}")
            if x == 72 and size == 11 and y in col_ys and right > self.col - 6:
                bad.append(f"TEXT>COL y={y} {right:.0f}: {t}")
            if x == 72 and size == 12 and right > self.col - 6:
                bad.append(f"TITLE y={y} {right:.0f}: {t}")
            if (y, t) in self.labels and right > 245:
                bad.append(f"INDEX LABEL y={y} {right:.0f}: {t}")
        if bad:
            raise SystemExit("width check failed:\n" + "\n".join(bad))


def section_head(p, y, label, fill, stroke):
    p.a(f'<rect x="30" y="{y}" width="620" height="28" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
    p.text(13, "#ffffff", 340, y + 19, label, bold="600", middle=True)


def sublabel(p, y, label):
    p.text(11, "#555", 50, y, label, bold="500")


def card(p, y, c, dashed):
    cid, colour, row, title, lines, dose = c
    bar, fill, stroke, tcol, xcol = PAL[colour]
    h = 73
    p.a(f"<!-- {cid}. {title} ({row}) — y={y}, h={h} -->")
    p.a(f'<rect x="30" y="{y}" width="8" height="{h}" rx="2" fill="{bar}"/>')
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    p.a(f'<rect x="38" y="{y}" width="612" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="0.8"{dash}/>')
    p.text(11, "#555", 54, y + 14, cid, bold="500", middle=True)  # centred: P10–P12 clear the title at x 72
    p.text(12, tcol, 72, y + 14, title, bold="500")
    assert len(lines) == 3, cid
    for i, ln in enumerate(lines):
        p.text(11, xcol, 72, y + 29 + 15 * i, ln)
    for i, d in enumerate(dose):
        if i == 0:
            p.text(12, tcol, p.col, y + 14, d, bold="500")
        else:
            p.text(11, xcol, p.col, y + 14 + 15 * i, d)
    p.a("")
    return y + h


def cards(p, y, label, items, dashed):
    sublabel(p, y + 22, label)
    y += 32
    for c in items:
        y = card(p, y, c, dashed) + 6
    return y - 6


def build(f):
    p = Page(f["col"])
    a = p.a
    a("")
    p.text(15, "#1a1a1a", 340, 28, f["title"], bold="500", middle=True)
    p.text(11, "#666", 340, 44, f["subtitle"], middle=True)
    a("")
    a("<!-- LEGEND -->")
    a('<rect x="30" y="54" width="620" height="56" rx="6" fill="#f7f7f7" stroke="#ccc" stroke-width="0.8"/>')
    p.text(11, "#1a1a1a", 50, 72, "Target area — dashed cards are add-ons", bold="500")
    x = 50
    for colour, label in f["legend"]:
        a(f'<rect x="{x}" y="80" width="10" height="10" rx="2" fill="{PAL[colour][0]}"/>')
        p.text(11, "#333", x + 16, 90, label)
        x = int(x + 16 + width(label, 11) + 18)
    a("")
    a("<!-- PRINCIPLE -->")
    a('<rect x="30" y="120" width="620" height="68" rx="8" fill="#fff3e0" stroke="#e8a020" stroke-width="1"/>')
    p.text(12, "#8b5e00", 50, 139, PRINCIPLE[0], bold="500")
    for i, ln in enumerate(PRINCIPLE[1:]):
        p.text(11, "#9e6e10", 50, 156 + 13 * i, ln)
    a("")
    a("<!-- ══════════════════════════════════════ -->")
    a("<!-- PRE-WORKOUT: JOINT CONTROL -->")
    a("<!-- ══════════════════════════════════════ -->")
    a("")
    section_head(p, 204, f["pre_head"], "#2a7a5a", "#1a5a3a")
    a("")
    p.text(10, "#888", 50, 248, f["pre_goal"])
    a("")
    y = cards(p, 248, "Core — every session", f["pre_core"], False)
    y = cards(p, y, "Add-ons — pick by your session's targets", f["pre_add"], True)
    a("<!-- ══════════════════════════════════════ -->")
    a("<!-- POST-WORKOUT: JOINT CHECK -->")
    a("<!-- ══════════════════════════════════════ -->")
    a("")
    y += 20
    section_head(p, y, f["post_head"], "#1a5c8a", "#0e3d5c")
    a("")
    p.text(10, "#888", 50, y + 44, POST_GOAL)
    a("")
    y = cards(p, y + 44, "Core — every session", f["post_core"], False)
    y = cards(p, y, "Add-ons — when your session calls for them", f["post_add"], True)
    # breathing note
    y += 20
    a("<!-- BREATHING NOTE -->")
    a(f'<rect x="30" y="{y}" width="620" height="44" rx="8" fill="#e8f4fd" stroke="#5aabf0" stroke-width="1"/>')
    p.text(12, "#1a5c8a", 50, y + 17, BREATH[0], bold="500")
    p.text(11, "#2272a8", 50, y + 34, BREATH[1])
    a("")
    y += 44 + 14
    # target index
    n = len(f["index"])
    h = 20 * n + 40
    a("<!-- TARGET INDEX -->")
    a(f'<rect x="30" y="{y}" width="620" height="{h}" rx="6" fill="#f7f7f7" stroke="#ccc" stroke-width="0.8"/>')
    p.text(12, "#1a1a1a", 50, y + 20, "Target index — what each drill prepares; pick add-ons by your session", bold="500")
    for i, (colour, label, ids) in enumerate(f["index"]):
        p.text(11, PAL[colour][0], 50, y + 40 + 20 * i, label, bold="500")
        p.labels.add((y + 40 + 20 * i, label))
        p.text(11, "#444", 250, y + 40 + 20 * i, ids)
    a("")
    y += h + 12
    # self-check
    n = len(f["check"])
    h = 18 * n + 42
    a("<!-- SELF-CHECK -->")
    a(f'<rect x="30" y="{y}" width="620" height="{h}" rx="6" fill="#f7f7f7" stroke="#ccc" stroke-width="0.8"/>')
    p.text(12, "#1a1a1a", 50, y + 22, f["check_head"], bold="500")
    for i, (colour, ln) in enumerate(f["check"]):
        a(f'<rect x="50" y="{y + 32 + 18 * i}" width="7" height="7" rx="1" fill="{PAL[colour][0]}"/>')
        p.text(11, "#444", 64, y + 40 + 18 * i, ln)
    a("")
    y += h + 12
    # rules
    n = len(f["rules"])
    h = 20 * n + 48
    a("<!-- hEDS RULES -->")
    a(f'<rect x="30" y="{y}" width="620" height="{h}" rx="6" fill="#f7f7f7" stroke="#ccc" stroke-width="0.8"/>')
    p.text(12, "#1a1a1a", 50, y + 22, "Every drill, every session — hEDS / HSD rules", bold="500")
    for i, ln in enumerate(f["rules"]):
        a(f'<rect x="50" y="{y + 32 + 20 * i}" width="7" height="7" rx="1" fill="#e8a020"/>')
        p.text(11, "#444", 64, y + 40 + 20 * i, ln)
    a("")
    y += h + 12
    # timeline
    a("<!-- TIMING SUMMARY -->")
    a(f'<rect x="30" y="{y}" width="620" height="66" rx="8" fill="#e8f4fd" stroke="#5aabf0" stroke-width="1"/>')
    p.text(12, "#1a5c8a", 50, y + 20, "Session timeline", bold="500")
    for i, ln in enumerate(f["timeline"]):
        p.text(11, "#2272a8", 50, y + 37 + 17 * i, ln)
    a("")
    y += 66 + 20
    a("<!-- VERSION NOTE -->")
    assert f["note"].startswith(f"v{f['version']} — ")
    p.text(9, "#aaa", 340, y, f["note"], middle=True)
    a("")
    p.check()
    head = f'<svg width="100%" viewBox="0 0 680 {y + 16}" xmlns="http://www.w3.org/2000/svg" style="font-family: sans-serif;">'
    return "\n".join([head] + p.out + ["</svg>"]) + "\n"


def main():
    out = sys.argv[1]
    for f in (UPPER, LOWER):
        ids = [c[0] for k in ("pre_core", "pre_add", "post_core", "post_add") for c in f[k]]
        assert len(ids) == len(set(ids)), f["stem"]
        svg = build(f)
        path = os.path.join(out, f["stem"] + ".svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(svg)
        print(path, f"v{f['version']}", len(ids), "cards:", " ".join(ids))


if __name__ == "__main__":
    main()
