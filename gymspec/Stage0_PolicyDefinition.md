# Stage 0 — Policy Definition

**Normative · draft.** Everything in this document is binding on Stages 1–2.
Rationale, evidence, closed decisions and deferred material → `Stage0_SupplementInfo.md`. `[HYP]` marks hypertrophy-specific content; everything else is goal-agnostic.

**Decisions vs rules.** §0 holds policy: stances, scope, accepted limits — statements no test can falsify. §3 holds behaviour: normative statements the implementation is built and tested against. Behaviour is stated once, in §3; §0 references R-numbers rather than restating them.

---

## 0. Project decisions

### 0.1 Scope and risk

| Item | Value |
|---|---|
| Athlete | **One athlete: Harry** (§1.1). Every plan and routine file serves his current block, set in Current state (§4.1). |
| Risk | **Every joint is unstable under load.** Hypermobility (hEDS/HSD spectrum) is systemic, so R1–R10 apply to every joint and every exercise, primary or alternative, at all times: they are the baseline, not a response to a problem. |
| Loading gate | **Staged loading applies to every joint, all the time** (§2.5 · R11–R14 · R24 · D-28). Each joint holds its own loading stage in Current state (§4.1). |
| Clinician override | **A treating clinician's criteria override the exit criteria in §2.5, and a clinician's stretching prescription overrides R7 for the muscle it names** — e.g. gentle stretching of a short muscle with the neighbouring joint held stable (D-43). |
| Scheduling | **Harry schedules every session: which days hold training, conditioning and sport sessions, and how they interleave** (D-48). Plans and routine files assign no days. Plans state each routine's regions, its sessions per week (§4.1 `current_routines`) and the sports not to play the day after it (R21); routine files state its regions and those sports, and the Stage 2 register keeps its sessions per week (Stage 2 D-05). R20 and R21 bind the schedule Harry sets. |
| Session density | **Joint control, not fitness, bounds session density and supersets** (R19). |
| Goals and sports | **The specification is goal- and sport-agnostic.** Block type, block goal, priority targets and in-season sports change from block to block; they live in Current state (§4.1), and sport rules key off the sport's profile (§1.2). |
| Out of scope | **Nutrition** (D-08): the diet itself — a fat-loss period only selects the maintenance block (§0.3) · **Harry's PDF exports in `gympdf/`**, left untouched (D-14). |

### 0.2 Principles

| Item | Value |
|---|---|
| Hard gates | **Equipment, safety constraints and the loading gate are hard gates** (R15 · R1–R10 · R11–R14). An exercise that fails one is out before it is considered. |
| Selection criteria | **Exercises that pass the hard gates are chosen by five criteria, each outranking the next** (D-35): (1) hypermobility joint safety — lower residual joint risk wins; (2) the priority targets in Current state; (3) goal fit — how well the exercise meets the goal-fit test of the block goal covering its region (tests: Stage 1, D-36); (4) session efficiency; (5) sport compatibility — tilts a decision only between options equal on 1–4, or when Current state names an in-season sport (D-05). |
| Control, not range | **Loading stages unlock on control, not range** (R14): hypermobile joints already have excess range. |
| One effort scale | **Reps + RIR is the only scale for effort and load** (R16 · R17). |

### 0.3 Goals and blocks

| Item | Value |
|---|---|
| Regions | **Two regions: upper body (trunk included), and lower body** (§2.1 · D-04). |
| One goal per region | **A block sets one goal per region it trains, and every muscle in that region follows it** (§4.1 · D-03). A goal is one row of the goal table (§2.2). |
| Planning order | **Training goal → target muscle groups → training volume → exercises, chosen by the selection criteria (§0.2)** (D-35). Steps → Stage 1. |
| Block types | **A block is either a focus block or a maintenance block** (§4.1 `block_type`). |
| Focus blocks | **A focus block programs only its priority targets.** Any exercise whose prime mover is a priority target is eligible; those that load other muscles least are preferred, unless that extra load is harvest used on purpose to get another priority target enough sets (§2.3 · D-22). Every other muscle gets zero direct sets and no target; harvest that lands on it is incidental. Rules → Stage 1. |
| Maintenance blocks | **A maintenance block is a separate block whose main focus is keeping every muscle group (§2.1) activated during a fat-loss period** (D-23). Its volume, goal rows and exercise rules → Stage 1 (Supplement §6). |
| Volume | **Volume is counted in weekly sets per muscle, and sessions split them freely within R19 and R20** (§2.3 · D-27). Strength and power spread each target's sets over every training session of its region (§2.7 · R20), since per-session returns flatten early. The goal table's Sets are per exercise per session, for the exercise's target muscle (§2.2 · D-29); which goals carry a weekly target is set in Stage 1. |

### 0.4 Accepted limits

| # | Limit |
|---|---|
| a | Some growth and weekly capacity are traded for joint control: sets stop short of failure (R17 · R18), sessions stay below the per-session volume the evidence supports (R19), and each region trains at most 3 times a week (R20). Accepted because joint safety ranks first (§0.2). |
| b | Effort, range and symptoms are self-assessed: RIR, ~70–80% of range, pain ≤5/10 and the "loose joint" feeling have no external measure. Accepted because 1RM testing and testing to muscular failure are avoided in this population (Supplement §5.4); the §2.5 symmetry tests stop at technical failure (D-85). |
| c | Muscles outside a focus block detrain while it runs. Accepted because detrained size returns within the first retraining weeks (Supplement §5.4). |
| d | Sport sessions are not dosed: their load counts toward no set total or session ceiling, and Harry schedules them (§0.1). Accepted because sport load varies from session to session and is not tracked. |
| e | Until a joint passes its control test (§2.5), every routine keeps it at loading stage 1 — bilateral work only: no unilateral, plyometric or impact loading (D-54), the §2.5 tests aside (D-85) — although badminton loads it that way. Accepted because every joint is staged (D-28). |
| f | A week in which Harry swaps a gym session for a conditioning session trains below the plan's weekly sets. Accepted because conditioning prepares him for his sports and he places it himself (D-52 · D-53). |

---

## 1. Athlete, sports and equipment

### 1.1 Athlete

| Item | Value |
|---|---|
| Profile | Male, born 1991, 168–170 cm, ~57 kg. |
| Limbs | Long femur and humerus. |
| Joints | Hypermobile (hEDS/HSD spectrum): every joint is unstable under load and injury-prone (§0.1). |
| Background | Sport since childhood; fitness is not a limiter (§0.1). |

### 1.2 Sport profiles

One profile per sport (§4.2), muscles grouped by region. Read by R21 and by the Stage 1 sport filter. **Carryover** lists the qualities that, trained in the gym, transfer to the sport's performance or resilience; the sport filter favours exercises that train them. Evidence and grades → Supplement §5.5.

| Field | Archery | Badminton |
|---|---|---|
| Demand — upper | Rear and middle delts, mid/lower traps, rhomboids, lats, pec major, rotator cuff, triceps, forearm flexors and extensors, abs, obliques, spinal erectors | Shoulder internal rotators (pec major, lats, teres major, subscapularis), posterior rotator cuff, forearm pronators and supinators, wrist flexors and extensors, grip, triceps, obliques |
| Demand — lower | Calves, hip abductors and adductors | Quads, glute max, glute med, hamstrings, calves/Achilles, ankle evertors |
| Avoid the day before | The upper demand muscles | Calves/Achilles, quads, glute max and glute med, rotator cuff, forearm and grip |
| Carryover | Horizontal abduction and scapular retraction strength-endurance, incl. isometric holds at shoulder height; cuff external rotation; shoulder extension and adduction; pulling strength; trunk anti-rotation and anti-extension holds | Internal-rotation strength balanced by eccentric external rotation; pronation/supination and wrist flexion/extension; trunk rotation and anti-rotation; eccentric quad and glute; calf–Achilles capacity; overhead triceps secondary |
| Loads | Shoulders (cuff, biceps long head); elbows (toward hyperextension); fingers and wrists; spine | Shoulders, elbows, wrists; lumbar spine; knees; ankles and Achilles |

### 1.3 Equipment

**Stations** — one each, independent of one another; a station in use is unavailable (D-09).

| Station | Detail |
|---|---|
| Smith machine | — |
| Cable machine | Lat-pulldown/seated-row combo with two pulleys, high (pulldown) and low (row); attachments: its own bars plus 2 D-handles. List of exercises that can be executed on this machine: rows, pulldowns, pullover, curl, pushdown, overhead extension. |
| Hip abductor/adductor machine | — |
| Adjustable bench | — |

**Always available:** bands — 2 long, 2 short, Harry's own · multi-purpose frame: pull-up bars with varied handle positions, also the rack · Olympic barbells · adjustable dumbbells · foam roller · tennis ball · low step or box (5–20 cm) (D-30).

**Conditioning:** badminton court · bike, stationary or outdoor · pool · jump rope (D-44).

---

## 2. Training scheme

### 2.1 Regions

| Region | Muscles |
|---|---|
| Upper body | Upper-body + trunk muscles group (Entire Abs & Obliques, Entire Back, Chest & Shoulders, Arms & Hands). |
| Lower body | Lower-body muscles group (Hips and Gluteals, Thighs, Calves and Shins). |

### 2.2 Goal table (for each target muscle)

Reps per set; Sets per exercise per session, applied to the exercise's target muscle — a muscle's weekly sets add up over its exercises and sessions (§2.3); NSCA-based, adapted for hEDS (D-29). The values are a reference: within a row, the safer end for the joints is taken, except hypertrophy RIR from block week 5 (R17 · R18 · D-33 · D-45). A block's goal for a region is one row (§0.3). RM = reps + RIR.

| Goal | Sets | Reps | RIR | Load check | Rest |
|---|---|---|---|---|---|
| Hypertrophy | 3–6 | compounds 8–15 <br> isolation 10–20 <br> forearm/abs isolation 12–25 <br> timed isometrics, any muscle, each held at least its band's bottom reps × 4 s (D-58 · D-87) | R18 | none — reps + RIR set the load | 60–90 s |
| Strength | 2–6 | 3–5 | 1–3 | reps + RIR ≤ 6 (≈ ≥85% 1RM) | 2–5 min |
| Power | 3–5 | 1–3 | ≥3 | reps + RIR 4–8 (≈ 80–90% 1RM) | 2–5 min |
| Muscular endurance | 2–3 | ≥12 | 1–3 | reps + RIR ≥ 12 (≈ ≤67% 1RM) | ≤30 s |
| General fitness | 1–2 | 8–15 | 2–4 | none | 30–90 s |

The load check is read from reps + RIR, never tested (R16).

### 2.3 Set units

| Unit | Definition |
|---|---|
| Reps | Repetitions in one set, prescribed with RIR (R16). |
| Working set | One performed set of one exercise, warm-ups excluded. The goal table's Sets (§2.2) count working sets; R19's exercise time covers them and the rest between them. |
| Direct set | For a muscle: a working set in which that muscle is the prime mover. Counts 1. |
| Indirect set | For a muscle: a working set in which that muscle is a meaningful synergist but not the prime mover (rows for biceps, presses for triceps/front delt). Counts 0.5. |
| Fractional sets | Direct + 0.5 × indirect. The unit of weekly targets (Stage 1) and of the per-muscle session ceiling (R19). |
| Harvest | 0.5 × indirect sets: what a muscle collects without being the prime mover — any muscle an exercise loads beyond its prime mover, priority target or not (§0.3). |
| Session sets | For a muscle: the fractional sets it collects in one session. Ceiling: R19. |
| Weekly sets | For a muscle: its session sets summed over the week — sets × sessions when every session is equal. What weekly targets count (§0.3). |

**Which count to use.** Per muscle — fractional sets: weekly targets, session sets and the per-muscle session ceiling (R19). Per session and per exercise — working sets: the goal table's Sets (§2.2) and the sets whose time R19 caps. The two meet through direct sets: every working set is direct for exactly one muscle, so Σ working sets = Σ direct sets. That identity is a check, not a third count; Stage 1's capacity check relies on it.

### 2.4 Block

**Block.** The run of weeks in which one goal set stays in force: the block type, one goal row per trained region and the priority targets (§4.1). Routines, volume, sets and reps are derived from it top-down (§0.3 Planning order) and progress inside the block without ending it. The block ends when the goal set changes — a target is reached or replaced, a goal row changes, or an injury forces a new goal (D-40). **Block week** counts from the block start in Current state (§4.1).

### 2.5 Loading gate

Staged loading for every joint (D-28); each joint's current loading stage is kept in Current state (§4.1). R1–R10 apply at every loading stage.

| Loading stage | Loaded flexion depth (R3 · R11) | Unilateral (R12) | Plyometric / impact (R13) |
|---|---|---|---|
| 1 Partial range, bilateral | Partial range | No | No |
| 2 Full range, bilateral | Full range | No | No |
| 3 Unilateral | Full range | Yes | No |
| 4 Plyometric / impact | Full range | Yes | Yes |

**Exit criteria** — all must hold before the next loading stage unlocks (R14):

| # | Criterion |
|---|---|
| 1 | The step gate (§2.6) passes for two consecutive weeks at current loading. |
| 2 | Control: the joint's control test below is clean. It is a test, not a training set. |
| 3 | Symmetry, for paired joints: the weaker side reaches ≥90% of the stronger on one repeatable strength test — reps to technical failure on the same bodyweight, band-loaded or fixed-dumbbell movement, with the same set-up and cadence each time (D-68), scored on the mean of 2 sessions (D-67 · D-81). For the arm: ≥80% at the shoulder and ≥85% at the elbow and wrist (D-67). |

**Control tests**

| Joint | Test | Partial range | Symmetry test (criterion 3) |
|---|---|---|---|
| Knee | 10 bodyweight step-downs per leg from a 15–20 cm box at 60 beats a minute: 2 beats down, 2 up (D-84); no valgus, no pelvic drop, no pain | Above parallel | Single-leg sit-to-stand from a raised seat (thighs above parallel), arms crossed, touching the seat without sitting, reps to technical failure at 60 beats a minute: 2 beats down, 2 up (D-80 · D-82) |
| Ankle | Per leg: 10 single-leg heel raises at 60 beats a minute (up on one beat, down on the next), fingertip support, full height every rep, no inversion or eversion wobble, no pain; then a 30 s single-leg stance, eyes open, arms crossed, no touchdown or foot wobble (D-61) | R1's range, read as ~70–80% of the knee-to-wall lunge range | Single-leg heel raises to technical failure, same set-up both sides, at 60 beats a minute: up on one beat, down on the next (D-82) |
| Hip | Per leg: 5 single-leg squats to ~60° of knee bend (above parallel) at 60 beats a minute: 1 beat down, 1 up (D-84), filmed from the front; "good" on all five of Crossley's criteria — overall, trunk, pelvis, hip, knee; no pain (D-62) | R1's range | Single-leg bridges to technical failure, heel on the bench, at 60 beats a minute: up on one beat, down on the next (D-82) |
| Shoulder | Scapular dyskinesis test: one unloaded set, then 8–10 slow cycles of flexion and 8–10 of abduction, both arms together with 1.5 kg dumbbells, 2 s up and 2 s down, raised as far as comfortable, filmed from ~2 m behind; no obvious dyskinesis (winging or dysrhythmia) on either side, no worse than the unloaded set, no slipping, no pain (D-63) | Elevation ~75% of the measured active range; external rotation from neutral to the smaller of 45° and ~75% of its range; extension to neutral only | ExtRA abduction: one arm, back to the wall, 2.5 kg, scaption to 90° at 30 beats a minute (2 s up, 2 s down), soft elbow, reps to technical failure |
| Elbow | Kneeling push-ups on hex dumbbell handles: 10 reps at 60 beats a minute (3 beats down until the upper arms are level with the torso, 2 up, a 2-beat hold at the top), filmed side-on once per side; then, per arm, a 30 s hold on hands and knees; no rep or hold reaches straight (a bend of ~15° on paused video), no snap, clunk or drift into lockout, no pain (D-64) | Loaded reps stop 20–30% of the flexion arc short of straight (≥ 28–42° for a 140° arc) and short of full flexion; hyperextension is never loaded; measured side-on | One-arm seated dumbbell curls to technical failure, a fixed load giving 12–20 reps, 60 beats a minute: 2 beats up, 2 down (D-71) |
| Wrist | Per side, forearm supported, 1 kg dumbbell, 60 beats a minute (up on one beat, down on the next, D-71), inside range stops: 10 extensions, 10 flexions, 10 radial-to-ulnar deviations (forearm pronated) and 10 pronation–supination turns, filmed from above and the side; no clunk or catch, no giving way, no pain, no stop breached, on the beat (D-65) | ~70–80% of flexion and extension, read from tripod video (D-77); deviation and rotation held by stops and checked on video | Band wrist extensions to technical failure at 60 beats a minute, 2 beats up and 2 down (D-71), forearm pronated, same band and anchor; or grip with a dynamometer |
| Spine | Luomajoki's six movement-control tests, self-filmed: waiter's bow, pelvic tilt, sitting knee extension, rocking forward and backward on hands and knees (fists or handles), prone knee bend; 3 slow reps each, a test positive when 2 or more reps fail; at most 1 positive test, no pain (D-66) | 70–80% of flexion, extension and side-bending, capped at 70–80% of the healthy mean (D-69): ~36–42° of lumbar flexion and ~12–15° of extension, self-filmed side-on with a pen taped flat on the spine at the low-back dimples (≈S2) and another 15 cm higher, the change in angle between them read as the range (D-72 · D-77); rotation judged on video | — (not a paired joint) |

"Above parallel" caps the knee's loaded flexion at about 90° (R3 example). Outside squat patterns, a knee held static at about 90° or less while the load works elsewhere (hip thrust, seated calf raise), or bent deepest where the load is lightest (cycling), stays inside it (D-57).

Every joint now has a test line (D-61…D-66). The spine's partial range is capped at a healthy reference; every other joint's is read from his own measured range (R1 · D-69). Every angle these tests need is read from tripod video; the phone is never held on the limb (D-77).

**Tests, not training sets.** Every test in this section — range readings, control tests and symmetry tests — is a test, not a training set (D-85). Its line here, and the routine card that carries it out, set its range, load, side, pace and end point; R1–R25 do not apply to it, with two exceptions: R9's stops apply to every test, and a test session counts as a training session (§2.7) of the region it tests, so R20 spaces it like one. R14 and R24 act on the results, not on the test.

### 2.6 Step gate

Every progression step is checked against the step gate, which passes only when all four elements hold. A failed element is a **flare**.

| # | Element |
|---|---|
| 1 | Pain ≤5/10 during and after (D-01) |
| 2 | Baseline again the next morning |
| 3 | No swelling or warmth within 24 h |
| 4 | No "loose joint" feeling that day |

What a fail changes in the dose → Stage 1 (Supplement §6).

### 2.7 Training session

**Training session.** Any session of resistance work — weights, cables, bands, bodyweight or a joint protocol (D-47). It trains, and counts toward, every region whose muscles get direct sets in it (§2.1 · §2.3); indirect sets on another region's muscles fall under R20's per-muscle guard instead. Its pre and post mobility halves belong to it. Foam rolling, conditioning and sport sessions are not training sessions; conditioning sessions are separate sessions Harry fits in flexibly (D-53). Spacing: R20.

---

## 3. Governing rules

| ID | Rule |
|---|---|
| R1 — Peak tension range | **Peak tension sits at ~70–80% of the available range of motion.** Loaded stretch stays short of end range. Available range is his own measured range; at the spine, the smaller of his own and the healthy mean (D-69). |
| R2 — Soft bend | **Every joint keeps a soft bend in every position, the stretched position included.** No joint reaches terminal extension or terminal flexion under load. An exercise whose resistance peaks at the end of a joint's range, the soft bend its only margin, carries an end-range warning (D-55). |
| R3 — Gated range | **Every joint works only inside the range its current loading stage allows** (§2.5). Control, not range, unlocks each stage (R14). |
| R4 — Pulldown and pull-up stop | **Pulldowns and pull-ups stop at ~90–95% arm extension, with the shoulder blades braced at the top: held there by muscle, never pulled up toward the ears or left hanging** (D-42). Bracing is a hold, not an added movement. |
| R5 — Loaded shoulder extension | **Shoulder extension under load (incline or behind the torso) uses a supported position, or a cable with a fixed line of pull, in preference to free dumbbells.** An unsupported variant carries a warning. |
| R6 — Overhead loading | **Overhead loading keeps the scapula braced, and a cable line of pull ranks above free dumbbells.** |
| R7 — Active mobility | **Mobility work uses active drills: movements and holds made by the muscles crossing the joint, inside the range they control, with nothing external pushing a joint further and no bounce at end range** (D-43). Static-passive, PNF and ballistic stretching are not programmed; foam rolling manages tightness. A clinician's prescription overrides R7 (§0.1). |
| R8 — Trapezius | **The upper trapezius is not programmed directly; lower and mid trapezius take priority.** |
| R9 — In-session abort | **A session is skipped when joints feel loose that day; a set ends the moment a joint feels unstable, whatever reps are left; training stops on pain or swelling.** The abort decides the current set; the step gate (§2.6) decides the next dose. |
| R10 — Power work | **Power work is explosive in the lifting (concentric) phase only; its lowering follows R25.** No bounce, rebound or catch at end range. |
| R11 — Gated depth | **A joint's loaded flexion stays within the depth its loading stage allows, and so does the depth of any joint that would force it deeper in the same pattern.** Knee at stage 1 ⇒ hip depth is also capped, since squats and good mornings load both (RDL gives partial coverage). |
| R12 — Gated unilateral loading | **A joint takes unilateral loading — one limb working alone, moving or held, in any plane, against an external load, body weight or its own weight — only from loading stage 3** (D-31 · D-54). Walking, cycling and swimming, whose load passes from limb to limb every step or stroke, stay outside it. |
| R13 — Gated impact | **A joint takes plyometric or impact loading only from loading stage 4** (D-31). |
| R14 — Loading-stage unlock | **A joint unlocks one loading stage at a time, in the order of §2.5, and only when every exit criterion holds.** A flare returns it to the previous stage. A joint with no control test in §2.5 cannot meet exit criterion 2, so it stays at its loading stage until one is added. |
| R15 — Equipment | **Every exercise in every routine file, primary or alternative, is executable with the equipment and conditioning resources in §1.3** (D-30 · D-44). |
| R16 — Reps + RIR only | **Every prescription states sets × reps + RIR; load and effort are never programmed or tested by %1RM or RPE.** The load check (§2.2) is read, not tested. A timed hold states sets × hold time + seconds in reserve: the hold ends that many seconds before Harry expects to fail, each rep in reserve that R17 and R18 call for counting as ~4 s, a 3 s lowering and a 1 s lift (R25) (D-60). |
| R17 — Most RIR | **Where the block goal's row leaves a choice, the prescription takes the most RIR the row permits; hypertrophy from block week 5 is the exception (R18).** The row's values are a reference; the safer end for the joints is taken (D-33 · D-45). |
| R18 — Effort caps | **In weeks 1–4 of any block, every set ends at 2 RIR or more, whatever the row allows, and compounds stop short of failure in every goal.** `[HYP]` The hypertrophy RIR ranges are 2–3 for compounds and 1–2 for isolation: weeks 1–4 take their most (compounds 3, isolation 2), and from week 5 sets end at their least — compounds 2 RIR, isolation 1 RIR (D-45). A set counts only if it would have failed within the stated reps. |
| R19 — Session ceilings | **A session holds at most 8 fractional sets per muscle, and its exercise time — working sets and the rest between them — runs about 60 min and never past 75 min** (D-49). Warm-up sets and the mobility halves sit outside the exercise time. Both are ceilings with no per-session minimum, and neither is raised to fit a plan. |
| R20 — Session spacing | **Each region trains in at most 3 training sessions a week (§2.7), with at least 48 h between two sessions that train it. Two current routines that share no region — the only pair that can fall on consecutive days — never have a muscle that gets direct sets in one and collects sets in the other, and a training session on the day after another runs only if the step gate (§2.6) passed that morning for every joint both sessions load** (D-47 · D-50). The 48 h applies per region; Harry sets the days (§0.1). |
| R21 — Sport days | **Every routine names each sport with a profile (§1.2) whose "avoid the day before" muscles collect sets in it (§2.3), and that sport is not played the day after the routine. The day after a sport session, a training session runs only if the step gate (§2.6) passed that morning for every joint the sport loaded and the session will load** (D-51). |
| R22 — Restart ramp | **After a layoff of 3 weeks or more, working loads run at ≈60% of pre-layoff working loads in weeks 1–2, ≈80% in weeks 3–4 and 100% from week 5; progression starts after that.** Volume stays at the bottom of the range throughout. RIR is a ceiling on effort, not a target: RIR well above the row's range is expected in weeks 1–4 and is not a reason to add load. Load rises only when all prescribed reps complete inside the step gate (§2.6). Eccentric tempo: R25. |
| R23 — Left–right balance | **Training is left–right balanced: exercises are bilateral, or unilateral ones are done equally on each side** (D-07). |
| R24 — Suspended progression | **A block that excludes a region suspends the loading-gate progression of that region's joints, and the plan says so when the block is set.** The exit criteria need loading to evaluate. |
| R25 — Eccentric tempo | **The lowering (eccentric) phase of every loaded rep takes 2–3 s, in every goal** (D-32). Plyometric and impact reps are exempt; their landings stay under R10 and R13 (D-38). |

### Rule examples

Each rule passes when the implementation produces the *Pass* behaviour and fails when it produces the *Fail* behaviour. All values are illustrative. Fixture used below — the Current state of the `CLAUDE.md` example: focus block · upper and lower Hypertrophy · priority targets biceps, quads · block week 1 after a 2-month layoff · every joint at loading stage 1 · badminton in season · current routines: none yet. For R20–R21, Harry's week: full-body training Monday, Wednesday, Friday; badminton Sunday.

| Rule | Pass | Fail |
|---|---|---|
| R1 — preacher curl | Each rep turns ~70–80% into the available elbow range | Lowered to full elbow extension and held in the stretch |
| R2 — Smith squat; DB kickback | Each rep finishes with a soft knee bend; the kickback, heaviest at the end of elbow extension, keeps a soft elbow and is listed with its end-range warning | Knees locked out at the top; or the kickback listed without the warning |
| R3 — knee at stage 1 | Wall sit held above parallel | Wall sit held at parallel (knee at 90°) |
| R4 — lat pulldown | Returns to ~90–95% arm extension with the shoulder blades braced: the shoulders stay away from the ears | "Stretch at top": the stack pulls the shoulders up to the ears; or the elbows lock out |
| R5 — behind-the-torso curl | Behind-body curl on the cable (fixed line of pull) | Incline DB curl with the arms hanging free, listed without a warning |
| R6 — triceps overhead | Cable overhead extension, scapula braced | Standing overhead DB extension with the scapula unbraced while the cable option passes |
| R7 — cool-down | Active drills: shoulder CARs with both arms together, prone Y-T-W holds; tightness goes to foam rolling | 30 s static hamstring stretch; or a partner contract-relax (PNF) hamstring stretch |
| R8 — traps | Prone Y raise for lower and mid traps | Barbell shrugs for the upper trap |
| R9 — unstable knee | The knee feels unstable on rep 6 of 10 → the set ends at rep 6 | The remaining 4 reps are completed |
| R10 — Smith speed bench | Explosive press, 2–3 s lowering, no bounce off the chest | Bar dropped fast and bounced off the chest |
| R11 — hip at stage 2, knee at stage 1 | Smith squat stops above parallel, the knee's cap | Smith squat to full depth "because the hip is at stage 2" |
| R12 — every joint at stage 1 | Bilateral goblet squat; shoulder CARs with both arms together; band external rotation with both hands on one band | Bulgarian split squat with a 3 s lowering; or single-leg stance, a one-arm band external rotation or side-lying hip abduction |
| R13 — knee at stage 1 | No hops, jumps or landings in any session | Pogo hops (popliteus protocol Phase 3) programmed |
| R14 — knee unlock | Stage 1 → 2 after two consecutive clean step-gate weeks, 10 clean step-downs per leg and ≥90% symmetry | Stage 1 → 3 in one move; or 1 → 2 after a single clean week; or the shoulder unlocked while its dyskinesis test still shows obvious dyskinesis |
| R15 — equipment | Preacher curl on the adjustable bench with dumbbells; or 12 min on the bike | Leg extension machine (not in §1.3); or a rowing machine |
| R16 — prescription | 3 × 10–12, 2 RIR; or a week-1 wall sit (compound, 3 RIR) as 3 × 35 s with ~12 s in reserve | 3 × 10 at 70% 1RM; or 3 × 10 at RPE 8; or a wall sit held to failure |
| R17 — Smith squat, week 1 (compound, range 2–3 RIR) | 3 RIR | 2 RIR |
| R18 — weeks 1 and 5 | Week 1: preacher curl stops at 2 RIR, no compound set taken to failure. Week 5: preacher curl at 1 RIR, Smith squat at 2 RIR | Week 1: preacher curl taken to 1 RIR. Week 5: Smith squat taken to 1 RIR; or preacher curl kept at 2 RIR |
| R19 — Wednesday | Exercise time ≈35 min (18 working sets at 60–90 s rest); quads 6 fractional sets; or a strength session at 70 min | Exercise time 80 min; or quads 9 fractional sets |
| R20 — week | Full-body Monday, Wednesday, Friday; or upper and lower routines three times each, the erectors trained directly in the upper routine and collecting no sets in the lower one, each next-day session run after a passed morning step gate | Full-body Wednesday and Thursday; or a fourth lower session (a joint protocol on its own day counts); or back extensions in the upper routine while the lower routine's RDLs give the erectors indirect sets; or Tuesday's session run after a failed morning step gate |
| R21 — badminton Sunday | The full-body routine names badminton, since quads and glutes collect sets in it, and is not done Saturday; Monday's session runs after that morning's step gate passes for knees and ankles | The routine names no sport although its Smith squats train the quads; or it is done Saturday; or Monday's session runs despite knee swelling after Sunday |
| R22 — 2-month layoff | Weeks 1–2 ≈60%, weeks 3–4 ≈80%, week 5 100% of pre-layoff loads | Week 1 at pre-layoff loads; or load raised in week 2 because every set ended at 5 RIR |
| R23 — rows at loading stage 1 | Seated cable row with both arms | Single-arm rows for the draw arm only |
| R24 — next block trains upper only | The plan states "lower-body joints' progression suspended this block"; the knee stays at stage 1 | The knee moves to stage 2 during the upper-only block; or the suspension goes unstated |
| R25 — preacher curl | Each rep lowered in 2–3 s | Reps dropped in under 1 s |

---

## 4. Schemas

### 4.1 Current state — one per conversation

Set at the start of each conversation. A field with a default keeps it until Harry changes it; a field without one is asked before planning.

| Field | Definition |
|---|---|
| `block_type` | Focus or maintenance (§0.3). No default. |
| `block_goal` | One goal-table row (§2.2) for each region the block trains, upper and lower; a region the block does not train reads "not trained". The rows are offered as choices when asked. No default. |
| `priority_targets` | Focus block: muscles, not regions — the only muscles it programs (§0.3). Maintenance block: every muscle group (§2.1). No default. |
| `block_start` | Date; block week counts from it (§2.4). No default. |
| `block_week` | Derived from `block_start`. |
| `layoff` | Layoff before this block; 3 weeks or more triggers R22. Default: ~2 months. |
| `loading_stages` | Every joint's current loading stage (§2.5). Default: stage 1 for every joint, until R14 unlocks the next (D-28). |
| `in_season` | Each in-season sport, e.g. "badminton"; its days are Harry's to set (§0.1). No default. |
| `current_routines` | The routine files in use, each with the regions it trains and its training sessions per week (§2.7). Every new or edited routine is built against them (D-48). No default. |

Invariants: one goal per trained region (§0.3); every priority target is a muscle of a trained region; every in-season sport has a profile (§1.2); every joint has a loading stage; across the current routines, no region exceeds 3 training sessions a week (R20).

### 4.2 Sport profile — one per sport

| Field | Definition |
|---|---|
| `demand` | Muscles the sport relies on, grouped by region (§2.1). |
| `avoid_day_before` | Muscles not to fatigue the day before a session of the sport (R21). |
| `carryover` | Qualities whose training carries over to the sport; read by the Stage 1 sport filter. |
| `loads` | Joints and tissues the sport loads; read by R21 and the Stage 1 sport filter. |

Invariant: all four fields are filled; their evidence and grades go to Supplement §5.5.

---

## 5. Open items

None.
