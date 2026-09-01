"""Offline regression tests; the actual 25-page rendering needs separate visual QA."""
from pathlib import Path
import copy
import json
import os
import tempfile
import unittest

from workbook import PACKAGE, create_edition, read_input, latex, build
from strokes import ACTIVE, draw_glyph, load_character, panel_layout
from analysis import validate_inputs, word_count


def fixture():
    records = json.loads((PACKAGE / 'assets/reference/my-old-home-lines.json').read_text())
    return {'title_english': 'My Old Home', 'poet_english': 'Tao Yuanming', 'translator': 'Burton Watson',
            'short_citation': 'Miscellaneous Poems, No. 7', 'source_note': 'Supplied script, p. 6.',
            'sources': [{'label': 'User-supplied study reference'}], 'lines': records}


class WorkbookTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('WORKBOOK_RENDER_TEST') == '1', 'Set WORKBOOK_RENDER_TEST=1 for a full second-layout build.')
    def test_generic_five_page_build(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = fixture()
            data['title_english'] = 'Layout Fixture'
            data['lines'] = data['lines'][:2]
            data['layout'] = {'english_columns': 2, 'chinese_columns': 2}
            file = root / 'input.json'
            file.write_text(json.dumps(data))
            output = create_edition(file, [], root / 'edition')
            pdf = build(output / 'poem.json')
            from pypdf import PdfReader
            self.assertEqual(len(PdfReader(pdf).pages), 5)

    def test_balanced_rows(self):
        self.assertEqual(panel_layout(15), (2, 8))
        self.assertEqual(panel_layout(24), (2, 12))
        self.assertEqual(panel_layout(4), (1, 4))

    def test_forms(self):
        folder = PACKAGE / 'assets/stroke-data'
        self.assertEqual(len(load_character('為', folder)['strokes']), 9)
        self.assertEqual(len(load_character('遲', folder)['strokes']), 15)
        with self.assertRaises(ValueError):
            load_character('龘', Path(tempfile.gettempdir()))

    def test_input_integrity_and_fresh_folders(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            input_file = root / 'input.json'
            data = fixture()
            input_file.write_text(json.dumps(data))
            self.assertEqual(len(read_input(input_file)['lines']), 12)
            source = root / 'source.txt'
            source.write_text('Original source remains unchanged.')
            one = create_edition(input_file, [source], root / 'editions')
            two = create_edition(input_file, [source], root / 'editions')
            self.assertNotEqual(one, two)
            self.assertEqual((one / 'Background/source.txt').read_text(), source.read_text())
            broken = copy.deepcopy(data)
            broken['lines'][0]['characters'].pop()
            input_file.write_text(json.dumps(broken))
            with self.assertRaises(ValueError):
                read_input(input_file)
            broken = copy.deepcopy(data)
            broken['complete_english'] = ['Something different']
            input_file.write_text(json.dumps(broken))
            with self.assertRaises(ValueError):
                read_input(input_file)

    def test_latex_safety(self):
        self.assertIn(r'\textbackslash{}input', latex(r'\input{secret}'))
        self.assertEqual(latex('100% & **word**'), r'100\% \& \textbf{word}')

    def test_red_is_last_and_no_dark_overlay(self):
        # Inspect calls, not a prewritten audit flag: active red is the last
        # non-white painted path, and no stroked outline is ever drawn.
        from reportlab.pdfgen.canvas import Canvas
        with tempfile.TemporaryDirectory() as temp:
            canvas = Canvas(str(Path(temp) / 'test.pdf'))
            fills = []
            state = {'color': None}
            original_color, original_path = canvas.setFillColor, canvas.drawPath
            def color(value, *args, **kwargs):
                state['color'] = value
                return original_color(value, *args, **kwargs)
            def path(value, *args, **kwargs):
                self.assertEqual(kwargs.get('stroke'), 0)
                fills.append(state['color'])
                return original_path(value, *args, **kwargs)
            canvas.setFillColor, canvas.drawPath = color, path
            data = load_character('日', PACKAGE / 'assets/stroke-data')
            draw_glyph(canvas, data, 0, 0, 64, step=1)
            self.assertEqual(fills[-2], ACTIVE)
            self.assertEqual(fills.count(ACTIVE), 1)
            canvas.save()

    def test_analysis_quote_limit_and_source_resolution(self):
        poem = fixture()
        paragraph = {'text': 'A sourced claim.', 'citations': [{'source': 'scholar', 'locator': 'p. 1'}]}
        data = {
            'research_date': '2026-08-31',
            'orientation': [paragraph],
            'line_readings': [{'lines': list(range(1, 13)), 'analysis': 'A close reading.', 'citations': []}],
            'references_and_images': [{'term': '日', 'analysis': 'The sun.', 'citations': []}],
            'historical_context': [paragraph], 'biography': [paragraph], 'reception': [paragraph],
            'own_analysis': [paragraph], 'interpretive_limits': [paragraph],
            'scholarly_excerpts': [{'source': 'scholar', 'quote': 'A short exact quotation.', 'context': 'Useful context.'}],
            'sources': [{'id': 'scholar', 'author': 'A. Scholar', 'title': 'Study', 'year': '2020',
                         'kind': 'article', 'access_note': 'Checked.', 'url': 'https://example.org'}]
        }
        self.assertEqual(len(validate_inputs(poem, data)), 1)
        self.assertEqual(word_count('一個歸字真是含藏著最大的安慰'), 14)
        broken = copy.deepcopy(data)
        broken['scholarly_excerpts'][0]['quote'] = ' '.join(['word'] * 26)
        with self.assertRaises(ValueError):
            validate_inputs(poem, broken)
        broken = copy.deepcopy(data)
        broken['orientation'][0]['citations'][0]['source'] = 'missing'
        with self.assertRaises(ValueError):
            validate_inputs(poem, broken)


if __name__ == '__main__':
    unittest.main()
