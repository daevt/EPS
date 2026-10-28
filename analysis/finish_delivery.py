"""Archive manifest-external figure files, refresh the gallery, and package sources."""
from pathlib import Path
import argparse
import html
import json
import shutil
import zipfile
from finalize_assets import ordered_files

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECT = ROOT / 'EPS_Report_LaTeX'


def safe_move(source, archive):
    source = source.resolve()
    assert source.is_relative_to(ROOT)
    archive.parent.mkdir(parents=True, exist_ok=True)
    target = archive
    serial = 1
    while target.exists():
        target = archive.with_name(archive.stem + f'-{serial}' + archive.suffix)
        serial += 1
    shutil.move(str(source), str(target))


def prepare(files):
    valid = {str(Path(rel).with_suffix(ext)).replace('\\', '/')
             for _, _, rel in files for ext in ('.drawio', '.png', '.svg', '.pdf')}
    moved = 0
    for name, base in [('analysis', HERE), ('project', PROJECT)]:
        for file in (base / 'diagrams').rglob('*'):
            if file.is_file() and file.relative_to(base).as_posix() not in valid:
                safe_move(file, HERE / '.render-cache' / 'superseded' / name / file.relative_to(base))
                moved += 1

    overview = json.loads((HERE / 'overview_manifest.json').read_text(encoding='utf-8-sig'))['diagrams']
    activity = json.loads((HERE / 'activity_models.json').read_text(encoding='utf-8-sig'))['diagrams']
    sequence = json.loads((HERE / 'sequence_models.json').read_text(encoding='utf-8-sig'))['diagrams']
    nav, cards = [], []
    for index, (key, title, rel) in enumerate(files, 1):
        anchor = f'view-{index}'
        nav.append(f'<a href="#{anchor}">{html.escape(key)}</a>')
        stem = Path('analysis') / Path(rel)
        png, svg, pdf = [stem.with_suffix(ext).as_posix() for ext in ('.png', '.svg', '.pdf')]
        cards.append(f'<article id="{anchor}"><h2>{index}. {html.escape(key)} — {html.escape(title)}</h2>'
                     f'<p><a href="{stem.as_posix()}">Editable draw.io</a> · <a href="{png}">PNG</a> · '
                     f'<a href="{svg}">SVG</a> · <a href="{pdf}">Vector PDF</a></p>'
                     f'<a href="{png}"><img loading="lazy" src="{png}" alt="{html.escape(title)}"></a></article>')
    page = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>EPS — Diagram gallery</title><style>body{font:16px/1.55 system-ui,sans-serif;background:#eef2f6;color:#172b4d;margin:0}'
            'header,main{max-width:1200px;margin:auto;padding:24px}nav{display:flex;flex-wrap:wrap;gap:8px}nav a{padding:4px 8px;background:white;border:1px solid #b8c8dc;border-radius:5px}'
            'a{color:#1764a0}article{background:white;border:1px solid #c7d2df;padding:22px;margin:24px 0}img{display:block;max-width:100%;height:auto;margin:auto}</style>'
            f'<header><h1>EPS — Analysis diagram gallery</h1><p>{len(files)} current editable views: {len(overview)} overview, '
            f'{len(activity)} activity and {len(sequence)} sequence views across 24 logical sequences. The report uses six focused overview figures; the map remains in the library.</p>'
            f'<p><a href="EPS_Analysis_Diagrams.drawio">All {len(files)} draw.io pages</a> · '
            f'<a href="EPS_Sequence_Diagrams.drawio">{len(sequence)} sequence pages</a> · '
            '<a href="EPS_Report_LaTeX/EPS_Report.pdf">Full report</a> · '
            '<a href="EPS_Report_LaTeX/EPS_Analysis.pdf">Analysis PDF</a> · '
            '<a href="EPS_Report_LaTeX/EPS_Sequence_Diagrams.pdf">Sequence PDF</a></p><nav>' + ''.join(nav) +
            '</nav></header><main>' + ''.join(cards) + '</main></html>')
    (ROOT / 'EPS_Diagrams_Gallery.html').write_text(page, encoding='utf-8')
    print(f'Gallery updated with {len(files)} current views; archived {moved} manifest-external assets.')


def pack(files):
    allowed = set()
    for name in ['README_EPS_Delivery.md', 'AI_Reuse_Guide.md', 'EPS_Analysis.md',
                 'Example_Report_Structure_Guide.md', 'HUONG_DAN_AI_VE_DIAGRAM_DRAWIO.md',
                 'EPS_Diagrams_Gallery.html',
                 'EPS_Analysis_Diagrams.drawio', 'EPS_Sequence_Diagrams.drawio']:
        path = ROOT / name
        if path.is_file():
            allowed.add(path)
    for _, _, rel in files:
        for ext in ('.drawio', '.png', '.svg', '.pdf'):
            for base in (HERE, PROJECT):
                path = base / Path(rel).with_suffix(ext)
                if path.is_file():
                    allowed.add(path)
    for path in HERE.iterdir():
        if path.is_file() and path.suffix in {'.py', '.cjs', '.json', '.md', '.txt'}:
            allowed.add(path)
    for path in (HERE / 'vendor').rglob('*'):
        if path.is_file():
            allowed.add(path)
    # Accepted print evidence referenced by Selective_Sequence_Implementation.md.
    proof_dir = HERE / 'sequence_trials' / 'repair_round1'
    for name in ['report_page_B3.pdf', 'report_page_B3.tex', 'report_page_B3_measurement.json',
                 'proof_measurements.json', 'proof_portrait.pdf', 'proof_landscape.pdf']:
        path = proof_dir / name
        if path.is_file():
            allowed.add(path)
    for path in PROJECT.rglob('*'):
        if not path.is_file() or path.name == 'EPS_Report (1).pdf' or path.suffix in {'.aux', '.log', '.out'} or path.name.endswith('.build.log'):
            continue
        if path.suffix in {'.tex', '.pdf', '.py', '.json', '.md', '.png', '.svg', '.drawio'}:
            allowed.add(path)
    assert (PROJECT / 'source' / 'Introduction_Planning.pdf') in allowed
    assert (PROJECT / 'EPS_Sequence_Diagrams.tex') in allowed
    assert (PROJECT / 'sections' / 'sequence.tex') in allowed
    output = ROOT / 'EPS_Report_Source_and_Diagrams.zip'
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(allowed):
            archive.write(path, path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert 'EPS_Report_LaTeX/EPS_Sequence_Diagrams.tex' in names
        assert 'EPS_Report_LaTeX/EPS_Report (1).pdf' not in names
        assert all(f'analysis/sequence_trials/repair_round1/{name}' in names for name in
                   ['report_page_B3.pdf', 'report_page_B3.tex', 'report_page_B3_measurement.json',
                    'proof_measurements.json', 'proof_portrait.pdf', 'proof_landscape.pdf'])
        print(f'ZIP checked: {len(names)} entries; {output.stat().st_size:,} bytes.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pack', action='store_true')
    args = parser.parse_args()
    files = ordered_files()
    prepare(files)
    if args.pack:
        assert (HERE / 'PDF_Validation.json').is_file(), 'Run final PDF verification before packaging.'
        pack(files)
