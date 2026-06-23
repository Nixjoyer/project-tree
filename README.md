# Project Tree

![Last commit](https://img.shields.io/github/last-commit/Nuxview/Project-Tree)
![Repo size](https://img.shields.io/github/repo-size/Nuxview/Project-Tree)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-0B5FFF?logo=opensourceinitiative&logoColor=white)

Project Tree is a small, deterministic utility that generates a Markdown representation of a project’s directory structure. It produces stable, predictable output and optionally watches the filesystem for structural changes. The installed command is `projtree`.

---

## Features

* Generates a **deterministic Markdown project tree**
* Uses a **simple, explicit ignore system** based on exact name matching
* Optional **watch mode** for continuous regeneration
* **Minimal, testable, and robust design**

---

## Installation

If you already have `UV` installed, simply run:

```bash
uv pip install "git+https://github.com/Nuxview/Project-Tree.git"
```

---

## Getting Started

1. Install the package using the steps above.
2. Run `projtree` from your project root to generate `structure.md`.

```bash
projtree
```

## Usage

See the [usage documentation](docs/usage.md) for the full command reference, options, and example output.

---

## Ignore System

* Built-in defaults include common directory and file names (e.g. `.git`, `__pycache__`, `node_modules`)
* A `.projtreeignore` file in the project root is supported
* For normal runs, CLI `--ignore` arguments are merged with project and built-in ignores
* In `--watch` mode, CLI `--ignore` values are also forwarded, so watching uses built-in defaults, `.projtreeignore`, and any CLI-supplied ignores
* Ignore rules match **exact names anywhere in the tree** (e.g., `src` ignores any file/dir named `src` at any depth)
* Ignore entries are treated as exact names, not paths. For example, `target` works, but `src/target` does not match nested paths
* No globbing, wildcards, or pattern-based matching in v1
* If the output file is under the project root, its file name is also added to the ignore set to prevent regeneration loops

Example `.projtreeignore`:

```text
.venv
__pycache__
build
dist
```

---

## Running Tests

If you installed development dependencies:

```bash
pytest
```

All generator tests assert against **full output** to enforce deterministic structure.
Watcher tests are intentionally minimal and validate regeneration behavior only.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
