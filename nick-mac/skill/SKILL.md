---
name: nick-mac
description: Review and align Nick's Macs with an evolving standard build of tools, apps, and configurations. Compare every manifest item, help Nick keep the recorded value, adopt the target's alternative, or define a new standard, then apply one accepted alignment plan. Also use to extend or revise the build.
---

# Nick Mac

Develop Nick's standard Mac build through repeated reviews across his computers. The build evolves until Nick decides the complete formula is settled. Finder, Terminal, and voice transcription are initial components; tools, apps, and configurations can be added throughout the process.

## Standard and scope

Nick Mac is installed only in the Nick Skills repository at `.agents/skills/nick-mac`, linked to its source here. Do not install it globally.

Read [manifest.json](manifest.json) and the [component catalog](references/components.md). Load specifications and assets only for the selected components. Use paths relative to this skill directory, including when invoked through its installed symlink.

The manifest records the current baseline and item review states. A provisional snapshot is a starting point for review. No computer is permanently authoritative, and observing a setting does not adopt it as standard. Use “target Mac” and “recorded standard”; keep computer names out of skill instructions and portable artifacts.

A normal run reviews the whole manifest on the target Mac. Honor a named subset or inspection-only request. Target the local Mac unless Nick names another accessible target. Editing this skill does not itself authorize running its configuration procedures.

Elgato Stream Deck and its Corsair helper are optional. Nick selects the computers that use them; monitor connection alone does not make them required. Record target choices in run history, never a computer-name list in the portable skill or standard.

FluidVoice must send no reporting at all, including weekly activity, detailed analytics, and automatic diagnostic reports. A detailed-analytics switch alone is insufficient. Follow the [voice transcription procedure](references/components/voice-transcription.md) to prevent reporting before first launch and verify the result. Do not offer residual reporting as an acceptable substitute.

Software versions are out of scope: do not inventory, report, compare, pin, upgrade, or downgrade releases. Track tool identity, presence, and effective configuration. Independent application updates are allowed; updater settings remain ordinary configuration choices.

## Review, decide, apply

1. **Inspect.** Compare each selected manifest item with the target's actual configuration. Include app identity/presence, settings, assets, dependencies, Login Items/background tasks, Nick skill installation scopes, and verification gaps. On a full review, inventory installed user apps and tools as candidates for manifest additions; distinguish intentional tools from their supporting packages. Surface relevant app settings outside the captured baseline as review candidates. Use `scripts/compare-standard.py` for the supported preference comparisons and supplement it with each component's checks. An unset preference requires an effective-setting check; absence alone does not establish equivalent behavior.
2. **Resolve differences.** For every differing item, show the recorded and observed alternatives. Let Nick keep the recorded standard, adopt the target's value as standard, define a new value, or defer the item. Group related questions for concise answers, but preserve individual choices. Treat missing and additional tools the same way; do not silently install, remove, or adopt them.
3. **Present one plan.** Combine Nick's choices into a reviewable plan of proposed standard updates and target changes. Include unresolved items and any installation, replacement, restart, permission, or device-specific step that affects his decision. For an item he has not decided, show the alternatives in the plan rather than selecting one silently. He may resolve choices and accept the resulting plan in one reply.
4. **Wait for acceptance.** Do not change target configuration or adopt proposed standards before Nick accepts the plan. Earlier acceptance of the same concrete work still counts. An inspection-only request ends with findings. If nothing differs, report that without asking for an empty approval.
5. **Apply the accepted scope.** Update accepted standard artifacts, manifest review states, and [decision record](references/decisions.md) together, then align the target using the component procedures. Preserve unrelated configuration and back up replaced settings. Continue independent accepted work if an item is blocked. Bring back only material changes to the accepted plan.
6. **Verify independently and carry forward.** Perform implementation checks, then require a full [post-alignment review](references/post-alignment-review.md) by a separate sub-agent that made none of the changes. The implementing agent's own checks cannot substitute for that review. Resolve findings within the accepted scope and obtain independent re-verification before declaring alignment complete. Report deferred, blocked, and unverified items explicitly. Only Nick decides when the entire formula is finalized.

## Reports and review decisions

Keep each run's history in this repository at `nick-mac/reports/YYYY-MM-DD/YYYY-MM-DD-<computer-name>-alignment.md`, outside the installed `skill/` directory. Read the target's actual computer name for the filename; computer names belong in run reports, not portable standards or skill instructions. Use an ordinary, Git-visible filename. Preserve earlier runs; use a distinct run suffix for a second inspection of the same computer on the same date.

Use one combined Markdown table with Ref, Item, Baseline, This Mac, Recommendation, and Decision columns, one row per decision item in comparison order. Preserve recorded choices and write `Pending` in unanswered Decision cells so the preview retains all six columns in every row. Save each conversational decision immediately in this same file; do not maintain a separate decision document. A Pending or blank decision means no change: recommendations and baseline values are not authorization. Only an explicit decision for an item, or an explicitly specified group, can select a change. A recorded choice does not mean it has been applied.

Keep the table concise and actionable: describe what Nick sees or can do and what the recommendation would change. Explain technical names only when needed; an incomplete baseline observation is not a defined replacement configuration. Retain supporting inspection evidence and verification in the same file, under a collapsible details section when lengthy. Avoid duplicate decision summaries and instructions.

## Maintaining the build

Every managed value has a stable item ID. Preference IDs use `<component-id>:<domain>:<key>`; nested dictionary keys append `/subkey`. Asset and app-control IDs are documented in the component references. In the manifest's `item_decisions`, map each reviewed ID to its `review_state` (`accepted` or `deferred`), `choice` (`keep-recorded`, `adopt-observed`, `define-new`, or `defer`), and `decided_on` date. Store the selected value in its referenced standard artifact and the rationale in the decision record. Advance the manifest revision when an accepted standard changes.

When Nick adds a tool, app, or configuration, give it a component entry or add it to the appropriate existing component. Document inspection, application, verification, and any dependencies. Review newly discovered items before making them requirements.

Keep credentials, device identity, recordings, history contents, and unrelated shell configuration out of standard artifacts. Record settings that control those features when Nick chooses them. Do not bypass macOS permission prompts or treat a stored login preference as proof of login-item registration.

When changing the comparison helper, run `python3 -m unittest discover -s <skill-directory>/tests -v`. The [bundled tests](tests/test_compare_standard.py) use synthetic settings, require only Python's standard library, and do not inspect or modify the computer's configuration.
