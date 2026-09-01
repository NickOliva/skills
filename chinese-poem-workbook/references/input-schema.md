# Canonical input

Use UTF-8 JSON. `new` copies the input into the new output folder as `poem.json`; paths in the input do not cause arbitrary files to be read. Source files are copied only through explicit `--source` arguments. Pass audio master paths explicitly to the audio script.

```json
{
  "title_english": "My Old Home",
  "title_chinese": "雜詩十二首·其七",
  "poet_english": "Tao Yuanming",
  "poet_chinese": "陶淵明",
  "translator": "Burton Watson",
  "short_citation": "Miscellaneous Poems, No. 7 | Watson translation",
  "source_note": "English wording follows the supplied exhibition script, p. 6.",
  "sources": [
    {"label": "User-provided script", "location": "Video_script.pdf", "note": "Page 6"}
  ],
  "layout": {"paper": "letter", "english_columns": 1, "chinese_columns": 1, "compact_margins": false},
  "complete_chinese": ["日月不肯遲"],
  "complete_english": ["Sun and moon refuse to slow their pace"],
  "lines": [
    {
      "line": 1,
      "chinese": "日月不肯遲",
      "english": "Sun and moon refuse to slow their pace",
      "context": "Explain the complete line's syntax and any departure in the literary translation.",
      "characters": [
        {"character": "日", "pinyin": "rì", "meaning": "**Sun; day.** Together with 月 forms the subject.", "form": "Write the internal bar before closing the bottom."}
      ]
    }
  ],
  "audio": {
    "speed": 0.6,
    "chinese_voice": "Meijia",
    "english_voice": "Samantha",
    "chinese_rate": 120,
    "english_rate": 125,
    "chinese_spoken_lines": ["日月不肯遲。"],
    "english_spoken_lines": ["Sun and moon refuse to slow their pace"]
  }
}
```

This is a schema illustration, **not a buildable one-line poem**: provide an entry for all five characters and the complete actual poem, never only the illustrated character.

Required: English title, English poet name (or explicit “Anonymous”), translator label, short citation, source note, sources, and nonempty sequential `lines`. Chinese title/poet may be omitted only when genuinely unavailable. Use an English-first title with no path separators. Meaning and form strings are plain text with optional `**bold**` phrases; arbitrary raw LaTeX is not accepted as content.

Each `characters` array must reproduce the Chinese line exactly after stripping punctuation/spacing. Count **occurrences**, including repeated characters. Pinyin is context-sensitive; assign readings per occurrence, not per unique glyph. Prefer tone marks. The renderer doesn't invent missing analyses. Unknown readings must be resolved or explicitly flagged before publication, not guessed.

The optional complete-poem arrays control the opening page's line breaks. If omitted, they use the study lines. Their combined wording must match all the study units (whitespace/Chinese punctuation aside), so no verse can disappear. To accommodate a translation with different lineation, put its complete original lines in `complete_english` and carefully align equivalent passages in study units without changing the actual words. Document the alignment. `chinese_columns` and `english_columns` accept 1 or 2; columns read down first, then continue at the top of the next column. Chinese display runs horizontally left to right unless a specifically reviewed alternate renderer is provided.

`compact_margins: true` uses 9 mm rather than 12 mm top and bottom margins without shrinking text or stroke diagrams. Use it only after a default Letter build reports a dense line, and confirm that every object remains inside the print-safe bounds. `audio` is optional; defaults are specified above. Explicit spoken-line arrays may add editorial Chinese punctuation for phrasing, but must preserve the words and line count. A pronunciation-only override should be documented, not silently applied. A supplied audio recording must be checked against these texts before passing it as a master; the script can test its signal, not recognize its content.

Do not put machine secrets, API keys, private identifying information, or unrelated account data into this file.
