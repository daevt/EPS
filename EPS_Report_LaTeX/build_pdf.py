"""Compile both retained PDF deliverables from main.tex (two passes each)."""
from pathlib import Path
import argparse
import shutil
import subprocess

PROJECT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--analysis-only', action='store_true')
    parser.add_argument('--assemble-only', action='store_true', help='Keep existing compiled PDFs and restore the original prefix pages.')
    parser.add_argument('--passes', type=int, default=2)
    args = parser.parse_args()
    executable = shutil.which('pdflatex')
    fallback = Path.home() / 'AppData/Local/Programs/TeXLive/2026/bin/windows/pdflatex.exe'
    if not executable and fallback.is_file():
        executable = str(fallback)
    if not executable:
        raise RuntimeError('Install a TeX distribution with pdflatex, or add it to PATH.')
    jobs = [('EPS_Analysis', r'\def\AnalysisOnly{1}\input{main.tex}'), ('EPS_Sequence_Diagrams', 'EPS_Sequence_Diagrams.tex')]
    if not args.analysis_only:
        jobs.insert(0, ('EPS_Report', 'main.tex'))
    for name, source in ([] if args.assemble_only else jobs):
        for pass_number in range(1, args.passes + 1):
            result = subprocess.run([executable, '-interaction=nonstopmode', '-halt-on-error',
                                     '-file-line-error', '-jobname=' + name, source],
                                    cwd=PROJECT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log = result.stdout.decode('utf-8', errors='replace')
            (PROJECT / (name + '.build.log')).write_text(log, encoding='utf-8')
            if result.returncode:
                print(log[-14000:])
                raise RuntimeError(f'{name}: compilation failed on pass {pass_number}')
            print(f'{name}: pass {pass_number} complete')
    if not args.analysis_only:
        # Preserve the original pages as original PDF page objects, avoiding
        # fractional transforms introduced by an include-PDF TeX backend.
        from pypdf import PdfReader, PdfWriter
        original = PdfReader(PROJECT / 'source/Introduction_Planning.pdf')
        compiled = PdfReader(PROJECT / 'EPS_Analysis.pdf')
        writer = PdfWriter()
        writer.append(original)
        writer.append(compiled)
        writer.add_metadata({'/Title':'EPS Report - Analysis MVP','/Author':'Group 1'})
        temporary = PROJECT / 'EPS_Report.assembled.pdf'
        with temporary.open('wb') as stream:
            writer.write(stream)
        temporary.replace(PROJECT / 'EPS_Report.pdf')
        print('Original Introduction/Planning page objects preserved unchanged.')
    print('PDF output saved beside main.tex.')

if __name__ == '__main__':
    main()
