# Selective sequence merge results

## Decision

Only **B3 + B3_outcomes** was accepted. The guarded `B3_funding` reference remains. The B3 native page keeps the original family, colors, UML conventions, message wording, note content, and source cell IDs; it uses the user's requested synchronized 14 px business labels and reflowed geometry. The superseded `B3_outcomes` source and exports are archived outside the active manifest. The final local correction reduced only the reference frame height from 60 to 50 and its label cell height from 40 to 30; all x/y positions, widths, styles, IDs, text, and business semantics remain unchanged.

The other eight requested pairs remain separate. They were tested in the same corrected layout and their smallest business/participant/guard/reference/note glyphs fell below 9 pt in both fixed A4 boxes. The decision is therefore limited to the one view that passed the threshold. No message or business rule was removed or condensed.

| Parent | Candidate continuation | Decision | Portrait A4 minimum business glyph | Landscape A4 minimum business glyph |
|---|---|---|---:|---:|
| B3 | B3_outcomes | Inline; retain B3_funding | 9.103 pt actual report page | 6.632 pt |
| A5 | A5_reconciliation | Keep separate | 8.106 pt best-case 757 bp box | 6.699 pt |
| U4.API | U4.API_authorized_request | Keep separate | 8.106 pt best-case 757 bp box | 7.903 pt |
| U3 | U3_authorized_flow | Keep separate | 8.106 pt best-case 757 bp box | 5.766 pt |
| U4 | U4_outcomes | Keep separate | 8.479 pt best-case 757 bp box | 5.712 pt |
| U6 | U6_outcomes | Keep separate | 8.106 pt best-case 757 bp box | 5.816 pt |
| B2 | B2_outcomes | Keep separate | 8.106 pt best-case 757 bp box | 5.816 pt |
| S2 | S2_outcomes | Keep separate | 8.106 pt best-case 757 bp box | 5.816 pt |
| U8 | U8_outcomes | Keep separate | 8.106 pt best-case 757 bp box | 6.025 pt |

The accepted B3 size is measured from a one-page pdflatex report-style inclusion with the report's Times face, fancy header/footer, and single-line caption. It uses a 510 × 700 bp figure box and 15 mm figure-only margins; pdfplumber 0.11.9 measured a 9.103 pt minimum for the diagram body. There were no overfull warnings or clipping and the caption fits on one line. See [report_page_B3.pdf](sequence_trials/repair_round1/report_page_B3.pdf), [report_page_B3.tex](sequence_trials/repair_round1/report_page_B3.tex), and [report_page_B3_measurement.json](sequence_trials/repair_round1/report_page_B3_measurement.json).

For the eight rejected pairs, the portrait figures were tested in the larger 510 × 757 bp figure-only box (the maximum height available before a report header, caption, and footer); all already fall below 9 pt there. Landscape uses 755 × 510 bp. These bounds are actual pdflatex inclusion proofs measured with pdfplumber 0.11.9 and cross-checked with pdf.js. The recorded minimum excludes the page title, subtitle, and two legend lines, while including participants, messages, guards, refs, frame labels, and business notes. See [proof_measurements.json](sequence_trials/repair_round1/proof_measurements.json), [proof_portrait.pdf](sequence_trials/repair_round1/proof_portrait.pdf), and [proof_landscape.pdf](sequence_trials/repair_round1/proof_landscape.pdf).

## Source and behavior checks

- The geometry was produced by the draw.io skill's `seqlayout.py` engine. The trial runner imported the existing sequence builder as a library and called only its in-memory modularization/render helpers; it did not run the fresh-generation entry point.
- All 58 baseline structured views were checked against the baseline manifest before candidate construction. An independent expanded trace compared messages, sender/receiver, return/async markers, guards, nesting, notes, and retained refs across all 24 logical IDs: 24/24 matched.
- The B3 merge is an exact guarded-reference splice. Every child message retains its original order and source-view/source-index provenance. Stable source semantic cell IDs are retained; imported participant IDs are consistently mapped to the parent participants.
- Native validation of final `SD_B3.drawio` reported 0 errors, 0 through-vertex cases, and 0 crossings. Its 12 overlap warnings are expected container/lifeline geometry (guard labels inside their fragment, reference frame crossing lifeline regions); the native PNG was inspected and its 15 DOM text boxes have no text-box intersections above 0.5 px in either axis. Message labels remain clear of participant headers and frame separators.
- The actual report-style A4 portrait proof passes at 9.103 pt minimum after adding the report header, footer, and caption. Landscape is recorded for comparison and does not pass the threshold. The accepted report placement must use the documented portrait box.
- Candidate PNGs are draft renderings without embedded source, and final SVG/PDF/native files were rendered locally by `analysis/render_diagrams.cjs` using the recovered official viewer bundle; no network access was used.

The earlier syntax/partial-write harness failures are retained under `sequence_trials/repair_round1_invalid_*` as debugging artifacts and are not counted as layout evidence. The synchronized 14 px compact layout is the second and last valid layout attempt. Formal review fix count: 2/2. The final reference-frame clearance edit was a two-cell manual geometry correction, not a new layout attempt or global geometry change.

## Safety and repeatability

`sequence_trials/repair_round1_inputs` preserves the original 18 native pages, baseline manifest, content JSON, builder helper, and geometry engine copy as historical evidence. The former trial runner depended on a user-local skill path and a restored pre-merge active set, so `sequence_trials/run_repair_round.py` is now a no-write historical stub. The completed promotion script and the older merge script are also no-write stubs. Future editing uses active native XML and the active manifest as canonical, followed by a local render for review. The fresh builder entry point refuses to overwrite active diagrams.

The eight unaccepted pairs retain their original native sources and manifest entries. A1, P1–P3, all API variant logical IDs, all six report overview views, all 22 activity views, report files, content JSON, and other delivery assets were not edited. Superseded B3 continuation files are preserved under `sequence_trials/superseded/B3_outcomes/`.

## Changed paths

- `analysis/diagrams/sequence/SD_B3.drawio` — accepted native B3 merge.
- `analysis/diagrams/sequence/SD_B3.png`, `SD_B3.svg`, `SD_B3.pdf` — refreshed final exports.
- `analysis/sequence_models.json` — B3 merged model; B3_outcomes removed from active view/part lists; all other source views retained.
- `analysis/sequence_trials/superseded/B3_outcomes/` — original continuation source and exports.
- `analysis/sequence_trials/repair_round1/` — staged candidates, draft renders, DOM, compiled proofs, and validation/measurement evidence.
- `analysis/sequence_trials/repair_round1_inputs/` — historical source inputs and geometry engine copy.
- `analysis/sequence_trials/changed_paths.txt` — complete workspace-relative file list for the sequence work and proof artifacts in this task.
- `analysis/sequence_trials/run_repair_round.py` — no-write historical trial-runner stub.
- `analysis/promote_sequence_merge.py` — no-write historical promotion stub.
- `analysis/selective_sequence_merge.py` — no-write compatibility stub.
- `analysis/build_sequence_diagrams.py` — fresh-generation overwrite guard and corrected manifest provenance wording.
- `analysis/Selective_Sequence_Implementation.md` — this implementation and decision record.


## Portable evidence selection

The portable ZIP includes the six linked accepted-print proof files listed above (the fixed B3 LaTeX proof, its measurement, and the portrait/landscape comparison measurements and PDFs). Other trial drafts, invalid attempts, caches, checkpoints, and superseded sources remain workspace history and are not part of the portable package.
