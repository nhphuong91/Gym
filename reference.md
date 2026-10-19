# reference.md — programming reference (instructions point here by §)

## R1 Staged-loading gate — exit criteria and unlock order
Moved to Stage 0 §2.5 · R14 (Supplement §2.1 · D-75).

## R2 Evidence baseline — regional growth and exercise selection (verified Sep 2026)
- Long-muscle-length training: small overall advantage; distal-targeting effect trivial and uncertain at the ~22% length differences typical of real exercises (Varović et al. 2025, meta-analysis). Lengthened partials ≈ full ROM in trained lifters (Wolf et al. 2025). Hence L is the preferred slot for total growth, and distal targeting is not a programming goal.
- Regional bias follows the resistance profile: preacher vs incline curl gave distinct regional growth (Zabaleta-Korta 2023; Kassiano 2025); shoulder angle alone, profile matched, gave none (Attarieh 2025; Front. Physiol. 2026).
- Overhead extension grew the triceps long head ~1.5× more than pushdowns (Maeo 2023) — the two-joint case where L matters most.
- Systematic exercise variation → more uniform growth (Fonseca 2014); random high-frequency rotation does not help (Kassiano 2022).
- S (short-length) work carries no cited growth advantage in this file; it is programmed for joint safety, not growth stimulus (§R5).
- Zone label convention: preacher curl = L (early ROM), overhead extension = L, spider curl = M, cable pushdown = M.

## R3 Format examples
- Exercise row — Preacher curl · DB + bench · L · 3 × 10–12, 2 RIR · 60–90 s · straight · —
- Set-count row — Biceps · target 10 · harvest 5.0 (10 pulling sets × 0.5) · direct 5 + 2 buffer = 7 (harvest ≥50% of target) · total 12.0 fractional.
- Capacity line — Σ direct after buffer 59 (= Σ working sets) ≤ 84 (28 × 3 sessions) ✓ · no session over 28 working sets or 8 fractional sets per muscle ✓
- Zone coverage line — biceps L + M ✓ · triceps L + M, no S (permanent shortfall) ✓ · rear delt M + S, S capped at the torso plane ✓
- Alternatives row — Primary: cable overhead triceps extension (cable, L). Alt 1: seated two-hand overhead DB extension, back supported (L, warning: brace scapula). Alt 2: band overhead extension anchored high on the frame (L, consistent line of pull).
- Superset check — Smith incline press + cable seated row: valid (rule 1; grip demand does not compromise the press, rule 4). Smith incline press + cable pushdown: invalid (pushdown pre-fatigues triceps, the press's key synergist, rule 3).
- Sport verdict — Incline DB curl: red (free-hanging shoulder extension under load; no growth advantage over a supported curl, Attarieh 2025). Preacher curl: green (same growth stimulus, supported shoulder, L).

## R4 Generator and SVG conventions
- Text extraction from an SVG or its .txt mirror: grep -oP '(?<=>)[^<]{8,}(?=</text>)' <file> | grep -viE '^(x=|y=)'.
- Generator run: python3 -B, so no __pycache__ lands in gymtools/svg_routine_generator/; a scratch script puts that folder on sys.path, imports from routine_generator and writes render() output to the working copy.
- Visual check: render the SVG in Chromium in the cloud workspace with sans-serif set to Liberation Sans (Arial metrics, as in Edge on Windows), then view the PNG.
- Helper scripts: gymtools/ (see its README, stored 2026-10-09) keeps the generator (gymtools/svg_routine_generator/, moved from the Gym folder root on 2026-10-09) and the tools earlier sessions built: the picture helpers and the build behind evaluation_upperbody v3, the two-column copy, width and animation-frame checks, the catalogue build and checks, and the Stage 0 cross-reference check. They are tools, not stored copies: rebuild a routine from the SVG just read, and check catalogue/rows.py against gymspec/ExerciseCatalogue.json before building.
- Line endings: SVGs, .txt mirrors and every .md file, CLAUDE.md and reference.md included, use LF (checked 2026-10-08); an edit keeps the file's own.
- Dataclasses: Routine, Section, Exercise, Pair, InfoBox, RulesBox, SetCountBox, SetCountEntry, AlternativesTable, AltRow; render(). card_height_override = 70 for 3-detail cards, 86 for 2-subtitle cards. New muscle colors: monkey-patch MUSCLE_COLORS with MuscleColor.
- Layout: 680 px wide; section headers gray #e8e8e8, left-aligned, size 12 weight 500, height 24, rx=4; legend 2-line, swatches at x=50; overflow check by char-width heuristic (size 11 = 5.5 px, 12 = 6.0, 9 = 4.5) against the 650 px right edge.
- Cable exercises (all occupy the one cable unit): rows, pulldowns, pullover, curl, pushdown, lateral raise, external rotation, reverse fly, overhead extension.
- Interim file rules (Stage 0 D-74 · D-76 · D-78): replaced by Stage2_RoutineFiles.md (Stage 2 D-07).

## R5 Rationale
Scaffold
- The prompt is goal- and sport-agnostic: block goal, priority targets and in-season sport change from block to block, so they live in Current state and are set at the start of each conversation. Sport profiles hold what each sport demands and loads, so rules can key off whichever sport is in season.
- Goal-table adaptations for hEDS: hypertrophy reps sit above NSCA's 6–12 (equal growth at lower absolute joint load, §R6); hypertrophy rest starts at 60 s (§R6); where a row leaves a choice, the most RIR it permits is taken, because technical failure precedes muscular failure in hypermobile joints. Power RIR ≥3, endurance RIR 1–3 and general-fitness RIR 2–4 are judgement calls, not cited values.
- Weekly per-muscle targets exist for hypertrophy only: the dose-response evidence here (§R6) is strongest for hypertrophy, so other goals are dosed per exercise from their row.
- Priority (3) is "goal fit": where this file gives "stimulus" a specific meaning it means growth, so a power or endurance block would be ranked on hypertrophy criteria. Goal fit points to a per-goal selection criterion in <dosing>. "Specificity" was avoided: it reads as sport specificity, which is priority (5). Power evidence: movement, load and velocity specificity drive power gains, with ballistic, plyometric and Olympic-lift exercises as the primary tools (Cormie, McGuigan & Newton 2011, Sports Med 41:125–46). (D5)
- One goal per region: mixing goals between regionally close muscles is hard to plan and execute; an upper/lower split is not (Harry, Sep 2026). Trunk sits with upper body. (D3, D4)
- Rules are phrased as what to do: Anthropic's prompting guide advises stating what to do rather than what not to do, giving the reason (Claude generalizes from it), and dropping forceful emphasis on current models ("Prompting best practices", platform.claude.com, checked Sep 2026). (D6)
Tooling
- Card-height changes regenerate because SVG height auto-scales; str_replace cannot re-flow everything below the change.
- Minor edits go straight to the file; major edits regenerate it whole, because patching a large change piece by piece costs more tokens than regenerating. The generator is a tool, not a stored copy: regeneration rebuilds from the file just read, so a stale definition in routine_generator.py never reverts a direct edit.
- The .txt mirror is written with every SVG write: it stands in for the SVG whenever files must be attached, and a stale mirror means planning from an outdated routine.
- Work stays on Harry's computer: copying a file to the cloud workspace and back is slow and leaves two copies that can drift. The cloud workspace serves what the computer lacks — Chromium and image viewing.
Joints
- hEDS/HSD is systemic, so every joint is treated as unstable and <constraints> apply unconditionally. <gates> adds staged loading for a joint that currently needs more than baseline; an empty gate means no joint needs extra staging, not that any joint is unrestricted.
- Stages are gated on control, not range: hypermobile joints already have excess range.
- No passive stretching: muscles tighten protectively around unstable joints and stretching removes that tone; foam rolling addresses the tightness sensation without end-range lengthening.
- Lats can over-activate in multidirectional shoulder instability; lower/mid traps are usually under-recruited; upper trap compensates.
- The in-session abort and the step gate answer different questions: the abort decides the current set, the step gate decides next week's dose.
Exercise selection
- S is chosen for joint safety, not growth stimulus (§R2): for muscles whose risky position is the stretched end, S puts peak tension away from it. Where the shortened position is itself terminal (triceps: full elbow extension), no S exists.
- Bands first for S: band tension rises with elongation, so it peaks where the muscle is shortest; bands are owned, so S coverage never waits on an occupied machine. Ownership also makes the band the tie-breaking alternative.
- When a gate blocks every L option, M is the fallback: L's advantage is small (§R2), so little is lost and the gate never bends.
- Long-limbed lifters get disproportionate visual payoff from regional distribution (more muscle length between tendons).
- Hip abductor/adductor machine: available; program when relevant.
Dosing and schedule
- Focus blocks drop unlisted muscles entirely instead of holding them at maintenance: capacity concentrates on the block, and detrained size returns within the first retraining weeks (§R6, muscle memory). Maintenance for all muscles is the final phase, set once every focus block is done.
- 48 h between lifting sessions is joint recovery. Capping lifting at 3 sessions/week costs no growth, because frequency has no detectable effect once weekly volume is matched (§R6).
- The per-session cap is a joint-control limit: control degrades with fatigue in hypermobile joints, so the cap is never raised to fit a plan.
- Sport-day rules key off the sport's profile: the day before protects what the sport needs (fatigue there costs performance and, with hEDS, joint control under fast multidirectional load); the day after checks the joints the sport just loaded before lifting loads them again.
- Reps + RIR only: 1RM testing is avoided in this population (§R6), and excluding RPE keeps a single effort scale across every plan.

## R6 Dosing — evidence and rationale
Set units
- Direct vs indirect: a set is direct for the muscle that is its primary force generator, and indirect for a muscle that contributes meaningfully without being the primary force generator. 'Fractional' volume counts indirect sets as 0.5; it fitted hypertrophy data better than counting them as 1 ('total') or 0 ('direct') (Pelland et al. 2025, below).
- Indirect sets likely contribute less than half: the same group's exploratory re-analysis put an indirect set at ~32% of a direct set for hypertrophy and ~16% for strength (Remmert et al. 2025, SportRxiv preprint). Basis for the <dosing> buffer: +2 direct sets when harvest supplies ≥50% of a muscle's target.
- Harvest needs a real compound behind it: shoulder abduction (lateral deltoid) and most rotation have no meaningful compound driver, so those muscles harvest nothing (anatomical reasoning).
- Isolation added to multi-joint training: no significant extra elbow-flexor growth in untrained men over 10 weeks (Gentil et al. 2013, Appl Physiol Nutr Metab, ultrasound) or in trained men over 8 weeks (de França et al. 2015, Appl Physiol Nutr Metab 40:822–6, arm circumference only, n = 20); one untrained 8-week trial reported larger arm-circumference gains with isolation added (reported by Gentil's group, citation not verified). Small, short, volume-unequated, mostly crude measures — consistent with indirect sets counting for something, not with dropping direct work.
Volume
- Volume drives growth; frequency does not once volume is fixed: hypertrophy rises with weekly sets on a square-root curve with no detectable superiority beyond ~31 fractional sets/week; frequency slope +0.32 %/extra day, interval crossing zero. Synergist sets counted at 0.5 fit the data best. (Pelland, Remmert, Robinson, Hinson & Zourdos 2025, Sports Med, DOI 10.1007/s40279-025-02344-w; 67 studies, n = 2,058.) So how a weekly total is split across sessions matters little for growth.
- Minimum effective dose ≈ 4 fractional sets per muscle per week (Pelland et al. 2025 as reported in secondary summaries — not checked against the paper; consistent with Iversen et al. 2021, "No Time to Lift?", Sports Med).
- Per session: returns flatten at ~11 fractional sets per muscle for hypertrophy and ~2 direct sets for strength (PUOS — the volume beyond which extra sets have <50 % probability of a detectable gain; counted per muscle, not per exercise; Remmert et al. 2025, SportRxiv preprint, same dataset). Data are thin above ~10 sets/session (mean 5.95 ± 4.49, range 0–24), hence a soft cap; Krieger's earlier analysis put the bend at 6–8 total sets with ≥2 min rest. The analysis defines a ceiling only, no per-session floor; the first set of a session gives the largest marginal gain. <dosing>'s ceiling sits below ~11 on purpose: joint control degrades with fatigue in hypermobile joints. For strength, the authors favour shorter, more frequent sessions over piling sets into one — the basis for spreading strength and power sets across every available session.
- Progressing volume in steps beats holding it: +4 or +6 sets every 2 weeks outperformed constant volume over 12 weeks in trained men (strength clearly, hypertrophy small). Harry's step is 1–2 sets, not 4–6. (Enes, De Souza & Souza-Junior 2023, MSSE, DOI 10.1249/MSS.0000000000003317.)
Effort, reps, rest and load
- Proximity to failure: hypertrophy improves gradually as sets end closer to failure; strength gain does not (Robinson et al. 2024, Sports Med 54:2209–31). With volume matched, failure vs non-failure gives similar hypertrophy (Refalo et al. 2023, Sports Med 53:649–65). Both from verified reference lists, not re-fetched. Why 1–3 RIR: most of the growth stimulus with less fatigue per set, and technical failure precedes muscular failure in hypermobile joints.
- Rep-range equivalence: growth is similar across ~6–30 reps when effort is matched (Schoenfeld et al. 2017 load meta-analysis; Lopez et al. 2021 — not re-checked). Higher reps are preferred for the lower absolute joint load, not for growth.
- Rest: a small hypertrophy benefit for inter-set rest >60 s and no appreciable difference beyond 90 s (Singer et al. 2024, Front Sports Act Living, DOI 10.3389/fspor.2024.1429789); 3 min beat 1 min for size and strength in trained men (Schoenfeld et al. 2016, JSCR, DOI 10.1519/JSC.0000000000001272). Rest length had no meaningful effect on the per-session PUOS (Remmert et al. 2025).
- Goal table source: sets, reps, rest and %1RM by training goal follow the NSCA's load-and-repetition and rest-period assignments (Haff & Triplett 2016, Essentials of Strength Training and Conditioning, 4th ed.). Its "sets" are per exercise per session, not per muscle per week.
- %1RM ↔ repetition maximum (NSCA training load chart, adapted from Landers 1984): 1RM 100 % · 2RM 95 · 3RM 93 · 4RM 90 · 5RM 87 · 6RM 85 · 7RM 83 · 8RM 80 · 9RM 77 · 10RM 75 · 12RM 67. Translating without testing a 1RM: a load's RM = reps performed + RIR, so a %1RM band becomes an RM band (e.g. 67–85 % ≈ 6–12RM) and is prescribed as reps + RIR whose sum falls inside it. Hence the strength row runs 3–5 reps rather than NSCA's ≤6: compounds keep ≥1 RIR, and ≥85 % caps reps + RIR at 6.
- Load-step size: ACSM's 2–10 % rule (Ratamess et al. 2009 position stand, not re-checked); hEDS takes the bottom of it.
Hypermobility-specific
- Heavy loading is compatible with hEDS/HSD when ramped and symptom-gated: high-load, full-range shoulder strengthening in 100 HSD patients over 16 weeks was tolerated and superior to low-load mid-range (Liaghat et al. 2022, BJSM 56:1269–76, DOI 10.1136/bjsports-2021-105223). Feasibility ramp: weeks 1–3 at 50–90 % of 10RM → 3×10RM → 4×8RM, load up only when all reps complete with acceptable symptoms (Liaghat et al. 2020, via Zabriskie 2022, J Funct Morphol Kinesiol 7:61). Harry's gate matches the study's ≤5/10.
- Hypermobile people strengthen at a normal rate from a lower start (~40 % in 12 weeks; To & Alexander 2019, Arch Phys Med Rehabil 100:1243–50); a self-directed program that under-progressed load produced no gains (Luder et al. 2021). 1RM testing is avoided in this population → reps + RIR. Slow ≠ static.
- Muscle memory: 10 weeks of detraining did not compromise total adaptation and losses returned within the first retraining weeks, size faster-lost than strength (Halonen et al. 2024, Scand J Med Sci Sports, DOI 10.1111/sms.14739); <8 weeks retraining regained 1RM in older men (Blocquiaux et al. 2020, Exp Gerontol). Hence the 60/80/100 % ramp is paced by joint tolerance, not by muscle.
- Deloads: a full week off mid-block gave no hypertrophy benefit and slightly less strength (Coleman et al. 2024, PeerJ 12:e16777) → symptom-triggered, sets halved, loads kept.

## R7 Sport profiles — evidence (checked Sep 2026)
Grade: A peer-reviewed data on the sport · B related population, small sample or secondary citation · C coaching source or reasoning · H Harry's account. Volume/page numbers not all re-checked.
Archery (Olympic recurve — H)
- Clicker reaction time, draw force and post-release sway speed predicted shot score in 39 elite recurve archers (Spratford & Campbell 2017, Eur J Sport Sci 17:539–45). A
- Middle and posterior deltoid drive draw-side horizontal abduction through the draw and release (Simsek & Ertan, ISBS case study — year not captured). B
- Skill groups differed in flexor digitorum superficialis, extensor digitorum, middle and posterior deltoid and all three trapezius parts (Simsek, Cerrah, Ertan & Soylu 2018, S Afr J Res Sport Phys Educ Recreat 40:141–55 — details from a reference list). A
- Scapular muscle activity damps upper-arm tremor at full draw (Lin et al. 2010, J Sports Sci 28:415–21). A
- Bow shoulder stronger in adduction and internal rotation; extensors stronger in both shoulders than in non-athletes (Kim et al. 2018, Clin Shoulder Elb 21:145–50; 15 archers). A, small sample
- Draw hand releases by active finger-extensor contraction (Ertan et al. 2003, Hum Mov Sci 22:37–45). A
- Elite archers fire the finger extensors to keep the bow hand off the grip (Ertan 2009, J Sci Med Sport 12:357–60). A
- Sustained posterior deltoid, middle/lower trapezius and anconeus activity (Mat Salleh et al. 2024, Ann Appl Sport Sci 12:e1452 — compound archers). B
- Trunk muscles (pecs, abdominals) involved. H · Pec major as the bow-shoulder adductor/internal rotator: anatomy applied to Kim 2018. C
- Triceps holding the bow elbow: anconeus data above plus bow-arm mechanics. C
- Rhomboids: no EMG source found (deep muscle). C
- Legs: standing sway is controlled at the ankle (calves) and hip (abductors/adductors) (Winter 1995, Gait Posture 3:193–214 — cited from memory, not retrieved). B
- Injuries: shoulder 30–53%, elbow 12.8% (epicondylitis), spine and forearm 8.9–19.9% (Agranovich et al., archery injuries literature review — year/journal not captured). B
- Overuse shoulder pain 52.9%, 64.6% of it when drawing (Niestroj, Schöffl & Küpper 2018, J Sports Med Phys Fitness 58:1063–70 — figures via a secondary source). B
- Painful archer shoulders mainly involved supraspinatus, biceps long head and subscapularis (Grover & Akhoury, Asian J Sports Med — year not confirmed). A
- Fingers as a loaded tissue: no injury source found; listed from the finger-hook demand (Ertan 2003). C
- Hyperextending bow elbow: turning the arm moves the elbow out of the string path (archery360.com). C
Badminton
- Smash speed correlates with shoulder internal rotation at contact and pelvis–thorax separation (King, Towler, Dillon & McErlain-Naylor 2020, Appl Sci 10:1248). A
- Shoulder internal-rotation velocity ≈66% of racket-head speed (Liu, Kim & Tan 2002, NTU report); forearm pronation, wrist flexion and trunk rotation also contribute — both via a secondary source. B
- Shoulder internal-rotation and elbow-extension velocity correlated with smash speed (Salim et al. — via a secondary source). B
- Triceps key at contact; wrist flexors/extensors key for accuracy (Sakurai & Ohtsuki 2000, J Sports Sci 18:901–14 — via a secondary source). B
- Eccentric external-rotator vs concentric internal-rotator work was studied for the smash's cocking and deceleration phases (Ng & Lam 2002, JOSPT 32:399–404) — result not retrieved; the posterior cuff's decelerating role is reasoning. C
- Forearm supination for backhand strokes: low-quality source only. C
- Grip tightening at impact: not sourced. C
- Overhead triceps transfer to the smash: no data found. C
- Lunges ≈15% of movements in singles (Kuntze, Mansfield & Sellers 2010, J Sports Sci 28:183–91 — via a secondary source). B
- Forward lunge: professionals showed higher gastrocnemius, biceps femoris, gluteus maximus, external oblique and latissimus activity (Jiang, Li & Xiu 2025, Sensors 25:1644). A
- Quadriceps braking in the lunge: reasoning, indirectly supported by the patellar tendinopathy rate below. C
- Glute max/med activity tracks knee valgus and tibial shear in single-leg landing (Hu et al. 2023 — journal inferred from an index record). A
- Ankle evertors: inferred from ankle sprains being the most common injury. C
- Injuries: lower limb ≈52%, ankle most common, sprains most prevalent (Marchena-Rodríguez et al. 2024, systematic review/meta-analysis). A
- Senior players: knees, ankles and shoulders most injured; patellar tendinopathy 20.3% (cross-sectional survey — authors/year not captured). B
- Dominant-shoulder pain in 52% of world-class players (Fahlström, Yeap, Alfredson & Söderman 2006, Scand J Med Sci Sports 16:168–73). A
- Overuse risk to both the limbs and the spine (Pardiwala et al. 2020, Indian J Orthop 54:237–45). A
- Elbow and wrist as loaded tissues: no injury source retrieved. C
- Achilles rupture is common in recreational men; 21% of ruptures in a Danish registry happened in badminton (Kaldau et al. 2022, J Sports Sci Med, citing Barfod et al. 2021). A
- 97% recreational, mean age 36, 94% mid- or late-game; local muscle fatigue implicated (Fahlström, Björnstig & Lorentzon 1998, Am J Sports Med 26:467–70). A
Carryover lines in <athlete> are reasoning from the demand and injury lines above, not transfer studies. C

## R8 Decision log
D adopted · X rejected · P open. Each line: ID · decision · why. An X item returns only with new, cited evidence.
D1 · step-gate pain ceiling ≤5/10 during and after · the ceiling HSD patients tolerated in Liaghat's high-load trial (§R6)
D2 · the hip abductor/adductor machine is programmed when it passes <constraints> and <gates> · reason not recorded
D3 · one goal per region per block; every muscle in a region follows it · mixing goals between close muscles is hard to plan and execute; an upper/lower split is not
D4 · trunk (abs, obliques, spinal erectors) counts as upper body · reason not recorded
D5 · priority (3) is goal fit, judged on a per-goal selection criterion in <dosing>; "stimulus" means growth stimulus only · "stimulus quality" would rank power or endurance blocks on growth; "specificity" reads as sport specificity, which is priority (5)
D6 · rules say what to do and give their reason; hard gates carry no "never"; research is part of the role; reference sections are §R1–R8 · Anthropic's prompting guidance: state what to do, give the reason, drop forceful emphasis (§R5)
D7 · left–right balanced training: bilateral exercises, or unilateral ones done equally on each side · reason not recorded
D8 · <athlete> slimmed: stats in the first line; bodyweight, Standing aims and nutrition removed; conversation-start timing only in <athlete>; profiles list muscles by region; Current state adds block start, layoff, and in-season sports + days with no default · no rule read bodyweight; aims and timing duplicated <role>; nutrition is out of scope
D9 · stations (Smith, cable with high and low pulleys, hip abductor/adductor machine, adjustable bench) are one each, independent, and unavailable while in use; bands, frame, barbells and dumbbells are always available · with one of each, any station — the bench included — can be occupied
D10 · Harry manages load steps; a plan states an exact step only when a source gives one · reason not recorded
D11 · mobility routines keep a pre and a post half with active drills only; a change to one routine updates every routine that references it · <constraints> 7 bans static stretching; routines cite each other, so a partial update leaves stale citations
D12 · the Gym folder on Harry's computer is the workspace: fixed paths; work and run the generator there, the cloud only for steps the computer lacks; working copies in scratch outside the folder; roles table with a build column · the subfolders are fixed (checked 26 Sep); a cloud round-trip per edit is slow and leaves copies that drift (§R5); replaces D11's type-and-role file identification, built for an upload layout
D13 · the .txt mirror is written with every SVG write and read only when files are attached · SVGs are readable in place; the mirror keeps a fallback for attaching files
D14 · gympdf/ is Harry's; Claude leaves it untouched · Harry exports and checks the PDFs himself
D15 · cross-file references cite exercises by number with the name beside it, and mobility items by ID; dependents are found by searching the name or ID · Harry prefers numbers for ease; the name keeps citations findable after a renumber (all 8 foam-rolling numbers had gone stale)
X1 · a "Not available" equipment list (pec deck, leg extension, leg curl, separate cable stack, rope attachment, ab strap, ab wheel, wrist roller) · reason not recorded
X2 · "never by breath or heart rate" as the bound on session density · reason not recorded; <athlete> now states the bound positively (joint control)
X3 · moving the hip abductor/adductor bullet from §R5 into §R8 · reason not recorded
P1 · a deload trigger for power · "down ≥2 reps" doesn't fit 1–3-rep sets
P2 · the step-back unit for non-hypertrophy goals · "−1 set/muscle" assumes weekly per-muscle sets, which only hypertrophy has
P3 · whether indirect sets count across regions (lower-body hinges toward trunk, which is upper) · regions can carry different goals (D3)
P4 · long femur/humerus is read by no rule · waits on limb-length research (T2; first reading: catalogue A9, 2026-10-06)
P5 · §R7 has 10 unsourced and 15 partly sourced evidence lines · waits on verification pass V
P6 · bench exercises (Smith bench work included) need alternatives, and a two-station exercise needs alternatives that avoid both · follows from D9; <programming> not yet updated
P7 · check each cable exercise against high and low pulleys only (e.g. external rotation may need mid-height) · D9 limits the cable machine to two pulleys