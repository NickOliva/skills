---
skill_name: chinese-poem-workbook
installation_scope: machine
installation_target: ~/.agents/skills/chinese-poem-workbook
installation_method: symlink
---

# Chinese Poem Workbook Requirements

## Purpose

Create accurate bilingual Chinese-poetry calligraphy workbooks with slow audio, or separate sourced poem-analysis editions, while preserving text, translation, provenance, and editable build materials.

## Requirements

1. Support distinct workbook and analysis modes. When both are requested, share one verified poem text but produce separate deliverables.
2. Resolve the exact poem, title status, poet, translator, textual variants, lineation, and source before building. Never silently normalize characters or substitute a translation.
3. Preserve supplied source material and provenance in the poem folder without deleting originals or following out-of-scope symlinks.
4. Represent every Chinese character occurrence in `poem.json` with contextual pronunciation, meaning and grammatical function, form guidance, and an exact line mapping.
5. Use licensed vector stroke data. Missing or mismatched glyphs must be resolved and visually checked, never invented.
6. The workbook must contain exactly `1 + 2N` pages: one complete-poem opening page followed by a study and tracing page for every line.
7. Study pages must include the full line, readable model glyphs, pinyin, stroke counts, contextual explanations, and numbered incremental stroke diagrams.
8. Facing tracing pages must align with the study pages and provide six large light-gray tracing copies per character.
9. Active strokes must be opaque bright red without a dark underdrawing; completed and future strokes must remain visually distinct.
10. Produce Chinese and English MP3 listening copies plus WAV masters at 60% of the verified source speed with pitch preserved. Label synthetic audio and record engine, voice, source, speed, duration, and validation.
11. Analysis editions must include the complete poem and selected translation, line-by-line close reading, context, biography, reception, short attributable scholarly excerpts, original synthesis, interpretive limits, and works consulted.
12. Separate literal meaning, translation choices, scholarly claims, and original interpretation. Preserve uncertain attribution and do not invent biography or symbolism.
13. Keep quoted online excerpts within 25 English words or Chinese characters per source excerpt and retain citations and locators.
14. Build with the supplied scripts and Pandoc/Eisvogel assets. Preserve canonical JSON, editable Markdown, renderers, licenses, source hashes, logs, and verification notes.
15. Render and inspect every PDF page and representative facing spreads. Validate page mapping, glyph variants, clipping, line completeness, audio signal and duration, and source-copy hashes.

## Boundaries

- Do not fabricate calligraphy, pronunciation, translation, scholarship, attribution, or audio.
- Do not upload private source material or incur paid service costs without authorization.
- Do not redistribute supplied copyrighted translations outside the user’s requested workspace.
- Do not append analysis to the calligraphy workbook.

## Success evidence

- The complete Chinese poem and complete selected English translation appear without omission.
- Every study line has one aligned study/tracing pair and every character occurrence has complete data.
- PDFs are legible and visually verified; audio files decode, contain real signal, and preserve all words.
- The output folder is reproducible from retained inputs, scripts, assets, licenses, and provenance.
