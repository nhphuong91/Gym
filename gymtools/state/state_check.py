"""State-file check for the athlete record and the track block files (Stage 2 R67 · R68 · §3.4 · R66 (10)).

Run from the Gym folder:
  python3 -B gymtools/state/state_check.py                                    athlete.json and every gymstate/<track>/block_NN.json
  python3 -B gymtools/state/state_check.py gymstate/Lower_STR/block_01.json   one block file, read with athlete.json
  python3 -B gymtools/state/state_check.py gymstate/athlete.json              the athlete record alone
  python3 -B gymtools/state/state_check.py --across Delt_Abs_archery Lower_STR
        only when Harry asks (Stage 0 §0.1 · D-103): training sessions a week per region over the newest block of each
        track named (Stage 0 R20); the cross-routine guard and the sport notes are judged from the routine files
  python3 -B gymtools/state/state_check.py --selftest                         planted faults, each must FAIL

Reads, from the Gym folder this script sits in:
- gymspec/Stage0_PolicyDefinition.md: the §4.1 field names, the §2.2 goal rows, the §1.2 sport columns;
- gymspec/ExerciseCatalogue.json: the muscles with their region, and the joints (its vocabulary);
- gymspec/Stage2_SupplementInfo.md §9: the register's tracks, stems and regions;
- gymplan/: the routine files, directly in it (shared) and in each track folder (Stage 2 §0.1).

Checks:
- athlete record: exactly loading_stages, in_season and log; every catalogue joint at loading stage 1-4; every
  in-season sport with a Stage 0 §1.2 profile; log rows of date, changes and follow_ups;
- block file name and place: gymstate/<track>/block_NN.json; "track" equals the folder and "block" equals NN; no
  block file left directly in gymstate/ (the single chain before Stage 2 D-16);
- fields: exactly track, block, status, builds_on, current_state, plan, log; current_state exactly the Stage 0 §4.1
  fields but loading_stages and in_season; each current routine, plan and log row exactly its Stage 2 §3.4 keys; types;
- status prepared, active or finished; builds_on null in a track's block_01, otherwise its previous block, which exists;
- the Stage 0 §4.1 invariants: block type; one goal row, or "not trained", per region, at least one region trained;
  every priority target a catalogue muscle of a trained region; per region, at most 3 training sessions a week across
  the block's current routines (R20);
- each current routine and plan routine: its path is a file in the track's own folder or directly in gymplan/ (no other
  track's, Stage 0 D-102); a current routine is in the register, with the register's regions, trained by the block;
- plan: null (a NOTE while routines are current) or its fields, with a YYYY-MM-DD approval date and built_with; a NOTE
  for every difference between built_with and the athlete record, which the next conversation on the track names (R68);
- log: at least one row; YYYY-MM-DD dates that never go back; at least one change per row; follow_ups and, in a block
  file, spec_gaps as lists of lines.
A FAIL exits 1. A NOTE is a judgement the delivery states.
"""
import copy
import datetime
import json
import pathlib
import re
import sys

BLOCK_KEYS = {"track", "block", "status", "builds_on", "current_state", "plan", "log"}
ATHLETE_KEYS = {"loading_stages", "in_season", "log"}
ATHLETE_FIELDS = ("loading_stages", "in_season")
ROUTINE_KEYS = {"path", "regions", "sessions_week"}
PLAN_KEYS = {"version", "approved", "routines", "checks", "zone_coverage", "progression", "suspensions", "built_with"}
LOG_KEYS = {"date", "changes", "follow_ups", "spec_gaps"}
ATHLETE_LOG_KEYS = {"date", "changes", "follow_ups"}
STATUSES = ("prepared", "active", "finished")
REGIONS = ("upper", "lower")
NOT_TRAINED = "not trained"
BLOCK_TYPES = ("focus", "maintenance")
NAME = re.compile(r"block_(\d{2})\.json")
ARCHIVE = "PreviousOldRoutines"


def section(text, head):
    """Text after the heading matching head, up to the next ## or ### heading."""
    m = re.search(head, text, re.M)
    if not m:
        raise SystemExit(f"FAIL cannot find {head!r} in the spec")
    rest = text[m.end():]
    e = re.search(r"^#{2,3} ", rest, re.M)
    return rest[:e.start()] if e else rest


def register(sec):
    """Path -> regions from the register table (Track | Stem | Role | Regions | Build): a track's file is <track>/<stem>,
    a shared file (track "—") its stem; grouped stems ("_B") and per-stem regions ("upper · lower")."""
    def regs(part):
        return set() if part in ("—", "-", "") else {r.strip() for r in part.split("+")}
    reg = {}
    for line in sec.splitlines():
        if not line.startswith("| ") or line.startswith("| Track ") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        track = cells[0]
        stems = [s.strip() for s in cells[1].split("·")]
        full = [stems[0]] + [stems[0].rsplit("_", 1)[0] + s if s.startswith("_") else s for s in stems[1:]]
        full = [s if track in ("—", "-", "") else f"{track}/{s}" for s in full]
        parts = [p.strip() for p in cells[3].split("·")]
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
        lost = [f for f in ATHLETE_FIELDS if f not in self.fields]
        if lost:
            raise SystemExit(f"FAIL Stage 0 §4.1 has no {', '.join(lost)}, the athlete fields of Stage 2 §3.4")
        self.block_fields = [f for f in self.fields if f not in ATHLETE_FIELDS]
        self.goals = re.findall(r"^\| ([A-Z][^|]*?) \| \d", section(p0, r"^### 2\.2 .*$"), re.M)
        head = re.search(r"^\| Field \|(.*)\|\s*$", section(p0, r"^### 1\.2 .*$"), re.M)
        self.sports = [c.strip().lower() for c in head.group(1).split("|") if c.strip()]
        cat = json.loads((spec / "ExerciseCatalogue.json").read_text(encoding="utf-8"))
        self.muscles = {m["id"]: m["region"] for m in cat["vocabulary"]["muscles"]}
        self.joints = [j["id"] for j in cat["vocabulary"]["joints"]]
        s2 = (spec / "Stage2_SupplementInfo.md").read_text(encoding="utf-8")
        self.register = register(section(s2, r"^## 9\. Register.*$"))
        plan = gym / "gymplan"
        self.plan_dir = {p.stem for p in plan.glob("*.svg")}
        for d in sorted(plan.iterdir()) if plan.is_dir() else []:
            if d.is_dir() and d.name != ARCHIVE:
                self.plan_dir |= {f"{d.name}/{p.stem}" for p in d.glob("*.svg")}


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


def lines(x):
    return isinstance(x, list) and all(isinstance(s, str) for s in x)


def check_stages(ls, spec, F, where="loading stage"):
    if not isinstance(ls, dict):
        F(f"{where}s: not an object of joint -> stage")
        return
    for j in spec.joints:
        if j not in ls:
            F(f"{where} of {j}: missing — every joint has one (Stage 0 §4.1)")
    for j, v in ls.items():
        if j not in spec.joints:
            F(f"{where} of {j!r}: not a joint of the catalogue")
        elif not (whole(v, 1) and v <= 4):
            F(f"{where} of {j}: {v!r}, not 1–4 (Stage 0 §2.5)")


def check_sports(ins, spec, F, where="in-season sport"):
    if not lines(ins):
        F(f"{where}s: not a list of sports")
        return
    for s in ins:
        if s.lower() not in spec.sports:
            F(f"{where} {s!r}: no profile in Stage 0 §1.2")


def check_log(log, want, F):
    if not isinstance(log, list) or not log:
        F("log: no rows — every conversation that changed the file adds one (R67)")
        return
    last = None
    for i, row in enumerate(log):
        where = f"log row {i + 1}"
        if not isinstance(row, dict):
            F(f"{where}: not an object")
            continue
        keys(row, want, where, F)
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
        for k in ("follow_ups", "spec_gaps"):
            if k in row and k in want and not lines(row[k]):
                F(f"{where}: {k} — not a list of lines")


def check_athlete(rec, spec):
    """The athlete record against Stage 2 §3.4; returns (fails, notes)."""
    fails, notes = [], []
    F = fails.append
    if not isinstance(rec, dict):
        F("the athlete record is not a JSON object")
        return fails, notes
    keys(rec, ATHLETE_KEYS, "the athlete record", F)
    if "loading_stages" in rec:
        check_stages(rec["loading_stages"], spec, F)
    if "in_season" in rec:
        check_sports(rec["in_season"], spec, F)
    if "log" in rec:
        check_log(rec["log"], ATHLETE_LOG_KEYS, F)
    return fails, notes


def own_path(path, track, where, F):
    """A routine path is a file of this track's folder or a shared file directly in gymplan/ (Stage 0 D-102)."""
    if "/" in path and not path.startswith(track + "/"):
        F(f"{where}: {path} is another track's routine (Stage 0 D-102)")
        return False
    return True


def check_state(cs, spec, track, F):
    """A block's Current state against Stage 0 §4.1, the athlete fields aside; returns the trained regions."""
    keys(cs, set(spec.block_fields), "current_state", F,
         extra="not a block field of Stage 0 §4.1 (the athlete fields sit in gymstate/athlete.json)")
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
            path = rt.get("path")
            if isinstance(path, str) and path:
                where = path
                if path in seen:
                    F(f"{path}: listed twice")
                seen.add(path)
                own_path(path, track, "current routine", F)
                if path not in spec.plan_dir:
                    F(f"{path}: no gymplan/{path}.svg")
                if path not in spec.register:
                    F(f"{path}: not in the register (Stage 2 Supplement §9 · R52)")
            regs = rt.get("regions")
            if not isinstance(regs, list) or not regs or any(r not in REGIONS for r in regs):
                F(f"{where}: regions {regs!r} — a list of upper and/or lower")
                regs = []
            elif isinstance(path, str) and path in spec.register and not set(regs) <= spec.register[path]:
                F(f"{where}: regions {regs} differ from the register's {sorted(spec.register[path])}")
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
                F(f"{r} region: {n} training sessions a week across the block's current routines, more than 3 (R20)")
    return trained


def built_with_notes(bw, athlete):
    """R68: each difference between a plan's built_with and the athlete record."""
    out = []
    a_ls, b_ls = athlete.get("loading_stages") or {}, bw.get("loading_stages") or {}
    for j in sorted(set(a_ls) | set(b_ls)):
        if a_ls.get(j) != b_ls.get(j):
            out.append(f"{j} {b_ls.get(j, '—')} → {a_ls.get(j, '—')}")
    a_in, b_in = sorted(athlete.get("in_season") or []), sorted(bw.get("in_season") or [])
    if a_in != b_in:
        out.append(f"in_season {b_in or 'none'} → {a_in or 'none'}")
    return out


def check_block(state, name, folder, siblings, spec, athlete):
    """All checks on one block file; returns (fails, notes)."""
    fails, notes = [], []
    F = fails.append
    m = NAME.fullmatch(name)
    if not m:
        F(f"name {name}: not block_NN.json (Stage 2 §3.4)")
    if not isinstance(state, dict):
        F("the file is not a JSON object")
        return fails, notes
    keys(state, BLOCK_KEYS, "the file", F)
    track = state.get("track")
    if "track" in state and track != folder:
        F(f"track {track!r} differs from its folder {folder!r} (Stage 2 §3.4)")
    nn = int(m.group(1)) if m else None
    if m and "block" in state and state.get("block") != nn:
        F(f"block number {state.get('block')!r} differs from the name's {nn} (Stage 2 §3.4)")
    if "status" in state and state["status"] not in STATUSES:
        F(f"status {state['status']!r}: not prepared, active or finished (Stage 2 §3.4)")
    if "builds_on" in state and nn is not None:
        bo = state["builds_on"]
        if nn == 1:
            if bo is not None:
                F(f"builds_on {bo!r}: a track's block_01 builds on nothing (null, Stage 2 §3.4)")
        else:
            prev = f"block_{nn - 1:02d}"
            if bo != prev:
                F(f"builds_on {bo!r}: not the track's previous block, {prev} (Stage 2 §3.4)")
            elif f"{prev}.json" not in siblings:
                F(f"builds_on {bo}: no gymstate/{folder}/{prev}.json — a track's blocks form one chain (Stage 2 §3.4)")
    cs = state.get("current_state")
    if not isinstance(cs, dict):
        F("current_state: not an object")
        cs = {}
    else:
        check_state(cs, spec, folder, F)
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
                if not isinstance(rts, list) or not all(isinstance(x, dict) and set(x) == {"path", "version"} for x in rts):
                    F("plan routines: not a list of {path, version}")
                else:
                    for x in rts:
                        if not isinstance(x["path"], str) or not whole(x["version"], 1):
                            F(f"plan routine {x}: a path and a version of at least 1")
                            continue
                        if own_path(x["path"], folder, "plan routine", F) and x["path"] not in spec.plan_dir:
                            F(f"plan routine {x['path']}: no gymplan/{x['path']}.svg")
            for k in ("checks", "zone_coverage", "progression"):
                if k in plan and not lines(plan[k]):
                    F(f"plan {k}: not a list of lines")
            if "suspensions" in plan and plan["suspensions"] is not None and not isinstance(plan["suspensions"], str):
                F("plan suspensions: not text or null")
            bw = plan.get("built_with")
            if "built_with" in plan:
                if not isinstance(bw, dict):
                    F("plan built_with: not an object of loading_stages and in_season")
                else:
                    keys(bw, set(ATHLETE_FIELDS), "plan built_with", F)
                    if "loading_stages" in bw and not (isinstance(bw["loading_stages"], dict) and all(
                            whole(v, 1) and v <= 4 for v in bw["loading_stages"].values())):
                        F("plan built_with loading_stages: not an object of joint -> stage 1–4")
                    if "in_season" in bw and not lines(bw["in_season"]):
                        F("plan built_with in_season: not a list of sports")
                    if isinstance(athlete, dict):
                        diff = built_with_notes(bw, athlete)
                        if diff:
                            notes.append("the athlete record changed since this plan: " + "; ".join(diff)
                                         + " — the next conversation on this track names it first (R68)")
    if "log" in state:
        check_log(state["log"], LOG_KEYS, F)
    return fails, notes


def across_counts(blocks):
    """Sessions a week per region over the named tracks' newest blocks: [(track, current_routines)] -> (lines, fails)."""
    per = {r: [] for r in REGIONS}
    for track, cr in blocks:
        for rt in cr or []:
            for r in set(rt.get("regions") or []):
                if r in per and whole(rt.get("sessions_week"), 1):
                    per[r].append((track, rt["sessions_week"]))
    out, fails = [], []
    for r in REGIONS:
        n = sum(s for _, s in per[r])
        by = ", ".join(f"{t} {s}" for t, s in per[r]) or "none"
        out.append(f"{r}: {n} training sessions a week ({by})")
        if n > 3:
            fails.append(f"{r} region: {n} training sessions a week across {', '.join(sorted({t for t, _ in per[r]}))}, more than 3 (R20)")
    return out, fails


def selftest(gym):
    spec = Spec(gym)
    # Its own routine set, register and athlete record, so the test does not depend on gymplan/ or gymstate/ today.
    spec.plan_dir = {"T/routine_t_A", "T/routine_t_B", "T/routine_t_C", "T/routine_t_lower", "routine_t_shared", "U/routine_t_A"}
    spec.register = {"T/routine_t_A": {"upper"}, "T/routine_t_B": {"upper"}, "T/routine_t_C": {"upper"},
                     "T/routine_t_lower": {"lower"}, "routine_t_shared": set(), "U/routine_t_A": {"upper"}}
    athlete = {"loading_stages": {j: 1 for j in spec.joints}, "in_season": [spec.sports[0]],
               "log": [{"date": "2026-10-24", "changes": ["record started"], "follow_ups": []}]}
    values = {
        "block_type": "focus",
        "block_goal": {"upper": spec.goals[0], "lower": NOT_TRAINED},
        "priority_targets": [m for m, r in spec.muscles.items() if r == "upper"][:2],
        "layoff": "~2 months",
        "current_routines": [{"path": "T/routine_t_A", "regions": ["upper"], "sessions_week": 1},
                             {"path": "T/routine_t_B", "regions": ["upper"], "sessions_week": 1}],
    }
    missing = [f for f in spec.block_fields if f not in values]
    if missing:
        print(f"FAIL selftest: no fixture value for Stage 0 §4.1 field(s) {missing}")
        return 1
    base = {"track": "T", "block": 2, "status": "active", "builds_on": "block_01",
            "current_state": {f: values[f] for f in spec.block_fields},
            "plan": {"version": "v1", "approved": "2026-10-25",
                     "routines": [{"path": "T/routine_t_A", "version": 1}, {"path": "routine_t_shared", "version": 1}],
                     "checks": ["(1) hard gates — PASS"], "zone_coverage": ["chest: L and M"],
                     "progression": ["card 1: next step"], "suspensions": None,
                     "built_with": {"loading_stages": dict(athlete["loading_stages"]), "in_season": list(athlete["in_season"])}},
            "log": [{"date": "2026-10-24", "changes": ["file started"], "follow_ups": [], "spec_gaps": []},
                    {"date": "2026-10-25", "changes": ["plan v1 approved"], "follow_ups": ["one"], "spec_gaps": ["a gap"]}]}
    sib = {"block_01.json", "block_02.json"}
    lower = next(m for m, r in spec.muscles.items() if r == "lower")
    cs = lambda s: s["current_state"]

    def first_block(s):
        s["block"] = 1
        s["builds_on"] = "block_00"

    block_faults = [
        ("a block field missing", lambda s: cs(s).pop("layoff"), "layoff missing"),
        ("an athlete field in the block file", lambda s: cs(s).__setitem__("loading_stages", {}), "not a block field"),
        ("block type", lambda s: cs(s).__setitem__("block_type", "strength"), "block_type"),
        ("goal row", lambda s: cs(s)["block_goal"].__setitem__("upper", "Bulk"), "not a goal row"),
        ("no region trained", lambda s: cs(s)["block_goal"].__setitem__("upper", NOT_TRAINED), "trains no region"),
        ("target in an untrained region", lambda s: cs(s)["priority_targets"].append(lower), "does not train"),
        ("unknown muscle", lambda s: cs(s)["priority_targets"].append("lats2"), "not a catalogue muscle"),
        ("target listed twice", lambda s: cs(s)["priority_targets"].append(cs(s)["priority_targets"][0]), "listed twice"),
        ("routine not in gymplan/", lambda s: cs(s)["current_routines"].append({"path": "T/routine_t_missing", "regions": ["upper"], "sessions_week": 1}), "no gymplan/"),
        ("another track's routine", lambda s: cs(s)["current_routines"].append({"path": "U/routine_t_A", "regions": ["upper"], "sessions_week": 1}), "another track's routine"),
        ("routine in an untrained region", lambda s: cs(s)["current_routines"].append({"path": "T/routine_t_lower", "regions": ["lower"], "sessions_week": 1}), "trains lower"),
        ("four upper sessions a week", lambda s: cs(s)["current_routines"].append({"path": "T/routine_t_C", "regions": ["upper"], "sessions_week": 2}), "(R20)"),
        ("regions unlike the register", lambda s: cs(s)["current_routines"][0].__setitem__("regions", ["upper", "lower"]), "differ from the register"),
        ("sessions a week as text", lambda s: cs(s)["current_routines"][0].__setitem__("sessions_week", "1"), "sessions_week"),
        ("a routine named by stem", lambda s: cs(s)["current_routines"].__setitem__(0, {"stem": "routine_t_A", "regions": ["upper"], "sessions_week": 1}), "path missing"),
        ("log date going back", lambda s: s["log"].append({"date": "2026-10-01", "changes": ["x"], "follow_ups": [], "spec_gaps": []}), "never go back"),
        ("log row without changes", lambda s: s["log"][0].__setitem__("changes", []), "at least one line"),
        ("log row without spec_gaps", lambda s: s["log"][1].pop("spec_gaps"), "spec_gaps missing"),
        ("number unlike the name", lambda s: s.__setitem__("block", 3), "differs from the name"),
        ("plan approval date", lambda s: s["plan"].__setitem__("approved", "yesterday"), "YYYY-MM-DD"),
        ("unknown top-level field", lambda s: s.__setitem__("notes", "x"), "unknown field"),
        ("status", lambda s: s.__setitem__("status", "started"), "not prepared, active or finished"),
        ("builds_on not the previous block", lambda s: s.__setitem__("builds_on", "block_05"), "not the track's previous block"),
        ("track unlike its folder", lambda s: s.__setitem__("track", "V"), "differs from its folder"),
        ("plan routine by stem", lambda s: s["plan"].__setitem__("routines", [{"stem": "routine_t_A", "version": 1}]), "not a list of {path, version}"),
        ("plan routine of another track", lambda s: s["plan"]["routines"].append({"path": "U/routine_t_A", "version": 1}), "another track's routine"),
        ("plan without built_with", lambda s: s["plan"].pop("built_with"), "built_with missing"),
    ]
    athlete_faults = [
        ("joint without a stage", lambda a: a["loading_stages"].pop(spec.joints[-1]), "every joint has one"),
        ("stage out of range", lambda a: a["loading_stages"].__setitem__(spec.joints[0], 5), "not 1–4"),
        ("sport without a profile", lambda a: a.__setitem__("in_season", ["tennis"]), "no profile"),
        ("a block field in the athlete record", lambda a: a.__setitem__("current_routines", []), "unknown field"),
        ("athlete log date going back", lambda a: a["log"].append({"date": "2026-10-01", "changes": ["x"], "follow_ups": []}), "never go back"),
        ("spec gaps in the athlete log", lambda a: a["log"][0].__setitem__("spec_gaps", []), "spec_gaps — unknown field"),
    ]
    f, n = check_block(copy.deepcopy(base), "block_02.json", "T", sib, spec, athlete)
    fa, na = check_athlete(copy.deepcopy(athlete), spec)
    clean = not f and not n and not fa
    print(("PASS" if clean else "FAIL") + f" clean fixture: block {len(f)} FAIL, {len(n)} NOTE · athlete {len(fa)} FAIL"
          + ("" if clean else f" {f + n + fa}"))
    caught, total = 0, 0

    def report(label, found, expect, got):
        nonlocal caught, total
        total += 1
        hit = next((x for x in found if expect in x), None)
        caught += bool(hit)
        print(("PASS" if hit else "FAIL") + f" planted: {label} -> " + (hit or f"not caught: {got}"))

    for label, mutate, expect in block_faults:
        s = copy.deepcopy(base)
        mutate(s)
        f, _ = check_block(s, "block_02.json", "T", sib, spec, athlete)
        report(label, f, expect, f)
    s = copy.deepcopy(base)
    f, _ = check_block(s, "block_02.json", "T", {"block_02.json"}, spec, athlete)
    report("builds_on a missing block", f, "no gymstate/T/block_01.json", f)
    s = copy.deepcopy(base)
    first_block(s)
    f, _ = check_block(s, "block_01.json", "T", sib, spec, athlete)
    report("block_01 building on a block", f, "builds on nothing", f)
    f, _ = check_block(copy.deepcopy(base), "block_2.json", "T", sib, spec, athlete)
    report("file name block_2.json", f, "not block_NN.json", f)
    for label, mutate, expect in athlete_faults:
        a = copy.deepcopy(athlete)
        mutate(a)
        f, _ = check_athlete(a, spec)
        report(label, f, expect, f)
    a = copy.deepcopy(athlete)
    a["loading_stages"][spec.joints[0]] = 2
    _, n = check_block(copy.deepcopy(base), "block_02.json", "T", sib, spec, a)
    report("athlete record changed since the plan (a NOTE)", n, "(R68)", n)
    _, f = across_counts([("T", base["current_state"]["current_routines"]),
                          ("U", [{"path": "U/routine_t_A", "regions": ["upper"], "sessions_week": 2}])])
    report("two tracks at 2 + 2 upper sessions (--across)", f, "(R20)", f)
    print(f"RESULT: {caught}/{total} planted faults caught; clean fixture {'passes' if clean else 'FAILS'}")
    return 0 if clean and caught == total else 1


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, ValueError) as e:
        return None, str(e)


def show(label, fails, notes):
    print(f"{label}: " + (f"{len(fails)} FAIL" if fails else "clean" + (f" ({len(notes)} NOTE)" if notes else "")))
    for x in notes:
        print(f"  NOTE {x}")
    for x in fails:
        print(f"  FAIL {x}")


def main(argv):
    gym = pathlib.Path(__file__).resolve().parents[2]
    args = argv[1:]
    if args == ["--selftest"]:
        return selftest(gym)
    spec = Spec(gym)
    st = gym / "gymstate"
    ath_path = st / "athlete.json"
    athlete, err = load(ath_path) if ath_path.exists() else (None, "no gymstate/athlete.json (Stage 2 R67)")
    if args and args[0] == "--across":
        tracks, out = args[1:], []
        if len(tracks) < 2:
            print("FAIL --across needs two or more tracks")
            return 1
        for t in tracks:
            files = sorted((st / t).glob("block_*.json"))
            if not files:
                print(f"FAIL {t}: no gymstate/{t}/block_NN.json")
                return 1
            state, e = load(files[-1])
            if e:
                print(f"FAIL {files[-1].name}: {e}")
                return 1
            out.append((t, (state.get("current_state") or {}).get("current_routines")))
            print(f"{t}: {files[-1].name}, status {state.get('status')}")
        lines_, fails = across_counts(out)
        for x in lines_:
            print(f"  {x}")
        print("  NOTE the cross-routine guard (Stage 0 R20) and the sport notes (Stage 0 R21) are judged from the routine files")
        for x in fails:
            print(f"  FAIL {x}")
        print(f"RESULT: {len(fails)} FAIL" if fails else "RESULT: clean")
        return 1 if fails else 0
    blocks = sorted(st.glob("*/block_*.json"))
    print(f"State files: athlete.json and {len(blocks)} block files in {len({p.parent.name for p in blocks})} tracks"
          f" · Stage 0 §4.1 block fields: {', '.join(spec.block_fields)}; athlete fields: {', '.join(ATHLETE_FIELDS)}"
          f" · goals: {', '.join(spec.goals)} · sports: {', '.join(spec.sports)} · {len(spec.joints)} joints"
          f" · {len(spec.muscles)} muscles · {len(spec.register)} register entries · {len(spec.plan_dir)} files in gymplan/")
    total_f = total_n = 0
    if args:
        path = pathlib.Path(args[0])
        targets = [] if path.name == "athlete.json" else [path]
        check_ath = path.name == "athlete.json"
    else:
        targets, check_ath = blocks, True
        for p in sorted(st.glob("block_*.json")):
            show(p.name, [f"gymstate/{p.name}: a block file of the single chain; block files sit in gymstate/<track>/ (Stage 2 §3.4)"], [])
            total_f += 1
    if check_ath:
        f, n = ([err], []) if err else check_athlete(athlete, spec)
        show("athlete.json", f, n)
        total_f, total_n = total_f + len(f), total_n + len(n)
    elif err:
        show("athlete.json", [err], [])
        total_f += 1
    for p in targets:
        state, e = load(p)
        if e:
            show(p.name, [e], [])
            total_f += 1
            continue
        sib = {q.name for q in p.parent.glob("block_*.json")}
        f, n = check_block(state, p.name, p.parent.name, sib, spec, athlete if isinstance(athlete, dict) else None)
        show(f"{p.parent.name}/{p.name} ({state.get('status') if isinstance(state, dict) else '?'})", f, n)
        total_f, total_n = total_f + len(f), total_n + len(n)
    print(f"RESULT: {total_f} FAIL" if total_f else "RESULT: clean" + (f" ({total_n} NOTE)" if total_n else ""))
    return 1 if total_f else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
