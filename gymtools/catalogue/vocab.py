"""Controlled vocabularies for the exercise catalogue (Stage 1 §3.2 · D-03)."""

# Muscles: id -> (name, covers, group, region). Groups and regions: Stage 0 §2.1.
MUSCLES = {
    # upper — abs & obliques
    "abs": ("Abs", "rectus abdominis, transversus abdominis", "abs & obliques", "upper"),
    "obliques": ("Obliques", "internal and external obliques", "abs & obliques", "upper"),
    # upper — back
    "lats": ("Lats", "latissimus dorsi, teres major", "back", "upper"),
    "upper_back": ("Upper back", "mid and lower trapezius, rhomboids", "back", "upper"),
    "erectors": ("Spinal erectors", "erector spinae", "back", "upper"),
    "upper_trap": ("Upper trapezius", "never programmed directly (Stage 0 R8)", "back", "upper"),
    # upper — chest & shoulders
    "chest": ("Chest", "pectoralis major, sternal and clavicular heads", "chest & shoulders", "upper"),
    "front_delt": ("Front delt", "anterior deltoid", "chest & shoulders", "upper"),
    "side_delt": ("Side delt", "middle (lateral) deltoid", "chest & shoulders", "upper"),
    "rear_delt": ("Rear delt", "posterior deltoid", "chest & shoulders", "upper"),
    "rotator_cuff": ("Rotator cuff", "infraspinatus, teres minor, supraspinatus, subscapularis", "chest & shoulders", "upper"),
    "serratus": ("Serratus anterior", "serratus anterior", "chest & shoulders", "upper"),
    # upper — arms & hands
    "biceps": ("Biceps", "elbow flexors: biceps brachii, brachialis, brachioradialis", "arms & hands", "upper"),
    "triceps": ("Triceps", "long, lateral and medial heads", "arms & hands", "upper"),
    "forearm_flexors": ("Forearm flexors", "wrist and finger flexors, grip", "arms & hands", "upper"),
    "forearm_extensors": ("Forearm extensors", "wrist and finger extensors", "arms & hands", "upper"),
    "forearm_rotators": ("Forearm rotators", "pronators and supinators", "arms & hands", "upper"),
    # lower — hips & gluteals
    "glutes": ("Glutes", "gluteus maximus", "hips & gluteals", "lower"),
    "hip_abductors": ("Hip abductors", "gluteus medius and minimus, TFL", "hips & gluteals", "lower"),
    "adductors": ("Adductors", "adductor longus, brevis and magnus, gracilis", "hips & gluteals", "lower"),
    "hip_flexors": ("Hip flexors", "iliopsoas, rectus femoris at the hip", "hips & gluteals", "lower"),
    # lower — thighs
    "quads": ("Quads", "quadriceps", "thighs", "lower"),
    "hamstrings": ("Hamstrings", "biceps femoris, semitendinosus, semimembranosus", "thighs", "lower"),
    # lower — calves & shins
    "calves": ("Calves", "gastrocnemius, soleus", "calves & shins", "lower"),
    "tibialis": ("Tibialis anterior", "tibialis anterior", "calves & shins", "lower"),
    "popliteus": ("Popliteus", "popliteus", "calves & shins", "lower"),
    "evertors": ("Ankle evertors", "fibularis longus and brevis", "calves & shins", "lower"),
}

# Stage 0 §1.2 "Avoid the day before", mapped onto the muscle ids (R21).
AVOID_DAY_BEFORE = {
    "archery": {
        "source": "the upper demand muscles (Stage 0 §1.2)",
        "muscles": ["rear_delt", "side_delt", "upper_back", "lats", "chest", "rotator_cuff",
                    "triceps", "forearm_flexors", "forearm_extensors", "abs", "obliques", "erectors"],
    },
    "badminton": {
        "source": "calves/Achilles, quads and glutes, rotator cuff, forearm and grip (Stage 0 §1.2)",
        "muscles": ["calves", "quads", "glutes", "hip_abductors", "rotator_cuff",
                    "forearm_flexors", "forearm_extensors", "forearm_rotators"],
        "reading": "glute max and glute med (Stage 0 §1.2 · D-56)",
    },
}

# Stage 0 §1.2 carryover rows, as short tags.
CARRYOVER = {
    "archery": {
        "RET": "horizontal abduction and scapular retraction strength-endurance",
        "HOLD": "isometric holds at shoulder height",
        "ER": "cuff external rotation",
        "EXT": "shoulder extension and adduction",
        "PULL": "pulling strength",
        "TRUNK": "trunk anti-rotation and anti-extension holds",
    },
    "badminton": {
        "IR": "internal-rotation strength balanced by eccentric external rotation",
        "FORE": "pronation/supination and wrist flexion/extension",
        "TRUNK": "trunk rotation and anti-rotation",
        "ECC": "eccentric quad and glute",
        "CALF": "calf–Achilles capacity",
        "TRI": "overhead triceps (secondary)",
    },
}

# Joints staged by the loading gate (Stage 0 §2.5). Control tests: knee; ankle and hip (D-61 · D-62);
# shoulder, elbow, wrist and spine (D-63…D-66).
JOINTS = {
    "shoulder": True, "elbow": True, "wrist": True, "spine": True,
    "hip": True, "knee": True, "ankle": True,
}

# Stage 0 §1.3.
STATIONS = {
    "smith": "Smith machine",
    "cable": "Cable machine (rows, pulldowns, pullover, curl, pushdown, overhead extension)",
    "hip_machine": "Hip abductor/adductor machine",
    "bench": "Adjustable bench",
}
EQUIPMENT = {
    "bands": "bands — 2 long, 2 short",
    "frame": "multi-purpose frame: pull-up bars, also the rack (anchor points, pins)",
    "barbell": "Olympic barbells and plates",
    "dumbbells": "adjustable dumbbells",
    "foam_roller": "foam roller",
    "tennis_ball": "tennis ball",
    "low_box": "low step or box, 5–20 cm",
    "court": "badminton court",
    "bike": "bike, stationary or outdoor",
    "pool": "pool",
    "jump_rope": "jump rope",
}

KINDS = {
    "resistance": "Working sets with reps; counted in sets (Stage 0 §2.3)",
    "hold": "Timed isometric working sets; a hypertrophy option for any muscle (Stage 0 §2.2 · D-58), prescribed as sets × hold time + seconds in reserve (Stage 0 R16 · D-60)",
    "drill": "Active drill for a session's mobility halves or warm-up (Stage 0 R7 · §2.7); not counted in sets",
    "conditioning": "Conditioning resource or court work (Stage 0 §1.3); dosed only on request (Stage 1 §0.1)",
}

STATUS = {
    "open": "Passes the hard gates at the default Current state (every joint at loading stage 1), with its cues",
    "locked": "Needs a higher loading stage for at least one joint; opens when R14 unlocks it",
    "excluded": "Fails a hard gate in every form; see the linked replacement",
}

SOURCES = {
    "corpus": "Taken from the routine files, with gate cues added",
    "corpus-fixed": "Taken from the routine files, but a cue, depth, anchor or variant had to change to pass a gate (✏️)",
    "proposed": "Not taken from the routine files: named by the spec or filling a gap (✏️)",
    "confirmed": "Not taken from the routine files: proposed to Harry with its facts and added once he confirmed it (Stage 1 §3.2 · D-08) (✏️)",
}
