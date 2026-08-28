#!/usr/bin/env python3

"""Ignore loading and matching utilities shared by CLI and watcher flows."""

from pathlib import Path

DEFAULT_IGNORES: set[str] = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".env",
    ".pytest_cache",
    "build",
    "dist",
}


def load_ignore_file(root: Path) -> set[str]:
    """
    Load ignore entries from a .projtreeignore file in the root directory.

    Rules:
    - One name per line
    - Blank lines ignored
    - Lines starting with '#' ignored
    - Exact name matching only
    """
    ignore_file = root / ".projtreeignore"
    ignore: set[str] = set()

    if not ignore_file.exists():
        return ignore

    for line in ignore_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ignore.add(line)

    return ignore


def is_ignored(
    path: Path,
    root: Path,
    *,
    extra_ignores: set[str] | None = None,
    preloaded_ignores: set[str] | None = None,
) -> bool:
    """Check whether path should be omitted using exact-name segment matching."""
    ignores = DEFAULT_IGNORES | (
        load_ignore_file(root) if preloaded_ignores is None else preloaded_ignores
    )

    if extra_ignores:
        ignores |= extra_ignores

    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False

    return any(part in ignores for part in relative.parts)
