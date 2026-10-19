# Stage 1 — Supplement Info

**Non-normative.** Companion to `Stage1_Programming.md`: terminology, architecture history, decision log, rejected alternatives, corpus evidence, deferred material, walkthrough and references.
Where the two documents disagree, the normative document governs. Stage 0 terminology (`Stage0_SupplementInfo.md` §1) applies unchanged. `[W#]` → §8 References; "Stage 0 [W#]" → `Stage0_SupplementInfo.md` §7. Section numbers found only here (§5.1–§5.5, §6–§8) refer to this Supplement; every other § refers to `Stage1_Programming.md`, unless prefixed "Stage 0".

---

## 1. Terminology

Terms introduced by Stage 1.

| Term | Meaning in this project |
|---|---|
| Plan | The record a request produces (§3.1): routines, exercise rows, alternatives, set counts, exercise time, sport notes and checks |
| Routine | A session template for the regions it trains, with its sessions per week; Harry places it in his week (Stage 0 §0.1) |
| Zone · L · M · S | Where in a muscle's range an exercise's resistance peaks: long length, mid-range, short length (R26) |
| Zone coverage | A priority target's L plus M-or-S exercises in a week (R28) |
| Permanent shortfall | A zone a muscle can never have under Stage 0 R2 or R5, named once (R27) |
| Compound | A multi-joint exercise; in a plan, the only source of harvest (R35) |
| Harvest source | The planned exercise an indirect set is traced to (R35) |
| Buffer | The 2 extra direct sets added when harvest supplies at least half a target (R36) |
| Superset · pair · straight sets | Two exercises alternated set by set · its two partners · sets run alone (R38 · R39) |
| Antagonist · soft antagonist | Opposing actions, e.g. push ↔ pull · one muscle across two joint actions, e.g. knee flexion ↔ hip extension (R38) |
| Station exercise | An exercise that occupies a station (Stage 0 §1.3) and so needs alternatives (R41) |
| Sport verdict | Green, yellow or red per in-season sport (R31) |
| Flare response · step back · deload | Repeat the dose after a flare · one set less or 5% less load after two flares in 4 weeks · a week at half the sets on a trigger (R43 · R44) |
| Exercise facts | The per-exercise record a plan relies on (§3.2) |
| Exercise catalogue · open · locked · excluded | The seed-data file of exercise facts every plan takes (§0.1 · D-03): `ExerciseCatalogue.json`, mirrored in `ExerciseCatalogue.md` · a row's status at the screened loading stages: passes the hard gates now · needs a higher loading stage for some joint · fails a hard gate in every form |
| Ramp band | The restart-ramp weeks a block week falls in: ≈60%, ≈80% or 100% (Stage 0 R22) |
| Maintenance dose · group sets | A maintenance block's floor of 4 and default of 6–10 fractional sets a week per muscle group · every set whose prime mover is in the group, plus harvest (R47) |

---

## 2. Architecture history

Stage 1 opens from 19 deferrals of Stage 0 (`Stage0_SupplementInfo.md` §6) and from CLAUDE_old.md `<programming>`, `<dosing>`, `<output>` and `<verification>`.

| Deferral (source) | Stage 1 answer |
|---|---|
| Zones: labels, availability per muscle, triceps without S, bands first for S, `[HYP]` coverage, L gap → best M, S never displacing a passing L, lengthened work as the growth lever (CLAUDE_old.md `<programming>` Regional) | R26–R29 · §2.1 hypertrophy |
| Sport filter: four questions and a verdict; the risk question on every exercise | R31 |
| Supersets, rules 1–8 | R38 · R39 |
| Alternatives table, rules 1–9 | R41 |
| Planning order reconciled with Stage 0 D-35 | §0.2 · Steps |
| Goal-fit tests per goal (Stage 0 D-36) | R30 · §2.1 |
| Focus-block rules (Stage 0 D-22) | R32 |
| Maintenance block (Stage 0 D-23) | R47 (D-04) |
| Volume and capacity: weekly targets, traced harvest, buffer, frequency, which goals carry a weekly target (Stage 0 D-29) | R33–R37 |
| Exercise-time estimate (Stage 0 D-49) | R40 |
| Split: sessions per region; order and days are Harry's (Stage 0 D-47 · D-48) | S1.7 · R37 · R45 |
| Conditioning work (Stage 0 D-44 · D-52) | §0.1 Conditioning: gates only, dosed on request (Stage 0 D-53) |
| Robustness to a swapped session (Stage 0 D-53, proposal) | Not adopted: Harry accepts the swapped week's shortfall (D-05) |
| Progression, step-gate response, deload (`<dosing>`; Stage 0 D-10) | R42–R44 · D-01 |
| Plan output format and format examples (`<output>`; reference.md §R3) | R45 · §3.1 |
| Plan checks (`<verification>`) | R46 |
| Evidence and reasoning on regional growth, set units, volume, frequency, harvest, progression, load steps, deloads (reference.md §R2, §R5, §R6) | §5.4 · §5.5 |
| P1 power deload trigger · P2 step-back unit · P3 cross-region harvest · P4 long limbs · P6 bench and two-station alternatives | D-06 (R44) · D-07 (R43) · D-02 (R35) · Backlog (§6) · R41 |
| Seed data: an exercise catalogue (Stage 0 D-18) | §0.1 · §3.2 · D-03 · `ExerciseCatalogue.json`, built 2026-10-02 |

**Changed on the way from CLAUDE_old.md** ✏️

| CLAUDE_old.md | Stage 1 | Why |
|---|---|---|
| S "outranks L for a gated or flare-prone joint" | R29: S enters as the M-or-S slot, or where its residual joint risk is lower than every passing L | Every joint is staged (Stage 0 D-28), so "gated" no longer singles a joint out; Stage 0's criterion 1 carries the intent |
| Capacity check Σ direct ≤ 28 × sessions/week | Exercise time per routine (R40) against Stage 0 R19 | Stage 0 D-49 dropped the 28-set ceiling |
| Load +2.5–5% | Harry's smallest step (R42 (b)) | Stage 0 D-10 |
| Plan header with the day | Regions and sessions per week, no day (R45) | Stage 0 D-48 |
| Smith, cable and hip machine as the stations for alternatives | The bench too; a two-station exercise avoids both (R41) | Stage 0 D-09; reference.md P6 |
| Exactly two alternatives per primary | Two, or the gap named (R41) | Some primaries have one passing alternative (§7) |
| Schedule check: 48 h rule and sport-day rules | Region sessions, cross-routine guard, sport note (R46 (8)–(9)) | Stage 0 D-47 · D-50 · D-51 |
| Deload trigger "… or a gate fail" | Performance trigger only (R44) | The same flare was also "repeat last week's dose"; Harry chose the dose repeat (D-01) |
| Isolation to 0–1 RIR after 4 flare-free weeks | Gone | Stage 0 D-33 · D-45 |
| Deload trigger "performance down ≥2 reps at the same load" | The same, plus a felt-RIR form for 1–3-rep sets (R44) | Power sets could never show a 2-rep drop (D-06) |
| Step back "−1 set/muscle or −5% load" | Per affected exercise outside hypertrophy (R43) | Only hypertrophy counts weekly sets per muscle (D-07) |
| Maintenance targets for all muscles, "defined later" | R47 | D-04 |

---

## 3. Decision log — closed open items

Log IDs are local to Stage 1; each row names the OI it closes, and OI numbers restart after each cleared round. An amendment to a frozen stage is also logged in that stage's Supplement. The freeze itself is a row.

| # | Question | Decision | Lands in |
|---|---|---|---|
| D-01 | Flare vs deload (O3, round 1) | A: a flare repeats the last week's dose for the exercises loading that joint, and two flares within 4 weeks step back (R43); deloads follow performance only (R44). A flare is a joint signal; a deload answers whole-body fatigue | R43 · R44 |
| D-02 | Indirect sets across regions (O6, round 1; reference.md P3) | Harry: ignore them. Indirect sets a muscle collects from the other region's exercises count toward no target (C). Stage 0 R20's cross-routine guard, a recovery check, still sees them | R35 |
| D-03 | Exercise catalogue (O7, round 1; Stage 0 D-18) | A: after round 1, build one catalogue of exercise facts (§3.2) from the corpus as seed data — JSON with a schema id and per-row provenance, plus a `.md` mirror; plans take their facts from it | §0.1 · §3.2 · §6 |
| D-04 | Maintenance block (O1, round 1; Stage 0 D-23) | A: every muscle group gets at least 4 fractional sets a week, 6–10 by default, over at least two sessions; both regions run the hypertrophy row at the loads the last block reached; fewest exercises per group, compounds first. Why: no trial pins a minimum in a deficit; the lowest doses that held muscle kept the load, and 12 sets a week held as well as 30 (§5.4) | R47 · §0.1 · §0.3 (f) |
| D-05 | Spreading targets (O2, round 1) | Harry: in a week he swaps a gym session for cardio (Stage 0 D-53), he accepts not reaching the target. R37 stays as written (A) | R37 |
| D-06 | Power deload trigger (O4, round 1; reference.md P1) | A: one trigger for every goal — at the same load, reps at the target RIR fall by 2 or more, or, in sets of 1–3 reps, the RIR felt at the same load and reps falls by 2 or more, for two sessions | R44 |
| D-07 | Step-back unit outside hypertrophy (O5, round 1; reference.md P2) | A: one set less per affected exercise, within its row's Sets, or 5% less load | R43 |
| D-08 | Exercises missing from the catalogue (catalogue Q6, chat 2026-10-03) | Harry: check with him before adding. A plan that needs an exercise not in the catalogue proposes it with its facts (§3.2); it enters the catalogue only once he confirms | §3.2 |
| D-09 | Replacements for exercises locked by Stage 0 D-54 (catalogue Q9 · Q10, chat 2026-10-03) | Harry: the replacements stand in for the locked exercises while their joints sit below the stage those need (stages 1–2 for single-limb work); once the joints reach it, the originals return to the candidates and the replacements stay candidates too. He confirmed all eight proposed, with Claude's three fixes (two-band adduction, a band per foot for the popliteus, the supine leg lift); N4 takes the band form, Claude's recommendation, under his "proceed" | §3.2 · `ExerciseCatalogue.json` C130–C137 |
| D-10 | Rule examples and the walkthrough after catalogue A9 (T11, chat 2026-10-06) | Harry: OK. With every joint at stage 1, a bar on his back takes his shoulders past 45° of external rotation (catalogue A9), so R28's example fills the quads' M slot with the goblet squat, and §7 re-runs: the goblet squat stands in for the requested Smith squat (D-09), the wall sit takes the second quads slot (Stage 0 D-58), and the preacher curl has no L alternative without the bench until shoulder stage 2 (Stage 0 D-63). R40's example follows the re-run | R28 · R40 examples · §7 |
| D-11 | Sets per exercise (O9 · O10, chat 2026-10-13; raised while planning the upper-body block) | A + H: every exercise takes at least the bottom of its goal row's Sets, and at most the top, in each session it appears in (Stage 0 §2.2); in hypertrophy a target's direct sets round up to the smallest split into such exercises that fills its zone slots, and the plan states the sets above the target. H, Harry's floor of 8 reps a set: a timed hold lasts at least its band's bottom reps × 4 s (Stage 0 D-87). Why: Stage 0 §2.2 and Stage 0 §2.3 already count Sets per exercise per session, but R40's example and §7 ran two exercises at 2 sets; Harry set at least 3 sets per exercise per session (O10 A). §7 re-runs: biceps and quads 12 a week | R48 · R40 and R46 (3) · S1.6 · §3.1 `set_count` · §7 |

**Dissolved without a decision**

None.

---

## 4. Rejected alternatives

| Alternative | Rejected because |
|---|---|
| A midpoint exercise-time estimate (middle of rep and rest ranges) | Stage 0 R19 is a ceiling; only an upper bound guarantees it (R40) |
| A 2 s lowering in the time estimate | Stage 0 R25 allows up to 3 s; the estimate takes the slower end |
| A planned deload every 4–6 weeks, common practice [W52] | CLAUDE_old.md deloads on triggers only, and a week off mid-programme cost strength without adding size [W51] |
| A flare triggering a deload week, alone or before the repeated dose (O3 B, C, round 1) | Harry: a flare repeats the dose; deloads follow performance only (D-01) |
| Counting the other region's indirect sets always, or when both regions share a goal (O6 A, B, round 1) | Harry: ignore them (D-02) |
| No catalogue: each plan states its own exercise facts (O7 B, round 1) | One source keeps harvest, zones and gate needs consistent across plans (D-03) |
| A maintenance floor only — 4 sets per group a week — or deferring the maintenance block (O1 B, C, round 1) | The default of 6–10 leaves margin for a longer or deeper deficit (D-04) |
| Spreading every priority target over two or more sessions (O2 B, round 1) | Harry accepts a swapped week's shortfall (D-05) |
| No performance trigger for power (O4 B, round 1) | With deloads performance-only (D-01), power would never deload (D-06) |
| Load-only step back outside hypertrophy (O5 B, round 1) | A set less per affected exercise keeps the load the goal needs (D-07) |

---

## 5. Corpus evidence

### 5.1 Corpus status

| File | Finding | Consequence |
|---|---|---|
| `routine_upperbody` v6 · `routine_lowerbody` v4 | Re-read on Harry's computer, 2026-10-02, as walkthrough samples (text extraction as in reference.md §R4) | Quirks in §5.2 and §7 |
| The other 12 routine files | Re-read on Harry's computer, 2026-10-02, to build the exercise catalogue; the 2 foam-rolling files were read and left out (tissue release, not exercise: Stage 0 §2.7) | §5.2 · `ExerciseCatalogue.md` |

### 5.2 Observations

| Observation | Informs |
|---|---|
| `routine_upperbody` v6 labels the preacher curl "shortened bias", the spider curl "lengthened bias" and the cable pushdown "shortened bias"; by resistance profile they are L, M and M | R26 |
| `routine_upperbody` v6 pairs the lat pulldown with a DB chest fly: the same joint, and not a listed antagonist pair | R38 |
| `routine_upperbody` v6 lists a DB flat bench press as the Smith bench press's alternative (it uses the bench, the primary's second station), plus a cable crossover and a cable lateral raise, which the cable machine cannot execute (Stage 0 D-25) | R41 · Stage 0 R15 |
| `routine_upperbody` v6 gives the medial delt 3 and the rotator cuff 2 direct sets; no compound performs shoulder abduction or rotation, so neither can harvest | R35 |
| `routine_lowerbody` v4 counts glutes at "~5–6 sets" from 3 hip-thrust sets plus RDL synergy; traced, that is 3 + 1.5 = 4.5 fractional sets (M2) | R35 · R36 |
| `routine_lowerbody` v4 counts three wall-sit holds as quad sets; Stage 0 §2.2 then allowed timed isometrics only for forearm and abs isolation — every muscle since Stage 0 D-58 | §2.1 H2 · Stage 0 §2.2 |
| `routine_lowerbody` v4 runs the sit-to-stand to a "bench at 90° knee": parallel, beyond the knee's stage-1 range | Stage 0 R3 · R11 (S1.4) |
| `routine_lowerbody` v4 gives calves 6 sets; a hypertrophy block's calf target starts at 12 | R33 |
| Catalogue screen, revision 8 (2026-10-06, after Stage 0 D-54 · D-55, the stage-1 ranges Stage 0 D-63…D-69, Harry's bar-on-back reading and the vertical-pull grips, catalogue A9 · T12): the corpus holds 111 distinct exercises. 40 pass the hard gates as written, with cues. 31 pass once a cue, depth, anchor or variant changes (✏️ — squats and wall sits above parallel, R4's braced stop and a grip about 1.25× shoulder width for vertical pulls, bands anchored off the Smith, DB handles for push-ups, holds capped at ~70–80% of range, drills run with both limbs together, curls' bottom bend and overhead triceps work held inside the stage-1 ranges). 36 wait for a higher loading stage: single-limb work of any kind (Stage 0 D-54), impact and court work, and eight rows past the shoulder's stage-1 range (Stage 0 D-63) — three of them hold a bar on the back, which Harry's long humerus takes past 45° of external rotation (A9). 4 fail: cable exercises the machine cannot execute (Stage 0 R15) | S1.4 · R46 (1) · `ExerciseCatalogue.md` |
| The alternatives tables of the three upper focus files cite exercise numbers 2 above their cards: numbering from before v6 removed warm-up block A | Stage 2 (§6) |
| `routine_upperbody_focus_B` v6 lists hands-high incline push-ups as the Smith incline press's alternative; hands high matches a decline-press angle, so the incline angle calls for feet-high push-ups | R41 (joint angle) |

### 5.3 Measurements

| # | Measure | Method | Result |
|---|---|---|---|
| M1 | Exercise time of `routine_upperbody` v6 by R40 | Sets, reps and rests from the file text; top of ranges; 4 s per rep; rest after each pair; last rest dropped | ≈30.5 min upper bound vs "~28 min" stated |
| M2 | Glute fractional sets in `routine_lowerbody` v4 by R35 | 3 hip-thrust direct sets + 3 RDL sets × 0.5 | 4.5 vs "~5–6" stated |
| M3 | Station conflicts among the `routine_upperbody` v6 alternatives by R41 | Each alternative's stations against its primary's | 1 shared station (DB flat bench press); 2 alternatives not executable (cable crossover, cable lateral raise) |

Run 2026-10-02: text extracted on Harry's computer (`grep`, reference.md §R4); arithmetic re-run in Python.

### 5.4 Training evidence ✏️

| Finding | Source | Informs |
|---|---|---|
| Long vs short mean muscle length gave practically equivalent regional growth across 12 studies: proximal SMD 0.05, mid 0.07, distal 0.09, mostly inside the equivalence region | [W1] | R26 · R28 |
| Preacher and incline curls grew different regions (preacher distal, incline proximal); strength was specific to the curl trained | [W2] · [W3] | R26 · R28 |
| Shoulder angle alone, resistance profile matched, changed nothing: curls at shoulder flexion vs extension, and neutral vs peak extension | [W4] · [W5] | §2.1 hypertrophy tie-breaker |
| Cable lateral raises (peak at long length) and dumbbell lateral raises (peak at short length) grew the lateral delt alike in trained lifters | [W6] | R26 · R29 |
| Overhead vs neutral triceps extension: long head +28.5% vs +19.6%, about 1.5-fold | [W7] | §2.1 hypertrophy (triceps long head) |
| Varying exercises grew all four quadriceps heads where one exercise missed some; total growth was similar; excessive random variation may compromise gains, though one trial found random variation gave similar gains | [W8] · [W9] · [W10] | R28 · S1.6 |
| Short partials grew least: knee-extension short partials ≈ no training at 60–70% sites; calves 3.4% (short) vs 15.2% (long partials); long beat short partials in a meta-analysis (ES 0.28) | [W11] · [W12] · [W13] · [W14] | R29: S is chosen for joint safety, not growth |
| Indirect sets at 0.5 fit the dose–response best; an exploratory estimate puts an indirect set at ~32% of a direct one for hypertrophy and ~16% for strength | [W15] · [W16] | R35 · R36 · §0.3 (b) |
| More weekly volume raised size and strength with diminishing returns, steeper for strength; per-session returns flatten at ~11 fractional sets (hypertrophy) and ~2 direct sets (strength); frequency mattered little for hypertrophy | [W16] · [W15] | R33 · R37 · Stage 0 R19 |
| Adding curls and extensions to multi-joint training added no arm growth (untrained and trained men) | [W17] · [W18] | R35 · R36: indirect sets count, direct work stays |
| A minimum of 4 weekly sets per muscle group at 6–15 RM; supersets and similar techniques roughly halve session time | [W19] | R47 · R38 · R40 |
| ACSM 2026: every major muscle group at least twice a week; hypertrophy ≥10 sets per muscle group a week; strength ≥80% 1RM; power 30–70% 1RM with the fastest concentric; stopping at 2–3 RIR gives the same outcomes with less fatigue | [W20] | R33 · R34 · R47 · §5.5 Stage 0 review |
| Strength gains are specific to the equipment type and to the range trained; unstable surfaces cut force output | [W21] · [W22] · [W23] · [W24] | §2.1 strength S1–S2 |
| Multi-joint vs single-joint at equal volume: one trial favoured multi-joint, a review found them equivalent | [W25] · [W26] | §2.1 tie-breakers |
| Load steps of 2–10% | [W27] | §2.1 S3 · R42 |
| Power depends on movement, load and velocity specificity; in weaker men, heavy strength training matched ballistic training for power; fast-up, controlled-down training improved power (older adults, mostly machines) | [W28] · [W29] · [W30] | §2.1 power P1–P2 |
| Power-optimal loads sit around 30–70% 1RM; low velocity loss within a set favours jump and sprint gains | [W31] · [W32] · [W20] | §2.1 power P3 · §5.5 Stage 0 review |
| Weightlifting pulls without the catch are at least as effective as lifts with it, but they finish in full extension | [W33] | §2.1 power (Stage 0 R2 rules them out) |
| Low-load, high-rep training improves local muscular endurance most | [W34] · [W35] · [W36] | §2.1 endurance E1 |
| RIR is misjudged by about one rep, worse above 12 reps; fatigue changes lift kinematics; hypermobile people have poorer joint position sense | Stage 0 [W64] · [W37] · Stage 0 [W66] | §2.1 endurance E2–E3 |
| Closed-chain programmes improved proprioception, balance and pain in joint hypermobility syndrome; exercise evidence in EDS is sparse | [W38] · [W39] | §2.1 general fitness · §0.3 (e) |
| Heavy, ramped loading was tolerated in hypermobile shoulders | Stage 0 [W12] | §2.1 strength |
| Young adults kept their hypertrophy for 32 weeks on a third of the training volume (fibre size even on a ninth); older adults needed more | [W40] | R47 |
| Intensity is the key variable for keeping strength and size; one session a week can suffice in younger adults | [W41] | R47 |
| 4 sets a week kept quadriceps size and strength for 12 weeks (untrained women) | [W42] | R47 |
| A ~500 kcal/day deficit prevented lean-mass gains but not strength gains (meta-analysis) | [W43] | R47 |
| In a deficit, ≥10 weekly sets went with little lean-mass loss (low certainty); 12 vs 30 sets per muscle group a week kept fat-free mass alike in a 40% deficit over 4 weeks (trained, n = 16), and low vs high volume did likewise in trained men; one set to failure twice a week kept lean mass and strength for 4 weeks in a 20% deficit; contest-prep guidance trains each muscle at least twice a week | [W44] · [W45] · [W46] · [W47] · [W53] | R47 |
| Supersets matched traditional sets in reps, volume load, strength and hypertrophy, in shorter sessions with higher perceived exertion; agonist–antagonist pairs raised reps | [W48] | R38 · R40 |
| Progressing reps or progressing load: both viable over 8 weeks | [W49] | R42 |
| Adding sets in steps beat holding volume constant (from reference.md, not re-checked) | [W50] | R42 (c) |
| A week off mid-programme cost strength and added no size; consensus defines a deload as reduced training stress — fewer sets or reps, lower frequency or more RIR — usually ~7 days every 4–6 weeks, planned or autoregulated | [W51] · [W52] | R44 · D-01 · D-06 |
| Prone (hip-extended) leg curls work the biarticular hamstrings shorter than seated curls and grew them less: whole hamstrings +9.3% vs +14.1% over 12 weeks (n = 20, one leg per condition) | [W54] | R26 (catalogue zone labels) |
| The hip thrust puts peak glute tension near full hip extension, while the squat's sticking region sits in deeper hip flexion; 9 weeks of either grew the gluteus maximus alike (n = 34) | [W55] | R26 (catalogue zone labels) |
| A wide-grip pull-up reached 90° of arm abduction with 45° of external rotation (n = 11, motion capture); the shoulder-width front grip was not flagged, and the supinated grip starts in marked external rotation. A clinical review puts the front pulldown's grip at 1.25–1.5× shoulder width, torso leaning back ~30°, clear of abduction with external rotation. Lat activation did not differ across seven grips from 1× to 1.5× shoulder width, with or without a 30° lean (n = 40, all p > 0.05) | [W56] · [W57] · [W58] | Catalogue grip cues for vertical pulls at shoulder stage 1 (Stage 0 D-63) |
| In multidirectional shoulder instability, rehabilitation trains the anterior deltoid with flexion raises first — short lever, 0–4 kg, 8–20 reps, after posterior-deltoid work — and adds controlled overhead presses later; elevation past 90° comes last. Anterior-deltoid activity in the bench press and the lateral raise is similar (21% of a maximal contraction at 60% 1RM), and the shoulder press's is highest (33%), by EMG only | [W59] · [W60] | Catalogue C138 (front raise, revision 10) |

### 5.5 Reasoning ✏️

| Reasoning | Informs |
|---|---|
| Compounds before direct sets: harvest is real only when a planned compound produces it, so the compounds exist before direct sets are derived | §0.2 · R35 · R36 |
| The zone label is a fact about the exercise and serves every goal; the coverage rule is a growth strategy and binds hypertrophy only | R26–R28 |
| With every joint staged (Stage 0 D-28), "S outranks L for a gated joint" would put S first everywhere; Stage 0's criterion 1 — residual joint risk — keeps the intent for a joint that is actually at risk | R29 |
| L stays first for hypertrophy although its meta-analytic edge is trivial: nothing is lost by it, and some muscles (the triceps long head) show large effects | R28 · §2.1 |
| The buffer: counted at 0.5 instead of ~0.32, harvest overstates by 0.18 per indirect set; at half of a 10-set target that is 1.8 sets, about the buffer. Larger harvest shares outgrow it (§0.3 (b)) | R36 |
| Exercise time as an upper bound: Stage 0 R19 is a ceiling; 4 s per rep follows Stage 0 R25 (3 s down, 1 s up) | R40 |
| The bench is a station: with one of each, an occupied bench blocks every bench exercise (Stage 0 D-09), so bench and two-station exercises need alternatives that avoid all their stations | R41 |
| Goal-fit tests rank only exercises that already pass the hard gates; in hypermobile joints, guided paths and mechanical stops matter most when fatigue rises (endurance) or loads are heavy (strength) | §2.1 |
| Power at loading stages 1–3: jumps, throws and catches are out (Stage 0 R10 · R13) and pulls finish in terminal extension (Stage 0 R2); heavy lifts with maximal concentric intent remain, and they matched ballistic training in weaker men | §2.1 power |
| Spreading targets was proposed because splitting a target over two sessions costs nothing at equal volume and halves what a swapped session takes away; Harry accepts the swapped week's shortfall instead (Stage 0 §0.4 (f)), so R37 stays (D-05) | R37 |
| Maintenance (D-04): keeping the load is what preserves muscle, so loads stay where the last block left them while volume drops toward a floor of 4 sets a group a week; the default of 6–10 gives margin, and more than ~12 added no retention in deficit trials | R47 |
| Cross-region indirect sets count toward no target (D-02): with one goal per region (Stage 0 §0.3), a set trained under one region's row does not stand in for the other region's work; recovery is a separate matter, which Stage 0 R20's guard covers | R35 |
| 🔖 Stage 0 review notes, not Stage 1 decisions: (1) ACSM 2026 puts power at 30–70% 1RM while Stage 0's power row reads ≈80–90% (NSCA); with no ballistic release allowed before stage 4, light loads must be braked before lockout, which favours the heavier row for now. (2) ACSM 2026 finds 2–3 RIR as effective as going closer, with less fatigue, which bears on Stage 0 D-45's isolation at 1 RIR. (3) ACSM 2009 allows longer rests for muscular endurance than the row's ≤30 s (NSCA) | Stage 0 §2.2 · R18 |

---

## 6. Deferred material

| Item | To |
|---|---|
| Exercise catalogue as seed data (Stage 0 D-18) | Done 2026-10-02: `ExerciseCatalogue.json` + `.md` (D-03) |
| Catalogue readings of Stage 0 rules: R12's scope, knee depth outside squat patterns, 'glutes' in badminton's avoid-the-day-before row, the kickback's exclusion, holds as hypertrophy sets (`ExerciseCatalogue.md` §5, A1–A5) | Decided 2026-10-03: Stage 0 D-54…D-58 |
| Stale alternative-table numbers in the three upper focus files (§5.2) | Stage 2 |
| P4 · long femur and humerus are read by no rule; they wait on limb-length research (T2). First reading, Harry 2026-10-06: his long humerus takes a bar on the back past 45° of shoulder external rotation, or bends the wrists heavily (catalogue A9: bar-on-back rows wait for shoulder stage 2) | Backlog |
| Smith front squat with arms crossed: a quads row that takes heavy loads on a mechanical stop (§2.1 S2) inside shoulder stage 1 (catalogue A9) | Backlog: only if the shoulder stays at stage 1 (Harry, T10 A, 2026-10-06) |
| A conditioning (aerobic) goal row | Backlog (Stage 0 §6) |
| Ankle and hip control tests, which also gate court drills (Stage 0 D-52) | Decided 2026-10-03: Stage 0 D-61 · D-62 |
| Shoulder, elbow, wrist and spine control tests, which gate the catalogue's locked one-arm rows | Decided 2026-10-04: Stage 0 D-63…D-66 |
| Where the plan's rows, alternatives, set counts, exercise time and sport note sit in a routine file | Stage 2 |
| Stage 0 review notes on power load, RIR and endurance rest (§5.5) | Harry's Stage 0 review |

---

## 7. Walkthrough

**Sample.** The prompt's canonical example, plus real quirks from `routine_upperbody` v6 and `routine_lowerbody` v4.

Source: "Build full-body routine A: preacher curl and Smith squat." Fixture: focus block · upper and lower Hypertrophy · priority targets biceps, quads · block week 1 after a 2-month layoff · every joint at loading stage 1 · badminton in season · current routines: none yet.

| Step | Definition | Decision | Action | Output |
|---|---|---|---|---|
| S1.1 | Stage 0 §4.1 | §0.1 Input | Every field set; no current routines; a new routine | Current state valid · empty inventory · new routine |
| S1.2 | Stage 0 R17 · R18 · R20 · R22 · R24 | §0.2 | Hypertrophy in both regions; weeks 1–2 → ≈60% loads; week 1 → compounds 3 RIR, isolation 2 RIR; no region excluded; routine A trains both regions, so ≤3 sessions a week | Frame |
| S1.3 | R33 | §0.2 Volume | Bottom of the range | Biceps 10 · quads 10 |
| S1.4 | R26–R32 · Stage 0 R1–R15 | Stage 0 §0.2 | Biceps: preacher curl (L, supported), spider curl (M), band curl with elbows ahead (S). Quads: the requested Smith squat waits for shoulder stage 2 — a bar on Harry's back takes his shoulders past 45° of external rotation (Stage 0 §2.5 · D-63; catalogue A9) — so the goblet squat stands in (D-09). Ranked: wall sit above parallel (hold, M; Stage 0 D-58), first under R32 since it loads no other muscle; goblet squat above parallel (M); the sit-to-stand fails H2, since at body weight 3 RIR lies past 15 reps. Every L blocked by Stage 0 R3 · R11 at stage 1. Badminton verdicts green; the goblet squat carries over (eccentric quad) | Ranked candidates |
| S1.5 | R35 | §0.2 order | No planned exercise trains biceps or quads as a synergist; rows are out (R32) | Harvest 0 · 0 |
| S1.6 | R36 · R28 · R29 · R48 | — | Biceps direct 10 rounds up to 12 from preacher (L) + spider (M), quads 10 to 12 from goblet squat + wall sit (both M): two exercises of at least 3 sets in each session (R48) | Biceps L + M ✓ · quads M, L gap named |
| S1.7 | R37 · Stage 0 R19 · R20 | — | 12 ≥ 9 → two sessions, 6 + 6 per muscle; 6 ≤ 8 per session; one routine, so no cross-routine guard; the goblet squat keeps the requested exercise's 3 sets | Routine A × 2 a week: preacher 3 · spider 3 · goblet squat 3 · wall sit 3 |
| S1.8 | Stage 0 §2.2 · R16–R18 · R22 · R25 | — | Isolation 10–12 reps at 2 RIR; goblet squat 10–12 at 3 RIR; wall sit held at least 32 s (8 reps × 4 s, Stage 0 §2.2 · D-87), ending ~12 s before failure (3 RIR at ~4 s each, Stage 0 R16 · D-60); 60–90 s; ≈60% loads; 2–3 s lowering | Exercise rows |
| S1.9 | R38–R40 | — | Preacher ↔ goblet squat (cross-region, no overlap), isolation first; spider ↔ wall sit (a hold is a neutral partner). Time with holds of h s: 3 × (48 + 48 + 90) + 3 × (48 + h + 90) − 90 = 882 + 3h s | ≈17 min at h = 45 s, ≈19.2 min at h = 90 s ✓ (Stage 0 R19) |
| S1.10 | R41 · Stage 0 R21 | — | Preacher (bench): no L without the bench at shoulder stage 1 — the behind-body cable curl (L, fixed line, Stage 0 R5) waits for shoulder stage 2 (Stage 0 D-63) — so both alternatives are named as a gap. Spider (bench): band curl with elbows at the sides, standing cable curl (both M, band first). The goblet squat and the wall sit use no station, so they need none. Quads and glutes collect sets → badminton | Alternatives · "Day after: no badminton" |
| S1.11 | R42 · Stage 0 R22 | — | Ramp loads in weeks 1–4; progression from week 5 | Progression lines |
| S1.12 | R45 · R46 | — | Plan assembled; checks 1–10 listed with two named gaps: quads L at stage 1, the preacher curl's alternatives (no L without the bench until shoulder stage 2) | Plan |

**Corpus quirks traced**

| Quirk | Step | Rule | Result |
|---|---|---|---|
| Preacher curl "shortened bias" (`routine_upperbody` v6) | S1.4 | R26 | L |
| Glutes "~5–6 sets" (`routine_lowerbody` v4) | S1.5 | R35 | 4.5 fractional (M2) |
| DB flat bench press as the Smith bench press's alternative (v6) | S1.10 | R41 | Fails: shares the bench (M3) |
| "~28 min working" (v6) | S1.9 | R40 | ≈30.5 min upper bound, inside Stage 0 R19 (M1) |
| Lat pulldown ↔ DB chest fly (v6) | S1.9 | R38 | Not a superset: same joint, not antagonists |
| Sit-to-stand to a bench at 90° knee (v4) | S1.4 | Stage 0 R3 · R11 | Out while the knee sits at stage 1 |

**What Stage 2 receives**

| Item | Field | Value |
|---|---|---|
| Routine A | Regions · sessions a week | Upper + lower · 2 |
| Exercise rows | Exercise · zone · sets × reps + RIR · rest · load | Preacher curl · L · 3 × 10–12, 2 RIR · Spider curl · M · 3 × 10–12, 2 RIR · Goblet squat above parallel · M · 3 × 10–12, 3 RIR · Wall sit above parallel · M · 3 × a hold of at least 32 s ending ~12 s before failure — all 60–90 s, loads at ≈60% of pre-layoff |
| Pairing | Pairs and order | Preacher ↔ goblet squat, isolation first · spider ↔ wall sit, isolation first |
| Alternatives | Per station exercise | As in S1.10, with the preacher curl's gap named |
| Set count | Target · harvest · direct | Biceps 10 · 0 · 12, 2 above the target (R48) · quads 10 · 0 · 12, 2 above the target (R48) |
| Zone coverage | Per target | Biceps L + M ✓ · quads M, L gap named (knee at stage 1) |
| Exercise time | Per session | ≈17 min with 45 s holds |
| Sport note | — | Day after: no badminton (quads, glutes) |
| Checks | R46 (1)–(10) | Pass, with the two gaps named |

Verified 2026-10-02: exercise times, harvest and buffer arithmetic re-run in Python; rule, step and section references checked by script. Re-run 2026-10-06 on the same fixture (D-10): the Smith squat waits for shoulder stage 2 (catalogue A9), so does the behind-body cable curl (Stage 0 D-63), and timed holds count as hypertrophy sets (Stage 0 D-58); exercise time re-computed in Python. Re-run 2026-10-13 (D-11): spider curl and wall sit at 3 sets (R48), biceps and quads 12 a week, the wall sit held at least 32 s (Stage 0 D-87); exercise time re-computed in Python.

---

## 8. References

W1–W47 and W53 were read by research agents on 2026-10-02, abstract or full text unless marked; their quotes came through a fetch summariser, so exact figures are worth a spot-check before they are relied on. W48–W52 were read by Claude the same day, W54–W55 too, for the exercise catalogue (abstract and results via the fetch summariser). PubMed showed a reCAPTCHA page, and several publishers returned 402, 403 or 429; those sources were read through repositories or publisher abstracts instead. W56–W58 were read by Claude on 2026-10-06 for the catalogue's vertical pulls: W56 in full through Imperial's open-access copy, W57 through a full-text PDF, W58 on the publisher's page; ResearchGate returned 429 and PubMed a reCAPTCHA page. W59–W60 were read by Claude on 2026-10-12 for the catalogue's front raise, through a fetch summariser: W59 as a full-text PDF on a clinic's site, W60 on the publisher's page; PubMed and PubMed Central showed a reCAPTCHA page.

| ID | Source | Used for |
|---|---|---|
| W1 | Varović, Wolf, Steele, Schoenfeld, Grgic & Mikulic 2025, Int J Sports Med 46(14):1027–36, [DOI 10.1055/a-2615-4935](https://doi.org/10.1055/a-2615-4935); [SportRxiv preprint](https://sportrxiv.org/index.php/server/preprint/view/464) | R26 · R28 |
| W2 | Zabaleta-Korta et al. 2023, J Hum Kinet 88:259–70, [DOI 10.5114/jhk/163561](https://doi.org/10.5114/jhk/163561) | R26 · R28 |
| W3 | Kassiano et al. 2025, Int J Sports Med 46(5):334–43, [DOI 10.1055/a-2517-0509](https://doi.org/10.1055/a-2517-0509) | R26 · R28 |
| W4 | Attarieh et al. 2025, Eur J Sport Sci 25(4):e12279, [DOI 10.1002/ejsc.12279](https://doi.org/10.1002/ejsc.12279) ([ECU repository](https://ro.ecu.edu.au/ecuworks2022-2026/5998/)) | §2.1 hypertrophy |
| W5 | Larsen et al. 2026, Front Physiol 17:1750722, [DOI 10.3389/fphys.2026.1750722](https://doi.org/10.3389/fphys.2026.1750722) | §2.1 hypertrophy |
| W6 | Larsen et al. 2025, Front Physiol 16:1611468, [DOI 10.3389/fphys.2025.1611468](https://doi.org/10.3389/fphys.2025.1611468) | R26 · R29 |
| W7 | Maeo et al. 2023, Eur J Sport Sci 23(7):1240–50, [DOI 10.1080/17461391.2022.2100279](https://doi.org/10.1080/17461391.2022.2100279) | §2.1 hypertrophy |
| W8 | Fonseca et al. 2014, J Strength Cond Res 28(11):3085–92, [DOI 10.1519/JSC.0000000000000539](https://doi.org/10.1519/JSC.0000000000000539) | R28 |
| W9 | Kassiano et al. 2022, J Strength Cond Res 36(6):1753–62, [DOI 10.1519/JSC.0000000000004258](https://doi.org/10.1519/JSC.0000000000004258) | R28 |
| W10 | Baz-Valle et al. 2019, PLoS One 14(12):e0226989, [DOI 10.1371/journal.pone.0226989](https://doi.org/10.1371/journal.pone.0226989) | R28 |
| W11 | Pedrosa et al. 2022, Eur J Sport Sci 22(8):1250–60, [DOI 10.1080/17461391.2021.1927199](https://doi.org/10.1080/17461391.2021.1927199) | R29 |
| W12 | Kassiano et al. 2023, J Strength Cond Res 37(9):1746–53, [DOI 10.1519/JSC.0000000000004460](https://doi.org/10.1519/JSC.0000000000004460) | R29 |
| W13 | Pedrosa et al. 2023, Sports 11(2):39, [DOI 10.3390/sports11020039](https://doi.org/10.3390/sports11020039) | R29 |
| W14 | Strey et al. 2026, Sport Sci Health 22(1):33, [DOI 10.1007/s11332-025-01586-5](https://doi.org/10.1007/s11332-025-01586-5) — 🔖 verification level not reported | R29 |
| W15 | Remmert, Pelland, Robinson, Hinson & Zourdos 2025, [SportRxiv preprint](https://sportrxiv.org/index.php/server/preprint/view/537) | R35 · R36 · R37 |
| W16 | Pelland et al. 2026 (online Dec 2025), Sports Med 56(2):481–505, [DOI 10.1007/s40279-025-02344-w](https://doi.org/10.1007/s40279-025-02344-w) — abstract and methods only | R33 · R35 · R37 |
| W17 | Gentil et al. 2013, Appl Physiol Nutr Metab 38(3):341–4, [DOI 10.1139/apnm-2012-0176](https://doi.org/10.1139/apnm-2012-0176) | R35 · R36 |
| W18 | de França et al. 2015, Appl Physiol Nutr Metab 40(8):822–6, [DOI 10.1139/apnm-2015-0109](https://doi.org/10.1139/apnm-2015-0109) | R35 · R36 |
| W19 | Iversen, Norum, Schoenfeld & Fimland 2021, Sports Med, [DOI 10.1007/s40279-021-01490-1](https://doi.org/10.1007/s40279-021-01490-1) ([SASMA summary](https://www.sasma.org.za/articles/no-time-to-lift-designing-time%E2%80%91efficient-training-programs-for-strength-and-hypertrophy-a-narrative-review/)) | R47 · R38 · R40 |
| W20 | Currier et al. 2026, ACSM position stand, Med Sci Sports Exerc 58(4):851–72, [DOI 10.1249/MSS.0000000000003897](https://doi.org/10.1249/MSS.0000000000003897) — abstract and a [secondary summary](https://getfitcraft.com/science/acsm-2026-resistance-training-guidelines) | R33 · R34 · R47 · §5.5 |
| W21 | Haugen et al. 2023, BMC Sports Sci Med Rehabil 15:103, [DOI 10.1186/s13102-023-00713-4](https://doi.org/10.1186/s13102-023-00713-4) | §2.1 strength |
| W22 | Wolf et al. 2023, Int J Strength Cond 3(1), [DOI 10.47206/ijsc.v3i1.182](https://doi.org/10.47206/ijsc.v3i1.182) | §2.1 strength · §0.3 (d) |
| W23 | Pallarés et al. 2021, Scand J Med Sci Sports 31:1866–81, [DOI 10.1111/sms.14006](https://doi.org/10.1111/sms.14006) | §2.1 strength |
| W24 | Zemková 2021, Appl Sci 11:3401, [DOI 10.3390/app11083401](https://doi.org/10.3390/app11083401) | §2.1 strength S2 |
| W25 | Paoli et al. 2017, Front Physiol 8:1105, [DOI 10.3389/fphys.2017.01105](https://doi.org/10.3389/fphys.2017.01105) | §2.1 tie-breakers |
| W26 | Gentil, Fisher & Steele 2017, Sports Med 47:843–55, [DOI 10.1007/s40279-016-0627-5](https://doi.org/10.1007/s40279-016-0627-5) | §2.1 tie-breakers |
| W27 | Ratamess et al. 2009, ACSM position stand, Med Sci Sports Exerc 41(3):687–708, [DOI 10.1249/MSS.0b013e3181915670](https://doi.org/10.1249/MSS.0b013e3181915670) | §2.1 S3 · R42 · §5.5 |
| W28 | Cormie, McGuigan & Newton 2011, Sports Med 41:125–46, [DOI 10.2165/11538500-000000000-00000](https://doi.org/10.2165/11538500-000000000-00000) | §2.1 power |
| W29 | Cormie, McGuigan & Newton 2010, Med Sci Sports Exerc 42:1582–98, [DOI 10.1249/MSS.0b013e3181d2013a](https://doi.org/10.1249/MSS.0b013e3181d2013a) | §2.1 power |
| W30 | Balachandran et al. 2022, JAMA Netw Open 5:e2211623, [DOI 10.1001/jamanetworkopen.2022.11623](https://doi.org/10.1001/jamanetworkopen.2022.11623) | §2.1 power P1 |
| W31 | Soriano et al. 2015, Sports Med 45:539–56, [DOI 10.1007/s40279-015-0341-8](https://doi.org/10.1007/s40279-015-0341-8) | §2.1 power · §5.5 |
| W32 | Jukic et al. 2023, Sports Med 53:177–214, [DOI 10.1007/s40279-022-01754-4](https://doi.org/10.1007/s40279-022-01754-4) | §2.1 power P3 |
| W33 | Suchomel et al. 2020, J Funct Morphol Kinesiol 5:28, [DOI 10.3390/jfmk5020028](https://doi.org/10.3390/jfmk5020028); Suchomel et al. 2015, Sports Med, [DOI 10.1007/s40279-015-0314-y](https://doi.org/10.1007/s40279-015-0314-y) | §2.1 power |
| W34 | Campos et al. 2002, Eur J Appl Physiol 88:50–60, [DOI 10.1007/s00421-002-0681-6](https://doi.org/10.1007/s00421-002-0681-6) | §2.1 endurance |
| W35 | Schoenfeld et al. 2015, J Strength Cond Res 29:2954–63, [DOI 10.1519/JSC.0000000000000958](https://doi.org/10.1519/JSC.0000000000000958) | §2.1 endurance |
| W36 | Hackett et al. 2022, Sci Sports 37:405–20, [DOI 10.1016/j.scispo.2021.11.002](https://doi.org/10.1016/j.scispo.2021.11.002) | §2.1 endurance |
| W37 | Erman et al. 2023, PLOS ONE 18:e0289089, [DOI 10.1371/journal.pone.0289089](https://doi.org/10.1371/journal.pone.0289089) | §2.1 endurance E2 |
| W38 | Ferrell et al. 2004, Arthritis Rheum 50:3323–28, [DOI 10.1002/art.20582](https://doi.org/10.1002/art.20582) | §2.1 general fitness |
| W39 | Buryk-Iggers et al. 2022, Arch Rehabil Res Clin Transl 4:100189, [DOI 10.1016/j.arrct.2022.100189](https://doi.org/10.1016/j.arrct.2022.100189) | §2.1 general fitness · §0.3 (e) |
| W40 | Bickel, Cross & Bamman 2011, Med Sci Sports Exerc 43:1177–87, [DOI 10.1249/MSS.0b013e318207c15d](https://doi.org/10.1249/MSS.0b013e318207c15d) | R47 |
| W41 | Spiering et al. 2021, J Strength Cond Res 35:1449–58, [DOI 10.1519/JSC.0000000000003964](https://doi.org/10.1519/JSC.0000000000003964) | R47 |
| W42 | Mpampoulis et al. 2024, Sports 12:198, [DOI 10.3390/sports12070198](https://doi.org/10.3390/sports12070198) | R47 |
| W43 | Murphy & Koehler 2022, Scand J Med Sci Sports 32:125–37, [DOI 10.1111/sms.14075](https://doi.org/10.1111/sms.14075) | R47 |
| W44 | Roth et al. 2022, Eur J Appl Physiol 122:1129–51, [DOI 10.1007/s00421-022-04896-5](https://doi.org/10.1007/s00421-022-04896-5) | R47 |
| W45 | Roth et al. 2023, Scand J Med Sci Sports 33:20–35, [DOI 10.1111/sms.14237](https://doi.org/10.1111/sms.14237) — sets and RIR via a secondary source | R47 |
| W46 | Nait-Yahia et al. 2026, Eur J Clin Nutr 80:781–90, [DOI 10.1038/s41430-026-01757-8](https://doi.org/10.1038/s41430-026-01757-8) — n = 16 | R47 |
| W47 | Carlson et al. 2022, Res Q Exerc Sport 94:990–1000, [DOI 10.1080/02701367.2022.2097625](https://doi.org/10.1080/02701367.2022.2097625) | R47 |
| W48 | Zhang, Weakley, Li et al. 2025, Sports Med 55:953–75, [DOI 10.1007/s40279-025-02176-8](https://doi.org/10.1007/s40279-025-02176-8) | R38 · R40 |
| W49 | Plotkin et al. 2022, PeerJ 10:e14142, [DOI 10.7717/peerj.14142](https://doi.org/10.7717/peerj.14142) | R42 |
| W50 | Enes, De Souza & Souza-Junior 2023, Med Sci Sports Exerc, [DOI 10.1249/MSS.0000000000003317](https://doi.org/10.1249/MSS.0000000000003317) — not re-checked | R42 (c) |
| W51 | Coleman et al. 2024, PeerJ 12:e16777, [DOI 10.7717/peerj.16777](https://doi.org/10.7717/peerj.16777) | R44 · §4 |
| W52 | Bell, Strafford, Coleman, Androulakis Korakakis & Nolan 2023, Sports Med Open 9:87, [DOI 10.1186/s40798-023-00633-0](https://doi.org/10.1186/s40798-023-00633-0) ([DCU repository](https://doras.dcu.ie/30319/1/Integrating_Deloading_into_Strength_and_Physique_S.pdf)) | R44 · §4 |
| W53 | Helms et al. 2015 (epub 2014), J Sports Med Phys Fitness 55:164–78 ([ECU repository](https://ro.ecu.edu.au/ecuworkspost2013/1869/)) | R47 |
| W54 | Maeo et al. 2021, Med Sci Sports Exerc 53(4):825–37, [DOI 10.1249/MSS.0000000000002523](https://doi.org/10.1249/MSS.0000000000002523) ([ResearchGate record](https://www.researchgate.net/publication/344445943_Greater_Hamstrings_Muscle_Hypertrophy_but_Similar_Damage_Protection_after_Training_at_Long_versus_Short_Muscle_Lengths)) | R26 (catalogue) |
| W55 | Plotkin et al. 2023, Front Physiol 14:1279170, [DOI 10.3389/fphys.2023.1279170](https://doi.org/10.3389/fphys.2023.1279170) | R26 (catalogue) |
| W56 | Prinold & Bull 2016, J Sci Med Sport 19:629–35, [DOI 10.1016/j.jsams.2015.08.002](https://doi.org/10.1016/j.jsams.2015.08.002) ([Imperial repository, CC BY](https://spiral.imperial.ac.uk/entities/publication/cc9a7a65-fb9b-488b-8e90-c311fe7eb086)) | Catalogue (vertical pulls) |
| W57 | Fees, Decker, Snyder-Mackler & Axe 1998, Am J Sports Med 26(5), [DOI 10.1177/03635465980260052301](https://doi.org/10.1177/03635465980260052301) — clinical review | Catalogue (vertical pulls) |
| W58 | Buonsenso et al. 2025, J Funct Morphol Kinesiol 10(3):345, [DOI 10.3390/jfmk10030345](https://doi.org/10.3390/jfmk10030345) | Catalogue (vertical pulls) |
| W59 | Watson, Warby, Balster, Lenssen & Pizzari 2017, Shoulder Elbow 9(1):46–53, [DOI 10.1177/1758573216652087](https://doi.org/10.1177/1758573216652087) ([full text](https://georgemurrellshoulders.com.au/wp-content/uploads/2020/10/Watson-Warby-protocol.pdf)) — the MDI rehabilitation programme, part 2 | Catalogue (front raise) |
| W60 | Watson, Pizzari, Balster, Lenssen & Warby 2022, J Clin Med 11(17):5140, [DOI 10.3390/jcm11175140](https://doi.org/10.3390/jcm11175140) — review | Catalogue (front raise) |
