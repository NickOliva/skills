---
name: nick-tool-cleanup
description: Inventory optional software on Nick's computers, identify enabled or uncertain telemetry, preserve explicit telemetry approvals, opt tools out on request, and compare device inventories for missing or unexpected tools. Use for local tool audits, telemetry/privacy checks, device tooling comparisons, unexpected-install investigations, or telemetry opt-outs; do not use for ordinary software installation or removal without a reviewed finding.
---

# Nick Tool Cleanup

Keep an evidence-backed inventory of optional software and make unapproved telemetry conspicuous. Treat silence as **not approved**: an enabled setting is not consent.

## Durable files

Use `/Users/nick/Vaults/Work/Tooling/Devices` unless Nick supplies another root. Give each device its own directory:

```text
Devices/<device-slug>/
  <device-slug>.md
  inventory.json
  telemetry-approvals.toml
```

The Markdown file is the human-facing record. `inventory.json` supplies stable IDs for comparison. `telemetry-approvals.toml` is the only authority for telemetry Nick explicitly allowed on that device.

Never infer approval from an enabled setting, prior use, installation, vendor defaults, or lack of complaint. Add an approval only after Nick explicitly authorizes that named telemetry channel. Store the channel ID, approval date, and Nick's stated reason or scope. Removing or disabling telemetry does not require deleting its historical approval entry; mark it revoked instead.

## Audit workflow

1. Read [references/audit-spec.md](references/audit-spec.md).
2. From this skill directory, run:

   ```bash
   python3 scripts/inventory_tools.py audit
   ```

   Use `--output-root` only when Nick identifies a different destination. Use `--dry-run` for testing that must not update the Vault.
3. Review command failures and coverage notes. Supplement the deterministic scan when package managers, application stores, extension hosts, or background services present on that platform were not covered.
4. Investigate high-risk findings before assigning a parent application. Distinguish the **host application or process** that caused the activity, the **embedded component or library** that implemented it, and the evidence and confidence for that attribution.
5. For unfamiliar telemetry, verify the current behavior and opt-out using first-party documentation or source. Do not call telemetry enabled merely because the word `analytics` appears in a file. Preserve URLs and local evidence in the report.
6. Keep enabled, unapproved telemetry at the top of the Markdown report. Follow it with uncertain telemetry, approved telemetry, disabled telemetry, the installed-tool inventory, recent or unexplained items, cross-device gaps, and coverage limitations.
7. Report the updated path and only material findings in chat.

The scanner suppresses common telemetry variables in discovery subprocesses so the audit itself does not unnecessarily create telemetry. Do not launch a GUI application merely to learn its version or telemetry state.

## Scheduled audit

A scheduled run is read-only with respect to installed tools and their settings. It may update the device report and snapshot, but it must not:

- grant or revoke telemetry approval;
- opt a tool out;
- uninstall, install, upgrade, or launch a tool; or
- delete suspicious artifacts.

Flag every enabled channel absent from `telemetry-approvals.toml`. Also flag unknown states for review, but do not describe them as proven telemetry. If evidence changes, retain the latest evidence and say what remains uncertain.

## Record an explicit approval

Only after Nick explicitly approves a named channel, run:

```bash
python3 scripts/inventory_tools.py approve \
  --tool-id <stable-telemetry-channel-id> \
  --reason "<Nick's stated scope or reason>"
```

Then rerun `audit`. Use `revoke --tool-id <id> --reason "<reason>"` when Nick withdraws approval. Do not use these commands during an unattended scheduled run.

## Opt out of telemetry

An explicit request such as “disable telemetry for Codex” authorizes only that named channel and the minimum configuration change needed to disable it.

1. Resolve the exact host app, embedded component, version, current state, and configuration scope. Ask only if multiple scopes would materially differ.
2. Verify the current vendor-supported opt-out from first-party documentation or installed source. Prefer a persistent per-user setting over a temporary process variable. If only a session-scoped control exists, say so.
3. Protect the audit command itself with temporary opt-out environment variables. Prefer app-native settings or commands; otherwise edit the smallest relevant user config while preserving unrelated content.
4. Show or describe the exact target before a system-wide change, background-agent change, or account-level privacy change. Do not interpret “opt out” as permission to uninstall the tool.
5. Apply the change, restart only the affected process when necessary, and verify the effective state without generating avoidable telemetry.
6. Rerun the audit. Record the mechanism and evidence in the report. Do not add an allowlist entry for disabled telemetry.

For Codex analytics and ONNX Runtime, keep the channels separate: `codex.analytics` is OpenAI Codex product analytics; `onnxruntime.telemetry` is Microsoft telemetry emitted by the ONNX Runtime library embedded in a host. ONNX is a machine-learning model format; ORT is the runtime that executes ONNX models. A file such as `:memory:.ses` is component evidence, not by itself the name of the responsible application.

## Compare devices and investigate surprises

The audit compares this device's stable tool IDs against every sibling `inventory.json` under the Devices root. Interpret differences as prompts for review, not automatic installation instructions.

- **Missing here:** present on another device but absent here. Offer to investigate or install only when Nick requests it.
- **Only here:** absent from all other recorded devices. Check installation time, path, package manager, signer or provenance, parent bundle, background service, and likely installer before calling it unwanted.
- **Version drift:** same tool with differing versions. Do not upgrade automatically.
- **Telemetry-policy drift:** compare matching channel states and explicit approvals across devices. Approval is device-specific unless Nick explicitly makes it fleet-wide.

Never remove an unexpected tool solely because another computer lacks it. Present the evidence and ask for a deletion decision when removal is desired.

## Platform coverage

On macOS, examine `/Applications`, `~/Applications`, Homebrew formulae and casks, common language-level tool managers, editor extensions, Codex plugins and personal skills, and non-Apple LaunchAgents/LaunchDaemons. On Linux or Windows, adapt these categories to the native application/package managers, extension hosts, startup services, and user-level tool managers.

Exclude operating-system base components and transitive project dependencies by default. List scan omissions explicitly; “all tools” means all optional tools discoverable through the covered sources, not a claim that an opaque application bundle or unmanaged environment has been exhaustively decomposed.
