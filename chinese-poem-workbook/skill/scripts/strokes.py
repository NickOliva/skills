"""Licensed, vector-only stroke models. No generated/fabricated character shapes."""
from pathlib import Path
import hashlib
import json
import math
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

INK = HexColor('#252D31')
ACTIVE = HexColor('#FF0000')
PAST = HexColor('#737373')
FUTURE = HexColor('#E9E9E9')
TRACE = HexColor('#C7C7C7')
GLYPH_SIZE = 34.8
MAX_COLUMNS = 12


def svg_path(c, d):
    tokens = re.findall(r'[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', d)
    path = c.beginPath()
    i, command = 0, None
    current = start = (0, 0)
    while i < len(tokens):
        if tokens[i].isalpha():
            command = tokens[i]
            i += 1
        if command in ('Z', 'z'):
            path.close()
            current, command = start, None
            continue
        if command not in ('M', 'L', 'Q', 'C'):
            raise ValueError(f'Unsupported SVG command: {command}; obtain a supported source, do not guess.')
        count = {'M': 2, 'L': 2, 'Q': 4, 'C': 6}[command]
        v = [float(x) for x in tokens[i:i + count]]
        if len(v) != count:
            raise ValueError('Truncated SVG path')
        i += count
        if command == 'M':
            path.moveTo(*v)
            current = start = tuple(v)
            command = 'L'
        elif command == 'L':
            path.lineTo(*v)
            current = tuple(v)
        elif command == 'C':
            path.curveTo(*v)
            current = tuple(v[-2:])
        else:
            x0, y0 = current
            qx, qy, x1, y1 = v
            path.curveTo(x0 + 2 * (qx - x0) / 3, y0 + 2 * (qy - y0) / 3,
                         x1 + 2 * (qx - x1) / 3, y1 + 2 * (qy - y1) / 3, x1, y1)
            current = (x1, y1)
    return path


def load_character(ch, data_dir, fetch=False):
    data_dir = Path(data_dir)
    code = f'U{ord(ch):04X}'
    override = data_dir / f'{code}-override.json'
    if override.exists():
        data = json.loads(override.read_text())
        for key in ('source', 'license', 'y_down'):
            if key not in data:
                raise ValueError(f'{override}: missing {key}')
    elif ch == '為' and (data_dir / 'U70BA-AnimCJK.svg').exists():
        file = data_dir / 'U70BA-AnimCJK.svg'
        paths = ET.parse(file).getroot().findall('{http://www.w3.org/2000/svg}path')
        outlines = [p.attrib['d'] for p in paths if 'id' in p.attrib]
        medians = []
        for p in paths:
            if 'clip-path' in p.attrib:
                nums = [float(x) for x in re.findall(r'[-+]?\d+(?:\.\d+)?', p.attrib['d'])]
                medians.append(list(zip(nums[::2], nums[1::2])))
        if len(outlines) != 9:
            raise ValueError('The reviewed 為 override must have nine strokes.')
        data = {'strokes': outlines, 'medians': medians, 'y_down': True,
                'source': 'https://github.com/parsimonhi/animCJK/blob/ec5e17cca76c87587790bcbce5ea0b4d4fb753d6/svgsZhHant/28858.svg',
                'license': 'Arphic Public License', 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
    else:
        file = data_dir / f'{code}.json'
        url = 'https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0.1/' + urllib.parse.quote(ch) + '.json'
        if not file.exists():
            if not fetch:
                raise ValueError(f'No reviewed stroke data for {ch} ({code}); use --fetch-strokes then inspect the form.')
            with urllib.request.urlopen(url, timeout=30) as response:
                raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise ValueError('Unexpectedly large stroke file')
            candidate = json.loads(raw)
            if not candidate.get('strokes') or not candidate.get('medians'):
                raise ValueError(f'Invalid stroke source for {ch}')
            file.write_bytes(raw)
        data = json.loads(file.read_text()) | {
            'y_down': False, 'source': url, 'license': 'Arphic Public License',
            'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
    if not data.get('strokes') or len(data['strokes']) != len(data.get('medians', [])):
        raise ValueError(f'Missing strokes or centerlines for {ch}')
    if any(len(m) < 2 for m in data['medians']):
        raise ValueError(f'Incomplete direction data for {ch}')
    return data


def draw_glyph(c, data, x, y, size, step=None, color=INK):
    c.saveState()
    c.translate(x, y)
    c.scale(size / 1024, size / 1024)
    if data['y_down']:
        c.translate(0, 1024)
        c.scale(1, -1)
    else:
        c.translate(0, 124)
    # IMPORTANT: omit active outline from the background pass entirely.
    # Paint it LAST, opaque red; completed crossing strokes cannot cover it.
    for j, d in enumerate(data['strokes']):
        if j == step:
            continue
        c.setFillColor(color if step is None else PAST if j < step else FUTURE)
        c.drawPath(svg_path(c, d), fill=1, stroke=0)
    if step is not None:
        c.setFillColor(ACTIVE)
        c.drawPath(svg_path(c, data['strokes'][step]), fill=1, stroke=0)
        # White-only cues: never a black/dark centerline, halo outline or arrow.
        pts = data['medians'][step]
        c.setFillColor(white)
        c.circle(*pts[0], 20, stroke=0, fill=1)
        a, b = pts[-2], pts[-1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        if length:
            ux, uy = dx / length, dy / length
            p = c.beginPath()
            p.moveTo(*b)
            p.lineTo(b[0] - 42 * ux + 17 * uy, b[1] - 42 * uy - 17 * ux)
            p.lineTo(b[0] - 42 * ux - 17 * uy, b[1] - 42 * uy + 17 * ux)
            p.close()
            c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def panel_layout(n):
    rows = math.ceil(n / MAX_COLUMNS)
    cols = math.ceil(n / rows)
    return rows, cols


def character_assets(ch, data, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    code = f'U{ord(ch):04X}'
    c = canvas.Canvas(str(destination / f'{code}-model.pdf'), pagesize=(64, 64), pageCompression=1)
    draw_glyph(c, data, 0, 0, 64)
    c.showPage()
    c.save()
    n = len(data['strokes'])
    rows, cols = panel_layout(n)
    cw, chh = GLYPH_SIZE + 2, GLYPH_SIZE + 10.5
    width, height = cols * cw, rows * chh
    c = canvas.Canvas(str(destination / f'{code}-steps.pdf'), pagesize=(width, height), pageCompression=1)
    for j in range(n):
        x, y = (j % cols) * cw, (rows - 1 - j // cols) * chh
        draw_glyph(c, data, x + 1, y + 9.5, GLYPH_SIZE, step=j)
        c.setFillColor(INK)
        c.setFont('Helvetica', 7.1)
        c.drawCentredString(x + cw / 2, y + 1, str(j + 1))
    c.showPage()
    c.save()
    # Six standalone, pale glyphs: no instructions and no red/black steps.
    trace_cell, trace_size = 68, 56
    c = canvas.Canvas(str(destination / f'{code}-trace.pdf'), pagesize=(6 * trace_cell, 68), pageCompression=1)
    for j in range(6):
        draw_glyph(c, data, j * trace_cell + 6, 6, trace_size, color=TRACE)
    c.showPage()
    c.save()
    return {'code': code, 'strokes': n, 'rows': rows, 'columns': cols,
            'steps_per_row': [min(cols, n - i * cols) for i in range(rows)],
            'diagram_width': width, 'diagram_height': height, 'glyph_size_bp': GLYPH_SIZE,
            'trace_copies': 6, 'trace_glyph_size_bp': trace_size,
            'active_color': '#FF0000', 'active_painted_last': True, 'dark_active_centerline': False,
            'source': data['source'], 'license': data['license'], 'sha256': data.get('sha256')}
