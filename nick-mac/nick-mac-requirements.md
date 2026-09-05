---
skill_name: nick-mac
installation_scope: repo
installation_target: .agents/skills/nick-mac
installation_method: symlink
---

# Nick Mac Requirements

Status: Draft for local review. Updated 2026-09-05. Deliverable: Skill.

## Intent

Develop and apply Nick's standard Mac build through repeated reviews across his computers. The formula evolves item by item until Nick decides it is complete. Finder, Terminal, voice transcription, and other tools, apps, and configurations are components of this build.

No computer is permanently authoritative. The recorded standard starts from observed settings and Nick's choices, then evolves through explicit decisions during later reviews. Skill text must not identify computers by name.

## Review and alignment

1. Maintain a manifest of tools, apps, and configuration items, grouped into components. Give each item a stable identity, recorded value or artifact, review state, and a way to inspect, apply, and verify it. Keep provisional observations distinct from decisions Nick has accepted.
2. Identify the target Mac and compare its actual state with the manifest. A review may cover the whole build or named components. Missing or additional tools and configuration items can become review candidates; their presence alone does not make them standard.
3. For every differing item, show the recorded value and the target's value. Ask Nick whether to keep the recorded standard, adopt the target's alternative as the standard, or define a new value. This applies to every kind of item, including tool identity, installation choices, shortcuts, appearance, and device-dependent settings.
4. Present one combined, reviewable plan containing those choices, any proposed standard changes, target changes, installations, dependencies, and unresolved items. Let Nick answer in batches, defer items, or select a subset. Resolve his choices before final plan acceptance; do not ask again for decisions already made.
5. Apply only the accepted plan. Acceptance covers the stated repository-standard updates and target changes, without another prompt for every component. If new evidence materially changes the plan, bring back only that change. Inspection-only and skill-editing requests do not authorize configuring the Mac.
6. Update the manifest, affected standard artifacts, and concise decision record together when Nick adopts a new standard. Preserve unresolved and provisional items for the next review. Never silently promote a snapshot, copy another computer wholesale, or mark the complete formula finalized without Nick saying so.
7. After every alignment, require a full independent review by a separate sub-agent that made none of the changes. It must inspect actual target state against the complete manifest, accepted plan, exceptions, and original evidence, including functional checks and unintended changes. The implementing agent fixes findings within the accepted scope; the reviewer rechecks them. Record evidence and pass/fail/unverified results in the same report. Self-review or helper exit codes cannot substitute. Do not declare alignment complete with an incomplete independent review.
8. Track tool identity and configuration, not software versions. Do not collect or display installed version numbers, compare or pin releases, or propose upgrades/downgrades. Applications may update independently. Compare effective configuration behavior rather than assuming an unset preference always means the same behavior.
9. Keep device names, hardware identifiers, credentials, recordings, transcript history, and personal shell secrets out of portable standard artifacts. Capture configuration intent and resolve hardware-specific equivalents in the plan. Preserve history-retention settings separately from history content.

10. Review Login Items and background tasks on every full run. Attribute each task by its label, executable, parent application, and current installation; duplicate names and missing icons alone are not faults. Revisit accepted cleanup and retention choices on each target, including telemetry opt-out persistence, without assuming identical paths or user IDs.

11. Check every skill in the Nick Skills repository against its requirements declaration: required installation, machine or repository scope, target path, symlink method, and current repository source. Include missing, broken, duplicate, wrong-scope, stale-copy, and undeclared installations in the combined review plan. Requirements-only skills without a built SKILL.md are pending implementation, not ready to install. Discover newly added skills on every run.

## Initial baseline and component organization

- **Finder and Terminal:** capture the current configuration as provisional review material. Reconsider all inherited settings; old hard-coded helpers must not enforce them. Actual Terminal profile identifiers are configuration data, not computer identities.
- **Voice transcription:** Nick chose the currently installed and configured FluidVoice setup as the initial standard. Capture portable preference overrides, effective defaults, selected models, dictionary/vocabulary, and relevant app controls. Later differences still go through the same keep/adopt/new decision process.
- **FluidVoice reporting:** no reporting ever, including weekly/daily activity, detailed analytics, telemetry, and automatic diagnostic uploads from the app or its helpers. Establish effective prevention before first launch and verify scheduling, retries, relaunch/login, and runtime behavior independently. A detailed-analytics toggle is insufficient. If prevention cannot be established and verified, keep FluidVoice inactive and mark it blocked; do not offer residual reporting as an alternative. Local-only history and debug logs remain separate.
- **Optional peripherals:** Elgato Stream Deck and its Corsair helper are optional, on computers Nick explicitly selects. Connecting to a desktop monitor does not make them required. Keep selections in run history, with no computer-name lists in the portable skill or standard. Retention does not authorize enabling background activity.
- **Required applications:** include every application in the reviewed candidate table except Keynote, Numbers, Slack, and OneDrive. Application identity/presence is accepted; each additional application's configuration remains to be reviewed. The application manifest records the exact list.
- **Not required:** Keynote, Numbers, Slack, and OneDrive. Their presence is allowed; exclusion alone does not authorize uninstalling them. Nick separately authorized uninstalling OneDrive from the current target Mac.
- **Additional tools and configurations:** add named manifest items as they are reviewed. The separate command-line-tool inventory remains candidates; this application selection does not adopt it automatically.
- Keep the main skill focused on the shared review loop. Component references hold desired state, inspection, application, verification, dependencies, and limitations. Use scripts or assets where useful; an application UI procedure is also a valid implementation.

## Repository and review

Store run history in one Git-visible file at `nick-mac/reports/YYYY-MM-DD/YYYY-MM-DD-<computer-name>-alignment.md`, outside `skill/`. Use the inspected computer's actual name in the report filename; do not create a separate computer subfolder. Computer names may appear in run history but not in portable standards or skill instructions. Preserve prior runs, with a distinct run suffix if another inspection occurs on the same date.

Combine comparison, recommendation, and decision in a compact Markdown table for preview mode: Ref, Item, Baseline, This Mac, Recommendation, and Decision columns, one row per item in comparison order. Preserve selected decisions and write `Pending` in unanswered Decision cells so the preview retains all six columns in every row. Save conversational decisions immediately in this file; do not maintain a separate decision file. Pending or blank means no change. Neither a recommendation nor the baseline is authorization; require an explicit decision covering the item or a specifically identified group. Distinguish recorded decisions from applied changes.

Describe visible behavior or capability and the practical effect of each recommendation in plain language. Do not present an incomplete baseline observation as a specified alternative. Preserve detailed findings and verification in the same file, collapsed when lengthy; omit repeated decision summaries and instructions. Do not use `.local.md` names. Storing a report does not itself request committing or pushing it.

Maintain requirements outside `nick-mac/skill/`. Bundle reusable scripts, assets, and tests inside that directory so the installed skill is self-contained. Tests use synthetic settings and must not depend on a particular computer or the current chosen baseline. Install Nick Mac only through `.agents/skills/nick-mac -> ../../nick-mac/skill` in this repository, with no machine-wide Nick Mac discovery copy. Preserve the existing explicit-invocation policy. Check other Nick skills against their own declared scopes, not Nick Mac’s scope. Standard edits update the installed skill files immediately; accepted alignment runs apply configurations to computers. Leave this revision local and uncommitted for Nick's inspection.

## Success evidence

- Reviewing a different computer exposes both alternatives for every differing manifest item and allows a new value or deferral.
- Adopting a target setting updates the repository standard only as part of an accepted plan; keeping the standard updates the target only as accepted.
- An application update alone never produces a difference, a version report, or an alignment action. Required app presence and effective configuration are checked separately.
- Matching items need no change. Partial reviews remain useful, and unresolved choices carry into subsequent reviews.
- FluidVoice's portable configuration is captured without copying history or device identity; app permissions, login registration, model readiness, and dictation behavior are checked separately.
- FluidVoice cannot be marked aligned without verified zero reporting, including scheduled weekly activity.
- Every alignment receives a full review by a non-implementing sub-agent; unresolved findings remain explicit until independently rechecked.
- Optional Elgato/Corsair presence is allowed, and absence is not a missing requirement unless Nick selected it for that target.
- A new component uses the same review process, and finalizing the complete formula requires Nick's explicit decision.
