# gymtools — helper scripts kept from earlier sessions

Stored 2026-10-09 at Harry's request, so later sessions can reuse them. The generator moved in the same day: svg_routine_generator/ now sits here instead of in the Gym folder root.

These are tools, not stored copies of the routines. The files in gymplan/, gymtxt/, gymspec/ and gymstate/ are the source of truth (reference.md §R4):

- Rebuild a routine from the SVG you just read, not from a script here.
- Before a new catalogue revision, check that catalogue/rows.py still matches gymspec/ExerciseCatalogue.json (see the catalogue check below).

## What is here

| File | What it does | Checked 2026-10-09 |
|---|---|---|
| svg_routine_generator/ | The generator. routine_generator.py, the single-file bundle, is the one in use; it is imported and never edited. The package files (model, svg_render, theme) and the two example routines are older versions, kept as data-format references. Moved here from the Gym folder root on 2026-10-09. | From here, v3 and the 2-col copy rebuild byte-identical (md5 7f36a39a…, c883d4e5…) |
| svg/figs.py | Draws the 20 moving pictures of evaluation_upperbody v3, each in a 156 × 132 box, plus helpers for new ones. `Scene` samples a pose at 30 frames and animates points, cx/cy and d with `<animate>`. Its still fallback is the start pose plus a faint ghost of the end pose. Other helpers: `beat_dots`, `caption`, `label`, `floor`, `ik`, `wedge`. | Used by the v3 build below |
| svg/build_evaluation_upperbody_v3.py | The definition that built evaluation_upperbody v3 (2026-10-07). It monkey-patches the generator's card renderer for picture cards and adds the four eval colours; the generator itself is not edited. | Rebuilds v3 byte-identical (md5 7f36a39a…) |
| svg/build_2col.py | Makes the two-column copy from a v3 file on a 1,360 px page. Cards are moved as they are; the header, legend, intro boxes, section headers and version note are redrawn. The copy is a one-off and is not kept in step with v3, so refresh it only when Harry asks. | Rebuilds evaluation_upperbody_2col v1 byte-identical (md5 c883d4e5…) |
| svg/build_evaluation_lowerbody_2col_v1.py | Makes the two-column copy of evaluation_lowerbody v1 on a 1,360 px page (Stage 2 D-09), from a copy of build_2col.py: cards, pictures, links and end boxes moved as they are; header, legend, intro boxes, section headers and version note redrawn; v1's sport note left out (Stage 2 R59). A one-off, not kept in step with v1, so refresh it only when Harry asks. | Builds evaluation_lowerbody_2col v1 byte-identical (md5 f7c9bd56…); check_widths flags its 3 centred lines, as expected |
| svg/build_evaluation_lowerbody_v1.py | The definition that built evaluation_lowerbody v1 (2026-10-08). Self-contained: it lays out the cards and draws its 13 moving pictures in v3's style, without the generator or figs.py. It writes only the SVG, to the path given; copy it into gymplan/ and cp it to gymtxt/. | Rebuilds v1 byte-identical (md5 f75c935d…) |
| svg/check_widths.py | Text-overflow check by the §R4 character-width estimate, at 0.5 px per character per point of font size, any size: text past the 650 px edge; picture texts over 154 px (pictures sit at x 486); in a file with pictures, card lines at x 72 or 136 past x 480; in a file without, card lines that run into the right column on a line where it has text; card titles that run into the right column, found per file (x 490 in generator files, 510–515 in the mobility files). Takes several files. Rewritten 2026-10-14: it stopped on font sizes 10.5, 13 and 14, and flagged detail lines as picture overlaps in files without pictures. | 2026-10-14, all 17 files: no overflow in 12; the 2-col copy's 3 centred lines, as expected; 3 lines in routine_lowerbody v4 and 2 in routine_upperbody v6 (long titles, version notes) to check by eye; 7 in stretching_lower_hEDS and 8 in stretching_upper_hEDS, all of which fit in the render, where the estimate errs wide |
| svg/render_png.py | Renders an SVG to PNG in Chromium, with sans-serif set to Liberation Sans (the §R4 render check). | OK |
| svg/render_frames.py | Renders PNGs of an animated SVG at chosen times: it pauses the animation and sets the clock. Prints the `<animate>` count and any console errors. | v3: 94 animations, no errors |
| svg/picture_grid.py | Puts all the pictures from figs.py on one sheet at chosen times, for review. | OK |
| svg/yt_search.py | Lists the top YouTube results (video id, title, channel, length) for each search written into the script. It found the 7 videos linked in evaluation_lowerbody v1, which were then checked by title and channel through oEmbed (see Link checks). Runs on the PC: the cloud workspace can't reach YouTube. | On the PC: 7 searches, no errors |
| catalogue/build.py · rows.py · vocab.py | Builds ExerciseCatalogue.json and its .md mirror. The data is revision 12 (2026-10-25): C139–C141, L options for the front delt, rear delt and abs (Stage 1 D-15); revision 11 added v8 provenance from the upper focus files, revision 10 C138, the stage-2 cues and v7 provenance. Revision 11's change table is now written into build.py, as revision 10's is. | 2026-10-25: rows and vocabulary matched gymspec rev 11 before the change; with the rev 11 JSON as the previous file, rev 12 rebuilds byte-identical, keeps every rev 11 row and revision unchanged, and verify.py passes. 2026-10-13: the same check on rev 11 with the rev 10 JSON |
| catalogue/verify.py | Catalogue checks: every corpus card is covered, alternatives, mirror parity, vocabulary, cross-references into both Supplements, and (check 6, added 2026-10-15) the files in gymplan/ against the catalogue: each file at or above the latest version the catalogue cites, every cited card present under its number, and its title, card text or the citation's own words matching a cited row (Stage 2 D-04 · R61); a card cited only inside a range (one merged row) is checked for presence. Its file list holds the latest cited versions (upper focus v8 since 2026-10-13); a text-only version leaves it. The confirmed-row check covers the stage-1 replacements only, since C138 is a D-08 addition. | 2026-10-13: ALL PASS on gymspec rev 11. 2026-10-15: ALL PASS with the files edited on 2026-10-14 (lower focus v4, popliteus v6, cardio v1, mobility v3 and v2 matched through their cited versions); a planted card swap and a removed mobility ID both FAIL. 2026-10-25: check 6 skips a stem found only in gymplan/PreviousOldRoutines/, Harry's archive (SKIP lines, Stage 2 D-15), and a FAIL now exits 1: ALL PASS with the 4 archived stems skipped; a planted citation of a stem found nowhere FAILs with exit 1 |
| plan/pair_check.py | Superset check from catalogue facts: every pair against Stage 1 R38 and R39, with stations from Stage 0 §1.3 — (1) shared muscle, (2) shared station, (3) pair type, (4) the heavy-compound clause. On routine files it also lists straight sets (R39) and checks each alternative of a paired exercise against both partners' stations. Pairs by catalogue ID while planning (`--pair`), the routine files before delivery (CLAUDE.md, Routine request). Cards map to rows through the catalogue's provenance lines: the file's own version when the catalogue cites it, otherwise the latest cited version below it, and then every card's title must match a row cited for its number (Stage 2 D-04 · R61); a changed card FAILs until the catalogue cites the new version. REVIEW and NOTE lines are judgements the plan states; a FAIL exits 1. | 2026-10-15: `--selftest` 14/14; upper focus v8 unchanged; a cue-only v9 copy of focus A maps through v8 and passes, and a v9 copy with card 3 swapped FAILs on the name. 2026-10-13: `--selftest` 14/14 — the spec's R38 pass and fail examples, reference.md §R3, the walkthrough's S1.9 pairs, v7's two invalid pairs. Upper focus v8: all pairs pass (B1 REVIEW, B2 NOTE), 0 straight sets. On the v7 copies it caught the 2 invalid pairs, 9 straight sets and 3 alternatives needing a partner's station |
| spec/xref_check.py | Cross-reference check over CLAUDE.md and each stage's two docs (Stages 0–2 today; a later stage is picked up once both its files exist): §, R-, S-, D-, W-, M- and O- references, accepted-limit letters, a pass and a fail example per rule, Input, Action items and Output per step, no "should" or "may" in rules, duplicate IDs, and each stage's Open items against CLAUDE.md `<stages>`. Its docstring says how each reference resolves. Exits 1 when it lists issues. | No false positives; 16 planted faults all caught. Live docs (2026-10-15): clean, Stage 2 included; the 3 issues of 2026-10-13 on Stage1_SupplementInfo.md line 141 (Stage 0 D-refs without "Stage 0") were fixed on 2026-10-15 |
| state/state_check.py | State-file check (Stage 2 R67 · §3.4 · R66 (10)) on the newest gymstate/block_NN.json, or the file given: fields and types against Stage 0 §4.1, read from the doc, and Stage 2 §3.4; the §4.1 invariants, with goal rows from §2.2, muscles and joints from the catalogue's vocabulary and sport profiles from §1.2, and at most 3 training sessions a week per region (R20); each current routine in gymplan/ and in the register (Stage 2 Supplement §9), trained by the block; the plan's fields; log dates in order. A FAIL exits 1; a NOTE is a judgement the delivery states. Its selftest uses its own routine set, so it does not depend on gymplan/. | 2026-10-25: `--selftest` 22/22 planted faults caught, clean fixture passes. block_01.json: clean, 1 NOTE (plan null: the upper block's plan-only fields were not kept on 2026-10-13); after they were rebuilt the same day, clean with no NOTE |
| analysis/er_geom.py | Rough geometry from the catalogue's revision 8 check of vertical-pull grips (T12): how far the shoulder turns out at the bottom of a front pulldown. | Parses; needs numpy |

## How to run (from the Gym folder)

Write outputs to a scratch folder, never straight into gymplan/, gymtxt/ or gymspec/. Use `-B` so no `__pycache__` lands in the folder.

```
python3 -B gymtools/svg/build_evaluation_upperbody_v3.py gymtools/svg_routine_generator <out.svg>
python3 -B gymtools/svg/build_2col.py gymtools/svg_routine_generator gymplan/evaluation_upperbody.svg <out.svg>
python3 -B gymtools/svg/build_evaluation_lowerbody_2col_v1.py gymtools/svg_routine_generator gymplan/evaluation_lowerbody.svg <out.svg>
python3 -B gymtools/svg/build_evaluation_lowerbody_v1.py <out.svg>
python3 -B gymtools/svg/check_widths.py gymplan/<file>.svg [...]
python3 -B gymtools/svg/render_png.py <file.svg> <out.png>
python3 -B gymtools/svg/render_frames.py <file.svg> <out_dir> 0 2.6
python3 -B gymtools/svg/picture_grid.py <out_dir> 0 2
python3 -B gymtools/svg/yt_search.py
cd gymspec && python3 -B ../gymtools/spec/xref_check.py
python3 -B gymtools/state/state_check.py [gymstate/block_NN.json]
python3 -B gymtools/state/state_check.py --selftest
python3 -B gymtools/plan/pair_check.py gymplan/<routine>.svg [...]
python3 -B gymtools/plan/pair_check.py --pair C040 C048 [--pair C001 C035 ...]
python3 -B gymtools/plan/pair_check.py --selftest
python3 -B gymtools/analysis/er_geom.py
```

### Catalogue

Run these from gymtools/catalogue.

1. Check that rows.py is still in step with the live catalogue. True means in step. False means the JSON was edited after revision 9, so bring rows.py and vocab.py up to it first.

   ```
   python3 -B build.py <tmp>
   python3 -c "import json; a=json.load(open('<tmp>/ExerciseCatalogue.json',encoding='utf-8')); b=json.load(open('../../gymspec/ExerciseCatalogue.json',encoding='utf-8')); print(a['rows']==b['rows'] and a['vocabulary']==b['vocabulary'])"
   ```

2. Build a new revision. First add a REVISIONS entry in build.py, then:

   ```
   python3 -B build.py <out_dir> ../../gymspec/ExerciseCatalogue.json
   python3 -B verify.py <out_dir> ../../gymspec
   ```

verify.py has the exercise routine files and card counts as of 2026-10-13 written into it, at the latest version the catalogue cites. Update that list when an exercise, a card number or a pairing changes, or a new exercise routine is added; a text-only version leaves it (Stage 2 D-04), and check 6 confirms the files still match. The evaluation files stay out of the catalogue: they hold tests, not exercises, as the foam-rolling files hold tissue release.

## Needs

- Python 3.10 or later.
- Playwright with Chromium for render_png, render_frames and picture_grid. The cloud workspace has it; the PC's Linux shell does not (checked 2026-10-09).
- numpy for er_geom.
- The generator, gymtools/svg_routine_generator/routine_generator.py (2026-07-22, md5 119e30d6…). It is imported and never edited.

## Things learned the hard way (2026-10-03 … 10-08)

- **.txt mirrors.** Write a .txt mirror with `cp` on the PC after its SVG lands, then compare md5s. On 2026-10-07, a .txt sent through the upload route came back with C2PA metadata added. The .py and .md files here went through upload unchanged.
- **Apostrophes.** The generator does not escape them. When matching rendered text, search for a plain `'`, not `&#x27;`.
- **Hyphenated words.** Use textwrap with `break_on_hyphens=False`, or words like "side-on" get split.
- **Animation frames.** To check them, use `svg.pauseAnimations(); svg.setCurrentTime(t)`; render_frames.py does this.
- **Link checks.** YouTube watch pages return HTTP 429 to the fetch tool. Its oEmbed endpoint (`https://www.youtube.com/oembed?url=<video url>&format=json`) gives the title and channel. PubMed Central asked for a reCAPTCHA, and Europe PMC returned 429. Don't work around a refusal; give Harry the link to open.
- **Width estimate (§R4).** Characters per font size: 9 = 4.5 px, 10 = 5.0, 11 = 5.5, 12 = 6.0, 15 = 7.5; any size at 0.5 px per point (10.5 = 5.25, 13 = 6.5, 14 = 7.0).

## Not kept

These were one-offs: the doc-edit scripts for D-77 … D-79, the v1 and v2 evaluation builders, and older catalogue revisions.
