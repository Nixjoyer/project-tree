# Contributing to Project Tree

Thank you for your interest in contributing to Project Tree! This document outlines the guidelines and best practices for contributing code, documentation, and improvements to the project.

---

## Table of Contents

<!--toc:start-->
- [Contributing to Project Tree](#contributing-to-project-tree)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Key Reading](#key-reading)
  - [Development Setup](#development-setup)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
    - [3. Install Dependencies](#3-install-dependencies)
    - [4. Verify Installation](#4-verify-installation)
  - [Code Standards](#code-standards)
    - [Structure and Organization](#structure-and-organization)
    - [Python Style](#python-style)
    - [Naming Conventions](#naming-conventions)
    - [Example Function Structure](#example-function-structure)
  - [Testing Guidelines](#testing-guidelines)
    - [Core Principle: Full-Output Assertion](#core-principle-full-output-assertion)
    - [Running Tests](#running-tests)
    - [Test Organization](#test-organization)
    - [Writing Tests](#writing-tests)
    - [Test Philosophy](#test-philosophy)
      - [Note on Ignore System Testing](#note-on-ignore-system-testing)
  - [Making Changes](#making-changes)
    - [Workflow](#workflow)
    - [Types of Changes](#types-of-changes)
      - [Bug Fixes](#bug-fixes)
      - [New Features](#new-features)
      - [Documentation](#documentation)
    - [Backwards Compatibility](#backwards-compatibility)
  - [Design Principles](#design-principles)
    - [1. **Correctness Over Features**](#1-correctness-over-features)
    - [2. **Simplicity Over Abstraction**](#2-simplicity-over-abstraction)
    - [3. **Explicit Behavior Over Cleverness**](#3-explicit-behavior-over-cleverness)
    - [4. **Testability**](#4-testability)
    - [5. **Separation of Concerns**](#5-separation-of-concerns)
      - [Important: Output File Handling](#important-output-file-handling)
    - [6. **Platform Independence**](#6-platform-independence)
  - [Pull Request Process](#pull-request-process)
    - [Before Submitting](#before-submitting)
    - [PR Description](#pr-description)
    - [Review Process](#review-process)
    - [After Merge](#after-merge)
  - [Common Tasks](#common-tasks)
    - [Adding a New CLI Flag](#adding-a-new-cli-flag)
    - [Adding a Test](#adding-a-test)
    - [Debugging](#debugging)
  - [Getting Help](#getting-help)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
<!--toc:end-->

---

## Getting Started

### Prerequisites

- **Python 3.10+** (as specified in `pyproject.toml`)
- **Git** for version control
- **UV** (recommended) or pip/venv for dependency management

### Key Reading

Before contributing, familiarize yourself with:

- [Architecture Document](docs/architecture.md) – Comprehensive design overview
- [README.md](README.md) – Project purpose
- [usage.md](docs/usage.md) – Usage instructions
- [pyproject.toml](pyproject.toml) – Project metadata and dependencies

---

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nuxview/Project-Tree.git
cd Project-Tree
```

### 2. Create a Virtual Environment

Using **UV** (recommended):

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Using **venv**:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

Install the package in editable mode with dev dependencies:

```bash
uv pip install -e ".[dev]"
# Or with pip:
pip install -e ".[dev]"
```

This installs:

- `projtree` itself (editable)
- `watchdog>=5.0.0` (core dependency)
- `pytest` (for testing)

### 4. Verify Installation

Run the test suite to confirm everything is set up correctly:

```bash
pytest
```

---

## Code Standards

### Structure and Organization

Project Tree follows a **separation of concerns** principle across four layers:

| Layer | Module | Responsibility |
| ------- | -------- | ----------------- |
| **CLI** | `cli.py` | Argument parsing and orchestration |
| **Generation** | `generator.py` | Read-only, deterministic tree generation |
| **Ignore System** | `ignore.py` | Ignore rule resolution |
| **Watcher** | `watcher.py` | Optional filesystem monitoring |

When adding features, place code in the appropriate module.

### Python Style

- **Language Version**: Python 3.10+ features are acceptable (e.g., type unions with `|`, match statements)
- **Type Hints**: All functions must include type hints for parameters and return values
  - Prefer modern syntax: `set[str]`, `dict[str, int]`, `str | None` (3.10+)
  - Note: `generator.py` uses older style (`Optional[Set[str]]`) for historical reasons, but new code should use modern style
- **Docstrings**: Use docstrings for all public functions and classes:

  ```python
  def load_ignore_file(root: Path) -> set[str]:
      """
      Load ignore entries from a .projtreeignore file in the root directory.

      :param root: Root directory containing .projtreeignore
      :return: Set of ignore rules
      """
   ```

- **Line Length**: Keep lines reasonably sized; aim for readability
- **Imports**:
  - Group imports: standard library, third-party, local
  - Avoid wildcard imports (`from x import *`)
  - Use `from pathlib import Path` for filesystem operations (not `os`)
  - Prefer modern syntax; avoid `typing` module imports when using Python 3.10+ built-in generics

### Naming Conventions

- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private members: prefix with `_` (e.g., `_internal_helper()`)
- Test functions: `test_<what_is_being_tested>` (e.g., `test_single_file`)

### Example Function Structure

```python
from pathlib import Path


def parse_ignore(value: str) -> set[str]:
    """Parse comma-separated ignore rules into a set."""
    return {item.strip() for item in value.split(",") if item.strip()}
```

---

## Testing Guidelines

### Core Principle: Full-Output Assertion

All tests validating tree generation **must assert the complete output**, not fragments:

```python
# GOOD: Assert complete output
expected = (
    "# Project Structure\n\n"
    "## Generated by projtree\n\n"
    "```text\n"
    ".\n"
    "└── src\n"
    "    └── main.py\n"
    "```\n"
)
assert result == expected

# AVOID: Partial assertions
assert "main.py" in result  # Not enough; can miss formatting errors
```

This practice ensures:

- Ordering remains deterministic
- Formatting regressions are immediately visible
- No unintended content creeps into output

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_basic_tree.py

# Run with verbose output
pytest -v

# Run with coverage (if installed)
pytest --cov=projtree
```

### Test Organization

- **`test_basic_tree.py`** – Pure generation logic (determinism, output format, ignore behavior)
- **`test_cli.py`** – CLI argument parsing and orchestration
- **`test_watcher_basic.py`** – Minimal watcher integration tests
- **`utils.py`** – Shared test helpers (e.g., `touch()` for file creation)

### Writing Tests

Use `tmp_path` fixture from pytest for isolated temporary directories:

```python
def test_single_file(tmp_path: Path):
    # Create test structure
    (tmp_path / "README.md").write_text("", encoding="utf-8")

    # Run generator
    result = generate_markdown_tree(tmp_path)

    # Assert complete output
    expected = (
        "# Project Structure\n\n"
        "## Generated by projtree\n\n"
        "```text\n"
        ".\n"
        "└── README.md\n"
        "```\n"
    )
    assert result == expected
```

### Test Philosophy

- **Deterministic, read-only logic is tested exhaustively** (generator, ignore resolution)
- **Side effects are tested minimally** (watcher, filesystem I/O)
- **No mocks for deterministic functions** – call them directly
- **Avoid flaky timing-dependent tests** – use deterministic assertions

#### Note on Ignore System Testing

When testing ignore behavior, remember that ignore rules match against any **path component (segment)** of the relative path (operates only on names):

- Ignoring `"src"` prevents traversal of any directory or file named `src` at any depth
- This applies uniformly across nested levels (top-level `src/` and nested paths containing `src`)
- See [architecture.md Section 6.4](docs/architecture.md#64-matching-rules) for detailed matching rules

---

## Making Changes

### Workflow

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code standards outlined above
   - Keep commits atomic and descriptive
   - Update tests alongside implementation

3. **Test thoroughly**

   ```bash
   pytest -v
   ```

4. **Update documentation**
   - If behavior changes, update [architecture.md](docs/architecture.md)
   - If CLI changes, update help text and [README.md](README.md)
   - Add docstrings to new functions

5. **Commit with clear messages**

   ```bash
   git commit -m "feat: add support for custom ignore patterns"
   git commit -m "test: add unit tests for pattern matching"
   ```

### Types of Changes

#### Bug Fixes

- Include a test that reproduces the bug
- Fix the issue
- Ensure the test now passes
- Update [architecture.md](docs/architecture.md) if behavior changes

#### New Features

- Ensure the feature aligns with Project Tree's **minimalist philosophy** (see [Design Principles](#design-principles))
- Add comprehensive tests with full-output assertions
- Update [architecture.md](docs/architecture.md) with design details
- Update [README.md](README.md) with usage examples

#### Documentation

- Fix typos and clarify language
- Ensure links are valid
- Keep architecture docs in sync with code

### Backwards Compatibility

Project Tree is currently in v1.x. Maintain backwards compatibility with:

- Existing CLI interface (no breaking changes to arguments)
- Output format (changes require semver bump)
- `.projtreeignore` file format

Breaking changes require explicit discussion and semver versioning.

---

## Design Principles

Project Tree v1 prioritizes:

### 1. **Correctness Over Features**

- Stable, predictable output takes precedence
- Deferred features are listed in [architecture.md](docs/architecture.md#10-deferred-features)
- When unsure, omit rather than add complexity

### 2. **Simplicity Over Abstraction**

- Code should be readable in isolation
- Avoid unnecessary abstractions
- Each function should have a single, clear responsibility

### 3. **Explicit Behavior Over Cleverness**

- No implicit magic or hidden defaults
- Clear documentation for edge cases
- Deterministic output under all conditions

### 4. **Testability**

- Deterministic functions (no hidden state)
- No mocking required for core logic
- Tests serve as live documentation

### 5. **Separation of Concerns**

Adhere to the **four-layer architecture**:

- **CLI** handles only argument parsing, ignore aggregation, and orchestration
- **Generator** handles only tree generation (read-only, deterministic path traversal and ignore filtering)
- **Ignore** handles only ignore rule resolution and matching logic
- **Watcher** handles only filesystem monitoring and regeneration triggering

Code that spans layers should be refactored.

#### Important: Output File Handling

The output file (default `structure.md`) is handled at the **orchestration layer**, not in the generator:

- **CLI**: Resolves output path and passes it to the generator
- **Watcher**: Adds output filename to ignore set to prevent watching it
- **Generator**: Remains pure and unaware of the output file

This ensures the generator stays testable and deterministic.

### 6. **Platform Independence**

- Use `pathlib.Path` for filesystem operations (not `os`)
- Test behavior on Linux, macOS, and Windows
- Avoid platform-specific hacks

---

## Pull Request Process

### Before Submitting

- [ ] Tests pass: `pytest -v`
- [ ] Code follows style guidelines (type hints, docstrings)
- [ ] Commits are atomic and descriptive
- [ ] Documentation is updated ([architecture.md](docs/architecture.md), [README.md](README.md))
- [ ] No unrelated changes included

### PR Description

Use this template:

```markdown
## Summary
Brief description of the change.

## Type
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactor

## Changes
- List specific changes
- Include reasoning for design decisions

## Testing
- Describe how changes were tested
- Include any edge cases considered

## Related Issues
Closes #123
```

### Review Process

1. Request review from maintainers
2. Address feedback promptly
3. Update PR description if scope changes
4. Ensure CI/CD passes (when applicable)

### After Merge

- Celebrate!
- Your contribution is now part of Project Tree

---

## Common Tasks

### Adding a New CLI Flag

1. Add argument to `argparse` in `cli.py`
2. Pass parameter to generation/watcher functions
3. Add tests in `test_cli.py`
4. Update [README.md](README.md) with usage example
5. Update [architecture.md](docs/architecture.md) CLI section

### Adding a Test

1. Open `tests/test_basic_tree.py` (or appropriate test file)
2. Create a test function: `def test_<feature>(tmp_path: Path):`
3. Use `tmp_path` fixture to create isolated test data
4. Assert complete output (not fragments)
5. Run: `pytest tests/test_basic_tree.py::test_<feature> -v`

### Debugging

```bash
# Run tests with printing
pytest -v -s

# Run single test
pytest tests/test_basic_tree.py::test_single_file -v

# Interactive debugging
python -c "from projtree.generator import generate_markdown_tree; print(generate_markdown_tree('.'))"
```

---

## Getting Help

- **Questions**: Open an issue with the `question` label
- **Bugs**: Open an issue with detailed reproduction steps
- **Features**: Discuss in an issue before submitting a PR
- **Code Review**: Ask for clarification in PR comments

---

## License

By contributing, you agree that your contributions will be licensed under the same license as Project Tree (see [LICENSE](LICENSE)).

---

## Acknowledgments

Thank you for helping make Project Tree better! This project thrives on community contributions and feedback.
