#!/usr/bin/env python3
"""Build and validate a sourced Chinese-poem analysis with Pandoc/Eisvogel."""
from pathlib import Path
import argparse
from datetime import date
import json
import re
import shutil
import subprocess
import unicodedata

from pypdf import PdfReader


PACKAGE = Path(__file__).resolve().parent.parent
HAN_RE = re.compile(r'[\u3400-\u9fff\uf900-\ufaff]+')
CJK_RUN_RE = re.compile(r'[\u3000-\u303f\u3400-\u9fff\uf900-\ufaff]+')


def safe_name(text):
    value = re.sub(r'[\x00-\x1f/\\:*?"<>|]', '-', text).strip(' .')
    if not value:
        raise ValueError('Invalid English title')
    return value


def normalized(text):
    return ''.join(c for c in text if not c.isspace() and not unicodedata.category(c).startswith('P'))


def word_count(text):
    """Count Han characters conservatively as words for quotation limits."""
    han = sum(len(match.group(0)) for match in HAN_RE.finditer(text))
    no_han = HAN_RE.sub(' ', text)
    return han + len(re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", no_han))


def tex(text):
    replacements = {
        '\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
        '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
    }
    escaped = ''.join(replacements.get(c, c) for c in str(text)).replace('--', '-{}-')
    return CJK_RUN_RE.sub(lambda m: r'{\hanfont ' + m.group(0) + '}', escaped)


def tex_url(url):
    # \url handles ordinary URL punctuation. Percent is escaped because TeX treats it as a comment.
    return str(url).replace('%', r'\%').replace('#', r'\#')


def load_json(path):
    return json.loads(Path(path).read_text())


def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def poem_lines(poem, language):
    return poem.get('complete_' + language) or [line[language] for line in poem['lines']]


def validate_inputs(poem, analysis):
    for field in ('title_english', 'poet_english', 'translator', 'lines'):
        if not poem.get(field):
            raise ValueError(f'poem.json is missing {field}')
    for field in ('research_date', 'orientation', 'line_readings', 'references_and_images',
                  'historical_context', 'biography', 'reception', 'own_analysis',
                  'interpretive_limits', 'scholarly_excerpts', 'sources'):
        if not analysis.get(field):
            raise ValueError(f'analysis.json is missing {field}')
    sources = analysis['sources']
    ids = [s.get('id') for s in sources]
    if not all(ids) or len(ids) != len(set(ids)):
        raise ValueError('Every source needs a unique id')
    by_id = {s['id']: s for s in sources}
    for source in sources:
        for field in ('author', 'title', 'year', 'kind', 'access_note'):
            if not source.get(field):
                raise ValueError(f"Source {source['id']} is missing {field}")
        if not source.get('url') and not source.get('local_path'):
            raise ValueError(f"Source {source['id']} needs a URL or local path")

    paragraph_groups = ['orientation', 'historical_context', 'biography', 'reception',
                        'own_analysis', 'interpretive_limits']
    for group in paragraph_groups:
        for item in analysis[group]:
            paragraphs = item.get('paragraphs') if isinstance(item, dict) and 'paragraphs' in item else [item]
            for paragraph in paragraphs:
                if not paragraph.get('text'):
                    raise ValueError(f'Empty paragraph in {group}')
                for citation in paragraph.get('citations', []):
                    if citation.get('source') not in by_id:
                        raise ValueError(f"Unknown source id {citation.get('source')} in {group}")
    covered_lines = []
    for reading in analysis['line_readings']:
        if not reading.get('lines') or not reading.get('analysis'):
            raise ValueError('Every line reading needs lines and analysis')
        if any(n < 1 or n > len(poem['lines']) for n in reading['lines']):
            raise ValueError('Line reading refers to a nonexistent poem line')
        covered_lines.extend(reading['lines'])
        for citation in reading.get('citations', []):
            if citation.get('source') not in by_id:
                raise ValueError('Unknown source id in line reading')
    if sorted(covered_lines) != list(range(1, len(poem['lines']) + 1)):
        raise ValueError('Line readings must cover every poem line exactly once')
    for item in analysis['references_and_images']:
        if not item.get('term') or not item.get('analysis'):
            raise ValueError('Every reference/image entry needs term and analysis')
        for citation in item.get('citations', []):
            if citation.get('source') not in by_id:
                raise ValueError('Unknown source id in reference/image entry')
    for excerpt in analysis['scholarly_excerpts']:
        if excerpt.get('source') not in by_id or not excerpt.get('quote') or not excerpt.get('context'):
            raise ValueError('Every excerpt needs a known source, quote, and context')
        count = word_count(excerpt['quote'])
        if count > 25:
            raise ValueError(f'Scholarly excerpt exceeds 25 words/characters ({count}): {excerpt["quote"]}')
    return by_id


def citation_tex(citations, by_id):
    if not citations:
        return ''
    labels = []
    for citation in citations:
        source = by_id[citation['source']]
        number = source['_number']
        label = f'S{number}'
        if source.get('url'):
            label = r'\href{' + tex_url(source['url']) + '}{' + label + '}'
        if citation.get('locator'):
            label += ', ' + tex(citation['locator'])
        labels.append(label)
    return r'\hspace{0.2em}{\sffamily\fontsize{8}{9.4}\selectfont\color{Quiet}[' + '; '.join(labels) + ']} '


def paragraphs_tex(items, by_id):
    out = []
    for item in items:
        if isinstance(item, dict) and 'heading' in item:
            out.append(r'\subsection{' + tex(item['heading']) + '}')
            paragraphs = item['paragraphs']
        else:
            paragraphs = [item]
        for paragraph in paragraphs:
            out.append(tex(paragraph['text']) + citation_tex(paragraph.get('citations', []), by_id) + r'\par\medskip')
    return '\n'.join(out)


def cover_tex(poem, analysis):
    chinese = poem_lines(poem, 'chinese')
    english = poem_lines(poem, 'english')
    source_note = analysis.get('poem_text_note') or poem.get('source_note', '')
    out = [
        r'\thispagestyle{empty}',
        r'\noindent\begin{minipage}[t][\textheight][t]{0.97\linewidth}',
        r'{\fontsize{25}{29}\selectfont ' + tex(poem['title_english']) + r'\par}',
        r'\vspace{3pt}{\sffamily\fontsize{10}{12}\selectfont\color{Quiet}POEM ANALYSIS\quad ' +
        tex(poem['poet_english']) + (r' · ' + tex(poem.get('poet_chinese', '')) if poem.get('poet_chinese') else '') + r'\par}',
        r'\vspace{3pt}{\hanfont\fontsize{11}{14}\selectfont ' + tex(poem.get('title_chinese', '')) + r'\par}',
        r'\vspace{9pt}\par\noindent\color{Rule}\rule{\linewidth}{0.5pt}\par\color{Ink}\vspace{9pt}',
        r'\begin{minipage}[t]{0.27\linewidth}',
        r'{\sffamily\fontsize{8.5}{10}\selectfont\color{Quiet}CHINESE\par}\vspace{7pt}',
    ]
    for line in chinese:
        out.append(r'{\hanfont\fontsize{14}{19}\selectfont ' + tex(line) + r'\par}')
    out += [r'\end{minipage}\hfill\begin{minipage}[t]{0.67\linewidth}',
            r'{\sffamily\fontsize{8.5}{10}\selectfont\color{Quiet}ENGLISH · ' + tex(poem['translator']) + r'\par}\vspace{7pt}']
    size = '9.3' if len(english) > 10 else '10.3'
    leading = '12.3' if len(english) > 10 else '13.8'
    for line in english:
        out.append(r'{\fontsize{' + size + '}{' + leading + r'}\selectfont ' + tex(line) + r'\par}')
    out += [r'\end{minipage}', r'\vfill\par\noindent\color{Rule}\rule{\linewidth}{0.5pt}\par\color{Ink}\vspace{5pt}',
            r'{\sffamily\fontsize{7.8}{9.5}\selectfont\color{Quiet}' + tex(source_note) + r'\par}',
            r'\vspace{4pt}{\sffamily\fontsize{7.8}{9.5}\selectfont\color{Quiet}Research checked ' +
            tex(analysis['research_date']) + r'. Short quotations are reproduced for private study; the analysis distinguishes quotation, paraphrase, and original interpretation.\par}',
            r'\end{minipage}\clearpage']
    return '\n'.join(out)


def source_entry(source):
    pieces = [source['author'] + '.', source['title'] + '.', source.get('container', ''), str(source['year']) + '.']
    if source.get('details'):
        pieces.append(source['details'])
    line = ' '.join(x for x in pieces if x).replace('..', '.')
    out = r'\textbf{S' + str(source['_number']) + '.} ' + tex(line)
    if source.get('url'):
        out += r'\par{\sffamily\fontsize{8}{9.5}\selectfont\url{' + tex_url(source['url']) + r'}\par}'
    if source.get('local_path'):
        out += r'\par{\sffamily\fontsize{8}{9.5}\selectfont ' + tex(source['local_path']) + r'\par}'
    out += r'{\sffamily\fontsize{8}{9.5}\selectfont\color{Quiet}' + tex(source['kind'] + '. ' + source['access_note']) + r'\par}\medskip'
    return out


def build_document(poem, analysis, by_id):
    out = [cover_tex(poem, analysis), r'\tableofcontents\clearpage',
           r'\section{Orientation}', paragraphs_tex(analysis['orientation'], by_id),
           r'\section{Close reading}']
    for reading in analysis['line_readings']:
        records = [poem['lines'][n - 1] for n in reading['lines']]
        line_label = ', '.join(str(n) for n in reading['lines'])
        out += [r'\needspace{10\baselineskip}', r'\subsection{' + tex(reading.get('heading', 'Lines ' + line_label)) + '}',
                r'{\hanfont\fontsize{15}{20}\selectfont ' + r'\quad '.join(tex(x['chinese']) for x in records) + r'\par}',
                r'\vspace{3pt}{\itshape ' + r' / '.join(tex(x['english']) for x in records) + r'\par}\smallskip',
                tex(reading['analysis']) + citation_tex(reading.get('citations', []), by_id) + r'\par\medskip']
    out.append(r'\section{Images, references, and key terms}')
    for item in analysis['references_and_images']:
        out += [r'\needspace{6\baselineskip}', r'\subsection{' + tex(item['term']) + '}',
                tex(item['analysis']) + citation_tex(item.get('citations', []), by_id) + r'\par\medskip']
    out += [r'\section{Historical context}', paragraphs_tex(analysis['historical_context'], by_id),
            r'\section{The poet}', paragraphs_tex(analysis['biography'], by_id),
            r'\section{Reception and attribution}', paragraphs_tex(analysis['reception'], by_id),
            r'\section{Short scholarly excerpts}']
    for excerpt in analysis['scholarly_excerpts']:
        source = by_id[excerpt['source']]
        out += [r'\needspace{8\baselineskip}', r'\begin{quote}\color{Accent}\large “' + tex(excerpt['quote']) + r'”\end{quote}']
        if excerpt.get('translation'):
            out.append(r'{\itshape Translation: “' + tex(excerpt['translation']) + r'”\par}\smallskip')
        cite = citation_tex([{'source': excerpt['source'], 'locator': excerpt.get('locator', '')}], by_id)
        out.append(tex(excerpt['context']) + cite + r'\par\medskip')
    out += [r'\section{My analysis}', paragraphs_tex(analysis['own_analysis'], by_id),
            r'\section{Interpretive limits}', paragraphs_tex(analysis['interpretive_limits'], by_id),
            r'\section{Works consulted}']
    out.extend(source_entry(s) for s in analysis['sources'])
    return '\n'.join(out)


def style_tex(title):
    return r'''
\usepackage{xcolor}
\usepackage{fontspec}
\usepackage{microtype}
\usepackage{needspace}
\usepackage{xurl}
\newfontfamily\hanfont[Path=/System/Library/Fonts/Supplemental/,FontIndex=5]{Songti.ttc}
\definecolor{Ink}{HTML}{263238}
\definecolor{Quiet}{HTML}{617078}
\definecolor{Rule}{HTML}{D8DFE2}
\definecolor{Accent}{HTML}{733B31}
\color{Ink}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\setlength{\emergencystretch}{2em}
\pagestyle{plain}
\setcounter{tocdepth}{1}
\hypersetup{colorlinks=true,linkcolor=Accent,urlcolor=Accent}
'''


def excerpts_markdown(analysis):
    by_id = {s['id']: s for s in analysis['sources']}
    lines = ['# Analysis sources and copied excerpts', '',
             f"Research checked {analysis['research_date']}. Every quotation is 25 words/Chinese characters or fewer. Full copyrighted articles and books were not copied.", '']
    for excerpt in analysis['scholarly_excerpts']:
        source = by_id[excerpt['source']]
        lines += [f"## {source['author']} — {source['title']}", '', f"> {excerpt['quote']}", '']
        if excerpt.get('translation'):
            lines += [f"Translation: {excerpt['translation']}", '']
        lines += [f"Context: {excerpt['context']}", '', f"Locator: {excerpt.get('locator', 'online excerpt')}", '']
        if source.get('url'):
            lines += [f"Source: {source['url']}", '']
    return '\n'.join(lines)


def build(poem_path, analysis_path=None):
    poem_path = Path(poem_path).resolve()
    analysis_path = Path(analysis_path or poem_path.with_name('analysis.json')).resolve()
    poem, analysis = load_json(poem_path), load_json(analysis_path)
    by_id = validate_inputs(poem, analysis)
    for number, source in enumerate(analysis['sources'], 1):
        source['_number'] = number

    root = poem_path.parent
    source_dir = root / 'Analysis Sources'
    source_dir.mkdir(exist_ok=True)
    asset_dir = source_dir / 'assets' / 'eisvogel'
    if not asset_dir.exists():
        shutil.copytree(PACKAGE / 'assets' / 'eisvogel', asset_dir)
    script_dir = source_dir / 'scripts'
    script_dir.mkdir(exist_ok=True)
    if Path(__file__).resolve() != (script_dir / 'analysis.py').resolve():
        shutil.copy2(__file__, script_dir / 'analysis.py')
    shutil.copy2(analysis_path, source_dir / 'analysis.json')
    shutil.copy2(poem_path, source_dir / 'poem.json')
    (source_dir / 'Source Excerpts.md').write_text(excerpts_markdown(analysis))

    metadata = {
        'papersize': 'letter', 'fontsize': '10.5pt', 'classoption': ['twoside'],
        'geometry': ['top=20mm', 'bottom=19mm', 'inner=22mm', 'outer=18mm'],
        'mainfont': 'Georgia',
        'mainfontoptions': ['Path=/System/Library/Fonts/Supplemental/', 'Extension=.ttf',
                            'UprightFont=Georgia', 'BoldFont=Georgia Bold', 'ItalicFont=Georgia Italic',
                            'BoldItalicFont=Georgia Bold Italic'],
        'sansfont': 'Arial',
        'sansfontoptions': ['Path=/System/Library/Fonts/Supplemental/', 'Extension=.ttf',
                            'UprightFont=Arial', 'BoldFont=Arial Bold', 'ItalicFont=Arial Italic',
                            'BoldItalicFont=Arial Bold Italic'],
        'titlepage': False, 'disable-header-and-footer': True, 'lang': 'en-US',
        'pdf-title': poem['title_english'] + ' - Poem Analysis',
    }
    style = source_dir / 'Style.tex'
    style.write_text(style_tex(poem['title_english']))
    body = build_document(poem, analysis, by_id)
    md = '---\n' + json.dumps(metadata, ensure_ascii=False, indent=2) + '\n...\n\n```{=latex}\n' + body + '\n```\n'
    name = safe_name(poem['title_english']) + ' - Poem Analysis'
    md_path, pdf_path = root / (name + '.md'), root / (name + '.pdf')
    md_path.write_text(md)
    template = source_dir / 'assets/eisvogel/eisvogel.latex'
    cmd = ['pandoc', str(md_path), '--from=markdown+raw_tex', '--template=' + str(template),
           '--include-in-header=' + str(style), '--pdf-engine=tectonic', '--output=' + str(pdf_path)]
    tex_cmd = [x for x in cmd if not x.startswith('--pdf-engine=') and not x.startswith('--output=')]
    subprocess.run(tex_cmd + ['--standalone', '--to=latex', '--output=' + str(source_dir / 'analysis.tex')], cwd=root, check=True)
    result = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    (source_dir / 'Build.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError('Pandoc/Eisvogel failed; see Analysis Sources/Build.log\n' + result.stderr[-8000:])
    validate(poem_path, analysis_path)
    return pdf_path


def validate(poem_path, analysis_path=None):
    poem_path = Path(poem_path).resolve()
    analysis_path = Path(analysis_path or poem_path.with_name('analysis.json')).resolve()
    poem, analysis = load_json(poem_path), load_json(analysis_path)
    validate_inputs(poem, analysis)
    root = poem_path.parent
    pdf = root / (safe_name(poem['title_english']) + ' - Poem Analysis.pdf')
    reader = PdfReader(pdf)
    if len(reader.pages) < 8:
        raise ValueError(f'Analysis is unexpectedly short: {len(reader.pages)} pages')
    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
    cover = normalized(reader.pages[0].extract_text() or '')
    for line in poem_lines(poem, 'chinese') + poem_lines(poem, 'english'):
        if normalized(line) not in cover:
            raise ValueError('Opening page is missing poem text: ' + line)
    for heading in ('Orientation', 'Close reading', 'Historical context', 'The poet',
                    'Short scholarly excerpts', 'My analysis', 'Interpretive limits', 'Works consulted'):
        if heading not in text:
            raise ValueError('Missing analysis section: ' + heading)
    for excerpt in analysis['scholarly_excerpts']:
        expected = excerpt.get('translation') or excerpt['quote']
        if normalized(expected) not in normalized(text):
            raise ValueError('PDF is missing a scholarly excerpt')
    log = (root / 'Analysis Sources/Build.log').read_text()
    bad = [line for line in log.splitlines() if any(x in line.lower() for x in ('overfull', 'missing character'))]
    if bad:
        raise ValueError('Layout/font warning: ' + '\n'.join(bad))
    report = {
        'pdf': str(pdf), 'pages': len(reader.pages), 'poem_lines': len(poem['lines']),
        'sources': len(analysis['sources']), 'scholarly_excerpts': len(analysis['scholarly_excerpts']),
        'quotation_limit': '25 words/Chinese characters per excerpt',
        'full_poem_on_opening_page': True,
        'visual_review': 'Separate full-page visual review required.',
        'validated': date.today().isoformat(),
    }
    save_json(root / 'Analysis Sources/Validation Report.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    make = sub.add_parser('build')
    make.add_argument('--poem', required=True)
    make.add_argument('--analysis')
    check = sub.add_parser('validate')
    check.add_argument('--poem', required=True)
    check.add_argument('--analysis')
    args = parser.parse_args()
    if args.command == 'build':
        print(build(args.poem, args.analysis))
    else:
        print(json.dumps(validate(args.poem, args.analysis), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
