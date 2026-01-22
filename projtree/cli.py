import argparse
import sys
from pathlib import Path

from projtree.generator import generate_markdown_tree
from projtree.ignore import DEFAULT_IGNORES, load_ignore_file
from projtree.watcher import watch_and_generate

DEFAULT_OUTPUT = "structure.md"


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
        help=f"Change output file name(default: {DEFAULT_OUTPUT})",
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

    if args.watch_only and not args.watch:
        parser.error("--watch-only requires --watch")

    root_path = Path(args.path).resolve()
    output_path = Path(args.output)

    # Resolve ignores
    ignore: set[str] = set()
    ignore |= DEFAULT_IGNORES
    ignore |= load_ignore_file(root_path)

    if args.ignore:
        ignore |= parse_ignore(args.ignore)

    if args.watch:
        watch_and_generate(
            root_path=root_path,
            output_path=output_path,
            debounce_seconds=0.4,
            initial_generate=not args.watch_only,
        )
        return 0

    # Non-watch mode
    try:
        markdown = generate_markdown_tree(root_path, ignore=ignore)
        output_path.write_text(markdown, encoding="utf-8")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
