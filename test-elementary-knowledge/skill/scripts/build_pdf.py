#!/usr/bin/env python3
"""Render Markdown with bundled Eisvogel and optionally require a page count."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def executable(requested: str | None, candidates: tuple[str, ...], label: str) -> str:
    for candidate in (requested,) if requested else candidates:
        expanded = str(Path(candidate).expanduser())
        resolved = shutil.which(expanded)
        if resolved:
            return resolved
    raise SystemExit(f"Missing {label}: {requested or ', '.join(candidates)}")


def count_practice_pages(node: object) -> int:
    if isinstance(node, list):
        return sum(count_practice_pages(item) for item in node)
    if not isinstance(node, dict):
        return 0
    own = 0
    if node.get("t") == "Div":
        own = int("practice-page" in node["c"][0][1])
    return own + sum(count_practice_pages(value) for value in node.values())


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    result = subprocess.run(command, text=True, capture_output=True, **kwargs)
    if result.returncode:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or "Command failed")
    if result.stderr.strip():
        print(result.stderr.strip())
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-pages", type=int)
    parser.add_argument("--font-size", choices=("11pt", "12pt", "14pt"), default="12pt")
    parser.add_argument("--paper", choices=("letter", "a4"), default="letter")
    parser.add_argument("--pandoc")
    parser.add_argument("--engine")
    parser.add_argument("--pdfinfo")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    if args.expected_pages is not None and args.expected_pages < 1:
        parser.error("--expected-pages must be positive")

    source = args.source.expanduser().resolve()
    output = (args.output or source.with_suffix(".pdf")).expanduser().absolute()
    if not source.is_file() or source.suffix.lower() != ".md":
        parser.error(f"Markdown source not found: {source}")
    if output.suffix.lower() != ".pdf" or output.resolve() == source:
        parser.error("Output must be a separate .pdf file")
    if (output.exists() or output.is_symlink()) and not args.replace:
        parser.error(f"Output exists; use --replace only for an intended update: {output}")

    pandoc = executable(args.pandoc, ("pandoc", "/opt/homebrew/bin/pandoc"), "Pandoc")
    engine = executable(
        args.engine,
        ("tectonic", "/opt/homebrew/bin/tectonic", "xelatex", "lualatex",
         "/Library/TeX/texbin/xelatex", "/Library/TeX/texbin/lualatex"),
        "Tectonic, XeLaTeX, or LuaLaTeX",
    )
    pdfinfo = executable(args.pdfinfo, ("pdfinfo",), "Poppler pdfinfo")
    skill = Path(__file__).resolve().parent.parent
    template = skill / "assets/eisvogel/eisvogel.latex"
    layout = skill / "assets/workbook-layout.tex"
    lua_filter = skill / "scripts/workbook-layout.lua"
    for required in (template, layout, lua_filter):
        if not required.is_file():
            parser.error(f"Missing bundled resource: {required}")

    ast = json.loads(run([pandoc, str(source), "--from=markdown", "--to=json"]).stdout)
    authored_pages = count_practice_pages(ast.get("blocks", []))
    if args.expected_pages is not None and authored_pages != args.expected_pages:
        parser.error(f"Expected {args.expected_pages} practice-page blocks; found {authored_pages}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="elementary-pdf-", dir=output.parent) as scratch:
        scratch_path = Path(scratch)
        draft = scratch_path / "rendered.pdf"
        # Load portable TeX fonts by filename; older TeX bundles lack sourcesans.sty.
        font_defaults = scratch_path / "fonts.json"
        font_options = [
            "BoldFont=texgyreheros-bold.otf", "ItalicFont=texgyreheros-italic.otf",
            "BoldItalicFont=texgyreheros-bolditalic.otf",
        ]
        font_defaults.write_text(json.dumps({
            "mainfont": "texgyreheros-regular.otf", "mainfontoptions": font_options,
            "sansfont": "texgyreheros-regular.otf", "sansfontoptions": font_options,
        }), encoding="utf-8")
        env = os.environ.copy()
        if Path(engine).name == "tectonic":
            env.setdefault("TECTONIC_CACHE_DIR", str(Path(tempfile.gettempdir()) / "elementary-tectonic-cache"))
        command = [
            pandoc, str(source), "--from=markdown", "--standalone",
            f"--template={template}", f"--pdf-engine={engine}",
            f"--lua-filter={lua_filter}", f"--include-in-header={layout}",
            f"--metadata-file={font_defaults}",
            "--metadata=titlepage:false", "--metadata=toc:false",
            "--metadata=toc-own-page:false", "--metadata=colorlinks:false",
            "--metadata=disable-header-and-footer:false",
            f"--metadata=fontsize:{args.font_size}", f"--metadata=papersize:{args.paper}",
            "--metadata=geometry:margin=18mm,includehead,includefoot",
            f"--resource-path={source.parent}{os.pathsep}{template.parent}",
            f"--output={draft}",
        ]
        run(command, cwd=source.parent, env=env)
        info = run([pdfinfo, str(draft)], env={**env, "LC_ALL": "C"}).stdout
        match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
        if not match:
            raise SystemExit("Could not verify PDF page count; no output published")
        actual_pages = int(match.group(1))
        if args.expected_pages is not None and actual_pages != args.expected_pages:
            raise SystemExit(
                f"Expected {args.expected_pages} PDF pages; got {actual_pages}. "
                "Rebalance content while preserving writing space; no output published."
            )
        if args.replace:
            os.replace(draft, output)
        else:
            # Hard-link promotion is atomic and cannot overwrite a racing writer.
            os.link(draft, output)
    print(f"Created {output} ({actual_pages} pages); visual and answer checks still required.")


if __name__ == "__main__":
    main()
