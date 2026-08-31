# Pandoc/Eisvogel workbook production

Use this workflow for focused practice PDFs. The supplied builder also handles optional concept-guide PDFs, without imposing a 20-page limit on those guides.

## Plan the student pages

Confirm the selected concept and grade from the conversation. Plan 20 pages that stay within that scope: prerequisite checks where needed, individual subskills, varied applications, and mixed review of the selected concept. Adjust the sequence to the subject; do not force an unrelated page quota for each stage.

Write original, unambiguous problems. Vary representations, contexts, and reasoning demands within grade expectations. For reading or science tasks, supply the passage, data, or diagram needed to answer. Keep those materials beside their questions. Avoid problems that require unavailable manipulatives or unstated information.

Use a small number of well-spaced problems per page. As a starting point, allow 35–50 mm of writing height for a short calculation and 55–80 mm for multi-step work, drawing, or written explanation; younger learners may need larger writing areas. Two to four problems often fit, but choose density by the work required, not a fixed question count. Count prompt text, headings, and gaps in the page budget. Do not shrink fonts or work areas just to obtain 20 pages.

Create a separate answer key as problems are written. Identify answers by page and problem, include worked steps or model responses, and check that every problem is solvable and has a matching, correct answer. The key is outside the student PDF's 20-page count.

## Author the Markdown source

The builder uses the bundled Eisvogel template, `assets/workbook-layout.tex`, and `scripts/workbook-layout.lua`. The Lua filter inserts a page break between `.practice-page` blocks and keeps each `.problem` block together with its work area. Use exactly 20 page blocks for a workbook. Each must contain a useful page of problems, not blank padding.

Use this shape for each page, with unique IDs and real content:

````markdown
---
title: "Addition within 1,000"
subtitle: "Grade 3 practice"
lang: en-US
header-left: "Addition within 1,000"
header-right: "Grade 3"
footer-left: "Practice workbook"
---

:::: {.practice-page #page-01}
# Practice 1: Add by place value

Name: ____________________  Date: __________

Show how you found each sum.

::: {.problem #p01-01}
**1.** Calculate $236 + 142$.

\workarea{45mm}
:::

::: {.problem #p01-02}
**2.** A library has 124 books on one shelf and 253 on another.
How many books are on the two shelves altogether?

\workarea{60mm}
:::
::::
````

Continue with `.practice-page` blocks through page 20, changing the page heading and IDs. Do not add a trailing manual page break. In the actual workbook, fill each page appropriately; the two-problem illustration above is a syntax example, not a required density.

Use Pandoc math such as `$3 \times 4$` and `$\frac{2}{3}$` for typeset equations. Do not put equations inside code spans. The `\workarea{height}` command creates a light, printable blank work box. Add appropriate ruled lines, grids, number lines, or diagrams when the task needs them; keep them within the relevant problem block. Avoid large minipages: a whole problem must fit inside the printable page height.

The builder defaults to US Letter, 18 mm margins, 12 pt text, and TeX Gyre Heros fonts loaded by filename for compatibility with older TeX bundles. Use `--font-size 14pt` for larger text and `--paper a4` when appropriate. It suppresses cover and contents pages. Use short running headers; place longer topic descriptions in page content. Reserve most of each practice page for student work.

## Build

Resolve `<skill-dir>` to this installed skill's directory. Required tools are Pandoc, Tectonic/XeLaTeX/LuaLaTeX, and Poppler's `pdfinfo` and `pdftoppm`. The template and its license are bundled under `assets/eisvogel/`; there is no dependency on another personal skill. Use locally available executables or the Codex workspace runtime. Executable paths may be passed to the builder when they are not on `PATH`.

```bash
python3 <skill-dir>/scripts/build_pdf.py <output-dir>/addition-grade-3-practice.md \
  --output <output-dir>/addition-grade-3-practice.pdf \
  --expected-pages 20
```

The builder requires 20 `.practice-page` blocks when `--expected-pages 20` is used, then checks the actual PDF page count using `pdfinfo`. It builds in a temporary directory and publishes only a PDF whose count passes. It refuses to overwrite an existing output unless `--replace` is specified for an intended update. It does not assess educational completeness, answer correctness, or visual usability.

For an optional concept-guide or answer-key PDF, run the builder without `--expected-pages`; those documents are not restricted to 20 pages. Do not wrap an ordinary guide in `.practice-page` blocks.

If a required tool is missing, locate an existing installation or arrange an authorized installation. Preserve the source if the environment cannot build it. Do not replace Pandoc/Eisvogel with ReportLab, browser printing, or another template.

## Inspect and repair

1. Render **every final student page** using `pdftoppm -r 100 -png <workbook.pdf> <qa-dir>/page`. Inspect all pages, using contact sheets for an initial overview and full-page images to check details. Inspect any additional PDFs as well.
2. Check page numbering, headers, legible equations, complete diagrams, and the absence of clipped or overlapping text. Make sure every page has student problems and realistic writing space, with no answers exposed. Watch for long prompts, broken fractions, tiny text, and content escaping work boxes or margins.
3. Confirm the actual student PDF has exactly 20 pages. If it overflows, shorten instructions, rebalance problems, or change page allocation; preserve appropriate font sizes and writing space. Do not trim content blindly or append empty pages to satisfy the count.
4. Recheck problem IDs, grade scope, duplicate problems, calculations, and the separate key. Rebuild and re-inspect after changes. Deliver the PDF, editable source, and answer key only after these checks pass.
