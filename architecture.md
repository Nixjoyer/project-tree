# ProjTree v1 Architecture

## 1. Purpose

ProjTree is a small, deterministic utility that generates a Markdown representation of a project’s directory structure. Its primary goals are:

* Produce **stable, predictable output** suitable for documentation and version control
* Respect common project ignore conventions
* Remain **simple, inspectable, and testable**
* Support optional **watch mode** for continuous regeneration

Version 1 (v1) intentionally limits scope to ensure correctness and reliability.

---

## 2. High-Level Overview

ProjTree consists of four core layers:

1. **CLI Layer** – Argument parsing and orchestration
2. **Generation Layer** – Pure logic for building Markdown output
3. **Ignore System** – Centralized ignore resolution
4. **Watcher Layer** – Optional filesystem monitoring

The design principle is **separation of concerns**: generation is pure and testable, while I/O and side effects are isolated.

---

## 3. Directory Structure

The repository layout for ProjTree v1 reflects a deliberately small and explicit codebase. Below is the **actual structure** as generated from the main branch:

```
.
├── projtree
│   ├── __init__.py
│   ├── cli.py
│   ├── generator.py
│   ├── ignore.py
│   └── watcher.py
├── tests
│   ├── test_basic_tree.py
│   ├── test_watcher_basic.py
│   └── utils.py
├── .gitignore
├── .projtreeignore
├── LICENSE
├── pyproject.toml
└── STRUCTURE.md
```

### Directory and File Roles

**`projtree/`** — Core package implementation

* `__init__.py`: Marks the package; contains no runtime logic
* `cli.py`: Command-line interface entry point and argument parsing
* `generator.py`: Pure, deterministic Markdown tree generation logic
* `ignore.py`: Ignore rule resolution (defaults + `.projtreeignore`)
* `watcher.py`: Optional filesystem watching using watchdog

**`tests/`** — Test suite

* `test_basic_tree.py`: Verifies generator output correctness and determinism
* `test_watcher_basic.py`: Minimal integration tests for watch mode
* `utils.py`: Shared helpers for test setup and assertions

**Top-level files**

* `.gitignore`: Git ignore rules for the repository
* `.projtreeignore`: Project-specific ignore rules consumed by ProjTree
* `LICENSE`: Project license
* `pyproject.toml`: Packaging metadata, dependencies, and entry points
* `STRUCTURE.md`: Generated Markdown output (often ignored in other projects)

---

## 4. CLI Layer (`cli.py`)

### Responsibilities

The CLI layer is responsible for all user-facing interaction and orchestration. It translates command-line arguments into well-defined actions without embedding any generation or watcher logic.

Specifically, the CLI:

* Parses and validates command-line arguments
* Resolves filesystem paths
* Aggregates ignore rules from all sources
* Dispatches execution to either one-shot generation or watch mode
* Handles user-facing errors and exit codes

---

### Interface (v1)

The CLI interface in v1 is intentionally compact and stable. The current help output is:

```
usage: projtree [-h] [-o OUTPUT] [--ignore IGNORE] [--watch] [--watch-only]
                [path]

Generate a deterministic Markdown project tree.

positional arguments:
  path                 Root directory of the project (default: current
                       directory)

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output Markdown file (default: STRUCTURE.md)
  --ignore IGNORE      Comma-separated list of file or directory names to
                       ignore
  --watch              Watch filesystem and regenerate on structural changes
  --watch-only         Watch for changes without initial generation
```

---

### Flag Semantics

* **`path`**

  * Root directory to scan
  * Defaults to the current working directory

* **`-o / --output`**

  * Path to the generated Markdown file
  * Defaults to `STRUCTURE.md` in the current directory

* **`--ignore`**

  * Comma-separated list of file or directory *names* to ignore
  * Names are matched exactly (no globbing)
  * Combined with built-in ignores and `.projtreeignore`

* **`--watch`**

  * Enables filesystem watching using watchdog
  * Regenerates output on structural changes

* **`--watch-only`**

  * Requires `--watch`
  * Skips the initial generation
  * Only regenerates after the first detected change

---

### Design Constraints (v1)

* The CLI performs **no filesystem traversal itself**
* All generation logic lives in `generator.py`
* Watch mode is optional and explicitly opt-in
* Invalid flag combinations are rejected early

---

## 5. Generation Layer (`generator.py`)

### Responsibilities

* Traverse the filesystem
* Apply ignore rules
* Produce Markdown output

### Key Characteristics

* **Pure function**: no filesystem writes
* Deterministic ordering
* Output format is strictly defined

### Core API

```python
def generate_markdown_tree(
    root: Path,
    *,
    ignore: set[str] | None = None,
) -> str
```

This function:

* Walks directories top-down
* Sorts entries lexicographically
* Applies ignore filtering by name
* Emits Markdown using a fixed indentation scheme

---

## 6. Ignore System (`ignore.py`)

### 6.1 Purpose and Scope

The Ignore System defines how `projtree` determines which files and directories are excluded from traversal, display, and watcher-triggered regeneration.

Its goals are:

* Deterministic behavior across platforms
* Explicit, predictable resolution order
* Minimal magic: no globbing or implicit pattern expansion in v1
* Consistency between **generation** and **watcher** behavior

The ignore system operates **only on names**, not paths or patterns.

---

### 6.2 Sources of Ignore Rules

Ignore rules may originate from up to three sources, listed here in **strict precedence order (highest first)**:

1. **CLI-provided ignores**
   Passed via `--ignore`, as a comma-separated list of names.
2. **Project ignore file** (`.projtreeignore`)
   Located at the root of the traversal.
3. **Built-in defaults**
   Hardcoded exclusions required for correct operation (e.g., `.git`, output file).

Lower-precedence rules are overridden by higher-precedence rules when conflicts arise.

---

### 6.3 Resolution Order

Ignore resolution proceeds in the following order:

1. Initialize the ignore set with **built-in defaults**
2. Load and merge rules from `.projtreeignore` (if present)
3. Load and merge rules from `--ignore` CLI arguments
4. Freeze the ignore set for the duration of:

   * A single generation run, or
   * A single watcher session

Once frozen, the ignore set **must not change** unless:

* The process restarts, or
* The watcher detects a change to `.projtreeignore` (see Chapter 7)

This guarantees deterministic output for a given input state.

---

### 6.4 Matching Rules

Ignore rules are evaluated using the following rules:

* Matching is done against the **basename** of files and directories
* Matching is **exact**, case-sensitive or case-insensitive depending on the host filesystem
* No globbing, wildcards, regex, or path-based matching is supported in v1

Examples:

* `node_modules` ignores all directories named `node_modules` at any depth
* `__pycache__` ignores all `__pycache__` directories
* `*.log` has **no effect** and is treated as a literal name

This constraint is intentional to preserve simplicity and predictability.

---

### 6.5 Directory vs File Behavior

Ignore rules apply uniformly to:

* Files
* Directories

However, directories have an additional effect:

* If a directory is ignored, **its entire subtree is pruned**
* No traversal, inspection, or watcher registration occurs for that subtree

This ensures both performance and correctness.

---

### 6.6 Output File Handling

The output file (default: `STRUCTURE.md`, or the value of `--output`) is treated specially:

* It is **always ignored**, regardless of user configuration
* This prevents:

  * Self-inclusion in the generated tree
  * Infinite regeneration loops when using `--watch`

This behavior is non-configurable in v1.

---

### 6.7 Edge Cases and Clarifications

#### 6.7.1 Conflicting Rules

If the same name appears in multiple sources:

* The name is ignored if **any source includes it**
* There is no allowlist or negation mechanism in v1

Example:

* `.projtreeignore` ignores `dist`
* CLI does not mention `dist`
* Result: `dist` is ignored

---

#### 6.7.2 Empty or Missing Ignore Files

* A missing `.projtreeignore` is treated as an empty file
* An empty `.projtreeignore` has no effect
* Whitespace-only lines are ignored

---

#### 6.7.3 Duplicate Entries

Duplicate ignore entries:

* Are silently deduplicated
* Do not affect behavior or performance

---

#### 6.7.4 Path-Like Entries

Entries containing path separators (e.g., `src/build`) are treated as literal names and **will not match anything** unless a file or directory with that exact name exists.

This avoids ambiguity and platform-specific behavior.

---

### 6.8 Interaction with the Watcher Layer

The ignore system directly affects the watcher:

* Ignored paths are **never watched**
* Events originating from ignored paths are discarded
* Changes to `.projtreeignore` itself **are always watched**

When `.projtreeignore` changes:

1. The ignore set is recomputed
2. The watcher is reinitialized as needed
3. A regeneration is triggered after debounce

See Chapter 7 for watcher guarantees and non-guarantees.

---

### 6.9 Non-Goals (v1)

The following are explicitly out of scope for v1:

* Glob patterns
* Negation rules (`!`)
* Per-directory ignore files
* Path-based matching
* Git-compatible ignore semantics

These may be considered in future versions but are intentionally excluded to keep v1 minimal and reliable.

---

### 7.0 Core API

```python
def is_ignored(
    path: Path,
    root: Path,
    *,
    extra_ignores: set[str] | None = None,
) -> bool
```

---

## 7. Watcher Layer (`watcher.py`)

### Responsibilities

The watcher layer provides optional, continuous regeneration of the project tree by monitoring filesystem changes. It is intentionally thin and conservative in scope.

Its responsibilities are:

* Observe filesystem events under the project root
* Detect *structural changes*
* Trigger regeneration via the existing generator logic
* Avoid infinite regeneration loops

---

### Definition: Structural Change (v1)

In ProjTree v1, a **structural change** is defined as **any filesystem event that may alter the directory tree**, including:

* Creation of files or directories
* Deletion of files or directories
* Renaming or moving files or directories
* Directory-level metadata changes that may reflect added or removed entries

Importantly:

* The watcher **does not attempt to distinguish** between file-level and directory-level events
* Directory modification events are treated as structural, even if the underlying file event is not observed

This definition is intentionally broad to ensure correctness across platforms and filesystems.

---

### Debounce Behavior

Filesystem operations frequently emit multiple events for a single user action. To prevent excessive regeneration, the watcher applies a **time-based debounce** strategy:

* On the first qualifying event, regeneration is scheduled after a short delay
* Additional events received during the debounce window reset the timer
* Regeneration occurs once no new events have been observed for the duration of the debounce interval

The debounce interval is fixed in v1 and chosen conservatively to balance responsiveness and stability.

---

### Non-Guarantees (Explicit)

The watcher layer in v1 deliberately makes **no guarantees** about:

* Capturing every individual filesystem event
* The ordering or type of events received from the operating system
* Immediate regeneration after a change
* Cross-platform event consistency

Instead, the only guarantee provided is:

> If the filesystem stabilizes after a structural change, the generated output will eventually reflect the new structure.

---

### Loop Prevention

To avoid infinite regeneration loops:

* The output file itself is explicitly ignored by the watcher
* Regeneration is skipped if the newly generated Markdown output is byte-for-byte identical to the existing file

---

### Non-Goals (v1)

The watcher layer does **not** provide:

* Fine-grained event filtering
* One-shot watch semantics
* Incremental or partial regeneration
* Snapshot diffs or change summaries

All advanced watch behavior is deferred to future versions.

---

## 8. Testing Strategy

### 8.1 Objectives

The `projtree` test suite is designed to enforce the following properties:

* Deterministic, stable output for a given filesystem state
* Clear separation between pure logic and side-effecting components
* High signal-to-noise ratio in test failures
* Minimal coupling to platform-specific filesystem behavior

The test suite prioritizes **correctness guarantees** over exhaustive behavioral simulation.

---

### 8.2 Core Principle: Full-Output Assertion

All tests that validate tree generation **must assert against the full output**, not partial fragments.

This rule exists to ensure:

* Ordering is deterministic
* No unintended output is added or removed
* Formatting regressions are immediately detected

Partial assertions (e.g., “contains X”) are explicitly discouraged except when validating error messages or CLI help output.

**Rationale:**
Project tree output is the *primary product* of `projtree`. Any change to it—intentional or accidental—must be visible in tests.

---

### 8.3 Pure Logic vs Side Effects

The test suite distinguishes between:

* **Pure, deterministic logic**
  (e.g., tree generation, ignore resolution)
* **Side-effecting orchestration**
  (e.g., filesystem watching, debounce timing)

Pure logic is tested exhaustively and directly.

Side-effecting components are tested **minimally and indirectly**, with strict boundaries.

---

### 8.4 Watcher Testing Philosophy

Filesystem watchers are inherently:

* Platform-dependent
* Timing-sensitive
* Non-deterministic under load

As a result, watcher tests are intentionally minimal.

Watcher tests exist to verify only:

1. The watcher starts successfully
2. Structural change events trigger regeneration
3. Ignored paths do not trigger regeneration
4. The watcher shuts down cleanly

They do **not** attempt to verify:

* Exact debounce timing
* Event coalescing behavior
* OS-specific event semantics
* High-frequency event storms

These behaviors are delegated to the underlying `watchdog` library and are outside the project’s control.

---

### 8.5 Justification for Minimal Watcher Tests

Attempting to fully simulate watcher behavior would:

* Introduce flaky tests
* Require arbitrary sleeps and timing heuristics
* Reduce confidence rather than increase it
* Obscure genuine regressions with environmental noise

Instead, the test suite treats the watcher as an **integration boundary**, not a unit under exhaustive validation.

This is a deliberate design choice.

---

### 8.6 CLI Testing Rules

CLI tests must:

* Invoke the CLI as a user would
* Assert on complete stdout or stderr output where feasible
* Validate exit codes explicitly

CLI help output is tested separately and may use partial assertions, but only to account for platform-dependent formatting differences.

---

### 8.7 Regression Lock-In

Once behavior is covered by a test:

* Changing that behavior requires updating the test
* Updating the test requires a corresponding documentation change

This enforces alignment between:

* Code
* Tests
* Architecture documentation

Silent behavior changes are treated as regressions, not refactors.

---

### 8.8 Non-Goals

The test suite does not aim to:

* Benchmark performance
* Stress-test filesystem event throughput
* Validate third-party library correctness
* Simulate every possible filesystem edge case

Those concerns are intentionally excluded to preserve test clarity and reliability.

---

### 8.9 Summary

In short:

* **Pure logic is tested strictly**
* **Side effects are tested minimally**
* **Output is asserted in full**
* **Flakiness is treated as a failure of design**

This strategy ensures that `projtree` remains stable, predictable, and maintainable as it evolves.

---

## 9. Design Philosophy

ProjTree v1 prioritizes:

* Correctness over features
* Simplicity over abstraction
* Explicit behavior over cleverness

Every component should be:

* Readable in isolation
* Testable without mocks
* Easy to remove or extend

---

## 10. Deferred Features

The following are intentionally **out of scope** for v1:

* Snapshot/diff engine
* Machine-readable output formats
* Ignore pattern matching
* Incremental regeneration
* Advanced watch semantics

These will be introduced incrementally after v1 stabilization.

---

## 11. Versioning

* v1.x: Stable Markdown generator with watch support
* v2.x (planned): Snapshot model and extensible outputs

---

## 12. Summary

ProjTree v1 is a deliberately minimal, robust foundation. It solves one problem well: generating a clean, deterministic project tree. All future enhancements build on this stable core.
