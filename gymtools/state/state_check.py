"""State-file check for gymstate/block_NN.json (Stage 2 R67 · §3.4 · R66 (10)).

Run from the Gym folder:
  python3 -B gymtools/state/state_check.py                      the newest gymstate/block_NN.json
  python3 -B gymtools/state/state_check.py gymstate/block_01.json
  python3 -B gymtools/state/state_check.py --selftest           planted faults, each must FAIL

Reads, from the Gym folder this script sits in:
- gymspec/Stage0_PolicyDefinition.md: the §4.1 field names, the §2.2 goal rows, the §1.2 sport columns;
- gymspec/ExerciseCatalogue.json: the muscles with their region, and the joints (its vocabulary);
- gymspec/Stage2_SupplementInfo.md §9: the register's stems and regions;
- gymplan/: the routine files.

Checks:
- name and number: block_NN.json, and "block" equals NN (Stage 2 §3.4);
- fields: exactly block, current_state, plan, log; current_state exactly the Stage 0 §4.1 fields; each current
  routine, plan and log row exactly its Stage 2 §3.4 keys; types;
- the Stage 0 §4.1 invariants: block type; one goal row, or "not trained", per region, at least one region trained;
  every priority target a catalogue muscle of a trained region; every joint at loading stage 1-4; every in-season
  sport with a profile; per region, at most 3 training sessions a week across the current routines (R20);
- each current routine: gymplan/<stem>.svg exists, the register lists it, and its regions are the register's and
  trained by the block;
- plan: null (a NOTE while routines are current) or its fields, with a YYYY-MM-DD approval date;
- log: at least one row; YYYY-MM-DD dates that never go back; at least one change per row.
A FAIL exits 1. A NOTE is a judgement the delivery states.
"""
import copy
import datetime
import json
import pathlib
import re
import sys

TOP_KEYS = {"block", "current_state", "plan", "log"}
ROUTINE_KEYS = {"stem", "regions", "sessions_week"}
PLAN_KEYS = {"version", "approved", "routines", "checks", "zone_coverage", "progression", "suspensions"}
LOG_KEYS = {"date", "changes", "follow_ups"}
REGIONS = ("upper", "lower")
NOT_TRAINED = "not trained"
BLOCK_TYPES = ("focus", "maintenance")
NAME = re.compile(r"block_(\d{2})\.json")


def section(text, head):
    """Text after the heading matching head, up to the next ## or ### heading."""
    m = re.search(head, text, re.M)
    if not m:
        raise SystemExit(f"FAIL cannot find {head!r} in the spec")
    rest = text[m.end():]
    e = re.search(r"^#{2,3} ", rest, re.M)
    return rest[:e.start()] if e else rest


def register(sec):
    """Stem -> regions from the register table; grouped stems ("_B") and per-stem regions ("upper · lower")."""
    def regs(part):
        return set() if part in ("—", "-", "") else {r.strip() for r in part.split("+")}
    reg = {}
    for line in sec.splitlines():
        if not line.startswith("| ") or line.startswith("| Stem ") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        stems = [s.strip() for s in cells[0].split("·")]
        full = [stems[0]] + [stems[0].rsplit("_", 1)[0] + s if s.startswith("_") else s for s in stems[1:]]
        parts = [p.strip() for p in cells[2].split("·")]
        if len(full) > 1 and len(parts) == len(full):
            reg.update({s: regs(p) for s, p in zip(full, parts)})
        else:
            both = set().union(*(regs(p) for p in parts))
            reg.update({s: set(both) for s in full})
    return reg


class Spec:
    """What the check reads from the spec docs, the catalogue and gymplan/."""

    def __init__(self, gym):
        spec = gym / "gymspec"
        p0 = (spec / "Stage0_PolicyDefinition.md").read_text(encoding="utf-8")
        rows = re.findall(r"^\| `(\w+)` \| ([^|]*)\|", section(p0, r"^### 4\.1 .*$"), re.M)
        self.fields = [f for f, d in rows if not d.strip().startswith("Derived")]
        self.goals = re.findall(r"^\| ([A-Z][^|]*?) \| \d", section(p0, r"^### 2\.2 .*$"), re.M)
        head = re.search(r"^\| Field \|(.*)\|\s*$", section(p0, r"^### 1\.2 .*$"), re.M)
        self.sports = [c.strip().lower() for c in head.group(1).split("|") if c.strip()]
        cat = json.loads((spec / "ExerciseCatalogue.json").read_text(encoding="utf-8"))
        self.muscles = {m["id"]: m["region"] for m in cat["vocabulary"]["muscles"]}
        self.joints = [j["id"] for j in cat["vocabulary"]["joints"]]
        s2 = (spec / "Stage2_SupplementInfo.md").read_text(encoding="utf-8")
        self.register = register(section(s2, r"^## 9\. Register.*$"))
        self.plan_dir = {p.stem for p in (gym / "gymplan").glob("*.svg")}


def iso(d):
    if not isinstance(d, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        return False
    try:
        datetime.date.fromisoformat(d)
        return True
    except ValueError:
        return False


def whole(n, low):
    return isinstance(n, int) and not isinstance(n, bool) and n >= low


def keys(obj, want, where, F, extra="unknown field"):
    for k in sorted(want - obj.keys()):
        F(f"{where}: {k} missing")
    for k in sorted(obj.keys() - want):
        F(f"{where}: {k} — {extra}")


def check_state(cs, spec, F):
    """Current state against Stage 0 §4.1; returns the trained regions."""
    keys(cs, set(spec.fields), "current_state", F, extra="not a Stage 0 §4.1 field")
    bt = cs.get("block_type")
    if "block_type" in cs and bt not in BLOCK_TYPES:
        F(f"block_type {bt!r}: not focus or maintenance (Stage 0 §0.3)")
    trained = set()
    goal = cs.get("block_goal")
    if "block_goal" in cs:
        if not isinstance(goal, dict):
            F("block_goal: not an object of upper and lower")
        else:
            keys(goal, set(REGIONS), "block_goal", F)
            for r in REGIONS:
                if r in goal and goal[r] != NOT_TRAINED and goal[r] not in spec.goals:
                    F(f'block_goal {r}: {goal[r]!r} is not a goal row of Stage 0 §2.2 or "not trained"')
            trained = {r for r in REGIONS if r in goal and goal[r] != NOT_TRAINED}
            if not trained:
                F("block_goal: the block trains no region")
    pt = cs.get("priority_targets")
    if "priority_targets" in cs and not (bt == "maintenance" and pt == "every muscle group"):
        if not isinstance(pt, list) or not pt or not all(isinstance(x, str) for x in pt):
            F("priority_targets: not a list of muscles (Stage 0 §4.1)")
        else:
            if len(set(pt)) < len(pt):
                F("priority_targets: a muscle listed twice")
            for x in pt:
                if x not in spec.muscles:
                    F(f"priority target {x!r}: not a catalogue muscle")
                elif spec.muscles[x] not in trained:
                    F(f"priority target {x!r}: a {spec.muscles[x]}-body muscle, in a region the block does not train (Stage 0 §4.1)")
    if "layoff" in cs and (not isinstance(cs["layoff"], str) or not cs["layoff"].strip()):
        F("layoff: empty")
    ls = cs.get("loading_stages")
    if "loading_stages" in cs:
        if not isinstance(ls, dict):
            F("loading_stages: not an object of joint -> stage")
        else:
            for j in spec.joints:
                if j not in ls:
                    F(f"loading stage of {j}: missing — every joint has one (Stage 0 §4.1)")
            for j, v in ls.items():
                if j not in spec.joints:
                    F(f"loading stage of {j!r}: not a joint of the catalogue")
                elif not (whole(v, 1) and v <= 4):
                    F(f"loading stage of {j}: {v!r}, not 1–4 (Stage 0 §2.5)")
    ins = cs.get("in_season")
    if "in_season" in cs:
        if not isinstance(ins, list) or not all(isinstance(x, str) for x in ins):
            F("in_season: not a list of sports")
        else:
            for s in ins:
                if s.lower() not in spec.sports:
                    F(f"in-season sport {s!r}: no profile in Stage 0 §1.2")
    cr = cs.get("current_routines")
    if "current_routines" in cs:
        if not isinstance(cr, list):
            F("current_routines: not a list")
            return trained
        per, seen = {r: 0 for r in REGIONS}, set()
        for i, rt in enumerate(cr):
            where = f"current routine {i + 1}"
            if not isinstance(rt, dict):
                F(f"{where}: not an object")
                continue
            keys(rt, ROUTINE_KEYS, where, F)
            stem = rt.get("stem")
            if isinstance(stem, str) and stem:
                where = stem
                if stem in seen:
                    F(f"{stem}: listed twice")
                seen.add(stem)
                if stem not in spec.plan_dir:
                    F(f"{stem}: no gymplan/{stem}.svg")
                if stem not in spec.register:
                    F(f"{stem}: not in the register (Stage 2 Supplement §9 · R52)")
            regs = rt.get("regions")
            if not isinstance(regs, list) or not regs or any(r not in REGIONS for r in regs):
                F(f"{where}: regions {regs!r} — a list of upper and/or lower")
                regs = []
            elif isinstance(stem, str) and stem in spec.register and not set(regs) <= spec.register[stem]:
                F(f"{where}: regions {regs} differ from the register's {sorted(spec.register[stem])}")
            for r in regs:
                if r not in trained:
                    F(f"{where}: trains {r}, a region the block does not train (Stage 0 §4.1 block_goal)")
            sw = rt.get("sessions_week")
            if not whole(sw, 1):
                F(f"{where}: sessions_week {sw!r} — a whole number, at least 1")
            else:
                for r in set(regs):
                    per[r] += sw
        for r, n in per.items():
            if n > 3:
                F(f"{r} region: {n} training sessions a week across the current routines, more than 3 (R20)")
    return trained


def check(state, name, spec):
    """All checks on one state file; returns (fails, notes)."""
    fails, notes = [], []
    F = fails.append
    m = NAME.fullmatch(name)
    if not m:
        F(f"name {name}: not block_NN.json (Stage 2 §3.4)")
    if not isinstance(state, dict):
        F("the file is not a JSON object")
        return fails, notes
    keys(state, TOP_KEYS, "the file", F)
    if m and state.get("block") != int(m.group(1)):
        F(f"block number {state.get('block')!r} differs from the name's {int(m.group(1))} (Stage 2 §3.4)")
    cs = state.get("current_state")
    if not isinstance(cs, dict):
        F("current_state: not an object")
        cs = {}
    else:
        check_state(cs, spec, F)
    if "plan" in state:
        plan = state["plan"]
        if plan is None:
            if cs.get("current_routines"):
                notes.append("plan is null while routines are current: their plan-only fields are not kept (Stage 2 §3.4)")
        elif not isinstance(plan, dict):
            F("plan: not an object or null")
        else:
            keys(plan, PLAN_KEYS, "plan", F)
            if "approved" in plan and not iso(plan["approved"]):
                F(f"plan approved {plan['approved']!r}: not a YYYY-MM-DD date")
            rts = plan.get("routines")
            if "routines" in plan:
                if not isinstance(rts, list) or not all(isinstance(x, dict) and set(x) == {"stem", "version"} for x in rts):
                    F("plan routines: not a list of {stem, version}")
                else:
                    for x in rts:
                        if x["stem"] not in spec.plan_dir:
                            F(f"plan routine {x['stem']}: no gymplan/{x['stem']}.svg")
            for k in ("checks", "zone_coverage", "progression"):
                if k in plan and (not isinstance(plan[k], list) or not all(isinstance(x, str) for x in plan[k])):
                    F(f"plan {k}: not a list of lines")
            if "suspensions" in plan and plan["suspensions"] is not None and not isinstance(plan["suspensions"], str):
                F("plan suspensions: not text or null")
    if "log" in state:
        log = state["log"]
        if not isinstance(log, list) or not log:
            F("log: no rows — every conversation that changed the file adds one (R67)")
        else:
            last = None
            for i, row in enumerate(log):
                where = f"log row {i + 1}"
                if not isinstance(row, dict):
                    F(f"{where}: not an object")
                    continue
                keys(row, LOG_KEYS, where, F)
                d = row.get("date")
                if "date" in row:
                    if not iso(d):
                        F(f"{where}: date {d!r} — not YYYY-MM-DD")
                    else:
                        if last and d < last:
                            F(f"{where}: date {d} before the row above ({last}); log dates never go back")
                        last = d
                ch = row.get("changes")
                if "changes" in row and (not isinstance(ch, list) or not ch or not all(isinstance(x, str) and x.strip() for x in ch)):
                    F(f"{where}: changes — at least one line")
                fu = row.get("follow_ups")
                if "follow_ups" in row and (not isinstance(fu, list) or not all(isinstance(x, str) for x in fu)):
                    F(f"{where}: follow_ups — not a list of lines")
    return fails, notes


def selftest(gym):
    spec = Spec(gym)
    # Its own routine set, so the test does not depend on which files gymplan/ holds today.
    spec.plan_dir = {"routine_t_A", "routine_t_B", "routine_t_C", "routine_t_lower"}
    spec.register = {"routine_t_A": {"upper"}, "routine_t_B": {"upper"}, "routine_t_C": {"upper"}, "routine_t_lower": {"lower"}}
    values = {
        "block_type": "focus",
        "block_goal": {"upper": spec.goals[0], "lower": NOT_TRAINED},
        "priority_targets": [m for m, r in spec.muscles.items() if r == "upper"][:2],
        "layoff": "~2 months",
        "loading_stages": {j: 1 for j in spec.joints},
        "in_season": [spec.sports[0]],
        "current_routines": [{"stem": "routine_t_A", "regions": ["upper"], "sessions_week": 1},
                             {"stem": "routine_t_B", "regions": ["upper"], "sessions_week": 1}],
    }
    missing = [f for f in spec.fields if f not in values]
    if missing:
        print(f"FAIL selftest: no fixture value for Stage 0 §4.1 field(s) {missing}")
        return 1
    base = {"block": 1,
            "current_state": {f: values[f] for f in spec.fields},
            "plan": {"version": "v1", "approved": "2026-10-25", "routines": [{"stem": "routine_t_A", "version": 1}],
                     "checks": ["(1) hard gates — PASS"], "zone_coverage": ["chest: L and M"],
                     "progression": ["card 1: next step"], "suspensions": None},
            "log": [{"date": "2026-10-24", "changes": ["file started"], "follow_ups": []},
                    {"date": "2026-10-25", "changes": ["knee: loading stage 1 -> 2"], "follow_ups": ["one"]}]}
    lower = next(m for m, r in spec.muscles.items() if r == "lower")
    cs = lambda s: s["current_state"]
    faults = [
        ("a Stage 0 §4.1 field missing", lambda s: cs(s).pop("layoff"), "layoff missing"),
        ("a field Stage 0 §4.1 does not have", lambda s: cs(s).__setitem__("block_start", "2026-10-13"), "not a Stage 0 §4.1 field"),
        ("block type", lambda s: cs(s).__setitem__("block_type", "strength"), "block_type"),
        ("goal row", lambda s: cs(s)["block_goal"].__setitem__("upper", "Bulk"), "not a goal row"),
        ("no region trained", lambda s: cs(s)["block_goal"].__setitem__("upper", NOT_TRAINED), "trains no region"),
        ("target in an untrained region", lambda s: cs(s)["priority_targets"].append(lower), "does not train"),
        ("unknown muscle", lambda s: cs(s)["priority_targets"].append("lats2"), "not a catalogue muscle"),
        ("target listed twice", lambda s: cs(s)["priority_targets"].append(cs(s)["priority_targets"][0]), "listed twice"),
        ("joint without a stage", lambda s: cs(s)["loading_stages"].pop(spec.joints[-1]), "every joint has one"),
        ("stage out of range", lambda s: cs(s)["loading_stages"].__setitem__(spec.joints[0], 5), "not 1–4"),
        ("sport without a profile", lambda s: cs(s).__setitem__("in_season", ["tennis"]), "no profile"),
        ("routine not in gymplan/", lambda s: cs(s)["current_routines"].append({"stem": "routine_t_missing", "regions": ["upper"], "sessions_week": 1}), "no gymplan/"),
        ("routine in an untrained region", lambda s: cs(s)["current_routines"].append({"stem": "routine_t_lower", "regions": ["lower"], "sessions_week": 1}), "trains lower"),
        ("four upper sessions a week", lambda s: cs(s)["current_routines"].append({"stem": "routine_t_C", "regions": ["upper"], "sessions_week": 2}), "(R20)"),
        ("regions unlike the register", lambda s: cs(s)["current_routines"][0].__setitem__("regions", ["upper", "lower"]), "differ from the register"),
        ("sessions a week as text", lambda s: cs(s)["current_routines"][0].__setitem__("sessions_week", "1"), "sessions_week"),
        ("log date going back", lambda s: s["log"].append({"date": "2026-10-01", "changes": ["x"], "follow_ups": []}), "never go back"),
        ("log row without changes", lambda s: s["log"][0].__setitem__("changes", []), "at least one line"),
        ("number unlike the name", lambda s: s.__setitem__("block", 2), "differs from the name"),
        ("plan approval date", lambda s: s["plan"].__setitem__("approved", "yesterday"), "YYYY-MM-DD"),
        ("unknown top-level field", lambda s: s.__setitem__("notes", "x"), "unknown field"),
    ]
    f, n = check(copy.deepcopy(base), "block_01.json", spec)
    clean = not f
    print(("PASS" if clean else "FAIL") + f" clean fixture: {len(f)} FAIL, {len(n)} NOTE" + ("" if clean else f" {f}"))
    caught = 0
    for label, mutate, expect in faults:
        s = copy.deepcopy(base)
        mutate(s)
        f, _ = check(s, "block_01.json", spec)
        hit = next((x for x in f if expect in x), None)
        caught += bool(hit)
        print(("PASS" if hit else "FAIL") + f" planted: {label} -> " + (hit or f"not caught: {f}"))
    f, _ = check(copy.deepcopy(base), "block_1.json", spec)
    hit = next((x for x in f if "not block_NN.json" in x), None)
    caught += bool(hit)
    print(("PASS" if hit else "FAIL") + " planted: file name block_1.json -> " + (hit or f"not caught: {f}"))
    total = len(faults) + 1
    print(f"RESULT: {caught}/{total} planted faults caught; clean fixture {'passes' if clean else 'FAILS'}")
    return 0 if clean and caught == total else 1


def main(argv):
    gym = pathlib.Path(__file__).resolve().parents[2]
    if argv[1:] == ["--selftest"]:
        return selftest(gym)
    if len(argv) > 1:
        path = pathlib.Path(argv[1])
    else:
        files = sorted((gym / "gymstate").glob("block_*.json"))
        if not files:
            print("FAIL no gymstate/block_NN.json (R67)")
            return 1
        path = files[-1]
    spec = Spec(gym)
    print(f"State file: {path.name} · Stage 0 §4.1 fields: {', '.join(spec.fields)} · goals: {', '.join(spec.goals)}"
          f" · sports: {', '.join(spec.sports)} · {len(spec.joints)} joints · {len(spec.muscles)} muscles"
          f" · {len(spec.register)} register stems · {len(spec.plan_dir)} files in gymplan/")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"FAIL {path.name}: {e}")
        print("RESULT: 1 FAIL")
        return 1
    fails, notes = check(state, path.name, spec)
    newest = sorted(p.name for p in path.parent.glob("block_*.json"))
    if newest and path.name != newest[-1]:
        notes.append(f"{path.name} is not the newest state file ({newest[-1]}), so not the current block (R67)")
    for x in notes:
        print(f"NOTE {x}")
    for x in fails:
        print(f"FAIL {x}")
    print(f"RESULT: {len(fails)} FAIL" if fails else "RESULT: clean" + (f" ({len(notes)} NOTE)" if notes else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
