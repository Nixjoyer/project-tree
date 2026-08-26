#!/usr/bin/env python3

"""Command-line entry points and orchestration for project tree generation."""

import argparse
import sys
from pathlib import Path

from projtree import __version__
from projtree.generator import generate_markdown_tree
from projtree.ignore import DEFAULT_IGNORES, load_ignore_file
from projtree.watcher import watch_and_generate

DEFAULT_OUTPUT = "structure.md"


def parse_ignore(value: str) -> set[str]:
    """Parse a comma-separated ignore list into normalized exact-name entries."""
    return {item.strip() for item in value.split(",") if item.strip()}


def argparse_main(argv: list[str] | None = None) -> int:
    """Run the CLI workflow and return a process-style exit code."""
    parser = argparse.ArgumentParser(
        prog="projtree",
        description="Generate a deterministic Markdown project tree.",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s: {__version__}",
        help="show installed version and exit",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="root directory of the project (default: current directory)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"change output file name (default: {DEFAULT_OUTPUT})",
    )

    parser.add_argument(
        "--ignore",
        help="comma-separated list of file or directory names to ignore",
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help="watch filesystem and regenerate on structural changes",
    )

    parser.add_argument(
        "--watch-only",
        action="store_true",
        help="watch for changes without initial generation",
    )

    args = parser.parse_args(argv)

    if args.watch_only and not args.watch:
        parser.error("--watch-only requires --watch")

    root_path = Path(args.path).resolve()
    output_path = Path(args.output)

    cli_ignores = parse_ignore(args.ignore) if args.ignore else set()

    ignore: set[str] = set()
    ignore |= DEFAULT_IGNORES
    ignore |= load_ignore_file(root_path)
    ignore |= cli_ignores

    # Exclude output file only when writing under the project root.
    try:
        output_path.resolve().relative_to(root_path)
        ignore.add(output_path.name)
    except ValueError:
        pass

    if args.watch:
        watch_and_generate(
            root_path=root_path,
            output_path=output_path,
            debounce_seconds=0.4,
            initial_generate=not args.watch_only,
            extra_ignores=cli_ignores,
        )
        return 0

    try:
        markdown = generate_markdown_tree(root_path, ignore=ignore)
        output_path.write_text(markdown, encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


def main() -> None:
    """CLI process entrypoint."""
    raise SystemExit(argparse_main())


if __name__ == "__main__":
    main()
