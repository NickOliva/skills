---
skill_name: nick-mac
installation_scope: machine
installation_target: ~/.codex/skills/nick-mac
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
3. For every differing item, show the recorded value and the target's value. Ask Nick whether to keep the recorded standard, adopt the target's alternative as the standard, or define a new value. This applies to every kind of item, including application versions, installation choices, shortcuts, appearance, and device-dependent settings.
4. Present one combined, reviewable plan containing those choices, any proposed standard changes, target changes, installations, dependencies, and unresolved items. Let Nick answer in batches, defer items, or select a subset. Resolve his choices before final plan acceptance; do not ask again for decisions already made.
5. Apply only the accepted plan. Acceptance covers the stated repository-standard updates and target changes, without another prompt for every component. If new evidence materially changes the plan, bring back only that change. Inspection-only and skill-editing requests do not authorize configuring the Mac.
6. Update the manifest, affected standard artifacts, and concise decision record together when Nick adopts a new standard. Preserve unresolved and provisional items for the next review. Never silently promote a snapshot, copy another computer wholesale, or mark the complete formula finalized without Nick saying so.
7. Verify the actual outcome of accepted changes, skip unnecessary rewrites, and preserve unrelated configuration. Report aligned, changed and verified, deferred, blocked, or requiring a manual check. A helper's successful exit alone does not prove the UI works.
8. Keep device names, hardware identifiers, credentials, recordings, transcript history, and personal shell secrets out of portable standard artifacts. Capture configuration intent and resolve hardware-specific equivalents in the plan. Preserve history-retention settings separately from history content.

## Initial baseline and component organization

- **Finder and Terminal:** capture the current configuration as provisional review material. Reconsider all inherited settings; old hard-coded helpers must not enforce them. Actual Terminal profile identifiers are configuration data, not computer identities.
- **Voice transcription:** Nick chose the currently installed and configured FluidVoice setup as the initial standard. Capture portable preference overrides, effective defaults, selected models, dictionary/vocabulary, version, and relevant app controls. Later differences still go through the same keep/adopt/new decision process.
- **Additional tools, apps, and configurations:** add named manifest items and component specifications as they are reviewed. Do not limit the skill to its initial components or imply that every installed application is already part of the standard.
- Keep the main skill focused on the shared review loop. Component references hold desired state, inspection, application, verification, dependencies, and limitations. Use scripts or assets where useful; an application UI procedure is also a valid implementation.

## Repository and review

Maintain requirements outside `nick-mac/skill/`. Bundle reusable scripts, assets, and tests inside that directory so the installed skill is self-contained. Tests use synthetic settings and must not depend on a particular computer or the current chosen baseline. Preserve the installed symlink and the existing explicit-invocation policy. Standard edits update the installed skill files immediately; accepted alignment runs apply configurations to computers. Leave this revision local and uncommitted for Nick's inspection.

## Success evidence

- Reviewing a different computer exposes both alternatives for every differing manifest item and allows a new value or deferral.
- Adopting a target setting updates the repository standard only as part of an accepted plan; keeping the standard updates the target only as accepted.
- Matching items need no change. Partial reviews remain useful, and unresolved choices carry into subsequent reviews.
- FluidVoice's portable configuration is captured without copying history or device identity; app permissions, login registration, model readiness, and dictation behavior are checked separately.
- A new component uses the same review process, and finalizing the complete formula requires Nick's explicit decision.
