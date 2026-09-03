---
name: nick-museums
description: Research and plan museum visits for Nick, maintain his forward exhibition calendar, assess exceptional worldwide art opportunities, estimate longer-trip costs, and produce sourced Markdown and Pandoc/Eisvogel PDFs. Use for museum recommendations, exhibition discovery, museum trip planning, museum-calendar updates, or art-travel cost questions; do not use for commercial gallery searches or automatic purchasing, booking, or calendar changes.
---

# Nick Museums

Turn Nick's available time or museum interest into a short, verified, taste-aware decision document. The skill also supports a comprehensive weekly exhibition-calendar scan and exceptional worldwide opportunity monitoring.

## Required context

Read [references/museum-profile.md](references/museum-profile.md) completely before researching or producing an output. It contains Nick's art profile, travel context, ranking thresholds, and baseline museum registry. Then read `references/private.local.md` when present for more precise private travel context.

The optional local profile may contain a private street address. Use it only for local routing calculations. Never reproduce it in a report, citation, browser form, third-party request, or conversation; identify the origin publicly as `Mamaroneck, NY`. Prefer city-, station-, or ZIP-level routing unless Nick explicitly authorizes the street address for a specific transaction. If the local profile is absent, use `Mamaroneck, NY` as the origin.

## Choose the workflow

### On-demand visit or venue plan

Use when Nick supplies a date/window, asks what is worth seeing, names an institution or exhibition, or asks for a practical visit plan.

1. Resolve the real calendar date and timezone. Ask at most one question only if a missing time, transport, companion, or overnight constraint would materially change feasibility or cost.
2. Search the full relevant registry plus plausible newly opened or exceptional venues. For a named museum, still evaluate its current exhibitions and relevant permanent works rather than treating the institution as uniformly suitable.
3. Verify consequential facts from first-party pages: dates, hours and closures, member or timed-entry rules, ticket status, last admission, current gallery location, and object-level on-view status. Ownership does not establish display.
4. Rank by Nick's preference fit, artistic importance or rarity, availability, travel burden, usable gallery time, cost when material, and confidence. Give a decisive top three and no more than three backups when choosing among venues. For a single venue, produce a prioritized route and clearly distinguish confirmed highlights from contingencies.
5. Include enough logistics to leave home: public address, realistic travel range, parking or transit guidance, admission/reservation details, suggested duration, and official links. Label estimates and unresolved facts.
6. Produce both Markdown and PDF under `~/Vaults/Knowledge/Art/Museum Briefings/<YYYY>/`, using `YYYY-MM-DD-<short-slug>-museum-options.md` and the matching `.pdf`. Use [scripts/build_report.py](scripts/build_report.py) for the PDF.
7. Stop when Nick can decide or make the visit. After he chooses, offer a proposed calendar event; do not create or change it without explicit approval of that event.

### Weekly exhibition calendar

Use for the separate scheduled Sunday task or when Nick asks to refresh the forward calendar.

1. Load the prior digest and state from `~/Vaults/Knowledge/Art/Museum Briefings/state/` when present. Preserve first-seen dates and prior details so unchanged entries are not labeled new.
2. Audit every registry institution in the museum profile and discover material openings, closures, relocations, or newly relevant institutions.
3. Separately search worldwide for the high-priority artists, works, schools, canonical Chinese handscrolls, and photography interests specified in the museum profile. Apply the higher worldwide threshold and distinguish awareness from a travel recommendation.
4. Include every announced future regional match without an arbitrary end horizon. Organize by month and opening date; mark new, changed, opening soon, and closing soon. Add `Worldwide highlights` and `Closing soon and reasonably accessible` exactly as required.
5. Include a compact source-audit appendix naming every institution checked, failures, and material uncertainties. Completeness means an auditable sweep, not an unsupported claim.
6. Write `YYYY-MM-DD-museum-calendar.md` and its PDF under the year folder. Update durable state only after the report is successfully written and verified.

### Cost or calendar follow-up

For an overnight, rail, or fly-worthy option, provide a timestamped all-in range with visible assumptions and compare sensible modes when cost could change the decision. Expedia is optional, not required. Do not sign in, transmit personal data, hold inventory, or enter a booking flow without separate authorization.

Calendar free/busy reading requires Nick's authorization. Event creation or modification requires explicit approval of the exact proposed event, including any travel blocks. Never create speculative holds from the Sunday digest.

## Research and writing standard

- Browse every time; hours, display status, schedules, tickets, prices, parking, and construction are volatile.
- Prefer official museum exhibition, collection, visit, and ticket pages. Use reputable secondary sources to discover leads or add context, not as the sole support for consequential facts when first-party evidence exists.
- Cite every recommended exhibition and consequential logistical fact near the claim. State when a fragile or rotating object's on-view status cannot be confirmed.
- Optimize for the art, not the institution's label. Exclude commercial galleries by default, reject AI-generated imagery, and apply the taste priorities in the museum profile.
- Lead with the recommendation. Keep the decision section phone-friendly; put detailed research and the source audit in an appendix.

## PDF production and verification

Run:

```bash
python3 scripts/build_report.py /absolute/path/to/report.md
```

The builder requires Pandoc, an available TeX engine, and the vendored Eisvogel template. Render the result with `pdftoppm`, inspect every page, and verify legibility, working hierarchy, page numbers, sources, and absence of the private street address before delivery. Do not substitute a different PDF generator for the required Pandoc/Eisvogel pipeline.

## Authorization boundaries

Research and report generation are read-only. Never buy tickets; book travel, lodging, or parking; join a membership; contact an institution; publish or share a report; sign in to a travel provider; or create, edit, or delete calendar events without separate explicit authorization.
