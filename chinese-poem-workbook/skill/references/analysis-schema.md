# Analysis input schema

Place UTF-8 `analysis.json` beside the verified `poem.json`. The renderer uses the full poem and translator attribution from `poem.json`; do not duplicate or silently revise them here.

```json
{
  "research_date": "2026-08-31",
  "poem_text_note": "Chinese witness and English translation provenance.",
  "orientation": [
    {"text": "Central reading in plain English.", "citations": [{"source": "source_id", "locator": "p. 12"}]}
  ],
  "line_readings": [
    {
      "lines": [1, 2],
      "heading": "Time will not wait",
      "analysis": "Close reading of exactly these poem lines.",
      "citations": []
    }
  ],
  "references_and_images": [
    {
      "term": "南山 — South Mountain",
      "analysis": "Literal referent, supported resonance, and uncertainty.",
      "citations": [{"source": "source_id", "locator": "p. 13"}]
    }
  ],
  "historical_context": [
    {"heading": "Political and literary setting", "paragraphs": [{"text": "Context.", "citations": []}]}
  ],
  "biography": [
    {"text": "Short evidence-based biography.", "citations": []}
  ],
  "reception": [
    {"text": "Transmission, attribution, and later reception.", "citations": []}
  ],
  "scholarly_excerpts": [
    {
      "source": "source_id",
      "quote": "No more than 25 words or Chinese characters.",
      "translation": "Optional labeled translation of a Chinese quotation.",
      "locator": "p. 12",
      "context": "Why this short quotation helps read the poem."
    }
  ],
  "own_analysis": [
    {"heading": "Synthesis", "paragraphs": [{"text": "This edition's original analysis.", "citations": []}]}
  ],
  "interpretive_limits": [
    {"text": "What the poem and available evidence do not establish.", "citations": []}
  ],
  "sources": [
    {
      "id": "source_id",
      "author": "Author",
      "title": "Title",
      "container": "Journal, book, repository, or institution",
      "year": "2020",
      "details": "Volume, issue, pages, publisher, DOI, or translator.",
      "url": "https://example.org/source",
      "local_path": "Optional relative or absolute local source path",
      "kind": "peer-reviewed article",
      "access_note": "Open PDF checked 2026-08-31; relevant pages 12–14."
    }
  ]
}
```

Required arrays are shown above and must be nonempty. `line_readings` may group adjacent lines, but collectively it must analyze every line exactly once; the validator rejects gaps and duplicates. Paragraphs are plain text. Do not insert Markdown, HTML, or raw LaTeX into content fields.

Each citation contains a `source` ID and optional `locator`. Every ID must exist in `sources`. Use URLs for online material and `local_path` for supplied sources; at least one is required. `access_note` states what was actually inspected, not what may exist behind a paywall.

The copied quotation is limited to 25 English words or Chinese characters. `translation` does not replace the exact original quote. Keep commentary outside the quote. This is a conservative reproduction limit, not a conclusion that every 25-word quotation is automatically lawful in every context.
