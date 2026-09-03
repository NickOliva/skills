---
skill_name: build-employment-opportunity-dossier
installation_scope: machine
installation_target: ~/.codex/skills/build-employment-opportunity-dossier
installation_method: symlink
---

# Employment Opportunity Dossier Requirements

## Purpose

Turn a job link, recruiter message, pasted listing, or company-and-role lead into an interview-ready, evidence-backed Obsidian dossier with editable Markdown and polished PDFs.

## Requirements

1. Research the role, company, business model, ownership, growth, locations, relevant people, reputation, litigation or regulatory risk, and candidate fit.
2. Prefer first-party and authoritative sources. Label claims as verified, inferred, or unverified, and preserve conflicts instead of silently resolving them.
3. Establish candidate fit only from supplied or current professional materials; never infer experience from the job description or reproduce personal contact details.
4. Create ten predictable documents: executive brief, position, company, locations, people, interview preparation, business model/growth/ownership, reputation/litigation/career risks, candidate suitability, and sources.
5. For public companies, include dated, split-aware stock history without investment advice. For private companies, explicitly state that no public trading history exists and analyze verified ownership instead.
6. Treat employee reviews as self-selected evidence and distinguish allegations, proceedings, findings, settlements, dismissals, and company responses.
7. Store outputs under `/Users/nick/Vaults/Work/Employment Opportunities/<Company> - <Opportunity Title>` unless the user specifies another destination.
8. Preserve user-authored files when refreshing an existing dossier.
9. Generate matching PDFs with the bundled Pandoc/Eisvogel workflow and retain Markdown sources.
10. Render and inspect every PDF page; correct clipping, bad glyphs, broken links, unsupported claims, placeholders, and weak page breaks before delivery.

## Boundaries

- Do not submit applications, sign in, contact recruiters or employees, or transmit user information.
- Do not invent reporting lines, office locations, role scope, candidate history, valuations, or legal conclusions.
- Summarize copyrighted sources and link to them rather than reproducing them at length.

## Success evidence

- All ten Markdown files and ten readable PDFs exist.
- Material facts have nearby citations and the source ledger records access dates and conflicts.
- Reporting line, location, compensation, ownership, candidate-fit gaps, and material career risks are explicit.
- The executive brief and interview preparation are concise enough to use during an interview.
