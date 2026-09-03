#!/usr/bin/env python3
"""Inventory optional tools, flag unapproved telemetry, and compare devices."""

from __future__ import annotations

import argparse
import configparser
import datetime as dt
import json
import os
import platform
import plistlib
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


DEFAULT_OUTPUT_ROOT = Path("/Users/nick/Vaults/Work/Tooling/Devices")
SKIP_DIRS = {
    ".git", ".hg", ".svn", ".cache", ".Trash", "Library", "node_modules",
    ".venv", "venv", "dist", "build", "DerivedData",
}
QUIET_ENV = {
    "DO_NOT_TRACK": "1",
    "ORT_DISABLE_TELEMETRY": "1",
    "HOMEBREW_NO_ANALYTICS": "1",
    "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
    "POWERSHELL_TELEMETRY_OPTOUT": "1",
    "AZURE_CORE_COLLECT_TELEMETRY": "0",
    "CHECKPOINT_DISABLE": "1",
    "NEXT_TELEMETRY_DISABLED": "1",
    "GATSBY_TELEMETRY_DISABLED": "1",
    "NG_CLI_ANALYTICS": "false",
    "UV_CACHE_DIR": "/private/tmp/nick-tool-cleanup-uv-cache",
}


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return result or "unknown-device"


def run(command: list[str], timeout: int = 15, quiet: bool = True) -> dict[str, Any]:
    env = os.environ.copy()
    if quiet:
        env.update(QUIET_ENV)
    try:
        proc = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout, env=env, check=False,
        )
        return {
            "ok": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr.strip(),
            "returncode": proc.returncode,
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "stdout": "", "stderr": str(exc), "returncode": None}


def device_name() -> str:
    if sys.platform == "darwin":
        for key in ("ComputerName", "LocalHostName"):
            result = run(["scutil", "--get", key], quiet=False)
            if result["ok"] and result["stdout"].strip():
                return result["stdout"].strip()
    return os.environ.get("COMPUTERNAME") or socket.gethostname().split(".")[0]


def birth_date(path: Path) -> str:
    try:
        stamp = path.stat().st_birthtime
    except (AttributeError, OSError):
        return ""
    return dt.datetime.fromtimestamp(stamp).astimezone().date().isoformat()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def add_tool(
    tools: dict[str, dict[str, Any]], tool_id: str, name: str, category: str,
    version: str = "", source: str = "", path: str = "", installed: str = "",
    notes: str = "",
) -> None:
    candidate = {
        "id": tool_id,
        "name": name,
        "category": category,
        "version": version or "unknown",
        "source": source,
        "path": path,
        "installed": installed or "unknown",
        "notes": notes,
    }
    old = tools.get(tool_id)
    if not old:
        tools[tool_id] = candidate
        return
    for key in ("version", "source", "path", "installed", "notes"):
        if old.get(key) in ("", "unknown") and candidate.get(key) not in ("", "unknown"):
            old[key] = candidate[key]


def collect_apps(tools: dict[str, dict[str, Any]], failures: list[str]) -> None:
    for root in (Path("/Applications"), Path.home() / "Applications"):
        if not root.exists():
            continue
        try:
            apps = sorted(root.glob("*.app"), key=lambda item: item.name.casefold())
        except OSError as exc:
            failures.append(f"Applications at {root}: {exc}")
            continue
        for app in apps:
            info: dict[str, Any] = {}
            try:
                with (app / "Contents" / "Info.plist").open("rb") as handle:
                    info = plistlib.load(handle)
            except (OSError, plistlib.InvalidFileException, ValueError):
                pass
            name = str(info.get("CFBundleDisplayName") or info.get("CFBundleName") or app.stem)
            bundle = str(info.get("CFBundleIdentifier") or slug(name))
            version = str(info.get("CFBundleShortVersionString") or info.get("CFBundleVersion") or "")
            add_tool(
                tools, f"app:{bundle}", name, "Applications", version,
                "macOS application bundle", str(app), birth_date(app),
            )


def collect_line_manager(
    tools: dict[str, dict[str, Any]], failures: list[str], executable: str,
    command: list[str], category: str, prefix: str, parser,
) -> None:
    binary = shutil.which(executable)
    if not binary:
        return
    add_tool(tools, f"cli:{executable}", executable, "Command-line tools", source="PATH", path=binary)
    result = run(command)
    if not result["ok"]:
        failures.append(f"{executable}: {result['stderr'] or 'collection command failed'}")
        return
    try:
        for name, version in parser(result["stdout"]):
            add_tool(tools, f"{prefix}:{name.casefold()}", name, category, version, executable)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        failures.append(f"{executable}: could not parse inventory ({exc})")


def parse_brew(text: str) -> Iterable[tuple[str, str]]:
    for line in text.splitlines():
        parts = line.split()
        if parts:
            yield parts[0], " ".join(parts[1:])


def parse_npm(text: str) -> Iterable[tuple[str, str]]:
    data = json.loads(text or "{}")
    for name, metadata in sorted(data.get("dependencies", {}).items()):
        yield name, str((metadata or {}).get("version", ""))


def parse_code(text: str) -> Iterable[tuple[str, str]]:
    for line in text.splitlines():
        item = line.strip()
        if not item:
            continue
        name, marker, version = item.rpartition("@")
        yield (name, version) if marker else (item, "")


def parse_dotnet(text: str) -> Iterable[tuple[str, str]]:
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 3 and not set(parts[0]) <= {"-"} and parts[0].casefold() != "package":
            yield parts[0], parts[1]


def parse_uv(text: str) -> Iterable[tuple[str, str]]:
    for line in text.splitlines():
        match = re.match(r"^(\S+)\s+v?([^\s]+)", line.strip())
        if match:
            yield match.group(1), match.group(2)


def parse_pipx(text: str) -> Iterable[tuple[str, str]]:
    data = json.loads(text or "{}")
    for name, metadata in sorted(data.get("venvs", {}).items()):
        main = (metadata or {}).get("metadata", {}).get("main_package", {})
        yield name, str(main.get("package_version", ""))


def parse_cargo(text: str) -> Iterable[tuple[str, str]]:
    for line in text.splitlines():
        match = re.match(r"^(\S+)\s+v([^:]+):$", line.strip())
        if match:
            yield match.group(1), match.group(2)


def collect_managers(tools: dict[str, dict[str, Any]], failures: list[str]) -> None:
    specs = [
        ("brew", ["brew", "list", "--formula", "--versions"], "Homebrew formulae", "brew-formula", parse_brew),
        ("brew", ["brew", "list", "--cask", "--versions"], "Homebrew casks", "brew-cask", parse_brew),
        ("npm", ["npm", "ls", "-g", "--depth=0", "--json"], "Global npm packages", "npm", parse_npm),
        ("pipx", ["pipx", "list", "--json"], "pipx applications", "pipx", parse_pipx),
        ("uv", ["uv", "tool", "list"], "uv tools", "uv-tool", parse_uv),
        ("cargo", ["cargo", "install", "--list"], "Cargo applications", "cargo", parse_cargo),
        ("dotnet", ["dotnet", "tool", "list", "--global"], ".NET global tools", "dotnet-tool", parse_dotnet),
        ("code", ["code", "--list-extensions", "--show-versions"], "VS Code extensions", "vscode-extension", parse_code),
        ("cursor", ["cursor", "--list-extensions", "--show-versions"], "Cursor extensions", "cursor-extension", parse_code),
    ]
    for executable, command, category, prefix, parser in specs:
        collect_line_manager(tools, failures, executable, command, category, prefix, parser)


def collect_mas(tools: dict[str, dict[str, Any]], failures: list[str]) -> None:
    if not shutil.which("mas"):
        return
    result = run(["mas", "list"])
    if not result["ok"]:
        failures.append(f"Mac App Store: {result['stderr'] or 'mas list failed'}")
        return
    for line in result["stdout"].splitlines():
        match = re.match(r"^(\d+)\s+(.+?)\s+\(([^)]+)\)$", line.strip())
        if match:
            app_id, name, version = match.groups()
            add_tool(tools, f"mas:{app_id}", name, "Mac App Store", version, "mas")


def collect_codex(tools: dict[str, dict[str, Any]]) -> None:
    config = Path.home() / ".codex" / "config.toml"
    text = read_text(config)
    for match in re.finditer(r'^\[plugins\."([^"]+)"\]\s*\nenabled\s*=\s*true', text, re.MULTILINE):
        plugin = match.group(1)
        add_tool(tools, f"codex-plugin:{plugin}", plugin, "Codex plugins", source=str(config))
    for root in (Path.home() / ".codex" / "skills", Path.home() / ".agents" / "skills"):
        if not root.exists():
            continue
        for skill_file in root.glob("*/SKILL.md"):
            name = skill_file.parent.name
            add_tool(
                tools, f"codex-skill:{name}", name, "Personal Codex skills",
                source=str(root), path=str(skill_file.parent),
            )


def collect_launch_items(tools: dict[str, dict[str, Any]], failures: list[str]) -> None:
    if sys.platform != "darwin":
        return
    roots = (
        Path.home() / "Library" / "LaunchAgents",
        Path("/Library/LaunchAgents"),
        Path("/Library/LaunchDaemons"),
    )
    for root in roots:
        if not root.exists():
            continue
        try:
            items = list(root.glob("*.plist"))
        except OSError as exc:
            failures.append(f"Launch items at {root}: {exc}")
            continue
        for item in items:
            info: dict[str, Any] = {}
            try:
                with item.open("rb") as handle:
                    info = plistlib.load(handle)
            except (OSError, plistlib.InvalidFileException, ValueError):
                pass
            label = str(info.get("Label") or item.stem)
            if label.startswith("com.apple."):
                continue
            executable = str(info.get("Program") or "")
            if not executable and isinstance(info.get("ProgramArguments"), list):
                executable = str((info.get("ProgramArguments") or [""])[0])
            add_tool(
                tools, f"launch-item:{label}", label, "Background services",
                source=str(root), path=executable or str(item), installed=birth_date(item),
            )


def truthy(value: str | None) -> bool:
    return str(value or "").strip().casefold() in {"1", "true", "yes", "on"}


def toml_section_value(text: str, section: str, key: str) -> str | None:
    section_match = re.search(
        rf"^\[{re.escape(section)}\]\s*$([\s\S]*?)(?=^\[|\Z)", text, re.MULTILINE,
    )
    if not section_match:
        return None
    key_match = re.search(
        rf"^{re.escape(key)}\s*=\s*(.+?)\s*$", section_match.group(1), re.MULTILINE,
    )
    return key_match.group(1).strip().strip('"\'') if key_match else None


def find_ort_artifacts(limit: int = 50) -> list[Path]:
    roots = (Path.cwd(), Path.home() / "repos", Path.home() / "Vaults", Path.home() / "Documents")
    found: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        try:
            root = root.resolve()
        except OSError:
            continue
        for base, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = [name for name in dirs if name not in SKIP_DIRS and not name.startswith(".")]
            if ":memory:.ses" not in files:
                continue
            path = Path(base) / ":memory:.ses"
            try:
                resolved = path.resolve()
            except OSError:
                resolved = path
            if resolved not in seen:
                seen.add(resolved)
                found.append(path)
            if len(found) >= limit:
                return found
    return found


def provenance_app(path: Path) -> tuple[str, str]:
    if sys.platform != "darwin" or not shutil.which("xattr"):
        return "unknown", "not available"
    result = run(["xattr", "-px", "com.apple.provenance", str(path)], quiet=False)
    marker = re.sub(r"\s+", "", result["stdout"]).casefold()
    if not result["ok"] or not marker:
        return "unknown", "no provenance tag"
    matches: list[str] = []
    for root in (Path("/Applications"), Path.home() / "Applications"):
        if not root.exists():
            continue
        for app in root.glob("*.app"):
            candidate = run(["xattr", "-px", "com.apple.provenance", str(app)], quiet=False)
            candidate_marker = re.sub(r"\s+", "", candidate["stdout"]).casefold()
            if candidate["ok"] and candidate_marker == marker:
                label = "ChatGPT/Codex Desktop" if app.stem == "ChatGPT" else app.stem
                matches.append(label)
    if len(matches) == 1:
        return matches[0], "matching macOS provenance tag"
    if matches:
        return ", ".join(sorted(matches)), "non-unique matching macOS provenance tag"
    return "unknown", "provenance tag did not match an installed application bundle"


def parse_jsonc_setting(path: Path, key: str) -> str | None:
    match = re.search(rf'"{re.escape(key)}"\s*:\s*"([^"]+)"', read_text(path))
    return match.group(1) if match else None


def finding(
    channel_id: str, host: str, component: str, state: str, evidence: str,
    opt_out: str, source_url: str, confidence: str = "high",
) -> dict[str, str]:
    return {
        "id": channel_id,
        "host": host,
        "component": component,
        "state": state,
        "evidence": evidence,
        "opt_out": opt_out,
        "source_url": source_url,
        "confidence": confidence,
    }


def collect_telemetry(
    tools: dict[str, dict[str, Any]], failures: list[str], artifacts: list[Path],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    config_path = Path.home() / ".codex" / "config.toml"
    config = read_text(config_path)
    analytics = toml_section_value(config, "analytics", "enabled")
    analytics_disabled = analytics is not None and analytics.casefold() == "false"
    findings.append(finding(
        "codex.analytics", "ChatGPT/Codex Desktop", "OpenAI Codex product analytics",
        "disabled" if analytics_disabled else "enabled",
        f"{config_path}: analytics.enabled={analytics if analytics is not None else 'absent; documented default applies'}",
        "Set [analytics] enabled = false in ~/.codex/config.toml",
        "https://learn.chatgpt.com/docs/config-file/config-advanced#metrics",
    ))
    otel_exporter = toml_section_value(config, "otel", "exporter")
    otel_metrics = toml_section_value(config, "otel", "metrics_exporter")
    otel_active = any(value and value.casefold() != "none" for value in (otel_exporter, otel_metrics))
    findings.append(finding(
        "codex.otel", "ChatGPT/Codex Desktop", "Codex OpenTelemetry exporter",
        "enabled" if otel_active else "not configured",
        f"{config_path}: exporter={otel_exporter or 'none'}, metrics_exporter={otel_metrics or 'none'}",
        "Set exporters to none or remove the explicit exporter",
        "https://learn.chatgpt.com/docs/config-file/config-advanced#otel",
    ))
    ort_process_disabled = truthy(os.environ.get("ORT_DISABLE_TELEMETRY"))
    ort_launchd_result = run(["launchctl", "getenv", "ORT_DISABLE_TELEMETRY"], quiet=False) if sys.platform == "darwin" else {"stdout": ""}
    ort_launchd_disabled = truthy(ort_launchd_result.get("stdout", ""))
    ort_agent = Path.home() / "Library" / "LaunchAgents" / "com.nick.tool-cleanup.telemetry-optouts.plist"
    ort_persistent = ort_agent.exists() and "ORT_DISABLE_TELEMETRY" in read_text(ort_agent)
    ort_agent_status = run(
        ["launchctl", "print", f"gui/{os.getuid()}/com.nick.tool-cleanup.telemetry-optouts"],
        quiet=False,
    ) if sys.platform == "darwin" else {"ok": False, "stdout": ""}
    ort_agent_loaded = bool(
        ort_agent_status.get("ok") and "last exit code = 0" in ort_agent_status.get("stdout", "")
    )
    ort_disabled = ort_process_disabled or ort_launchd_disabled or (ort_persistent and ort_agent_loaded)
    if artifacts:
        hosts: list[str] = []
        evidence_bits: list[str] = []
        for artifact in artifacts[:5]:
            host, host_evidence = provenance_app(artifact)
            hosts.append(host)
            evidence_bits.append(f"{artifact} ({host_evidence})")
        known_hosts = sorted({item for item in hosts if item != "unknown"})
        host = ", ".join(known_hosts) if known_hosts else "Unattributed host application"
        add_tool(
            tools, "runtime:onnxruntime", "ONNX Runtime (ORT)", "Embedded runtimes",
            source="ORT telemetry session artifact", path=str(artifacts[0]),
            notes=f"Embedded component; host attribution: {host}",
        )
        findings.append(finding(
            "onnxruntime.telemetry", host, "Microsoft ONNX Runtime telemetry",
            "disabled" if ort_disabled else "enabled",
            "; ".join(evidence_bits)
            + f"; current process={'disabled' if ort_process_disabled else 'not disabled'}"
            + f"; launchd={'disabled for future launches' if ort_launchd_disabled else 'value not visible inside audit sandbox'}"
            + f"; persistent login agent={'loaded successfully' if ort_agent_loaded else ('present but not loaded' if ort_persistent else 'absent')}"
            + ("; restart host application to apply to the current process" if not ort_process_disabled else ""),
            "Set ORT_DISABLE_TELEMETRY=1 in the host application's effective launch environment",
            "https://github.com/microsoft/onnxruntime/blob/main/docs/Privacy.md",
            "high" if known_hosts else "medium",
        ))
    if "cli:brew" in tools:
        brew_state = run(["brew", "analytics", "state"], quiet=False)
        normalized_state = brew_state.get("stdout", "").casefold()
        disabled = "analytics are disabled" in normalized_state
        enabled = "analytics are enabled" in normalized_state
        findings.append(finding(
            "homebrew.analytics", "Homebrew", "Homebrew analytics",
            "disabled" if disabled else ("enabled" if enabled else "unknown"),
            f"brew analytics state: {brew_state.get('stdout', '').strip() or brew_state.get('stderr', 'unavailable')}",
            "Run brew analytics off", "https://docs.brew.sh/Analytics",
        ))
    if "cli:dotnet" in tools:
        disabled = truthy(os.environ.get("DOTNET_CLI_TELEMETRY_OPTOUT"))
        findings.append(finding(
            "dotnet.cli.telemetry", ".NET CLI", "Microsoft .NET CLI telemetry",
            "disabled" if disabled else "enabled",
            f"DOTNET_CLI_TELEMETRY_OPTOUT={'set' if disabled else 'unset; documented default applies'}",
            "Set DOTNET_CLI_TELEMETRY_OPTOUT=1 persistently",
            "https://learn.microsoft.com/dotnet/core/tools/telemetry",
        ))
    if shutil.which("pwsh"):
        disabled = truthy(os.environ.get("POWERSHELL_TELEMETRY_OPTOUT"))
        findings.append(finding(
            "powershell.telemetry", "PowerShell", "Microsoft PowerShell telemetry",
            "disabled" if disabled else "enabled",
            f"POWERSHELL_TELEMETRY_OPTOUT={'set' if disabled else 'unset; documented default applies'}",
            "Set POWERSHELL_TELEMETRY_OPTOUT=1 before PowerShell starts",
            "https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_telemetry",
        ))
    vscode_app = any(tool["name"] == "Visual Studio Code" for tool in tools.values()) or shutil.which("code")
    if vscode_app:
        settings = Path.home() / "Library" / "Application Support" / "Code" / "User" / "settings.json"
        level = parse_jsonc_setting(settings, "telemetry.telemetryLevel")
        findings.append(finding(
            "vscode.telemetry", "Visual Studio Code", "Microsoft VS Code telemetry",
            "disabled" if str(level).casefold() == "off" else "enabled",
            f"{settings}: telemetry.telemetryLevel={level or 'absent; documented default applies'}",
            "Set telemetry.telemetryLevel to off",
            "https://code.visualstudio.com/docs/configure/telemetry",
        ))
    if shutil.which("az"):
        azure_config = Path.home() / ".azure" / "config"
        parser = configparser.ConfigParser()
        value = None
        try:
            parser.read(azure_config)
            value = parser.get("core", "collect_telemetry", fallback=None)
        except configparser.Error as exc:
            failures.append(f"Azure CLI telemetry config: {exc}")
        disabled = str(value).casefold() in {"no", "false", "0", "off"}
        findings.append(finding(
            "azure-cli.telemetry", "Azure CLI", "Microsoft Azure CLI telemetry",
            "disabled" if disabled else "enabled",
            f"{azure_config}: core.collect_telemetry={value or 'absent; documented default applies'}",
            "Set core.collect_telemetry = no in ~/.azure/config",
            "https://learn.microsoft.com/cli/azure/azure-cli-telemetry",
        ))
    return findings


def parse_approvals(path: Path) -> dict[str, dict[str, Any]]:
    approvals: dict[str, dict[str, Any]] = {}
    for block in re.split(r"(?=^\[\[approval\]\]\s*$)", read_text(path), flags=re.MULTILINE):
        if not block.startswith("[[approval]]"):
            continue
        values: dict[str, Any] = {}
        for key, raw in re.findall(r'^([a-z_]+)\s*=\s*(.+?)\s*$', block, re.MULTILINE):
            raw = raw.strip()
            if raw in ("true", "false"):
                values[key] = raw == "true"
            elif len(raw) >= 2 and raw[0] == raw[-1] == '"':
                values[key] = raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        if values.get("tool_id"):
            approvals[str(values["tool_id"])] = values
    return approvals


def toml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def write_approvals(path: Path, approvals: dict[str, dict[str, Any]]) -> None:
    lines = [
        "schema_version = 1", "",
        "# Entries are changed only after Nick explicitly approves or revokes a channel.",
    ]
    order = ("tool_id", "approved", "approved_at", "reason", "revoked_at", "revocation_reason")
    for tool_id in sorted(approvals):
        record = approvals[tool_id]
        lines.extend(["", "[[approval]]"])
        for key in order:
            if key not in record:
                continue
            value = record[key]
            rendered = str(value).lower() if isinstance(value, bool) else toml_quote(str(value))
            lines.append(f"{key} = {rendered}")
    atomic_write(path, "\n".join(lines) + "\n")


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def load_snapshots(root: Path, current_slug: str) -> dict[str, dict[str, Any]]:
    snapshots: dict[str, dict[str, Any]] = {}
    if not root.exists():
        return snapshots
    for path in root.glob("*/inventory.json"):
        if path.parent.name == current_slug:
            continue
        data = load_json(path)
        if data:
            snapshots[path.parent.name] = data
    return snapshots


def compare_devices(
    current_tools: list[dict[str, Any]], current_telemetry: list[dict[str, Any]],
    snapshots: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    current = {item["id"]: item for item in current_tools}
    elsewhere: dict[str, set[str]] = defaultdict(set)
    versions: dict[str, dict[str, str]] = defaultdict(dict)
    policy: dict[str, dict[str, str]] = defaultdict(dict)
    for device, snapshot in snapshots.items():
        for item in snapshot.get("tools", []):
            tool_id = str(item.get("id"))
            elsewhere[tool_id].add(device)
            versions[tool_id][device] = str(item.get("version", "unknown"))
        for item in snapshot.get("telemetry", []):
            policy[str(item.get("id"))][device] = (
                f"{item.get('state', 'unknown')}; approved={'yes' if item.get('approved') else 'no'}"
            )
    missing = [
        {"id": tool_id, "devices": sorted(devices)}
        for tool_id, devices in sorted(elsewhere.items()) if tool_id not in current
    ]
    only_here = [tool_id for tool_id in sorted(current) if tool_id not in elsewhere]
    drift = []
    for tool_id, item in sorted(current.items()):
        other_versions = versions.get(tool_id, {})
        values = {item.get("version", "unknown"), *other_versions.values()}
        if other_versions and len(values) > 1:
            drift.append({"id": tool_id, "here": item.get("version", "unknown"), "elsewhere": other_versions})
    policy_drift = []
    for item in current_telemetry:
        other_policy = policy.get(item["id"], {})
        here = f"{item['state']}; approved={'yes' if item.get('approved') else 'no'}"
        if other_policy and len({here, *other_policy.values()}) > 1:
            policy_drift.append({"id": item["id"], "here": here, "elsewhere": other_policy})
    return {
        "missing_here": missing,
        "only_here": only_here,
        "version_drift": drift,
        "telemetry_policy_drift": policy_drift,
    }


def changes_since(prior: dict[str, Any] | None, tools: list[dict[str, Any]]) -> dict[str, Any]:
    if not prior:
        return {"baseline": True, "new": [], "removed": []}
    before = {str(item.get("id")) for item in prior.get("tools", [])}
    current = {item["id"] for item in tools}
    return {"baseline": False, "new": sorted(current - before), "removed": sorted(before - current)}


def md_cell(value: Any) -> str:
    return str(value or "—").replace("|", "\\|").replace("\n", " ")


def tool_table(items: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Tool | Version | Stable ID | Source | Location | Installed |",
        "|---|---|---|---|---|---|",
    ]
    for item in items:
        lines.append(
            f"| {md_cell(item['name'])} | {md_cell(item['version'])} | `{md_cell(item['id'])}` | "
            f"{md_cell(item['source'])} | {md_cell(item['path'])} | {md_cell(item['installed'])} |"
        )
    return lines


def telemetry_table(items: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Channel | Host application | Component/provider | State | Approved | Evidence | Opt-out |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in items:
        source = f"[vendor documentation]({item['source_url']})" if item.get("source_url") else "research needed"
        lines.append(
            f"| `{md_cell(item['id'])}` | {md_cell(item['host'])} | {md_cell(item['component'])} | "
            f"{md_cell(item['state'])} ({md_cell(item['confidence'])} confidence) | "
            f"{'yes' if item.get('approved') else 'no'} | {md_cell(item['evidence'])} | "
            f"{md_cell(item['opt_out'])}; {source} |"
        )
    return lines


def render_report(snapshot: dict[str, Any]) -> str:
    telemetry = snapshot["telemetry"]
    enabled_unapproved = [item for item in telemetry if item["state"] == "enabled" and not item["approved"]]
    unknown = [item for item in telemetry if item["state"] == "unknown"]
    approved = [item for item in telemetry if item["state"] == "enabled" and item["approved"]]
    inactive = [item for item in telemetry if item["state"] in {"disabled", "not configured"}]
    lines = [
        f"# Tool inventory — {snapshot['device']['name']}", "",
        f"Last audited: {snapshot['generated_at']}", "",
        f"Optional tools found: **{len(snapshot['tools'])}**  ",
        f"Enabled telemetry without explicit approval: **{len(enabled_unapproved)}**  ",
        f"Telemetry states needing research: **{len(unknown)}**", "",
        "## Attention: enabled telemetry without explicit approval", "",
    ]
    lines.extend(telemetry_table(enabled_unapproved) if enabled_unapproved else ["None found."])
    lines.extend(["", "## Telemetry needing review", ""])
    lines.extend(telemetry_table(unknown) if unknown else ["None found."])
    lines.extend(["", "## Enabled telemetry explicitly approved", ""])
    lines.extend(telemetry_table(approved) if approved else ["None recorded."])
    lines.extend(["", "## Disabled or not-configured telemetry", ""])
    lines.extend(telemetry_table(inactive) if inactive else ["None found."])
    lines.extend(["", "## Changes since the previous audit", ""])
    changes = snapshot["changes"]
    if changes["baseline"]:
        lines.append("Baseline created; future audits will identify additions and removals.")
    else:
        lines.append(f"New: {', '.join(f'`{item}`' for item in changes['new']) or 'none'}")
        lines.append("")
        lines.append(f"No longer found: {', '.join(f'`{item}`' for item in changes['removed']) or 'none'}")
    lines.extend(["", "## Installed optional tools", ""])
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in snapshot["tools"]:
        grouped[item["category"]].append(item)
    for category in sorted(grouped):
        lines.extend([f"### {category}", ""])
        lines.extend(tool_table(sorted(grouped[category], key=lambda item: item["name"].casefold())))
        lines.append("")
    comparison = snapshot["comparison"]
    lines.extend(["## Cross-device gaps", ""])
    if not snapshot["compared_devices"]:
        lines.append("No other device snapshots exist yet.")
    else:
        lines.append(f"Compared with: {', '.join(snapshot['compared_devices'])}.")
        sections = (
            ("Missing here", comparison["missing_here"]),
            ("Only here", comparison["only_here"]),
            ("Version drift", comparison["version_drift"]),
            ("Telemetry-policy drift", comparison["telemetry_policy_drift"]),
        )
        for title, items in sections:
            lines.extend(["", f"### {title}", ""])
            if not items:
                lines.append("None.")
                continue
            if title == "Missing here":
                lines.extend(f"- `{item['id']}` — present on {', '.join(item['devices'])}" for item in items)
            elif title == "Only here":
                lines.extend(f"- `{item}`" for item in items)
            else:
                for item in items:
                    other = ", ".join(f"{device}: {value}" for device, value in sorted(item["elsewhere"].items()))
                    lines.append(f"- `{item['id']}` — here: {item['here']}; {other}")
    lines.extend(["", "## Coverage and limitations", ""])
    lines.append("Covered: application bundles, selected package managers and global tool registries, editor extensions, Codex plugins/personal skills, and non-Apple background launch items available to this account.")
    lines.append("")
    lines.append("Excluded by default: operating-system base components, transitive project dependencies, opaque contents of application bundles, and managers not named below.")
    lines.extend(["", "### Collection failures", ""])
    lines.extend(f"- {failure}" for failure in snapshot["failures"])
    if not snapshot["failures"]:
        lines.append("None.")
    lines.extend(["", "_Inventory differences and telemetry findings are review cues, not authorization to install, uninstall, or change settings._", ""])
    return "\n".join(lines)


def audit(args: argparse.Namespace) -> int:
    display_name = device_name()
    device_slug = slug(display_name)
    output_root = Path(args.output_root).expanduser()
    device_dir = output_root / device_slug
    snapshot_path = device_dir / "inventory.json"
    prior = load_json(snapshot_path)
    approvals_path = device_dir / "telemetry-approvals.toml"
    approvals = parse_approvals(approvals_path)
    failures: list[str] = []
    tools: dict[str, dict[str, Any]] = {}
    collect_apps(tools, failures)
    collect_managers(tools, failures)
    collect_mas(tools, failures)
    collect_codex(tools)
    collect_launch_items(tools, failures)
    telemetry = collect_telemetry(tools, failures, find_ort_artifacts())
    for item in telemetry:
        record = approvals.get(item["id"], {})
        item["approved"] = bool(record.get("approved"))
        item["approval"] = record
    tool_list = sorted(tools.values(), key=lambda item: (item["category"], item["name"].casefold()))
    other = load_snapshots(output_root, device_slug)
    snapshot = {
        "schema_version": 1,
        "generated_at": now().isoformat(timespec="seconds"),
        "device": {"name": display_name, "slug": device_slug, "platform": platform.platform()},
        "tools": tool_list,
        "telemetry": telemetry,
        "changes": changes_since(prior, tool_list),
        "compared_devices": sorted(other),
        "comparison": compare_devices(tool_list, telemetry, other),
        "failures": failures,
    }
    report = render_report(snapshot)
    if args.dry_run:
        print(report)
        return 0
    device_dir.mkdir(parents=True, exist_ok=True)
    if not approvals_path.exists():
        write_approvals(approvals_path, {})
    report_path = device_dir / f"{device_slug}.md"
    atomic_write(report_path, report)
    atomic_write(snapshot_path, json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    print(report_path)
    return 0


def change_approval(args: argparse.Namespace, approved: bool) -> int:
    display_name = device_name()
    path = Path(args.output_root).expanduser() / slug(display_name) / "telemetry-approvals.toml"
    approvals = parse_approvals(path)
    stamp = now().isoformat(timespec="seconds")
    if approved:
        approvals[args.tool_id] = {
            "tool_id": args.tool_id, "approved": True,
            "approved_at": stamp, "reason": args.reason,
        }
    else:
        record = approvals.get(args.tool_id, {"tool_id": args.tool_id, "approved_at": stamp, "reason": ""})
        record.update({
            "approved": False, "revoked_at": stamp, "revocation_reason": args.reason,
        })
        approvals[args.tool_id] = record
    write_approvals(path, approvals)
    print(path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit_parser = subparsers.add_parser("audit", help="Inventory this device and compare snapshots")
    audit_parser.add_argument("--dry-run", action="store_true")
    approve_parser = subparsers.add_parser("approve", help="Record Nick's explicit telemetry approval")
    approve_parser.add_argument("--tool-id", required=True)
    approve_parser.add_argument("--reason", required=True)
    revoke_parser = subparsers.add_parser("revoke", help="Revoke a telemetry approval")
    revoke_parser.add_argument("--tool-id", required=True)
    revoke_parser.add_argument("--reason", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "audit":
        return audit(args)
    return change_approval(args, approved=args.command == "approve")


if __name__ == "__main__":
    raise SystemExit(main())
