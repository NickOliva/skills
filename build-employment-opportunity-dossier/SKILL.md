---
name: build-employment-opportunity-dossier
description: Research an employment opportunity from job links, recruiter messages, pasted text, or a company-and-role lead, then create a sourced Obsidian prospect folder with polished Pandoc/Eisvogel PDFs. Use for interview preparation, candidate-fit analysis, business-model and ownership analysis, employer-risk diligence, role analysis, stakeholder mapping, and opportunity-folder refreshes; do not use for submitting applications or contacting people.
---

# Build Employment Opportunity Dossier

Create an interview-ready, evidence-backed folder without inventing facts about the role, company, reporting line, offices, or people.

## Defaults

- Output root: `/Users/nick/Vaults/Work/Employment Opportunities`
- Folder name: `<Company> - <Opportunity Title>`, with filesystem-unsafe characters replaced
- Inputs may be one or more job URLs, pasted listing text, a recruiter message, or only a company and role. Treat all as employment leads; research missing context.
- Keep the Markdown originals beside the PDFs so the result remains editable and searchable in Obsidian.

Honor a different output path or folder name when the user supplies one. If a target folder already exists, inspect it first. Preserve user-authored notes and attachments; update generated files only when the user asked to refresh the dossier.

## Workflow

1. Read [references/dossier-spec.md](references/dossier-spec.md) before researching or authoring a dossier.
2. Establish the canonical company name, public opportunity title, internal title if different, source URLs, work model, and location. Surface conflicts rather than silently choosing one version.
3. Research current facts. Prefer the employer's posting, company pages, official leadership profiles, regulatory filings, court or agency records, investor materials, and first-party announcements. Use reputable secondary sources to test company claims, identify public feedback, and fill gaps. Establish the business model, growth history, ownership, public/private status, and material career risks rather than limiting research to the job description.
4. Establish the candidate evidence base before judging fit. Use candidate materials the user supplied and the most recent relevant, non-archived resume or career material in the work Vault when available. Do not infer experience from the opportunity itself. If candidate evidence is unavailable or materially incomplete, say so and create a role-relative self-assessment instead of inventing a biography.
5. Separate `Verified`, `Inferred`, and `Unverified` claims. Never state a reporting relationship as fact unless a source says so. A role's responsibilities may justify identifying *likely interfaces*, but label the reasoning.
6. Create the ten Markdown documents in the specification. Give every material claim a nearby human-readable link or footnote and include access dates in `99 Sources.md`. For public companies, include dated, split-aware stock-price history from a traceable market-data source. For private companies, explicitly document that no public ticker or stock-price history exists and analyze verified ownership or financial-sponsor history instead.
7. Build the PDFs with the vendored Eisvogel v3.5.1 template:

   ```bash
   python3 <skill-dir>/scripts/build_pdfs.py "<dossier-folder>"
   ```

   The script uses Pandoc, selects an installed system font to avoid optional Eisvogel font-package failures, and chooses an available TeX engine, preferring Tectonic. Do not substitute a different PDF renderer unless the user asks or the required toolchain is unavailable.
8. Validate content and rendering. Run `pdfinfo` on every PDF, render every page with `pdftoppm`, inspect the page images, and correct clipped text, broken links, overflow, blank pages, bad glyphs, or weak page breaks. Check that the ten PDFs exist and contain no TODO markers or tool tokens.
9. Report the folder path, the PDFs created, important uncertainties, and any missing evidence that the user should ask about in the interview.

## Boundaries

- Do not apply, sign in, message recruiters, contact employees, or transmit user information.
- Do not copy a full third-party article or profile into the dossier. Summarize and link.
- Do not infer a local office from the user's device location. For a remote role, identify the headquarters and only call another office "likely" when the listing or user context supports it.
- Treat stale search snippets as leads, not proof. Record source freshness and confidence.
- Employee-review sites are self-selected samples, not representative surveys. Record platform, access date, visible sample size and rating when available, distinguish repeated themes from isolated claims, and never identify nonpublic reviewers.
- Distinguish allegations, filed cases, rulings, settlements, dismissals, and regulatory findings. Do not imply guilt or company-wide practice from an unresolved claim. Include material counterevidence and the company's response when available.
- Do not present stock or ownership analysis as investment advice.
- Base candidate-fit conclusions on documented professional evidence. Distinguish direct matches, transferable experience, evidence gaps, and actual mismatches; do not turn an absent resume detail into a negative fact.
- Do not reproduce personal contact information or unrelated personal details from candidate materials in the dossier.
