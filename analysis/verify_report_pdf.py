"""Render final PDF pages for review and check the completed chapter inventory."""
from pathlib import Path
import hashlib
import json
import re
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageChops
from pypdf import PdfReader
import pdfplumber

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECT = ROOT / 'EPS_Report_LaTeX'
QA = ROOT / 'tmp' / 'pdf_review'

def page_text(page):
    textpage = page.get_textpage()
    text = textpage.get_text_range()
    textpage.close()
    return text

def check_links(path):
    reader = PdfReader(path)
    destinations = reader.named_destinations
    pages = {p.indirect_reference.idnum for p in reader.pages}
    count, invalid = 0, []
    for index, page in enumerate(reader.pages, 1):
        for reference in page.get('/Annots', []):
            annotation = reference.get_object()
            action = annotation.get('/A', {})
            dest = annotation.get('/Dest')
            if not dest and action.get('/S') == '/GoTo':
                dest = action.get('/D')
            if not dest:
                continue
            count += 1
            if isinstance(dest,str):
                if dest not in destinations:
                    invalid.append({'page':index,'destination':dest})
            elif isinstance(dest,list) and hasattr(dest[0],'idnum') and dest[0].idnum not in pages:
                invalid.append({'page':index,'destination':'missing page object'})
    return {'internal_link_count':count,'invalid_targets':invalid}

def main():
    QA.mkdir(parents=True, exist_ok=True)
    analysis = pdfium.PdfDocument(PROJECT / 'EPS_Analysis.pdf')
    sequence = pdfium.PdfDocument(PROJECT / 'EPS_Sequence_Diagrams.pdf')
    full = pdfium.PdfDocument(PROJECT / 'EPS_Report.pdf')
    original = pdfium.PdfDocument(PROJECT / 'source' / 'Introduction_Planning.pdf')
    texts = []
    thumbnails = []
    for i in range(len(analysis)):
        page = analysis[i]
        texts.append(page_text(page))
        image = page.render(scale=0.60).to_pil().convert('RGB')
        image.thumbnail((235, 335))
        tile = Image.new('RGB', (255, 365), 'white')
        tile.paste(image, ((255-image.width)//2, 5))
        ImageDraw.Draw(tile).text((10, 344), f'Analysis PDF page {i+1}', fill='black')
        thumbnails.append(tile)
        if i in {0, 2, 10, 18, 20, 29, 40, len(analysis)-1} or any(k in texts[-1] for k in ['3.2 Use case Details', '3.3 Activity Diagram', '3.4 Sequence Diagram', '3.5 Non-functional Requirements']):
            page.render(scale=1.5).to_pil().save(QA / f'analysis-page-{i+1:03d}.png')
        page.close()
    for start in range(0, len(thumbnails), 20):
        sheet = Image.new('RGB', (255*5,365*4), '#dfe4eb')
        for j, tile in enumerate(thumbnails[start:start+20]):
            sheet.paste(tile, ((j%5)*255,(j//5)*365))
        sheet.save(QA / f'contact-{start//20+1:02d}.png')
    old_page_comparisons = []
    for i in range(len(original)):
        before = original[i].render(scale=0.75).to_pil().convert('RGB')
        after = full[i].render(scale=0.75).to_pil().convert('RGB')
        same = before.size == after.size and ImageChops.difference(before, after).getbbox() is None
        old_page_comparisons.append({'physical_page':i+1, 'render_pixels_unchanged':same})
    joined = '\n'.join(texts)
    aux = (PROJECT / 'EPS_Analysis.aux').read_text(encoding='utf-8',errors='replace')
    labels = re.findall(r'\\newlabel\{(fig:[^}]+)\}', aux)
    manifest = json.loads((HERE / 'Report_Structure_Validation.json').read_text())
    caption_maps={}
    for name in ['EPS_Report','EPS_Analysis','EPS_Sequence_Diagrams']:
        aux_text=(PROJECT/(name+'.aux')).read_text(encoding='utf-8',errors='replace')
        caption_maps[name]=dict(re.findall(r'\\newlabel\{(fig:sequence-[^}]+)\}\{\{([^}]+)',aux_text))
    standalone_first=(PdfReader(PROJECT/'EPS_Sequence_Diagrams.pdf').pages[0].extract_text() or '')
    b3_proof=json.loads((HERE/'sequence_trials/repair_round1/report_page_B3_measurement.json').read_text(encoding='utf-8'))
    def find_caption_page(pdf, label_number):
        target='figure'+re.sub(r'[^0-9]','',label_number)+'b3fundescrow'
        hits=[]
        for index,page in enumerate(pdf.pages):
            normalized=re.sub(r'[^a-z0-9]','',(page.extract_text() or '').lower())
            if target in normalized: hits.append(index)
        assert len(hits)==1, f'Expected exactly one B3 caption {target}, found {hits}'
        return hits[0]
    views=json.loads((HERE/'sequence_models.json').read_text(encoding='utf-8-sig'))['diagrams']
    expected_report_figures=6+22+len(views)
    log = (PROJECT / 'EPS_Analysis.log').read_text(encoding='utf-8',errors='replace')
    # Render contact sheets for all three deliverables and preserve the B3 proof page from each.
    extra_review = {}
    for name in ['EPS_Report', 'EPS_Analysis', 'EPS_Sequence_Diagrams']:
        doc = pdfium.PdfDocument(PROJECT/(name+'.pdf'))
        tiles=[]
        b3page=None
        for i in range(len(doc)):
            page=doc[i]; txt=page_text(page)
            im=page.render(scale=0.34).to_pil().convert('RGB'); im.thumbnail((170,245))
            tile=Image.new('RGB',(185,265),'white'); tile.paste(im,((185-im.width)//2,3)); ImageDraw.Draw(tile).text((5,249),f'{name} {i+1}',fill='black'); tiles.append(tile)
            page.close()
        for start in range(0,len(tiles),20):
            sheet=Image.new('RGB',(925,1060),'#dfe4eb')
            for j,tile in enumerate(tiles[start:start+20]): sheet.paste(tile,((j%5)*185,(j//5)*265))
            sheet.save(QA/f'{name}-contact-{start//20+1:02d}.png')
        label_number=caption_maps[name]['fig:sequence-b3']
        b3page=find_caption_page(PdfReader(PROJECT/(name+'.pdf')),label_number)
        doc=pdfium.PdfDocument(PROJECT/(name+'.pdf')); doc[b3page].render(scale=1.5).to_pil().save(QA/f'{name}-B3-page-{b3page+1:03d}.png'); doc.close()
        with pdfplumber.open(PROJECT/(name+'.pdf')) as pdf:
            pg=pdf.pages[b3page]
            actual_counts={f'{size:.3f}':sum(round(c['size'],3)==size for c in pg.chars) for size in [7.152,7.802,9.103,10.403]}
            expected_counts=b3_proof['body_glyph_size_counts_pt']
            category_sizes=b3_proof['diagram_non_chrome_text_sizes_pt']
            category_min=min(float(size) for size in category_sizes)
            category_count_matches=all(actual_counts[size]==expected_counts[size] for size in actual_counts)
            extra_review[name]={'b3_physical_page':b3page+1,'b3_diagram_body_min_font_pt':category_min,
                'native_14px_body_glyph_count':actual_counts['9.103'],'accepted_proof_glyph_counts_match':category_count_matches,
                'b3_outside_page_chars':sum(c['x0']<0 or c['x1']>pg.width or c['top']<0 or c['bottom']>pg.height for c in pg.chars)}
        report = {
        'analysis_physical_pages':len(analysis), 'full_report_physical_pages':len(full),
        'original_physical_pages':len(original),
        'original_pages_render_comparison':old_page_comparisons,
        'expected_total_page_relation':len(full)==len(analysis)+len(original),
        'figure_labels':len(set(labels)), 'expected_figures':expected_report_figures, 'sequence_physical_pages':len(sequence), 'shared_sequence_source':(PROJECT/'sections/sequence.tex').is_file(), 'visual_review':extra_review,
        'eight_field_uc_specs':joined.count('Activation Event'),
        'unresolved_latex_references':'undefined references' in log or 'undefined on input line' in log,
        'overfull_boxes':len(re.findall('Overfull', log)),
        'missing_glyphs':len(re.findall('Missing character:',log)),
        'blank_analysis_pages':[i+1 for i,t in enumerate(texts) if len(t.strip())<20],
        'navigation':{name:check_links(PROJECT/name) for name in ['EPS_Analysis.pdf','EPS_Report.pdf']},
        'pdf_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [PROJECT/'EPS_Report.pdf',PROJECT/'EPS_Analysis.pdf',PROJECT/'EPS_Sequence_Diagrams.pdf']},
        'source_pdf_sha256':hashlib.sha256((PROJECT/'source/Introduction_Planning.pdf').read_bytes()).hexdigest(),
        'sequence_figure_labels':caption_maps['EPS_Analysis'], 'sequence_caption_maps_match':caption_maps['EPS_Report']==caption_maps['EPS_Analysis']==caption_maps['EPS_Sequence_Diagrams'], 'standalone_starts_at_section_3_4':('3.4 Sequence Diagram' in standalone_first),
        'build_log_warnings':{n:{'unresolved':'undefined references' in (PROJECT/(n+'.log')).read_text(encoding='utf-8',errors='replace'), 'overfull':len(re.findall('Overfull',(PROJECT/(n+'.log')).read_text(encoding='utf-8',errors='replace'))), 'missing_glyphs':len(re.findall('Missing character:',(PROJECT/(n+'.log')).read_text(encoding='utf-8',errors='replace')))} for n in ['EPS_Report','EPS_Analysis','EPS_Sequence_Diagrams']},
        'review_note':'Contact sheets and selected full pages saved for human visual inspection. Artifact checks are not EPS software tests.'}
    (HERE / 'PDF_Validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    assert report['expected_total_page_relation']
    assert all(x['render_pixels_unchanged'] for x in old_page_comparisons),'Original page rendering changed'
    assert report['figure_labels']==report['expected_figures']
    assert report['shared_sequence_source'] and report['sequence_physical_pages']==len(views)
    assert len(report['sequence_figure_labels'])==len(views)
    assert report['sequence_caption_maps_match'] and report['standalone_starts_at_section_3_4']
    assert all(v['b3_diagram_body_min_font_pt']>=9.0 and v['native_14px_body_glyph_count']==b3_proof['body_glyph_size_counts_pt']['9.103'] and v['accepted_proof_glyph_counts_match'] and v['b3_outside_page_chars']==0 for v in extra_review.values())
    assert all(not v['unresolved'] and not v['overfull'] and not v['missing_glyphs'] for v in report['build_log_warnings'].values())
    assert report['source_pdf_sha256']=='1cf077ae8e1794a04857f9e48fe70f965f5d57c56b2384854cf8e112d74b7435'
    assert report['eight_field_uc_specs']==22
    assert not report['unresolved_latex_references']
    assert not report['overfull_boxes'] and not report['missing_glyphs']
    assert not report['blank_analysis_pages']
    assert all(not r['invalid_targets'] for r in report['navigation'].values())
    print(json.dumps({k:v for k,v in report.items() if k not in ['original_pages_render_comparison','pdf_hashes']},indent=2))

if __name__ == '__main__':
    main()
