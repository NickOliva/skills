# Standard Decisions

The build is evolving. Record accepted changes by date and stable item ID, with the old value, chosen value, and Nick's reason when supplied. Keep computer names and unrelated device details out of this record. Values and assets live in their standard files; avoid duplicating large configuration data here.

## 2026-09-05 — Initial organization

- Nick chose iterative reviews across computers, with keep-recorded/adopt-observed/define-new choices for every differing item and one accepted alignment plan.
- The current Finder and Terminal settings are provisional review material. Inherited fixed menu, theme, and profile choices are reopened.
- Nick selected the captured FluidVoice setup as the initial voice transcription standard. Later differences remain subject to item-level decisions.
- No complete formula has been finalized. Additional tools, apps, and configuration items remain open to inclusion through review.

## 2026-09-05 — Application scope and inclusion

- Nick excluded software versions from the skill: identify tools and compare configuration, with updates managed independently. Removed captured software release/build fields and release comparisons; existing updater preferences remain configuration choices.
- Nick accepted inclusion of 1Password, Amazon Kindle, ChatGPT, Day One, Developer, Docker, Dropbox, FluidVoice, Google Chrome, Microsoft Excel, Microsoft PowerPoint, Microsoft Teams, Microsoft Word, Obsidian, Pages, Safari, TestFlight, Visual Studio Code, Xcode, and zoom.us. Each `applications:app:<bundle-id>` moved from candidate to required. Additional configuration choices remain awaiting review; FluidVoice retains its existing baseline.
- Keynote, Numbers, and Slack moved from candidate to not-required. This permits them to remain installed and does not authorize removal.
- OneDrive was initially deferred while Nick considered Office dependencies.

## 2026-09-05 — OneDrive excluded

- `applications:app:com.microsoft.OneDrive` changed from pending to not-required. Nick does not use OneDrive storage or syncing and excluded the desktop application from the standard.
- Nick separately authorized uninstalling OneDrive from the current target Mac. This does not authorize removal from other Macs; future runs review any proposed removal in the combined plan.

## 2026-09-05 — Background-task review

- Nick approved removing the stale Atlas updater and two Zoom updater tasks targeting an absent user installation. They were unloaded and their plists moved to Trash; the active Zoom installation's helpers were retained.
- Nick requested carrying these decisions into future Mac reviews. The background-items component records conditional cleanup of stale Atlas/Zoom tasks, retention of applicable Docker and installed-app helpers, and verification of the ONNX Runtime telemetry opt-out task. New targets still receive one combined plan before changes.
- Preserve `com.nick.tool-cleanup.telemetry-optouts`, which sets `ORT_DISABLE_TELEMETRY=1` at login. Use “Telemetry opt-out (ONNX Runtime)” in reports. No simple Settings display-name override was found; the functional task remains unchanged, as Nick permitted.
- The OneDrive uninstall required stopping its updater services and removing SyncReporter as well as the app. Keep this verification in future accepted uninstalls; do not confuse disabled background records with active services.

## 2026-09-05 — Repository-only Nick Mac and skill scope checks

- Nick moved Nick Mac from machine scope to this repository only. The repository discovery link points to `../../nick-mac/skill`; the previous global link was removed. An older global backup with the same skill name was preserved outside skill discovery.
- Every full run now audits all Nick Skills installation declarations for presence, proper scope, current source links, and duplicate or stale installations. Skills without implementations remain pending. Other installation differences are findings for review, not implicit authorization to move or install those skills.

## 2026-09-05 — Optional peripherals, zero reporting, and independent review

- `applications:app:com.elgato.StreamDeck`: previously unlisted, now explicitly optional (`not-required`), together with its Corsair helper. Nick selects targets individually in run history; monitor connection alone creates no requirement. Portable artifacts contain no computer-name lists.
- `voice-transcription:control:reporting`: the captured detailed-analytics-off preference is insufficient. Require zero reporting, including weekly activity and helper/diagnostic uploads, with prevention before first launch and independent verification. If unproven, keep FluidVoice inactive and report blocked; no residual-reporting alternative. This changes the standard, not target configuration.
- Every alignment now requires a full independent review by a separate sub-agent that implemented none of the changes, with evidence, findings, corrections, and independent rechecks recorded in the same alignment report.

## 2026-09-05 — Accepted alignment choices

- Finder desktop disk visibility and new-window Documents destination: accepted recorded values. Trim: disabled in the standard. Quick Action numeric ordering: retired; preserve remaining actions' relative order. Create PDF stays enabled.
- `finder:workflow:Open in Codex.workflow`: excluded from the standard; remove rather than repair when selected in the target plan.
- `terminal:shell:framework`, `terminal:shell:theme`, `terminal:shell:plugins`: adopt Oh My Zsh, the bundled `nick-mac` prompt, and Git plugin. Preserve unrelated startup-file contents.
- `background-items:telemetry-optout`: adopt the combined login task for ONNX Runtime and PowerShell opt-outs.
- Target-specific removals and retained application exceptions remain in the approved run report; they do not become blanket removal rules or relax the portable application requirements.

## 2026-09-05 — Review only after implementation is complete

- Independent review must not launch during partial alignment. The implementing agent must believe all accepted changes and required checks are 100% complete first. Explain and resolve outstanding work with Nick; never silently defer an accepted requirement. A premature review does not count as the final independent review. FluidVoice installation remains required.

## 2026-09-05 — AI enhancement off

- `voice-transcription:control:ai-enhancement`: Nick requires AI text enhancement off on the target and in the standard. Dictation AI prompts are Off; the AI editing shortcut is disabled. Speech recognition stays enabled. Enhancement model downloads and provider selection are no longer requirements; existing files may remain inactive. Manifest revision 8 records this replacement of the original enhancement-enabled baseline.
