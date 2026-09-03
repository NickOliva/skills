---
skill_name: nick-coach
installation_scope: machine
installation_target: ~/.codex/skills/nick-coach
installation_method: symlink
---

# Nick Coach Requirements

## Purpose

Turn an initial idea into a concise, decision-ready requirements brief through targeted research and a short adaptive coaching interview. When the user explicitly asks to proceed, create the resulting skill package from the approved requirements.

## Requirements

1. Start from the user’s prompt and referenced materials; do not ask the user to repeat available information.
2. Research current practices or examples before interviewing when they could materially improve the questions or recommendation.
3. Ask only high-leverage questions whose answers could change the outcome. Ask no more than three at once and normally finish within one or two rounds.
4. Challenge consequential assumptions and surface tensions, underexplored options, and one or two useful ideas outside the obvious framing.
5. Prefer a concrete recommendation over an undifferentiated menu while allowing conversational and partial answers.
6. Distinguish a plan/PRD, reusable skill, or hybrid deliverable and explain the recommendation.
7. Clearly separate user statements, sourced evidence, recommendations, and assumptions.
8. Save a concise Markdown brief containing only useful sections: intent, context, priorities, opportunity scan, decisions, requirements, success evidence, risks or open questions, and next step.
9. For skill briefs, include triggers, exclusions, inputs, outputs, workflow, stopping condition, interaction style, resources, authorization boundaries, and behavioral tests.
10. Honor a requested destination; otherwise save under `<workspace-root>/coach-briefs/<YYYY-MM-DD>-<slug>-requirements.md`.

## Skill package structure

When creating a skill from approved requirements:

1. Identify its project or owner scope, such as `nx`, `zfs`, or `nick`, and name the package `<scope>-<skill-name>`.
2. In a repository dedicated entirely to skills, create the package at `<repo-root>/<scope>-<skill-name>/`. In any other repository, create it at `<repo-root>/skills/<scope>-<skill-name>/`.
3. The package root must contain the requirements document and a literal `skill/` directory:
   - `<scope>-<skill-name>-requirements.md`
   - `skill/`
4. Keep only deployable skill contents in `skill/`: `SKILL.md` and any needed `agents/`, `scripts/`, `references/`, or `assets/`. The requirements document must remain outside it.
5. Give every skill requirements document installation frontmatter using this schema:

   ```yaml
   ---
   skill_name: <scope>-<skill-name>
   installation_scope: machine | repo
   installation_target: <target-path>
   installation_method: symlink
   ---
   ```

6. For repo scope, install at `<repo-root>/.agents/skills/<scope>-<skill-name>`. For machine scope, install at `~/.codex/skills/<scope>-<skill-name>`.
7. A symlink installation must target the package's nested `skill/` directory, never the package root.
8. Validate the deployable skill and verify that the installed symlink resolves to the intended `skill/` directory.

## Boundaries

- The default output is the requirements brief. Create the skill only when the user explicitly asks to proceed with implementation.
- Research and inspection do not authorize publishing, purchasing, applying, messaging, account changes, or other consequential external actions.
- Do not invent preferences, deadlines, budgets, owners, or requirements.

## Success evidence

- Every material requirement traces to the user, evidence, or a labeled recommendation.
- Accepted, rejected, and unresolved ideas remain distinguishable.
- The brief can guide planning or skill creation without replaying the interview.
- The saved artifact is concise enough to scan and contains no generic filler.
- A created skill uses the correct repository root, keeps requirements outside the deployable `skill/` directory, and is installed at the scope declared in its frontmatter.
