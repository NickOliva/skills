#!/usr/bin/env python3
"""Create source-preserving editions and build verified Pandoc/Eisvogel PDFs."""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess
import unicodedata

from pypdf import PdfReader
from strokes import character_assets, load_character

PACKAGE = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = Path('/Users/nick/Vaults/Knowledge/Poetry')
SKIP_NAMES = {'.DS_Store', '__pycache__', '.git'}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def save_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def han(ch):
    return ('\u3400' <= ch <= '\u9fff' or '\uf900' <= ch <= '\ufaff'
            or '\U00020000' <= ch <= '\U000323af')


def normalized(text):
    return ''.join(c for c in text if not c.isspace() and not unicodedata.category(c).startswith('P'))


def read_input(path):
    data = json.loads(Path(path).read_text())
    for field in ('title_english', 'poet_english', 'translator', 'short_citation', 'source_note'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f'Missing {field}')
    if not re.search('[A-Za-z]', data['title_english']) or any(c in data['title_english'] for c in '/\\\x00'):
        raise ValueError('Use an English-first title without path separators.')
    if not data.get('sources') or not data.get('lines'):
        raise ValueError('Supply sources and complete poem lines.')
    for n, line in enumerate(data['lines'], 1):
        if line.get('line') != n:
            raise ValueError('Line numbers must start at 1 and be consecutive.')
        for key in ('chinese', 'english', 'context', 'characters'):
            if not line.get(key):
                raise ValueError(f'Line {n}: missing {key}')
        expected = ''.join(c for c in line['chinese'] if han(c))
        actual = ''.join(x.get('character', '') for x in line['characters'])
        if actual != expected or not expected:
            raise ValueError(f'Line {n}: character analysis does not exactly reproduce the Chinese line.')
        for entry in line['characters']:
            if len(entry['character']) != 1 or not all(entry.get(k) for k in ('pinyin', 'meaning', 'form')):
                raise ValueError(f'Line {n}: incomplete character analysis.')
    for language in ('chinese', 'english'):
        complete = data.setdefault('complete_' + language, [x[language] for x in data['lines']])
        if not all(isinstance(x, str) and x for x in complete):
            raise ValueError(f'Empty {language} overview line')
        if normalized(''.join(complete)) != normalized(''.join(x[language] for x in data['lines'])):
            raise ValueError(f'Full {language} poem differs from study units; resolve alignment without losing text.')
        spoken = data.get('audio', {}).get(language + '_spoken_lines')
        if spoken is not None:
            if len(spoken) != len(data['lines']) or normalized(''.join(spoken)) != normalized(''.join(complete)):
                raise ValueError(f'{language} spoken text differs from the poem.')
    layout = data.get('layout', {})
    if layout.get('paper', 'letter') not in ('letter', 'legal', 'a3'):
        raise ValueError('Paper must be letter, legal or a3.')
    if any(layout.get(x + '_columns', 1) not in (1, 2) for x in ('chinese', 'english')):
        raise ValueError('Overview columns must be 1 or 2.')
    if not isinstance(layout.get('compact_margins', False), bool):
        raise ValueError('compact_margins must be true or false.')
    return data


def safe_name(text):
    name = re.sub(r'[\x00-\x1f/\\:*?"<>|]', '-', text).strip(' .')
    if not name or name in ('.', '..'):
        raise ValueError('Invalid folder name')
    return name


def copy_sources(sources, output):
    records, skipped = [], []
    background = output / 'Background'
    background.mkdir()
    for source_string in sources:
        given = Path(source_string).expanduser()
        if given.is_symlink():
            raise ValueError(f'Choose an explicit source, not a symlink: {given}')
        source = given.resolve(strict=True)
        if source == output or source in output.parents:
            raise ValueError('Output must not be inside an input source tree.')
        destination = background / source.name
        i = 2
        while destination.exists():
            destination = background / f'{source.stem} - {i}{source.suffix}'
            i += 1
        paths = sorted(source.rglob('*')) if source.is_dir() else [source]
        if source.is_dir():
            destination.mkdir()
        for item in paths:
            relative = item.relative_to(source) if source.is_dir() else Path(source.name)
            if any(part in SKIP_NAMES for part in relative.parts):
                skipped.append({'source': str(item), 'reason': 'non-content cache/version-control metadata'})
                continue
            if item.is_symlink():
                skipped.append({'source': str(item), 'reason': 'symlink not followed'})
                continue
            if not item.is_file():
                continue
            target = destination / relative if source.is_dir() else destination
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            before, after = sha(item), sha(target)
            if before != after:
                raise ValueError(f'Copy hash mismatch: {item}')
            records.append({'source': str(item), 'copy': str(target.relative_to(output)),
                            'sha256': before, 'bytes': target.stat().st_size})
    report = {'created_utc': datetime.now(timezone.utc).isoformat(), 'files': records, 'skipped': skipped}
    save_json(output / 'Source Copies.json', report)
    return report


def create_edition(input_path, source_paths, root=DEFAULT_ROOT):
    data = read_input(input_path)
    root = Path(root).expanduser().resolve()
    name = safe_name(data['title_english'] + ' - ' + data['poet_english'])
    # Resolve dangerous source/output nesting before creating anything.
    for source in source_paths:
        p = Path(source).expanduser().resolve(strict=True)
        if p == root or p in root.parents:
            raise ValueError('Selected input contains the output root; select a narrower source.')
    root.mkdir(parents=True, exist_ok=True)
    output, n = root / name, 2
    while True:
        try:
            output.mkdir()
            break
        except FileExistsError:
            output, n = root / f'{name} - {n}', n + 1
    save_json(output / 'poem.json', data)
    copy_sources(source_paths, output)
    (output / 'Sources.md').write_text('# Sources\n\n' + data['source_note'] + '\n\n' +
        '\n'.join('- ' + json.dumps(s, ensure_ascii=False) for s in data['sources']) +
        '\n\nExact local copies and hashes are listed in `Source Copies.json`. Originals were not modified.\n')
    return output


def latex(text):
    # Escape content before applying the only supported markup, bold and Han font.
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    def escaped(s):
        replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
                        '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
        s = ''.join(replacements.get(c, c) for c in s)
        s = s.replace('--', '-{}-')
        return re.sub(r'[\u3400-\u9fff]+', lambda m: r'{\hanfont ' + m[0] + '}', s)
    return ''.join(r'\textbf{' + escaped(p[2:-2]) + '}' if p.startswith('**') else escaped(p) for p in parts)


def font_header(paper, compact_margins=False):
    fonts = Path('/System/Library/Fonts/Supplemental')
    if not (fonts / 'Songti.ttc').exists() or not (fonts / 'Georgia.ttf').exists():
        raise ValueError('Reviewed Georgia/Songti fonts unavailable. Configure and verify suitable installed fonts before building.')
    font_options = lambda name: [f'Path={fonts}/', 'Extension=.ttf', f'UprightFont={name}',
                                f'BoldFont={name} Bold', f'ItalicFont={name} Italic', f'BoldItalicFont={name} Bold Italic']
    vertical_margin = '9mm' if compact_margins else '12mm'
    return {'papersize': paper, 'fontsize': '10pt', 'classoption': ['twoside'],
            'geometry': [f'top={vertical_margin}', f'bottom={vertical_margin}', 'inner=17mm', 'outer=13mm'],
            'mainfont': 'Georgia', 'mainfontoptions': font_options('Georgia'),
            'sansfont': 'Arial', 'sansfontoptions': font_options('Arial'),
            'titlepage': False, 'disable-header-and-footer': True, 'lang': 'en-US',
            'header-includes': [r'''
\usepackage{graphicx}
\newfontfamily\hanfont[Path=/System/Library/Fonts/Supplemental/,FontIndex=5]{Songti.ttc}
\definecolor{Ink}{HTML}{252D31}
\definecolor{Quiet}{HTML}{59636B}
\definecolor{Rule}{HTML}{D5DADD}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlength{\parfillskip}{0pt plus 1fil}
\setlength{\emergencystretch}{2em}
\newcommand{\divider}{\par\nointerlineskip{\color{Rule}\rule{\linewidth}{0.35pt}}\par}
\newcommand{\smallnote}[1]{{\sffamily\fontsize{7.5}{9.1}\selectfont\color{Quiet}#1\par}}
\newsavebox{\headerbox}
\newsavebox{\pagebox}
\newsavebox{\chinesebox}
\newsavebox{\englishbox}
\newdimen\rowgap
\newdimen\usedheight
\newdimen\pageheight
\pageheight=\dimexpr\textheight-12pt\relax
''']}


def figure(code, kind, width):
    return r'\includegraphics[width=' + str(width) + r'bp]{Workbook Sources/diagrams/' + code + '-' + kind + '.pdf}'


def column_text(items, columns, render):
    chunks = [items] if columns == 1 else [items[:(len(items) + 1) // 2], items[(len(items) + 1) // 2:]]
    rendered = []
    for chunk in chunks:
        rendered.append(r'\begin{minipage}[t]{' + (r'\linewidth' if columns == 1 else r'.48\linewidth') + '}' +
                        '\n'.join(render(x) for x in chunk) + r'\end{minipage}')
    return r'\hfill'.join(rendered)


def cover(data, assets):
    lines = []
    def chinese_line(s):
        glyphs = [figure(assets[c]['code'], 'model', 21) if c in assets else latex(c) for c in s]
        return r'{\centering ' + r'\hspace{3pt}'.join(glyphs) + r'\par}\nointerlineskip\vspace{1pt}'
    title = r'{\fontsize{24}{28}\selectfont ' + latex(data['title_english']) + r'\par}'
    byline = latex(data['poet_english']) + (' · ' + latex(data['poet_chinese']) if data.get('poet_chinese') else '')
    lines += [r'\sbox{\chinesebox}{\begin{minipage}{\linewidth}', title,
              r'\vspace{4pt}{\sffamily\fontsize{10}{12}\selectfont ' + byline + r'\par}',
              r'\vspace{4pt}{\hanfont\fontsize{11}{13}\selectfont ' + latex(data.get('title_chinese', '')) + r'\par}\vspace{10pt}',
              column_text(data['complete_chinese'], data.get('layout', {}).get('chinese_columns', 1), chinese_line),
              r'\end{minipage}}']
    lines += [r'\sbox{\englishbox}{\begin{minipage}{\linewidth}',
              r'{\sffamily\fontsize{9}{11}\selectfont\color{Quiet}ENGLISH · ' + latex(data['translator']) + r'\par}\vspace{8pt}',
              column_text(data['complete_english'], data.get('layout', {}).get('english_columns', 1),
                          lambda s: r'{\fontsize{12.8}{16}\selectfont ' + latex(s) + r'\par}'),
              r'\end{minipage}}',
              r'\typeout{WORKBOOK-COVER-CHINESE=\the\dimexpr\ht\chinesebox+\dp\chinesebox\relax}',
              r'\typeout{WORKBOOK-COVER-ENGLISH=\the\dimexpr\ht\englishbox+\dp\englishbox\relax}',
              r'\ifdim\dimexpr\ht\chinesebox+\dp\chinesebox\relax>.47\pageheight\errmessage{Chinese overview too tall; use columns or larger paper}\fi',
              r'\ifdim\dimexpr\ht\englishbox+\dp\englishbox\relax>.36\pageheight\errmessage{English overview too tall; use columns or larger paper}\fi',
              r'\noindent\begin{minipage}[t][\pageheight][t]{\textwidth}',
              r'\begin{minipage}[t][.49\pageheight][t]{\linewidth}\usebox{\chinesebox}\end{minipage}\par\nointerlineskip',
              r'\divider\vspace{9pt}\usebox{\englishbox}\par\vfill\divider\vspace{4pt}',
              r'\smallnote{HOW TO FOLLOW THE STEPS. Numbered panels run left to right, then continue on the next row. Bright red is the new stroke; gray is completed; pale gray is still to come. White dot = start; white arrow = finish/direction. Lift between panels, not at every bend.}',
              r'\vspace{3pt}\smallnote{READING \& SOUND. This edition reads left to right. Traditional vertical Chinese reads downward in columns from right to left. Pinyin and audio use modern Mandarin, not ancient pronunciation. Recordings are synthetic, at 60\% of the reference speed. Print double-sided, flip on the long edge.}',
              r'\vspace{3pt}\smallnote{' + latex(data['source_note']) +
              r' Models: modern regular script, not the poet\textquotesingle{}s handwriting. Stroke conventions can vary; sources and licenses are in Workbook Sources.}',
              r'\vspace{3pt}\smallnote{' + latex(data['short_citation']) + r'\hfill 1}', r'\end{minipage}\par']
    return '\n'.join(lines)


def model(entry, asset):
    return '\n'.join([r'\begin{minipage}[t]{70pt}\vspace{0pt}\centering',
        figure(asset['code'], 'model', 53) + r'\par',
        r'{\sffamily\fontsize{10.5}{12}\selectfont ' + latex(entry['pinyin']) + r'\par}',
        r'{\sffamily\fontsize{7.5}{9}\selectfont\color{Quiet}' + str(asset['strokes']) + r' strokes\par}',
        r'\end{minipage}%'])


def row_box(entry, asset, box):
    return '\n'.join(['\\sbox{\\' + box + r'}{\begin{minipage}{\linewidth}', model(entry, asset),
        r'\hspace{9pt}\begin{minipage}[t]{\dimexpr\linewidth-79pt\relax}\vspace{0pt}',
        r'{\fontsize{9}{11.2}\selectfont ' + latex(entry['meaning']) + r'\par}',
        r'\vspace{3pt}{\sffamily\fontsize{7.8}{9.5}\selectfont\color{Quiet}\textbf{Form.} ' + latex(entry['form']) + r'\par}\vspace{3pt}',
        figure(asset['code'], 'steps', asset['diagram_width']) + r'\par\end{minipage}\par\end{minipage}}'])


def facing_pages(rec, data, assets, box_names):
    n = rec['line']
    boxes = box_names[:len(rec['characters'])]
    out = [r'\sbox{\headerbox}{\begin{minipage}{\linewidth}',
           r'{\fontsize{19}{23}\selectfont ' + latex(data['title_english']) + ' — line ' + str(n) + r'\par}',
           r'\vspace{3pt}{\sffamily\fontsize{9}{11}\selectfont\color{Quiet}' + latex(data['poet_english']) +
           ' · English: ' + latex(data['translator']) + r'\par}',
           r'\vspace{5pt}{\hanfont\fontsize{22}{25}\selectfont ' + r'\hspace{7pt}'.join(latex(c) for c in rec['chinese']) + r'\par}',
           r'\vspace{5pt}{\itshape\fontsize{15}{18.5}\selectfont ' + latex(rec['english']) + r'\par}',
           r'\vspace{5pt}{\sffamily\fontsize{8.3}{10.5}\selectfont\color{Quiet}' + latex(rec['context']) + r'\par}',
           r'\vspace{5pt}\divider\vspace{4pt}\end{minipage}}']
    for entry, box in zip(rec['characters'], boxes):
        out.append(row_box(entry, assets[entry['character']], box))
    out.append(r'\usedheight=\dimexpr\ht\headerbox+\dp\headerbox' +
               ''.join('+\\ht\\' + b + '+\\dp\\' + b for b in boxes) + r'+19pt\relax')
    out.append(r'\rowgap=\dimexpr\pageheight-\usedheight\relax')
    out.append(r'\divide\rowgap by ' + str(max(1, len(boxes) - 1)))
    out.append(r'\typeout{WORKBOOK-LINE-' + str(n) + r'-ROWGAP=\the\rowgap}')
    out.append(r'\ifdim\rowgap<6pt\errmessage{Line ' + str(n) + r' too tall; choose larger paper, never shrink the stroke glyphs}\fi')
    for practice in (False, True):
        out += [r'\newpage', r'\noindent\begin{minipage}[t][\pageheight][t]{\textwidth}', r'\usebox{\headerbox}\par\nointerlineskip']
        for i, (entry, box) in enumerate(zip(rec['characters'], boxes)):
            if practice:
                out += ['\\begin{minipage}[c][\\dimexpr\\ht\\' + box + '+\\dp\\' + box + r'\relax][c]{\linewidth}',
                        model(entry, assets[entry['character']]),
                        r'\hspace{9pt}\begin{minipage}[t]{\dimexpr\linewidth-79pt\relax}\vspace{0pt}',
                        figure(assets[entry['character']]['code'], 'trace', 408), r'\end{minipage}\end{minipage}\par\nointerlineskip']
            else:
                out += ['\\usebox{\\' + box + r'}\par\nointerlineskip']
            if i < len(boxes) - 1:
                out += [r'\vspace{\dimexpr\rowgap/2-0.2pt\relax}\divider\vspace{\dimexpr\rowgap/2-0.2pt\relax}']
        out += [r'\vfill\vspace{5pt}\smallnote{' + latex(data['short_citation']) + ' · ' + ('Tracing' if practice else 'Study') +
                r'\hfill ' + str(2 * n + int(practice)) + '}', r'\end{minipage}\par']
    return '\n'.join(out)


def build(poem_path, fetch=False):
    poem_path = Path(poem_path).resolve()
    data = read_input(poem_path)
    output = poem_path.parent
    sources = output / 'Workbook Sources'
    sources.mkdir(exist_ok=True)
    for directory in ('eisvogel', 'stroke-data'):
        target = sources / 'assets' / directory
        if not target.exists():
            shutil.copytree(PACKAGE / 'assets' / directory, target)
    fixture_source = PACKAGE / 'assets/reference/my-old-home-lines.json'
    fixture_target = sources / 'assets/reference/my-old-home-lines.json'
    if fixture_source.exists() and fixture_source.resolve() != fixture_target.resolve():
        fixture_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fixture_source, fixture_target)
    target_scripts = sources / 'scripts'
    if Path(__file__).resolve().parent != target_scripts.resolve():
        target_scripts.mkdir(exist_ok=True)
        for script in Path(__file__).parent.glob('*.py'):
            shutil.copy2(script, target_scripts / script.name)
    unique = sorted({c['character'] for line in data['lines'] for c in line['characters']})
    assets = {c: character_assets(c, load_character(c, sources / 'assets/stroke-data', fetch), sources / 'diagrams') for c in unique}
    save_json(sources / 'Diagram Audit.json', assets)
    layout = data.get('layout', {})
    header = font_header(layout.get('paper', 'letter'), layout.get('compact_margins', False))
    # Eisvogel would otherwise insert an automatic title before our custom cover.
    header['pdf-title'] = data['title_english'] + ' - Chinese Poem Workbook'
    max_chars = max(len(x['characters']) for x in data['lines'])
    box_names = ['row' + chr(65 + i // 26) + chr(65 + i % 26) for i in range(max_chars)]
    header['header-includes'].append('\n'.join('\\newsavebox{\\' + b + '}' for b in box_names))
    latex_header = sources / 'Style.tex'
    latex_header.write_text('\n'.join(header.pop('header-includes')) + '\n')
    content = [cover(data, assets)] + [facing_pages(rec, data, assets, box_names) for rec in data['lines']]
    # JSON mappings are valid YAML, without requiring a separate YAML library.
    md = '---\n' + json.dumps(header, ensure_ascii=False, indent=2) + '\n...\n\n```{=latex}\n' + '\n'.join(content) + '\n```\n'
    name = safe_name(data['title_english']) + ' - Chinese Poem Workbook'
    md_path, pdf_path = output / (name + '.md'), output / (name + '.pdf')
    md_path.write_text(md)
    cmd = ['pandoc', str(md_path), '--from=markdown+raw_tex', '--template=' + str(sources / 'assets/eisvogel/eisvogel.latex'),
           '--include-in-header=' + str(latex_header), '--pdf-engine=tectonic', '--output=' + str(pdf_path)]
    tex_cmd = [x for x in cmd if not x.startswith('--pdf-engine=') and not x.startswith('--output=')]
    subprocess.run(tex_cmd + ['--standalone', '--to=latex', '--output=' + str(sources / 'workbook.tex')], cwd=output, check=True)
    result = subprocess.run(cmd, cwd=output, capture_output=True, text=True)
    (sources / 'Build.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError('Pandoc/Eisvogel failed; see Workbook Sources/Build.log\n' + result.stderr[-8000:])
    (output / 'Poem and Character Guide.md').write_text(readable(data, assets))
    save_json(sources / 'Page Map.json', [{'page': 1, 'kind': 'complete poem'}] +
              [{'page': 2 * r['line'] + p, 'line': r['line'], 'kind': 'tracing' if p else 'study'} for r in data['lines'] for p in (0, 1)])
    validate(poem_path, require_audio=False)
    return pdf_path


def readable(data, assets):
    text = [f"# {data['title_english']}\n\n{data['poet_english']} · {data.get('poet_chinese', '')}\n\n{data.get('title_chinese', '')}\n",
            '## Chinese\n\n' + '  \n'.join(data['complete_chinese']),
            f"\n## English — {data['translator']}\n\n" + '  \n'.join(data['complete_english']),
            '\n' + data['source_note'] + '\n']
    for line in data['lines']:
        text += [f"\n## Line {line['line']}: {line['chinese']}\n\n{line['english']}\n\n{line['context']}\n"]
        for c in line['characters']:
            text += [f"\n### {c['character']} — {c['pinyin']} ({assets[c['character']]['strokes']} strokes)\n\n{c['meaning']}\n\nForm: {c['form']}\n"]
    return '\n'.join(text)


def validate(poem_path, require_audio=True):
    poem_path = Path(poem_path).resolve()
    data = read_input(poem_path)
    root = poem_path.parent
    pdf = root / (safe_name(data['title_english']) + ' - Chinese Poem Workbook.pdf')
    pages = PdfReader(pdf).pages
    expected = 1 + 2 * len(data['lines'])
    if len(pages) != expected:
        raise ValueError(f'Expected {expected} pages, got {len(pages)}')
    cover_text = normalized(pages[0].extract_text())
    for english in data['complete_english']:
        if normalized(english) not in cover_text:
            raise ValueError('English overview text missing from page 1: ' + english)
    for line in data['lines']:
        for index in (2 * line['line'] - 1, 2 * line['line']):
            text = normalized(pages[index].extract_text())
            if normalized('line ' + str(line['line'])) not in text or normalized(line['english']) not in text:
                raise ValueError(f'Page {index + 1}: wrong line or missing translation')
            if normalized(line['chinese']) not in text:
                raise ValueError(f'Page {index + 1}: missing Chinese text')
    copied = json.loads((root / 'Source Copies.json').read_text())
    for file in copied['files']:
        if sha(root / file['copy']) != file['sha256']:
            raise ValueError('Background source copy changed: ' + file['copy'])
    audit = json.loads((root / 'Workbook Sources/Diagram Audit.json').read_text())
    if not all(x['trace_copies'] == 6 and x['glyph_size_bp'] >= 34 and x['active_color'] == '#FF0000' for x in audit.values()):
        raise ValueError('Invalid tracing or stroke model configuration')
    if require_audio and not (root / 'Audio Sources/Recording Details.json').exists():
        raise ValueError('Both-language audio still required')
    if (root / 'Audio Sources/Recording Details.json').exists():
        recordings = json.loads((root / 'Audio Sources/Recording Details.json').read_text())['readings']
        if {r['language'] for r in recordings} != {'chinese', 'english'}:
            raise ValueError('Both Chinese and English recordings are required.')
        for recording in recordings:
            if sha(root / recording['mp3']) != recording['sha256'] or not (root / recording['master']).is_file():
                raise ValueError('Missing or changed audio deliverable.')
            origin = recording['origin']
            if origin.get('preserved_reference') and sha(root / origin['preserved_reference']) != origin['source_sha256']:
                raise ValueError('Preserved audio master changed.')
    log = (root / 'Workbook Sources/Build.log').read_text()
    warnings = [line for line in log.splitlines() if any(s in line.lower() for s in ('overfull', 'missing character', 'too tall'))]
    if warnings:
        raise ValueError('Layout/font warnings must be resolved: ' + '\n'.join(warnings))
    report = {'pdf': str(pdf), 'pages': len(pages), 'lines': len(data['lines']),
              'character_occurrences': sum(len(x['characters']) for x in data['lines']),
              'unique_characters': len(audit), 'copied_sources_verified': len(copied['files']),
              'layout': 'cover, then even-study / odd-tracing', 'six_traces_per_character': True,
              'visual_review': 'Separate human/agent visual inspection required; this report is structural only.',
              'audio_metadata_present': (root / 'Audio Sources/Recording Details.json').exists()}
    save_json(root / 'Workbook Sources/Validation Report.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    new = sub.add_parser('new')
    new.add_argument('--input', required=True)
    new.add_argument('--source', action='append', default=[])
    new.add_argument('--output-root', default=str(DEFAULT_ROOT))
    make = sub.add_parser('build')
    make.add_argument('--poem', required=True)
    make.add_argument('--fetch-strokes', action='store_true')
    check = sub.add_parser('validate')
    check.add_argument('--poem', required=True)
    args = parser.parse_args()
    if args.command == 'new':
        print(create_edition(args.input, args.source, args.output_root))
    elif args.command == 'build':
        print(build(args.poem, args.fetch_strokes))
    else:
        print(json.dumps(validate(args.poem), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
