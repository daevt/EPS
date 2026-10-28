# EPS — Analysis report and diagram library

The current working set lives in this folder: `analysis/` contains the active sources and `EPS_Report_LaTeX/` contains the current reports and LaTeX project. `EPS_Report_Source_and_Diagrams.zip` is the portable copy of these current files. The full report, Analysis PDF and Sequence PDF below cover different scopes.

Previous checkpoints, superseded trials, temporary review files and the earlier delivery ZIP are kept separately in `_archive/EPS_Older_Versions_2026-10-28.zip` in the original workspace; this recovery archive is excluded from the portable ZIP. Use the working files above for further edits. See [the current draw.io editing guide](HUONG_DAN_AI_VE_DIAGRAM_DRAWIO.md).

## Deliverables

- [Full report](EPS_Report_LaTeX/EPS_Report.pdf): 108 pages, including the unchanged 11-page Introduction/Planning source.
- [Analysis report](EPS_Report_LaTeX/EPS_Analysis.pdf): 97 pages.
- [Sequence diagrams](EPS_Report_LaTeX/EPS_Sequence_Diagrams.pdf): 57 diagram views across 24 logical sequences.
- [Diagram gallery](EPS_Diagrams_Gallery.html): 86 editable views with PNG, SVG and vector PDF exports.
- [All diagrams as editable draw.io pages](EPS_Analysis_Diagrams.drawio): 86 pages. [Sequence-only board](EPS_Sequence_Diagrams.drawio): 57 pages.

## Source structure

`EPS_Report_LaTeX/main.tex` builds the full and Analysis PDFs. The full report reuses the unchanged `source/Introduction_Planning.pdf`; editable Analysis content lives in `sections/analysis.tex`. Section 3.4 is in `sections/sequence.tex`, shared by the report and standalone `EPS_Sequence_Diagrams.tex` entry point.

`analysis/diagrams/` stores the 86 current native diagrams and PNG/SVG/vector PDF exports: 7 overview pages, 22 activity diagrams, and 57 sequence views for 24 logical sequences (22 use cases plus B1.API and U4.API). Six focused overview figures appear in the report; the overview map remains in the library.

`EPS_Report_LaTeX/diagrams/` contains the portable copies used by all three LaTeX entry points. `analysis/content_*.json`, model JSON files and scripts retain the specification and render workflow. For future diagram edits, update the canonical native draw.io source, render and review its exports, then compile the reports.

## Rebuild

With Python, pypdf and TeX Live installed, run `python EPS_Report_LaTeX/build_pdf.py`. It compiles all three PDFs in two passes and preserves the original Introduction/Planning pages in the full report.

## Verified artifact checks

The refreshed reports contain 85 figures, retain all 22 eight-field use cases and four NFR groups, and have no unresolved LaTeX references, overfull boxes, missing glyphs or blank Analysis pages. The original 11-page source PDF matches its pinned SHA-256 and its pages render pixel-identically in the full report. The accepted B3 sequence page uses the fixed 510 × 700 bp placement; measured diagram business text minimum is 9.103 pt in each report. The active source and exports are current for all 86 native views. These are artifact checks, not EPS application tests.
