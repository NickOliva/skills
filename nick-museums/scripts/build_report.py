#!/usr/bin/env python3
"""Build one Nick Museums Markdown report with Pandoc and Eisvogel."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ENGINE_ORDER = (
    "/opt/homebrew/bin/tectonic",
    "tectonic",
    "xelatex",
    "lualatex",
    "pdflatex",
)


def resolve_executable(candidate: str) -> str | None:
    path = Path(candidate).expanduser()
    if path.is_absolute():
        return str(path) if path.is_file() and os.access(path, os.X_OK) else None
    return shutil.which(candidate)


def choose_engine(requested: str | None) -> str:
    if requested:
        resolved = resolve_executable(requested)
        if not resolved:
            raise SystemExit(f"Requested PDF engine is unavailable: {requested}")
        return resolved
    for candidate in ENGINE_ORDER:
        if resolved := resolve_executable(candidate):
            return resolved
    raise SystemExit("No supported TeX engine found (Tectonic, XeLaTeX, LuaLaTeX, or pdfLaTeX).")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Markdown report to build")
    parser.add_argument("--output", type=Path, help="PDF destination; defaults beside source")
    parser.add_argument("--pandoc", help="Pandoc executable override")
    parser.add_argument("--engine", help="TeX engine executable override")
    parser.add_argument(
        "--lua-filter",
        action="append",
        type=Path,
        default=[],
        help="Optional Pandoc Lua filter; may be repeated",
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file() or source.suffix.casefold() != ".md":
        raise SystemExit(f"Markdown source does not exist: {source}")
    output = (args.output or source.with_suffix(".pdf")).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    skill_dir = Path(__file__).resolve().parent.parent
    template_dir = skill_dir / "assets" / "eisvogel"
    template = template_dir / "eisvogel.latex"
    if not template.is_file():
        raise SystemExit(f"Vendored Eisvogel template is missing: {template}")

    pandoc = resolve_executable(args.pandoc or "pandoc")
    if not pandoc:
        raise SystemExit("Pandoc is unavailable.")
    engine = choose_engine(args.engine)

    command = [
        pandoc,
        str(source),
        "--from=markdown+smart",
        "--standalone",
        f"--template={template}",
        f"--pdf-engine={engine}",
        f"--resource-path={source.parent}{os.pathsep}{template_dir}",
        "--variable=colorlinks:true",
        "--variable=mainfont:Avenir Next",
        "--variable=sansfont:Avenir Next",
        "--variable=monofont:Menlo",
        f"--output={output}",
    ]
    for lua_filter in args.lua_filter:
        resolved_filter = lua_filter.expanduser().resolve()
        if not resolved_filter.is_file():
            raise SystemExit(f"Lua filter does not exist: {resolved_filter}")
        command.insert(-1, f"--lua-filter={resolved_filter}")
    result = subprocess.run(command, cwd=source.parent, text=True)
    if result.returncode:
        return result.returncode
    if not output.is_file() or output.stat().st_size == 0:
        print(f"PDF was not created: {output}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
