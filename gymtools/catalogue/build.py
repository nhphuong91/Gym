"""Build ExerciseCatalogue.json and its .md mirror from rows.py + vocab.py, with validation.

Run: python3 -B build.py <out_dir> [<previous ExerciseCatalogue.json>]
The second argument adds the change-from-previous-revision table. rows.py, vocab.py and REVISIONS hold
revision 12 (2026-10-25): with the revision 11 JSON as the second argument the output is byte-identical
to gymspec/ExerciseCatalogue.json rev 12. gymspec/ is the source of truth: before a new revision, check that
rows.py still matches it (gymtools/README.md), add a REVISIONS entry, then build and run verify.py.
"""
import json
import re
import sys
import unicodedata

from vocab import (MUSCLES, AVOID_DAY_BEFORE, CARRYOVER, JOINTS, STATIONS, EQUIPMENT,
                   KINDS, STATUS, SOURCES)
from rows import ROWS

BUILT = "2026-10-02"
SCHEMA = "stage1-exercise-catalogue/1"
HYP_HOLD_MUSCLES = {"abs", "obliques", "forearm_flexors", "forearm_extensors", "forearm_rotators"}

FIELDS = ["id", "key", "name", "kind", "region", "pattern", "prime_mover", "indirect", "zone", "compound",
          "stations", "equipment", "joints", "status", "unlock", "excluded_by", "excluded_why",
          "replaced_by", "cues", "warnings", "hyp_set", "day_after", "sport_notes", "alt_candidates",
          "targets", "source", "corpus", "used_in", "changed", "basis", "notes", "attention"]

REVISIONS = [
    {
        "n": 12,
        "date": "2026-10-25",
        "note": "L options for the front delt, rear delt and abs (the L search, Stage 1 D-15)",
        "changes": [
            "Harry asked for an L exercise for each upper-body priority target that had none (front delt, rear delt, upper back, abs) and "
            "confirmed three (Stage 1 §3.2 · D-08 · D-15): C139, the supine dumbbell front raise on the floor, open, as the floor stops the "
            "arms at the torso line and the shoulder is never loaded in extension (R5); C140, the side-lying dumbbell rear delt raise on the "
            "floor, locked until shoulder and elbow stage 3, as one arm works alone (R12); C141, the crunch over the foam roller, locked "
            "until spine stage 2, as loaded spinal extension waits for full range (Stage 1 [W63]).",
            "The upper back has no L with the kit: cable rows from full protraction keep an even pull, so M (C035); dumbbell, barbell and "
            "band rows peak at the top, so S (Stage 1 [W64]).",
        ],
    },
    {
        "n": 11,
        "date": "2026-10-13",
        "note": "provenance from the v8 upper focus files",
        "changes": [
            "The three upper-body focus files were rebuilt as v8: every exercise now sits in a superset that passes Stage 1 R38, with no "
            "straight sets (R39). The rows they use cite v8; the v7 lines stay as history, like v6's.",
            "C037, the bent-over wide DB row, is focus A's second alternative for the wide-grip cable row in place of the chest-supported row, "
            "which needs the bench the Smith press holds during that superset (Stage 0 §1.3; T16).",
        ],
        "diff": {"locked": [], "opened": [], "bilateral": [], "end_range": [], "holds": [], "added": [], "replaced": [], "unlock_path": [], "locked_range": [], "corpus_fixed": [], "cues": [], "provenance_v8": ["C001", "C002", "C005", "C006", "C009", "C012", "C016", "C017", "C018", "C024", "C026", "C027", "C028", "C029", "C030", "C031", "C035", "C036", "C037", "C038", "C039", "C040", "C042", "C045", "C046", "C049", "C050", "C051", "C053", "C060", "C134", "C138"]},
    },
    {
        "n": 10,
        "date": "2026-10-13",
        "note": "upper-body stage 2: cues, the two-arm front raise, provenance from the v7 upper focus files",
        "changes": [
            "Harry passed the upper-body loading-gate tests: shoulder, elbow, wrist and spine are at loading stage 2 (Stage 0 §2.5 · R14). "
            "The rows whose cues gave only the stage-1 limit now also say what applies from stage 2: overhead elevation, external rotation, "
            "the shoulder CARs and the low-back range (T15). Statuses are unchanged: the catalogue stays screened at the default Current state, "
            "and plans re-check against the actual one (§6, method 13).",
            "'(R12 at stage 1)' now reads '(R12 until stage 3)': one-limb work stays locked at stage 2 (Stage 0 R12 · §2.5; T15).",
            "C138, the two-arm dumbbell front raise, added once Harry confirmed it (Stage 1 §3.2 · D-08; T14): the front delt had no row, and the "
            "new upper-body block makes it a priority target. Overhead pressing waits: rehabilitation for unstable shoulders trains the front delt "
            "with flexion raises first (Stage 1 [W59] · [W60]).",
            "The three upper-body focus files were rebuilt as v7 for the new block; the rows they use cite them. 'Proposed' and 'confirmed' now "
            "mean not taken from the routine files, since some of those rows are now used in them (§4).",
        ],
        "diff": {"locked": [], "opened": [], "bilateral": [], "end_range": [], "holds": [], "added": ["C138"], "replaced": [], "unlock_path": [], "locked_range": [], "corpus_fixed": [], "cues_stage2": ["C003", "C004", "C005", "C008", "C009", "C010", "C012", "C016", "C017", "C018", "C020", "C028", "C029", "C036", "C037", "C038", "C039", "C040", "C041", "C046", "C047", "C049", "C050", "C051", "C052", "C053", "C054", "C056", "C057", "C058", "C059", "C064", "C065", "C067", "C072", "C073", "C074", "C075", "C076", "C084", "C085", "C086", "C092", "C096", "C097", "C098", "C100", "C101", "C105", "C106", "C108", "C112", "C115", "C117", "C119"], "provenance": ["C001", "C002", "C005", "C006", "C009", "C012", "C016", "C017", "C018", "C024", "C026", "C027", "C028", "C029", "C030", "C031", "C035", "C036", "C038", "C039", "C040", "C042", "C045", "C046", "C049", "C050", "C051", "C053", "C060", "C134"]},
    },
    {
        "n": 9,
        "date": "2026-10-06",
        "note": "the prone W as Harry holds it (T13)",
        "changes": [
            "Harry (T13): in the prone Y-T-W holds he keeps the W's arms at an angle, not spread wide, so his shoulders stay within 45° of external "
            "rotation. C108 cues the W that way at shoulder stage 1 (Stage 0 §2.5 · D-63) and stays open.",
        ],
        "diff": {"cues": ["C108"]},
    },
    {
        "n": 8,
        "date": "2026-10-06",
        "note": "vertical-pull grips at shoulder stage 1; provenance after the walkthrough's re-run",
        "changes": [
            "A wide grip reaches 45° of external rotation as the hands near the chest (Stage 1 [W56]), the stage-1 cap (Stage 0 §2.5 · D-63). "
            "The lat pulldown, the assisted pull-up and the band pulldown now cue hands about 1.25× shoulder width at shoulder stage 1, and the two "
            "pulldowns a ~30° lean back from the hips (Stage 1 [W57]); lat activation does not change with grip width (Stage 1 [W58]). Any width from stage 2 (T12).",
            "The Smith squat's and the barbell squat's notes now cite Stage 1 R28 and §2.1 S2: the walkthrough (Stage 1 §7) re-ran at every joint "
            "stage 1 and no longer uses them (Stage 1 D-10 · Stage 0 D-70; T11).",
            "No row added for the strength gap at shoulder stage 1: Harry waits for the shoulder control test, and the Smith front squat sits in "
            "Stage 1's backlog (T10).",
        ],
        "diff": {"corpus_fixed": ["C066"], "cues": ["C024", "C027", "C028"]},
    },
    {
        "n": 7,
        "date": "2026-10-06",
        "note": "bar-on-back rows locked (A9)",
        "changes": [
            "Harry (A9): with his long humerus, a bar held on the back takes the shoulders past 45° of external rotation, or the wrists bend heavily "
            "to keep them within it, so a wide grip does not keep it inside stage 1. The Smith squat, the barbell squat to pins and the Smith calf raise "
            "lock until the shoulder reaches stage 2 (Stage 0 §2.5 · D-63 · D-65).",
            "Each names its stage-1 replacement (Stage 1 D-09): the goblet squat for both squats; the deficit calf raise on the step and the standing "
            "calf raise for the Smith calf raise. Until shoulder stage 2, no open quads row takes heavy loads on a mechanical stop (Stage 1 §2.1, S2).",
        ],
        "diff": {"replaced": ["C064", "C066", "C084"], "locked_range": ["C064", "C066", "C084"]},
    },
    {
        "n": 6,
        "date": "2026-10-04",
        "note": "rows re-screened against the stage-1 ranges",
        "changes": [
            "Every row that loads the elbow, shoulder, wrist or spine was re-screened against the stage-1 ranges of Stage 0 §2.5 (D-63…D-66 · D-69). "
            "Cues now state them: elbows 20–30% of their bending range short of straight; arms no higher than ~75% of overhead elevation; "
            "external rotation to 45° or ~75%, whichever is smaller; shoulder extension to neutral; wrists within ~70–80%; "
            "the low back within ~36–42° of flexion and ~12–15° of extension. Each cue also says what applies from stage 2.",
            "Five rows lock until the shoulder reaches stage 2 (D-63), each naming its stage-1 replacement: the pull-up, "
            "the two behind-the-torso curls, the active hang and swimming.",
            "Six rows changed from the corpus ✏️: the spider and hammer curls' 15–20° bottom bend, and four overhead triceps rows held below ~75% of elevation.",
            "Bar-on-back squats stay open on a very wide grip; whether it keeps the shoulders within 45° of external rotation needs checking on video (A9).",
        ],
        "diff": {"replaced": ["C026", "C042", "C047", "C104", "C125"], "locked_range": ["C026", "C042", "C047", "C104", "C125"], "corpus_fixed": ["C041", "C046", "C049", "C050", "C051", "C106"], "cues": ["C001", "C002", "C003", "C004", "C005", "C006", "C007", "C008", "C009", "C010", "C012", "C013", "C014", "C016", "C017", "C018", "C020", "C024", "C025", "C027", "C028", "C029", "C030", "C031", "C032", "C033", "C035", "C036", "C037", "C038", "C039", "C040", "C041", "C043", "C044", "C045", "C046", "C048", "C049", "C050", "C051", "C052", "C053", "C054", "C055", "C056", "C057", "C058", "C059", "C062", "C064", "C066", "C097", "C098", "C099", "C100", "C101", "C102", "C103", "C106", "C108", "C134", "C135"]},
    },
    {
        "n": 5,
        "date": "2026-10-04",
        "note": "control tests for every joint",
        "changes": [
            "The shoulder, elbow, wrist and spine have control tests (Stage 0 §2.5 · D-63…D-66), so every joint now has one: "
            "every locked row shows 'control test exists'. Status is unchanged until Harry passes the tests (R14).",
            "Each joint's stage-1 range now comes from Stage 0 §2.5 (D-63…D-66 · D-69); row cues predating it were re-screened in revision 6.",
        ],
        "diff": {"unlock_path": ["C013", "C014", "C021", "C022", "C034", "C052", "C061", "C063", "C080", "C107"]},
    },
    {
        "n": 4,
        "date": "2026-10-03",
        "note": "stage-1 replacements added; ankle and hip control tests",
        "changes": [
            "Eight replacement rows added once Harry confirmed them (Stage 1 §3.2 · D-08 · D-09; Q9 · Q10): C130–C137 stand in for locked rows "
            "until their joints reach the stage those rows need; the originals then return to the candidates, beside them. "
            "Each locked original names its replacement in replaced_by.",
            "Three entered in fixed form ✏️: hip adduction with two bands, both legs (C133), since a self-resisted squeeze has no failure point "
            "for seconds in reserve (Stage 0 R16 · D-60); popliteus rotation with a band per foot (C136), since a band round both feet resists "
            "turning out, not in; the supine bent-knee leg lift (C137), since seated, the lift ends past R1's range.",
            "The ankle and hip have control tests (Stage 0 §2.5 · D-61 · D-62): rows locked on them show 'control test exists'. "
            "Status is unchanged until Harry passes the tests (R14).",
        ],
        "diff": {"added": ["C130", "C131", "C132", "C133", "C134", "C135", "C136", "C137"], "replaced": ["C061", "C077", "C080", "C082", "C083", "C093", "C094", "C095", "C107", "C113", "C114", "C122", "C123"], "unlock_path": ["C061", "C063", "C069", "C077", "C079", "C080", "C082", "C083", "C090", "C091", "C094", "C095", "C111", "C113", "C114", "C118", "C120", "C121", "C122", "C123", "C127", "C128", "C129"]},
    },
    {
        "n": 3,
        "date": "2026-10-03",
        "note": "Q7 and Q8 applied",
        "changes": [
            "Walking, cycling and swimming confirmed outside R12 (Stage 0 D-59).",
            "Holds are prescribed as sets × hold time + seconds in reserve, each rep in reserve counting as ~4 s (Stage 0 R16 · D-60).",
        ],
    },
    {
        "n": 2,
        "date": "2026-10-03",
        "note": "Harry's answers to the v1 readings applied",
        "changes": [
            "Unilateral loading widened (Stage 0 R12 · D-54): one limb working alone — moving or held, any plane, any load including its own weight — needs loading stage 3. "
            "Single-limb rows lock; rows that can run with both limbs together become bilateral variants.",
            "End-range peaks warned, not excluded (Stage 0 R2 · D-55): the DB kickback returns as an open row; nine rows carry the end-range warning.",
            "Timed holds count as hypertrophy sets for every muscle (Stage 0 §2.2 · D-58).",
            "'Glutes' in badminton's avoid-the-day-before row confirmed as glute max and glute med (Stage 0 §1.2 · D-56).",
            "Knee depth outside squat patterns confirmed (Stage 0 §2.5 · D-57).",
            "New exercises enter only after Harry confirms (Stage 1 §3.2 · D-08); proposed v1 rows are kept for his later review.",
        ],
        "diff": {
            "locked": ["C013", "C014", "C021", "C022", "C061", "C063", "C077", "C079", "C080", "C082", "C093", "C094", "C095", "C107", "C111", "C113", "C114", "C118", "C122", "C123"],
            "opened": ["C056"],
            "bilateral": ["C020", "C097", "C098", "C100", "C105", "C106", "C109", "C112", "C119"],
            "end_range": ["C044", "C056", "C074", "C075", "C076", "C104", "C115", "C116", "C117"],
            "holds": ["C068", "C076", "C080", "C088", "C089"],
        },
    },
]
REVISION = REVISIONS[0]

DECISIONS = {
    "A1": {"title": "Unilateral loading", "decision": "Harry: count also — limb weight, rotation, side-to-side work and holds count", "lands": "Stage 0 R12 · D-54"},
    "A2": {"title": "Timed holds", "decision": "Harry: allow them as hypertrophy sets for all other muscles too", "lands": "Stage 0 §2.2 · D-58 (effort: R16 · D-60)"},
    "A3": {"title": "Dumbbell kickback", "decision": "Harry: warn about end-range peaks, don't exclude", "lands": "Stage 0 R2 · D-55"},
    "A4": {"title": "'Glutes' in badminton's avoid row", "decision": "Harry: confirmed — glute max and glute med", "lands": "Stage 0 §1.2 · D-56"},
    "A5": {"title": "Knee depth outside squat patterns", "decision": "Harry: confirmed", "lands": "Stage 0 §2.5 · D-57"},
    "A6": {"title": "Proposed rows", "decision": "Harry: keep; he reviews them later", "lands": "this catalogue (rows marked A6)"},
    "Q6": {"title": "Exercises missing from the catalogue", "decision": "Harry: check with him before adding", "lands": "Stage 1 §3.2 · D-08"},
    "A7": {"title": "Walking, cycling and swimming under R12", "decision": "Harry (Q7): confirmed — they stay outside R12", "lands": "Stage 0 R12 · D-59"},
    "Q8": {"title": "Effort for a timed hold", "decision": "Harry: A — hold time + seconds in reserve", "lands": "Stage 0 R16 · D-60"},
    "Q9": {"title": "Replacements for locked rows", "decision": "Harry: they replace the locked exercises while the joints sit below the stage those need; from then on, the originals return to the candidates", "lands": "Stage 1 §3.2 · D-09"},
    "Q10": {"title": "Which replacements to add", "decision": "Harry: proceed — all eight (N1–N8), with Claude's three fixes; N4 in its band form (F1 A, Claude's recommendation)", "lands": "this catalogue: C130–C137"},
    "A9": {"title": "Shoulder rotation under a back-squat bar", "decision": "Harry (2026-10-06): with his long humerus, keeping the shoulders within 45° of external rotation bends the wrists heavily, so a bar on the back needs more than stage 1 allows", "lands": "this catalogue: C064, C066, C084 locked until shoulder stage 2; the goblet squat and the deficit and standing calf raises stand in (Stage 1 D-09)"},
    "T10": {"title": "Strength gap at shoulder stage 1", "decision": "Harry (2026-10-06): A — wait for the shoulder control test; no front-squat row for now", "lands": "Stage 1 Supplement §6 (backlog)"},
    "T11": {"title": "Rule examples and the walkthrough after A9", "decision": "Harry (2026-10-06): OK", "lands": "Stage 0 D-70 · Stage 1 D-10; C064 and C066 notes"},
    "T12": {"title": "Shoulder rotation in vertical pulls", "decision": "Harry (2026-10-06): research, no video check", "lands": "this catalogue: C024, C027, C028 grip cues (revision 8)"},
    "T13": {"title": "Shoulder rotation in the prone W", "decision": "Harry (2026-10-06): his W holds the arms at an angle, not spread wide, so external rotation stays within 45°", "lands": "this catalogue: C108 cue (revision 9)"},
    "T14": {"title": "A front-delt row", "decision": "Harry (2026-10-13, O8 A): add the two-arm dumbbell front raise; an overhead press waits for a later block", "lands": "this catalogue: C138 (revision 10)"},
    "T15": {"title": "Cues at upper-body stage 2", "decision": "Harry (2026-10-12, F3): OK — say what applies from stage 2 where a cue gives only the stage-1 limit, and read R12 as 'until stage 3'", "lands": "this catalogue: revision 10"},
    "T16": {"title": "Second alternative for the wide-grip cable row in focus A", "decision": "Harry (2026-10-13, Q4 a): the bent-over wide DB row, since the Smith press holds the bench during that superset", "lands": "this catalogue: C037 provenance (revision 11)"},
}

ATTENTION = {
    "A6": {"title": "Proposed rows, kept for Harry's review",
           "text": "Rows marked 'proposed' are not in the routine files: some are named by the spec (R8, R26, R29, R41 examples; Stage 1 §7), "
                   "the rest fill gaps — abs and obliques, forearms, cuff internal rotation, ankle evertors, the hip machine. Harry keeps them and reviews them later (Q5)."},
}

METHOD = [
    "Pool: every exercise in 12 corpus files — the 8 lifting routines, the popliteus protocol, the 2 mobility protocols and the cardio routine — "
    "primaries, alternatives and drills; duplicates merged into one row listing every source. The 2 foam-rolling files were read and left out: "
    "tissue release, not exercise (Stage 0 §2.7).",
    "Screen: each row is checked against the hard gates (Stage 0 §0.2: R1–R15) at the default Current state, every joint at loading stage 1 "
    "(Stage 0 §4.1). 'joints' records the loading stage each loaded joint needs; status follows: open (all at stage 1), locked (a joint needs "
    "more; every joint has a control test, Stage 0 §2.5 · D-61…D-66, so a locked row opens once Harry passes the tests its joints need, R14), "
    "excluded (fails a gate in every form).",
    "Unilateral (Stage 0 R12 · D-54): one limb working alone — moving or held, in any plane, against an external load, body weight or its own weight — "
    "needs loading stage 3 for every joint of that limb, and a single-leg stance for the stance leg's hip, knee and ankle. Where a drill can run with "
    "both limbs together, the row is the bilateral variant (corpus-fixed ✏️). Walking, cycling and swimming stay outside R12 (D-59).",
    "End-range warning (Stage 0 R2 · D-55): a row whose resistance peaks at the end of a joint's range, the soft bend its only margin, carries the warning.",
    "Holds (kind 'hold') count as hypertrophy sets for any muscle (Stage 0 §2.2 · D-58); a plan prescribes them as sets × hold time + seconds in reserve (Stage 0 R16 · D-60).",
    "New rows enter only after Harry confirms them (Stage 1 §3.2 · D-08). Rows marked 'proposed' were added in v1, before D-08; Harry keeps them for later review (A6). "
    "Rows marked 'confirmed' entered through D-08: the stage-1 replacements C130–C137 (Q9 · Q10) and the two-arm front raise C138 (T14).",
    "Replacements (Stage 1 D-09): a locked row's replaced_by names the open rows that stand in for it until its joints reach the stage it needs; "
    "it then returns to the candidates beside them. An excluded row's replaced_by is permanent. The mirror shows the reverse link as 'Stands in for'.",
    "Cues name the rule they satisfy. Rules that bind every row are not repeated in each: lowering 2–3 s (R25), the in-session abort (R9), "
    "left–right balance (R23), soft bend at every joint (R2) unless the row needs a specific cue.",
    "Zones (Stage 1 R26) label where the resistance peaks in the prime mover's range within the gated range; R26's reference labels are used "
    "as given; every L is truncated by R1; the triceps has no S slot (R27), so the kickback's S label fills no coverage. Mechanics labels carry basis 'mechanics'.",
    "Compound = multi-joint loading; in a plan only compounds produce harvest (Stage 1 R35). Indirect lists meaningful synergists; "
    "an isolation exercise's indirect muscles still collect sets for Stage 0 R19–R21, but give no harvest.",
    "day_after (Stage 0 R21) is computed: each sport whose avoid-the-day-before muscles collect sets in the row (prime or indirect). "
    "Drills and conditioning collect no sets.",
    "alt_candidates (Stage 1 R41) is computed for open station exercises: open rows of the same kind and movement pattern that share none "
    "of its stations — same prime mover first, then the closest zone, rows without a warning, band variants first among equals. "
    "The plan still checks antagonist role and joint angle, and picks two or names the gap.",
    "Plans re-check status against the actual Current state: a row's 'joints' gives the stage each joint needs.",
]

REFS = {
    "Stage 1 [W2]": "Zabaleta-Korta et al. 2023, J Hum Kinet 88:259–70",
    "Stage 1 [W3]": "Kassiano et al. 2025, Int J Sports Med 46(5):334–43",
    "Stage 1 [W6]": "Larsen et al. 2025, Front Physiol 16:1611468",
    "Stage 1 [W7]": "Maeo et al. 2023, Eur J Sport Sci 23(7):1240–50",
    "Stage 1 [W12]": "Kassiano et al. 2023, J Strength Cond Res 37(9):1746–53",
    "Stage 1 [W38]": "Ferrell et al. 2004, Arthritis Rheum 50:3323–28",
    "Stage 1 [W54]": "Maeo et al. 2021, Med Sci Sports Exerc 53(4):825–37, DOI 10.1249/MSS.0000000000002523",
    "Stage 1 [W55]": "Plotkin et al. 2023, Front Physiol 14:1279170, DOI 10.3389/fphys.2023.1279170",
    "Stage 1 [W56]": "Prinold & Bull 2016, J Sci Med Sport 19:629–35, DOI 10.1016/j.jsams.2015.08.002",
    "Stage 1 [W57]": "Fees, Decker, Snyder-Mackler & Axe 1998, Am J Sports Med 26(5), DOI 10.1177/03635465980260052301",
    "Stage 1 [W58]": "Buonsenso et al. 2025, J Funct Morphol Kinesiol 10(3):345, DOI 10.3390/jfmk10030345",
    "Stage 1 [W59]": "Watson, Warby, Balster, Lenssen & Pizzari 2017, Shoulder Elbow 9(1):46–53, DOI 10.1177/1758573216652087",
    "Stage 1 [W60]": "Watson, Pizzari, Balster, Lenssen & Warby 2022, J Clin Med 11(17):5140, DOI 10.3390/jcm11175140",
    "Stage 1 [W61]": "Strey, Irigoyen, McMahon & Pinto 2026, Sport Sci Health 22(1):33, DOI 10.1007/s11332-025-01586-5",
    "Stage 1 [W62]": "Wikipedia, Rear delt raise, checked 2026-10-25",
    "Stage 1 [W63]": "Russek, Hypermobility 104: Exercise Selection and Progression for HSD/hEDS and POTS, Clarkson University slides",
    "Stage 1 [W64]": "Pre-Script, Maximize back development using grip width and arm angle (blog)",
    "Stage 1 [W65]": "Escamilla et al. 2006, J Orthop Sports Phys Ther 36(2):45–57, DOI 10.2519/jospt.2006.36.2.45",
    "Stage 0 [W51]": "Mittal et al. 2021, GEAR program, Front Rehabil Sci, DOI 10.3389/fresc.2021.769792",
    "Stage 0 [W75]": "Hou et al. 2023, BMC Musculoskelet Disord 24:71, DOI 10.1186/s12891-023-06179-2",
}


def fail(msg):
    raise SystemExit("VALIDATION FAILED: " + msg)


def used_in(corpus):
    out = []
    for c in corpus:
        if c.startswith("routine_"):
            tag = "lifting"
        elif c.startswith("popliteus"):
            tag = "joint protocol"
        elif c.startswith("stretching_"):
            tag = "mobility"
        elif c.startswith("cardio"):
            tag = "cardio"
        else:
            fail("unknown corpus file: " + c)
        if tag not in out:
            out.append(tag)
    return out


def build():
    keys = [r["key"] for r in ROWS]
    if len(keys) != len(set(keys)):
        fail("duplicate keys")
    ids = {r["key"]: f"C{i:03d}" for i, r in enumerate(ROWS, 1)}
    rows = []
    for r in ROWS:
        k = r["key"]
        kind = r["kind"]
        if kind not in KINDS:
            fail(f"{k}: kind {kind}")
        prime = r.get("prime")
        indirect = list(r.get("indirect", []))
        if kind in ("resistance", "hold"):
            if prime not in MUSCLES:
                fail(f"{k}: prime {prime}")
            for m in indirect:
                if m not in MUSCLES or m == prime:
                    fail(f"{k}: indirect {m}")
            region = MUSCLES[prime][3]
            if r.get("compound") is None:
                fail(f"{k}: compound missing")
            if not r.get("pattern"):
                fail(f"{k}: pattern missing")
        else:
            if prime or indirect:
                fail(f"{k}: drills/conditioning carry no prime or indirect")
            region = r.get("region")
        stations = list(r.get("stations", []))
        equipment = list(r.get("equipment", []))
        for s in stations:
            if s not in STATIONS:
                fail(f"{k}: station {s}")
        for e in equipment:
            if e not in EQUIPMENT:
                fail(f"{k}: equipment {e}")
        joints = r.get("joints", [])
        for j in joints:
            if j["joint"] not in JOINTS or not 1 <= j["needs"] <= 4:
                fail(f"{k}: joint {j}")
            if j["needs"] > 1 and "note" not in j:
                fail(f"{k}: joint {j['joint']} needs a note")
        excluded_by = r.get("excluded_by")
        if excluded_by:
            status = "excluded"
            unlock = None
            if not r.get("excluded_why") or not r.get("replaced_by"):
                fail(f"{k}: excluded row needs excluded_why and replaced_by")
        else:
            maxneed = max([j["needs"] for j in joints] or [1])
            status = "open" if maxneed == 1 else "locked"
            unlock = None
            if status == "locked":
                parts = []
                for j in joints:
                    if j["needs"] > 1:
                        test = "control test exists" if JOINTS[j["joint"]] else "no control test yet, so it stays locked until one is added (R14)"
                        parts.append(f"{j['joint']} → stage {j['needs']}, {test}")
                unlock = "; ".join(parts)
        zone = r.get("zone")
        if zone not in ("L", "M", "S", None):
            fail(f"{k}: zone {zone}")
        if kind in ("resistance", "hold") and status == "open" and zone is None:
            fail(f"{k}: open resistance row needs a zone")
        source = r.get("source")
        if source not in SOURCES:
            fail(f"{k}: source {source}")
        corpus = list(r.get("corpus", []))
        if source in ("corpus", "corpus-fixed") and not corpus:
            fail(f"{k}: corpus row without provenance")
        if source == "corpus-fixed" and not r.get("changed"):
            fail(f"{k}: corpus-fixed row without 'changed'")
        if not r.get("basis"):
            fail(f"{k}: basis missing")
        # hypertrophy-set flag
        hyp_set = None
        attention = r.get("attention") or []
        if isinstance(attention, str):
            attention = [attention]
        attention = list(attention)
        if kind == "resistance":
            hyp_set = True
        elif kind == "hold":
            hyp_set = True  # Stage 0 §2.2 · D-58
        if source == "proposed" and "A6" not in attention:
            attention.append("A6")
        for a in attention:
            if a not in ATTENTION:
                fail(f"{k}: attention {a}")
        attention.sort()
        # day after (R21)
        day_after = []
        if kind in ("resistance", "hold") and status != "excluded":
            collected = [prime] + indirect
            for sport, spec in AVOID_DAY_BEFORE.items():
                hit = [m for m in collected if m in spec["muscles"]]
                if hit:
                    day_after.append({"sport": sport, "muscles": hit})
        # sport notes
        sport_notes = {}
        for sport, d in (r.get("sport") or {}).items():
            out = {}
            if d.get("carryover"):
                for tag in d["carryover"]:
                    if tag not in CARRYOVER[sport]:
                        fail(f"{k}: carryover tag {sport}/{tag}")
                out["carryover"] = [CARRYOVER[sport][t] for t in d["carryover"]]
            if d.get("conflicts"):
                out["conflicts"] = d["conflicts"]
            if out:
                sport_notes[sport] = out
        row = {
            "id": ids[k], "key": k, "name": r["name"], "kind": kind, "region": region, "pattern": r.get("pattern"),
            "prime_mover": prime, "indirect": indirect, "zone": zone,
            "compound": r.get("compound") if kind in ("resistance", "hold") else None,
            "stations": stations, "equipment": equipment, "joints": joints,
            "status": status, "unlock": unlock,
            "excluded_by": excluded_by or [], "excluded_why": r.get("excluded_why"),
            "replaced_by": [ids[x] if x in ids else fail(f"{k}: replaced_by {x}") for x in r.get("replaced_by", [])],
            "cues": list(r.get("cues", [])), "warnings": list(r.get("warnings", [])),
            "hyp_set": hyp_set, "day_after": day_after, "sport_notes": sport_notes,
            "alt_candidates": [],
            "targets": r.get("targets"),
            "source": source, "corpus": corpus, "used_in": used_in(corpus),
            "changed": r.get("changed"), "basis": list(r.get("basis", [])), "notes": r.get("notes"),
            "attention": attention,
        }
        rows.append(row)
    by_id = {x["id"]: x for x in rows}
    # replaced_by targets must be open
    for x in rows:
        for t in x["replaced_by"]:
            if by_id[t]["status"] != "open":
                fail(f"{x['id']}: replaced_by {t} is not open")
    # alternatives (R41)
    for x in rows:
        if x["status"] != "open" or x["kind"] not in ("resistance", "hold") or not x["stations"]:
            continue
        cands = [y for y in rows if y is not x and y["status"] == "open" and y["kind"] == x["kind"]
                 and y["pattern"] == x["pattern"] and not set(y["stations"]) & set(x["stations"])]
        zd = {("L", "L"): 0, ("M", "M"): 0, ("S", "S"): 0, ("L", "M"): 1, ("M", "L"): 1, ("M", "S"): 1, ("S", "M"): 1, ("L", "S"): 2, ("S", "L"): 2}
        cands.sort(key=lambda y: (y["prime_mover"] != x["prime_mover"], zd[(x["zone"], y["zone"])], bool(y["warnings"]),
                                  not ("bands" in y["equipment"] and not y["stations"]), y["id"]))
        x["alt_candidates"] = [f"{y['id']} ({y['zone']})" for y in cands[:4]]
    # rule references valid (R1–R48)
    text = json.dumps(rows, ensure_ascii=False)
    for m in re.findall(r"\bR(\d+)\b", text):
        if not 1 <= int(m) <= 48:
            fail(f"rule R{m} does not exist")
    # field order
    for x in rows:
        if list(x.keys()) != FIELDS:
            fail(f"{x['id']}: field order")
    return rows


def catalogue(rows):
    vocab = {
        "muscles": [{"id": k, "name": v[0], "covers": v[1], "group": v[2], "region": v[3]} for k, v in MUSCLES.items()],
        "avoid_day_before": AVOID_DAY_BEFORE,
        "carryover": CARRYOVER,
        "joints": [{"id": k, "control_test": v} for k, v in JOINTS.items()],
        "patterns": sorted({x["pattern"] for x in rows if x["pattern"]}),
        "stations": STATIONS, "equipment": EQUIPMENT,
        "kinds": KINDS, "status": STATUS, "sources": SOURCES,
    }
    counts = {s: sum(1 for x in rows if x["status"] == s) for s in STATUS}
    src = {s: sum(1 for x in rows if x["source"] == s) for s in SOURCES}
    return {
        "schema": SCHEMA,
        "encoding": "NFC",
        "status": "non-normative, draft",
        "built": BUILT,
        "revisions": REVISIONS,
        "governed_by": "Stage0_PolicyDefinition.md (hard gates) · Stage1_Programming.md §3.2 (exercise facts) · Stage 1 D-03",
        "screened_against": "default Current state: every joint at loading stage 1 (Stage 0 §4.1)",
        "summary": {"rows": len(rows), "status": counts, "source": src},
        "fields": FIELDS,
        "method": METHOD,
        "decisions": DECISIONS,
        "attention": ATTENTION,
        "references": REFS,
        "vocabulary": vocab,
        "rows": rows,
    }


# ───────────────────────── Markdown mirror ─────────────────────────

EQ_SHORT = {"bands": "bands", "frame": "frame", "barbell": "barbell + plates", "dumbbells": "dumbbells",
            "foam_roller": "foam roller", "tennis_ball": "tennis ball", "low_box": "low box", "court": "court",
            "bike": "bike", "pool": "pool", "jump_rope": "jump rope"}


def mname(m):
    return MUSCLES[m][0]


def render_md(cat):
    rows = cat["rows"]
    L = []
    a = L.append
    a("# Exercise Catalogue")
    a("")
    a(f"**Non-normative · draft.** Seed data for Stage 1 (`Stage1_Programming.md` §3.2 · D-03): the exercise facts every plan takes. "
      f"`ExerciseCatalogue.json` (schema `{cat['schema']}`) is the source; this file mirrors it and is regenerated from it — edit the JSON, not this file.")
    rv = cat["revisions"][0]
    a(f"Screened against the {cat['screened_against']}. Built {cat['built']}; revision {rv['n']}, {rv['date']}: {rv['note']} (§0). Where this file and the stage documents disagree, the stage documents govern.")
    a("")
    s = cat["summary"]
    a(f"**{s['rows']} rows** — open {s['status']['open']} · locked {s['status']['locked']} · excluded {s['status']['excluded']} · "
      f"from the corpus {s['source']['corpus']} · corpus-fixed ✏️ {s['source']['corpus-fixed']} · proposed ✏️ {s['source']['proposed']} · "
      f"confirmed ✏️ {s['source']['confirmed']}.")
    a("")
    a("**Marks:** ✏️ changed from the corpus or added · ⚠️ warning that travels with the exercise · 🔖 reading for Harry to confirm (§5) · "
      "📖 spec or corpus basis · 🌐 literature basis · 🧠 mechanics basis.")
    a("")
    a("---")
    a("")
    a("## 0. Revisions")
    a("")
    for rv in cat["revisions"]:
        a(f"**Revision {rv['n']} — {rv['date']}: {rv['note']}**")
        a("")
        for c in rv["changes"]:
            a(f"- {c}")
        a("")
        d = rv.get("diff")
        if d and any(d.values()):
            a(f"| Change from revision {rv['n'] - 1} | Rows |")
            a("|---|---|")
            for label, key in (("Locked by the widened R12", "locked"), ("Opened", "opened"), ("Turned into a bilateral variant ✏️", "bilateral"),
                               ("End-range warning added", "end_range"), ("Holds now counted as hypertrophy sets", "holds"),
                               ("Added ✏️", "added"), ("Replacement named (Stage 1 D-09)", "replaced"),
                               ("Unlock path changed: control test now exists", "unlock_path"),
                               ("Locked until shoulder stage 2 (§2.5 · D-63)", "locked_range"),
                               ("Changed from the corpus ✏️", "corpus_fixed"),
                               ("Cues re-screened for the stage-1 ranges", "cues"),
                               ("Cues with what applies from upper-body stage 2, and the R12 wording", "cues_stage2"),
                               ("Corpus provenance: the upper focus files v7", "provenance"),
                               ("Corpus provenance: the upper focus files v8", "provenance_v8")):
                if d.get(key):
                    a(f"| {label} | {', '.join(d[key])} |")
            a("")
    a("---")
    a("")
    a("## 1. Use")
    a("")
    a("| Step | How the catalogue serves it |")
    a("|---|---|")
    a("| S1.4 Candidates | Filter by `prime_mover` and `status`, then re-check `joints` against the actual loading stages in Current state |")
    a("| S1.5–S1.6 Harvest, direct sets | `compound` and `indirect` (Stage 1 R35); `hyp_set` says whether a hold counts toward a hypertrophy target |")
    a("| R26–R29 Zones | `zone`, labelled for the gated range |")
    a("| R41 Alternatives | `stations` and the computed `alt_candidates` |")
    a("| Stage 0 R21 Sport note | `day_after` lists each sport whose avoid-the-day-before muscles collect sets in the exercise |")
    a("| R31 Sport verdict | `sport_notes` (carryover, conflicts) plus `cues`, `warnings` and `notes` for the joint-risk question |")
    a("")
    a("---")
    a("")
    a("## 2. Index")
    a("")
    a("| ID | Exercise | Prime mover · zone | Stations | Status | Source |")
    a("|---|---|---|---|---|---|")
    for x in rows:
        pm = f"{mname(x['prime_mover'])} · {x['zone'] or '—'}" if x["prime_mover"] else f"{x['kind']}"
        st = ", ".join(STATIONS[s].split(" (")[0] for s in x["stations"]) or "—"
        status = x["status"] + (" 🔖" if "A7" in x["attention"] else "")
        srcm = {"corpus": "corpus", "corpus-fixed": "corpus-fixed ✏️", "proposed": "proposed ✏️", "confirmed": "confirmed ✏️"}[x["source"]]
        a(f"| {x['id']} | {x['name']} | {pm} | {st} | {status} | {srcm} |")
    a("")
    a("---")
    a("")
    a("## 3. Rows")
    a("")
    sections = []
    seen = set()
    for x in rows:
        if x["kind"] in ("resistance", "hold"):
            sec = (f"3.{'1' if x['region'] == 'upper' else '2'}", f"{x['region'].capitalize()} body — {MUSCLES[x['prime_mover']][2]}")
        elif x["kind"] == "drill":
            sec = ("3.3", "Drills — mobility halves and warm-ups")
        else:
            sec = ("3.4", "Conditioning")
        if sec[1] not in seen:
            seen.add(sec[1])
            sections.append(sec)
        x["_sec"] = sec[1]
    stands = {}
    for x in rows:
        for t in x["replaced_by"]:
            stands.setdefault(t, []).append(f"{x['id']} ({x['status']})")
    for x in rows:
        x["_for"] = stands.get(x["id"], [])
    level2 = {}
    for num, title in sections:
        level2.setdefault(num, []).append(title)
    heads = {"3.1": "Upper body", "3.2": "Lower body", "3.3": None, "3.4": None}
    for num in ["3.1", "3.2", "3.3", "3.4"]:
        titles = level2.get(num, [])
        if not titles:
            continue
        if heads[num]:
            a(f"### {num} {heads[num]}")
            a("")
        else:
            a(f"### {num} {titles[0]}")
            a("")
        for t in titles:
            if heads[num]:
                a(f"#### {t.split(' — ')[1].capitalize()}")
                a("")
            for x in rows:
                if x["_sec"] != t:
                    continue
                render_row(a, x)
    for x in rows:
        x.pop("_sec", None)
        x.pop("_for", None)
    a("---")
    a("")
    a("## 4. Vocabulary")
    a("")
    a("**Muscles** (Stage 0 §2.1 groups; R21 lists from Stage 0 §1.2)")
    a("")
    a("| ID | Muscle | Covers | Group | Region | Avoid the day before |")
    a("|---|---|---|---|---|---|")
    for m in cat["vocabulary"]["muscles"]:
        sports = [sp for sp, spec in AVOID_DAY_BEFORE.items() if m["id"] in spec["muscles"]]
        a(f"| `{m['id']}` | {m['name']} | {m['covers']} | {m['group']} | {m['region']} | {', '.join(sports) or '—'} |")
    a("")
    a(f"Badminton reading: {AVOID_DAY_BEFORE['badminton']['reading']}.")
    a("")
    tested = [k for k, v in JOINTS.items() if v]
    untested = [k for k, v in JOINTS.items() if not v]
    if untested:
        a(f"**Joints** — loading stages 1–4 (Stage 0 §2.5); control tests exist for the {', '.join(tested[:-1])} and {tested[-1]}; "
          f"the {', '.join(untested[:-1])} and {untested[-1]} stay at stage 1 until theirs are added (R14).")
    else:
        a("**Joints** — loading stages 1–4 (Stage 0 §2.5); every joint has a control test (D-61…D-66), and each joint's stage-1 range is set there.")
    a("")
    a("**Stations** (one each; a station in use is unavailable, Stage 0 §1.3): " + " · ".join(f"`{k}` {v}" for k, v in STATIONS.items()) + ".")
    a("")
    a("**Equipment** (always available, and conditioning resources): " + " · ".join(f"`{k}` {v}" for k, v in EQUIPMENT.items()) + ".")
    a("")
    a("**Kinds:** " + " · ".join(f"`{k}` {v}" for k, v in KINDS.items()) + ".")
    a("")
    a("**Status:** " + " · ".join(f"`{k}` {v}" for k, v in STATUS.items()) + ".")
    a("")
    a("**Source:** " + " · ".join(f"`{k}` {v}" for k, v in SOURCES.items()) + ".")
    a("")
    a("---")
    a("")
    a("## 5. Decisions and open readings")
    a("")
    a("**Decided** (Harry, chats 2026-10-03, 2026-10-06, 2026-10-12 and 2026-10-13)")
    a("")
    a("| # | Topic | Decision | Lands in |")
    a("|---|---|---|---|")
    for k, v in cat["decisions"].items():
        a(f"| {k} | {v['title']} | {v['decision']} | {v['lands']} |")
    a("")
    a("**Open** 🔖")
    a("")
    a("| # | Topic | Reading | Rows |")
    a("|---|---|---|---|")
    for k, v in cat["attention"].items():
        ids = [x["id"] for x in rows if k in x["attention"]]
        a(f"| {k} | {v['title']} | {v['text']} | {', '.join(ids) if ids else '—'} |")
    a("")
    a("---")
    a("")
    a("## 6. Method")
    a("")
    for i, mth in enumerate(cat["method"], 1):
        a(f"{i}. {mth}")
    a("")
    a("**Literature cited in rows**")
    a("")
    a("| Ref | Source |")
    a("|---|---|")
    for k, v in cat["references"].items():
        a(f"| {k} | {v} |")
    a("")
    return "\n".join(L)


def basis_mark(b):
    if "[W" in b:
        return "🌐 " + b
    if b.startswith("mechanics"):
        return "🧠 " + b
    return "📖 " + b


def render_row(a, x):
    head = f"**{x['id']} · {x['name']}** — "
    if x["prime_mover"]:
        comp = "hold" if x["kind"] == "hold" else ("compound" if x["compound"] else "isolation")
        head += f"{mname(x['prime_mover'])} · {x['zone'] or '—'} · {x['pattern']} · {comp} · "
    else:
        head += f"{x['kind']}{' · ' + x['region'] if x['region'] else ''} · "
    head += x["status"]
    if x["source"] != "corpus":
        head += " ✏️"
    a(head)
    a("")
    lines = []
    st = ", ".join(STATIONS[s].split(" (")[0] for s in x["stations"]) or "none"
    eq = ", ".join(EQ_SHORT[e] for e in x["equipment"]) or "none"
    jt = "; ".join(f"{j['joint']} {j['needs']}" + (f" — {j['note']}" if j.get("note") else "") for j in x["joints"]) or "—"
    lines.append(f"- Stations: {st} · Equipment: {eq} · Joints (stage needed): {jt}")
    if x["prime_mover"] and x["status"] != "excluded":
        ind = ", ".join(mname(m) for m in x["indirect"]) or "—"
        da = "; ".join(f"{d['sport']} ({', '.join(mname(m) for m in d['muscles'])})" for d in x["day_after"]) or "—"
        hs = "" if x["hyp_set"] is None or x["hyp_set"] else " · Not a hypertrophy set: timed isometrics count only for forearm and abs isolation (Stage 0 §2.2)"
        lines.append(f"- Indirect: {ind} · Day after: {da}{hs}")
    if x["targets"]:
        lines.append(f"- Targets: {x['targets']}")
    if x["status"] == "locked":
        lines.append(f"- Locked: {x['unlock']}")
    if x["status"] == "excluded":
        lines.append(f"- Excluded ({' · '.join(x['excluded_by'])}): {x['excluded_why']} Use instead: {', '.join(x['replaced_by'])}")
    elif x["replaced_by"]:
        lines.append(f"- Until it opens, use: {', '.join(x['replaced_by'])} (Stage 1 D-09)")
    if x.get("_for"):
        lines.append(f"- Stands in for: {', '.join(x['_for'])}")
    if x["cues"]:
        lines.append("- Cues: " + " · ".join(x["cues"]))
    for w in x["warnings"]:
        lines.append(f"- ⚠️ {w}")
    if x["sport_notes"]:
        parts = []
        for sp, d in x["sport_notes"].items():
            seg = []
            if d.get("carryover"):
                seg.append("carryover: " + "; ".join(d["carryover"]))
            if d.get("conflicts"):
                seg.append("conflict: " + d["conflicts"])
            parts.append(f"{sp} — " + ", ".join(seg))
        lines.append("- Sport: " + " · ".join(parts))
    if x["alt_candidates"]:
        lines.append("- Alternative candidates (R41 filter): " + ", ".join(x["alt_candidates"]))
    if x["notes"]:
        lines.append(f"- Notes: {x['notes']}")
    src = {"corpus": "📖 corpus", "corpus-fixed": "📖 corpus-fixed ✏️", "proposed": "proposed ✏️",
           "confirmed": "confirmed by Harry ✏️ (Stage 1 D-08)"}[x["source"]]
    if x["corpus"]:
        src += " — " + "; ".join(x["corpus"])
    lines.append(f"- Source: {src}")
    if x["changed"]:
        lines.append(f"- Changed ✏️: {x['changed']}")
    lines.append("- Basis: " + " · ".join(basis_mark(b) for b in x["basis"]))
    if x["attention"]:
        lines.append("- 🔖 " + ", ".join(x["attention"]))
    for ln in lines:
        a(ln)
    a("")


def dump_json(cat):
    """Readable JSON: header blocks indented; one row field per line, values compact."""
    compact = lambda v: json.dumps(v, ensure_ascii=False, separators=(", ", ": "))
    out = ["{"]
    keys = list(cat.keys())
    for i, k in enumerate(keys):
        end = "," if i < len(keys) - 1 else ""
        if k != "rows":
            body = json.dumps(cat[k], ensure_ascii=False, indent=2).replace("\n", "\n  ")
            out.append(f'  "{k}": {body}{end}')
            continue
        out.append('  "rows": [')
        for j, row in enumerate(cat["rows"]):
            out.append("    {")
            fk = list(row.keys())
            for n, f in enumerate(fk):
                out.append(f'      "{f}": {compact(row[f])}' + ("," if n < len(fk) - 1 else ""))
            out.append("    }" + ("," if j < len(cat["rows"]) - 1 else ""))
        out.append("  ]" + end)
    out.append("}")
    text = "\n".join(out) + "\n"
    assert json.loads(text) == cat
    return text


def revision_diff(rows, prev_path):
    prev = {x["key"]: x for x in json.load(open(prev_path, encoding="utf-8"))["rows"]}
    d = {"locked": [], "opened": [], "bilateral": [], "end_range": [], "holds": [], "added": [], "replaced": [], "unlock_path": [],
         "locked_range": [], "corpus_fixed": [], "cues": []}
    for x in rows:
        p = prev.get(x["key"])
        if not p:
            d["added"].append(x["id"])
            continue
        if x["id"] != p["id"]:
            fail(f"{x['key']}: ID moved from {p['id']} to {x['id']}")
        if set(x["replaced_by"]) - set(p["replaced_by"]):
            d["replaced"].append(x["id"])
        if x["status"] == "locked" and p["status"] == "locked" and x["unlock"] != p["unlock"]:
            d["unlock_path"].append(x["id"])
        if x["status"] == "locked" and p["status"] != "locked":
            if any("D-63" in (j.get("note") or "") for j in x["joints"]):
                d["locked_range"].append(x["id"])
            else:
                d["locked"].append(x["id"])
        elif x["status"] != "excluded" and x["cues"] != p["cues"]:
            d["cues"].append(x["id"])
        if (x["changed"] or "") != (p.get("changed") or "") and x["source"] == "corpus-fixed":
            d["corpus_fixed"].append(x["id"])
        if x["status"] == "open" and p["status"] != "open":
            d["opened"].append(x["id"])
        if x["changed"] and "D-54" in x["changed"] and x["status"] == "open" and not (p.get("changed") and "D-54" in p["changed"]):
            d["bilateral"].append(x["id"])
        if any("D-55" in w for w in x["warnings"]) and not any("End-range" in w for w in p.get("warnings", [])):
            d["end_range"].append(x["id"])
        if x["kind"] == "hold" and x["hyp_set"] and not p.get("hyp_set"):
            d["holds"].append(x["id"])
    return d


def main():
    out = sys.argv[1]
    rows = build()
    if len(sys.argv) > 2:
        REVISIONS[0]["diff"] = revision_diff(rows, sys.argv[2])
        if REVISIONS[0]["n"] == 11:  # revision 11: v8 provenance listed apart
            d = REVISIONS[0]["diff"]
            prev = {x["key"]: x for x in json.load(open(sys.argv[2], encoding="utf-8"))["rows"]}
            d["provenance_v8"] = [x["id"] for x in rows if x["key"] in prev and x["corpus"] != prev[x["key"]]["corpus"]]
    cat = catalogue(rows)
    js = dump_json(cat)
    js = unicodedata.normalize("NFC", js)
    md = unicodedata.normalize("NFC", render_md(cat)) + "\n"
    with open(f"{out}/ExerciseCatalogue.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    with open(f"{out}/ExerciseCatalogue.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    print(json.dumps(cat["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
