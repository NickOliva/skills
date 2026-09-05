#!/usr/bin/env python3
"""Read-only Nick Skills installation audit; requirements are the scope authority."""
import argparse
import json
import os
from pathlib import Path
import re


def frontmatter(path):
    """Read this repo's scalar declaration fields without a YAML dependency."""
    text = path.read_text()
    if not text.startswith('---\n') or '\n---' not in text[4:]:
        return {}
    header = text[4:].split('\n---', 1)[0]
    fields = {}
    for line in header.splitlines():
        match = re.fullmatch(r'([a-z_]+):\s*(.*?)\s*', line)
        if match:
            fields[match[1]] = match[2].strip('\"\'')
    return fields


def audit(repo, home, codex_home, external_roots=True):
    repo, home, codex_home = repo.resolve(), home.resolve(), codex_home.resolve()
    roots = {repo / '.agents/skills': 'repo', repo / '.codex/skills': 'repo',
             home / '.agents/skills': 'machine', home / '.codex/skills': 'machine',
             codex_home / 'skills': 'machine'}
    if external_roots:
        roots[Path('/etc/codex/skills')] = 'machine'
    # Parent discovery roots can unintentionally widen a repo-only skill's scope.
    for parent in repo.parents if external_roots else []:
        for kind in ['.agents', '.codex']:
            roots.setdefault(parent / kind / 'skills', 'ancestor')
    installed = []
    gaps = []
    for root, scope in roots.items():
        try:
            entries = list(root.iterdir()) if root.exists() else []
            for entry in entries:
                if entry.name.startswith('.'):
                    continue
                # Existing repositories may link a wrapper directory containing skill/.
                for relative in ['SKILL.md', 'skill/SKILL.md']:
                    file = entry / relative
                    if file.is_file():
                        installed.append((frontmatter(file).get('name'), entry, file.parent, scope))
        except (OSError, ValueError) as exc:
            gaps.append({'id': 'skill-installations:coverage:' + str(root),
                         'status': 'inspection-blocked', 'reason': str(exc)})
    records = []
    folders = {p.parent for p in repo.glob('*/*requirements.md')}
    folders |= {p.parent.parent for p in repo.glob('*/skill/SKILL.md')}
    for folder in sorted(folders):
        declarations = list(folder.glob('*requirements.md'))
        source = folder / 'skill'
        source_file = source / 'SKILL.md'
        name = frontmatter(source_file).get('name', folder.name) if source_file.is_file() else folder.name
        record = {'id': 'skill-installations:' + name, 'name': name, 'issues': []}
        issues = record['issues']
        if len(declarations) != 1:
            record.update(status='review-installation-declaration', reason='Need one requirements declaration.')
            records.append(record)
            continue
        declared = frontmatter(declarations[0])
        scope, raw = declared.get('installation_scope'), declared.get('installation_target', '')
        if declared.get('skill_name') != name or scope not in ['machine', 'repo'] or not raw or declared.get('installation_method') != 'symlink':
            record.update(status='review-installation-declaration', reason='Missing, inconsistent, or unsupported installation declaration.')
            records.append(record)
            continue
        if raw.startswith('~/'):
            target = home / raw[2:]
        elif raw.startswith('$CODEX_HOME/'):
            target = codex_home / raw[len('$CODEX_HOME/'):]
        else:
            target = Path(raw) if Path(raw).is_absolute() else repo / raw
        # Do not resolve target itself: it may be the symlink we need to inspect.
        target = Path(os.path.abspath(target))
        allowed = [root for root, kind in roots.items() if kind == scope]
        if target.parent not in allowed:
            issues.append('target-outside-declared-scope')
        record['recorded'] = {'scope': scope, 'target': str(target), 'source': str(source)}
        matches = [(entry, actual, kind) for found, entry, actual, kind in installed if found == name]
        record['observed'] = [{'path': str(entry), 'source': str(actual.resolve()), 'scope': kind}
                              for entry, actual, kind in matches]
        if not source_file.is_file():
            issues.append('source-not-built')
        if not target.exists() and not target.is_symlink():
            if source_file.is_file():
                issues.append('missing-installation')
        elif not target.is_symlink():
            issues.append('not-a-symlink')
        elif not target.exists():
            issues.append('broken-link')
        elif target.resolve() != source.resolve():
            issues.append('wrong-link-target')
        if len(matches) > 1:
            issues.append('duplicate-installation')
        for entry, actual, kind in matches:
            if kind != scope:
                issues.append('wrong-scope')
            if entry != target:
                issues.append('unexpected-installation-location')
        record['issues'] = sorted(set(issues))
        record['status'] = ('source-not-built' if record['issues'] == ['source-not-built'] else
                            'review-installation-difference' if issues else 'matches-recorded-value')
        records.append(record)
    return records + gaps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--codex-home', type=Path)
    args = parser.parse_args()
    codex_home = args.codex_home or Path(os.environ.get('CODEX_HOME', str(args.home / '.codex')))
    records = audit(args.repo, args.home, codex_home)
    print(json.dumps({'mode': 'read-only', 'items': records}, indent=2))
    return 1 if any(r['status'] == 'inspection-blocked' for r in records) else 0


if __name__ == '__main__':
    raise SystemExit(main())
