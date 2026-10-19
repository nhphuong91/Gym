# Stage 0 — Supplement Info

**Non-normative.** Companion to `Stage0_PolicyDefinition.md`: terminology, architecture history, decision log, rejected alternatives, corpus evidence, deferred material and references.
Where the two documents disagree, the Policy Definition governs. `[W#]` → §7 References. The corpus is the routine files in the Gym folder's `gymplan/`, read in place (D-17).
Section numbers found only here (§5.1–§5.6, §6, §7) refer to this Supplement; every other § and every R-number refers to the Policy Definition.

---

## 1. Terminology

| Term | Meaning in this project | Formerly |
|---|---|---|
| Stage (0, 1, 2) | A design stage of this specification: 0 Policy Definition, 1 Programming, 2 Routine Files | — |
| Loading stage | One of the four steps of the loading gate: partial range bilateral → full range bilateral → unilateral → plyometric/impact (§2.5) | "§R1 stage", "stage"; step 3 was "unilateral eccentric" until D-54 |
| Unilateral loading | One limb working alone — moving or held, in any plane, against an external load, body weight or its own weight; open from loading stage 3 (R12 · D-54). Walking, cycling and swimming pass the load from limb to limb and stay outside it | "unilateral eccentric loading through its flexion–extension cycle" (D-31) |
| End-range warning | The warning an exercise carries when its resistance peaks at the end of a joint's range, the soft bend its only margin (R2 · D-55) | — |
| Seconds in reserve | For a timed hold: the seconds left before failure when the hold ends; each rep in reserve counts as ~4 s (R16 · D-60) | — |
| Loading gate | Staged loading for every joint (§2.5 · R11–R14 · R24 · D-28) | `<gates>`, "staged-loading gate" (flagged joints only, before D-28) |
| Joint's loading stage | Every joint's current step on the loading gate, kept in Current state `loading_stages` (§4.1) | "flagged joint", "gated joint" (only flagged joints were staged before D-28) |
| Exit criteria | The three conditions that unlock the next loading stage (§2.5 · R14) | reference.md §R1 |
| Control test · symmetry test | The per-joint tests behind exit criteria 2 and 3 (§2.5); like the range readings, tests, not training sets (D-85) | — |
| Available range | A joint's own measured active range; for the spine, the smaller of his own and the healthy mean (R1 · D-69) | — |
| Step gate | The four-element symptom check every progression step passes (§2.6) | — |
| Flare | Any failed element of the step gate | — |
| In-session abort | Skipping a session, ending a set or stopping training within a session (R9); it decides the current set, not the next dose | — |
| Hard gates | Equipment (R15), safety constraints (R1–R10) and the loading gate (R11–R14) | `<equipment>`, `<constraints>`, `<gates>` |
| Selection criteria | The five ranked criteria that choose among exercises passing the hard gates (§0.2) | "conflict order" |
| Goal-fit test | A per-goal way to score how well an exercise suits the block goal: selection criterion 3 (§0.2; tests written in Stage 1, D-36) | "selection criterion" (D-05) |
| Joint-control limits | R18–R22: limits set by joint control, never raised to fit a plan; R19's exercise time is Harry's own cap, held the same way (D-49) | "joint-control limits" (session ceilings only) |
| Current state | The per-block input record (§4.1) | `<athlete>` Current state |
| Block · block week | The weeks one goal set stays in force, and the count from its start (§2.4) | "weeks a routine or set/rep scheme stays unchanged" (CLAUDE_old.md `<dosing>`) |
| Region | Upper body, trunk included, or lower body (§2.1) | — |
| Muscle group | One of the seven groups in §2.1 — upper: abs & obliques, back, chest & shoulders, arms & hands; lower: hips & gluteals, thighs, calves & shins | — |
| Focus block | A block that programs only its priority targets (§0.3) | — |
| Maintenance block | A separate block whose main focus is keeping every muscle group activated during a fat-loss period (§0.3) | "maintenance targets", a later phase (CLAUDE_old.md `<dosing>`) |
| Priority targets | The muscles a focus block programs (§4.1) | — |
| Working, direct and indirect set · fractional sets | Set units (§2.3) | — |
| Harvest | The sets a muscle collects from exercises in which it is not the prime mover: 0.5 × indirect sets, counted in fractional sets (§2.3). It covers every muscle an exercise loads beyond its prime mover, unlisted and non-focused muscles included. Used on purpose, it gets another priority target enough sets; on an unlisted muscle it is incidental and has no target (§0.3) | "harvest" (CLAUDE_old.md `<dosing>`) |
| Reps · session sets · weekly sets | The volume counting chain: reps per set → a muscle's sets per session → its weekly sets, the session sets summed over the week (§2.3 · §0.3) | — |
| Carryover | A quality that, trained in the gym, transfers to a sport's performance or resilience; listed per sport in §1.2 and favoured by the Stage 1 sport filter. E.g. isometric holds at shoulder height carry over to holding full draw in archery | — |
| RIR · RM | Reps in reserve: reps left before failure when a set ends. RM = reps + RIR (§2.2) | — |
| Station | A one-of-a-kind equipment unit, unavailable while in use (§1.3) | — |
| Conditioning resources | The court, bike, pool and jump rope listed in §1.3; their exercises pass the hard gates like any other (R15 · D-44) | "court and cardio sessions", outside the list (D-30) |
| Training session | Any session of resistance work — weights, cables, bands, bodyweight or a joint protocol; it counts toward every region whose muscles get direct sets in it, and its mobility halves belong to it (§2.7 · D-47 · D-50) | "lifting session" (CLAUDE_old.md `<dosing>`) |
| Exercise time | A session's working sets and the rest between them, warm-up sets and mobility halves excluded: about 60 min, never past 75 (R19 · D-49) | "≤28 working sets per session" (CLAUDE_old.md `<dosing>`) |
| Sport note | The note in a routine naming each sport not to be played the day after it — those whose "avoid the day before" muscles collect sets in it (R21 · D-51) | "the day before skips work that fatigues…" (CLAUDE_old.md `<dosing>`) |
| Current routines | The routine files in use, each with its regions and training sessions per week; every new or edited routine is built against them (§4.1 · D-48) | — |
| Braced scapula | The shoulder blade held by its own muscles where the arm has taken it, not hanging on the joint capsule. At the top of a pull it has turned upward with the arm overhead — normal, and not fought — and it is never pulled up toward the ears. A hold, not an added movement (R4 · R6 · D-42) | "active scapular depression" (CLAUDE_old.md `<constraints>` 4) |
| Active drill | A movement or hold made by the muscles crossing the joint, inside the range they control; nothing external pushes it further and nothing bounces (R7 · D-43). Includes CARs, controlled dynamic drills, isometric holds (at long muscle length too) and static-active holds; excludes static-passive, PNF and ballistic stretching | "active drills only" (CLAUDE_old.md `<constraints>` 7) |
| Static-passive · static-active · PNF · ballistic | Stretching methods [W60]: an external force (partner, strap, gravity, body weight) holds the end position while the muscle relaxes · the opposing muscles alone hold the end position · the stretched muscle contracts at end range, relaxes, and is taken further (contract-relax, hold-relax; in CRAC the opposing muscle pulls it further) · bouncing at end range | — |
| Implementation | The plans and routine files built under this specification | — |
| Corpus | The routine files in `gymplan/` (§5.1) | "routine files" |
| Owner | Harry, who decides every Open item | — |
| Spec round · routine request | The two task modes in `CLAUDE.md` `<task>` | — |

---

## 2. Architecture history

### 2.1 From CLAUDE_old.md + reference.md to the scaffold

| Removed | Replaced by | Why |
|---|---|---|
| CLAUDE_old.md as the single instruction file | `CLAUDE.md` (how the AI works) + stage docs (what binds) | The scaffold keeps the working method apart from the binding rules |
| reference.md (evidence, rationale, format examples, tooling, decision log) | Stage Supplements, non-normative | What binds stays apart from what explains |
| `<role>` first paragraph | `CLAUDE.md` `<role>` · §0.1 (goal- and sport-agnostic) | Layer 1, plus one stance |
| `<role>` hard gates and conflict order | §0.2 | Stances; the rules they rank are R1–R15 |
| `<role>` paragraph on how the two files divide the work, incl. "every § reachable from at least one rule" | `<stage_doc_spec>`; every evidence row names what it informs (§5.2–§5.6) | The two-file stage pair and the "Informs" column do the same job |
| `<athlete>` profile, sport profiles, Current state; `<dosing>` opening line | §1.1 · §1.2 · §4.1 · §4.2 | Domain items and the per-block input record |
| `<equipment>` | §1.3 · R15 | Domain items plus one testable rule |
| `<constraints>` intro and items 1–10 | §0.1 · R1–R10, numbers kept | Behaviour gets R-numbers; the same numbers keep old citations traceable |
| `<gates>` items 1–3 | R11–R13 | Same |
| reference.md §R1 (unlock order, exit criteria, control tests) | §2.5 · R14 ✏️ | It binds, so it leaves the explanatory file |
| `<dosing>` goal table, reps + RIR lines, Effort, set units, block definition | §2.2 · R16–R18 · §2.3 · §2.4 | Shared by every stage; Current state selects goal rows |
| `<dosing>` per-session caps, 48 h schedule, sport days, restart ramp, step gate | R19–R22 · §2.6 | Joint-control limits bind Stage 1 from above (D-21) |
| `<dosing>` Focus block | §0.3 (stance) · Stage 1 (rules, §6) | Stance now, behaviour with programming |
| `<programming>`, the rest of `<dosing>`, `<output>`, plan checks in `<verification>` | Stage 1 (§6) | Strict rounds (D-19) |
| `<files>`, `<workflow>` 3–4, the file check in `<verification>`, reference.md §R4 | Stage 2 (§6) | Strict rounds (D-19) |
| `<workflow>` 1, 2, 5 | `CLAUDE.md` `<task>`, routine request ✏️ | How the AI works belongs to layer 1 |
| reference.md §R3 format examples | `CLAUDE.md` `<example>` · Stage 1 (§6) | One example reused everywhere |
| reference.md §R5 rationale | §5.6 (Stage 0 lines) · Stages 1–2 (§6) ✏️ | The skeleton has no rationale slot |
| reference.md §R6, §R7 evidence | §5.4 · §5.5 · Stage 1 (§6) | Each evidence row names the rule it informs |
| reference.md §R8 log (D, X, P) | Decision log (D-01…D-15) · Rejected alternatives (X1–X3) · §6 (P1–P6; P7 closed by D-25) | Decision protocol; numbers kept |
| "§R1 stage" | "loading stage" ✏️ | Clash with the design Stages (D-34) |
| Staging for flagged joints only (`<gates>`; Current state `gated_joints`) | Staging for every joint, each with its own loading stage (§0.1 · §2.5 · §4.1 `loading_stages`) | D-28 |
| "Conflict order" (`<role>`) | "Selection criteria", with the planning order ahead of them (§0.2 · §0.3) | Harry: goal → muscles → volume → exercises chosen by five criteria (D-35) |
| Eccentric tempo inside the restart ramp (`<dosing>`; R22) | Its own rule, R25 | D-32 |
| Isolation to 0–1 RIR after 4 flare-free weeks (`<dosing>` Effort; R18) | Removed | Joint safety wins; the goal table's values are a reference (D-33) |
| Block = weeks a routine or set/rep scheme stays unchanged (`<dosing>`) | Block = weeks one goal set stays in force (§2.4) | Every progression step would have ended the block and restarted R18's weeks 1–4 (D-40) |
| §0.4 (a)–(d) of the first draft | (a) R14 detail · (b) R24 · (c) §5.6 · (d) §5.5 | Harry: none were limits, some were rules (D-24) |
| "Maintenance targets for all muscles, once the focus blocks are complete" (CLAUDE_old.md `<dosing>`; reference.md §R5) | Maintenance block, a separate block type for fat-loss periods (§0.3) | D-23 |
| "Active scapular depression" at the top of pulldowns and pull-ups (`<constraints>` 4) | Shoulder blades braced at the top (R4) | Harry asked whether it meant bracing or moving: it is a hold (D-42) |
| "No passive/static stretching" (`<constraints>` 7) | Active drills defined; static-passive, PNF and ballistic named; clinician override (R7 · §0.1) | D-43 |
| Court and cardio outside the equipment list (D-30) | Conditioning resources in §1.3; R15 covers every routine file | D-44 |
| Hypertrophy from week 5 at compounds 2–3 and isolation 1–2 RIR, read at the most RIR (`<dosing>` Effort + "take the most RIR it permits") | At the least: compounds 2, isolation 1 (R18) | D-45 |
| Lifting never on consecutive days, 3 sessions a week, pattern lift / rest / lift / rest / lift / rest / rest (`<dosing>`) | Each region ≤3 training sessions a week, 48 h apart; regions may run on consecutive days; per-muscle and step-gate guards (R20 · §2.7) | D-47 |
| Sport on rest days only; plans set the days (`<dosing>`) | Harry schedules every session; routines carry no days (§0.1 · §4.1 `current_routines`) | D-48 |
| ≤28 working sets per session (`<dosing>`) | Exercise time about 60 min, never past 75 (R19) | Harry: 28 was the result of his time cap (D-49) |
| Per-muscle guard on consecutive days (D-47) | Schedule-proof check across routines that share no region (R20) | Harry sets the days, so the check must hold for any order (D-50) |
| The day before a sport skips work that fatigues its "avoid the day before" muscles (`<dosing>`) | A sport note in every routine (R21) | Harry places the routines himself (D-51) |
| Cardio routine — "court and conditioning", hand-laid (CLAUDE_old.md file roles) | Routine work under the hard gates, court drills and games included (§5.2) | Its goal is like a gym session's (D-52) |

### 2.2 Gym adaptations to the scaffold (✏️, kept by D-34)

| # | Adaptation | Where | Why |
|---|---|---|---|
| 1 | A second `<task>` mode for routine requests | `CLAUDE.md` `<task>` | The Gym's AI also builds plans and files, not only spec docs |
| 2 | Corpus evidence widened: routine-file observations and measurements, training evidence, sport evidence graded A/B/C/H, reasoning | §5.1–§5.6 · `<stage_doc_spec>` item 2 | reference.md's graded evidence (§R7) and rationale (§R5) have no slot in the skeleton |
| 3 | A rule says what happens, keeps a prohibition only where no positive form exists, and may carry its reason in one clause | `<stage_doc_spec>` item 1 | Keeps D-06 (say what to do, give the reason) while longer justification stays here |
| 4 | Pre-scaffold decisions imported and numbered continuously, each naming its reference.md ID; decisions never recorded are out (D-39) | Decision log | Traceability to reference.md §R8 |
| 5 | Corpus read in place, no `SampleFile/` copy; no seed-data file yet | `<context>` · §5.1 | Copies drift (D-12); seed data waits for Stage 1 (D-18) |
| 6 | "Joint-control limits" widened from the session ceilings to R18–R22 | Terminology · D-21 | Names the group D-21 keeps in Stage 0 |
| 7 | "§R1 stage" renamed "loading stage" | Both docs · `<context>` | Clash with the design Stages |
| 8 | The Stage 0 header carries a variant legend (`[HYP]`) | Policy Definition header | R18 holds hypertrophy-specific text |
| 9 | Decisions taken in chat are logged with the chat question they close ("chat Q1") | Decision log | They closed questions asked before any Open item existed |

---

## 3. Decision log — closed open items

Log IDs are local to Stage 0; each row names the OI it closes, and OI numbers restart after each cleared round, so rows from D-42 on carry the round beside the OI: round 6 opened 2026-10-01 (closed by D-42…D-48), round 7 and round 8 on 2026-10-02. D-54…D-58 record Harry's answers to the exercise catalogue's readings (`ExerciseCatalogue.md` §5; chat, 2026-10-03), triggered by Stage 1; D-58 opened round 9 and D-60 closed it; D-59 confirms Claude's reading in D-54. Round 10 (ankle and hip control tests) opened 2026-10-03; D-61 · D-62 closed it. Round 11 (shoulder, elbow, wrist and spine; criterion 3 for the arm; range for hypermobile joints) opened the same day and was revised on 2026-10-04 after a second research pass; D-63…D-69 closed it. D-70 (chat, 2026-10-06) swaps R12's pass example after the catalogue's A9, triggered by Stage 1. D-71 · D-72 (chat, 2026-10-06) set the arm tests' paces and a self-filmed low-back range, raised while building the upper-body evaluation routine. D-73 · D-74 (chat, 2026-10-06) keep one prompt file, CLAUDE.md, and restate the rulebook for routine work, superseding D-20; D-75 · D-76 put routine work on Stages 0–1 as drafted until the freeze and add three more interim file rules. D-77…D-79 (chat, 2026-10-07) read every test angle from tripod video, put moving pictures on routine cards and link demonstration videos, raised by Harry on the upper-body evaluation routine. D-80…D-82 (chat, 2026-10-08) set the knee's symmetry test, a 2-session mean for the legs and the paces of the leg symmetry tests, raised while building the lower-body evaluation routine. D-83 (chat, 2026-10-08) keeps a two-column copy of the upper-body evaluation as a one-off. D-84 · D-85 (chat, 2026-10-09) set the paces of the knee and hip control tests and make every §2.5 test a test, not a training set, raised in a review of the lower-body evaluation routine; D-86 (chat, 2026-10-09) renumbers reference.md §R8. D-88 (chat, 2026-10-15), triggered by Stage 2, moves each routine's sessions per week from the routine files to the Stage 2 register (Stage 2 D-05 · D-08). Amendments made after the freeze are logged here too, naming the triggering stage. The freeze itself is a row. D-01…D-15 are imported from reference.md §R8 and numbered continuously; each names its reference.md ID, the same number since D-86. Decisions never recorded there (its former D3–D44) are out (D-39). D-16 onward were taken in this conversion.

| # | Question | Decision | Lands in |
|---|---|---|---|
| D-01 | Step-gate pain ceiling (reference.md D1) | ≤5/10 during and after. Why: the ceiling HSD patients tolerated in Liaghat's high-load trial [W12] | §2.6 |
| D-02 | Hip abductor/adductor machine (reference.md D2) | Programmed when it passes the constraints and the gates. Why: not recorded | §0.2 (hard gates; its §1.3 detail was removed, D-25) |
| D-03 | Goals across regions (reference.md D3) | One goal per region per block; every muscle in a region follows it. Why: mixing goals between close muscles is hard to plan and execute; an upper/lower split is not (Harry, Sep 2026) | §0.3 · §4.1 |
| D-04 | Region of the trunk (reference.md D4) | Trunk (abs, obliques, spinal erectors) counts as upper body. Why: not recorded | §2.1 |
| D-05 | Meaning of conflict-order priority 3 (reference.md D5) | Goal fit, judged on a per-goal selection criterion; "stimulus" means growth stimulus only. Why: "stimulus quality" would rank power or endurance blocks on growth; "specificity" reads as sport specificity, which is priority 5 | §0.2 · D-36 |
| D-06 | Rule wording (reference.md D6) | Rules say what to do and give their reason; hard gates carry no "never"; research is part of the role; reference sections are §R1–R8. Why: Anthropic's prompting guidance — state what to do, give the reason, drop forceful emphasis [W1]. The §R1–R8 part is superseded by D-16 | `CLAUDE.md` `<role>`, `<stage_doc_spec>` · §3 |
| D-07 | Left–right balance (reference.md D7) | Bilateral exercises, or unilateral ones done equally on each side. Why: not recorded | R23 |
| D-08 | Slimming `<athlete>` (reference.md D8) | Stats in the first line; bodyweight, Standing aims and nutrition removed; conversation-start timing only in `<athlete>`; profiles list muscles by region; Current state adds block start, layoff, and in-season sports + days with no default. Why: no rule read bodyweight; aims and timing duplicated `<role>`; nutrition is out of scope | §0.1 · §1.1 · §1.2 · §4.1 |
| D-09 | Stations (reference.md D9) | Smith, cable (high and low pulleys), hip abductor/adductor machine and adjustable bench are one each, independent, and unavailable while in use; bands, frame, barbells and dumbbells are always available. Why: with one of each, any station — the bench included — can be occupied | §1.3 · R15 |
| D-10 | Load steps (reference.md D10) | Harry manages load steps; a plan states an exact step only when a source gives one. Why: not recorded | Stage 1 (§6) |
| D-11 | Mobility routines (reference.md D11) | Pre and post halves with active drills only; a change to one routine updates every routine that references it. Why: static stretching is banned (R7); routines cite each other, so a partial update leaves stale citations. Its type-and-role file identification is replaced by D-12 | R7 · Stage 2 (§6) |
| D-12 | Workspace (reference.md D12) | The Gym folder on Harry's computer is the workspace: fixed paths; work and run the generator there, the cloud only for steps the computer lacks; working copies in scratch outside the folder; roles table with a build column. Why: the subfolders are fixed (checked 26 Sep); a cloud round-trip per edit is slow and leaves copies that drift | Stage 2 (§6) |
| D-13 | .txt mirror (reference.md D13) | Written with every SVG write; read only when files are attached. Why: SVGs are readable in place; the mirror keeps a fallback for attaching files | Stage 2 (§6) |
| D-14 | `gympdf/` (reference.md D14) | Harry's; left untouched. Why: Harry exports and checks the PDFs himself | §0.1 |
| D-15 | Cross-file references (reference.md D15) | Exercises cited by number with the name beside it, mobility items by ID; dependents found by searching the name or ID. Why: Harry prefers numbers for ease; the name keeps citations findable after a renumber (all 8 foam-rolling numbers had gone stale) | Stage 2 (§6) |
| D-16 | Stage layout (chat Q1, 2026-09-29) | Three stages: 0 Policy Definition · 1 Programming (Current state → Plan) · 2 Routine Files (Plan → SVG + .txt). Supersedes the §R1–R8 part of D-06 | `CLAUDE.md` `<stages>` · Architecture history |
| D-17 | Folder (chat Q2 and brief L7, 2026-09-29) | The scaffold docs live in `gymspec/` inside the Gym folder; the corpus stays in `gymplan/` and is read in place | `CLAUDE.md` `<context>` · §5.1 |
| D-18 | Seed data (chat Q3, 2026-09-29) | None for now; added when Stage 1 needs it | §6 |
| D-19 | Delivery (chat Q4, 2026-09-29) | Strict rounds: `CLAUDE.md` and the Stage 0 pair first, then a stop for Harry's decisions; Stages 1–2 follow in later rounds, their material parked in §6 meanwhile | Architecture history · §6 |
| D-20 | Rulebook for routine work until the freeze (O1) | A: CLAUDE_old.md + reference.md govern plans and file edits until Stages 0–2 are all frozen; these docs govern spec rounds only. Superseded by D-74: on 2026-10-03 the rulebook was renamed CLAUDE_old.md, now history only, and CLAUDE.md became this project prompt | `CLAUDE.md` `<task>` |
| D-21 | Home of the joint-control limits (O2) | A: R18–R22 stay in Stage 0 | §3 |
| D-22 | Focus blocks and harvest (chat 2026-09-29, Q6) | Any exercise whose prime mover is a priority target is eligible; those that load other muscles least are preferred, unless the extra load is harvest used on purpose to get another priority target enough sets. Work that lands on unlisted or non-focused muscles is also harvest: incidental, with no target | §0.3 · §2.3 |
| D-23 | Maintenance (chat 2026-09-29) | A maintenance block is a separate block whose main focus is keeping every muscle group activated during a fat-loss period; it replaces "maintenance targets once the focus blocks are complete". Current state gains `block_type` | §0.1 · §0.3 · §4.1 · §6 |
| D-24 | Accepted limits (chat 2026-09-29) | The first draft's (a)–(d) were not limits: (a) → R14 detail, (b) → R24, (c) → §5.6, (d) → §5.5. §0.4 rewritten with four genuine limits, drafted by Claude on Harry's instruction | §0.4 · R14 · R24 |
| D-25 | Cable machine and hip machine (Harry's edit of §1.3, 2026-09-29; closes P7) | The cable machine executes rows, pulldowns, pullover, curl, pushdown and overhead extension; lateral raise, external rotation and reverse fly left the list. The hip machine's detail was removed: the hard gates cover every station (D-02) | §1.3 |
| D-26 | Muscle groups (Harry's edit of §2.1, 2026-09-29) | Upper body, trunk included: abs & obliques, back, chest & shoulders, arms & hands. Lower body: hips & gluteals, thighs, calves & shins. Why: not recorded | §2.1 |
| D-27 | Volume counting (chat 2026-09-29; checked against §5.4) | Reps per set → sets per session → weekly sets per muscle; weekly sets are what targets count, and sessions split them freely within R19–R20. Checked: the free split holds for hypertrophy; strength does better spread over sessions. The unit of the goal table's Sets column stays open (O10) | §0.3 · §2.3 |
| D-28 | Scope of staged loading (O9) | B: every joint is staged, all the time. Current state keeps each joint's loading stage (`loading_stages`); every joint starts at stage 1 and unlocks through R14. Harry accepted that joints without a control test stay at stage 1 | §0.1 · §0.4 (e) · §2.5 · R3 · R11–R14 · R24 · §4.1 |
| D-29 | Unit of the goal table's Sets (O10) | A, as Harry put it: the NSCA's sets are per exercise and also apply to each muscle through its exercise — sets per exercise per session, for the exercise's target muscle. Which goals carry a weekly target → Stage 1 | §2.2 · §0.3 |
| D-30 | Equipment scope (O4) | A: R15 covers gym work; court and cardio sessions sit outside §1.3. Harry has a foam roller, a tennis ball and a low step or box (5–20 cm), now "always available"; he has no EZ-bar (chat Q7). Scope superseded by D-44; the equipment items stand | §1.3 · R15 |
| D-31 | Reading of the gate rules (O5) | A: R12 lifts at loading stage 3 and R13 at stage 4 | R12 · R13 |
| D-32 | Eccentric tempo (O6) | A: every loaded rep lowers in 2–3 s, in every goal — its own rule, R25; R10 and R22 point to it | R25 · R10 · R22 |
| D-33 | R17 vs R18 (O7) | Harry: prefer what is safer for the joints; the goal table's values are a reference. R17 governs — the safer end of the row, the most RIR it permits — and R18's step to 0–1 RIR for isolation is dropped. Superseded in part by D-45: hypertrophy from block week 5 | R17 · R18 · §2.2 |
| D-34 | Gym adaptations to the scaffold (O8) | A: all kept, including "loading stage" | §2.2 of this Supplement |
| D-35 | Planning order and selection criteria (Harry's comment on O3) | Planning runs training goal → target muscle groups → training volume → exercises; exercises are then chosen by the five criteria of §0.2, renamed from "conflict order". O3 stayed open for the goal-fit tests (closed by D-36) | §0.2 · §0.3 |
| D-36 | Where the goal-fit tests are written (O3) | A: in Stage 1, beside exercise selection. Hypertrophy's test is lengthened work first with L + M/S coverage (CLAUDE_old.md `<programming>`); strength, power, muscular-endurance and general-fitness tests need research in that round | §0.2 · §6 |
| D-37 | Partial range for joints without a test line (O11) | A: until a joint's line in §2.5 defines it, its partial range is R1's range — peak tension at ~70–80% of available range, short of end range | §2.5 |
| D-38 | Eccentric tempo vs plyometric and impact reps (O12) | A: plyometric and impact reps are exempt from R25; their landings stay under R10 and R13 | R25 |
| D-39 | Decision-log numbering (Harry, 2026-09-30) | Decisions never recorded (reference.md's former D3–D44) are out and the log is numbered continuously; each imported row names its reference.md ID. T1, the backfill, is withdrawn | Decision log · §6 |
| D-40 | Definition of a block (chat 2026-09-30) | A block is the run of weeks one goal set stays in force — block type, goal row per region, priority targets. Routines, volume, sets and reps derive from it top-down and progress inside it; it ends when the goal changes (target reached or replaced, injury, etc.). Replaces "weeks a routine or set/rep scheme stays unchanged" | §2.4 |
| D-41 | Links in References (chat 2026-09-30) | Every reference carries a link (DOI, PubMed or publisher page); a source that cannot be identified is marked, not dropped | §7 |
| D-42 | R4 scapula cue (O1, round 6) | B, worded on Harry's question "bracing or moving?": at the top the shoulder blades are braced — held by muscle where the arm has taken them, never pulled up toward the ears or left hanging. Bracing is a hold, not an added movement; the shoulder blade's upward turn with the arm overhead is normal and is not fought | R4 · Terminology (Braced scapula) |
| D-43 | Mobility (O2, round 6) | B: R7 defines active drills — movements and holds made by the muscles crossing the joint, inside the range they control, nothing external pushing further, no bounce; static-passive, PNF and ballistic stretching are not programmed, static-active holds are active drills. A treating clinician's stretching prescription overrides R7 for the muscle it names | R7 · §0.1 · Terminology |
| D-44 | Conditioning resources (O3, round 6) | B: §1.3 lists the badminton court, a bike (stationary or outdoor), a pool and a jump rope, all available; R15 covers every exercise in every routine file. The hard gates now bind conditioning: jump rope and court footwork are impact (R13), lunging drills unilateral eccentric (R12). Supersedes D-30's scope | §1.3 · R15 |
| D-45 | Hypertrophy RIR (O4, round 6) | B: from block week 5, hypertrophy compounds end at 2 RIR and isolation at 1 RIR, the least of their ranges; weeks 1–4 are unchanged (compounds 3, isolation 2); every other goal keeps the most RIR its row permits. Why: growth rises linearly closer to failure, most at light loads, and RIR is under-called by ~1 rep; strength gains don't depend on it and power prefers distance from failure (§5.4). Supersedes D-33 for hypertrophy from week 5 | R17 · R18 · §2.2 · §0.4 (a) |
| D-46 | R19 total ceiling (O5, round 6) | A: at most 28 working sets per session, all muscles combined. Origin (Harry): he caps a session at ~1 h, and 28 sets fill about an hour at hypertrophy rest. Superseded by D-49: 28 was the result of the time cap, not a cap of its own, and is dropped | R19 · §5.6 |
| D-47 | Session spacing (O6, round 6) | C: a training session is any session of resistance work and counts toward every region it trains; each region trains at most 3 times a week, 48 h apart; regions may fall on consecutive days; no muscle collects sets on consecutive days when either day gives it direct sets; a session the day after another runs only after a passed morning step gate for every joint both load | R20 · §2.7 · §0.3 Volume · §0.4 (a) · R21 |
| D-48 | Scheduling (O7, round 6) | Harry's own answer: he decides the sport days and how training sessions interleave; the AI builds routines, assigns no days, and keeps track of the current routines (Current state `current_routines`). Replaces R20's weekly pattern and "sport on rest days only" | §0.1 · R20 · §4.1 · `CLAUDE.md` `<task>`, `<example>` |
| D-49 | Session time (O1, round 7) | A, as Harry set it: a session's exercise time — working sets and the rest between them — runs about 60 min and never past 75 min (1 h, at most 15 min more); warm-up sets and the mobility halves sit outside it. The 28-working-set ceiling was the result of this time cap, not a cap of its own, and is dropped (supersedes D-46). Stage 1 sets how minutes are estimated | R19 · §2.3 · §6 |
| D-50 | Per-muscle guard under Harry's scheduling (O2, round 7) | B: schedule-proof — two current routines that share no region, the only pair that can fall on consecutive days, never have a muscle that gets direct sets in one and collects sets in the other; any order Harry picks then passes. A session trains a region when that region's muscles get direct sets in it | R20 · §2.7 |
| D-51 | Sport note (O3, round 7) | B, as Harry put it: every routine carries a note naming each sport he should not play the day after that session. A sport is named when muscles on its "avoid the day before" list collect sets in the routine; every sport with a profile is checked, so the note survives season changes (Claude's reading, open to change). R21's day-after-sport step gate stays | R21 · §0.1 · Stage 2 (§6) |
| D-52 | Court work in the cardio routine (O4, round 7) | Harry: activities inside a sport session are not counted; the cardio routine is not a sport session — its goal is like a gym session's, preparing him for his sports. So the cardio routine is routine work, and every exercise in it, court drills, rallies and games included, passes the hard gates (B in effect) | §5.2 · R12 · R13 · R15 · §6 |
| D-53 | Conditioning sessions and R20 (O1, round 8) | Harry: the cardio session is a separate session he builds into his week and applies flexibly, at times dropping one of the week's gym sessions to make room. C in effect: conditioning sessions stay outside R20; their exercises still pass the hard gates (D-52), and a week with a swapped gym session is an accepted limit. Claude reads "build" as fitting the session into his week; the cardio routine file is still built under the spec on request | §2.7 · R20 · §0.4 (f) |
| D-54 | Unilateral loading (catalogue Q1 · A1; triggered by Stage 1) | Harry: "count also" — limb-weight-only work, rotation, side-to-side work and holds count, as well as one limb lowering a load. R12 gates every exercise in which one limb works alone, moving or held, in any plane, against an external load, body weight or its own weight; loading stage 3 is renamed "unilateral". Claude reads walking, cycling and swimming as outside R12 — their load passes from limb to limb every step or stroke, with no impact, and R15's pass example programs the bike — open to change. Consequence: until joints other than the knee get control tests, single-leg stance, hip CARs on one leg, clamshells, side-lying hip work, Copenhagen and side planks, one-arm band work and the dead bug stay out; drills that can run with both limbs together (shoulder, wrist and ankle CARs, band external rotation with one band) stay in | R12 · §2.5 · §0.4 (e) · R7 and R12 examples |
| D-55 | End-range peak (catalogue Q2 · A3) | Harry: an exercise whose load peaks at the end of a joint's range is not excluded; it carries a warning. R2 adds the end-range warning; the DB kickback returns with it, and Stage 1 R27 still gives the triceps no S | R2 · R2 example |
| D-56 | 'Glutes' in badminton's avoid-the-day-before row (catalogue Q3 · A4) | Harry confirmed: glute max and glute med, as the badminton demand row names both | §1.2 |
| D-57 | Knee depth outside squat patterns (catalogue Q4 · A5) | Harry confirmed: "above parallel" caps the knee's loaded flexion at about 90°; a knee held static at about 90° or less while the load works elsewhere, or bent deepest where the load is lightest, stays inside loading stage 1 | §2.5 |
| D-58 | Timed isometric holds (catalogue A2) | Harry: allow them as hypertrophy sets for every muscle, not only forearm and abs isolation. How a hold states its effort is open (O1, round 9) | §2.2 · §5 |
| D-59 | Walking, cycling and swimming under R12 (catalogue Q7, chat 2026-10-03) | Harry confirmed Claude's reading in D-54: they stay outside R12, since their load passes from limb to limb every step or stroke | R12 |
| D-60 | Effort for a timed hold (O1, round 9) | A: a hold states sets × hold time + seconds in reserve — it ends that many seconds before Harry expects to fail — and each rep in reserve that R17 and R18 call for counts as ~4 s, one rep's time under R25 (Claude's conversion, open to change). Self-assessed like RIR (§0.4 (b)); keeps one effort scale | R16 · R16 example |
| D-61 | Ankle control test (O1, round 10) | A: per leg, 10 single-leg heel raises at 60 beats a minute with fingertip support, full height every rep, no inversion or eversion wobble, no pain; then a 30 s single-leg stance, eyes open, arms crossed. Partial range: ~70–80% of the knee-to-wall lunge range. Symmetry test: heel raises to technical failure. Mirrors the knee test — a count, a quality check, no pain | §2.5 |
| D-62 | Hip control test (O2, round 10) | A: per leg, 5 slow single-leg squats to ~60° of knee bend, filmed from the front, "good" on all five of Crossley's criteria. Partial range: R1's range. Symmetry test: single-leg bridges to technical failure, heel on the bench. Claude added "no pain", as the knee and ankle tests have it (open to change) | §2.5 |
| D-63 | Shoulder control test (O1, round 11) | A: the scapular dyskinesis test as documented in full, passed against an unloaded set; partial range from Watson's programme — elevation ~75%, external rotation to the smaller of 45° and ~75%, extension to neutral; symmetry by ExtRA abduction with a soft elbow (an unvalidated change) | §2.5 |
| D-64 | Elbow control test (O2, round 11) | A: kneeling push-ups on handles plus a 30 s one-arm hold, clean when no rep or hold reaches straight (~15° on paused video, Claude's figure); partial range stops 20–30% of the flexion arc short of straight; symmetry by one-arm dumbbell curls to failure. No validated elbow control test exists | §2.5 |
| D-65 | Wrist control test (O3, round 11) | A: a 1 kg open-chain set at 60 beats a minute, radial-to-ulnar deviation included, clean when nothing clunks or gives way; partial range ~70–80% of flexion and extension by phone; symmetry by band wrist extensions or a grip dynamometer. Unvalidated. Phone reading superseded by D-77 | §2.5 |
| D-66 | Spine control test (O4, round 11) | A: Luomajoki's six tests, 3 reps each, a test positive at 2 or more failed reps; clean = at most 1 positive; partial range measured by phone at T12–L1 and S1–S2, capped by D-69; phone reading superseded by D-77 | §2.5 |
| D-67 | Criterion 3 for the arm (O5, round 11) | B: shoulder ≥80%, elbow and wrist ≥85%, on the mean of 2 sessions; the legs keep ≥90%. Why: healthy dominant arms are 10.8–17.3% stronger | §2.5 |
| D-68 | Criterion 3 load (O6, round 11) | B: a fixed dumbbell load is allowed beside bodyweight and bands — the same weight, set-up and cadence each time | §2.5 |
| D-69 | Available range for a hypermobile joint (O7, round 11) | C: his own measured range everywhere except the spine, whose partial range is capped at 70–80% of the healthy mean (~36–42° of lumbar flexion, ~12–15° of extension). Why: training through a controlled own range was supported in hypermobile shoulders and knees; no trial covers the spine, where passive structures carry the load | R1 · §2.5 |
| D-70 | R12's example after the catalogue's A9 (T11, chat 2026-10-06; triggered by Stage 1) | Harry: OK — the pass example's bilateral Smith squat becomes a bilateral goblet squat. With every joint at stage 1, a bar on his back takes his shoulders past 45° of external rotation, or bends his wrists heavily, so the Smith squat waits for shoulder stage 2 (§2.5 · D-63 · D-65) | R12 example |
| D-71 | Paces for the arm tests (T14, chat 2026-10-06; raised while building the upper-body evaluation routine) | Harry: OK — no validated pace exists for these tests as written, so they borrow tested ones: the wrist control set at 60 beats a minute, up on one beat and down on the next, as the heel-raise test [W72]; one-arm curls and band wrist extensions to failure at 60 beats a minute, 2 beats up and 2 down, ExtRA's 2 s up and 2 s down [W112], which also gives the three arm symmetry tests one rhythm. Unvalidated | §2.5 |
| D-72 | Low-back range without a helper (T15, chat 2026-10-06; raised while building the upper-body evaluation routine) | Harry: OK — beside the phone at T12–L1 and S1–S2, a self-filmed method: pens taped flat on the spine at the low-back dimples (≈S2) and 15 cm higher, filmed side-on from a tripod, the change in angle between them read as the range. Claude's adaptation of dual inclinometry, unvalidated; "15 cm higher" approximates T12–L1 and was not checked against the landmarking study, which could not be read. The reading moves the cap only when his range is below the healthy mean (D-69). The phone option is superseded by D-77 | §2.5 |
| D-73 | One prompt file (Q14, chat 2026-10-06) | A: `gymspec/Project_Prompt.md` is retired; `CLAUDE.md` in the Gym folder root is the only copy of the project prompt, and every reference names it. References to the rulebook it replaced name `CLAUDE_old.md`. Why: the two copies drifted — CLAUDE.md, deployed 2026-10-03, kept the round-9 status until 2026-10-06 | `CLAUDE.md` · every reference |
| D-74 | Rulebook for routine work until the freeze (Q15, chat 2026-10-06) | B: CLAUDE.md — its routine-request mode — and reference.md govern plans and file edits until Stages 0–2 are all frozen; CLAUDE_old.md is history only. Three file rules that lived only there move into reference.md §R4 as interim rules — version note, stem naming, edit method by scope — until Stage 2 replaces them. Supersedes D-20. Superseded in part by Stage 2 D-07: since 2026-10-15 file handling comes from Stage 2 as drafted | `CLAUDE.md` `<task>` · reference.md §R4 |
| D-75 | Training rules for routine work before the freeze (Q16, chat 2026-10-06) | A: until Stages 0–2 are all frozen, plans and routine files take every training rule from Stages 0–1 as drafted — Stage 0 R1–R25 with its sections, Stage 1 R26–R47 with the catalogue; CLAUDE.md and reference.md cover the working method and file handling. Extends D-74. Why: the retired rulebook's training rules all moved into Stages 0–1 (§2.1), and CLAUDE.md and reference.md hold none. Superseded in part by Stage 2 D-07: since 2026-10-15 file handling comes from Stage 2 as drafted | `CLAUDE.md` `<task>` |
| D-76 | Interim file rules, part 2 (Q17, chat 2026-10-06) | A: three more rules that lived only in the retired rulebook join reference.md §R4 until Stage 2 replaces them — the routine-files table (role and build of every routine file), the fallback when the Gym folder can't be reached, and the file checks before delivery. Stage 2 replaced them on 2026-10-15 (Stage 2 D-07) | reference.md §R4 |
| D-77 | Angles without a phone on the limb (Q18, chat 2026-10-07; raised by Harry on the upper-body evaluation routine) | A: the phone only films, from a tripod; every angle in the loading-gate tests is read afterwards from the paused video with Kinovea's angle tools [W134]. The phone level app on the hand (wrist, D-65) and the phone at T12–L1 and S1–S2 (spine, D-66 · D-72) are dropped, so the spine keeps the pens method. Why: holding a phone on his own moving limb was unclear and awkward; angles read from photos and video agreed with goniometry [W128]–[W131], and Kinovea's angles with AutoCAD [W132], though the dropped phone method was valid too [W116 · W133], so the wrist trades a little evidence for one method. The spine trades more: the dropped phone method had ICC 0.85–0.92 when an examiner placed it [W121], and the pens method it keeps is unvalidated (D-72); its reading moves the cap only when his range is below the healthy mean (D-69). The beat comes from a second device, or from an iPhone allowed to play audio while filming [W135] | §2.5 wrist and spine partial range · §2.5 closing paragraph |
| D-78 | Moving pictures in routine files (Q19, chat 2026-10-07) | B: a test or exercise card may carry a moving picture, an SVG animation that plays when the file is opened in a web browser and, everywhere else, shows the start pose with the end pose faint. Until Stage 2 it follows an interim rule in reference.md §R4. Why: Harry could not picture the tests from the text alone. Since 2026-10-15 Stage 2 R62 holds the rule (Stage 2 D-07) | reference.md §R4 · Stage 2 |
| D-79 | Demonstration videos (Q20, chat 2026-10-07) | A: Claude looks for one video per test and links it where a credible channel's title names the movement, checked by title and channel through YouTube's oEmbed; the video pages refused reads (HTTP 429), so none was watched. A video shows the movement only; where it differs from the card, the card rules. In the upper-body file, tests with no such video rely on their picture, plus Kinovea's guide [W134] for the five filmed ranges and the source paper's figure for the shoulder-blade check [W82] and ExtRA [W112]; the side-bend has its picture only | `gymplan/evaluation_upperbody.svg` · `gymplan/evaluation_lowerbody.svg` |
| D-80 | Knee symmetry test (Q1, chat 2026-10-08; raised while building the lower-body evaluation routine) | A: single-leg sit-to-stand from a raised seat — the low box on the bench, thighs above parallel — arms crossed, touching the seat without sitting, reps to technical failure. Why: quadriceps-dominant and inside the knee's stage-1 range; timed versions are reliable and keep their left–right asymmetry between sessions [W136 · W137]; the paced, to-failure form is unvalidated | §2.5 knee row |
| D-81 | Criterion 3 for the legs (Q2, chat 2026-10-08; raised while building the lower-body evaluation routine) | B: the legs keep ≥90%, scored on the mean of 2 sessions 2–7 days apart, as the arm (D-67). Why: with the heel-rise test's SEM of 2.2 reps at ~33 reps [W72], a perfectly even pair fails one session ~26% of the time and a 2-session mean ~11% (Claude's simulation, errors taken as independent per side and session) | §2.5 criterion 3 |
| D-82 | Paces for the leg symmetry tests (Q3, chat 2026-10-08; raised while building the lower-body evaluation routine) | C: the sit-to-stand at 60 beats a minute, 2 beats down and 2 up, so one knee lowers body weight in 2 s; the bridge at 60 beats a minute, one beat each way, as the heel raises [W72], for finer rep resolution. Unvalidated; the classic bridge test has no speed control [W138] | §2.5 knee, hip and ankle rows |
| D-83 | Two-column copy of the upper-body evaluation (Q21 · Q22, chat 2026-10-08) | Q21 A: two columns on a 1,360 px page, not half-width cards. Q22 B: a one-off copy, not updated when v3 changes; a new file, evaluation_upperbody_2col with its .txt copy; v3 unchanged. Why: Harry found v3 a bit long and asked that the existing file stay as it is | `gymplan/evaluation_upperbody_2col.svg` · reference.md §R4 routine table |
| D-84 | Paces for the knee and hip control tests (B3, chat 2026-10-09; raised in a review of the lower-body evaluation routine) | A: the step-down at 60 beats a minute, 2 beats down and 2 up; the single-leg squat at 60 beats a minute, 1 beat down and 1 up. These are the paces on the routine's cards 6 and 9, now in §2.5, where the beat replaces "slow". Why: the pace decides pass or fail, so it belongs in the testable spec, as the arm paces (D-71) and the leg symmetry paces (D-82) do. The squat's pace follows a published protocol of about one squat per 2 s [W140]; the step-down's is unvalidated | §2.5 knee and hip rows |
| D-85 | Tests and the training rules (B4 · B7, chat 2026-10-09; raised in a review of the lower-body evaluation routine) | A, a full exemption: every §2.5 test — range readings, control tests and symmetry tests — is a test, not a training set. Its §2.5 line and its routine card set its range, load, side, pace and end point, and R1–R25 do not apply to it except R9's stops and R20, for which a test session counts as a training session of the region it tests. §0.4 (b) now names muscular-failure testing, and (e) sets the §2.5 tests aside. First written with only R12, R16–R18 and R25 exempted; widened the same day when Harry confirmed the exemption covers every rule (B7). Why: read literally, the tests failed R1–R3, R12, R15, R16, R18, R25 and §0.4 (b) and (e) — heel raises to full height under body weight, range readings to the end of the range, one limb to technical failure at loading stage 1, some reps lowered in 1 s, kit outside §1.3 — and only the control tests were marked as tests (criterion 2). Technical failure precedes muscular failure in hypermobile joints (§5.6 of this Supplement) | §2.5 · §0.4 (b) (e) · Terminology |
| D-86 | reference.md §R8 numbering (Z1, chat 2026-10-09) | Harry: the stale line "D3–D44 · backfill … pending · waits on T1" is removed, since T1 was withdrawn by D-39 and no record of the former D3–D44 was found in the Gym folder; D45–D57 are renumbered D3–D15, so each reference.md ID equals its row here (D-03…D-15). References in reference.md §R5 and §R8 and in this log follow | reference.md §R5 · §R8 · D-03…D-15 · D-39 · Dissolved T1 |
| D-87 | Minimum hold time (O9 H, chat 2026-10-13; triggered by Stage 1 D-11 while planning the upper-body block) | Harry: a timed hold lasts at least the bottom reps of its band in the goal row × 4 s, the same ~4 s per rep R16 uses for seconds in reserve, so a hold is no shorter than the shortest set it stands in for: a compound hold at least 32 s, a plank (abs isolation) at least 48 s. It follows Harry's floor of 8 reps a set (F4). R16's wall-sit example moves from 3 × 30 s to 3 × 35 s | §2.2 hypertrophy row · R16 example · Stage 1 D-11 |
| D-88 | Sessions per week on routine files (Stage 2 O6, chat 2026-10-15; triggered by Stage 2) | Harry: A — plans state each routine's regions, its sessions per week and its sport note; routine files state the regions and the sport note; the Stage 2 register keeps the sessions per week. Why: Harry keeps them in the Stage 2 Supplement rather than on each file (Stage 2 D-05) | §0.1 |

**Dissolved without a decision**

| Item | Status |
|---|---|
| T1 · backfill of reference.md's former D3–D44 from the 19–22 Sep 2026 chats | Dropped: decisions never recorded are out (D-39) |

---

## 4. Rejected alternatives

An X item from reference.md returns only with new, cited evidence.

| Alternative | Rejected because |
|---|---|
| A "Not available" equipment list: pec deck, leg extension, leg curl, separate cable stack, rope attachment, ab strap, ab wheel, wrist roller (X1) | Reason not recorded; §1.3 lists what is available instead |
| Bounding session density "never by breath or heart rate" (X2) | Reason not recorded; §0.1 states the bound positively (joint control) |
| Moving the hip abductor/adductor bullet from §R5 into §R8 (X3) | Reason not recorded |
| Stage-0-only layout: one pair holding every rule | The Gym already has two transformations (Current state → Plan → file), which get their own stages; the planning order and file workflow would have been forced into rules, with no walkthrough (D-16) |
| Four stages, with Programming split into Block design and Session design | Harvest needs the planned compounds before direct sets can be derived, so the two stages would depend on each other (D-16) |
| Copying the corpus into `SampleFile/` | Copies drift (D-12); the corpus is read in place (D-17) |
| Seed data as a Current state + stations JSON | It duplicates Stage 0 text and can drift (D-18) |
| Staged loading for flagged joints only (O9 A) | Harry chose every joint (D-28). The case made for it: graded loading already came from R1–R10, R18, R22 and the step gate, and the rehab evidence uses pattern staging to return an injured or symptomatic joint [W50] [W51] |
| Flagged joints plus a pattern ramp after each layoff (O9 C) | Not chosen (D-28) |
| Goal-table Sets as sets per target muscle per session, or as weekly sets per muscle (O10 B, C) | The NSCA's sets are per exercise and reach each muscle through its exercise (D-29) |
| Isolation to 0–1 RIR after 4 flare-free weeks (R18, first draft; O7 A, C) | Joint safety wins; the goal table's values are a reference (D-33) |
| R15 limited to lifting, or kept as written (O4 B, C) | Owned recovery items join the list; court and cardio sit outside it (D-30, scope since superseded by D-44) |
| R12–R13 read literally, never lifted while a joint is staged (O5 B) | The unlock order would lose its last two stages (D-31) |
| Eccentric tempo during the restart ramp only (O6 B) | Harry: always (D-32) |
| R4 kept as "active scapular depression" (O1 A, round 6) | Read as a pull-down with the arms overhead, it fights the shoulder blade's upward turn, which unstable-shoulder rehab trains [W56] (D-42) |
| R7's ban without a clinician exception (O2 A, round 6) | Published hEDS guidance allows focused stretching of a short muscle with the joint held stable [W58] [W59]; the override keeps the ban as the default (D-43) |
| Conditioning resources kept outside §1.3 (O3 A, round 6) | They are available and will serve future goals; listing them puts their exercises under the hard gates (D-44) |
| Hypertrophy at the most RIR from week 5 (O4 A), or every set at 1 RIR, compounds included (O4 C) (round 6) | A leaves growth on the table at light loads; C has no hEDS evidence for heavy compounds near failure (D-45) |
| A time cap in place of 28, or no total ceiling (O5 B, C, round 6) | 28 seemed to encode Harry's ~1 h session (D-46); since D-49 the time cap has replaced 28 after all |
| Lifting capped at 3 sessions a week (O6 A), or the region cap without guards (O6 B) (round 6) | A: per-muscle frequency is the same under the region cap, and shorter sessions help joint control; B: the trunk, grip, the shoulder under a bar and the lumbar spine would take load on consecutive days unguarded (D-47) |
| Sport on non-training days only, with or without a full rest day (O7 A, B, round 6) | Harry schedules sport and training himself (D-48) |
| The hour covering the whole session, warm-ups and mobility halves included (O1 B, round 7); or no time rule (O1 C) | Harry: the hour is for the exercises only, with at most 15 min more (D-49) |
| Keeping 28 working sets beside the time cap (D-46) | 28 was the result of the time cap, not a cap of its own (D-49) |
| Harry checking the per-muscle guard by hand from per-routine muscle lists (O2 A, round 7) | The schedule-proof form lets any order he picks pass (D-50) |
| Routines carrying nothing for R21, or dropping R21 (O3 A, C, round 7) | Harry wants a note in each routine naming the sports not to play the day after (D-51) |
| Rallies and games in a routine counted as sport, outside the gates (O4 A, round 7) | The cardio routine's goal is like a gym session's — preparing for his sports — so it is routine work (D-52) |
| A conditioning session counted as a training session under R20, or held to R20's next-day check (O1 A, B, round 8) | Harry fits conditioning in flexibly as a separate session, at times in place of a gym session (D-53) |
| A hold's effort as a share of its maximal hold time (O1 B), or as a 0–10 rating (O1 C) (round 9) | B needs a maximal hold test, which this population avoids (§0.4 (b)); C adds a second effort scale (D-60) |
| The ankle test with an eyes-closed stance added (O1 B), or the Star Excursion reach (O1 C) (round 10) | B: eyes-closed times vary widely and could hold the ankle at stage 1 for a long time [W73]; C: needs a floor-tape set-up, and every reach loads the knee as a single-leg squat (D-61) |
| The hip test as a 30 s Trendelenburg stance (O2 B), or the knee's step-down scored on hip criteria (O2 C) (round 10) | B agreed weakly with 3-D motion and not at all with abductor torque [W77]; C would let the hip unlock only together with the knee (D-62) |
| The shoulder test as Watson's control criteria (O1 B), or the Y-balance test or CKCUEST (O1 C) (round 11) | B: no reliability data, and the corrected position needs a trained eye; C: maximal reach at end range on a locked elbow and flat palm, or hand strikes at speed, against R1, R2 and R13 (D-63) |
| Elbow position sense (O2 B), or one-arm reaches from a kneeling push-up position (O2 C) (round 11) | B's smallest real change (~5.5°) exceeds the hypermobile deficit (~1–1.6°); C is shoulder-dominant and voids the published data (D-64) |
| The wrist test with a closed-chain scale push (O3 B), or wrist position sense or the push-off test (O3 C) (round 11) | B is unvalidated; C: position sense was poorly reliable (ICC 0.07–0.47) and the push-off test is a maximal push in extension (D-65) |
| The spine test as McGill's endurance holds (O4 B), or four movement-control tests (O4 C) (round 11) | B measures capacity, not control, with holds to failure; C is blind to flexion control (D-66) |
| ≥90% for the arm (O5 A), or each arm side against its own first score (O5 C) (round 11) | A fails most healthy shoulders and about half of healthy wrists; C misses a lagging side (D-67) |
| Bodyweight or bands only (O6 A), or crane-scale isometrics as well (O6 C) (round 11) | A leaves the arm's tests without reliability data; C is a maximal effort with untested day-to-day reliability (D-68) |
| His own range everywhere (O7 A), or a healthy cap everywhere (O7 B) (round 11) | A lets the spine load near a normal end range; B has no trial support at the limbs and blunts what stage 2 unlocks (D-69) |
| Step-downs to failure (Q1 B), or a banded seated knee extension (Q1 C), as the knee's symmetry test; one session for the legs (Q2 A); one pace for both leg tests, 1 or 2 beats each way (Q3 A, B) (chat 2026-10-08) | Q1 B fails mostly on form, which the step-down control test already scores; Q1 C puts the band's peak tension at a straight hypermobile knee; Q2 A fails an even pair about 1 time in 4; Q3 A lowers one knee under body weight in 1 s, Q3 B coarsens the bridge's rep count (D-80…D-82) |

---

## 5. Corpus evidence

### 5.1 Corpus status

| File | Finding | Consequence |
|---|---|---|
| `gymplan/*.svg` | Canonical routine files | The corpus, read in place |
| `gymtxt/*.txt` | Byte-identical to their SVGs (M1) | Mirrors, not a second corpus |
| `gympdf/*.pdf` | Harry's exports (D-14) | Not read |
| `gymtools/svg_routine_generator/` examples | Old routine versions, kept as data-format references | Not corpus |
| Routine content | Files from before the scaffold were written before the CLAUDE_old.md rules (§5.2) | Observations inform rules; files are not edited in a spec round |

### 5.2 Observations

| Observation | Where | Informs |
|---|---|---|
| No prescription states RIR, RPE or %1RM; lifting cards give sets × reps only (M3) | All 14 files | R16 |
| 18 equipment entries named items not in §1.3: foam roller 7, tennis ball 8, low step 2, EZ-bar 1 (M4). Since D-30 only the EZ-bar entry remains outside the list | foam_rolling_upperbody_hEDS, foam_rolling_lowerbody_hEDS, popliteus_prevention_protocol, routine_upperbody | R15 (D-30) |
| Cardio uses a court, a bike, a pool and a jump rope, all listed since D-44. Jump rope ("good-knee-day only") is impact, open only at loading stage 4. The court phase — footwork drills, rallies and a game — is routine work (D-52): split-step landings, rallies and the game need loading stage 4, lunges stage 3. The ankle and hip have control tests since D-61 · D-62 but stay at stage 1 until Harry passes them (R14); the court phase stays out until the ankle, knee and hip reach stage 4 | cardio_routine | R15 · R12 · R13 · R14 |
| The cardio cool-down's wall sit is held "at ~90°", below the knee's stage-1 range (above parallel) | cardio_routine | R3 · §2.5 |
| The mobility routines already use active drills only: CARs, isometric holds (some at long muscle length), activation drills, slow eccentrics, balance work. 🔖 The "isometric biceps lengthened hold" is done with the arm extended — to check against R2's soft bend | stretching_upper_hEDS, stretching_lower_hEDS | R7 · R2 |
| The popliteus protocol is resistance work for the knee: as a training session it counts toward the lower region's 3 a week unless done inside a lower session | popliteus_prevention_protocol | R20 · §2.7 |
| A mobility cue primes quads "for leg extensions and box squats"; leg extension is not in §1.3 (X1 list) | stretching_lower_hEDS | R15 |
| Lat pulldown cue "let shoulder elevate at top" | routine_upperbody ex. 3 · routine_upperbody_focus_B ex. 2 | R4 |
| Five files describe a knee rehab phase with single-leg eccentric loading restricted; since D-28 every joint starts at loading stage 1, which matches | routine_lowerbody, routine_lowerbody_focus_{A,B,C}, popliteus_prevention_protocol (plus a cue in stretching_lower_hEDS) | §4.1 · R12 |
| "Hip abductor/adductor machine: deferred until knee is stable" in the rules box | routine_upperbody, routine_lowerbody, routine_lowerbody_focus_{A,B,C}, popliteus_prevention_protocol | §0.2 (D-02) |
| Cable exercises the machine cannot execute (D-25): external rotation, reverse fly and lateral raise on 8 cards, plus cable lateral raise and cable crossover as alternatives (M6) | routine_upperbody, routine_upperbody_focus_{A,B,C} | R15 · §1.3 |
| Popliteus Phase 3 adds pogo hops and landings only after Phase 2 is pain-free, and adds the landing absorb only once the knee clears single-leg eccentrics | popliteus_prevention_protocol | R12 · R13 · R14 |
| Nutrition notes (collagen, protein) before and after every lifting session | 8 lifting routines | §0.1 (D-08) |
| "Maintenance volume" as the routine's goal | routine_upperbody | §0.3 (maintenance block, D-23) |
| Preacher curl labelled "shortened bias", spider curl "lengthened bias"; reference.md §R2 labels preacher L and spider M | routine_upperbody ex. 5 | Stage 1 (§6) |
| Foam-rolling exercise numbers follow an older routine numbering (M5) | foam_rolling_lowerbody_hEDS, foam_rolling_upperbody_hEDS | Stage 2 (§6) · D-15 |
| cardio_routine has no version note (M2) | cardio_routine | Stage 2 (§6) |

### 5.3 Measurements

| # | Measure | Method | Result |
|---|---|---|---|
| M1 | SVG ↔ .txt mirror identity | `cmp` per stem | 14 of 14 identical |
| M2 | Version note present | Search for a "vN — " note | 13 of 14; cardio_routine has none |
| M3 | Prescriptions stating RIR, RPE or %1RM | Text search in all 14 SVGs | 0 files |
| M4 | Equipment entries outside §1.3 | Card equipment lines (x = 490, font size 11) compared with §1.3 | 18 entries: foam roller 7, tennis ball 8, low step 2, EZ-bar 1 |
| M5 | Foam-rolling "(ex. n)" references matching the current routine | Name and number matched by hand against the card numbers | Lower: 0 of 7 match routine_lowerbody v4 — each is +2, consistent with the numbering before v4 removed warm-up section A; upper: 1 of 11 match routine_upperbody v6 |
| M6 | Cable exercises outside the §1.3 list (D-25) | Card comments and alternatives text matched against the list | 8 cards (external rotation 3, reverse fly 3, lateral raise 2) in 4 upper routines, plus 2 alternatives in routine_upperbody |

Run 2026-09-29 on Harry's computer: bash, `grep -P`, `cmp`; text extraction as in reference.md §R4.

### 5.4 Training evidence ✏️

| Finding | Source | Informs |
|---|---|---|
| Heavy loading is compatible with hEDS/HSD when ramped and symptom-gated: high-load, full-range shoulder strengthening in 100 HSD patients over 16 weeks was tolerated and beat low-load mid-range. Protocol: weeks 1–3 at 50, 70, 90% of estimated 10RM, then 3 × 10RM, then 4 × 8RM — near failure — supervised twice weekly, pain <5/10 allowed; more transient soreness (56% vs 37%) and headaches (40% vs 20%), no serious adverse events (re-read 2026-10-01) | [W12] | §0.1 · R22 · R18 (D-45) |
| Feasibility ramp: weeks 1–3 at 50–90% of 10RM → 3 × 10RM → 4 × 8RM; load rises only when all reps complete with acceptable symptoms. The study's ≤5/10 matches Harry's gate | [W13] | R22 · §2.6 (D-01) |
| Hypermobile people strengthen at a normal rate from a lower start (~40% in 12 weeks); a self-directed program that under-progressed load produced no gains. 1RM testing is avoided in this population. Slow ≠ static | [W14] · [W15] | R16 · Stage 1 (progression) |
| Muscle memory: 10 weeks of detraining did not compromise total adaptation, and losses returned within the first retraining weeks, size faster-lost than strength; <8 weeks of retraining regained 1RM in older men | [W16] · [W17] | R22 · §0.3 |
| Proximity to failure: hypertrophy rises linearly as sets end closer to failure — ≈0.5 percentage points of growth per rep closer (response-ratio slope −0.48; SMD slope −0.019; preprint values) — and heavier loads may not need as low an RIR; strength gains show no clear relationship. With volume matched, failure and non-failure give similar hypertrophy. [W4] re-read 2026-10-01 (abstract and preprint); [W5] from a verified reference list | [W4] · [W5] | R17 · R18 (D-45) |
| Ending at 1–2 RIR (leg press 2, leg extension 1) grew the quadriceps as much as training to failure over 8 weeks in 18 trained lifters, with less velocity loss | [W61] | R18 (D-45) |
| At 30% 1RM, sets short of failure grew less than sets to failure; at 80% 1RM, failure added nothing; strength gains did not depend on failure (25 untrained men; read via a secondary summary) | [W62] | R18 (D-45) · §2.2 reps |
| Power: low velocity-loss thresholds — sets ended far from failure, ≤20% — gave the best jump, sprint and heavy-load-velocity gains (meta-analysis) | [W63] | §2.2 power RIR · R17 |
| RIR estimates: people under-predict reps to failure by ~0.95 reps on average; accuracy is worse above 12 reps and better closer to failure, with heavier loads and in later sets | [W64] | R18 (D-45) · §0.4 (b) |
| Fatigue impairs active joint position sense at the knee, ankle and hip (meta-analysis); people with joint hypermobility syndrome show poorer lower-limb joint position sense | [W65] · [W66] | R18 · R19 |
| Lat activity falls and lower-trapezius activity rises as shoulder elevation increases (isometric pull-down, 60° → 120°) | [W52] | R4 · R8 |
| Muscle length: training at longer vs shorter mean muscle lengths gave practically equivalent regional hypertrophy (meta-analysis; preprint abstract read, published version not opened); lengthened partials matched full range in trained lifters across 8 upper-body exercises, a cable single-arm pulldown included; single trials favour long lengths for some muscles (overhead vs neutral triceps, title only) | [W54] · [W53] · [W55] | R4 · R1 |
| Rehab for multidirectional shoulder instability (Watson program) is built on scapular control, particularly upward rotation; Ehlers–Danlos-type laxity is present in a minority of MDI cases | [W56] · [W57] | R4 · R6 (D-42) |
| hEDS/HSD physical therapy: stretching hypermobile joints is commonly discouraged and overpressure into open-packed positions is avoided, but focused stretching of a muscle causing imbalance is appropriate with the local joint held stable; proprioceptive training should include the hypermobile range; strengthening progresses slowly | [W58] | R7 · §0.1 (D-43) |
| EDS Society: careful, gentle stretching helps tight muscles, overstretching beyond normal range harms; stabilise flexible areas before stretching tight ones; movement-control and stabiliser work at low joint load suits EDS and HSD; people with unstable joints should avoid high-impact activities such as running and jumping | [W59] | R7 · R13 · §1.3 (D-43 · D-44) |
| Frequency guidance: novices train the whole body 2–3 days a week; intermediates 3–4 (4 with a split, each major muscle group twice); advanced 4–6 | [W67] | R20 (D-47) |
| At least one day, and no more than three, between workouts that stress the same muscle groups; split routines may run on consecutive days for different muscle groups; frequency drops when other stress is high | [W68] | R20 (D-47) |
| 3 vs 6 sessions a week gave similar adaptations in trained men (title only — the abstract was not reachable) | [W69] | R20 (D-47) |
| Split and full-body routines give equivalent hypertrophy and strength when volume is equated (via a secondary summary) | [W70] | R20 (D-47) |
| Tendon collagen synthesis peaks ~24 h after exercise and stays raised for ~3 days; degradation peaks earlier, and without sufficient rest net collagen loss may occur | [W71] | R20 (D-47) |
| Growth is similar across ~6–30 reps when effort is matched (not re-checked) | [W6] · [W7] | §2.2 hypertrophy reps |
| Rest: a small hypertrophy benefit above 60 s and no appreciable difference beyond 90 s; 3 min beat 1 min for size and strength in trained men; rest length had no meaningful effect on the per-session PUOS | [W8] · [W9] · [W11] | §2.2 rest |
| Goal table: sets, reps, rest and %1RM by goal follow the NSCA load-and-repetition and rest-period assignments; NSCA "sets" are per exercise per session, not per muscle per week | [W2] | §2.2 |
| %1RM ↔ RM: 1RM 100 · 2RM 95 · 3RM 93 · 4RM 90 · 5RM 87 · 6RM 85 · 7RM 83 · 8RM 80 · 9RM 77 · 10RM 75 · 12RM 67. A load's RM = reps + RIR, so a %1RM band becomes an RM band (67–85% ≈ 6–12RM), prescribed as reps + RIR whose sum falls inside it. Hence the strength row runs 3–5 reps rather than NSCA's ≤6: compounds keep ≥1 RIR, and ≥85% caps reps + RIR at 6 | [W3] | §2.2 load check · R16 |
| Volume drives growth; frequency does not once volume is fixed: a square-root curve with no detectable gain beyond ~31 fractional sets/week; frequency slope +0.32%/extra day, interval crossing zero; synergist sets counted at 0.5 fit best (67 studies, n = 2,058). For strength, frequency showed a positive effect with diminishing returns | [W10] | §2.3 · §0.3 Volume · R20 · Stage 1 |
| Weekly sets per muscle group is the volume unit of the hypertrophy dose-response: each extra weekly set added ~0.37% growth; <5 sets/week 5.4%, 5–9 sets 6.6%, 10+ sets 9.8% (15 studies, 34 treatment groups) | [W47] | §0.3 Volume · §2.3 |
| With weekly volume equated, training frequency does not significantly or meaningfully change hypertrophy, so a weekly total can be split by preference | [W48] · [W10] | §0.3 Volume (D-27) |
| Strength: higher frequency gives larger gains mostly through extra volume; with volume equated there is no significant frequency effect overall, though multi-joint and upper-body exercises gained from higher frequency in subgroup analyses | [W49] | §0.3 Volume (strength spread) |
| Per session, returns flatten at ~11 fractional sets per muscle for hypertrophy and ~2 direct sets for strength (PUOS, counted per muscle); data are thin above ~10 sets/session (mean 5.95 ± 4.49, range 0–24), hence a soft cap; an earlier analysis put the bend at 6–8 total sets with ≥2 min rest. The analysis gives a ceiling only, no floor; the first set of a session gives the largest gain. The authors ask for cautious reading of the PUOS | [W11] · [W19] | R19 · §0.3 Volume |
| Power: movement, load and velocity specificity drive power gains, with ballistic, plyometric and Olympic-lift exercises as the primary tools | [W18] | D-05 · D-36 |
| hEDS/JHS physical therapy: treatment is individualized and focuses on learning to control movement; exercise is taught and graded per ACSM guidance to avoid flare-ups; return to sport after injury or illness is carefully progressed to avoid re-injury | [W50] | D-28 · §4 |
| GEAR program (EDS and generalized HSD patients): progressions run closed → open chain, proximal → distal, non-weight-bearing → weight-bearing, mid-range isometrics → through-range, bilateral → unilateral, short → long lever; each prescription is tailored to the patient's symptoms; a step up follows when effort stays below 3/10 and any pain increase settles within 2 h | [W51] | D-28 · §4 |
| People with benign joint hypermobility syndrome had poorer lower-limb joint position sense than controls (meta-analysis of 5 studies, n = 254); hypermobile adults also sensed elbow and knee position worse, though closed-chain stability tests did not differ | [W74] · [W81] | §2.5 (O1 · O2, round 10) |
| Unstable ankles with generalized hypermobility reached less far on the Star Excursion test's posteromedial (83.6 vs 92.8%) and posterolateral (84.7 vs 95.7%) directions; 12 weeks of balance training improved both groups alike and halved re-sprains in the hypermobile group (n = 40) | [W75] | §2.5 (O1, round 10) |
| Single-leg heel-rise test (10° incline, 60 beats/min, fingertip support, stop when height, cadence or posture fails): test–retest ICC 0.96, SEM 2.2 reps; men about 37 reps at 20 years and 33 at 30, left and right alike (n = 566) | [W72] | §2.5 (O1, round 10) |
| Single-leg stance, arms crossed, best of 3 trials up to 45 s: ICC ≥0.99; ages 18–39 hold about 44–45 s eyes open, men 16.9 s and women 13.1 s eyes closed | [W73] | §2.5 (O1, round 10) |
| Weight-bearing (knee-to-wall) lunge test of ankle dorsiflexion: inter-clinician ICC 0.80–0.99, intra-clinician 0.65–0.99; minimal detectable change 4.6–4.7° or 1.6–1.9 cm | [W80] | §2.5 partial range (O1, round 10) |
| Single-leg squat rated good, fair or poor on overall impression, trunk, pelvis, hip and knee: inter- and intra-rater κ 0.60–0.80; good performers fired gluteus medius 115–152 ms earlier and had more hip abduction torque | [W76] | §2.5 (O2, round 10) |
| Trendelenburg test (30 s single-leg stance, pelvis drop or trunk shift = positive) in 18 healthy adults: weak agreement with 3-D motion analysis (κ 0.22–0.25) and no correlation with hip abductor torque | [W77] | §2.5 (O2, round 10) |
| Single-leg hamstring bridge: a low score preceded hamstring injury in Australian football (482 players); newer variants: inter-rater ICC >0.98, test–retest ICC 0.68–0.75 | [W78] · [W79] | §2.5 symmetry test (O2, round 10) |
| Scapular dyskinesis test (5 weighted flexions and abductions, rated from behind as normal, subtle or obvious): κw 0.48–0.61, agreement 75–82%. Shoulders rated "obvious" showed less upward rotation (p < .001), less clavicular elevation (p < .001) and more clavicular protraction (p = .044) in 3-D, but dyskinesis was unrelated to symptoms in overhead athletes | [W82] · [W83] | §2.5 (O1, round 11) |
| Hypermobile shoulders (HSD, n = 12): 16 weeks of heavy cuff and scapular strengthening, up to 4 × 8 RM, each exercise kept free of subluxation and of obvious scapular dyskinesis; adherence 83%, no serious adverse events, WOSI 51% better, strength 28–31% higher | [W84] | §2.5 (O1, round 11) |
| Multidirectional-instability programme (Watson): progression from scapula setting to arc of motion once the scapula drill is done against a band with 1 kg in the hand for 3 × 20; early work within 0–30° of abduction and 0–45° of external rotation | [W85] | §2.5 (O1, round 11) |
| CKCUEST (15 s of alternate touches, hands 91.4 cm apart): ICC > 0.75 within and between sessions, SEM 1.45–2.76 touches, MDC 2.05–3.91; healthy men ~21 (sedentary) to ~24 touches (recreational athletes); the axial load on the support arm is close to body weight | [W86] | §2.5 (O1, round 11) |
| Posterior shoulder endurance test (prone, 90° horizontal abduction and full external rotation, load by body weight and arm length, held to failure): ICC 0.85 pain-free and 0.77 painful, MDC90 17–31 s; asymptomatic men ~68.5 s in an earlier study, as cited. Shoulder endurance test (band, from 90° flexion to 90/90 at a rising cadence): ICC 0.78–0.93 | [W87] · [W88] | §2.5 symmetry test (O1, round 11) |
| Smartphone range-of-motion apps (systematic review): adequate reliability or validity for most movements at every joint studied; spinal axial rotation fell short in 4 of 9 studies. Elbow: phone vs goniometer ICC > 0.95, elbow flexion lowest at 0.84 | [W89] · [W92] | §2.5 partial ranges (O1–O4, round 11) |
| Hypermobile adults (Beighton ≥ 4, n = 46 vs 37) reproduced elbow and knee angles at 30° and 60° less accurately; the CKCUEST, a closed-chain lower-limb test and grip strength did not differ | [W81] | §2.5 (O2, round 11) |
| Elbow position sense, active reproduction at 45–75°: test–retest ICC 0.57–0.75, best at 60°; SEM 2°; healthy mean absolute error 5.7°. With a phone app, elbow position sense was reliable between 50° and 110° | [W90] · [W91] | §2.5 (O2, round 11) |
| Chronic wrist hypermobility (25 people vs 25 matched controls; midcarpal instability in 96.5%): worse wrist position sense, isometric wrist extension, grip strength and function (effect sizes 0.41–0.75). Wrist stabilising exercise (3 × 10 up to 8 × 10, 0.5–1.0 kg, daily for 12 weeks) did no better than a hand orthosis in hypermobile adults (n = 169) | [W93] · [W94] | §2.5 (O3, round 11) |
| Wrist position sense, active reproduction: test–retest ICC 0.07–0.47, SEM 2°, mean absolute error 3.98°; healthy men's mean errors at 20° 2.5–4.5° (n = 100). Push-off test (a maximal push through a grip dynamometer with the handle reversed): inter-rater ICC 0.85–0.97, intra-rater 0.92–0.96 in wrist and elbow patients (n = 22) | [W95] · [W96] · [W97] | §2.5 (O3, round 11) |
| Lumbar movement-control tests rated from video: inter-rater κ 0.24–0.71, 6 of 10 tests > 0.6; both rater pairs > 0.6 on pelvic tilt, one-leg stance (left), sitting knee extension and rocking forward; less experienced raters did worse. With six tests, people with low back pain averaged 2.21 positive and healthy controls 0.75 (d = 1.18); only 5 of 102 healthy had 3 or more | [W98] · [W99] | §2.5 (O4, round 11) |
| Torso endurance (75 young adults): reliability .97–.99 in 5 subjects retested on 5 days; men (n = 31): extensors 146 ± 51 s, flexors 144 ± 76 s, side bridges 94 ± 34 s right and 97 ± 35 s left; flexor:extensor 0.99. In a later study: side bridges ICC 0.74–0.96, extensors 0.79, flexors 0.66 | [W100] · [W101] | §2.5 (O4, round 11) |
| Upper-limb strength asymmetry (scoping review and meta-analysis): the dominant side was 11.6% stronger on average, 2.1–19.5% by joint and movement — shoulder 17.3%, wrist 11.9%, elbow 10.8%, grip 8.1%, forearm 4.7%; men 13.2%; athletes excluded | [W102] | §2.5 criterion 3 (O5, round 11) |
| Scapular dyskinesis test as documented in full (75 athletes, live raters; 1.5 or 2.5 kg by body mass at 68.1 kg; 8–10 cycles, 2 s up and 2 s down, arms raised as far as possible): McClure's normal/subtle/obvious scale agreed κ > 0.81 between raters for flexion and substantially for abduction; same rater κ 0.67–0.81 | [W104] | §2.5 (O1, round 11) |
| ExtRA abduction (one arm, back to the wall, 2.5 kg, 90° scaption at 30 beats a minute, straight elbow, reps to failure): limits of agreement ±7.5–7.8 reps within a rater and ±11.7–13.1 between raters; correlated strongly (0.70–0.89) with 6 of 40 isokinetic measures and moderately with 26; norms from 344 adults (mean age 53.5) | [W112] | §2.5 symmetry test (O1 · O6, round 11) |
| Crane-scale isometric shoulder external rotation (arm at the side, strapped to a fixed point): ICC 0.95 within a session, SEM 9.3 N; ICC 0.90 against a handheld dynamometer; between-session reliability untested; ~USD 50 | [W114] | §2.5 symmetry test (O6, round 11) |
| National-level badminton men: isometric external rotation equal between sides (1.23 vs 1.25 N·m/kg); internal rotation stronger on the racket side (1.57 vs 1.44) | [W123] | §2.5 criterion 3 (O5, round 11) |
| Upper Quarter Y-Balance Test (one-arm push-up position, three maximal reaches): test–retest 0.80–0.99, inter-rater 1.00 (22 retested); composite reach 84.5 ± 8.3% of limb length (read by a research agent) | [W124] | §2.5 (O1, round 11) |
| Goniometry in hypermobility assessments: inter-rater SEM 1.1–6.2°; joints without a firm end point, such as the elbow, are harder to measure, and a large carrying angle can mimic hyperextension (read by a research agent) | [W125] | §2.5 partial range (O2, round 11) |
| 30-second arm curl, dominant arm, ages 18–35 (n = 57): ICC 0.94 (0.90–0.97), typical error 1.6 reps | [W113] | §2.5 symmetry test (O2 · O6, round 11) |
| Palmar midcarpal instability: the "catch-up clunk" appears moving from radial to ulnar deviation; often bilateral, and asymptomatic or barely symptomatic with generalized laxity; treated with proprioceptive control and isometric strengthening of flexor and extensor carpi ulnaris | [W115] | §2.5 (O3, round 11) |
| Wrist range self-measured with an iPhone: within 2° of a goniometer, ICC > 0.94 (n = 60); remote self-measurement reliable for flexion and extension only; goniometry's minimal detectable difference at the wrist is 18° (read by a research agent) | [W116] · [W117] · [W118] | §2.5 partial range (O3, round 11) |
| Grip: a low-cost dynamometer agreed with the reference device (ICC > 0.97); grip was not weaker in women with hEDS/HSD (hand flexors spared) or in generalized hypermobility (read by a research agent; [W81] checked) | [W119] · [W120] · [W81] | §2.5 symmetry test (O3, round 11) |
| Wrist weight-bearing tolerance on a scale (healthy adults, n = 465; men ~82.5 lb): a maximal push with the elbow and wrist in full extension (read by a research agent) | [W127] | §2.5 (O3, round 11) |
| Six-test lumbar movement-control battery (3 reps each; a test positive when 2 or more fail): with "2 or more positive tests" as impaired, specificity 89% and LR+ 3.40 for chronic back pain vs none (n = 141, ages 20–40); trained raters agreed κ 0.37–0.67 on single tests but κ 0.35 on the overall result | [W103] | §2.5 (O4, round 11) |
| Lumbar range with a phone (dual inclinometry at T12–L1 and S1–S2, examiner-placed; 30 adults): ICC 0.85–0.92, smallest real change ~6–8°; healthy means: flexion 51–52°, extension 16.5–18.4°. Side-bending by a fingertip slide down the thigh: ICC 0.84–0.86 (read by a research agent) | [W121] · [W122] | §2.5 partial range (O4 · O7, round 11) |
| No validated pace was found for a one-arm curl, a band wrist extension or a light wrist control set as written: the 30-second arm curl runs as many full-range curls as possible [W113]; the hypermobile wrist programme sets 0.5–1 kg and 3 × 10 up to 8 × 10 a day, with no pace [W94]. Paced tests that exist: heel raises at 60 beats a minute, one beat each way [W72]; ExtRA at 2 s up and 2 s down, stopped when height, pace or plane fails [W112] | [W113] · [W94] · [W72] · [W112] | §2.5 paces (D-71) |
| Angles read from photos or video against a goniometer: elbow, self-taken smartphone photos, ICC 0.74–0.83 (32 people) [W128]; wrist, photos taken at home by patients, substantial agreement for active bending and almost perfect for passive (30 of 69 patients sent photos) [W129]; shoulder and elbow on 10 cadavers, photo accuracy equal to goniometry and more precise than visual estimates [W130]; still phone images of shoulder internal rotation and forearm turning, ICC ≥ 0.91, the one significant difference 2.2° (20 people) [W131]. Kinovea's angles agreed with AutoCAD, best with the camera square to the movement [W132] | [W128] · [W129] · [W130] · [W131] · [W132] | §2.5 partial range (D-77) |
| Shoulder range self-measured with a phone app, standing (19 healthy adults): ICC 0.72–0.97 against a goniometer [W133]. The method D-77 drops was valid; it went for handling, not accuracy | [W133] | §2.5 partial range (D-77) |
| Hypermobile shoulders (HSD, n = 100), 16 weeks: full-range high-load work (twice weekly, supervised) vs neutral/mid-range low-load work (three times weekly). WOSI −174.5 (95% CI −341.4 to −7.7) favouring high load, under the 252-point MID (per protocol −250.7); more soreness (56 vs 37%) and headache (40 vs 20%); no serious adverse events. Load and range changed together, so the trial cannot say which mattered; progression required no subluxation, no obvious dyskinesis and symptoms below 5/10. A secondary summary reports one dislocation in the high-load group (not checked) | [W105] · [W84] | §2.5 (O7, round 11) |
| Same trial: exercise-induced pain averaged < 0.5/10 in both groups over 16 weeks; pain fell 0.89 (high load) vs 0.33 points (low load), not significant (read via a summary) | [W106] | §2.5 (O7, round 11) |
| Systematic review (4 studies, n = 186, hEDS/HSD shoulder symptoms): strengthening showed large effects on pain; evidence very limited; at one year, emotional well-being favoured the high-load programme | [W107] | §2.5 (O7, round 11) |
| Children with joint hypermobility and knee pain: exercise into the hypermobile range and to neutral both improved strength and pain; the hypermobile-range group gained more in self-esteem (read via [W110]) | [W111] · [W110] | §2.5 (O7, round 11) |
| Guidance for hEDS/HSD: a carefully graduated exercise prescription, evidence limited [W110]; include the hypermobile range in proprioceptive training, avoid overpressure into open-packed positions, progress slowly [W58] | [W110] · [W58] | §2.5 (O7, round 11) |
| Multidirectional shoulder instability (41 people aged 12–35, about 60% generally lax): Watson's staged programme — scapular control first, then load and elevation into functional ranges — beat a programme done mostly at 0° of elevation, at 12 and 24 weeks; minor soreness only | [W109] | §2.5 (O1 · O7, round 11) |
| Athletes with joint hypermobility had higher odds of shoulder injury (OR 3.25, 95% CI 1.64–6.43; 6 studies, 2,335 athletes; low-quality evidence) | [W108] | §2.5 (O7, round 11) |
| Exercise trials in Ehlers-Danlos syndrome: adverse events in < 1% of participants. Spinal stabilisation (8 weeks, 46 women with joint hypermobility syndrome) improved McGill endurance and pain (P = .022) (trial read via the review) | [W126] | §2.5 (O4 · O7, round 11) |
| Single-leg sit-to-stand, timed: the 5-repetition version had inter-rater ICC 0.99 on both legs and test–retest ICC 0.87–0.94, sessions 3–7 days apart [W136]; an app-timed version had interday ICC 0.81–0.89 with left–right asymmetry unchanged between sessions [W137]; the quadriceps are highly active in single-leg squats (as cited in [W136]) | [W136] · [W137] | §2.5 knee symmetry test (D-80) |
| Single-leg bridge test: heel on a box, knee ~20°, arms crossed, the other leg held vertical, the buttocks touching the floor between reps without rest, to failure, one warning before stopping [W139]; it lacks speed regulation and runs long [W138] | [W138] · [W139] | §2.5 hip symmetry pace (D-82) |
| A published single-leg squat protocol ran about one squat per 2 s to ~45–60° of knee flexion, rated on overall impression, trunk, pelvis, hip and knee [W140] | [W140] | §2.5 hip control pace (D-84) |

### 5.5 Sport evidence ✏️

Checked Sep 2026. Grade: A peer-reviewed data on the sport · B related population, small sample or secondary citation · C coaching source or reasoning · H Harry's account. Volume and page numbers not all re-checked.

| Finding | Source | Grade | Informs |
|---|---|---|---|
| Archery is Olympic recurve | Harry | H | §1.2 |
| Clicker reaction time, draw force and post-release sway speed predicted shot score in 39 elite recurve archers | [W20] | A | §1.2 archery |
| Middle and posterior deltoid drive draw-side horizontal abduction through the draw and release | [W21] | B | §1.2 archery demand, carryover |
| Skill groups differed in flexor digitorum superficialis, extensor digitorum, middle and posterior deltoid and all three trapezius parts (details from a reference list) | [W22] | A | §1.2 archery demand |
| Scapular muscle activity damps upper-arm tremor at full draw | [W23] | A | §1.2 archery carryover |
| Bow shoulder stronger in adduction and internal rotation; extensors stronger in both shoulders than in non-athletes (15 archers) | [W24] | A, small sample | §1.2 archery carryover |
| The draw hand releases by active finger-extensor contraction | [W25] | A | §1.2 archery demand |
| Elite archers fire the finger extensors to keep the bow hand off the grip | [W26] | A | §1.2 archery demand |
| Sustained posterior deltoid, middle/lower trapezius and anconeus activity (compound archers) | [W27] | B | §1.2 archery demand |
| Trunk muscles (pecs, abdominals) involved | Harry | H | §1.2 archery demand |
| Pec major as the bow-shoulder adductor/internal rotator: anatomy applied to [W24] | Reasoning | C | §1.2 archery demand |
| Triceps holding the bow elbow: the anconeus data above plus bow-arm mechanics | Reasoning | C | §1.2 archery demand |
| Rhomboids: no EMG source found (deep muscle) | — | C | §1.2 archery demand |
| Legs: standing sway is controlled at the ankle (calves) and hip (abductors/adductors) — cited from memory, not retrieved | [W28] | B | §1.2 archery demand, lower |
| Injuries: shoulder 30–53%, elbow 12.8% (epicondylitis), spine and forearm 8.9–19.9% | [W29] | B | §1.2 archery loads |
| Overuse shoulder pain 52.9%, 64.6% of it when drawing (figures via a secondary source) | [W30] | B | §1.2 archery loads |
| Painful archer shoulders mainly involved supraspinatus, biceps long head and subscapularis | [W31] | A | §1.2 archery loads |
| Fingers as a loaded tissue: no injury source found; listed from the finger-hook demand [W25] | Reasoning | C | §1.2 archery loads |
| Hyperextending bow elbow: turning the arm moves the elbow out of the string path | [W32] | C | §1.2 archery loads |
| Smash speed correlates with shoulder internal rotation at contact and pelvis–thorax separation | [W33] | A | §1.2 badminton demand, carryover |
| Shoulder internal-rotation velocity ≈66% of racket-head speed; forearm pronation, wrist flexion and trunk rotation also contribute (both via a secondary source) | [W34] | B | §1.2 badminton demand |
| Shoulder internal-rotation and elbow-extension velocity correlated with smash speed (via a secondary source) | [W35] | B | §1.2 badminton demand |
| Triceps key at contact; wrist flexors/extensors key for accuracy (via a secondary source) | [W36] | B | §1.2 badminton demand |
| Eccentric external-rotator vs concentric internal-rotator work was studied for the smash's cocking and deceleration phases — result not retrieved; the posterior cuff's decelerating role is reasoning | [W37] | C | §1.2 badminton carryover |
| Forearm supination for backhand strokes: low-quality source only | — | C | §1.2 badminton demand |
| Grip tightening at impact: not sourced | — | C | §1.2 badminton demand |
| Overhead triceps transfer to the smash: no data found | — | C | §1.2 badminton carryover |
| Lunges ≈15% of movements in singles (via a secondary source) | [W38] | B | §1.2 badminton demand, lower |
| Forward lunge: professionals showed higher gastrocnemius, biceps femoris, gluteus maximus, external oblique and latissimus activity | [W39] | A | §1.2 badminton demand |
| Quadriceps braking in the lunge: reasoning, indirectly supported by the patellar tendinopathy rate below | Reasoning | C | §1.2 badminton demand |
| Glute max/med activity tracks knee valgus and tibial shear in a single-leg badminton landing | [W40] | A | §1.2 badminton demand |
| Ankle evertors: inferred from ankle sprains being the most common injury | Reasoning | C | §1.2 badminton demand |
| Injuries: lower limb ≈52%, ankle most common, sprains most prevalent | [W41] | A | §1.2 badminton loads |
| Senior players: knees, ankles and shoulders most injured; patellar tendinopathy 20.3% | [W42] | B | §1.2 badminton loads |
| Dominant-shoulder pain in 52% of world-class players | [W43] | A | §1.2 badminton loads |
| Overuse risk to both the limbs and the spine | [W44] | A | §1.2 badminton loads |
| Elbow and wrist as loaded tissues: no injury source retrieved | — | C | §1.2 badminton loads |
| Achilles rupture is common in recreational men; 21% of ruptures in a Danish registry happened in badminton | [W45] | A | §1.2 badminton loads |
| 97% recreational, mean age 36, 94% mid- or late-game; local muscle fatigue implicated | [W46] | A | §1.2 badminton loads, avoid the day before |
| Carryover lines are reasoning from the demand and injury lines above, not transfer studies | Reasoning | C | §1.2 carryover |

### 5.6 Reasoning ✏️

| Reasoning | Informs |
|---|---|
| Block goal, priority targets and in-season sports change from block to block, so they live in Current state; sport profiles hold what each sport demands and loads, so rules key off whichever sport is in season | §0.1 · §1.2 · §4.1 |
| hEDS/HSD is systemic, so every joint is treated as unstable: R1–R10 apply unconditionally, and every joint is staged through the loading gate (D-28) | §0.1 · §2.5 |
| Loading stages are gated on control, not range: hypermobile joints already have excess range | §0.2 · R14 |
| Active drills only: muscles tighten protectively around unstable joints and passive stretching removes that tone; hypermobile joints lack control, not range. Foam rolling addresses the tightness sensation without end-range lengthening. PNF is out because it starts from a passively held end range and pushes further once the muscle relaxes; static-active holds stay in because the opposing muscles cap their range. A clinician can still prescribe focused stretching of a short muscle with the joint held stable (D-43) | R7 · §0.1 |
| Braced scapula at the top of a pull: a passive hang leaves a lax shoulder on its capsule, so the muscles hold the shoulder blade instead. The hold costs little lat growth — only the last bit of lat stretch, from the shoulder blade rising, is lost, and muscle-length effects are small (§5.4) — and it trains the lower trapezius, which R8 prioritises. It is a hold, not a pull-down: with the arms overhead the shoulder blade turns upward, and forcing it down and back fights that (D-42) | R4 · R6 · R8 |
| Lats can over-activate in multidirectional shoulder instability; lower/mid traps are usually under-recruited; the upper trap compensates | R8 |
| The in-session abort and the step gate answer different questions: the abort decides the current set, the step gate decides next week's dose | R9 · §2.6 |
| Goal-table adaptations for hEDS: hypertrophy reps sit above NSCA's 6–12 (equal growth at lower absolute joint load, §5.4); hypertrophy rest starts at 60 s (§5.4); the most RIR a row permits is taken, except hypertrophy from block week 5 (D-45), because technical failure precedes muscular failure in hypermobile joints. Power RIR ≥3 now has support — distance from failure helps power (§5.4); muscular-endurance RIR 1–3 and general-fitness RIR 2–4 are judgement calls, not cited values | §2.2 · R17 |
| Hypertrophy RIR from week 5 (D-45): growth rises linearly closer to failure and light loads need it most, so isolation — stable, single-joint, lowest joint risk — ends at 1 RIR; RIR is under-called by ~1 rep, so a written 1 RIR seldom means failure. Compounds end at 2 RIR: fatigue degrades joint position sense, hypermobile people start lower, and no hEDS data covers heavy compounds near failure, while HSD shoulders tolerated near-failure loading on shoulder exercises after a ramp. Strength gains don't depend on proximity and power prefers distance, so those rows keep the most RIR (§5.4) | R17 · R18 |
| Higher reps are preferred for the lower absolute joint load, not for growth | §2.2 |
| Reps + RIR only: 1RM testing is avoided in this population (§5.4), and excluding RPE keeps a single effort scale across every plan | R16 |
| The per-session ceiling is a joint-control limit: control degrades with fatigue in hypermobile joints, so it sits below the ~11-set PUOS on purpose and is never raised to fit a plan | R19 |
| Exercise time (D-49): Harry caps a session's exercises at about an hour, 15 min more at most. The old ≤28-set ceiling was that hour expressed in hypertrophy sets — 28 sets at 60–90 s rest with a 2–3 s lowering take ≈40–80 min — while at strength or power rest (2–5 min) 28 sets take ≈1–2.5 h. Counting minutes keeps every goal inside the same hour | R19 |
| Region spacing (D-47): 48 h between sessions of the same region keeps each muscle's and tendon's recovery window (≥1 day between sessions that stress the same muscles; tendon collagen synthesis peaks at ~24 h). Interleaving regions keeps per-muscle frequency at ≤3 a week, so growth is unchanged — frequency has no detectable effect once weekly volume is matched — while sessions get shorter, which helps joint control late in a session; weekly capacity doubles (six sessions' exercise time instead of three), and the per-muscle ceiling stays 8 × 3 = 24 fractional sets a week. The trunk, grip, the shoulder under a bar and the lumbar spine take load in both regions, hence the per-muscle and step-gate guards. Because Harry sets the days, the per-muscle guard is checked across routines: routines that share no region are the only ones that can fall on consecutive days, so keeping their muscles apart makes every order pass (D-50). No frequency study in hEDS was found (§5.4) | R20 · §2.7 |
| Sport-day rules key off the sport's profile: the day before protects what the sport needs (fatigue costs performance and, with hEDS, joint control under fast multidirectional load); the day after checks the joints the sport just loaded before a training session loads them again. Harry sets the days (D-48), so each routine's sport note tells him which sport not to play the day after it (D-51). The note counts sets (§2.3): grip held only to carry a weight collects none, so a grip-heavy session is judged by feel | R21 |
| Conditioning sessions sit outside R20: Harry fits them in flexibly, at times in place of a gym session, so that week trains below the plan (D-53). Their exercises still pass the hard gates (D-52), and R9's in-session abort covers them like any session | §2.7 · R20 · §0.4 (f) |
| The 60/80/100% ramp is paced by joint tolerance, not by muscle, since muscle returns within the first retraining weeks (§5.4) | R22 |
| Focus blocks drop unlisted muscles instead of holding them at maintenance: capacity concentrates on the block, and detrained size returns within the first retraining weeks (§5.4). Maintenance is its own block type, run during fat loss (D-23) | §0.3 · §0.4 (c) |
| Hip abductor/adductor machine: available; programmed when relevant | §0.2 (D-02) |

---

## 6. Deferred material

| Item | To |
|---|---|
| Zones: L/M/S labels (every L is truncated by R1); zone availability derived per muscle against R2 and R5; triceps has no S (permanent shortfall); bands first for S; `[HYP]` coverage — per muscle per week ≥1 L + ≥1 M/S, one slot → L; when the gate removes every L, name it and use the best M; S chosen for joint safety and never displacing a passing L; lengthened work as the total-growth lever; elbow flexors preacher (L) + mid-peak curl (M); triceps long head needs overhead work (CLAUDE_old.md `<programming>` Regional; reference.md §R2, §R5 Exercise selection) | Stage 1 |
| Sport filter: four questions and a green / yellow / red verdict; question 2 runs on every exercise (`<programming>`) | Stage 1 |
| Supersets, rules 1–8 (`<programming>`) | Stage 1 |
| Alternatives table, rules 1–9 (`<programming>`) | Stage 1 |
| Planning order: weekly target → harvest from the planned compounds → direct sets → split across sessions → sets per exercise → session totals (`<dosing>` Set units), reconciled with D-35 (goal → muscles → volume → exercises): harvest needs the planned compounds before direct sets are derived | Stage 1 |
| Goal-fit tests per goal: hypertrophy's is lengthened work first with L + M/S coverage (CLAUDE_old.md `<programming>`); strength, power, muscular endurance and general fitness need research (D-36) | Stage 1 |
| Focus-block rules behind the §0.3 stance, incl. the preference for exercises that load other muscles least and planned harvest (`<dosing>` Focus block; D-22) | Stage 1 |
| Maintenance block: volume, goal rows and exercise rules for keeping every muscle group activated during fat loss (D-23) | Stage 1 |
| Volume and capacity: `[HYP]` weekly targets 10–20 fractional sets (calves 12–18); other goals dosed per exercise; start at the bottom of the range; harvest traced to a compound, and muscles with no compound driver harvest nothing; direct = target − harvest, +2 where harvest ≥50% of target; target, harvest and direct stated per muscle; capacity check — the week's working sets and their rest fit the sessions' exercise time (R19 · D-49; the old Σ direct ≤ 28 × sessions/week is gone); frequency rules (`<dosing>`); which goals besides hypertrophy carry a weekly target (D-29) | Stage 1 |
| Exercise-time estimate: minutes per set from reps, tempo (R25) and rest (§2.2), shown per session in the plan (D-49) | Stage 1 |
| Split: training sessions per region within R20, the priority region getting more; the order and the days are Harry's (`<dosing>` Schedule; D-47 · D-48) | Stage 1 |
| Conditioning work: how the §1.3 conditioning resources are prescribed and dosed; the hard gates already apply (D-44), and the cardio routine is routine work (D-52) | Stage 1 |
| Proposal (2026-10-02): a week with a gym session swapped for conditioning (D-53) still trains every priority target if each target's sets are spread over more than one routine where capacity allows | Stage 1 |
| Progression (a)–(c); never load and sets on the same muscle in the same week; step-gate fail → repeat last week's dose; two fails in 4 weeks → one step back (−1 set/muscle or −5% load), hold 2 weeks; deload only on trigger → one week at 50% of sets, same loads (`<dosing>`) · D-10 | Stage 1 |
| Plan output format (`<output>`) and format examples (reference.md §R3) | Stage 1 |
| Plan checks (`<verification>`, every item but the last) | Stage 1 |
| Evidence on regional growth, set units, volume, frequency, harvest, progression, load steps and deloads (reference.md §R2, §R6) and the reasoning on weekly targets, exercise selection and long limbs (§R5) | Stage 1 |
| P1 · a deload trigger for power: "down ≥2 reps" doesn't fit 1–3-rep sets | Stage 1 |
| P2 · the step-back unit for non-hypertrophy goals: "−1 set/muscle" assumes weekly per-muscle sets, which only hypertrophy has | Stage 1 |
| P3 · whether indirect sets count across regions (lower-body hinges toward trunk, which is upper); regions can carry different goals (D-03) | Stage 1 |
| P4 · long femur/humerus is read by no rule; waits on limb-length research (T2) | Stage 1 |
| P6 · bench exercises (Smith bench work included) need alternatives, and a two-station exercise needs alternatives that avoid both; follows from D-09 | Stage 1 |
| Seed data: an exercise catalogue from the corpus (D-18) | Stage 1 |
| Workspace: the Gym folder with fixed paths; the cloud only for steps the computer lacks; working copies in scratch; fallback when the folder can't be reached (`<files>`; D-12) | Stage 2 (interim: reference.md §R4, D-76) |
| File roles table, generator vs hand-laid, naming and v1 for a new routine (`<files>`) | Stage 2 (interim: reference.md §R4, D-74 · D-76) |
| Version note (`<files>`) | Stage 2 (interim: reference.md §R4, D-74) |
| Where the sport note sits in a routine file and how it reads, e.g. "Day after: no badminton" (R21 · D-51) | Stage 2 |
| Cross-file references and updating dependents (`<files>`; D-15) | Stage 2 |
| .txt mirror written with every SVG write (D-13) | Stage 2 |
| Mobility routines: pre and post halves around every training session of their region (§2.7); a change to one updates every routine that references it (D-11) | Stage 2 |
| Edit method by scope; regeneration builds from the file just read (`<workflow>` 3–4) | Stage 2 (interim: reference.md §R4, D-74) |
| File check: edit method matches scope, version incremented, nothing changed outside the request (`<verification>`, last item) | Stage 2 (interim: reference.md §R4, D-76) |
| Moving pictures on routine cards: SVG animation (SMIL) with the start pose solid and the end pose faint as the still view; each picture a self-contained group that a regeneration carries over (D-78) | Stage 2 (interim: reference.md §R4, D-78) |
| Generator and SVG conventions (reference.md §R4) and tooling reasoning (§R5 Tooling) | Stage 2 |
| Corpus drift in §5.2: no RIR, the EZ-bar entry, cable exercises the machine cannot execute, nutrition notes, zone labels, pulldown cue, stale numbers, missing version note, the cardio wall sit and jump rope | Implementation — routine requests, once Harry approves |
| Control tests and partial ranges for every joint other than the knee, added to §2.5 (D-28; interim partial range: D-37). Ankle and hip: added 2026-10-03 (D-61 · D-62). Shoulder, elbow, wrist and spine: added 2026-10-04 (D-63…D-66), with criterion 3 for the arm (D-67 · D-68) and the range reading for hypermobile joints (D-69). Court work still needs stage 4 (D-52) | Done 2026-10-04 |
| A conditioning (aerobic) goal row, for future goals that need cardio (D-44) — awaiting Harry | Backlog |
| T2 · limb-length research (feeds P4) | Backlog |
| V · verification pass on §5.5 — P5 counts 10 unsourced and 15 partly sourced lines | Backlog |

---

## 7. References

Links found by searching each citation (2026-09-29/30): DOI, PubMed, PMC or the publisher's page. 🔖 W19, W21 and W34 could not be identified and carry no link; W35 is a probable match. A link shows the source exists; checking each finding against it is the verification pass (V, §6). W52–W71 were added 2026-10-01/02 with their findings read at the source, except: W55 and W69 by title only, W62 and W70 through secondary summaries, W66 partly. W72–W81 were added 2026-10-03 for the ankle and hip control tests, read through a fetch summariser (abstracts where marked; PubMed and PMC showed a reCAPTCHA, so publisher pages and repositories were used). W82–W102 were added 2026-10-03 for round 11, read the same way. W103–W127 were added 2026-10-04 in a second pass: sources marked "agent" were read by a research agent and not re-checked by Claude; the rest were checked at the source. W128–W135 were added 2026-10-07 for D-77…D-79, read through the fetch summariser at publisher pages, repositories and abstracts; a Europe PMC record refused a read (HTTP 429). W136–W140 were added 2026-10-08 for D-80…D-82, read through search summaries, abstracts and one protocol table; PMC pages refused direct reads with a reCAPTCHA.

| ID | Source | Used for |
|---|---|---|
| W1 | Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (checked Sep 2026) | D-06 |
| W2 | Haff & Triplett (eds.) 2016, Essentials of Strength Training and Conditioning, 4th ed., NSCA / Human Kinetics ([Google Books](https://books.google.com/books?id=bfuXCgAAQBAJ)) | §2.2 |
| W3 | NSCA training load chart, adapted from Landers 1984 ([NSCA PDF](https://www.nsca.com/contentassets/61d813865e264c6e852cadfe247eae52/nsca_training_load_chart.pdf)) | §2.2 load check |
| W4 | Robinson et al. 2024, Sports Med 54:2209–31, [DOI 10.1007/s40279-024-02069-2](https://doi.org/10.1007/s40279-024-02069-2); abstract via [Solent repository](https://pure.solent.ac.uk/en/publications/exploring-the-dose-response-relationship-between-estimated-resist/), slopes from the [SportRxiv preprint](https://sportrxiv.org/index.php/server/preprint/download/295/699/654) | R17 · R18 |
| W5 | Refalo et al. 2023, Sports Med 53:649–65 ([PubMed 36334240](https://pubmed.ncbi.nlm.nih.gov/36334240/)) | R18 |
| W6 | Schoenfeld, Grgic, Ogborn & Krieger 2017, low- vs high-load meta-analysis, JSCR 31(12), [DOI 10.1519/JSC.0000000000002200](https://doi.org/10.1519/JSC.0000000000002200) | §2.2 reps |
| W7 | Lopez et al. 2021, load network meta-analysis, Med Sci Sports Exerc, [DOI 10.1249/MSS.0000000000002585](https://doi.org/10.1249/MSS.0000000000002585) | §2.2 reps |
| W8 | Singer et al. 2024, Front Sports Act Living, [DOI 10.3389/fspor.2024.1429789](https://doi.org/10.3389/fspor.2024.1429789) | §2.2 rest |
| W9 | Schoenfeld et al. 2016, JSCR, [DOI 10.1519/JSC.0000000000001272](https://doi.org/10.1519/JSC.0000000000001272) | §2.2 rest |
| W10 | Pelland, Remmert, Robinson, Hinson & Zourdos 2025, Sports Med, [DOI 10.1007/s40279-025-02344-w](https://doi.org/10.1007/s40279-025-02344-w); abstract checked via the [SportRxiv preprint](https://sportrxiv.org/index.php/server/preprint/view/460) | §2.3 · §0.3 Volume · R20 |
| W11 | Remmert, Pelland, Robinson, Hinson & Zourdos 2025, [SportRxiv preprint](https://sportrxiv.org/index.php/server/preprint/view/537) | R19 · §2.2 rest · §0.3 Volume |
| W12 | Liaghat et al. 2022, BJSM 56:1269–76, [DOI 10.1136/bjsports-2021-105223](https://doi.org/10.1136/bjsports-2021-105223) | §0.1 · R22 · D-01 |
| W13 | Zabriskie 2022, J Funct Morphol Kinesiol 7:61, reporting Liaghat et al. 2020 ([MDPI](https://www.mdpi.com/2411-5142/7/3/61)) | R22 · §2.6 |
| W14 | To & Alexander 2019, Arch Phys Med Rehabil 100:1243–50 ([PubMed 30599140](https://pubmed.ncbi.nlm.nih.gov/30599140/)) | R16 |
| W15 | Luder et al. 2021, BMC Sports Sci Med Rehabil, [DOI 10.1186/s13102-021-00238-8](https://doi.org/10.1186/s13102-021-00238-8) | R16 |
| W16 | Halonen et al. 2024, Scand J Med Sci Sports, [DOI 10.1111/sms.14739](https://doi.org/10.1111/sms.14739) | R22 · §0.3 |
| W17 | Blocquiaux et al. 2020, Exp Gerontol 133:110860 ([PubMed 32017951](https://pubmed.ncbi.nlm.nih.gov/32017951/)) | R22 |
| W18 | Cormie, McGuigan & Newton 2011, Sports Med 41:125–46, [DOI 10.2165/11538500-000000000-00000](https://doi.org/10.2165/11538500-000000000-00000) | D-05 · D-36 |
| W19 | Krieger, earlier per-session volume analysis (year not recorded) — 🔖 not identified; his 2010 JSCR meta-analysis reports sets per exercise, not this bend | R19 |
| W20 | Spratford & Campbell 2017, Eur J Sport Sci 17:539–45, [DOI 10.1080/17461391.2017.1285963](https://doi.org/10.1080/17461391.2017.1285963) | §1.2 archery |
| W21 | Simsek & Ertan, ISBS case study (year not captured) — 🔖 not found in the ISBS archive | §1.2 archery |
| W22 | Simsek, Cerrah, Ertan & Soylu 2018, S Afr J Res Sport Phys Educ Recreat 40:141–55 ([AJOL](https://www.ajol.info/index.php/sajrs/article/view/168256)) | §1.2 archery |
| W23 | Lin et al. 2010, J Sports Sci 28:415–21, [DOI 10.1080/02640410903536434](https://doi.org/10.1080/02640410903536434) | §1.2 archery |
| W24 | Kim et al. 2018, Clin Shoulder Elb 21:145–50, [DOI 10.5397/cise.2018.21.3.145](https://doi.org/10.5397/cise.2018.21.3.145) | §1.2 archery |
| W25 | Ertan et al. 2003, Hum Mov Sci 22:37–45 ([PubMed 12623179](https://pubmed.ncbi.nlm.nih.gov/12623179/)) | §1.2 archery |
| W26 | Ertan 2009, J Sci Med Sport 12:357–60 ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1440244008000042)) | §1.2 archery |
| W27 | Mat Salleh et al. 2024, Ann Appl Sport Sci 12:e1452 ([AASS](https://aassjournal.com/article-1-1452-en.html)) | §1.2 archery |
| W28 | Winter 1995, Gait Posture 3:193–214 ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0966636296828499)) | §1.2 archery |
| W29 | Agranovich et al., Archery injuries: a literature review, Pediatr Traumatol Orthop Reconstr Surg ([journal page](https://journals.eco-vector.com/turner/article/view/625717)) | §1.2 archery |
| W30 | Niestroj, Schöffl & Küpper 2018, J Sports Med Phys Fitness 58:1063–70 ([PubMed 28944650](https://pubmed.ncbi.nlm.nih.gov/28944650/)) | §1.2 archery |
| W31 | Grover & Sinha (Akhoury G. K. Sinha) 2017, Asian J Sports Med 8(1) ([journal page](https://brieflands.com/journals/asjsm/articles/13338)) | §1.2 archery |
| W32 | archery360.com, 2022-02-17 ([article](https://archery360.com/2022/02/17/bowstring-hitting-your-arm-heres-how-to-stop-it/)) | §1.2 archery |
| W33 | King, Towler, Dillon & McErlain-Naylor 2020, Appl Sci 10:1248, [DOI 10.3390/app10041248](https://doi.org/10.3390/app10041248) | §1.2 badminton |
| W34 | Liu, Kim & Tan 2002, NTU report — 🔖 not found online; known only through a secondary source | §1.2 badminton |
| W35 | Salim, Lim et al., Motion analysis of arm movement during badminton smash, IEEE conference paper ([IEEE Xplore](https://ieeexplore.ieee.org/document/5742210/)) — 🔖 probable match | §1.2 badminton |
| W36 | Sakurai & Ohtsuki 2000, J Sports Sci 18:901–14, [DOI 10.1080/026404100750017832](https://doi.org/10.1080/026404100750017832) | §1.2 badminton |
| W37 | Ng & Lam 2002, JOSPT 32:399–404, [DOI 10.2519/jospt.2002.32.8.399](https://doi.org/10.2519/jospt.2002.32.8.399) | §1.2 badminton |
| W38 | Kuntze, Mansfield & Sellers 2010, J Sports Sci 28:183–91, [DOI 10.1080/02640410903428533](https://doi.org/10.1080/02640410903428533) | §1.2 badminton |
| W39 | Jiang, Li & Xiu 2025, Sensors 25:1644 ([PMC11944875](https://pmc.ncbi.nlm.nih.gov/articles/PMC11944875/)) | §1.2 badminton |
| W40 | Hu et al. 2023, Int J Perform Anal Sport 23(6), [DOI 10.1080/24748668.2023.2249760](https://doi.org/10.1080/24748668.2023.2249760) | §1.2 badminton |
| W41 | Marchena-Rodríguez et al. 2024, Res Sports Med 32(6), systematic review and meta-analysis, [DOI 10.1080/15438627.2024.2351964](https://doi.org/10.1080/15438627.2024.2351964) | §1.2 badminton |
| W42 | Pengked, Hareebin, Tawanwongsri & Manunyanon 2025, Electron J Gen Med — cross-sectional survey of senior players ([journal page](https://www.ejgm.co.uk/article/badminton-related-musculoskeletal-injuries-in-senior-players-epidemiology-and-preventive-strategies-15917)) | §1.2 badminton |
| W43 | Fahlström, Yeap, Alfredson & Söderman 2006, Scand J Med Sci Sports 16:168–73, [DOI 10.1111/j.1600-0838.2004.00427.x](https://doi.org/10.1111/j.1600-0838.2004.00427.x) | §1.2 badminton |
| W44 | Pardiwala et al. 2020, Indian J Orthop 54:237–45, [DOI 10.1007/s43465-020-00054-1](https://doi.org/10.1007/s43465-020-00054-1) | §1.2 badminton |
| W45 | Kaldau et al. 2022, J Sports Sci Med 21:224–32, citing Barfod et al. 2021 ([JSSM PDF](https://www.jssm.org/volume21/iss2/cap/jssm-21-224.pdf)) | §1.2 badminton |
| W46 | Fahlström, Björnstig & Lorentzon 1998, Am J Sports Med 26:467–70, [DOI 10.1177/03635465980260032201](https://doi.org/10.1177/03635465980260032201) | §1.2 badminton |
| W47 | Schoenfeld, Ogborn & Krieger 2017, J Sports Sci 35(11):1073–82 ([PubMed 27433992](https://pubmed.ncbi.nlm.nih.gov/27433992/)) | §0.3 Volume · §2.3 |
| W48 | Schoenfeld, Grgic & Krieger 2019, J Sports Sci 37(11):1286–95, [DOI 10.1080/02640414.2018.1555906](https://doi.org/10.1080/02640414.2018.1555906) | §0.3 Volume |
| W49 | Grgic et al. 2018, Sports Med 48(5):1207–20, [DOI 10.1007/s40279-018-0872-x](https://doi.org/10.1007/s40279-018-0872-x) | §0.3 Volume |
| W50 | Engelbert et al. 2017, Am J Med Genet C Semin Med Genet, [DOI 10.1002/ajmg.c.31545](https://doi.org/10.1002/ajmg.c.31545) | D-28 · §4 |
| W51 | Mittal et al. 2021, The GoodHope Exercise and Rehabilitation (GEAR) Program, Front Rehabil Sci, [DOI 10.3389/fresc.2021.769792](https://doi.org/10.3389/fresc.2021.769792) | D-28 · §4 |
| W52 | Park & Yoo 2013, J Electromyogr Kinesiol 23(6):1350–55 ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1050641113002137)) | R4 · R8 |
| W53 | Wolf et al. 2025, PeerJ 13:e18904, [DOI 10.7717/peerj.18904](https://doi.org/10.7717/peerj.18904) | R4 |
| W54 | Varovic, Wolf, Steele, Schoenfeld, Grgic & Mikulic 2025, Int J Sports Med, [DOI 10.1055/a-2615-4935](https://doi.org/10.1055/a-2615-4935); abstract read via the [SportRxiv preprint](https://sportrxiv.org/index.php/server/preprint/view/464) | R4 |
| W55 | Maeo et al. 2023, Eur J Sport Sci, [DOI 10.1080/17461391.2022.2100279](https://doi.org/10.1080/17461391.2022.2100279) — title only | R4 |
| W56 | Watson, Warby, Balster, Lenssen & Pizzari 2016, Shoulder Elbow, MDI rehabilitation programme, Part 2 ([PDF](https://www.schoudernetwerk.nl/SNNbestanden/2019/Inventarisatie/Shoulder%20&%20Elbow-2016-Watson-1758573216652087.pdf)) | R4 (D-42) |
| W57 | Warby et al. 2022, J Clin Med 11(17):5140 ([MDPI](https://www.mdpi.com/2077-0383/11/17/5140)) | R4 |
| W58 | Russek, Stott & Simmonds 2019, Phys Ther 99(9):1189–1200 ([journal page](https://academic.oup.com/ptj/article/99/9/1189/5510431); [accepted manuscript](https://discovery.ucl.ac.uk/id/eprint/10076290/7/Simmonds_Recognizing%20and%20Effectively%20Managing%20Hypermobility-Related%20Conditions_AAM.pdf)) | R7 · §0.1 (D-43) · §2.5 (O7, round 11) |
| W59 | The Ehlers-Danlos Society, Physical therapy (page modified 2024-02-06) ([page](https://www.ehlers-danlos.com/physical-therapy/)) | R7 · R13 (D-43 · D-44) |
| W60 | Physiopedia, Stretching ([page](https://www.physio-pedia.com/Stretching)) — definitions | R7 · Terminology |
| W61 | Refalo et al. 2024, J Sports Sci 42(1):85–101, [DOI 10.1080/02640414.2024.2321021](https://doi.org/10.1080/02640414.2024.2321021); abstract via the [AUT repository](https://openrepository.aut.ac.nz/items/dbe641c7-a606-4e00-94bc-bb2fbe253afa) | R18 (D-45) |
| W62 | Lasevicius et al. 2022, J Strength Cond Res 36(2) ([Semantic Scholar](https://www.semanticscholar.org/paper/Muscle-Failure-Promotes-Greater-Muscle-Hypertrophy-Lasevicius-Schoenfeld/684771f3ca33c9dccc11fed531089edaed102d38)) — read via a [Sci-Sport summary](https://sci-sport.com/en/strength-hypertrophy-muscle-failure-load-dependent/) | R18 (D-45) |
| W63 | Chen et al. 2024, Int J Sports Sci Coach 19(4):1863–77, [DOI 10.1177/17479541241244581](https://doi.org/10.1177/17479541241244581) | §2.2 power · R17 |
| W64 | Halperin et al. 2022, Sports Med 52:377–90, [DOI 10.1007/s40279-021-01559-x](https://doi.org/10.1007/s40279-021-01559-x) | R18 (D-45) · §0.4 (b) |
| W65 | Sayyadi et al. 2024, BMC Sports Sci Med Rehabil 16:35, [DOI 10.1186/s13102-024-00820-w](https://doi.org/10.1186/s13102-024-00820-w) | R18 · R19 |
| W66 | Smith et al. 2013, Rheumatol Int 33(11):2709–16, [DOI 10.1007/s00296-013-2790-4](https://doi.org/10.1007/s00296-013-2790-4) — abstract partly read | R18 |
| W67 | Ratamess et al. 2009, ACSM position stand, Med Sci Sports Exerc 41(3):687–708, [DOI 10.1249/MSS.0b013e3181915670](https://doi.org/10.1249/MSS.0b013e3181915670) | R20 (D-47) |
| W68 | NSCA, Determination of Resistance Training Frequency, citing Essentials of Personal Training, 2nd ed. ([NSCA](https://www.nsca.com/education/articles/kinetic-select/determination-of-resistance-training-frequency/)) | R20 (D-47) |
| W69 | Saric et al. 2019, J Strength Cond Res, [DOI 10.1519/JSC.0000000000002909](https://doi.org/10.1519/JSC.0000000000002909) — title only | R20 (D-47) |
| W70 | Ramos-Campo et al. 2024, J Strength Cond Res, [DOI 10.1519/JSC.0000000000004774](https://doi.org/10.1519/JSC.0000000000004774) — via a secondary summary | R20 (D-47) |
| W71 | Magnusson, Langberg & Kjaer 2010, Nat Rev Rheumatol 6:262–68, [DOI 10.1038/nrrheum.2010.43](https://doi.org/10.1038/nrrheum.2010.43) | R20 (D-47) |
| W72 | Hébert-Losier, Wessman, Alricsson & Svantesson 2017, Physiotherapy 103(4), [DOI 10.1016/j.physio.2017.03.002](https://doi.org/10.1016/j.physio.2017.03.002) ([ResearchGate record](https://www.researchgate.net/publication/315515008_Updated_reliability_and_normative_values_for_the_standing_heel-rise_test_in_healthy_adults)) | §2.5 (O1, round 10) |
| W73 | Springer, Marin, Cyhan, Roberts & Gill 2007, J Geriatr Phys Ther 30(1):8–15 ([PDF](https://geriatrictoolkit.missouri.edu/balance/Normative_Values_for_the_Unipedal_Stance_Test_Springer-JGPT.pdf)) | §2.5 (O1, round 10) |
| W74 | Smith, Jerman, Easton, Bacon, Armon, Poland & Macgregor 2013, Rheumatol Int 33(11):2709–16, [DOI 10.1007/s00296-013-2790-4](https://doi.org/10.1007/s00296-013-2790-4) ([UEA repository](https://ueaeprints.uea.ac.uk/id/eprint/46950/)) — abstract | §2.5 (round 10) |
| W75 | Hou et al. 2023, BMC Musculoskelet Disord 24:71, [DOI 10.1186/s12891-023-06179-2](https://doi.org/10.1186/s12891-023-06179-2) | §2.5 (O1, round 10) |
| W76 | Crossley, Zhang, Schache, Bryant & Cowan 2011, Am J Sports Med 39(4):866–73, [DOI 10.1177/0363546510395456](https://doi.org/10.1177/0363546510395456) — abstract | §2.5 (O2, round 10) |
| W77 | McCarney, Andrews, Henry, Fazalbhoy, Selva Raj, Lythgo & Kendall 2020, Chiropr Man Therap 28:53, [DOI 10.1186/s12998-020-00344-3](https://doi.org/10.1186/s12998-020-00344-3) | §2.5 (O2, round 10) |
| W78 | Freckleton et al. 2014, Br J Sports Med 48(8):713–17, [DOI 10.1136/bjsports-2013-092356](https://doi.org/10.1136/bjsports-2013-092356) — via an index summary | §2.5 (O2, round 10) |
| W79 | Waldhelm et al. 2024, Isokinet Exerc Sci 32(4):367–75, [DOI 10.3233/IES-230084](https://doi.org/10.3233/IES-230084) — abstract | §2.5 (O2, round 10) |
| W80 | Powden, Hoch & Hoch 2015, Man Ther 20(4):524–32, [DOI 10.1016/j.math.2015.01.004](https://doi.org/10.1016/j.math.2015.01.004) — abstract | §2.5 (O1, round 10) |
| W81 | Akaras, Deniz, Eymir & Sönmez 2025, Sci Rep 15:40529, [DOI 10.1038/s41598-025-24199-x](https://doi.org/10.1038/s41598-025-24199-x) | §2.5 (rounds 10–11) |
| W82 | McClure, Tate, Kareha & Irwin 2009, J Athl Train 44(2):160–4, [DOI 10.4085/1062-6050-44.2.160](https://doi.org/10.4085/1062-6050-44.2.160) ([SLUHN record](https://crin.sluhn.org/crms_ap/9/)) — abstract | §2.5 (O1, round 11) |
| W83 | Tate, McClure, Kareha & Irwin 2009, J Athl Train 44(2):165–73, [DOI 10.4085/1062-6050-44.2.165](https://doi.org/10.4085/1062-6050-44.2.165) ([SLUHN record](https://crin.sluhn.org/crms_ap/8/)) — abstract | §2.5 (O1, round 11) |
| W84 | Liaghat, Skou, Jørgensen et al. 2020, Pilot Feasibility Stud 6:97, [DOI 10.1186/s40814-020-00632-y](https://doi.org/10.1186/s40814-020-00632-y) | §2.5 (O1, round 11) |
| W85 | Watson, Warby, Balster, Lenssen & Pizzari 2016, Shoulder Elbow, [DOI 10.1177/1758573216652086](https://doi.org/10.1177/1758573216652086) ([PDF](https://www.schoudernetwerk.nl/SNNbestanden/2019/Inventarisatie/Shoulder%20&%20Elbow-2016-Watson-1758573216652086.pdf)) | §2.5 (O1, round 11) |
| W86 | Tucci, Martins, Sposito, Camarini & de Oliveira 2014, BMC Musculoskelet Disord 15:1, [DOI 10.1186/1471-2474-15-1](https://doi.org/10.1186/1471-2474-15-1) | §2.5 (O1, round 11) |
| W87 | Evans, Konz, Nitz & Uhl 2021, Phys Ther Sport 47:66–71, [DOI 10.1016/j.ptsp.2020.10.014](https://doi.org/10.1016/j.ptsp.2020.10.014) — abstract | §2.5 (O1, round 11) |
| W88 | Declève, Van Cant, Attar et al. 2021, Phys Ther Sport 47:201–7, [DOI 10.1016/j.ptsp.2020.12.005](https://doi.org/10.1016/j.ptsp.2020.12.005) ([ULB repository](https://dipot.ulb.ac.be/dspace/bitstream/2013/351864/3/j.ptsp.2020.12.005.pdf)) | §2.5 (O1, round 11) |
| W89 | Keogh, Cox, Anderson et al. 2019, PLoS One 14(5):e0215806, [DOI 10.1371/journal.pone.0215806](https://doi.org/10.1371/journal.pone.0215806) | §2.5 partial ranges (round 11) |
| W90 | Rider & Valdes 2024, J Hand Ther 37(2):243–9, [DOI 10.1016/j.jht.2023.08.015](https://doi.org/10.1016/j.jht.2023.08.015) — abstract | §2.5 (O2, round 11) |
| W91 | Ramos, Carnaz, Mattiello, Karduna & Zanca 2019, Phys Ther Sport 37:157–63, [DOI 10.1016/j.ptsp.2019.03.016](https://doi.org/10.1016/j.ptsp.2019.03.016) — abstract | §2.5 (O2, round 11) |
| W92 | Behnoush, Tavakoli, Bazmi et al. 2016, Asian J Sports Med 7(2):e30668, [DOI 10.5812/asjsm.30668](https://doi.org/10.5812/asjsm.30668) — abstract | §2.5 (O2, round 11) |
| W93 | Karagiannopoulos & Griech 2024, J Hand Ther 37(2):209–17, [DOI 10.1016/j.jht.2023.10.001](https://doi.org/10.1016/j.jht.2023.10.001) — abstract | §2.5 (O3, round 11) |
| W94 | Lindholm & Claesson 2025, Clin Rehabil 39(1):47–57, [DOI 10.1177/02692155241293265](https://doi.org/10.1177/02692155241293265) | §2.5 (O3, round 11) |
| W95 | Vincent, MacDermid, Michlovitz et al. 2014, J Hand Ther 27(3):185–91, [DOI 10.1016/j.jht.2014.03.002](https://doi.org/10.1016/j.jht.2014.03.002) — abstract | §2.5 (O3, round 11) |
| W96 | Shetty, Neelapala & Vishal 2024, Musculoskelet Sci Pract 73:103140, [DOI 10.1016/j.msksp.2024.103140](https://doi.org/10.1016/j.msksp.2024.103140) | §2.5 (O3, round 11) |
| W97 | Pilbeam & Hood-Moore 2018, Hand Ther 23(3):100–9, [DOI 10.1177/1758998318770227](https://doi.org/10.1177/1758998318770227) — abstract | §2.5 (O3, round 11) |
| W98 | Luomajoki, Kool, de Bruin & Airaksinen 2007, BMC Musculoskelet Disord 8:90, [DOI 10.1186/1471-2474-8-90](https://doi.org/10.1186/1471-2474-8-90) | §2.5 (O4, round 11) |
| W99 | Luomajoki, Kool, de Bruin & Airaksinen 2008, BMC Musculoskelet Disord 9:170, [DOI 10.1186/1471-2474-9-170](https://doi.org/10.1186/1471-2474-9-170) | §2.5 (O4, round 11) |
| W100 | McGill, Childs & Liebenson 1999, Arch Phys Med Rehabil 80(8):941–4, [DOI 10.1016/S0003-9993(99)90087-4](https://doi.org/10.1016/S0003-9993(99)90087-4) (read via an academia.edu copy) | §2.5 (O4, round 11) |
| W101 | Waldhelm & Li 2012, J Sport Health Sci 1(2):121–8, [DOI 10.1016/j.jshs.2012.07.007](https://doi.org/10.1016/j.jshs.2012.07.007) | §2.5 (O4, round 11) |
| W102 | Foley, Callaghan, Forman, Graham, Holmes & La Delfa 2025, Sci Rep 15:4636, [DOI 10.1038/s41598-025-87413-w](https://doi.org/10.1038/s41598-025-87413-w) | §2.5 criterion 3 (O5, round 11) |
| W103 | Wattananon, Ibrahim, Kongoun & Klahan 2025, PLoS One 20(6):e0325996, [DOI 10.1371/journal.pone.0325996](https://doi.org/10.1371/journal.pone.0325996) | §2.5 (O4, round 11) |
| W104 | Rossi, Pedroni, Martins & de Oliveira 2017, PLoS One 12(7):e0181518, [DOI 10.1371/journal.pone.0181518](https://doi.org/10.1371/journal.pone.0181518) | §2.5 (O1, round 11) |
| W105 | Liaghat, Skou, Søndergaard, Boyle, Søgaard & Juul-Kristensen 2022, Br J Sports Med 56(22):1269–76, [DOI 10.1136/bjsports-2021-105223](https://doi.org/10.1136/bjsports-2021-105223) — abstract | §2.5 (O7, round 11) |
| W106 | Liaghat et al. 2025, Scand J Pain 25(1), [DOI 10.1515/sjpain-2024-0072](https://doi.org/10.1515/sjpain-2024-0072) — via a [summary](https://www.physiotutors.com/research/loading-of-hypermobile-shoulders/) | §2.5 (O7, round 11) |
| W107 | Higo, Palmer, Liaghat et al. 2024, Arch Rehabil Res Clin Transl 6(3):100360 ([publisher page](https://www.sciencedirect.com/science/article/pii/S2590109524000582)) | §2.5 (O7, round 11) |
| W108 | Liaghat, Pedersen, Young, Thorlund, Juul-Kristensen & Juhl 2021, BMC Musculoskelet Disord 22, [DOI 10.1186/s12891-021-04249-x](https://doi.org/10.1186/s12891-021-04249-x) ([record](https://research.regionh.dk/en/publications/joint-hypermobility-in-athletes-is-associated-with-shoulder-injur)) — abstract | §2.5 (O7, round 11) |
| W109 | Warby, Ford, Hahne, Watson, Balster, Lenssen & Pizzari 2017, Am J Sports Med 45(11):2624–34 ([PDF](https://www.schoudernetwerk.nl/SNNbestanden/2019/Inventarisatie/RCT.GHInstabilityMDI.WarbyWatson.2017.pdf)) | §2.5 (O1 · O7, round 11) |
| W110 | Engelbert, Juul-Kristensen, Pacey et al. 2017, Am J Med Genet C 175C:158–67 ([PDF](https://www.ehlers-danlos.com/wp-content/uploads/2022/03/Engelbert_et_al-2017-American_Journal_of_Medical_Genetics_Part_C-_Seminars_in_Medical_Genetics.pdf)) | §2.5 (O7, round 11) |
| W111 | Pacey, Tofts, Adams, Munns & Nicholson 2013, Pediatr Rheumatol 11:30, [DOI 10.1186/1546-0096-11-30](https://doi.org/10.1186/1546-0096-11-30) — via [W110]; the page was rate-limited | §2.5 (O7, round 11) |
| W112 | Ford, Lewis, Tyros et al. 2026, Physiotherapy 131:101868, [DOI 10.1016/j.physio.2025.101868](https://doi.org/10.1016/j.physio.2025.101868) ([repository](https://bura.brunel.ac.uk/bitstream/2438/33074/4/FullText.pdf)) | §2.5 (O1 · O6, round 11) |
| W113 | Boshnjaku, Bahtiri, Feka, Krasniqi, Tschan & Wessner 2021, Data Brief 36:106988, [DOI 10.1016/j.dib.2021.106988](https://doi.org/10.1016/j.dib.2021.106988) | §2.5 (O2 · O6, round 11) |
| W114 | Dignazio, Marchant, Hutchinson, Popchak & Sprague 2025, Int J Sports Phys Ther 20(4):583–94, [DOI 10.26603/001c.132166](https://doi.org/10.26603/001c.132166) | §2.5 (O6, round 11) |
| W115 | Wolfe, Garcia-Elias & Kitay 2012, J Am Acad Orthop Surg 20(9):575–85, [DOI 10.5435/JAAOS-20-09-575](https://doi.org/10.5435/JAAOS-20-09-575) ([PDF](https://www.scottwolfemd.com/pdf/midcarpal-instability-review-wolfe-2012.pdf)) | §2.5 (O3, round 11) |
| W116 | Modest, Clair, DeMasi et al. 2019, J Hand Ther 32(4):507–14, [DOI 10.1016/j.jht.2018.03.004](https://doi.org/10.1016/j.jht.2018.03.004) — agent, abstract | §2.5 (O3, round 11) |
| W117 | Alford 2021, J Hand Ther 34(4):549–54, [DOI 10.1016/j.jht.2020.05.001](https://doi.org/10.1016/j.jht.2020.05.001) — agent, abstract | §2.5 (O3, round 11) |
| W118 | Reissner, Fischer, List, Taylor, Giovanoli & Calcagni 2019, J Orthop Surg Res 14:173, [DOI 10.1186/s13018-019-1177-y](https://doi.org/10.1186/s13018-019-1177-y) — agent | §2.5 (O3, round 11) |
| W119 | Panhale, Kini & Kothale 2025, J Hand Microsurg 17(4):100291, [DOI 10.1016/j.jham.2025.100291](https://doi.org/10.1016/j.jham.2025.100291) — agent, abstract | §2.5 (O3, round 11) |
| W120 | Coussens, Lapauw, Banica et al. 2022, J Musculoskelet Neuronal Interact 22(1):5–14 ([record](https://researchers.mq.edu.au/en/publications/muscle-strength-muscle-mass-and-physical-impairment-in-women-with/)) — agent, abstract | §2.5 (O3, round 11) |
| W121 | Pourahmadi et al. 2016, PeerJ 4:e2355, [DOI 10.7717/peerj.2355](https://doi.org/10.7717/peerj.2355) | §2.5 (O4 · O7, round 11) |
| W122 | Hecimovich & Hebert 2016, S Afr J Sports Med 28(1):23–6, [DOI 10.17159/2078-516x/2016/v28i1a745](https://doi.org/10.17159/2078-516x/2016/v28i1a745) — agent | §2.5 (O4, round 11) |
| W123 | Stausholm, Baun, Bjordal et al. 2021, Int J Sports Phys Ther 16(2):504–10, [DOI 10.26603/001c.21531](https://doi.org/10.26603/001c.21531) | §2.5 (O5, round 11) |
| W124 | Gorman, Butler, Plisky & Kiesel 2012, J Strength Cond Res 26(11):3043–8, [DOI 10.1519/JSC.0b013e3182472fdb](https://doi.org/10.1519/JSC.0b013e3182472fdb) — agent | §2.5 (O1, round 11) |
| W125 | Schlager, Ahlqvist, Rasmussen-Barr et al. 2018, BMC Musculoskelet Disord 19:376, [DOI 10.1186/s12891-018-2290-5](https://doi.org/10.1186/s12891-018-2290-5) — agent | §2.5 (O2, round 11) |
| W126 | Buryk-Iggers, Mittal, Santa Mina et al. 2022, Arch Rehabil Res Clin Transl 4(2):100189, [DOI 10.1016/j.arrct.2022.100189](https://doi.org/10.1016/j.arrct.2022.100189) | §2.5 (O4 · O7, round 11) |
| W127 | Barlow, Scholtz & Medeiros 2022, J Hand Ther 35(1):74–9, [DOI 10.1016/j.jht.2020.10.019](https://doi.org/10.1016/j.jht.2020.10.019) — agent | §2.5 (O3, round 11) |
| W128 | Meislin, Wagner & Shin 2016, J Hand Surg Am 41(4):510–5.e1, [DOI 10.1016/j.jhsa.2016.01.006](https://doi.org/10.1016/j.jhsa.2016.01.006) — abstract | §2.5 partial range (D-77) |
| W129 | Trehan, Rancy, Johnsen, Hillstrom, Lee & Wolfe 2017, J Wrist Surg 6(4), [DOI 10.1055/s-0037-1599830](https://doi.org/10.1055/s-0037-1599830) | §2.5 partial range (D-77) |
| W130 | Russo, Burn, Ismaily et al. 2018, J Orthop Sci 23(2):310–5, [DOI 10.1016/j.jos.2017.11.016](https://doi.org/10.1016/j.jos.2017.11.016) — abstract | §2.5 partial range (D-77) |
| W131 | Whitson, Cook, Middleton, Humphrey & Sciascia 2025, Int J Sports Phys Ther 20(12):1723–31, [DOI 10.26603/001c.147174](https://doi.org/10.26603/001c.147174) — abstract | §2.5 partial range (D-77) |
| W132 | Puig-Diví, Escalona-Marfil, Padullés-Riu et al. 2019, PLoS One 14(6):e0216448, [DOI 10.1371/journal.pone.0216448](https://doi.org/10.1371/journal.pone.0216448) — abstract | §2.5 partial range (D-77) |
| W133 | Shimizu, Saito, Kouno et al. 2022, JSES Int 6(4):655–9 ([DOAJ record](https://doaj.org/article/28bb5950c9e54ec098f48373f0376075)) — abstract | §2.5 partial range (D-77) |
| W134 | Kinovea documentation, "Measuring angles" ([page](https://kinovea.readthedocs.io/en/stable/measurement/angle.html)); Kinovea 2025.2, free and open source ([kinovea.org](https://www.kinovea.org/)), checked 2026-10-07 | D-77 · D-79 |
| W135 | Tom's Guide, "iOS 18 finally lets you record videos with background music" ([page](https://www.tomsguide.com/phones/iphones/how-to-record-video-with-background-music-in-ios-18)): Settings → Camera → Record Sound → Allow Audio Playback | D-77 |
| W136 | Waldhelm, Gubler, Sullivan, Witte, Buchheister & Bartz-Broussard 2020, Int J Sports Phys Ther 15(3):388–94 ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7296996)) — abstract | §2.5 (D-80) |
| W137 | Birinci, Makaracı, Aktaş, Atasever & Ruiz-Cárdenas 2026, Gait Posture 125:110100, [DOI 10.1016/j.gaitpost.2026.110100](https://doi.org/10.1016/j.gaitpost.2026.110100) — abstract | §2.5 (D-80) |
| W138 | Sano, Kawabata, Van Hooren et al. 2025, BMC Sports Sci Med Rehabil, [DOI 10.1186/s13102-025-01458-y](https://doi.org/10.1186/s13102-025-01458-y) — abstract | §2.5 (D-82) |
| W139 | Evidence in Motion, "Return to Sport Testing Appendix" (2025), single-leg bridge test after Freckleton et al. ([PDF](https://evidenceinmotion.com/wp-content/uploads/2025/04/Return-to-Sport-Testing-Appendix.pdf)) — secondary | §2.5 (D-82) |
| W140 | Int J Sports Phys Ther 2018, 13(3):526–36, Table 3, single-leg squat test protocol ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6044589/table/T3)) — table only | `evaluation_lowerbody` card 9 |
