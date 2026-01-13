import argparse
import sys
from pathlib import Path

from projtree.generator import generate_markdown_tree
from projtree.ignore import DEFAULT_IGNORES, load_ignore_file
from .watcher import watch_and_generate

DEFAULT_OUTPUT = "STRUCTURE.md"


def parse_ignore(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="projtree",
        description="Generate a deterministic Markdown project tree.",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory of the project (default: current directory)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output Markdown file (default: {DEFAULT_OUTPUT})",
    )

    parser.add_argument(
        "--ignore",
        help="Comma-separated list of file or directory names to ignore",
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch filesystem and regenerate on structural changes",
    )

    parser.add_argument(
        "--watch-only",
        action="store_true",
        help="Watch for changes without initial generation",
    )

    args = parser.parse_args(argv)

    root_path = Path(args.path).resolve()
    output_path = Path(args.output)

    if args.watch_only and not args.watch:
        parser.error("--watch-only requires --watch")

    watch_and_generate(
        root_path=Path(args.path),
        output_path=output_path,
        debounce_seconds=0.4,
        initial_generate=not args.watch_only,
    )

    else:
        markdown = generate_markdown_tree(Path(args.path))
        output_path.write_text(markdown, encoding="utf-8")

    # Ignore resolution (ordered)
    ignore: set[str] = set()

    # 1. Built-in defaults
    ignore |= DEFAULT_IGNORES

    # 2. Ignore file
    ignore |= load_ignore_file(root_path)

    # 3. CLI additions
    if args.ignore:
        ignore |= parse_ignore(args.ignore)

    try:
        markdown = generate_markdown_tree(root_path, ignore=ignore)
    except Exception as exc:
        print(f"Error generating tree: {exc}", file=sys.stderr)
        return 2

    try:
        output_path.write_text(markdown, encoding="utf-8")
    except OSError as exc:
        print(f"Error writing output file: {exc}", file=sys.stderr)
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
