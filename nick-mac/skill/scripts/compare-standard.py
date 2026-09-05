#!/usr/bin/env python3
"""Read-only comparison of recorded build items with local persisted settings."""

import argparse
import hashlib
import json
import plistlib
import subprocess
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
ABSENT = {"state": "unset"}


def normalized(value):
    if isinstance(value, bytes):
        try:
            return {"plist_data_json": json.loads(value)}
        except (ValueError, UnicodeDecodeError):
            return {"data_sha256": hashlib.sha256(value).hexdigest()}
    if isinstance(value, dict):
        return {key: normalized(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalized(item) for item in value]
    return value


def preference_items(component, spec, actual):
    """An absent override is not proof of equivalent effective defaults."""
    domain = spec["domain"]
    records = []

    def compare(key, expected, observed):
        if (isinstance(expected, dict) and isinstance(observed, dict)
                and "plist_data_json" not in expected
                and "state" not in expected and "state" not in observed):
            for child in sorted(expected.keys() | observed.keys()):
                compare(f"{key}/{child}", expected.get(child, ABSENT), observed.get(child, ABSENT))
            return
        records.append({
            "id": f"{component}:{domain}:{key}",
            "status": "matches-recorded-value" if expected == observed else "review-difference",
            "recorded": expected,
            "observed": observed,
        })

    for key, value in spec.get("set_preferences", {}).items():
        compare(key, value, normalized(actual[key]) if key in actual else ABSENT)
    for key in spec.get("review_unset_preferences", []):
        records.append({
            "id": f"{component}:{domain}:{key}",
            "status": "check-effective-setting" if key not in actual else "review-unrecorded-setting",
            "recorded": {"state": "effective-setting-needs-review"},
            "observed": normalized(actual[key]) if key in actual else ABSENT,
        })
    return records


def read_domain(domain, preferences_dir=None):
    if preferences_dir is not None:
        path = preferences_dir / f"{domain}.plist"
        return plistlib.loads(path.read_bytes()) if path.exists() else {}
    # Export consults the preferences service without changing the domain.
    result = subprocess.run(["/usr/bin/defaults", "export", domain, "-"], capture_output=True)
    if result.returncode:
        path = Path.home() / "Library/Preferences" / f"{domain}.plist"
        if not path.exists() and b"does not exist" in result.stderr:
            return {}
        raise RuntimeError(f"Could not read preference domain {domain}; inspect it directly.")
    return plistlib.loads(result.stdout)


def application_ids(applications):
    """Identify bundles without retaining release/build metadata."""
    found = set()
    for directory in applications:
        for path in directory.glob("*.app/Contents/Info.plist"):
            info = plistlib.loads(path.read_bytes())
            if info.get("CFBundleIdentifier"):
                found.add(info["CFBundleIdentifier"])
    return found


def collect(component, standard, read, applications, support):
    component_id = component["id"]
    records = []
    if component_id == "finder":
        for spec in standard["domains"]:
            records.extend(preference_items(component_id, spec, read(spec["domain"])))
        records.append({"id": "finder:control:services-and-workflows", "status": "check-in-app",
                        "recorded": standard["workflow_assets"],
                        "note": "Inspect workflow contents, native services, and candidate workflows individually."})
    elif component_id == "terminal":
        actual = read(standard["domain"])
        records.extend(preference_items(component_id, standard, actual))
        asset_dir = (SKILL / component["standard"]).parent
        for name, filename in standard["profiles"].items():
            profile = plistlib.loads((asset_dir / filename).read_bytes())
            observed = actual.get("Window Settings", {}).get(name, {})
            for key, value in profile.items():
                if key == "ProfileCurrentVersion":  # Native file format metadata.
                    continue
                expected = normalized(value)
                current = normalized(observed[key]) if key in observed else ABSENT
                records.append({"id": f"terminal:profile:{name}:{key}",
                                "status": "matches-recorded-value" if current == expected else "review-difference",
                                "recorded": expected, "observed": current})
        records.append({"id": "terminal:control:shell", "status": "inspect-startup-settings",
                        "recorded": standard["shell"]})
    elif component_id == "voice-transcription":
        app = standard["app"]
        spec = dict(standard, domain=app["bundle_id"])
        records.extend(preference_items(component_id, spec, read(app["bundle_id"])))
        present = app["bundle_id"] in application_ids(applications)
        records.append({"id": "voice-transcription:app:presence",
                        "status": "matches-recorded-value" if present else "review-difference",
                        "recorded": app["bundle_id"], "observed": app["bundle_id"] if present else ABSENT})
        asset_dir = (SKILL / component["standard"]).parent
        expected = json.loads((asset_dir / standard["vocabulary_file"]).read_text())
        target = support / "FluidVoice" / standard["vocabulary_file"]
        observed = json.loads(target.read_text()) if target.exists() else ABSENT
        records.append({"id": "voice-transcription:asset:vocabulary",
                        "status": "matches-recorded-value" if expected == observed else "review-difference",
                        "recorded": expected, "observed": observed})
        for path in standard["required_model_directories"]:
            records.append({"id": f"voice-transcription:model:{Path(path).name}",
                            "status": "verify-model-readiness" if (support / path).is_dir() else "review-missing-model"})
        for key, value in standard["app_controls"].items():
            records.append({"id": f"voice-transcription:control:{key}", "status": "check-in-app", "recorded": value})
        for key, value in standard.get("effective_settings", {}).items():
            records.append({"id": f"voice-transcription:setting:{key}", "status": "check-in-app", "recorded": value})
    elif component_id == "applications":
        installed = application_ids(applications)
        for app in standard["applications"]:
            requirement = app["requirement"]
            present = app["bundle_id"] in installed
            status = ("matches-recorded-value" if present else "review-difference") if requirement == "required" else requirement
            records.append({"id": f"applications:app:{app['id']}", "name": app["name"],
                            "status": status, "recorded": requirement,
                            "observed": "present" if present else "absent"})
            if requirement == "required" and app.get("configuration_status") == "awaiting-review":
                records.append({"id": f"applications:configuration:{app['id']}", "name": app["name"],
                                "status": "configuration-awaiting-review", "review_state": "provisional"})
    elif component_id == "background-items":
        for item in standard["items"]:
            records.append({"id": f"background-items:{item['id']}", "name": item["title"],
                            "status": "inspect-background-item", "recorded": item["standard"],
                            "specification": component["specification"]})
    else:
        records.append({"id": component_id, "status": "use-component-procedure",
                        "specification": component["specification"]})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--component", action="append", help="Manifest component ID; repeat for a subset.")
    parser.add_argument("--all", action="store_true", help="Include values matching the stored baseline.")
    parser.add_argument("--preferences-dir", type=Path, help="Read exported fixture plists instead of live preferences.")
    parser.add_argument("--applications-dir", type=Path, help="Override the application directory for offline inspection.")
    parser.add_argument("--support-dir", type=Path, default=Path.home() / "Library/Application Support")
    args = parser.parse_args()
    manifest = json.loads((SKILL / "manifest.json").read_text())
    components = manifest["components"]
    selected = set(args.component or [c["id"] for c in components])
    unknown = selected - {c["id"] for c in components}
    if unknown:
        parser.error("Unknown components: " + ", ".join(sorted(unknown)))
    applications = [args.applications_dir] if args.applications_dir else [
        Path("/Applications"), Path.home() / "Applications", Path("/System/Applications"),
        Path("/System/Applications/Utilities"), Path("/Applications/Utilities")]
    records = []
    for component in components:
        if component["id"] not in selected:
            continue
        standard = json.loads((SKILL / component["standard"]).read_text())
        try:
            items = collect(component, standard, lambda domain: read_domain(domain, args.preferences_dir), applications, args.support_dir)
            for item in items:
                decision = manifest.get("item_decisions", {}).get(item["id"], {})
                item["review_state"] = decision.get("review_state", item.get("review_state", component["initial_review_state"]))
            records.extend(items)
        except (OSError, ValueError, RuntimeError, plistlib.InvalidFileException) as exc:
            records.append({"id": component["id"], "status": "inspection-blocked", "reason": str(exc)})
    if not args.all:
        records = [r for r in records if r["status"] != "matches-recorded-value"]
    print(json.dumps({"manifest_revision": manifest["revision"], "mode": "read-only", "items": records,
                      "note": "Resolve differences and effective settings before presenting one alignment plan. This helper never applies changes."}, indent=2))
    return 1 if any(r["status"] == "inspection-blocked" for r in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
