---
skill_name: nick-tool-cleanup
installation_scope: machine
installation_target: ~/.codex/skills/nick-tool-cleanup
installation_method: symlink
---

# Tool Cleanup Requirements

## Purpose

Maintain an evidence-backed inventory of optional software, make enabled or uncertain telemetry visible, preserve explicit telemetry approvals, and compare devices without treating differences as permission to change them.

## Requirements

1. Store each device’s Markdown report, `inventory.json`, and `telemetry-approvals.toml` under `/Users/nick/Vaults/Work/Tooling/Devices/<device-slug>/` unless another root is supplied.
2. Treat silence as not approved. Only an active entry created after explicit user authorization makes a telemetry channel approved.
3. Classify telemetry as enabled, disabled, unknown, or not configured using local evidence and current first-party documentation.
4. Keep host-application attribution separate from the embedded component or library that implements telemetry, and record confidence.
5. Put enabled unapproved telemetry first, followed by uncertain, approved, disabled/not-configured, installed tools, cross-device differences, and coverage limitations.
6. Discover optional applications, package-manager tools, extensions, personal skills and plugins, and non-system background services appropriate to the platform.
7. Exclude operating-system base components and transitive project dependencies by default.
8. Scheduled audits may update reports and snapshots but must not alter tools, settings, approvals, or suspicious files.
9. Record or revoke approval only after explicit authorization for the named stable telemetry channel.
10. An explicit opt-out request authorizes only the minimum supported configuration change for that channel. Verify the effective state and rerun the audit.
11. Compare stable IDs across device inventories and report missing tools, unique tools, version drift, and telemetry-policy drift as review prompts.
12. Investigate provenance before calling an unexpected tool unwanted; never install, upgrade, uninstall, or delete solely because inventories differ.

## Boundaries

- Do not infer consent from installation, use, vendor defaults, or lack of complaint.
- Do not launch GUI applications merely to identify versions or telemetry state.
- Do not treat uncertain evidence as proof or a component artifact as proof of its host application.
- Do not uninstall or remove software without a separate reviewed finding and explicit request.
- Never store secrets, access tokens, account identifiers, or raw telemetry payloads in reports or approval files.

## Success evidence

- Reports distinguish state, approval, host, component, evidence, and supported opt-out.
- Enabled unapproved channels and unknown states are conspicuous.
- Inventory comparisons use stable IDs and preserve uncertainty.
- Any authorized opt-out is persistent where possible and independently verified.
