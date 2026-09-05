# Finder

Component: `finder`. Initial state: provisional observations awaiting item-level review.

## Recorded baseline

[standard.json](../../assets/finder/standard.json) contains observed Finder preferences, the filename-extension preference, native Quick Action availability, and known workflow candidates. The bundled [VS Code workflow](../../assets/open%20in%20vs%20code.workflow) matches the observed installation.

Trim is explicitly disabled; Create PDF remains enabled. Preserve the relative order of the other actions; numeric indexes, including inactive Trim, are no longer required. `Open in Codex.workflow` is excluded and must not be installed or repaired by the standard. Other inherited menu choices remain provisional. Review actual service visibility and behavior on each target. Other observed workflows are candidates; their assets and behavior have not yet been adopted.

## Inspect and plan

Run the comparison helper for `finder`, then inspect Finder's actual settings, Services/Quick Actions, relevant app availability, and any workflow differences. Use `<component>:<domain>:<key>` IDs for preferences and `finder:workflow:<workflow-name>` for workflows. Treat each Quick Action entry within a dictionary as a separate decision if it differs.

Show both alternatives for each difference. New workflow candidates or menu entries require a decision just like existing values. Native service labels and preference keys may vary by OS version; inspect the target before proposing a write. Do not infer a menu's complete contents from saved preferences alone.

## Apply accepted choices

For a changed standard, update only the chosen values and assets in the repository. For target changes, back up affected preferences or workflows, then set individual approved values through Finder/System Settings or typed `defaults write` operations. Remove an override only when the accepted choice is the target OS default. Merge selected Quick Action dictionary entries instead of replacing unrelated entries.

Copy or replace only workflows included in the accepted plan, retaining a backup of any replaced workflow. Register/enable a supporting app or extension only when that is included. The plan must identify required installs and any Finder/service restart.

## Verify

Read changed preference values again, compare installed workflow contents, and check the affected Finder menu/actions. A missing supporting app or unavailable UI check remains blocked or manual; do not claim exact menu alignment from preference writes alone.
