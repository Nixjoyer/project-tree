from pathlib import Path


DEFAULT_IGNORES: set[str] = {
    ".git",
    ".venv",
    ".virt",
    "__pycache__",
    "node_modules",
    ".env",
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

def is_ignored(path: Path, root: Path) -> bool:
    """
    Return True if the path should be ignored based on:
    - DEFAULT_IGNORES
    - .projtreeignore entries
    """
    ignores = DEFAULT_IGNORES | load_ignore_file(root)

    # Check each path component relative to root
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return False

    return any(part in ignores for part in relative.parts)
