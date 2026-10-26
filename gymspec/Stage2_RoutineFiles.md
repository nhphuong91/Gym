# Stage 2 — Routine Files

**Normative · draft.** Binding on the implementation once frozen. Governed by `Stage0_PolicyDefinition.md` and `Stage1_Programming.md` (both draft, under Harry's review): cited by section and R-number, never restated.
Rationale, evidence, deferred material and the walkthrough → `Stage2_SupplementInfo.md`. `[HYP]` marks hypertrophy-specific content; everything else is goal-agnostic.

**Purpose.** Turn an approved Plan (Stage 1 §3.1) into routine files — `gymplan/<stem>.svg`, each with its byte-identical mirror `gymtxt/<stem>.txt` — and keep every routine file, its dependents, the register (§3.1 · Supplement §9) and the block's state file (§3.4) in step through later edits. Stage 2 decides no training content (Stages 0–1), assigns no days (Stage 0 §0.1) and leaves Harry's PDF exports alone (Stage 0 §0.1).

---

## 0. Decisions

### 0.1 Scope

| Item | Value |
|---|---|
| Input | **An approved Plan (Stage 1 §3.1), or an approved request that changes a routine file's text or layout and no plan field; plus the routine files and the block's state file (R67), read in place.** A change to a plan field — an exercise, dose, pairing, alternative, set count, exercise time or sport note — runs through Stage 1 first. |
| Output | **Routine files, each `gymplan/<stem>.svg` with its mirror `gymtxt/<stem>.txt`; every dependent a change reaches (R61); the register's entries (Supplement §9); the block's state file (R67); a delivery report (§3.3).** |
| Files covered | **Every file directly in `gymplan/` and `gymtxt/`, whatever its role (§3.1): lifting routines, joint protocols, evaluations, mobility, foam rolling and conditioning. Their `PreviousOldRoutines/` subfolders, and the one in `gympdf/`, are Harry's archive of retired files: outside the register and the file checks, and read only when he directs (D-15).** |
| Content | **Stage 2 lays out what the approved plan, or a test's Stage 0 §2.5 line, holds; it decides no exercise, dose, pairing or sport note.** |

### 0.2 Workspace and tools

| Item | Value |
|---|---|
| Workspace | **The Gym folder on Harry's computer, `D:\Extra_Works\Gym`, with fixed paths: `gymplan/`, `gymtxt/`, `gymspec/`, `gymtools/`, `gymstate/`** (Stage 0 D-12 · R49). |
| Generator | **`gymtools/svg_routine_generator/routine_generator.py`, imported and never edited: a tool, not a stored copy of any routine** (R55). |
| Kept build scripts | **`gymtools/svg/build_*.py`, each the definition that built one file version: tools, like the generator** (R55). |
| State files | **`gymstate/`, one JSON file per block (§3.4); R67 sets how it is read and written** (D-11 · D-12). |
| Cloud workspace | **Only for the steps Harry's computer lacks — today Chromium, for the render check and a look at its PNG** (R49 · R64). |
| Checks | **The gymtools checks R66 names, run as `gymtools/README.md` says.** |

### 0.3 Accepted limits

| # | Limit |
|---|---|
| a | The Gym folder keeps no version history: a replaced version is gone, and only its successor's version note says what changed. Accepted because a file is replaced only by a working copy that passed every file check (R51). |
| b | The width estimate counts characters, and the render check is one PNG from Chromium with Liberation Sans, not Edge on Windows. Accepted because Liberation Sans keeps the metrics of Arial, Edge's sans-serif on Windows (Supplement §5.4). |
| c | Dependents are found by searching for an exercise's name, its card number and item IDs; a file that refers to a routine without any of them is missed. Accepted because routine files carry no links to one another (Stage 0 D-15). |
| d | A moving picture plays only in a web browser; a PDF export or another viewer shows its still view (Stage 0 D-78). |

---

## 1. Steps

| Step | Input | Action items | Output |
|---|---|---|---|
| S2.1 Intake | Approved plan or request · the block's state file: Current state with its `current_routines` (Stage 0 §4.1 · R67) · register (Supplement §9) | Reach the Gym folder, or take the fallback (R50); read the newest state file (R67); read every target file in place and note its version; classify each change by scope (§2.1); search every routine file for the targets' exercise names, card numbers and item IDs to list the dependents (R61) | Targets with versions · scope per change · dependents |
| S2.2 Stem, build and method | S2.1 · register | New file: stem and v1 (R53), register entry (R52); existing file: build type from the register; edit method by scope and build type (R54) | Stem, build type and edit method per file |
| S2.3 Working copies | S2.2 | Copy every target and dependent to scratch outside the Gym folder (R51); for a regeneration, write the definition from the file just read, or confirm that the kept build script rebuilds it byte-identical (R55) | Working copies · regeneration source |
| S2.4 Lay out | Working copies · plan, request or Stage 0 §2.5 lines | Put each field in its block (R58 · §3.2), the sport note in the post-workout note (R59), pictures and links as R62 and R63 set; rewrite the version note (R56) | Laid-out working copies |
| S2.5 Dependents | S2.1 dependents · S2.4 | Update every reference to a changed name, number or ID in the dependents, each with its own version note (R56), and the exercise catalogue's provenance lines when an exercise, its card number or its pairing changed (R60 · R61) | Updated dependents |
| S2.6 Check | Every working copy | Width estimate and render check (R64); conventions (R65); `pair_check.py` on every file built from a plan (Stage 1 R38 · R39); the file checks (R66); a failed check goes back to S2.4 | Check results |
| S2.7 Write and mirror | Working copies that passed S2.6 | Replace each file in `gymplan/`; copy it byte for byte to `gymtxt/` on Harry's computer and compare (R57); update the register (R52); write the state file — the changed Current state fields, the plan-only fields and this conversation's log row — and run `state_check.py` on it (R67) | Files, mirrors and state file in place |
| S2.8 Deliver | S2.1–S2.7 | Write the delivery report (§3.3) with every file check, one line each per file (R66); list issues outside the request as follow-ups, unfixed | Delivery report |

---

## 2. Rules

| ID | Rule |
|---|---|
| R49 — Workspace | **Routine files are read, edited and built in the Gym folder on Harry's computer, at the paths of §0.2; a file goes to the cloud workspace only for a step the computer lacks, such as the render check (R64), and the folder's copy stays the source for every next step.** A cloud round trip per edit is slow and leaves copies that drift (Stage 0 D-12). |
| R50 — Folder out of reach | **When the Gym folder cannot be reached, the delivery says so, works from the files Harry attaches, and writes the results into the folder once it is back, after reading each target there again.** |
| R51 — Working copies | **Every change is made on a working copy in scratch space outside the Gym folder, and a file in `gymplan/` is replaced only by a working copy that passed every file check (R66).** The folder keeps no version history (§0.3 (a)). |
| R52 — Register | **Every file directly in `gymplan/` is listed once in the register — stem, role, regions and build (§3.1), its entries kept in Supplement §9 (D-01) — and the delivery that adds or retires a file or changes its build type updates its entry; a file moved to Harry's archive (§0.1) is retired.** |
| R53 — Stem and first version | **A plan's routine takes the stem of the routine it replaces, as that file's next version; a routine with no predecessor takes a new stem by the naming pattern of §3.1 and starts at v1.** The stem names the session, not the block; the version note records the change. |
| R54 — Edit method by scope | **Each change takes the edit method §2.1 gives its scope and the file's build type, and a change spanning several scopes takes the method of the widest.** The SVG's height follows its content, so a structure change cannot be patched in place. |
| R55 — Regeneration source | **A regeneration builds from the file just read: a routine definition written from that file, or a kept build script that rebuilds that file byte-identical when run just before the change; the generator and every kept script stay unchanged, and a changed build runs from a copy.** A definition held in a tool would revert every direct edit made since it was written. |
| R56 — Version note | **Every routine file ends with one version note, "vN — <change>", naming the change its latest write made — for a change made across several files, the whole change or this file's share of it (D-06); every write raises N by one and rewrites the note, and a file without a note gets "v1 — …" at its first write.** |
| R57 — Mirror | **Every SVG written to `gymplan/` is copied byte for byte to `gymtxt/<stem>.txt` on Harry's computer in the same delivery, and the two files compare identical before delivery.** The mirror stands in for its SVG when files must be attached (Stage 0 D-13). |
| R58 — Source in the file | **A routine file built from a plan carries every field §3.2 gives the file, with the plan's values, in the block §3.2 names, and nothing §3.2 keeps in the plan; a test card carries its Stage 0 §2.5 line — the test, its range, load, side, pace and end point.** Harry trains from the file, so it holds what he applies set by set. |
| R59 — Sport note | **The sport note Stage 0 R21 requires sits on the first line of the post-workout note as "day after: no <sport>" for each sport it names, and the next line names the muscles from that sport's avoid-the-day-before list that collect sets in the routine; a routine that names no sport reads "day after: no sport limit". An evaluation file carries none (D-02): its tests are not training sets (Stage 0 D-85).** |
| R60 — Reference form | **A reference inside or across routine files cites an exercise by its card number with its name beside it, and a mobility item by its ID (Stage 0 D-15); every number it cites belongs to the cited file's current version. A region-wide file — mobility or foam rolling — cites no routine: it lists its drills or areas by target (muscle groups, joints, tendons or spots) for any session of its region, and Harry picks from it by the session's targets (D-03).** |
| R61 — Dependents | **A write that renames, swaps, removes or renumbers an exercise, or changes an item ID, updates every reference to it in the same delivery — found by searching the routine files for the old name's core words, case-insensitive, and for the ID — each routine file with its own version note (R56). The exercise catalogue's provenance lines change only when an exercise, its card number or its pairing changes; a version that changes none of them leaves the catalogue as it is (D-04).** |
| R62 — Moving pictures | **A picture on a card is one self-contained group marked `<!-- PIC n — label -->` in the card's picture box (§2.2): its SVG animation (SMIL) plays in Edge or Chrome, its still view shows the start pose solid and the end pose faint, its card is tall enough for both text and picture, and a regeneration carries the group over unchanged from the file just read (Stage 0 D-78).** |
| R63 — Links | **Every link a routine file carries was checked before delivery by its title and its channel or publisher — a video through its oEmbed answer — and names the movement or source its card cites; where a linked video differs from its card, the card holds (Stage 0 D-79).** |
| R64 — Width and render check | **Before delivery, every written SVG passes the width estimate of §2.2 and is rendered in Chromium with sans-serif set to Liberation Sans, and the PNG is looked at; a file with moving pictures also renders the start and the end of the cycle with no console errors.** |
| R65 — SVG conventions | **Every written SVG follows §2.2 — UTF-8 with LF line endings, a 680 px page, the version note as its last text, the picture box — and an edit keeps every other feature of the file's own form.** |
| R66 — File checks | **Before delivery, the delivery report lists for every written file the result of each check below, and names each failure with its fix.** (1) Edit method matches scope and build type (R54 · R55). (2) Version note raised by one and accurate (R56). (3) Mirror identical (R57). (4) Width estimate, render check and conventions (R64 · R65). (5) Fields in their blocks with the plan's values (R58), the sport note (R59), pictures and links (R62 · R63), and no day (Stage 0 §0.1). (6) References and dependents updated (R60 · R61). (7) On a file built from a plan, every pair passes Stage 1 R38 and R39 by `pair_check.py`. (8) Register entry (R52). (9) Nothing changed outside the request: a text diff of the working copy against the file just read shows only the requested change. (10) State file written, and `state_check.py` passes on it (R67). |
| R67 — State file | **Each block keeps one state file, `gymstate/block_<NN>.json` (§3.4), numbered on from the last block's, and the highest number is the current block. A conversation that plans or edits routine files reads it first and asks Harry only what it does not hold; a new block (Stage 0 §2.4) starts the next number and leaves the earlier files as they are. A conversation that changes Current state, approves a plan or writes a routine file updates the file before it ends — every changed field, the approved plan's plan-only fields (§3.2) and one log row with the date, the changes (fields, plan, files with their versions) and the open follow-ups — and `state_check.py` passes on it.** Without it, every field is asked again and the plan-only fields end with the chat (D-10 · D-13). |

### 2.1 Edit method by scope

R54's methods. A new file is built by the generator, or by a new build script kept in `gymtools/svg/` with its README row when the generator has no model for its cards (evaluation cards with pictures).

| Scope | What it covers | Generator or build-script file | Hand-laid file |
|---|---|---|---|
| Text | A swap that keeps the card's height, a set count, reps, RIR, rest, a cue, a note, a link, the version note | `str_replace` on the working copy | `str_replace` on the working copy |
| Shift | A change that moves many elements while the sections, their order and the card heights stay | A throwaway Python script on the working copy | A throwaway Python script on the working copy |
| Structure | Sections, their order, card heights, layout or colours — any card-height change | Regenerate the whole file (R55) | A throwaway Python script on the working copy: a hand-laid file has no model to regenerate from |

### 2.2 SVG conventions

R64's width estimate and R65's conventions, as the corpus holds them (Supplement §5.3).

| Item | Convention |
|---|---|
| Page | `viewBox` 680 px wide, its height set by the content; root `font-family: sans-serif`. A one-off two-column copy runs 1,360 px (Stage 0 D-83 · D-09). |
| Encoding | UTF-8, LF line endings. |
| Width estimate | 0.5 px per character per point of font size (size 9 = 4.5 px, 11 = 5.5 px, 15 = 7.5 px); no text past x 650; a card title ends before x 484, left of the sets column at x 490; text inside a picture stays within its 154 px. |
| Picture box | 156 × 132 px at x 486 on its card, one group per picture (R62). |
| Version note | The last text element: font size 9, centred on the page; generator files put `<!-- VERSION NOTE -->` before it. |
| Comments | Generator and build-script files mark each section `<!-- ── X LABEL ── -->`, each card `<!-- Xn — label -->` and each picture `<!-- PIC n — label -->`; hand-laid files keep their own. |

### 2.3 Rule examples

Each rule passes when the implementation produces the *Pass* behaviour and fails when it produces the *Fail* behaviour. Fixtures: the canonical example's plan (Stage 1 §7, "What Stage 2 receives") for a new file; the corpus as read on 2026-10-13 (Supplement §5.1) for edits. Values are illustrative.

| Rule | Pass | Fail |
|---|---|---|
| R49 — editing focus A | Focus A is edited on Harry's computer and staged to the cloud only to render its PNG | Every routine file is staged to the cloud, edited there and committed back; or the next edit starts from the cloud copy |
| R50 — folder out of reach | "The Gym folder is out of reach: working from the focus A you attached; v9 goes into the folder once it is back" — and, once back, focus A is read there again before the write | The edit is made from a memory of v8 without saying so; or the attached copy is written over a newer file in the folder |
| R51 — changing focus A | Focus A copied to scratch, edited, checked, then written over `gymplan/routine_upperbody_focus_A.svg` | `sed -i` run on the file in `gymplan/`; or a working copy saved in `gymplan/` beside it |
| R52 — new routine | `routine_fullbody_focus_A` is written with its entry: lifting — focus sessions, upper + lower, generator | The new file has no entry; `evaluation_lowerbody` stays listed as "generator" though its build script draws without the generator; or `cardio_routine`, moved to the archive, keeps its entry |
| R53 — new upper block | Session A of the current upper block replaced `routine_upperbody_focus_A` v6 as its v7; the first full-body session starts `routine_fullbody_focus_A` at v1 | Session A written as `routine_upperbody_hyp_A` beside the old focus A; or the full-body file started at v0 or v2 |
| R54 — three changes | A set count 3 → 4 on focus A by `str_replace`; a new pair section in focus B by regenerating the file; the court phase cut from `cardio_routine` by a throwaway script | A new section patched into focus B with `str_replace`; or `cardio_routine` pushed through the generator |
| R55 — regenerations | Focus B regenerated from a definition written from its v8 SVG; `evaluation_lowerbody` rebuilt by `build_evaluation_lowerbody_v1.py` after its output matched md5 f75c935d… | Focus B regenerated from the generator's bundled upper-body example; `evaluation_upperbody` rebuilt from its v3 script after a v4 text edit, losing that edit; or `routine_generator.py` edited for a new card style |
| R56 — version notes | Focus A v8 → v9, "v9 — preacher curl 4 → 3 sets"; the v8 trio's one note for the re-pairing made across all three files; `cardio_routine`'s first write added "v1 — …" | v8 → v10; the v8 note left after a write; a note naming an older change; or two notes in one file |
| R57 — focus A v9 | Written to `gymplan/`, copied with `cp` to `gymtxt/` on Harry's computer; `cmp` silent | The mirror sent through the upload route comes back with C2PA metadata; or the SVG at v9 beside a v8 mirror |
| R58 — canonical routine A; step-down card | Subtitle with block type, targets, loading stage, exercise time and working sets; cards with zone, cues, RIR for weeks 1–4 and from week 5; loads ≈60% in weeks 1–2 and ≈80% in weeks 3–4 in the pre-workout note; set-count box, alternatives table, sport note. The step-down card paced "60: 2 beats down, 2 up", as Stage 0 §2.5 sets it | Cards without RIR; the alternatives table left out; the R46 check list printed in the file; or the step-down card paced 1 beat each way |
| R59 — sport notes | "After: mobility post half · day after: no archery", then "Chest, delts, back, triceps and abs collect sets here — archery's day-before muscles (R21)"; a hamstring-and-adductor routine: "day after: no sport limit"; `evaluation_upperbody` v3 with no sport note | The note only in the rules box; "day after: no archery" with no muscles named; no line at all in a routine that names no sport; or `evaluation_lowerbody`'s "Day after: no badminton" line kept at its next write |
| R60 — references | Focus A's alternatives row "5 Overhead cable triceps ext." for card 5; "from upper body mobility protocol S2" in `cardio_routine`; `foam_rolling_upperbody_hEDS` v2: "Rhomboids · mid-trap — loaded by rows", no routine number | An alternatives row citing card 7 for the card numbered 5; "hip thrusts (ex. 5)" in a foam-rolling file, as v2 had it (Stage 0 M5); or a mobility timeline naming a routine's sections |
| R61 — an ID and a card move | S2 of `stretching_upper_hEDS` renumbered S3: `cardio_routine`'s "from upper body mobility protocol S2" becomes "S3", with its own note, in the same delivery. The hip thrust moves from card 5 to 3 in `routine_lowerbody`: every in-file reference to it and the catalogue's line for it change in the same delivery; a later cue-only version leaves the catalogue as it is | `cardio_routine` left citing S2; `cardio_routine` updated without its own note; the catalogue left citing card 5 for the hip thrust; or a catalogue revision made for a cue-only version |
| R62 — evaluation pictures | Each of `evaluation_lowerbody`'s 13 pictures is one group at x 486, start pose solid and end pose faint when paused; a regeneration copies the groups from the file just read | A picture split over two groups; a still view showing the end pose only; or pictures redrawn from `figs.py` over hand-edited ones |
| R63 — step-down video | Linked after its oEmbed answer gave a title naming the step-down and a physiotherapy channel; the card keeps its pace where the video differs | A link added unchecked; a video titled for another movement; or the card's pace changed to the video's |
| R64 — focus A; evaluation_upperbody | Focus A: width estimate clean, PNG looked at. `evaluation_upperbody`: frames at the start and the end of the cycle, no console errors | Delivered on the width estimate alone; a title past x 484 into the sets column; or an animated file delivered without its frames |
| R65 — new file | 680 px page, UTF-8, LF, the version note last | Saved with CRLF; the version note above the alternatives table; or a 700 px page |
| R66 — delivery | The report lists checks (1)–(10) per file with ✓ or ✗; the diff shows only the swapped card | "All checks pass" with no list; or a diff showing a cue the request did not name, delivered anyway |
| R67 — state file | The canonical example's delivery starts the next file, `block_<NN>.json`: the fixture's Current state, `routine_fullbody_focus_A` at 2 a week, the plan's R46 checks, zone coverage and next steps, and a log row naming v1; `state_check.py` passes, and the next conversation reads it and asks nothing it holds | The plan's next steps stay only in the chat; the next conversation asks the priority targets again; a new block overwrites the last block's file; or the knee's move to loading stage 2 is agreed in chat while the file still reads 1 |

---

## 3. Schemas

### 3.1 Register — one entry per routine file

The register's entries sit in Supplement §9 (D-01); this section sets their fields and the naming pattern. Which routines are current, with their sessions a week, sits in the state file (§3.4 · D-14).

| Field | Definition |
|---|---|
| `stem` | The file name without folder or extension; the SVG, its mirror and Harry's PDF export share it |
| `role` | Lifting · joint protocol · evaluation · mobility · foam rolling · conditioning · one-off copy. Mobility and foam rolling are region-wide: menus by target for any session of their region (R60) |
| `regions` | The regions its sessions train (Stage 0 §2.7), or "—" |
| `build` | Generator · build script, named · hand-laid (§2.1) |

**Naming pattern for a new stem.** Lifting: `routine_<upperbody|lowerbody|fullbody>` for a general routine, and `routine_<…>_<focus|maintenance>_<A, B, C…>` for the sessions of a focus or maintenance block (Stage 0 §0.3), lettered in plan order. Evaluation: `evaluation_<upperbody|lowerbody>`. Joint protocol: `<structure>_prevention_protocol`. Mobility: `stretching_<upper|lower>_hEDS`; foam rolling: `foam_rolling_<upperbody|lowerbody>_hEDS`. A one-off copy: its source's stem plus a suffix naming the difference, e.g. `_2col`.

### 3.2 Routine-file layout — a file built from a plan

Blocks from top to bottom, as the upper focus files v8 hold them (Supplement §5.2); Stage 1 §3.1 names the plan fields.

| Block | Carries | Plan field |
|---|---|---|
| Title | Regions, goal and session letter, e.g. "Upper body hypertrophy — Session A" | `routines` name |
| Subtitle | Block type · priority targets, named or counted · the trained joints' loading stage · exercise time · working sets | `header` · `routines` |
| Legend | The muscle groups the cards colour | — |
| Pre-workout note | The mobility pre half by name (Stage 0 §2.7) · warm-up sets outside the exercise time (Stage 0 R19) · the load band (Stage 0 R22) | `exercise_row` load band |
| Section header | One per pair or straight block: its muscles, minutes, rounds and the rest after each pair or set | `exercise_row` pairing and rest |
| Card | Number · exercise · prime mover with its zone, and the assisting muscles · cues, and each warning with its rule (⚠) · sets × reps, or sets × hold time · RIR for weeks 1–4 and from week 5 (Stage 0 R18), or seconds in reserve (Stage 0 R16) · stations or equipment. Partners are joined by "↕ then immediately", the first partner on top (Stage 1 R39) | `exercise_row` |
| Post-workout note | The mobility post half by name · the sport note (R59) · the next-day step-gate line (Stage 0 R20) | `routines` sport note |
| Rules box | The rules Harry applies set by set, each with its R-number: tempo and soft bend, range, the abort, RIR by block week, the unilateral gate, holds, the progression step, the step-gate log | `header` · `progression` |
| Timing summary | The session timeline from the pre half to the post half · exercise time by Stage 1 R40, with its basis · working sets | `routines` exercise time |
| Set-count box | Per priority target: sets in this session · weekly direct sets + harvest, and any sets above the target (Stage 1 R33 · R34 · R48) | `set_count` |
| Alternatives table | Per station exercise: card number and primary, alternative 1, alternative 2 or the named gap, each warning marked ⚠ with its rule | `alternatives` |
| Version note | "vN — change" (R56) | — |

Kept in the plan and the state file (§3.4), not in the file — the plan-only fields: the R46 check list, the zone-coverage lines (each card carries its zone), the next step per exercise (the rules box carries Stage 1 R42 as one line) and the Stage 0 R24 statement. The routine's sessions a week sit in the state file, not in the file (D-05 · D-14), as Stage 0 §0.1 says.

### 3.3 Delivery report — one per delivery

| Field | Definition |
|---|---|
| `files` | Per written file: stem, old → new version (or "new, v1"), scope and edit method (§2.1) |
| `checks` | R66's checks (1)–(10), one line each per file, ✓ or ✗ with the fix |
| `dependents` | Each dependent updated, with its new version; or "none found", with the search run |
| `register` | The entry added, changed or retired; or "unchanged" |
| `state` | The state file's changed fields and its new log row, with the `state_check.py` result (R67) |
| `follow_ups` | Issues seen outside the request, listed and left unfixed (`CLAUDE.md` `<task>`) |

### 3.4 State file — one per block

`gymstate/block_<NN>.json`, UTF-8 JSON, numbered from `01` (D-11 · D-12). The block start is Harry's and is not kept (Stage 0 D-91).

| Field | Definition |
|---|---|
| `block` | The file's number, as in its name |
| `current_state` | Every Stage 0 §4.1 field with its value; `current_routines` lists each routine's `stem`, `regions` and `sessions_week` (D-14) |
| `plan` | The approved plan's plan-only fields (§3.2): `version`, `approved` (date), `routines` (each stem with the version built from the plan), `checks` (Stage 1 R46), `zone_coverage`, `progression` (the next step per exercise), `suspensions` (the Stage 0 R24 statement, or null). Null until the block's first plan |
| `log` | One row per conversation that changed the file (R67), oldest first: `date`, `changes` (fields, plan, files with their versions), `follow_ups` (open issues, each kept until a later row closes it) |

Invariants: the Stage 0 §4.1 invariants hold; every current routine is a file in `gymplan/` with a register entry (R52), and trains only regions the block trains; no field outside this table and Stage 0 §4.1; log dates never go back. `state_check.py` tests them (R66 (10)).

---

## 4. Open items

None. Round 1 closed 2026-10-15 (Supplement §3, D-01…D-08); D-09 recorded 2026-10-22; D-10…D-14 recorded 2026-10-24 and 2026-10-25; D-15 recorded 2026-10-25.
