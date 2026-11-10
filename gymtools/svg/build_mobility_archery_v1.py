"""Build the archery-day mobility file from the data below (Stage 2 §2.1 · R55; register: build script).

Run from the Gym folder:  python3 -B gymtools/svg/build_mobility_archery_v1.py <out_dir>
Writes <out_dir>/stretching_archery_hEDS.svg (v1). Copy it into gymplan/ and cp it to gymtxt/stretching_archery_hEDS.txt
(Stage 2 R57); never write straight into gymplan/.

Copied from build_mobility_v2.py on 2026-11-10 (Harry: O1 A, O2 A, O3 A, O5 A): the same form and drawing code — 680 px page,
legend, principle box, a PRE and a POST section of core cards plus dashed add-ons, ID centred at x 54, title at x 72, dose
column at x 510, then the breathing note, target index, self-check, rules and timeline boxes, and the version note last.
The section labels, index, rules and timeline headings are data here, so this file can speak of practices and ends; the
v2 defaults are kept for its two files, which this script does not build.
A sport-day file, not a region-wide menu: a pre half before the first end and a post half after the last, both at the range
(O3 A), with one light band, a wall and a chair; floor work only as an add-on. Drills, not working sets: no sets are counted
and the file names no sport (Stage 0 §2.3 · R21); built under a deviation logged in gymstate/block_02.json (O1 A), since
Stage 0 §2.7 and Stage 2 §3.1 know mobility only around training sessions. The drills follow ExerciseCatalogue rev 23,
screened at block 02's loading stages: shoulder, elbow and wrist at 2; spine, hip, knee and ankle at 1. When a joint changes
stage, re-screen the rows, edit the data in a copy of this script, raise the version, rebuild and run the checks in
gymtools/README.md (Stage 2 R55 · R66).
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
ARCHERY = {
    "stem": "stretching_archery_hEDS", "version": 1, "col": 510,
    "title": "Mobility protocol — archery day (hEDS / HSD safe)",
    "subtitle": "Pre: joint control before your first end · Post: joint check after your last end · active drills only (R7)",
    "legend": [("teal", "Shoulder / cuff"), ("brown", "Scapula / upper back"), ("red", "Spine / neck"),
               ("navy", "Wrist / hand"), ("purple", "Ankles / breathing")],
    "pre_head": "PRE-SHOOTING — joint control  (core ~10 min · before your first end)",
    "pre_goal": "Core: every practice, in order · Add-ons: when the day calls for them · kit: a light band, a wall, a chair",
    "core_label": "Core — every practice, in this order",
    "pre_add_label": "Add-ons — when the day calls for them",
    "post_add_label": "Add-ons — when you need them",
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
         ["Rear delts · rhomboids · mid-trap — the muscles that pull the string back",
          "Hands stop in line with the shoulders, never behind the torso (R1)",
          "Elbows soft (R2); shoulder blades come together without a shrug (R8)"],
         ["2 × 8 reps", "3 s hold each rep", "light band"]),
        ("P5", "brown", "C099", "Scapular push-up hold, standing (fists on a wall at shoulder height)",
         ["Serratus anterior · lower trap — the bow arm's shoulder position",
          "Feet a step back, fists on the wall at shoulder height; wrists straight (R2)",
          "Push the shoulder blades apart ~80% and down; elbows soft, ~15° short of straight (R1 · R2)"],
         ["3 × 10 s hold", "standing", "wall"]),
        ("P6", "red", "C135", "Seated thoracic rotation, arms crossed",
         ["Upper-back rotation · obliques",
          "Sit tall on a chair or bench, arms crossed on the chest, pelvis still",
          "Turn the upper back to ~70–80% of the range and pause 2 s; no bounce; spine at stage 1 (R1 · R3 · R7)"],
         ["5 each side", "2 s pause", "seated"]),
        ("P7", "red", "C109", "Neck rotation holds, both hands resisting",
         ["Neck stabilisers — your head stays turned to the target every shot",
          "Both hands stacked on the side of the head; turn into them ~20%",
          "The head stays still; the hands only resist, never push the head further (R7)"],
         ["5 s each way", "× 2 rounds", "seated"]),
        ("P8", "navy", "C098", "Wrist CARs, both wrists together + palm press in 4 directions",
         ["Wrist capsule · forearm flexors and extensors — bow hand and draw hand",
          "Forearms on your thighs; both wrists circle slowly, ~70–80% of range",
          "Then palm into palm: bend up · bend down · thumb side · little-finger side, ~20–30% each"],
         ["5 circles each way", "+ 5 s × 4 directions", "seated"]),
        ("P9", "navy", "C150", "Finger tendon glides, both hands together",
         ["Finger flexors and extensors — the draw fingers' hook and release",
          "Forearms on your thighs, wrists straight; both hands move together (R12)",
          "Straight → hook → tabletop → soft fist → straight; never a tight fist, never bent backwards (R1 · R2)"],
         ["5 slow cycles", "~2 s per position", "seated"]),
    ],
    "pre_add": [
        ("P10", "brown", "C108", "Prone Y-T-W holds",
         ["Lower and mid trap · rhomboids · back of the cuff — floor or mat only",
          "Face down, chest on the floor, thumbs up; no shrug (R8)",
          "Y short of end range · T at the shoulder line · W with the arms angled, not spread wide (R1)"],
         ["1 round", "8 s each letter", "body weight"]),
        ("P11", "purple", "C112", "Ankle CARs, both feet together (seated)",
         ["Ankle capsule · calves — after long standing or on a cold day",
          "Seated, both feet lifted; both ankles circle slowly together (R12)",
          "The biggest circle you control, short of end range; note any catching (R1 · R7)"],
         ["5 each direction", "~10 s per circle", "seated"]),
    ],
    "post_head": "POST-SHOOTING — joint check and wind-down  (core ~3 min · after your last end)",
    "post_core": [
        ("S1", "teal", "C097", "Shoulder CARs, slow scan, both arms together",
         ["Joint check: compare with P1",
          "One slow circle each way; note any new catch, click or looseness",
          "Worse than in P1 → note it in the step-gate log; a loose shoulder ends the drill (§2.6 · R9)"],
         ["1 each direction", "~45 s per circle"]),
        ("S2", "navy", "C098", "Wrist CARs, slow scan, both wrists together",
         ["Joint check: compare with P8",
          "Forearms on your thighs; 3 slow circles each way, ~70–80% of range",
          "New catching or pain compared with P8 → note it in the step-gate log (§2.6)"],
         ["3 each direction", "seated"]),
        ("S3", "navy", "C150", "Finger tendon glides, slow scan",
         ["Joint check: compare with P9",
          "3 slow cycles, both hands together; note any new catching, locking or pain",
          "Worse than in P9 → note it in the step-gate log (§2.6)"],
         ["3 slow cycles", "seated"]),
    ],
    "post_add": [
        ("S4", "navy", "C105", "Biceps hold, both palms pressing forward (uprights or doorway)",
         ["Biceps · brachialis — if the draw arm feels tight; foam rolling first (R7)",
          "Facing a doorway: palms forward against the frame, arms at your sides (R5)",
          "Elbows at ~140–150°; press forward ~30% and hold, both arms together (R1 · R12)"],
         ["2 × 15 s hold", "doorway"]),
        ("S5", "purple", "C110", "90/90 breathing (feet on the bench or wall)",
         ["Diaphragm · deep core — winding down, at home after practice",
          "On your back, hips and knees at 90°, feet resting on a chair, bench or wall",
          "Breathe in 4 s through the nose, ribs widen · out 8 s, ribs drop; easy, unforced"],
         ["5 breaths", "4 s in / 8 s out", "~1 min"]),
    ],
    "index_head": "Target index — what each drill prepares for the shot",
    "index": [
        ("teal", "Shoulder capsule / cuff", "P1 · P2 · P3 · post S1"),
        ("brown", "Draw side: blades back", "P4 · add-on P10"),
        ("brown", "Bow arm: blade forward and down", "P5"),
        ("navy", "Elbow · biceps", "P5 (soft elbow) · post add-on S4"),
        ("red", "Upper back / trunk", "P6"),
        ("red", "Neck", "P7"),
        ("navy", "Wrist · forearm", "P8 · post S2"),
        ("navy", "Fingers", "P9 · post S3"),
        ("purple", "Ankles / long standing", "add-on P11"),
        ("purple", "Ribcage / winding down", "post add-on S5"),
    ],
    "check_head": "Before vs after — log any change with the step gate (§2.6)",
    "check": [
        ("teal", "Shoulders: S1 vs P1 — any new click, catch or looseness?"),
        ("navy", "Wrists and fingers: S2 vs P8 and S3 vs P9 — any new catching, locking or pain?"),
        ("brown", "Worse after a drill → log it and leave that drill out next practice"),
        ("red", "Day after archery: a training session runs only if that morning's step gate passes (R21)"),
    ],
    "rules_head": "Every drill, every practice — hEDS / HSD rules",
    "rules": [RULE_ACTIVE, RULE_RANGE, RULE_CARS,
              "Both arms or both hands together on every drill: one-arm work waits for loading stage 3 (R12)",
              "Spine at stage 1: the trunk turns only part-way, ribs down, pelvis still (R3)",
              RULE_LIGHT,
              "A joint feels loose or unstable → stop that drill; loose joints that day → skip the drills (R9)"],
    "timeline_head": "Practice-day timeline",
    "timeline": ["Pre core (~10 min) → add-ons if needed → your shooting warm-up → practice → post core (~3 min)",
                 "Drills, not working sets: no sets counted (§2.3); tightness after practice → foam rolling (R7)"],
    "note": "v1 — new: archery-day mobility, a pre half before the first end and a post half after the last (catalogue rev 23)",
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
    y = cards(p, 248, f.get("core_label", "Core — every session"), f["pre_core"], False)
    y = cards(p, y, f.get("pre_add_label", "Add-ons — pick by your session's targets"), f["pre_add"], True)
    a("<!-- ══════════════════════════════════════ -->")
    a("<!-- POST-WORKOUT: JOINT CHECK -->")
    a("<!-- ══════════════════════════════════════ -->")
    a("")
    y += 20
    section_head(p, y, f["post_head"], "#1a5c8a", "#0e3d5c")
    a("")
    p.text(10, "#888", 50, y + 44, POST_GOAL)
    a("")
    y = cards(p, y + 44, f.get("core_label", "Core — every session"), f["post_core"], False)
    y = cards(p, y, f.get("post_add_label", "Add-ons — when your session calls for them"), f["post_add"], True)
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
    p.text(12, "#1a1a1a", 50, y + 20, f.get("index_head", "Target index — what each drill prepares; pick add-ons by your session"), bold="500")
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
    p.text(12, "#1a1a1a", 50, y + 22, f.get("rules_head", "Every drill, every session — hEDS / HSD rules"), bold="500")
    for i, ln in enumerate(f["rules"]):
        a(f'<rect x="50" y="{y + 32 + 20 * i}" width="7" height="7" rx="1" fill="#e8a020"/>')
        p.text(11, "#444", 64, y + 40 + 20 * i, ln)
    a("")
    y += h + 12
    # timeline
    a("<!-- TIMING SUMMARY -->")
    a(f'<rect x="30" y="{y}" width="620" height="66" rx="8" fill="#e8f4fd" stroke="#5aabf0" stroke-width="1"/>')
    p.text(12, "#1a5c8a", 50, y + 20, f.get("timeline_head", "Session timeline"), bold="500")
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
    for f in (ARCHERY,):
        ids = [c[0] for k in ("pre_core", "pre_add", "post_core", "post_add") for c in f[k]]
        assert len(ids) == len(set(ids)), f["stem"]
        svg = build(f)
        path = os.path.join(out, f["stem"] + ".svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(svg)
        print(path, f"v{f['version']}", len(ids), "cards:", " ".join(ids))


if __name__ == "__main__":
    main()
