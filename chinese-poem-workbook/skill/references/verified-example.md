# Verified example — 31 August 2026

The revised reference is `assets/reference/My Old Home - Facing Pages Reference.pdf`: 25 Letter pages, verified individually at 120 DPI. `Overview.png`, `Study Page.png`, and `Tracing Page.png` preview the opening sequence. Use the full PDF and renderer as the layout reference, not merely a screenshot.

The output edition is `/Users/nick/Vaults/Knowledge/Poetry/My Old Home - Tao Yuanming`. It preserves the supplied Art-vault corpus, all 60 occurrence-level character analyses and the exact Watson wording. Audio is 60% of the original synthetic readings' pace, pitch-preserved (Mandarin 51.69 seconds; English 80.10 seconds).

Verified: 25-page mapping; six gray tracing copies for every character; aligned facing row rules; 34.8-point miniatures; 15-step sequences as 8 + 7; opaque #FF0000 strokes drawn last; no dark active-stroke centerline; full overview; no clipping or LaTeX overflow; 210 unchanged source/copy hashes. Pronunciation was not newly listening-verified.

Six regression tests pass, including a separate five-page/two-column layout fixture. Run with `WORKBOOK_RENDER_TEST=1 python3 scripts/test_workbook.py` to include that rendering test. The normal quick tests skip rendering. Run the skill-creator's `quick_validate.py` as well (requires PyYAML).

Installed via `/Users/nick/.agents/skills/chinese-poem-workbook`, a symlink to this repository skill. This is a standard skill installation, not a Template Gallery entry. Official skill-directory and symlink behavior: [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills).
