---
name: test-elementary-knowledge
description: Outline all relevant elementary school concepts with five solved example problems per concept, or create a grade-specific 20-page practice PDF for a selected concept using Pandoc and Eisvogel. Use for foundational subject guides, worked examples, and focused printable workbooks across elementary subjects.
---

# Test Elementary Knowledge

Support two modes: a comprehensive concept guide and a focused practice workbook. Keep chat replies short; do not shorten the requested artifacts to match that preference. There is no one-page or 300–500-word limit.

## Choose the mode and scope

- A subject request, such as “make a math output,” means **concept guide** unless the user asks for practice. A request to focus on an outline item, drill a concept, or make a workbook means **practice workbook**. Resolve selected item numbers against the existing outline; do not regenerate that outline instead of the requested workbook.
- Reuse the topic, grade, curriculum, country, and output destination already established in the conversation. Ask only for information that is missing and necessary.
- For a concept guide without a specified grade, cover foundational knowledge across elementary school; use kindergarten through grade 5 as the stated default scope unless context specifies another school system. A grade-specific request narrows coverage to that grade and essential prerequisites.
- A workbook needs a specific topic and grade. If the grade is missing, ask which grade to use; do not silently choose one. A missing curriculum or country alone need not block work: state a reasonable assumption.
- Match number ranges, operations, vocabulary, reading load, representations, and problem complexity to the requested grade. Check authoritative educational sources when uncertain about grade expectations or completeness, and before claiming alignment with named standards. Do not import advanced skills solely to fill pages.

## Mode 1: Concept guide

Produce a Markdown document in this order:

1. **Scope and complete outline.** Outline all relevant foundational concepts within the requested subject and grade range, ordered by prerequisites. Give each concept a stable number or ID. Use unnumbered category headings to group concepts; each numbered item must be a distinct, teachable concept, not a bundle hiding several skills.
2. **Five solved examples for every outline item.** Repeat each item's ID and title, briefly explain it, then give exactly five distinct example problems and their solutions. Show the steps or reasoning, not only the final answer. Progress from straightforward examples to varied applications without exceeding the grade scope. For non-math subjects, use appropriate questions, tasks, or interpretations with model answers and explanations.

Every numbered outline item, including any numbered subitem, requires its own five solved examples. Do not give five examples total or omit examples for a listed concept. Do not reduce the outline to fit an arbitrary length limit. Write large guides in sections if needed, then assemble the complete document before delivering it.

Check the outline against the subject's foundational domains and any requested standards. Reconcile the outline with the example sections: N numbered concepts must have N matching sections and 5N solved examples. Check every solution and any essential qualifications or units. Include linked sources when research was needed; do not claim universal curriculum completeness.

The default guide is Markdown. When a PDF is also requested, use the same Pandoc/Eisvogel builder described in [references/workbook-production.md](references/workbook-production.md), without the workbook page-count restriction.

## Mode 2: Focused practice workbook

Read [references/workbook-production.md](references/workbook-production.md) before authoring the workbook.

- Create **exactly 20 pages of student problems** about the selected concept, at the requested grade level. Cover its relevant subskills with deliberate progression and varied problems, not filler or repeated questions with cosmetic changes.
- Reserve sufficient space for the actual work: calculations, written explanations, diagrams, or drawings. Adjust problem count and workspace to the task and grade. Keep each prompt and its work area on the same page.
- Put the topic and grade on the workbook, use clear instructions and page numbers, and keep the design clean and printable. Do not spend the 20 pages on a cover, contents page, answer key, or blank padding.
- Solve every problem while authoring. Keep solutions in a **separate Markdown answer key**, using the same page and problem IDs. A separate answer-key PDF is optional when requested; answers must not consume the 20 student pages or appear beside the unsolved problems.
- Build the PDF with **Pandoc and the bundled Eisvogel template**. Retain the editable Markdown source. Use [scripts/build_pdf.py](scripts/build_pdf.py) to enforce the final PDF page count; do not silently substitute another generator.
- Inspect the rendered pages, verify usable work space and grade appropriateness, reconcile every problem with the answer key, and fix layout or content defects before delivery. Twenty source sections do not prove the PDF has 20 pages.

## Save and deliver

- Honor the requested or established folder, creating it if needed. Otherwise use `<workspace-root>/elementary-knowledge/`. Save guides as `<subject>-concept-guide.md`; save workbooks as `<topic>-grade-<grade>-practice.md` and `.pdf`, with `<topic>-grade-<grade>-answers.md` alongside them.
- Preserve unrelated existing files. Update a prior artifact when requested; otherwise choose an unused descriptive filename.
- If PDF tooling is unavailable, preserve the completed source and answer key, identify the missing dependency, and report the PDF as incomplete. Do not present Markdown as a completed PDF.
- Finish with artifact links and one short sentence. Do not paste the artifact into chat or repeat its contents.
