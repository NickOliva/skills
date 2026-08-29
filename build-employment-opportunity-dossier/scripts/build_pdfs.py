#!/usr/bin/env python3
"""Build numbered opportunity-dossier Markdown files with Pandoc/Eisvogel."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SOURCE_PATTERN = re.compile(r"^\d{2} .+\.md$")
ENGINE_ORDER = ("tectonic", "xelatex", "lualatex", "pdflatex")
FONT_ORDER = (
    "Avenir Next",
    "Helvetica Neue",
    "Helvetica",
    "Arial",
    "Noto Sans",
    "DejaVu Sans",
    "Liberation Sans",
)


def executable(name: str) -> str | None:
    override = os.environ.get(f"OPPORTUNITY_DOSSIER_{name.upper()}")
    if override:
        path = Path(override).expanduser()
        if not path.is_file():
            raise SystemExit(f"Configured executable does not exist: {path}")
        return str(path)
    return shutil.which(name)


def choose_engine(requested: str | None) -> str:
    if requested:
        result = executable(requested)
        if not result:
            raise SystemExit(f"Requested PDF engine is not available: {requested}")
        return result
    for name in ENGINE_ORDER:
        if result := executable(name):
            return result
    raise SystemExit(
        "No supported TeX engine found. Install Tectonic, XeLaTeX, LuaLaTeX, "
        "or pdfLaTeX."
    )


def choose_mainfont() -> str:
    override = os.environ.get("OPPORTUNITY_DOSSIER_MAINFONT")
    if override:
        return override

    fc_list = shutil.which("fc-list")
    if fc_list:
        result = subprocess.run(
            [fc_list, ":", "family"], capture_output=True, text=True, check=False
        )
        families = result.stdout.casefold()
        for candidate in FONT_ORDER:
            if candidate.casefold() in families:
                return candidate

    # Latin Modern ships with ordinary TeX installations and is a safe fallback.
    return "Latin Modern Roman"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dossier", type=Path, help="Folder containing numbered Markdown files")
    parser.add_argument("--engine", choices=ENGINE_ORDER)
    parser.add_argument("--pandoc", help="Path to pandoc")
    args = parser.parse_args()

    dossier = args.dossier.expanduser().resolve()
    if not dossier.is_dir():
        raise SystemExit(f"Dossier folder does not exist: {dossier}")

    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "eisvogel"
    template = template_dir / "eisvogel.latex"
    if not template.is_file():
        raise SystemExit(f"Vendored Eisvogel template is missing: {template}")

    pandoc = args.pandoc or executable("pandoc")
    if not pandoc:
        raise SystemExit("pandoc is not available on PATH")
    engine = choose_engine(args.engine)
    mainfont = choose_mainfont()
    build_env = os.environ.copy()
    if Path(engine).name == "tectonic":
        cache = Path(
            os.environ.get(
                "OPPORTUNITY_DOSSIER_TECTONIC_CACHE",
                str(Path(tempfile.gettempdir()) / "opportunity-dossier-tectonic-cache"),
            )
        ).expanduser()
        cache.mkdir(parents=True, exist_ok=True)
        build_env["XDG_CACHE_HOME"] = str(cache)

    sources = sorted(p for p in dossier.iterdir() if p.is_file() and SOURCE_PATTERN.match(p.name))
    if not sources:
        raise SystemExit(f"No numbered Markdown sources found in {dossier}")

    failures: list[str] = []
    for source in sources:
        output = source.with_suffix(".pdf")
        command = [
            pandoc,
            str(source),
            "--from=markdown+smart",
            "--standalone",
            f"--template={template}",
            f"--pdf-engine={engine}",
            f"--variable=mainfont:{mainfont}",
            f"--resource-path={dossier}{os.pathsep}{template_dir}",
            f"--output={output}",
        ]
        print(f"Building {output.name}")
        result = subprocess.run(command, cwd=dossier, env=build_env, text=True)
        if result.returncode:
            failures.append(source.name)

    if failures:
        print("Failed: " + ", ".join(failures), file=sys.stderr)
        return 1

    print(f"Built {len(sources)} PDF(s) in {dossier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
