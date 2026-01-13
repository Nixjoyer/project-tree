from pathlib import Path


def touch(path: Path) -> None:
    """
    Create an empty file at the given path, creating parents if needed.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
