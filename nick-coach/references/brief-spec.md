# Requirements Brief Specification

Read this reference only when the interview is complete enough to draft the saved artifact.

## Common structure

Use Markdown with concise sections. Include only sections that carry information.

1. **Title and status** — topic, date, `Draft` or `Ready`, and recommended deliverable type: `Plan/PRD`, `Skill`, or `Hybrid`.
2. **Intent** — the change Nick wants and why it matters.
3. **Context and evidence** — relevant source material, research findings, and links. Separate sourced facts from interpretation.
4. **Nick's priorities** — goals, preferences, working style, constraints, guardrails, and explicit non-goals.
5. **Opportunity scan** — useful patterns from the field, overlooked possibilities, and the ideas Nick accepted, rejected, or deferred.
6. **Decisions and rationale** — the important choices made during coaching and why.
7. **Requirements** — use `Must`, `Should`, `Could`, and `Won't` only when prioritization helps; otherwise use a short numbered list.
8. **Success evidence** — observable acceptance criteria or signals that the result is working.
9. **Risks, assumptions, and open questions** — include only consequential items and name the owner or next decision when known.
10. **Recommended next step** — the smallest sensible move after approval.

## If the recommendation is a plan or PRD

Add the relevant project shape: users or stakeholders, scope, major workstreams or phases, dependencies, decision points, and acceptance criteria. Do not invent dates, budgets, or owners. Use milestones only when they make the work easier to sequence or verify.

## If the recommendation is a skill

Add a proposed skill contract:

- working name and invocation examples;
- triggering requests and important exclusions;
- inputs and where they may come from;
- expected outputs and storage behavior;
- adaptive workflow and stopping condition;
- user interaction style;
- tools, references, scripts, or assets that would add concrete value;
- safety and authorization boundaries;
- realistic behavioral tests and success criteria.

Describe behavior and judgment, not merely a long prompt. Leave implementation choices open unless they are part of Nick's requirement.

## If the recommendation is hybrid

Separate the immediate project requirements from the reusable skill contract. Identify which knowledge belongs in the skill and which facts belong in project-specific input so the skill does not hard-code a single case.

## Quality check

Before saving, verify that:

- every important requirement traces to Nick's statement, evidence, or an explicitly labeled recommendation;
- unresolved assumptions are visible rather than silently decided;
- accepted and rejected possibilities are distinguishable;
- the artifact can guide a later planning or skill-creation session without replaying the interview;
- the document is short enough to scan and contains no generic filler.
