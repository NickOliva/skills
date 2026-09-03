# Employment Opportunity Dossier Specification

Use this structure for ordinary employment leads. Adapt section depth to available evidence, but create all ten documents so folders remain predictable.

## Required files

### `00 Executive Brief.md`

- One-page decision and interview brief
- Opportunity snapshot: public title, internal title if different, company, requisition, work model, compensation, status, and source links
- Why the role exists now, clearly separating evidence from inference
- Five highest-value interview themes
- Top verified people and likely interfaces
- Material inconsistencies, risks, and open questions
- Links to the other dossier files

### `01 Position.md`

- Canonical listing facts and verbatim-short title/compensation details where useful
- Responsibilities grouped into operating themes
- Required qualifications and success profile
- First 30/60/90-day hypothesis, labeled as an interview hypothesis
- Role scorecard: outcomes, measures, dependencies, and failure modes
- Listing discrepancies and questions they create

### `02 Company.md`

- Business model, products/services, scale, customers, geography, ownership when verified, and headquarters
- Strategy and growth model, especially acquisitions or transformation relevant to the opportunity
- Recent leadership or financial developments that change the role's context
- Culture claims: distinguish company statements from outside observations
- What the facts imply for this role, labeled as analysis

### `03 Locations.md`

- Work model and any required or preferred geography
- Headquarters address and evidence
- Offices named by the posting or otherwise relevant to likely collaboration or travel
- Do not dump the full office directory. Explain why each included location matters.
- If the candidate's likely office is unknown, say so and provide the best interview question.

### `04 People.md`

Create concise profiles for the verified reporting leader, likely reporting leader, and likely interfaces. For each person include:

- Current name and title with source and confidence
- Why the person matters to the opportunity
- Relevant background only
- Official profile and public professional-profile link when found
- Likely interview focus, explicitly labeled as analysis

Organize people as `Verified reporting line`, `Likely reporting line`, `Likely interfaces`, and `Context only`. Never put someone in the first category without direct evidence.

### `05 Interview Preparation.md`

- Interview thesis: three to five concise points
- Questions to ask the recruiter, hiring manager, peers, and executives
- Include an explicit team-composition question whenever direct reports are not verified: number of direct and indirect reports; titles and levels; locations; filled versus vacant roles; employees versus contractors or vendors; functional responsibilities inside and outside the team; planned hires; and the candidate's hiring, budget, and reorganization authority
- Questions the candidate is likely to receive and what a strong answer must demonstrate
- Evidence-based stories the candidate should prepare, expressed as prompts when the candidate's history is not available
- Technical topics and operating mechanisms to refresh
- Red flags and title/scope/authority questions
- A compact day-of interview cheat sheet

### `06 Business Model, Growth & Ownership.md`

Make this a standalone analysis rather than a duplicate of the general company profile.

- Explain how the company makes money: customers, products or services, revenue streams, pricing or commission mechanics, recurrence, distribution, important suppliers or partners, and major cost or operating drivers
- Describe the industry's value chain and where the company sits in it
- Trace founding, mergers, acquisitions, geographic or product expansion, and dated revenue, headcount, customer, location, or transaction milestones when evidence permits
- Separate organic growth, acquisition growth, and company marketing claims; identify integration dependence and risks relevant to the opportunity
- State whether the company is publicly traded, privately held, nonprofit, government-owned, or otherwise structured, with dated ownership evidence
- For a public company: identify exchange and ticker; include a dated, split-aware stock-price history with source, period, endpoints, material drawdowns or inflections, and relevant corporate events. Label market interpretation as analysis and avoid investment advice.
- For a private company: state plainly that it has no public stock price or trading history. Trace verified founders, parent companies, private-equity sponsors, recapitalizations, or ownership changes instead; do not invent valuation or returns.
- End with implications for the role and interview questions created by the business and ownership model

### `07 Reputation, Litigation & Career Risks.md`

Treat this as employer diligence, not an accusation ledger.

- Summarize public employee feedback across available platforms. Record platform, access date, visible rating and sample size when available, and recurring positive and negative themes. Explain self-selection, recency, location, and role-mix limitations.
- Search for material litigation, regulatory actions, government investigations, settlements, dismissals, sanctions, data or security incidents, layoffs, labor disputes, customer or partner controversies, financial distress, and ownership-related concerns
- Prioritize matters relevant to the candidate's likely function, leadership team, work location, or career risk; avoid dumping immaterial local disputes
- For each matter, record date, jurisdiction or authority, parties, case or release identifier when found, allegation or issue, procedural status, outcome, company response, and why it matters. Clearly distinguish allegations from findings.
- Include counterevidence, improvements, awards, strong retention signals, or favorable employee themes when supported
- Use a compact risk matrix with evidence strength, recency, severity, and interview relevance
- End with balanced conclusions, open questions, and specific interview questions that could confirm or disconfirm the risks

### `08 Candidate Suitability.md`

Make this a candid, evidence-backed assessment of the opportunity for the candidate, not generic encouragement.

- Identify the candidate materials used and their dates or versions. Prefer the most recent non-archived resume and any opportunity-specific materials supplied by the user. Omit personal contact information.
- State an overall fit conclusion in plain language, with the conditions or evidence gaps that could materially change it. Avoid false precision; use a numeric score only when the user asks for one.
- Map the role's highest-value requirements to documented candidate evidence. Separate direct matches, adjacent or transferable experience, missing evidence, and genuine mismatches.
- Identify differentiators the candidate can credibly use, including combinations of domain, operating, technical, financial, leadership, or transformation experience.
- Analyze likely rejection or failure points at both stages: interview/selection risk and on-the-job risk. Distinguish a skill gap from a positioning problem, unclear resume evidence, or an employer-side scope problem.
- Include a compact fit matrix with requirement, candidate evidence, alignment strength, risk, and the proof point or interview story to use.
- Recommend truthful positioning for gaps. Never suggest claiming experience the candidate has not documented.
- End with a pursue/continue/withdraw recommendation, conditions for success, questions that could change the assessment, and the three to five stories the candidate should prioritize.
- If reliable candidate material is unavailable, replace the conclusion with a clearly labeled provisional assessment and self-assessment questions.

### `99 Sources.md`

- Source ledger with title, publisher, URL, access date, source type, and what it supports
- Note source conflicts, blocked pages, snippet-only evidence, and stale material
- Separate primary and secondary sources
- Separate employee-feedback, court/regulatory, market-data, and ownership sources when used
- Include a distinct candidate-evidence section naming the resume or other professional materials used for the suitability analysis
- Do not include private contact information or people-search data

## Markdown and PDF conventions

Every Markdown file begins with YAML like:

```yaml
---
title: "Alera Group - VP, Finance Operations"
subtitle: "Executive Brief"
author: "Opportunity Dossier"
date: "2026-08-27"
subject: "Employment opportunity research"
keywords: [employment, interview, Alera Group]
lang: "en-US"
titlepage: true
titlepage-color: "17324D"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "46A5A5"
toc: true
toc-own-page: true
colorlinks: true
linkcolor: "NavyBlue"
urlcolor: "TealBlue"
generated_by: "build-employment-opportunity-dossier"
---
```

Set `toc: false` for a genuinely one-page executive brief. Use plain ASCII hyphens in prose. Prefer short paragraphs and compact tables. Avoid wide tables; convert them to bullets when a table would exceed page width. Use `\newpage` only for deliberate section breaks.

Use descriptive Markdown links and footnotes. A material fact should be traceable without requiring the source ledger, while `99 Sources.md` remains the complete audit trail. Preserve uncertainty with labels such as `Verified`, `Strong inference`, `Tentative`, and `Unknown`.

## Research quality bar

- Confirm current titles on first-party leadership pages or dated announcements when possible.
- Compare multiple job copies for discrepancies, but treat the employer's live posting as canonical unless there is strong evidence otherwise.
- For people, avoid personal addresses, personal phone numbers, private emails, family details, or unrelated biography.
- For locations, cite an official office page or the company's own footer/contact material.
- Recent means relevant to the role and normally within 24 months; older history belongs only when it explains the business model or leadership background.
- Put the retrieval date on every web source because job postings and profiles change.
- Prefer SEC filings, exchange or issuer investor relations, state and federal regulators, court dockets or published opinions, and dated company announcements for ownership, financial, litigation, and regulatory claims.
- For employee feedback, report themes conservatively. A review site's aggregate score is a platform-specific signal, not a measured fact about the entire workforce.
- Search by company legal name, major former names, parent or sponsor, and material subsidiaries. Do not attribute a subsidiary's matter to the whole enterprise without explaining the relationship.

## Completion checks

- Ten Markdown files and ten matching PDFs exist.
- The folder name includes company and title.
- Every PDF opens, has at least one page, and visually renders cleanly.
- No `TODO`, placeholder, internal tool identifier, or unsupported claim remains.
- The executive brief discloses title, reporting-line, location, and compensation uncertainty.
- All people links resolve to the intended person or are explicitly labeled as search-result-only.
- Ownership/public status is explicit; stock history is present for public companies or explicitly inapplicable for private companies.
- Employee feedback is sampled transparently, and litigation/regulatory claims state procedural status and distinguish allegations from findings.
- Candidate suitability distinguishes direct evidence, transferable experience, missing evidence, and genuine mismatch, with no invented biography or reproduced contact details.
- Interview preparation explicitly tests team composition, staffing status, functional boundaries, and hiring or budget authority when public sources do not identify the direct-report organization.
