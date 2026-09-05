# Build Manifest

[manifest.json](../manifest.json) registers the current components. Each standard artifact contains individual values to compare; component-level agreement never bypasses review of a differing item.

| Component | Specification | Starting review state |
| --- | --- | --- |
| Finder | [Finder](components/finder-context-menu.md) | Current configuration captured as provisional |
| Terminal and shell | [Terminal](components/terminal-zsh.md) | Current configuration captured as provisional |
| Applications | [Applications](components/applications.md) | Inclusion accepted; additional configurations await review |
| Background tasks | [Login and background items](components/background-items.md) | Review and retention policies accepted; inspect each target |
| Voice transcription | [FluidVoice](components/voice-transcription.md) | Captured setup chosen as initial standard |

For an unset setting, inspect its effective application or OS default before concluding there is a difference. State any coverage gap; preferences alone do not inventory all UI behavior.

## Extending the manifest

Add installations and configurations as named items within an existing component, or create a component when it has its own inspection and application procedure. Give it stable IDs, a standard artifact, review state, dependencies, and verification. Add scripts only when they improve reliability.

Review newly discovered apps and tools as candidates. Do not promote an entire installed-software inventory to the standard. Use the same keep/adopt/new decision for every item, and update the standard and decision record only under the accepted plan.

Track application identity and configuration without software versions. Presence alone does not establish configuration alignment.
