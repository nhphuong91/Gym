# Stage 1 — Programming

**Normative · draft.** Binding on Stage 2 once frozen. Governed by `Stage0_PolicyDefinition.md` (draft, under Harry's review): cited by section and R-number, never restated.
Rationale, evidence, deferred material and the walkthrough → `Stage1_SupplementInfo.md`. `[HYP]` marks hypertrophy-specific content; everything else is goal-agnostic.

**Purpose.** Turn Current state (Stage 0 §4.1) and the current routines into a Plan (§3.1): for each routine, its exercises with sets × reps + RIR, rest, load band and pairing, its alternatives, its set count per muscle, its exercise time and its sport note, plus the checks it passed. Stage 1 does not draw routine files (Stage 2), choose days (Harry, Stage 0 §0.1) or dose nutrition (Stage 0 §0.1).

---

## 0. Decisions

### 0.1 Scope

| Item | Value |
|---|---|
| Input | **Current state, from the block's state file, and the current routines** (Stage 0 §4.1 · Stage 2 R67). Every field the state file does not hold is asked before planning, and every current routine is read before a new one is built or an old one edited (S1.1). |
| Output | **A Plan per request** (§3.1): one or more routines, each a session template with its regions and sessions per week. Harry places them in his week (Stage 0 §0.1). |
| Goals | **Every goal row of Stage 0 §2.2 is planned through the same steps**; `[HYP]` parts apply to hypertrophy only. |
| Conditioning | **Conditioning routines are checked against the hard gates (Stage 0 §0.2) and dosed only when Harry asks for a conditioning plan**: he builds and applies those sessions himself (Stage 0 D-53). |
| Maintenance block | **A maintenance block programs every muscle group by R47** (D-04). |
| Exercise catalogue | **One catalogue of exercise facts (§3.2), built from the corpus as seed data — JSON plus a `.md` mirror — supplies every plan** (D-03). Built 2026-10-02: `ExerciseCatalogue.json`, mirrored in `ExerciseCatalogue.md`. |

### 0.2 Planning

| Item | Value |
|---|---|
| Planning order | **Targets → candidates → compounds → harvest → direct sets → split → prescription → pairing → alternatives → progression → checks.** Stage 0's order (goal → muscles → volume → exercises, Stage 0 §0.3 · Stage 0 D-35) runs with compounds chosen before direct sets, because harvest is traced to planned exercises (R35). |
| Zones | **Zone labels apply to every goal; zone coverage binds hypertrophy only** (R26–R29). |
| Volume | **`[HYP]` A hypertrophy block counts weekly fractional sets per priority target, a maintenance block counts them per muscle group, and every other goal takes its row's Sets per exercise** (R33 · R47 · R34). |
| Routines, not weeks | **A plan builds routines; it states each routine's regions and sessions per week and never a day** (R45 · Stage 0 §0.1). |

### 0.3 Accepted limits

| # | Limit |
|---|---|
| a | Zone labels, prime movers and synergists come from exercise mechanics and published EMG or imaging, not from measurements on Harry. Accepted because nothing else is available outside a lab. |
| b | An indirect set counts 0.5 although it is likely worth about a third of a direct set for hypertrophy; the +2 buffer (R36) covers the overcount until harvest passes about half of a target. Accepted because 0.5 fits the dose–response data best and keeps counting simple (Supplement §5.4). |
| c | Exercise time is an upper-bound estimate (R40); set-up and changeovers beyond the prescribed rest are not counted. Accepted because the ceiling is what matters (Stage 0 R19). |
| d | Every L is truncated (Stage 0 R1) and strength stays specific to the trained range. Accepted because joint safety ranks first (Stage 0 §0.2). |
| e | The goal-fit tests for strength, power, muscular endurance and general fitness rest on general-population evidence; none was tested in hypermobile people (Supplement §5.4). |
| f | The maintenance floor of 4 fractional sets per muscle group a week comes from muscle-gain data in energy balance and short deficit trials; no trial tested it over a long or deep deficit. Accepted because keeping the load, which R47 does, matters most for retention (Supplement §5.4 · D-04). |

---

## 1. Steps

| Step | Input | Action items | Output |
|---|---|---|---|
| S1.1 Intake | Request · the block's state file (Stage 0 §4.1 · Stage 2 R67) · current routines | Read Current state from the state file and ask every field it does not hold; check Stage 0 §4.1 invariants; read every current routine; classify the request — new block, new routine or edit | Validated Current state · routine inventory · request type |
| S1.2 Frame | S1.1 | Block type and goal row per region (Stage 0 §0.3); the ramp bands for every block week, from the layoff (Stage 0 R22); RIR for weeks 1–4 and from week 5 (Stage 0 R17 · R18), since Harry counts the block weeks (Stage 0 §2.4); suspended regions (Stage 0 R24); training sessions per region, ≤3 (Stage 0 R20) | Block frame |
| S1.3 Targets | Block frame | `[HYP]` weekly target per priority target (R33); maintenance: floor and default per muscle group (R47); other goals: no weekly target, Sets per exercise from the row (R34) | Target per muscle or group |
| S1.4 Candidates | Targets · Stage 0 §1.3 · loading stages | Per target, list exercises that pass the hard gates (Stage 0 §0.2); label zones (R26) and check zone availability (R27); score the goal-fit test (R30); give each a sport verdict (R31); rank by Stage 0's selection criteria, focus-block preference included (R32) | Ranked candidates per muscle |
| S1.5 Compounds and harvest | Candidates | Choose compounds first; trace every indirect set to its exercise (R35) | Harvest per muscle |
| S1.6 Direct sets | Targets · harvest | `[HYP]` direct = target − harvest, + buffer (R36); fill direct sets with exercises of the row's Sets that complete zone coverage, rounding up where a split needs it (R28 · R29 · R48) | Target, harvest and direct per muscle |
| S1.7 Split | Direct sets · block frame · current routines | Spread sets over routines by R37 and Stage 0's per-muscle session ceiling (R19); keep routines that share no region apart (Stage 0 R20); count each region's sessions across all current routines | Routine skeletons |
| S1.8 Prescription | Skeletons · goal rows | Sets × reps + RIR and rest from the row (Stage 0 §2.2 · R16–R18); load band (Stage 0 R22); tempo (Stage 0 R25) | Exercise rows |
| S1.9 Pairing and time | Exercise rows | Pair or run straight (R38 · R39); estimate exercise time (R40); over the ceiling → back to S1.7 | Paired rows · exercise time |
| S1.10 Alternatives and sport note | Paired rows · sport profiles | Two alternatives per station exercise (R41); the routine's sport note (Stage 0 R21) | Alternatives table · sport note |
| S1.11 Progression | Block frame · rows | Next step per exercise (R42); flare and deload handling (R43 · R44) | Progression lines |
| S1.12 Assemble and check | S1.1–S1.11 | Fill the Plan record (R45 · §3.1); run every check (R46), naming each shortfall and warning | Plan with check results |

---

## 2. Rules

| ID | Rule |
|---|---|
| R26 — Zone label | **Every exercise carries one zone label for its target muscle — L, M or S — by where in that muscle's range its resistance peaks: L at long length (early range), M at mid-range, S at short length (late range).** Every L is truncated by Stage 0 R1, never an end-range stretch. Reference labels: preacher curl L, overhead cable extension L, RDL L; spider curl M, cable pushdown M; prone Y raise S, band crossover at full adduction S. |
| R27 — Zone availability | **A muscle has an S zone only when its shortened position passes Stage 0 R2 and R5; otherwise its coverage is L + M, stated once as a permanent shortfall.** Where shortening is partly blocked, S runs to the rule's cap. Known shortfall: the triceps has no S, since its shortened position is terminal elbow extension (Stage 0 R2). |
| R28 — Zone coverage `[HYP]` | **In a hypertrophy block, every priority target gets at least one L and one M or S exercise a week; a muscle with one slot gets L.** When the hard gates remove every L option, the plan names the gap and uses the best M. |
| R29 — S selection | **An S exercise enters as the M-or-S slot of R28, or where it carries less residual joint risk than every passing L (Stage 0 §0.2, criterion 1); it never displaces a passing L of equal risk, and bands come first for S.** Band tension peaks at short length, and bands are never occupied. |
| R30 — Goal-fit test | **Every candidate is scored on the goal-fit test of its region's goal row (§2.1): it passes every "must" criterion, and the tie-breakers order those that pass.** The test is selection criterion 3 (Stage 0 §0.2). |
| R31 — Sport verdict | **For each in-season sport, every exercise gets a verdict from four questions — does it conflict with a demand in the sport's profile (Stage 0 §1.2); what joint risk remains after the hard gates; does it train a carryover quality; is there a safer variant with equal benefit — green (no issue), yellow (issue plus its named mitigation) or red (issue plus its blocking rule).** The joint-risk question runs on every exercise, in season or not. The verdict feeds selection criterion 5. |
| R32 — Focus selection | **In a focus block, an exercise enters only when its prime mover is a priority target, and among those, the one loading other muscles least ranks first unless that extra load is harvest planned for another priority target** (Stage 0 §0.3). Muscles outside the block get no direct sets. |
| R33 — Weekly target `[HYP]` | **Every priority target in a hypertrophy block has a weekly target of 10–20 fractional sets — calves 12–18 — starting at the bottom of the range.** The target rises within the range only through R42 (c). |
| R34 — Volume outside hypertrophy | **Strength, power, muscular-endurance and general-fitness muscles have no weekly target: each exercise takes its row's Sets (Stage 0 §2.2), starting at the row's bottom.** In a general-fitness block, every muscle group of a trained region appears in at least two training sessions a week. |
| R35 — Harvest traced | **A muscle's harvest counts only indirect sets from an exercise of its own region in the same plan that trains it as a meaningful synergist, each traced to that exercise; muscles whose action no planned compound performs — shoulder abduction, most rotation — harvest nothing.** Indirect sets from the other region's exercises count toward no target (D-02); Stage 0 R20's cross-routine guard still sees them. |
| R36 — Direct sets `[HYP]` | **Direct sets = weekly target − harvest, plus 2 where harvest supplies at least half of the target; the plan states target, harvest and direct for every priority target.** |
| R37 — Frequency | **In hypertrophy, muscular-endurance and general-fitness blocks, a muscle with fewer than 9 fractional sets a week trains in one session and a muscle with 9 or more in at least two; strength and power targets spread as Stage 0 §0.3 sets.** A week in which Harry swaps a session for cardio falls short of the plan, and he accepts that (Stage 0 §0.4 (f) · D-05). |
| R38 — Superset pairing | **A superset pairs two exercises that share no prime mover or key synergist: true antagonists (push ↔ pull, horizontal press ↔ row, vertical press ↔ pull, hinge ↔ knee extension), or a cross-region or cross-joint pair with no muscle overlap; two exercises for the same muscle are not a superset.** Neither partner pre-fatigues the other's prime mover or key synergist; a heavy compound pairs only with a partner that leaves grip, bracing and stabilizers fresh; an isometric hold is a neutral partner; one muscle across two joint actions (knee flexion ↔ hip extension) is a weaker but valid pair. |
| R39 — Pairing bookkeeping | **Pairing never changes set counts — each partner keeps its derived sets, and extra sets run straight — and the plan states which partner goes first.** |
| R40 — Exercise time | **A routine's exercise time is the sum over its working sets of reps × 4 s (lowering 3 s, lifting 1 s; holds at their hold time), plus the rest prescribed after each set or pair, at the top of every range; the routine's last rest is not counted.** The result is checked against Stage 0 R19's ceiling. |
| R41 — Alternatives | **Every exercise that needs a station (Stage 0 §1.3) gets two alternatives, closest stimulus first, each avoiding every station the primary uses; exercises with no station get none.** Alternatives keep the primary's intent — zone, antagonist role, joint angle — and pass the hard gates; an unsupported variant carries its Stage 0 R5 warning. Of two equal alternatives, the band variant ranks first. When fewer than two pass, the plan names the gap. |
| R42 — Progression | **Each exercise progresses one variable a week, in this order: (a) +1 rep per set until every set reaches the top of the rep range at the target RIR in two consecutive sessions; (b) then load up by Harry's smallest step, reps back to the bottom (Stage 0 D-10); (c) +1 set every 2 weeks while (a) and (b) stay inside the step gate — per muscle up to the weekly target (hypertrophy), per exercise within the row's Sets (other goals).** No muscle gets more load and more sets in the same week. Progression starts after the restart ramp (Stage 0 R22). |
| R43 — Flare response | **A failed step gate (a flare, Stage 0 §2.6) repeats the last week's dose for the exercises loading that joint; two flares within 4 weeks take one step back, held for 2 weeks: one set less per affected muscle in hypertrophy, one set less per affected exercise within its row's Sets in every other goal, or 5% less load** (D-07). |
| R44 — Deload | **A deload runs only on its trigger and is one week at half the sets, same loads. The trigger, for every goal: at the same load, reps at the target RIR fall by 2 or more — or, in sets of 1–3 reps, the RIR felt at the same load and reps falls by 2 or more — for two sessions** (D-06). A flare never triggers a deload: R43 answers it (D-01). |
| R45 — Plan contents | **Every plan carries the fields of §3.1, states each routine's regions, sessions per week and sport note, and assigns no day.** |
| R46 — Plan checks | **Before delivery, the plan lists the result of every check below, and names each shortfall and warning.** (1) Every exercise is on Stage 0 §1.3 and passes the hard gates, warnings with their mitigation. (2) Every programmed muscle belongs to the block (R32). (3) Sets, reps, RIR and rest match the goal row (Stage 0 §2.2 · R16–R18 · R48). (4) Pairs pass R38 and R39. (5) Target, harvest and direct follow R35 and R36; a maintenance block's groups follow R47. (6) Each routine stays within Stage 0 R19 by R40. (7) Zone coverage follows R27 and R28. (8) Each region's sessions and the cross-routine guard pass Stage 0 R20. (9) Every routine carries its sport note (Stage 0 R21). (10) Alternatives follow R41. |
| R47 — Maintenance block | **A maintenance block gives every muscle group (Stage 0 §2.1) at least 4 fractional sets a week — 6–10 by default — spread over at least two training sessions; both regions run the hypertrophy row (Stage 0 R17–R18) at the loads the last block reached, with the fewest exercises per group, compounds first** (D-04). A group's fractional sets count every set whose prime mover is in the group, plus harvest (R35); R33's targets and R36's buffer do not apply. |
| R48 — Sets per exercise | **Every exercise takes at least the bottom of its goal row's Sets, and at most the top, in each session it appears in (Stage 0 §2.2). `[HYP]` Where a target's direct sets (R36) cannot be split into such exercises while filling its zone slots (R28), the direct count rounds up to the smallest split that does, and the plan states the sets above the target.** |

### 2.1 Goal-fit tests

R30's tests. "Must" criteria are pass/fail; tie-breakers order the passing candidates. Evidence: Supplement §5.4.

| Goal | Must pass | Tie-breakers |
|---|---|---|
| Hypertrophy `[HYP]` | H1 the target muscle is the prime mover, or the exercise is a compound planned as its harvest source (R35) · H2 sets reach the row's RIR inside its rep range with the target muscle limiting the set, not grip, balance or breathing · H3 its zone fills a slot R28 needs | L before M before S for growth · resistance profile over limb angle: a shoulder-extended curl adds risk, not growth · triceps long head: an overhead extension for the L slot |
| Strength | S1 specific: movement pattern, equipment type and joint-angle band match the strength being targeted · S2 heavy-loadable: 3–5 reps at 1–3 RIR with the load as the limiter and a mechanical stop (Smith safeties, rack pins, machine stops) · S3 fine increments: the smallest load step is ≤10% of the working load | Multi-joint before single-joint |
| Power | P1 maximal-intent concentric that stops short of terminal extension with no impact, bounce or catch (Stage 0 R2 · R10 · R13) · P2 specific: force direction and joint sequence resemble the target action · P3 speed holds across the set's 1–3 reps | Multi-joint, large muscle mass. Until loading stage 4, heavy lifts moved with maximal concentric intent are the power tool |
| Muscular endurance | E1 light-loadable: ≥12 reps at 1–3 RIR with fine load steps · E2 fatigue-robust: a guided path (machine, cable or band), a mechanical stop and low balance demand · E3 a changeover that fits the row's rest | The set ends because the target muscle tires, not grip or breathing |
| General fitness | G1 simple: low skill, repeatable without coaching · G2 it trains a muscle group the week still needs for R34's two-session coverage | Multi-joint before single-joint · closed-chain work with a balance or proprioceptive element |

### 2.2 Rule examples

Each rule passes when the implementation produces the *Pass* behaviour and fails when it produces the *Fail* behaviour. Fixture as in Stage 0 §3 Rule examples: focus block · upper and lower Hypertrophy · priority targets biceps, quads · a new block after a 2-month layoff · every joint at loading stage 1 · badminton in season · current routines: none yet. Values are illustrative.

| Rule | Pass | Fail |
|---|---|---|
| R26 — preacher curl | Labelled L: resistance peaks early, with the forearm near horizontal | Labelled S ("shortened bias") |
| R27 — triceps | Coverage listed as L + M, "no S — permanent shortfall (Stage 0 R2)" | A DB kickback to full lockout listed as its S |
| R28 — quads at knee stage 1 | No L passes (depth capped above parallel): the gap is named and the goblet squat above parallel fills the slot as M | A squat below parallel as the L; or the missing L left unnamed |
| R29 — biceps | Preacher curl (L) kept; band curl with elbows ahead of the torso added as S | The band curl replaces the preacher curl although both pass and carry equal risk |
| R30 — strength block, lower | Smith squat above parallel: 3–5 reps at 1–3 RIR, safeties set, small plates | Band squat as the strength exercise (cannot reach ≤6 RM with fine steps) |
| R31 — badminton in season | Preacher curl: green (supported shoulder, no demand conflict) | Incline DB curl, arms hanging free, marked green without the risk question (Stage 0 R5) |
| R32 — biceps and quads focus | Preacher curl, spider curl, Smith squat, goblet squat; no direct chest or back sets | A cable row added "for balance" (prime mover: lats) |
| R33 — week 1 | Biceps target 10 | Biceps target 16 in week 1; or 8 |
| R34 — strength block | Smith squat at 2 sets per session (the row's bottom); no weekly quads target | A 12-set weekly quads target in the strength block |
| R35 — biceps | Harvest 3.0 from 6 cable-row sets, traced to the row | Harvest 2.0 "from general pulling" with no row in the plan; or lateral-delt harvest from presses; or erector harvest from lower-body RDLs counted toward an upper-body target |
| R36 — biceps | Target 10, harvest 5.0 → direct 5 + 2 = 7 | Direct 5: the buffer missing |
| R37 — quads, target 10 | Spread over two sessions, 5 + 5 | All 10 in one session |
| R38 — pairs | Preacher curl ↔ cable pushdown; preacher curl ↔ Smith squat (cross-region, no overlap) | Smith incline press ↔ cable pushdown (the pushdown pre-fatigues the press's triceps); lat pulldown ↔ DB fly (same joint, not antagonists) |
| R39 — curl 4 sets, pushdown 3 | Three rounds paired, the fourth curl set straight; "isolation first" stated | The curl cut to 3 sets to match the pushdown |
| R40 — routine A | 4 exercises, 12 sets — 9 at 10–12 reps, 3 wall-sit holds of 45 s — 90 s after each pair: ≈17 min | Time estimated at 1 s per rep; or not stated |
| R41 — Smith flat bench press | Alternatives avoid the Smith and the bench: DB floor press, push-up | DB flat bench press (uses the bench, the primary's second station) |
| R42 — preacher curl, week 6 | Every set at 12 for two sessions → next week up one step, back to 10 reps | Load and a set added to biceps in the same week |
| R43 — knee flares | One flare: next week repeats this week's quad dose. Two in 4 weeks, strength block: Smith squat 3 → 2 sets a session for 2 weeks, or 5% less load | Quad load raised the week after a flare; or quads cut by "one set per muscle" in a strength block with no weekly count |
| R44 — deload triggers | Reps at the same load down 2 for two sessions; or, in a power block, the same 2 reps felt at 1 RIR instead of 3 for two sessions → one week at half the sets, same loads | A deload every 4 weeks without a trigger; or a deload week after a single flare; or a power block left without a trigger |
| R45 — routine A | Regions upper + lower, 2 sessions a week, exercise rows, alternatives, set counts, exercise time, "Day after: no badminton", checks | "Monday: routine A"; or the sport note missing |
| R46 — delivery | A check list with ✓ or ✗ per item, the quads L shortfall named | "All checks pass" with no list |
| R47 — maintenance block | Back 6 fractional sets a week from rows and pulldowns over two sessions, at the last block's loads; calves 4 from standing and seated raises over two sessions | Calves 2 sets a week; or all of a group's sets in one session; or loads cut 20% "for the deficit" |
| R48 — biceps target 10, harvest 0, routine A twice a week | Preacher curl 3 + spider curl 3 in each session: 12 a week, "2 above the target (R48)" stated | Spider curl at 2 sets in a session; or the 2 extra sets left unstated |

---

## 3. Schemas

### 3.1 Plan — one per request

| Field | Definition |
|---|---|
| `header` | Block type, goal row per region, priority targets, the ramp bands for every block week (Stage 0 R22), RIR for weeks 1–4 and from week 5 (Stage 0 R17 · R18), plan version |
| `routines` | Per routine: name, regions trained (Stage 0 §2.7), sessions per week, exercise rows, exercise time (R40), sport note (Stage 0 R21) |
| `exercise_row` | Exercise · equipment and stations · zone (R26) · sets × reps + RIR · rest · load band · pairing or "straight", with the order (R38 · R39) · notes and warnings |
| `alternatives` | Per station exercise: two alternatives, or the named gap (R41) |
| `set_count` | `[HYP]` per priority target: target, harvest with its sources, direct (R33–R36) and any sets above the target (R48); maintenance: fractional sets and sessions per muscle group (R47); other goals: Sets per exercise (R34) |
| `zone_coverage` | `[HYP]` per priority target: its L and M/S exercises, shortfalls named (R27 · R28) |
| `progression` | Per exercise: the next step (R42) |
| `suspensions` | The Stage 0 R24 statement, when a region is excluded |
| `checks` | R46's list with results |

### 3.2 Exercise facts — one per exercise a plan uses

| Field | Definition |
|---|---|
| `name` | As Harry's routine files name it |
| `stations` | Stations it occupies (Stage 0 §1.3), or none |
| `prime_mover` | The one muscle its working sets count as direct for (Stage 0 §2.3) |
| `indirect` | Muscles collecting 0.5 per set (Stage 0 §2.3 · R35) |
| `zone` | L, M or S for the prime mover (R26) |
| `joints` | Joints loaded and the loading stage each needs: partial or full range, unilateral, impact (Stage 0 §2.5) |
| `sport_notes` | Carryover and conflicts per sport profile (R31) |

Invariant: every exercise in a plan takes its facts from the exercise catalogue (D-03). An exercise not yet in it is proposed to Harry with its facts and enters the catalogue only once he confirms (D-08). A locked exercise names the open exercises that replace it until its joints reach the loading stage it needs; it then returns to the candidates beside them (D-09).

---

## 4. Open items

None. Round 1 closed 2026-10-02 (Supplement §3, D-01…D-07); D-08 and D-09 recorded 2026-10-03; D-10 recorded 2026-10-06; D-11 recorded 2026-10-13; D-12 and D-13 recorded 2026-10-25.
