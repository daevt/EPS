"""Assemble the fresh EPS analysis figures and verify their saved exports.

Run after the three diagram builders and render_diagrams.cjs. This script only
uses manifest-listed diagrams, never a previous board or an old diagram set.
"""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET
import hashlib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECT = ROOT / 'EPS_Report_LaTeX'
ORDER = [f'U{i}' for i in range(1, 9)] + [f'B{i}' for i in range(1, 5)] + [f'S{i}' for i in range(1, 3)] + [f'A{i}' for i in range(1, 6)] + [f'P{i}' for i in range(1, 4)]

def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8-sig'))

def ordered_files():
    overview = read('overview_manifest.json')['diagrams']
    overview.sort(key=lambda d: (d['id'] != 'UC_Overview', ['UC_Overview', 'UC_Account', 'UC_SharedParty', 'UC_Buyer', 'UC_Seller', 'UC_Admin', 'UC_Payment'].index(d['id'])))
    activity = read('activity_models.json')['diagrams']
    activity.sort(key=lambda d: ORDER.index(d['use_case']))
    seq = read('sequence_models.json')
    logical = seq['logical_diagrams']
    seq_order = ORDER.copy()
    seq_order.insert(seq_order.index('U4') + 1, 'U4.API')
    seq_order.insert(seq_order.index('B1') + 1, 'B1.API')
    logical.sort(key=lambda d: seq_order.index(d['logical_id']))
    files = [(d['id'], d['title'], d['file']) for d in overview]
    files += [(d['diagram_id'], d['title'], d['filename']) for d in activity]
    for d in logical:
        files.append(('SD_' + d['logical_id'], d['title'], d['default_main']))
        files += [('SD_' + p['id'], p['title'], p['filename']) for p in d['parts']]
    assert len({f[2] for f in files}) == len(files)
    assert len(activity) == 22 and len(logical) == 24
    return files

def main():
    from pypdf import PdfReader
    files = ordered_files()
    combined = ET.Element('mxfile', host='app.diagrams.net', version='32.5.5', type='device', compressed='false')
    sequence_board = ET.Element('mxfile', host='app.diagrams.net', version='32.5.5', type='device', compressed='false')
    checks = []
    errors = []
    for index, (key, title, rel) in enumerate(files, 1):
        source = HERE / rel
        model = ET.parse(source)
        page = model.getroot().find('diagram')
        cells = page.findall('.//mxCell')
        ids = [c.get('id') for c in cells]
        if len(ids) != len(set(ids)):
            errors.append(f'{rel}: duplicate cell IDs')
        idset = set(ids)
        if not {'0', '1'}.issubset(idset):
            errors.append(f'{rel}: missing root cells')
        for c in cells:
            for attr in ('parent', 'source', 'target'):
                if c.get(attr) and c.get(attr) not in idset:
                    errors.append(f'{rel}: {c.get("id")} has dangling {attr}')
            if c.get('edge') == '1':
                g = c.find('mxGeometry')
                if g is None or g.get('relative') != '1':
                    errors.append(f'{rel}: edge geometry is not relative')
        domfile = HERE / '.render-cache' / 'dom' / (source.stem + '.dom.json')
        dom = json.loads(domfile.read_text())
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if dom.get('sourceSha256') != digest:
            errors.append(f'{rel}: export is stale')
        for extension in ('.png', '.svg', '.pdf'):
            if not source.with_suffix(extension).is_file():
                errors.append(f'{rel}: missing {extension} export')
        pdf = PdfReader(source.with_suffix('.pdf'))
        if len(pdf.pages) != 1:
            errors.append(f'{rel}: figure PDF must have one page')
        if not (pdf.pages[0].extract_text() or '').strip():
            errors.append(f'{rel}: figure PDF has no selectable text')
        if dom.get('nativeEdgeCount') != sum(c.get('edge') == '1' for c in cells):
            errors.append(f'{rel}: missing native edge path')
        clone = copy.deepcopy(page)
        clone.set('id', f'EPS-PAGE-{index:03d}-{key}')
        clone.set('name', f'{index:02d} {key} - {title}'[:180])
        combined.append(clone)
        if rel.startswith('diagrams/sequence/'):
            seqclone = copy.deepcopy(page)
            seqclone.set('id', f'EPS-SEQ-{len(sequence_board)+1:03d}-{key}')
            seqclone.set('name', f'{len(sequence_board)+1:02d} {key} - {title}'[:180])
            sequence_board.append(seqclone)
        checks.append({'id': key, 'source': rel, 'sha256': digest,
                       'vertices': sum(c.get('vertex') == '1' for c in cells),
                       'edges': sum(c.get('edge') == '1' for c in cells),
                       'render_width': dom['width'], 'render_height': dom['height']})
    if errors:
        raise RuntimeError('\n'.join(errors))
    ET.indent(combined, space='  ')
    target = ROOT / 'EPS_Analysis_Diagrams.drawio'
    ET.ElementTree(combined).write(target, encoding='utf-8', xml_declaration=True)
    sequence_target = ROOT / 'EPS_Sequence_Diagrams.drawio'
    ET.indent(sequence_board, space='  ')
    ET.ElementTree(sequence_board).write(sequence_target, encoding='utf-8', xml_declaration=True)
    destination = PROJECT / 'source' / 'Introduction_Planning.pdf'
    destination.parent.mkdir(parents=True, exist_ok=True)
    expected_source_hash = '1cf077ae8e1794a04857f9e48fe70f965f5d57c56b2384854cf8e112d74b7435'
    if not destination.is_file() or hashlib.sha256(destination.read_bytes()).hexdigest() != expected_source_hash:
        raise RuntimeError('Canonical project Introduction_Planning.pdf is missing or does not match its pinned SHA-256; do not substitute another file.')
    for _, _, rel in files:
        source = HERE / rel
        for extension in ('.drawio', '.png', '.svg', '.pdf'):
            dest = PROJECT / Path(rel).with_suffix(extension)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source.with_suffix(extension), dest)
    report = {'status': 'PASS', 'fresh_view_count': len(files), 'logical_activity_count': 22,
              'logical_sequence_count': 24, 'overview_view_count': 7,
              'sequence_view_count': len(read('sequence_models.json')['diagrams']),
              'report_figure_count': len(files)-1, 'sequence_board_pages': len(sequence_board),
              'source_pdf_sha256': expected_source_hash,
              'checks': ['XML IDs and references', 'relative edge geometry', 'native edge paths',
                         'source/export SHA-256 match', 'PNG and SVG present',
                         'single-page vector figure PDF with selectable text',
                         'Introduction/Planning source copied byte-for-byte'],
              'limits': 'Artifact validation only. No EPS application or acceptance scenario was executed.',
              'figures': checks}
    (HERE / 'Artifact_Validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Assembled {len(files)} fresh editable pages, copied all source/image/vector assets, and passed export checks.')

if __name__ == '__main__':
    main()
