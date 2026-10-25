"""Verify ExerciseCatalogue.json against the corpus card list, its .md mirror and the spec docs.

Run: python3 -B verify.py <dir with ExerciseCatalogue.json + .md> <gymspec dir>
Checks 1–2 list the routine files at the latest version the catalogue cites, with their card counts (2026-10-13); a
version that changes no exercise, card number or pairing leaves them as they are (Stage 2 D-04). Check 6 reads the files in
gymplan/ (beside the gymspec dir given) and confirms each one still matches the version the catalogue cites; a stem found
only in gymplan/PreviousOldRoutines/, Harry's archive, is skipped as retired (Stage 2 D-15). A FAIL exits 1.
"""
import json
import os
import re
import sys

out, spec = sys.argv[1], sys.argv[2]
cat = json.load(open(f"{out}/ExerciseCatalogue.json", encoding="utf-8"))
md = open(f"{out}/ExerciseCatalogue.md", encoding="utf-8").read()
rows = cat["rows"]
ok = True


# Card names (Stage 2 D-04 · R61). When the catalogue does not cite a file's own version, its cards map through the
# latest cited version below it, and each card's title must match a row cited for its number. Words are compared without
# filler (both arms, soft bend, …); equipment, direction, angle, grip, rotation and curl type must not conflict, and
# "reverse", "overhead" and "behind" must agree. A row also matches when every word of its key is in the full title.
# Checked 2026-10-15: all 101 cards the catalogue cites match their rows; no two rows of different pattern or prime mover
# match each other (4,205 pairs).
SYN = {"db": "dumbbell", "dbs": "dumbbell", "dumbbells": "dumbbell", "bb": "barbell", "rdl": "romanian deadlift",
       "rdls": "romanian deadlift", "ext": "extension", "iso": "isometric", "raises": "raise", "curls": "curl",
       "rows": "row", "squats": "squat", "presses": "press", "extensions": "extension", "holds": "hold",
       "cars": "car", "walks": "walk", "thrusts": "thrust", "bridges": "bridge", "flys": "fly", "flyes": "fly",
       "pulldowns": "pulldown", "pushdowns": "pushdown", "clamshells": "clamshell", "tkes": "tke", "lunges": "lunge",
       "er": "external rotation", "ir": "internal rotation", "pauses": "pause", "wrists": "wrist", "heels": "heel",
       "pressing": "press", "rotations": "rotation"}
GENERIC = {"machine", "feet", "foot", "together", "hold", "isometric", "slow", "recovery", "tempo", "light", "long",
           "short", "single", "leg", "legs", "bilateral", "both", "arms", "arm", "bodyweight", "bench", "only", "pre",
           "post", "optional", "deficit", "controlled", "under", "above", "below", "parallel", "knee", "knees", "elbow",
           "elbows", "soft", "bend", "variant", "variants", "alternate", "each", "side", "sides"}
STOP = {"the", "a", "an", "and", "with", "on", "of", "to", "in", "at", "for", "x", "s", "or", "from", "into", "as", "off",
        "between"}
MOVES = {"curl", "press", "row", "raise", "fly", "squat", "extension", "rotation", "pulldown", "pushdown", "deadlift",
         "bridge", "thrust", "lunge", "plank", "walk", "step", "car", "pullover", "sit", "hinge", "pull", "push"}
ONE_SIDED = {"reverse", "overhead", "behind"}
KINDS = [{"barbell", "dumbbell", "cable", "band", "smith"}, {"front", "lateral", "rear"}, {"incline", "decline", "flat"},
         {"narrow", "wide", "close"}, {"internal", "external"}, {"hammer", "preacher", "spider"}]


def words(t, paren=False):
    t = t.lower().replace("&amp;", "&").replace("&#x27;", "'")
    if not paren:
        t = re.sub(r"\([^)]*\)", " ", t)
    return {v for w in re.findall(r"[a-z0-9]+", t) for v in SYN.get(w, w).split() if v not in STOP and v not in GENERIC}


def same_name(title, row):
    a, b = words(title), words(row["name"])
    if a and b and len(a & b) >= 0.6 * len(a | b) and not (a ^ b) & ONE_SIDED \
            and not any((a & k) and (b & k) and (a & k) != (b & k) for k in KINDS):
        return True
    k = words(row["key"].replace("_", " "))
    return bool(k) and k <= words(title, paren=True) and (len(k) >= 2 or not k & MOVES)


def vtag(v):
    return "(no version)" if v == 0 else f"v{v}"


def cited_versions(stem, rows):
    """Versions of a file the catalogue cites; "(no version)" counts as 0."""
    pat = re.compile(re.escape(stem) + r" (?:v(\d+)|\(no version\)) (?:ex\. |alt\. for |[PS]\d)")
    return {int(m.group(1) or 0) for r in rows for c in r["corpus"] if (m := pat.match(c))}


def html_unesc(t):
    return t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#x27;", "'").replace("&quot;", '"')


def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok = ok and cond


# 1. Corpus cards: every numbered card / mobility ID is catalogued
cards = {
    "routine_upperbody v6": range(1, 9), "routine_lowerbody v4": range(1, 8),
    "routine_upperbody_focus_A v8": range(1, 9), "routine_upperbody_focus_B v8": range(1, 9),
    "routine_upperbody_focus_C v8": range(1, 7), "routine_lowerbody_focus_A v3": range(1, 9),
    "routine_lowerbody_focus_B v3": range(1, 9), "routine_lowerbody_focus_C v3": range(1, 12),
    "popliteus_prevention_protocol v5": range(1, 11), "cardio_routine (no version)": range(1, 16),
}
refs = [c for x in rows for c in x["corpus"]]
missing = []
for f, rng in cards.items():
    for n in rng:
        pat = re.compile(re.escape(f) + r" ex\. (\d+)(?:–(\d+))?\b")
        hit = False
        for c in refs:
            m = pat.match(c)
            if m:
                lo = int(m.group(1)); hi = int(m.group(2) or lo)
                if lo <= n <= hi:
                    hit = True
                    break
        if not hit:
            missing.append(f"{f} ex. {n}")
for f, ids in {"stretching_upper_hEDS v2": [f"P{i}" for i in range(1, 8)] + [f"S{i}" for i in range(1, 10)],
               "stretching_lower_hEDS v1": [f"P{i}" for i in range(1, 8)] + [f"S{i}" for i in range(1, 9)]}.items():
    for i in ids:
        if not any(c.startswith(f"{f} {i}") and (len(c) == len(f"{f} {i}") or c[len(f"{f} {i}")] == " ") for c in refs):
            missing.append(f"{f} {i}")
check(not missing, f"every corpus card and mobility item is catalogued ({len(missing)} missing: {missing})")

# 2. Alternatives per file (counts from the alternatives tables)
expected_alts = {"routine_upperbody v6": 18, "routine_upperbody_focus_A v8": 8, "routine_upperbody_focus_B v8": 4,
                 "routine_upperbody_focus_C v8": 6, "routine_lowerbody_focus_A v3": 2, "routine_lowerbody_focus_B v3": 4,
                 "routine_lowerbody_focus_C v3": 2, "popliteus_prevention_protocol v5": 2}
for f, n in expected_alts.items():
    got = sum(1 for c in refs if c.startswith(f + " alt. for"))
    # a corpus-fixed variant may cite the same alternative as its locked original
    check(got >= n, f"{f}: {got} alternative citations (table has {n})")

# 3. Mirror parity
ids = [x["id"] for x in rows]
check(ids == [f"C{i:03d}" for i in range(1, len(rows) + 1)], f"IDs sequential C001–C{len(rows):03d}")
idx = re.findall(r"^\| (C\d{3}) \|", md, re.M)
blocks = re.findall(r"^\*\*(C\d{3}) · ", md, re.M)
check(idx == ids, "index lists every row once, in order")
check(sorted(blocks) == ids, "row blocks list every row once (grouped by section)")
for x in rows:
    if f"**{x['id']} · {x['name']}**" not in md:
        check(False, f"{x['id']} name mismatch in mirror")
        break
else:
    check(True, "every row's name matches between JSON and mirror")
s = cat["summary"]
check(s["rows"] == len(rows) and sum(s["status"].values()) == len(rows) and sum(s["source"].values()) == len(rows), "summary counts add up")
check(f"**{s['rows']} rows**" in md, "mirror summary matches JSON")

# 4. Vocabulary and gate fields
st = set(cat["vocabulary"]["stations"]); eq = set(cat["vocabulary"]["equipment"])
check(all(set(x["stations"]) <= st and set(x["equipment"]) <= eq for x in rows), "R15: every station and equipment item is in Stage 0 §1.3")
check(all(x["status"] == "excluded" or (x["status"] == "open") == all(j["needs"] == 1 for j in x["joints"]) for x in rows), "status agrees with joint needs")
check(all(x["changed"] for x in rows if x["source"] == "corpus-fixed"), "every corpus-fixed row says what changed")
check(all(x["excluded_by"] and x["replaced_by"] for x in rows if x["status"] == "excluded"), "every excluded row names its gate and replacement")
check(all(by_id[t]["status"] == "open" for x in rows for t in x["replaced_by"]) if (by_id := {x["id"]: x for x in rows}) else False,
      "every replacement (replaced_by) is open")
reps = {t for x in rows if x["status"] == "locked" for t in x["replaced_by"]}
check(all(x["id"] in reps for x in rows if x["source"] == "confirmed" and any("Stage-1 replacement" in b for b in x["basis"])),
      "every confirmed replacement row stands in for a locked row (Stage 1 D-09)")
check(all(f"Stands in for: " in md.split(f"**{t} · ")[1].split("\n\n**")[0] for t in reps), "mirror shows each replacement's reverse link")
by = {x["id"]: x for x in rows}
bad = []
for x in rows:
    for a in x["alt_candidates"]:
        y = by[a.split()[0]]
        if set(y["stations"]) & set(x["stations"]) or y["status"] != "open" or y["pattern"] != x["pattern"]:
            bad.append((x["id"], a))
check(not bad, f"alt candidates share no station, are open and keep the pattern ({bad})")
check(all(not x["alt_candidates"] for x in rows if not x["stations"]), "no-station exercises carry no alternatives (R41)")

# 5. Cross-references into the spec
s0 = open(f"{spec}/Stage0_SupplementInfo.md", encoding="utf-8").read()
s1 = open(f"{spec}/Stage1_SupplementInfo.md", encoding="utf-8").read()
text = json.dumps(cat, ensure_ascii=False)
d0 = set(re.findall(r"Stage 0 (?:§[\d.]+ · )?D-(\d+)", text)) | set(re.findall(r"Stage 0 D-(\d+)", text))
miss0 = [d for d in d0 if f"| D-{d} |" not in s0]
check(not miss0, f"Stage 0 D-refs exist ({sorted(d0)}; missing {miss0})")
dall = sorted({int(m) for m in re.findall(r"\bD-(\d+)", text)})
s1max = max(int(m) for m in re.findall(r"^\| D-(\d+) \|", s1, re.M))
missall = [d for d in dall if f"| D-{d:02d} |" not in s0 and f"| D-{d:02d} |" not in s1]
hi = [d for d in dall if d > s1max and f"| D-{d:02d} |" not in s0]
check(not missall and not hi, f"every D-ref exists in a decision log ({dall}; Stage 1 log ends at D-{s1max:02d}; missing {missall + hi})")
w1 = set(re.findall(r"Stage 1 \[W(\d+)\]", text)) | {m for g in re.findall(r"Stage 1 \[W\d+\] · \[W(\d+)\]", text) for m in [g]}
miss1 = [w for w in w1 if f"| W{w} |" not in s1]
check(not miss1, f"Stage 1 W-refs exist ({sorted(w1, key=int)}; missing {miss1})")
w0 = set(re.findall(r"Stage 0 \[W(\d+)\]", text))
miss0w = [w for w in w0 if f"| W{w} |" not in s0]
check(not miss0w, f"Stage 0 W-refs exist ({sorted(w0)}; missing {miss0w})")
rr = sorted({int(m) for m in re.findall(r"\bR(\d+)\b", text)})
check(all(1 <= r <= 48 for r in rr), f"R-numbers within R1–R48 ({rr})")
# 6. Routine files against the catalogue (Stage 2 D-04 · R61): each file's version is at least the latest the catalogue
#    cites, every card or mobility item cited at that version is in the file under the same number, and its title, its
#    card text or the citation's own words match a cited row. A card cited only inside a range ("ex. 5–8", one merged
#    row) is checked for presence only. A text-only version leaves the catalogue as it is; a changed exercise, card number
#    or pairing needs a new revision.
plan = os.path.join(spec, "..", "gymplan")
TEXT = re.compile(r'<text font-size="(\d+)"( font-weight="500")?[^>]*? x="(\d+)" y="(\d+)"[^>]*>([^<]*)</text>')
cite = {}
for x in rows:
    for c in x["corpus"]:
        m = re.match(r"(\S+) (?:v(\d+)|\(no version\)) (?:ex\. (\d+)(?:–(\d+))?|([PS]\d+))(?: \((.*)\))?$", c)
        if m:
            rng = bool(m.group(4))
            ks = [m.group(5)] if m.group(5) else [str(n) for n in range(int(m.group(3)), int(m.group(4) or m.group(3)) + 1)]
            for k in ks:
                cite.setdefault(m.group(1), {}).setdefault(int(m.group(2) or 0), {}).setdefault(k, []).append(
                    (x, m.group(6) or "", rng))


def card_ok(title, full, cites):
    if all(rng for _, _, rng in cites):
        return True  # one merged row for a range of cards: presence only
    fw = words(full, paren=True)
    for row, qual, rng in cites:
        if same_name(title, row):
            return True
        k = words(row["key"].replace("_", " "))
        if k and k <= fw and (len(k) >= 2 or not k & MOVES):
            return True
        for item in re.split(r"[,;]", qual):
            iw = {w for w in words(item) if not w.isdigit() and w not in ("round", "rounds")}
            if iw and iw <= fw:
                return True
    return False


if not os.path.isdir(plan):
    print(f"SKIP routine files: no {plan}")
for stem, by_ver in sorted(cite.items()):
    if not os.path.isdir(plan):
        break
    use = max(by_ver)
    path = os.path.join(plan, stem + ".svg")
    if not os.path.exists(path):
        if os.path.exists(os.path.join(plan, "PreviousOldRoutines", stem + ".svg")):
            print(f"SKIP {stem}: retired to gymplan/PreviousOldRoutines/ (Stage 2 D-15)")
        else:
            check(False, f"{stem}: cited by the catalogue, but gymplan/ has no such file")
        continue
    t = [(int(a_), bool(b_), int(x_), int(y_), html_unesc(s_)) for a_, b_, x_, y_, s_ in TEXT.findall(open(path, encoding="utf-8").read())]
    ver = next((int(m.group(1)) for *_, s_ in t if (m := re.match(r"v(\d+) — ", s_))), 0)
    nums = [(y, s_) for size, bold, x_, y, s_ in t if size == 11 and bold and x_ == 54 and re.fullmatch(r"[PS]?\d+", s_)]
    ys = sorted({y for y, _ in nums})
    have = {}
    for y, k in nums:
        if k in have:
            continue
        end = next((y2 for y2 in ys if y2 > y), y + 90)
        title = next((s_ for size, bold, x_, y2, s_ in t if size == 12 and bold and 60 <= x_ <= 80 and y2 == y), "")
        full = " ".join(s_ for size, bold, x_, y2, s_ in t if 60 <= x_ <= 480 and y <= y2 < end)
        have[k] = (title, full)
    missing = [k for k in by_ver[use] if k not in have]
    bad = [k for k, cs in by_ver[use].items() if k in have and not card_ok(have[k][0], have[k][1], cs)]
    check(ver >= use and not missing and not bad,
          f"{stem} v{ver}: cards match the catalogue's {vtag(use)}" + (f" — missing {missing}" if missing else "")
          + (f" — no match for {bad}" if bad else "") + ("" if ver >= use else f" — the file is older than {vtag(use)}"))

print("ALL PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
