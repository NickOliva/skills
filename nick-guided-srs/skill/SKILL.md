---
name: nick-guided-srs
description: Distill course guidebooks and other learning sources into atomic, significant SRS-ready facts and quotations, grouped by the source's lectures, chapters, articles, or comparable structure. Use when Nick asks to auto-ingest source material into an Active SRS Sources Markdown note; do not create flashcards or make keep/discard decisions.
---

# Nick Guided SRS

Perform **1. Auto Ingest Source** by turning source material into reviewable checkbox data for Nick's guided SRS workflow.

## Workflow

1. Resolve the destination Markdown note, normally beneath `~/Vaults/Knowledge/Learning/Active SRS Sources`. Treat its containing folder as the source set unless Nick identifies other files.
2. Read every requested source completely. For a Great Courses guidebook, ingest every lecture guide rather than the table of contents, bibliography, advertising, or other publishing matter. Extract PDF text page-by-page and visually inspect pages when layout could affect meaning.
3. Reconstruct the source's ordered learning structure. Preserve lecture, chapter, article, or equivalent titles and numbering exactly enough to trace each item back to the source. Treat a separately supplied timeline as its own lecture-like top-level grouping when requested.
4. Distill the content into significant, atomic checklist items. Use a simple subgroup only when it materially improves navigation inside a long source unit.
5. Write the result at the bottom of the destination note under a single `# Source Data` heading. On reruns, replace only the existing `# Source Data` section; preserve everything above it.
6. Verify completeness, ordering, atomicity, source fidelity, and Markdown shape before finishing.

## Item standard

Write each item as `- [ ] <statement>`.

- Express one learnable proposition per item. Split claims joined only because they appeared in one source sentence.
- Make the statement understandable on its own: name the relevant person, text, school, place, or period instead of relying on dangling pronouns or the preceding item.
- Prefer durable, high-value claims: definitions, doctrines, arguments, contrasts, causes, consequences, practices, works, chronology, and relationships between ideas.
- Retain meaningful dates, technical terms, and uncertainty such as `c.` or disputed attribution. Normalize obvious PDF extraction artifacts, but do not silently strengthen the source's claim.
- Use direct quotation marks only for wording worth remembering. Keep quoted wording exact, concise, and attributed in the same item. Otherwise paraphrase faithfully without quotation marks.
- Exclude administrative prose, repeated lecture previews, suggested-reading lists, bibliography entries, photo captions, and trivia that does not improve understanding.
- Do not add outside facts, corrections, interpretations, questions, answers, tags, priorities, or keep/discard judgments during auto-ingest.

## Output structure

Use this shape, adapting labels to the source:

```markdown
# Source Data

## Lecture 1: Exact Lecture Title

### Optional simple subgroup

- [ ] One self-contained fact.
- [ ] Another self-contained fact.

## Timeline: Source Timeline Title

- [ ] c. 500 BCE — One self-contained chronological fact.
```

Keep top-level source units in source order. Place an added timeline after the ordinary course units unless Nick requests another position. Do not put checkboxes outside `# Source Data`.

## Final checks

- Every requested source unit appears once and has substantive items.
- Titles and numbering match the source, and ordering is stable.
- Each checkbox contains one source-supported proposition with enough context to stand alone.
- Exact quotations are clearly quoted and attributed; paraphrases are not presented as quotations.
- Near-duplicates, extraction debris, and orphaned headings are absent.
- The destination contains exactly one `# Source Data` heading and all pre-existing content above it remains intact.
