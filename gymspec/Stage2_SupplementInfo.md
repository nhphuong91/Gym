# Stage 2 — Supplement Info

**Non-normative.** Companion to `Stage2_RoutineFiles.md`: terminology, architecture history, decision log, rejected alternatives, corpus evidence, deferred material, walkthrough, references and the register's entries.
Where the two documents disagree, the normative document governs. Stage 0 and Stage 1 terminology (`Stage0_SupplementInfo.md` §1 · `Stage1_SupplementInfo.md` §1) apply unchanged. `[W#]` → §8 References; "Stage 0 [W#]" → `Stage0_SupplementInfo.md` §7. Section numbers found only here (§5.1–§5.5, §6–§9) refer to this Supplement; every other § refers to `Stage2_RoutineFiles.md`, unless prefixed "Stage 0" or "Stage 1".

---

## 1. Terminology

Terms introduced by Stage 2.

| Term | Meaning in this project |
|---|---|
| Routine file | A file in `gymplan/`, `<stem>.svg`, with its mirror in `gymtxt/`; every role in the register (§3.1), not only lifting |
| Stem | A routine file's name without folder or extension, shared by the SVG, its mirror and Harry's PDF export |
| Mirror | `gymtxt/<stem>.txt`, a byte copy of the SVG (R57 · Stage 0 D-13) |
| Register | The list of routine files — stem, role, regions, build (§3.1 · R52) — whose entries sit in §9 (D-01) |
| State file · log row | `gymstate/block_<NN>.json`, one per block: Current state, the plan-only fields and a log (§3.4 · R67 · D-10…D-14) · one conversation's entry in that log: date, changes, open follow-ups |
| Plan-only fields | The plan fields a routine file does not carry — the R46 check list, the zone coverage, the next step per exercise, the Stage 0 R24 statement (§3.2) — kept in the state file |
| Build type · generator · build script · hand-laid | How a file is produced: by the generator from a routine definition · by a kept script in `gymtools/svg/` · by hand, with no model to rebuild from (§3.1 · §2.1) |
| Routine definition | The generator's data — Routine, Section, Exercise, Pair and the boxes — from which `render()` writes an SVG |
| Working copy | The scratch copy a change is made on before it replaces the file (R51) |
| Scope · text · shift · structure | How far a change reaches, which sets its edit method (§2.1 · R54) |
| Regeneration · regeneration source | Rebuilding a whole file · what it is rebuilt from: the file just read, or a kept build script that rebuilds that file byte-identical (R55) |
| Version note | A file's last text, "vN — change" (R56) |
| Reference · dependent | A citation of a file's exercise number and name, or of an item ID, inside or across files · a file holding a reference to a changed file (R60 · R61) |
| Region-wide file | A mobility or foam-rolling file: a menu of drills or areas by target — muscle groups, joints, tendons or spots — for any session of its region, which Harry picks from by the session's targets; it cites no routine (R60 · D-03) |
| Card · section · block | One exercise or test with its prescription · the cards under one header, a pair or a straight block · any of the parts §3.2 lists |
| Moving picture · still view | An SVG animation (SMIL) on a card · what a viewer without animation shows: the start pose solid, the end pose faint (R62 · Stage 0 D-78) |
| Width estimate · render check | Text width from character counts (§2.2) · a PNG rendered in Chromium with Liberation Sans, and looked at (R64) |
| File checks · delivery report | The ten checks of R66 · the record a delivery ends with (§3.3) |
| One-off copy | A file made once from another and not kept in step with it, e.g. `evaluation_upperbody_2col` (Stage 0 D-83) |

---

## 2. Architecture history

Stage 2 opens from the 11 deferrals Stage 0 sends here (`Stage0_SupplementInfo.md` §6), the 2 Stage 1 sends (`Stage1_SupplementInfo.md` §6), `CLAUDE_old.md` `<files>`, `<workflow>` 3–4 and the last `<verification>` item, and the interim file rules of reference.md §R4 (Stage 0 D-74 · D-76 · D-78).

| Deferral (source) | Stage 2 answer |
|---|---|
| Workspace: the Gym folder with fixed paths; the cloud only for steps the computer lacks; working copies in scratch; the fallback when the folder can't be reached (Stage 0 D-12; interim, reference.md §R4) | §0.2 · R49 · R50 · R51 |
| File roles table, generator vs hand-laid, naming and v1 for a new routine (interim, reference.md §R4) | §3.1 · §9 · R52 · R53 · D-01 |
| Version note (interim, reference.md §R4) | R56 · §2.2 · D-06 |
| Where the sport note sits in a routine file and how it reads (Stage 0 D-51) | R59 · §3.2 · D-02 |
| Cross-file references and updating dependents (Stage 0 D-15) | R60 · R61 · D-03 · D-04 |
| The .txt mirror, written with every SVG write (Stage 0 D-13) | R57 |
| Mobility routines: a pre and a post half around every training session of their region; a change to one updates every routine that references it (Stage 0 D-11) | §3.1 · §3.2 · R60 · R61 |
| Edit method by scope; regeneration from the file just read (interim, reference.md §R4) | §2.1 · R54 · R55 |
| File check: edit method, version, nothing changed outside the request (interim, reference.md §R4) | R66 |
| Moving pictures (Stage 0 D-78; interim, reference.md §R4) | R62 · §2.2 |
| Generator and SVG conventions (reference.md §R4) and the tooling reasoning (reference.md §R5) | §0.2 · §2.2 · R65 · §5.5 |
| Stale alternative-table numbers in the three upper focus files (Stage 1 Supplement §5.2) | Fixed by the v7–v8 rebuilds (M6); R60 keeps them in step |
| Where the plan's rows, alternatives, set counts, exercise time and sport note sit in a routine file (Stage 1 Supplement §6) | §3.2 · R58 |

The register's entries sit in §9, a section the scaffold's list of Supplement sections does not have, so that a new stem changes no normative text (D-01).

**Changed on the way** ✏️

| Before (source) | Stage 2 | Why |
|---|---|---|
| Evaluation files "generator-built" (reference.md §R4) | Build type "build script", the script named in the register (§9) | `evaluation_lowerbody` v1 is drawn without the generator, and v3's script patches the generator's card renderer (gymtools/README.md) |
| Regeneration "from the file just read, never from a definition already in routine_generator.py" (reference.md §R4) | From the file just read, or a kept build script that rebuilds it byte-identical (R55) | The scripts kept since 2026-10-09 rebuild their files byte-identical (M7); one that does not would revert a direct edit |
| "A file without one starts at v1" (reference.md §R4) | Its first write adds "v1 — …" (R56) | The line read two ways; `cardio_routine` was the case (M2) |
| A note "on its latest change" (reference.md §R4) | A note naming the change of its write; files changed together can share one (R56) | Harry: the v8 trio's shared note is fine (D-06) |
| "gymtxt/<stem>.txt byte copy" (reference.md §R4) | Copied with `cp` on Harry's computer and compared (R57) | The upload route added C2PA metadata to a mirror (2026-10-07) |
| A visual check in Chromium with Liberation Sans (reference.md §R4) | Width estimate and render check, with frames for moving pictures (R64) | The estimate reads every line of a long file; the frames catch a broken animation |
| File checks: method, version, mirror, nothing outside the request (reference.md §R4) | Nine checks (R66); "nothing outside" tested by a text diff | Each check names its test; CLAUDE.md's routine request already runs `pair_check.py` on files |
| Roles: foam rolling "rest days"; cardio "court and conditioning" (reference.md §R4) | Foam rolling outside training sessions; conditioning as routine work under the hard gates (§9) | The wording of Stage 0 §2.7 · Stage 0 D-52 · D-53 |
| A new routine "named like its siblings" (reference.md §R4) | A naming pattern with full-body and maintenance stems (§3.1) | The canonical example is full-body and has no sibling (§7) |
| Routine files state each routine's sessions per week (Stage 0 §0.1) | The register keeps them; the file does not (§3.2 · §9) | Harry (D-05); Stage 0 §0.1 amended to match (D-08 · Stage 0 D-88) |
| The interim file rules of reference.md §R4 govern routine-file work until Stages 0–2 are all frozen (Stage 0 D-74 · D-76 · D-78) | Stage 2 as drafted governs it from the close of round 1; the interim lines of reference.md §R4 are retired (D-07) | Harry (D-07) |
| Mobility and foam-rolling files cite a routine's exercise numbers, "matched to" one routine (Stage 0 D-15) | Region-wide files cite no routine: menus by target (R60) | Harry (D-03) |
| The catalogue cites every version of an exercise routine file (practice, catalogue revisions 8–11) | Only versions that change an exercise, a card number or a pairing (R61) | Harry (D-04) |
| Current state set at the start of each conversation, and the plan-only fields kept only in the chat (Stage 0 §4.1 · §3.2) | One state file per block, read first and written before delivery (R67 · §3.4) | Harry (D-10…D-13): every field without a default was asked again, and the plan-only fields were lost |
| The register keeps the sessions a week (D-05) | The state file's `current_routines` keeps them; the register keeps stem, role, regions and build (§3.1 · §9) | Harry (D-14): which routines are current is block state, not a property of the file |

---

## 3. Decision log — closed open items

Log IDs are local to Stage 2; each row names the OI it closes, and OI numbers restart after each cleared round, so each row carries the round beside the OI. An amendment to another stage is also logged in that stage's Supplement. The freeze itself is a row.

Round 1 opened 2026-10-13 (`Stage2_RoutineFiles.md` §4). On 2026-10-14 Harry closed its first four items and decided two findings of the first draft in chat, F1 and F2 (D-01…D-06); on 2026-10-15 he closed the last two (D-07 · D-08), which closed the round. On 2026-10-22 a routine request for the lower-body two-column copy added D-09. On 2026-10-24 Harry's request for a state file carried from one conversation to the next added D-10…D-14 (O1–O5 of that chat; Q4 on 2026-10-25).

| # | Question | Decision | Lands in |
|---|---|---|---|
| D-01 | Where the register's entries live (round 1 · O1) | Harry: in the Stage 2 Supplement, beside the drafted options (§3.1 of the normative doc, a register file, a comment in each file). §3.1 keeps the fields and the naming pattern; the entries sit in §9, so a new stem changes no normative text | §3.1 · R52 · §9 |
| D-02 | A sport note on evaluation files (round 1 · O2) | B, as Harry put it: an evaluation is a separate session, and what follows it is his to manage, so nothing links it to a sport. Evaluation files carry no sport note; `evaluation_lowerbody`'s note goes at its next write. Claude's case for A, kept on record: tests to technical failure tire the muscles R21 keeps fresh for a sport | R59 · §6 |
| D-03 | References in region-wide files (round 1 · O3) | B, as Harry put it: a mobility file prepares every muscle group, joint and tendon of its region for the whole session, and a foam-rolling file covers every muscle group or spot a session trained; both are menus he picks from by target, so they cite no routine. Their routine links were removed on 2026-10-14 (F4, M11) | R60 · §3.1 · §9 |
| D-04 | Catalogue provenance for every version (round 1 · O4) | Harry: "no". Read as B, Claude's recommendation: a version that changes no exercise, card number or pairing leaves the catalogue as it is; `pair_check.py` and `catalogue/verify.py` then map a stem's cards through its latest cited version (tools changed 2026-10-15, M12). C — no versions in provenance at all — was not chosen | R61 · §6 |
| D-05 | Sessions a week on routine files (F1, chat 2026-10-14) | Harry: the files need not state them; this Supplement keeps them, in the register (§9). Stage 0 §0.1 then asked routine files to state them; it was amended to match (D-08). Superseded in part by D-14: the state file, not the register, keeps them | §3.1 · §3.2 · R52 · §9 |
| D-06 | One version note shared by files changed together (F2, chat 2026-10-14) | Harry: no problem — the v8 trio's shared note stands. R56's note names the change of its write: the whole change made across several files, or this file's share of it | R56 |
| D-07 | From when Claude follows Stage 2's file rules (round 1 · O5) | C: from the close of round 1 (2026-10-15), routine-file work takes its file handling from Stage 2 as drafted, as Stage 0 D-75 did for training rules. `CLAUDE.md` `<task>` now says so, and the seven interim lines of reference.md §R4 are replaced by one line pointing here. Stage 0 D-74 and D-75 are superseded in part; the interim rules of Stage 0 D-76 and D-78 have given way to Stage 2 | `CLAUDE.md` `<task>` · reference.md §R4 |
| D-08 | Stage 0 §0.1 to match D-05 (round 1 · O6) | A: Stage 0 §0.1 now reads that plans state each routine's regions, sessions per week and sport note, routine files state the regions and the sport note, and the Stage 2 register keeps the sessions per week; logged in Stage 0 as Stage 0 D-88, triggered by Stage 2 | Stage 0 §0.1 · §9 |
| D-09 | Two-column copy of the lower-body evaluation (O1 · O2 of a routine request, chat 2026-10-22) | Harry: a one-off copy of `evaluation_lowerbody` v1 on a 1,360 px page, as Stage 0 D-83 did for the upper body: stem `evaluation_lowerbody_2col`, v1 unchanged, built by `build_evaluation_lowerbody_2col_v1.py`, made from a copy of `build_2col.py` (R55). O1 A: §2.2's Page row covers any one-off two-column copy. O2 B: the upper copy's layout — sections start full width, two cards per row, card 5 alone, section D beside card 12. The copy leaves out v1's sport note (R59 · D-02) | §2.2 · §9 |
| D-10 | What the state file carries (O1, chat 2026-10-24) | B: Current state (Stage 0 §4.1), the approved plan's plan-only fields (§3.2) and one log row for each conversation that changes them — date, changes, open follow-ups | R67 · §3.4 |
| D-11 | State-file layout (O2, chat 2026-10-24; Q4, chat 2026-10-25) | B: one file per block in `gymstate/`; the highest number is the current block, and earlier files stay as its history. Q4: numbered `block_01.json`, `block_02.json`…, since the block start is Harry's and is not written down (Stage 0 D-91); first drafted as `block_<block_start>.json` | R67 · §0.2 · §3.4 |
| D-12 | State-file format and check (O3, chat 2026-10-24) | A: JSON, tested by `gymtools/state/state_check.py` — its fields against Stage 0 §4.1 and §3.4, the Stage 0 §4.1 invariants, each current routine against `gymplan/` and the register — reported as R66's check (10) | §3.4 · R66 · `gymtools/README.md` |
| D-13 | Where the state-file rules land (O4, chat 2026-10-24) | A: R67 and §3.4 here, read at intake (S2.1) and written with the files (S2.7); Stage 0 §4.1 is one per block, kept in the state file (Stage 0 D-90); Stage 1 S1.1 reads it (Stage 1 D-12); `CLAUDE.md` `<task>` reads it first | R67 · §3.4 · S2.1 · S2.7 · `CLAUDE.md` `<task>` |
| D-14 | Where the sessions a week live (O5, chat 2026-10-24) | A: in the state file's `current_routines`; the register keeps stem, role, regions and build, and the upper focus role drops "of the current upper block" (§3.1 · R52 · §9). Supersedes D-05 in part: the routine file still does not state them | §3.1 · §3.2 · R52 · §9 · Stage 0 §0.1 |

**Dissolved without a decision**

None.

---

## 4. Rejected alternatives

| Alternative | Rejected because |
|---|---|
| Editing routine files in the cloud workspace and committing them back | Slow, and two copies drift (Stage 0 D-12) |
| Regenerating from a definition stored in a tool | It reverts the direct edits made since (reference.md §R5 · R55) |
| Patching a structure change with `str_replace` | The SVG's height follows its content, and a patch cannot re-flow what lies below (reference.md §R5) |
| A mirror of extracted text only | The byte copy stands in for the whole SVG when files must be attached (Stage 0 D-13) |
| Mirrors written through the upload route | One came back with C2PA metadata (2026-10-07) |
| Routine copies stored in gymtools as a version history | gymtools holds tools, not copies, and a stored copy invites regenerating from a stale definition (gymtools/README.md) |
| Harry's PDF exports as a source | His exports, left untouched (Stage 0 D-14) |
| The register's entries in the normative doc, in a register file, or in a comment in each file (round 1 · O1 A, B, C) | Harry: in this Supplement (D-01) |
| A sport note on evaluation files, by a Stage 2 file rule or by amending Stage 0 (round 1 · O2 A, C) | Harry: an evaluation is a separate session, and what follows it is his to manage (D-02) |
| Region-wide references with a routine's stem added, or listing every current routine (round 1 · O3 A, C) | Harry: region-wide files are menus picked by target (D-03) |
| Catalogue provenance for every version, or for none by version (round 1 · O4 A, C) | Harry: not every version (D-04) |
| Stage 2's file rules from the freeze only, or at once while items were open (round 1 · O5 A, B) | Harry: from the close of round 1 (D-07) |
| Stage 0 §0.1 kept as it was, with sessions per week stated on each routine file (round 1 · O6 B) | It would have undone D-05 (D-08) |
| Sessions a week stated on each routine file (F1) | Harry: the register keeps them (D-05) |
| A version note limited to its own file's share of a change (F2) | Harry: a note shared by files changed together is fine (D-06) |
| A state file with Current state only, or with Harry's training events added — step-gate results, flares, gate tests (O1 A, C, chat 2026-10-24) | Harry: Current state, the plan-only fields and a log (D-10) |
| One state file overwritten each time, or one per conversation (O2 A, C) | Harry: one per block, kept as the history (D-11) |
| State files named by the block start, or by the goal set (Q4) | The block start is Harry's and is not written down (Stage 0 D-91), and a goal set can repeat (D-11) |
| A state file in Markdown tables, or JSON with a generated .md mirror (O3 B, C) | Harry: JSON with a check (D-12) |
| The state-file rules in `CLAUDE.md` only, or in a Stage 3 of their own (O4 B, C) | Harry: R67 and §3.4 in Stage 2 (D-13) |
| The whole register moved into the state file, or the sessions a week kept in both (O5 B, C) | Harry: the state file keeps the sessions a week, the register the facts of each file (D-14) |

---

## 5. Corpus evidence

### 5.1 Corpus status

| File | Finding | Consequence |
|---|---|---|
| The 17 SVGs in `gymplan/` | Read on Harry's computer, 2026-10-13: text, comments, version notes, references, line endings, widths | §5.2 · §5.3 |
| The 17 mirrors in `gymtxt/` | Byte-identical to their SVGs (M1) | Mirrors, not a second corpus |
| `gymtools/` | The generator's md5 checked and the three kept build scripts re-run (M7 · M10) | R55 |
| The 9 files edited on 2026-10-14 | F3: weekday names out of `routine_lowerbody_focus_A`, `_B`, `_C`, `popliteus_prevention_protocol` and `cardio_routine`. F4: routine links out of the two mobility and the two foam-rolling files (D-03). Each from a working copy on Harry's computer (M11) | §5.2 rows marked fixed |
| `gympdf/` | Harry's exports (Stage 0 D-14) | Not read |

### 5.2 Observations

| Observation | Informs |
|---|---|
| The upper focus files v8 are the first built from a Stage 1 plan. Top to bottom: title; subtitle with block type, targets, loading stage, exercise time and working sets; legend; a pre-workout note naming the mobility pre half and the warm-up sets outside the exercise time; one section per pair with minutes, rounds and rest; cards with prime mover and zone, cues, sets × reps, RIR for weeks 1–4 and from week 5, and stations; a post-workout note with the mobility post half, the sport note and the next-day step-gate line; a rules box citing R-numbers; a timing summary; a set-count box; an alternatives table by card number; the version note | §3.2 · R58 |
| None of the v8 files states its sessions a week, which Stage 0 §0.1 then asked routine files to state — kept that way: the register holds it (D-05), and Stage 0 §0.1 now says so (D-08) | §3.2 · §9 |
| The v8 trio carry one identical note — "v8 — re-paired: every exercise in a superset, no straight sets (R38 · R39) · lat pulldown 4, pullover 3, biceps 7 · replaces v7" — though the pulldown sits in focus C and the pullover in focus B; acceptable (D-06) | R56 |
| The v8 sport note: "After: mobility post half · day after: no archery", then "Chest, delts, back, triceps and abs collect sets here — archery's day-before muscles (R21)" | R59 |
| `evaluation_lowerbody` v1 carries "Day after: no badminton — the symmetry tests take calves, quads and glutes to technical failure"; `evaluation_upperbody` v3 has none. The note goes at the file's next write (D-02) | R59 |
| Weekday names in 5 files (M4): "(Monday)", "(Wednesday)", "(Friday)" in the lower focus titles; "Friday cardio day", "Friday lunch tip", "Saturday foam rolling" and "Mon/Wed/Fri lifting" in `cardio_routine`; "Phases 1–2 → Monday (lower) · Phase 3 reactive → Friday (cardio)" in the popliteus protocol. Removed 2026-10-14 (F3) | R66 (5) · Stage 0 §0.1 |
| `cardio_routine` had no version note (M2); its first, v1, was written 2026-10-14 (F3) | R56 |
| The foam-rolling files cited "(ex. n)" of "the upper body routine" and "the lower body routine", the exercise named beside each; the lower numbers followed `routine_lowerbody` from before v4 (Stage 0 M5). Removed 2026-10-14, with "matched to … routine" in both subtitles (F4) | R60 · R61 · D-03 |
| The mobility files' timelines cited routine sections and times — "Warmup sets A (3 min) → Working sets B–E (27 min)", "~82 min" in `stretching_upper_hEDS` v2; "Warmup (2 min) → Working sets A–D (28–33 min)", "~59–67 min" in `stretching_lower_hEDS` v1 — and both subtitles read "matched to your routine". Replaced 2026-10-14 by "Pre half → warm-up sets → your gym session → post half" and "pick drills by target" (F4) | R60 · D-03 |
| `stretching_lower_hEDS` v1 primed the quads "for leg extensions and box squats" — the leg extension is not in Stage 0 §1.3 — and the posterior chain "before hip thrusts and box squats", exercises of older routines. Made general on 2026-10-14: "for squats and knee work", "before hip-extension and squat work" (F4) | R60 · D-03 |
| Mobility IDs cited across files resolve: `cardio_routine` cites S1 and S2 (slow shoulder CARs, eccentric push-up), `routine_upperbody` P1, P3, P4 and P5 | R60 |
| Build types: `evaluation_lowerbody` v1 is drawn by a self-contained script without the generator; `evaluation_upperbody` v3's script patches the generator's card renderer; the two-column copy is drawn from v3 (gymtools/README.md) | §3.1 · §9 |
| Hand-laid files lay out their own way: banner comments, card notes such as "P1. Shoulder CARs — y=262, h=73", and font sizes 10.5, 13 and 14, which the generator never writes; the 4 mobility and foam-rolling files carry the generator's `<!-- LEGEND -->` comment, but not its card comments (M9) | §2.2 · R65 |
| The generator does not escape apostrophes, and textwrap splits hyphenated words unless `break_on_hyphens=False` (gymtools/README.md) | §5.5 |
| A .txt mirror sent through the upload route came back with C2PA metadata (2026-10-07, gymtools/README.md) | R57 |
| `check_widths.py` stopped on font sizes outside its table and flagged x-72 detail lines as picture overlaps in files without pictures (M8). Rewritten 2026-10-14 (T3): every font size, and the right-column check only on lines where that column has text | R64 |
| The catalogue's rows cite "<stem> vN ex. n"; `pair_check.py` mapped cards through them by the file's current version only, and `catalogue/verify.py` holds each file's version and card count as of revision 11. Since 2026-10-15 (T5) `pair_check.py` maps a version the catalogue does not cite through the latest cited one and checks every card's name, and `verify.py` checks the files in gymplan/ against the versions it cites (M12) | R61 · D-04 |
| reference.md §R4's line on cable exercises still lists lateral raise, external rotation and reverse fly, which Stage 0 D-25 took off the cable machine's list | §6 |

### 5.3 Measurements

| # | Measure | Method | Result |
|---|---|---|---|
| M1 | SVG ↔ .txt mirror identity | `cmp` per stem | 17 of 17 identical, before and after the edits of 2026-10-14 |
| M2 | Version note | "vN — " text; position among the text elements; attributes | 16 of 17 files, each the last text, size 9, #aaa, centred; `<!-- VERSION NOTE -->` before it in 13 of the 16 (not in the two foam-rolling files or `stretching_lower_hEDS`); `cardio_routine` had none until its v1 of 2026-10-14 |
| M3 | Line endings | Count of CR bytes | 0 in 17 of 17: LF |
| M4 | Weekday names | Case-insensitive search for day names in the text | 5 files: `cardio_routine` (4 lines), `popliteus_prevention_protocol` (1), `routine_lowerbody_focus_A`, `_B`, `_C` (titles). 0 after the edits of 2026-10-14 |
| M5 | Sport note | "day after: no" in the text | 4 of 17: upper focus A, B, C v8 and `evaluation_lowerbody` v1 |
| M6 | Alternatives-table numbers against cards | Each row's number and name against the card of that number | 21 of 21 rows in 8 files match |
| M7 | Kept build scripts rebuild their files | Run on Harry's computer into scratch; md5 against `gymplan/` | 3 of 3 byte-identical: `evaluation_upperbody` v3 (7f36a39a…), `evaluation_upperbody_2col` v1 (c883d4e5…), `evaluation_lowerbody` v1 (f75c935d…) |
| M8 | Width estimate by `check_widths.py` | Run on every SVG | Before its rewrite (2026-10-13): clean 7; flags 7, among them the two-column copy's 3 centred lines; stops 3 on font sizes 10.5, 13 and 14. After (2026-10-14, the edited files included): no overflow in 12; the two-column copy's 3 centred lines, as expected; 3 lines in `routine_lowerbody` and 2 in `routine_upperbody` (long titles, version notes) to check by eye; 7 in `stretching_lower_hEDS` and 8 in `stretching_upper_hEDS`, all 15 of which fit in the render — the estimate errs wide there |
| M9 | Comment style | Comments per file | Card comments `<!-- Xn — … -->` in the 12 generator and build-script files and in no hand-laid file; section comments `<!-- ── … ── -->` in those 12 and `cardio_routine`; `<!-- LEGEND -->` in 16 of 17 |
| M10 | Generator identity | md5 | `routine_generator.py` 119e30d6…, as gymtools/README.md records |
| M11 | The edits of 2026-10-14 (F3 · F4) | One edit script, every replacement matched exactly once, run on Harry's computer on working copies and in the cloud on staged copies, md5 compared; text diff of each working copy against the file just read; width estimate; render in Chromium with Liberation Sans, every edited line looked at | 9 files, 36 replacements: only the intended lines changed; no new width flag; every edited line fits in the render; the rendered copies byte-identical to the working copies, which replaced the files; mirrors identical |
| M12 | `pair_check.py` and `catalogue/verify.py` after T5 | Name rule run over every card the catalogue cites, and over every pair of rows of different pattern or prime mover; `--selftest`; the upper focus files; planted copies: a cue-only v9 of focus A, a v9 with card 3 swapped, a mobility file with S2 removed; `verify.py` on the live catalogue | 101 of 101 cited cards match their rows; 0 of 4,205 cross pairs match; selftest 14/14; upper focus v8 as before (all pairs pass, B1 REVIEW, B2 NOTE); the cue-only v9 maps through v8 and passes, the swapped card and the removed ID FAIL; ALL PASS, the files edited on 2026-10-14 matching through their cited versions |

Run 2026-10-13 to 2026-10-15 on Harry's computer: bash, `grep -P`, `cmp`, `md5sum`, Python 3.10.12; text extraction as in reference.md §R4; renders in the cloud workspace with `render_png.py`.

### 5.4 Technical evidence ✏️

| Evidence | Source | Informs |
|---|---|---|
| SVG 1.1 takes its animation elements — animate, set, animateMotion, animateColor — from SMIL Animation, and adds animateTransform as a compatible extension | [W1] | R62 |
| SMIL animation in SVG plays in Chrome from version 5 and in Edge from version 79, the first Chromium release | [W2] | R62 · §0.3 (d) |
| Liberation Sans aims at Arial's metrics, so Chromium with Liberation Sans sets text as Edge does with Arial, its sans-serif on Windows (reference.md §R4) | [W3] | R64 · §0.3 (b) |
| oEmbed answers with a resource's title and author name; YouTube's endpoint gave the titles and channels when its watch pages refused reads with HTTP 429 (Stage 0 D-79) | [W4] | R63 |
| Content Credentials (C2PA) attach provenance metadata to a file, which is what the upload route added to a mirror on 2026-10-07 | [W5] | R57 |

### 5.5 Reasoning ✏️

| Reasoning | Informs |
|---|---|
| Work stays on Harry's computer: a cloud round trip per edit is slow and leaves two copies that drift, so the cloud serves only what the computer lacks, Chromium (reference.md §R5) | R49 |
| Minor edits go straight to the working copy; structure changes regenerate the whole file, since the SVG's height follows its content and patching a large change piece by piece costs more than regenerating it (reference.md §R5) | R54 · §2.1 |
| The generator is a tool, not a stored copy: a definition kept in a tool goes stale the moment its file is edited directly, and regenerating from it reverts that edit. A kept build script is safe exactly while it rebuilds the file byte-identical, which its md5 shows before use | R55 |
| The mirror stands in for its SVG when files must be attached; a stale mirror means planning from an outdated routine (reference.md §R5) | R57 |
| One note per write: the note says what the write changed, and a change made across several files can carry one note that reads the same in each (D-06) | R56 |
| The stem names the session, not the block: a new block's sessions replace the old ones as new versions, as the upper focus files kept their stems from v6 to v8, so the files Harry keeps and the references to them stay put | R53 |
| Harry trains from the file, so it carries what he applies set by set — prescription, cues, warnings, rest, pairing, the sport note — while the plan's checks and arithmetic stay with the plan | R58 · §3.2 |
| Sessions a week are Current state, which changes with the block; the state file keeps them with the rest of it, so neither the routine files nor the register need a rewrite when a block changes them (D-05 · D-14) | §3.2 · §3.4 · R67 |
| A "no sport limit" line shows that the note was worked out, not forgotten. Evaluation files carry none: an evaluation is a separate session, and what follows it is Harry's to manage (D-02) | R59 |
| Region-wide files are menus by target: a mobility file prepares every muscle group, joint and tendon of its region for the whole session, and a foam-rolling file covers every muscle group or spot a session trained; tied to one routine's numbers, they went stale with every change (Stage 0 M5) (D-03) | R60 |
| The catalogue holds exercise facts; a version that changes no exercise, card number or pairing changes no fact, so the catalogue stays as it is (D-04) | R61 |
| The register in this Supplement: a new stem changes no normative text, so routine requests stay out of the amendment protocol (D-01) | R52 · §9 |
| One rulebook for file work: Stage 2 from the close of round 1, so no file was edited under a rule an open item could still change (D-07) | §0.2 |
| The width estimate and the render check catch different faults: the estimate reads every line of a long file; the eye catches overlaps that character counts miss, and clears the lines the estimate flags in error (M8) | R64 |
| A text diff of the working copy against the file just read makes "nothing changed outside the request" a test | R66 |
| Writing text for the generator: apostrophes stay plain, since the generator does not escape them, and textwrap runs with `break_on_hyphens=False`, so words like "side-on" stay whole (gymtools/README.md) | §2.2 |

---

## 6. Deferred material

| Item | To |
|---|---|
| Corpus drift still open: sport notes missing from the pre-scaffold routines (M5); `evaluation_lowerbody`'s sport note, to go at its next write (D-02). Fixed 2026-10-14: the weekday names and `cardio_routine`'s missing note (F3), the region-wide files' routine links (F4) | Implementation — routine requests, once Harry approves |
| `pair_check.py` and `catalogue/verify.py`: map a stem's cards through its latest cited version and confirm each card's name against its row, so check (7) of R66 runs on a version the catalogue does not cite (D-04) | Done 2026-10-15 (T5, M12) |
| The matching change to Stage 0 §0.1 for D-05 | Done 2026-10-15: D-08 · Stage 0 D-88 |
| reference.md §R4's cable-exercise line, which still lists lateral raise, external rotation and reverse fly (Stage 0 D-25) | reference.md — Harry's OK |
| `check_widths.py`: read every font size and run its picture checks only on files with pictures | Done 2026-10-14 (T3) |
| `CLAUDE.md` `<governing_documents>` and `<stages>`: Stage 2 listed as draft, with its two files and its open items | Done 2026-10-14 (T1) |
| Proposal (2026-10-13): move a hand-laid file to the generator at its first structure-scale change, so that later structure changes regenerate | Backlog — awaiting Harry |
| Proposal (2026-10-13): a version history for `gymplan/` and `gymtxt/`, e.g. git in the Gym folder, which would lift §0.3 (a) | Backlog — awaiting Harry |

---

## 7. Walkthrough

**Sample.** The canonical example's plan (Stage 1 §7, "What Stage 2 receives"), plus real quirks from the corpus as read on 2026-10-13.

Source: the approved plan for "Build full-body routine A: preacher curl and Smith squat." Fixture: focus block · upper and lower Hypertrophy · priority targets biceps, quads · block week 1 after a 2-month layoff · every joint at loading stage 1 · badminton in season · current routines: none yet.

| Step | Definition | Decision | Action | Output |
|---|---|---|---|---|
| S2.1 | R50 · R67 · R61 · §2.1 | §0.1 Input | The folder is reached; no state file holds the block yet, as it starts now; no current routine, so no file to read; the request is a new file; no file cites routine A, and the region-wide mobility files it names cite no routine | One new file · no dependents |
| S2.2 | §3.1 · R52 · R53 · R54 | §0.2 | Upper + lower, a focus block, its first session: `routine_fullbody_focus_A`, v1, generator — a new pattern, since no full-body sibling exists | Stem · build type · method: a new generator file |
| S2.3 | R51 · R55 | — | Working copy in scratch on Harry's computer; the definition is written from the plan, as there is no file to read | Definition · working copy |
| S2.4 | R58 · §3.2 · R59 · R56 · Stage 0 §0.1 | §0.1 Content | Title "Full body hypertrophy — Session A"; subtitle "Focus block · biceps, quads · every joint at loading stage 1 · ~17 min · 12 working sets"; pre-workout note: the upper and lower mobility pre halves, warm-up sets outside the exercise time, loads ≈60% of pre-layoff in weeks 1–2 and ≈80% in weeks 3–4. A — Superset 1 (~9 min · 3 rounds · 60–90 s after each pair): 1 preacher curl, biceps (L), 3 × 10–12, 2 RIR · wk 5+: 1, DB + bench ↕ 2 goblet squat above parallel, quads (M), 3 × 10–12, 3 RIR · wk 5+: 2, DB · low box. B — Superset 2 (~7.5 min · 3 rounds): 3 spider curl, biceps (M), 3 × 10–12, 2 RIR · wk 5+: 1, DB + bench ↕ 4 wall sit above parallel, quads (M), 3 × 32 s or more, ~12 s in reserve · wk 5+: ~8 s. Post-workout note: "After: mobility post halves · day after: no badminton", then "Quads and glutes collect sets here — badminton's day-before muscles (R21)" and the next-day step-gate line. Set-count box: biceps 6 · week 12 (2 above, R48); quads 6 · week 12 (2 above, R48). Alternatives: 1 preacher curl — gap, no L without the bench until shoulder stage 2; 3 spider curl — band curl with the elbows at the sides · standing cable curl. "v1 — new file: full-body focus session A, biceps and quads". No day, and no sessions a week: the state file keeps "2 a week" (D-14) | Laid-out working copy |
| S2.5 | R60 · R61 | — | Nothing renamed or renumbered elsewhere; new cards, so the catalogue's rows C040, C041, C065 and C068 gain "routine_fullbody_focus_A v1 ex. 1", "ex. 3", "ex. 2" and "ex. 4" | Catalogue provenance |
| S2.6 | R64 · R65 · R66 | Stage 1 R38 · R39 | Width estimate clean; PNG looked at; `pair_check.py`: preacher ↔ goblet squat is cross-region, spider ↔ wall sit has a hold as neutral partner — both PASS, as in Stage 1 §7 (S1.9) | Checks ✓ |
| S2.7 | R57 · R52 · R67 | — | Written to `gymplan/`; copied with `cp` to `gymtxt/`; `cmp` silent; register entry: lifting — focus sessions, upper + lower, generator; the block's first state file, `block_<NN>.json`: the fixture's Current state with `routine_fullbody_focus_A` at 2 a week, the plan's R46 checks, zone coverage and next steps (Stage 1 §7), a log row naming v1; `state_check.py` passes | Files and state file in place |
| S2.8 | R66 · §3.3 | — | Report: new, v1, generated; checks (1)–(10) ✓; dependents: none found (searched "preacher", "spider", "goblet", "wall sit" and their card numbers); follow-ups: none | Delivery report |

**Corpus quirks traced**

| Quirk | Step | Rule | Result |
|---|---|---|---|
| Upper focus A–C v8 state no sessions a week: "Focus block · 9 targets · upper joints at loading stage 2 · ~41.5 min · 26 working sets" | S2.4 | R58 · §3.2 | Passes: the state file keeps 1 a week each (D-14) |
| The v8 trio share one note: "… lat pulldown 4, pullover 3, biceps 7 · replaces v7" | S2.4 | R56 | Passes: one change across three files (D-06) |
| The v8 sport note | S2.4 | R59 | Passes |
| The v8 alternatives tables cite cards 1, 2, 3, 5 · 1, 3 · 1, 2, 4; all 21 rows in the corpus match their cards (M6) | S2.4 | R60 | Passes; the v6 drift (Stage 1 Supplement §5.2) is gone |
| "(Monday)", "(Wednesday)", "(Friday)" in the lower focus titles v3; "Friday cardio day" (M4) | S2.4 | R66 (5) · Stage 0 §0.1 | Failed; fixed 2026-10-14 by each file's next write: lower focus A–C v4, the popliteus protocol v6, `cardio_routine` v1 (M11) |
| `cardio_routine` had no version note (M2) | S2.4 | R56 | Its first write, 2026-10-14, added "v1 — …" |
| `foam_rolling_lowerbody_hEDS` v2: "hip thrusts (ex. 5)", while `routine_lowerbody` v4 holds the hip thrust as card 3 (Stage 0 M5) | S2.5 | R60 | Failed; fixed 2026-10-14 in v3: no routine numbers (D-03) |
| `stretching_upper_hEDS` v2's timeline: "Warmup sets A (3 min) → Working sets B–E (27 min)" | S2.5 | R60 | Failed; fixed 2026-10-14 in v3: "Pre half (~14 min) → warm-up sets → your gym session → post half (~16 min)" (D-03) |
| `evaluation_lowerbody` v1 carries a sport note, `evaluation_upperbody` v3 none | S2.4 | R59 | `evaluation_upperbody` passes; `evaluation_lowerbody`'s note goes at its next write (D-02) |
| `build_evaluation_lowerbody_v1.py` rebuilds `evaluation_lowerbody` byte-identical (M7) | S2.3 | R55 | A valid regeneration source while the md5 matches |
| A mirror sent through the upload route came back with C2PA metadata (2026-10-07) | S2.7 | R57 | Fails; `cp` on Harry's computer passes |
| `check_widths.py` stopped on both stretching files and `cardio_routine` (M8) | S2.6 | R64 | Fixed 2026-10-14 (T3); its 15 flags in the stretching files fit in the render |

**What Harry receives**

| Item | Value |
|---|---|
| File | `gymplan/routine_fullbody_focus_A.svg` v1 and `gymtxt/routine_fullbody_focus_A.txt`, byte-identical |
| Register | New entry in §9: lifting — focus sessions · upper + lower · generator |
| State file | The block's first `gymstate/block_<NN>.json`: Current state, routine A at 2 a week, the plan-only fields and one log row (R67) |
| Catalogue | Provenance lines for C040, C041, C065 and C068: new cards (R61) |
| Delivery report | Checks (1)–(10) ✓ · no dependents · no follow-ups |

Verified 2026-10-13: the section times (558 s and 459 s, the routine's last rest dropped) and the exercise time (≈17 min with 45 s holds, as Stage 1 §7 counts them) re-run in Python; the corpus measurements run on Harry's computer (§5.3); rule, step and section references checked by `xref_check.py`. Re-run 2026-10-14 after D-01…D-06: no sessions a week in the file; the register entry carries them. Re-traced 2026-10-25 after D-10…D-14: the state file carries the sessions a week and the plan-only fields.

---

## 8. References

W1–W5 were read by Claude on 2026-10-13 through a fetch summariser; quotes are worth a spot-check before they are relied on.

| ID | Source | Used for |
|---|---|---|
| W1 | W3C, Scalable Vector Graphics (SVG) 1.1 (Second Edition), ch. 19 "Animation", 16 Aug 2011, [w3.org/TR/SVG11/animate.html](https://www.w3.org/TR/SVG11/animate.html) | R62 |
| W2 | Can I use, "SVG SMIL animation", [caniuse.com/svg-smil](https://caniuse.com/svg-smil) — checked 2026-10-13: Chrome from 5, Edge from 79, Firefox from 4, Safari from 6 | R62 · §0.3 (d) |
| W3 | Liberation Fonts, [github.com/liberationfonts/liberation-fonts](https://github.com/liberationfonts/liberation-fonts) — "aims at metric compatibility with Arial, Times New Roman, and Courier New" | R64 · §0.3 (b) |
| W4 | oEmbed specification, [oembed.com](https://oembed.com/) — the `title` and `author_name` fields; its video example queries `https://www.youtube.com/oembed` | R63 |
| W5 | Coalition for Content Provenance and Authenticity (C2PA), [c2pa.org](https://c2pa.org/) — Content Credentials | R57 |

---

## 9. Register

The register's entries (`Stage2_RoutineFiles.md` §3.1 · R52 · D-01), as of 2026-10-22; stems that share role, regions and build are grouped. Which routines are current, with their sessions a week, sits in the state file (R67 · D-14) — since 2026-10-25 `gymstate/block_01.json`, which took over the sessions a week Harry gave on 2026-10-13.

| Stem | Role | Regions | Build |
|---|---|---|---|
| routine_upperbody_focus_A · _B · _C | Lifting — focus sessions | upper | generator |
| routine_upperbody · routine_lowerbody | Lifting — a general routine per region | upper · lower | generator |
| routine_lowerbody_focus_A · _B · _C | Lifting — focus sessions | lower | generator |
| popliteus_prevention_protocol | Joint protocol — a phased rebuild for one joint, the knee | lower | generator |
| evaluation_upperbody | Evaluation — the region's loading-gate tests (Stage 0 §2.5), with moving pictures | upper | build script `build_evaluation_upperbody_v3.py` (the generator with `figs.py`) |
| evaluation_lowerbody | Evaluation — as above | lower | build script `build_evaluation_lowerbody_v1.py` (self-contained) |
| evaluation_upperbody_2col | One-off copy — evaluation_upperbody v3 on two columns, not kept in step (Stage 0 D-83) | upper | build script `build_2col.py` |
| evaluation_lowerbody_2col | One-off copy — evaluation_lowerbody v1 on two columns, not kept in step (D-09) | lower | build script `build_evaluation_lowerbody_2col_v1.py` |
| stretching_upper_hEDS · stretching_lower_hEDS | Mobility — region-wide: active drills by target, a pre and a post half, for any training session of its region (Stage 0 §2.7; D-03) | upper · lower | hand-laid |
| foam_rolling_upperbody_hEDS · foam_rolling_lowerbody_hEDS | Foam rolling — region-wide: release areas by target, outside training sessions (Stage 0 §2.7; D-03) | upper · lower | hand-laid |
| cardio_routine | Conditioning — routine work under the hard gates (Stage 0 D-52 · D-53) | — | hand-laid |

Regions "—": a file whose sessions train no region (conditioning, Stage 0 §2.7).
