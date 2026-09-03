---
skill_name: test-elementary-knowledge
installation_scope: machine
installation_target: ~/.codex/skills/test-elementary-knowledge
installation_method: symlink
---

# Elementary Knowledge Requirements

## Purpose

Create comprehensive elementary concept guides with solved examples or focused, printable, grade-specific practice workbooks.

## Concept-guide requirements

1. Default a broad subject request to concept-guide mode unless the user asks for practice.
2. Cover kindergarten through grade 5 when no grade is supplied, or the requested grade plus essential prerequisites when one is supplied.
3. Organize a complete prerequisite-ordered outline with stable IDs and distinct teachable concepts.
4. Provide exactly five varied, fully solved examples for every numbered concept or sub-concept.
5. Reconcile N outline items with N matching sections and 5N solved examples.
6. Check solutions, qualifications, units, and claimed curriculum alignment; cite authoritative sources when research is needed.

## Practice-workbook requirements

1. Require a specific concept and grade; ask for the grade when absent.
2. Create exactly twenty useful student-problem pages with deliberate progression, varied representations, grade-appropriate reading load, and adequate work space.
3. Do not count a cover, contents page, answer key, or blank padding among the twenty pages.
4. Keep each prompt and its work area together and include any passage, data, or diagram needed to solve it.
5. Solve every problem while authoring and create a separate Markdown answer key using matching page and problem IDs.
6. Build with the bundled Pandoc/Eisvogel workflow and retain editable Markdown.
7. Use the supplied builder to verify the actual PDF page count; source sections alone do not establish twenty pages.
8. Render and inspect every page for legibility, clipping, grade fit, usable work space, duplicate problems, exposed answers, and correct page mapping.

## Storage and boundaries

- Honor the requested destination; otherwise use `<workspace-root>/elementary-knowledge/`.
- Preserve unrelated files and avoid overwriting prior work unless an update is requested.
- Do not introduce advanced content merely to fill pages or reduce scope to satisfy an arbitrary response-length limit.
- If PDF tooling is unavailable, preserve the completed source and identify the PDF as incomplete.

## Success evidence

- Concept guides have complete outline/example reconciliation and correct solutions.
- Student workbooks contain exactly twenty substantive pages plus a separate complete answer key.
- Final PDFs are visually inspected, grade-appropriate, and free of clipping or layout defects.
