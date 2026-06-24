# Changelog

All notable changes merged to `main` or `master` are recorded here.
Entries are prepended automatically after the header separator when a pull request
meets the workflow's review requirements and is successfully merged to `main` or `master`.

Current automation is based on review state:

1. The pull request is approved by **Nuxview**.
2. No reviewer has an outstanding `CHANGES_REQUESTED` review (a later approval from the same reviewer supersedes it).
3. The pull request is successfully merged to `main` or `master`.

---

## 2026-06-05 19:10:39 UTC — PR #21: Document test suite internals and enforce docstrings

**Author:** @Copilot  
**Merge commit:** `68cf7bc06897b5cae551eacbcd2777ea79b5b0d6`  
**Merged at:** 2026-06-05T19:10:39Z

### Commits

- **`7e69086`** (2026-06-01): Initial plan
- **`44beab4`** (2026-06-01): docs: add internal docstrings across core modules
- **`3fb8772`** (2026-06-02): docs: add test suite docstrings

### Changed Files

  - `projtree/__init__.py` (modified)
  - `projtree/cli.py` (modified)
  - `projtree/generator.py` (modified)
  - `projtree/ignore.py` (modified)
  - `projtree/watcher.py` (modified)
  - `tests/conftest.py` (modified)
  - `tests/test_basic_tree.py` (modified)
  - `tests/test_cli.py` (modified)
  - `tests/test_internal_docs.py` (added)
  - `tests/test_watcher_basic.py` (modified)
  - `tests/utils.py` (modified)

---


## 2026-05-23 20:40:59 UTC — PR #12: feat: add changelog GitHub Action and initial changelog.md

**Author:** @Copilot  
**Merge commit:** `e4a213aa793fc338ce21a88a637b410c65623a6f`  
**Merged at:** 2026-05-23T20:40:59Z

### Commits

- **`59f70dd`** (2026-04-07): feat: add changelog GitHub Action and initial CHANGELOG.md
- **`27ef83a`** (2026-04-07): fix: address code review feedback on changelog workflow
- **`9050b5d`** (2026-05-19): Update .github/workflows/changelog.yml
- **`9374ab6`** (2026-05-19): Update docs/CHANGELOG.md
- **`c06439c`** (2026-05-19): refactor: rename CHANGELOG.md to changelog.md for lowercase consistency
- **`1cd2934`** (2026-05-19): Merge remote-tracking branch 'origin' into pr/copilot-swe-agent/12
- **`9adb051`** (2026-05-22): fix: update changelog workflow to use pull_request_target and improve review decision verification
- **`9c4c2c1`** (2026-05-22): fix: update approval checks in changelog workflow and documentation
- **`7b605eb`** (2026-05-23): fix: escape percentage signs in changelog entry formatting
- **`7ca0279`** (2026-05-23): docs: fix typo and sync changelog.md conditions with workflow
- **`8d87c89`** (2026-05-23): fix: resolve inconsistencies between workflow and changelog.md
- **`d4f6797`** (2026-05-23): docs: align changelog.md wording — 'added' → 'prepended'
- **`e6fa90a`** (2026-05-23): fix: enhance approval check logic and improve push retry mechanism in changelog workflow

### Changed Files

  - `.github/workflows/changelog.yml` (added)
  - `docs/changelog.md` (added)

---


