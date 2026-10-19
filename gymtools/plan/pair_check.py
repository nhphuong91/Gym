"""Superset check: every pair against Stage 1 R38 and R39, with stations from Stage 0 §1.3, using catalogue facts.

Run from the Gym folder:
  python3 -B gymtools/plan/pair_check.py gymplan/<routine>.svg [...]      every pair in routine files, plus their alternatives
  python3 -B gymtools/plan/pair_check.py --pair C040 C048 [--pair A B ...]  pairs by catalogue ID or key, while planning
  python3 -B gymtools/plan/pair_check.py --selftest                        the spec's pass and fail examples
Option --catalogue <path> (default gymspec/ExerciseCatalogue.json). Exits 1 when a pair or an alternative FAILs.

Per pair: (1) no shared prime mover or key synergist (catalogue prime_mover + indirect), except one muscle across two joint
actions; (2) no shared station (Stage 0 §1.3: a station in use is unavailable); (3) a pair type R38 names: listed antagonists,
opposite actions at the joint both move, cross-joint or cross-region, or a hold (neutral partner); (4) the heavy-compound clause.
PASS needs (1)-(3) and a settled (4). REVIEW: rule-valid, but the plan states the judgement named (the clause in (4) is a
judgement the catalogue cannot make). NOTE: joint-control note to state with the pair. File mode adds R39 (equal sets, extra
sets straight) and checks every alternative of a paired exercise against both partners' stations. Cards map to rows through
the catalogue's provenance lines ("<file> vN ex. n"): the file's own version when the catalogue cites it, otherwise the
latest cited version below it, as a version that changed no exercise, card number or pairing leaves the catalogue as it is
(Stage 2 D-04 · R61). Mapped that way, every card's title must match a row cited for its number, or the file FAILs: the
catalogue then needs the new version.
"""
import json
import re
import sys

JOINTS = {  # joints a movement pattern moves
    "horizontal press": {"shoulder", "elbow"}, "chest fly": {"shoulder"}, "horizontal pull": {"shoulder", "elbow"},
    "horizontal abduction": {"shoulder"}, "vertical pull": {"shoulder", "elbow"}, "vertical press": {"shoulder", "elbow"},
    "shoulder extension": {"shoulder"}, "shoulder flexion": {"shoulder"}, "shoulder abduction": {"shoulder"},
    "scapular upward rotation": {"shoulder"}, "shoulder rotation": {"shoulder"},
    "elbow flexion": {"elbow"}, "elbow extension": {"elbow"}, "wrist flexion": {"wrist"}, "wrist extension": {"wrist"},
    "forearm rotation": {"forearm"}, "trunk anti-extension": {"trunk"}, "trunk anti-rotation": {"trunk"},
    "trunk anti-lateral flexion": {"trunk"}, "squat": {"hip", "knee"}, "lunge": {"hip", "knee"}, "hinge": {"hip"},
    "hip extension": {"hip"}, "hip flexion": {"hip"}, "hip abduction": {"hip"}, "hip adduction": {"hip"},
    "knee flexion": {"knee"}, "knee extension": {"knee"}, "knee rotation": {"knee"}, "plantarflexion": {"ankle"},
    "dorsiflexion": {"ankle"}, "ankle eversion": {"ankle"}, "hop": {"ankle", "knee", "hip"},
}
F = frozenset
LISTED = {  # R38's named antagonist pairs
    F({"horizontal press", "horizontal pull"}): "horizontal press ↔ row (listed)",
    F({"vertical press", "vertical pull"}): "vertical press ↔ pull (listed)",
    F({"horizontal press", "vertical pull"}): "push ↔ pull (listed)",
    F({"hinge", "knee extension"}): "hinge ↔ knee extension (listed)",
}
OPPOSITE = {  # opposite actions at the joint both exercises move: push ↔ pull in R38's sense
    F({"chest fly", "horizontal pull"}): "horizontal adduction ↔ row",
    F({"chest fly", "horizontal abduction"}): "fly ↔ reverse fly",
    F({"horizontal press", "horizontal abduction"}): "horizontal press ↔ reverse fly",
    F({"vertical press", "shoulder extension"}): "vertical press ↔ shoulder extension",
    F({"shoulder flexion", "shoulder extension"}): "shoulder flexion ↔ extension",
    F({"shoulder flexion", "vertical pull"}): "shoulder flexion ↔ pull",
    F({"shoulder abduction", "vertical pull"}): "shoulder abduction ↔ adduction",
    F({"scapular upward rotation", "shoulder extension"}): "overhead raise ↔ shoulder extension",
    F({"scapular upward rotation", "vertical pull"}): "overhead raise ↔ pull",
    F({"elbow flexion", "elbow extension"}): "elbow flexion ↔ extension",
    F({"horizontal press", "elbow flexion"}): "push ↔ pull at the elbow",
    F({"vertical press", "elbow flexion"}): "push ↔ pull at the elbow",
    F({"horizontal pull", "elbow extension"}): "pull ↔ push at the elbow",
    F({"vertical pull", "elbow extension"}): "pull ↔ push at the elbow",
    F({"wrist flexion", "wrist extension"}): "wrist flexion ↔ extension",
    F({"hip flexion", "hip extension"}): "hip flexion ↔ extension",
    F({"hip flexion", "hinge"}): "hip flexion ↔ hinge",
    F({"hip abduction", "hip adduction"}): "hip abduction ↔ adduction",
    F({"plantarflexion", "dorsiflexion"}): "plantarflexion ↔ dorsiflexion",
    F({"knee flexion", "knee extension"}): "knee flexion ↔ extension",
    F({"knee flexion", "squat"}): "knee flexion ↔ knee extension",
    F({"knee flexion", "lunge"}): "knee flexion ↔ knee extension",
}
SOFT = {F({"knee flexion", "hinge"}): "hamstrings", F({"knee flexion", "hip extension"}): "hamstrings"}  # R38: weaker but valid


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


def load(path):
    cat = json.load(open(path, encoding="utf-8"))
    rows = cat["rows"]
    return rows, {r["id"]: r for r in rows} | {r["key"]: r for r in rows}


def moved(r):
    j = set(JOINTS.get(r["pattern"], set()))
    if r["compound"] and r["pattern"] in ("elbow flexion", "elbow extension"):
        j.add("shoulder")
    return j


def rotation(r):
    k = r["key"]
    return "er" if re.search(r"(^|_)er(_|$)", k) else "ir" if re.search(r"(^|_)ir(_|$)", k) else None


def heavy(r):
    return r["kind"] == "resistance" and bool(r["compound"])


def check_pair(a, b):
    """-> (verdict, [test lines], [notes])"""
    out, notes, fail, review = [], [], [], []
    for r in (a, b):
        if r["kind"] not in ("resistance", "hold"):
            return "FAIL", [f"{r['id']} is a {r['kind']}, not a working-set exercise"], []
    pa, pb = F({a["pattern"], b["pattern"]}), None
    ma, mb = {a["prime_mover"], *a["indirect"]}, {b["prime_mover"], *b["indirect"]}
    shared = ma & mb
    soft = SOFT.get(pa)
    if shared and not (soft and shared == {soft}):
        fail.append(f"(1) shared muscle: {', '.join(sorted(shared))}")
    else:
        out.append("(1) no shared muscle" if not shared else f"(1) only {soft}, across two joint actions")
    st = set(a["stations"]) & set(b["stations"])
    if st:
        fail.append(f"(2) shared station: {', '.join(sorted(st))} (Stage 0 §1.3)")
    else:
        out.append("(2) no shared station")
    holds = [r for r in (a, b) if r["kind"] == "hold"]
    if holds:
        kind = f"a hold is a neutral partner ({holds[0]['name']})"
    elif pa in LISTED:
        kind = LISTED[pa]
    elif pa in OPPOSITE:
        kind = OPPOSITE[pa]
    elif soft:
        kind = "one muscle across two joint actions (weaker but valid)"
    elif a["pattern"] == b["pattern"] == "shoulder rotation" and {rotation(a), rotation(b)} == {"er", "ir"}:
        kind = "internal ↔ external rotation"
    elif a["region"] != b["region"]:
        kind = "cross-region"
    elif not (moved(a) & moved(b)):
        kind = f"cross-joint ({'/'.join(sorted(moved(a)))} ↔ {'/'.join(sorted(moved(b)))})"
    else:
        kind = None
        fail.append(f"(3) same joint ({'/'.join(sorted(moved(a) & moved(b)))}), not antagonists: {a['pattern']} ↔ {b['pattern']}")
    if kind:
        out.append(f"(3) {kind}")
    hv = [r for r in (a, b) if heavy(r)]
    if not hv:
        out.append("(4) no heavy compound")
    elif len(hv) == 2 and pa in LISTED:
        out.append("(4) listed compound pair")
    else:
        for r in hv:
            other = b if r is a else a
            if heavy(other):
                review.append(f"(4) two heavy compounds outside R38's list: state why {other['name']} leaves {r['name']}'s grip, bracing and stabilizers fresh")
            elif other["pattern"].startswith("trunk"):
                review.append(f"(4) {other['name']} works the trunk: state why {r['name']}'s bracing stays fresh")
            elif not (JOINTS.get(other["pattern"], set()) & moved(r)):
                out.append(f"(4) {other['name']} works none of {r['name']}'s joints")
            else:
                review.append(f"(4) {other['name']} works a joint {r['name']} moves: state why its grip, bracing and stabilizers stay fresh")
    if all(any("(R6)" in c for c in r["cues"]) for r in (a, b)):
        notes.append("both brace the shoulder blades overhead (R6): state the order and the fallback")
    verdict = "FAIL" if fail else "REVIEW" if review else "PASS"
    return verdict, fail + out + review, notes


def show(label, a, b, extra=""):
    v, lines, notes = check_pair(a, b)
    print(f"{label}{a['id']} {a['name']} → {b['id']} {b['name']}{extra}")
    print(f"    {v}  " + " · ".join(lines))
    for n in notes:
        print(f"    NOTE  {n}")
    return v


TEXT = re.compile(r'<text font-size="(\d+)"( font-weight="500")?[^>]*? x="(\d+)" y="(\d+)"[^>]*>([^<]*)</text>')


def unesc(s):
    return s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#x27;", "'").replace("&quot;", '"')


def check_file(path, rows):
    stem = re.sub(r"\.(svg|txt)$", "", path.replace("\\", "/").split("/")[-1])
    texts = [(int(m.group(1)), bool(m.group(2)), int(m.group(3)), int(m.group(4)), unesc(m.group(5)))
             for m in TEXT.finditer(open(path, encoding="utf-8").read())]
    ver = next((m.group(1) for *_, t in texts if (m := re.match(r"v(\d+) — ", t))), None)
    if not ver:
        print(f"{path}: no version note"); return False
    vers = cited_versions(stem, rows)
    use = int(ver) if int(ver) in vers else max((v for v in vers if v < int(ver)), default=None)
    if use is None:
        print(f"{path}: the catalogue cites no version of {stem} up to v{ver}"); return False
    tag = f"{stem} {vtag(use)}"
    card, cited = {}, {}
    for r in rows:
        for c in r["corpus"]:
            m = re.match(re.escape(tag) + r" ex\. (\d+)(?:–(\d+))?$", c)
            if m:
                for n in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
                    card[n] = r
                    cited.setdefault(n, []).append(r)
    titles = {y: t for size, bold, x, y, t in texts if size == 12 and bold and 60 <= x <= 80}
    sections, cur, nums, alts, in_alt = [], None, [], [], False
    for size, bold, x, y, t in texts:
        if size == 12 and bold and x == 50 and t.startswith("Alternatives"):
            in_alt = True
        elif size == 12 and bold and x == 50 and re.match(r"[A-Z] — ", t):
            cur = {"head": t, "cards": []}; sections.append(cur)
        elif size == 11 and bold and x == 54 and t.isdigit() and cur is not None and not in_alt:
            cur["cards"].append({"n": int(t), "title": titles.get(y)})
        elif size == 12 and bold and x == 490 and cur is not None and cur["cards"] and not in_alt:
            cur["cards"][-1]["sets"] = int(re.match(r"(\d+)", t).group(1))
        elif in_alt and size == 10 and not bold and x == 50 and (m := re.match(r"(\d+)\s+(.*)$", t)):
            alts.append({"n": int(m.group(1)), "label": m.group(2), "names": []})
        elif in_alt and size == 10 and not bold and x in (280, 470) and alts:
            alts[-1]["names"].append(t)
    mapped = f", mapped through {vtag(use)}: Stage 2 D-04" if use != int(ver) else ""
    print(f"== {stem} v{ver}  ({sum(len(s['cards']) for s in sections)} cards, {len(sections)} sections{mapped})")
    ok, partner, counts = True, {}, {"PASS": 0, "REVIEW": 0, "FAIL": 0, "straight sets": 0}
    if use != int(ver):
        for s in sections:
            for c in s["cards"]:
                rs = cited.get(c["n"], [])
                if rs and not any(same_name(c["title"] or "", r) for r in rs):
                    names = " / ".join(r["name"] for r in rs)
                    print(f"  card {c['n']} \"{c['title']}\" does not match its {vtag(use)} row ({names}): "
                          f"the catalogue needs v{ver} (Stage 2 R61)")
                    ok = False
    for s in sections:
        letter = s["head"][0]
        miss = [c["n"] for c in s["cards"] if c["n"] not in card]
        if miss:
            print(f"  {letter}: card {miss} not cited by the catalogue as '{tag} ex. n'"); ok = False; continue
        if len(s["cards"]) == 2 and "Superset" in s["head"]:
            c1, c2 = s["cards"]
            a, b = card[c1["n"]], card[c2["n"]]
            partner[c1["n"]], partner[c2["n"]] = b, a
            extra = f"   {c1['sets']}/{c2['sets']} sets"
            v = show(f"  {letter}  ", a, b, extra)
            counts[v] += 1
            ok = ok and v != "FAIL"
            if c1["sets"] != c2["sets"]:
                k = abs(c1["sets"] - c2["sets"]); counts["straight sets"] += k
                print(f"    R39  {k} extra set(s) of {(a if c1['sets'] > c2['sets'] else b)['name']} run straight")
        else:
            for c in s["cards"]:
                counts["straight sets"] += c.get("sets", 0)
                print(f"  {letter}  {card[c['n']]['id']} {card[c['n']]['name']}: straight, {c.get('sets')} sets (R39)")
    for alt in alts:
        prim = card.get(alt["n"])
        lab = alt["label"].rstrip(".").lower()
        found = [r for r in rows for c in r["corpus"]
                 if c.startswith(f"{tag} alt. for ") and c[len(f"{tag} alt. for "):].lower().startswith(lab)]
        found = list({r["id"]: r for r in found}.values())
        bad = []
        for r in found:
            if prim and set(r["stations"]) & set(prim["stations"]):
                bad.append(f"{r['name']} uses the primary's {'/'.join(set(r['stations']) & set(prim['stations']))} (R41)")
            p = partner.get(alt["n"])
            if p and set(r["stations"]) & set(p["stations"]):
                bad.append(f"{r['name']} needs {'/'.join(set(r['stations']) & set(p['stations']))}, held by partner {p['name']} (Stage 0 §1.3)")
        if not found:
            bad.append("no catalogue row cites these alternatives")
        print(f"  alt #{alt['n']} {alt['label']}: " + ("FAIL " + "; ".join(bad) if bad else f"OK ({len(found)} rows, stations clear of both partners)"))
        ok = ok and not bad
    print("  " + " · ".join(f"{k} {v}" for k, v in counts.items()))
    return ok


SELFTEST = [  # (a, b, expected, source)
    ("C040", "C048", "PASS", "Stage 1 R38 pass: preacher curl ↔ cable pushdown"),
    ("C040", "C064", "PASS", "Stage 1 R38 pass: preacher curl ↔ Smith squat (cross-region)"),
    ("C002", "C048", "FAIL", "Stage 1 R38 fail: Smith incline press ↔ cable pushdown"),
    ("C024", "C008", "FAIL", "Stage 1 R38 fail: lat pulldown ↔ DB fly"),
    ("C002", "C032", "PASS", "reference.md §R3: Smith incline press + cable seated row"),
    ("C040", "C065", "PASS", "Stage 1 walkthrough S1.9: preacher ↔ goblet squat"),
    ("C041", "C068", "PASS", "Stage 1 walkthrough S1.9: spider curl ↔ wall sit (hold)"),
    ("C072", "C070", "PASS", "R38: one muscle across two joint actions (prone curl ↔ RDL)"),
    ("C138", "C018", "FAIL", "v7 focus A, superset 4: front raise ↔ band reverse fly"),
    ("C138", "C017", "FAIL", "v7 focus C, superset 3: front raise ↔ chest-supported rear fly"),
    ("C036", "C009", "REVIEW", "heavy compound with an isolation: the plan states the judgement"),
    ("C036", "C017", "FAIL", "shared bench and muscles"),
    ("C060", "C001", "REVIEW", "a trunk hold beside a heavy press: the plan states why bracing stays fresh"),
    ("C031", "C039", "PASS", "v8 focus B, superset 2: pullover ↔ prone Y raise (with a NOTE: both braced overhead)"),
]


def main(argv):
    path = "gymspec/ExerciseCatalogue.json"
    if "--catalogue" in argv:
        i = argv.index("--catalogue"); path = argv[i + 1]; del argv[i:i + 2]
    rows, ix = load(path)
    ok = True
    if argv and argv[0] == "--selftest":
        for a, b, exp, src in SELFTEST:
            v, _, _ = check_pair(ix[a], ix[b])
            good = v == exp
            ok = ok and good
            print(f"{'ok ' if good else 'BAD'} {v:6s} expected {exp:6s} {a}–{b}  {src}")
        print("SELFTEST PASS" if ok else "SELFTEST FAIL")
        return 0 if ok else 1
    if argv and argv[0] == "--pair":
        while argv:
            if argv[0] != "--pair" or len(argv) < 3:
                print(__doc__); return 2
            v = show("", ix[argv[1]], ix[argv[2]])
            ok = ok and v != "FAIL"
            argv = argv[3:]
        return 0 if ok else 1
    if not argv:
        print(__doc__); return 2
    for f in argv:
        ok = check_file(f, rows) and ok
    print("ALL PAIRS PASS (REVIEW and NOTE lines need a stated judgement)" if ok else "PAIR CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
