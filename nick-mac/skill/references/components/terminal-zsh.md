# Terminal and Shell

Component: `terminal`. Initial state: provisional observations awaiting item-level review.

## Recorded baseline

[standard.json](../../assets/terminal/standard.json) records the observed startup/default profile selections and captured appearance assets. Profile names in the data identify Terminal configurations, not computers. The `.terminal` assets contain appearance settings, without startup commands or environment secrets.

The accepted shell standard is Oh My Zsh with the Git plugin and the bundled `nick-mac.zsh-theme`. Its prompt shows the current folder, Git branch/status, commit age, and a new-line prompt marker. Compare these choices separately from the provisional Terminal appearance. The theme name identifies configuration, not a computer.

## Inspect and plan

Compare profile selections and the fields of the selected profiles. Inspect the target's login shell and relevant framework/theme/bootstrap settings without exposing unrelated environment variables or credentials. Use preference IDs from the shared workflow, `terminal:profile:<profile-name>` for appearance, and `terminal:shell:<setting>` for shell choices.

Offer the recorded appearance, the target's alternative, or a newly specified profile/setup. Review appearance differences at the setting level when Nick wants to combine choices. Do not automatically choose a framework, theme, or named built-in profile.

## Apply accepted choices

Update the repository selections and appearance assets when Nick adopts a different standard. Back up any target profile before replacement. Import the chosen `.terminal` profile through Terminal's settings, or merge its approved fields into the target's profile dictionary, then set only the approved startup/default selections. Include any opened Terminal window or restart in the accepted plan.

For shell changes, preserve unrelated startup-file content and make a minimal edit to the agreed setting. Installing or replacing a framework is a distinct plan item. Do not copy an entire shell configuration between computers.

## Verify

Read profile selections and appearance fields again, check shell-file syntax after edits, and confirm the selected appearance and prompt in a new Terminal session when that check is accepted and available. Report any remaining visual/session check explicitly.
