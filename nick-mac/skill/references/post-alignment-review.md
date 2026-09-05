# Independent post-alignment review

After every alignment, assign a full read-only review to a fresh sub-agent that did not implement any of the changes. This is mandatory before reporting alignment complete, including when implementation was split among agents. An implementing agent cannot review its own changes. Use a fresh context when available, supplying the accepted plan, recorded decisions, original inspection, current standard, relevant procedures, and locations of evidence. Implementation success claims are not proof.

The reviewer must independently inspect the target and repository:

- Re-run the complete manifest comparison and component-specific checks. Reconcile every plan item with actual state, including intended retentions, explicit exceptions, and deferred items. A full review does not authorize changes outside the accepted scope.
- Verify apps, settings, assets, shell behavior, model readiness, permissions, login/background services, skill scope/source links, and removed-item leftovers. Check functional behavior where applicable; command exit codes and stored preferences alone are insufficient.
- Confirm the repository standard and decision records match the accepted choices, optional components were not made mandatory, and portable files contain no computer-name lists.
- Verify FluidVoice's zero-reporting requirement independently using the suppression mechanism and runtime evidence described in the voice transcription procedure. Cover delayed/weekly reporting, retries, relaunch/login, and helper processes; a short quiet observation is not proof that scheduled reporting is disabled.
- Compare before/after evidence for unintended changes, and identify missing evidence rather than assuming success.

Return findings by report reference or stable item ID, with expected state, observed state, evidence, and pass/fail/unverified outcome. Put a concise independent-review result in the existing alignment report, including the reviewer identity, date, scope, and unresolved findings. Do not create a second decision file.

The reviewer reports findings without repairing the target. The implementing agent handles corrections within the accepted plan, and the independent reviewer then rechecks them and relevant regressions. Material scope changes return to Nick. If the sub-agent cannot run, target access is unavailable, or required evidence remains missing, mark the review incomplete; do not substitute a self-review or claim full alignment.
