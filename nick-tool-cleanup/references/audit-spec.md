# Audit specification

## State vocabulary

- `enabled`: direct local evidence or a documented default applies and no effective opt-out was found.
- `disabled`: an effective opt-out or disabled setting was found.
- `unknown`: the tool may collect telemetry, but local state or current vendor behavior is unresolved.
- `not configured`: an optional exporter or telemetry path exists but has no active destination.

An enabled channel is `approved` only when an active entry with the same stable channel ID exists in this device's `telemetry-approvals.toml`.

## Required report order

1. Summary and scan time
2. Enabled, unapproved telemetry
3. Unknown telemetry needing review
4. Enabled, explicitly approved telemetry
5. Disabled or not-configured telemetry
6. Optional tools grouped by category
7. Cross-device gaps and version drift
8. Coverage and collection failures

Telemetry rows should include channel ID, host application, component/provider, state, approval, local evidence, and the supported opt-out or a research-needed marker. Do not collapse the host and component into one column.

Tool rows should include stable ID, display name, version when available, discovery source, path or install scope when useful, and installation/birth date when available. Stable IDs should prefer bundle IDs or package-manager coordinates over display names.

## Telemetry controls initially recognized

Treat this as a starting catalog, not a permanent truth. Recheck first-party documentation before making changes.

| Channel ID | Host/component | Detection | Typical opt-out |
|---|---|---|---|
| `codex.analytics` | ChatGPT/Codex / Codex analytics | `[analytics].enabled` in `~/.codex/config.toml`; current documented default is enabled | Set `[analytics] enabled = false` |
| `codex.otel` | ChatGPT/Codex / OpenTelemetry exporter | Active `[otel]` exporter in Codex config | Set exporters to `none` or remove the explicit exporter |
| `onnxruntime.telemetry` | Attributed host / Microsoft ONNX Runtime | ORT session artifact, loaded runtime, or explicit setting | Set `ORT_DISABLE_TELEMETRY=1` in the effective environment before host launch |
| `homebrew.analytics` | Homebrew | Homebrew present plus effective analytics state | `brew analytics off` or the supported no-analytics environment setting |
| `dotnet.cli.telemetry` | .NET CLI | `dotnet` present and `DOTNET_CLI_TELEMETRY_OPTOUT` state | Set `DOTNET_CLI_TELEMETRY_OPTOUT=1` persistently |
| `powershell.telemetry` | PowerShell | `pwsh` present and `POWERSHELL_TELEMETRY_OPTOUT` state | Set `POWERSHELL_TELEMETRY_OPTOUT=1` before launch |
| `vscode.telemetry` | Visual Studio Code | `telemetry.telemetryLevel` in user settings or documented default | Set `telemetry.telemetryLevel` to `off` |
| `azure-cli.telemetry` | Azure CLI | `collect_telemetry` in `~/.azure/config` or documented default | Set `collect_telemetry = no` in the telemetry section |

Do not assume a shell environment variable reaches a macOS GUI app launched from Finder or the Dock. Verify the effective launch environment and persistence across login before calling an ORT opt-out complete.

## Attribution evidence

Prefer, in order:

1. a live process with the file open or a trace showing the write;
2. an application log naming the component and artifact;
3. package or bundle contents plus matching timestamp/provenance and task context;
4. distinctive file format or vendor source confirming only the component.

Levels 3–4 may justify `likely` component attribution but not an unsupported claim about the host application. Record confidence. For `:memory:.ses`, the timestamp-and-UUID format identifies the telemetry session component; separately establish which host loaded ORT.

## Approval file

The scanner owns this TOML structure:

```toml
schema_version = 1

[[approval]]
tool_id = "example.telemetry"
approved = true
approved_at = "2026-09-02T10:00:00-04:00"
reason = "Nick explicitly approved this channel for this device."
```

Revocation changes `approved` to `false` and adds `revoked_at` and `revocation_reason`. Never put access tokens, device secrets, raw event payloads, or account identifiers in the report or approval file.
