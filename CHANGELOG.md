# Changelog

All notable changes merged to `main` or `master` are recorded here.
Entries are prepended automatically after the header separator when a pull request is successfully merged to `main` or `master`.

---

## 2026-08-28 07:04:17 UTC — PR #25: Add New Workflows

**Author:** @Nuxview  
**Merge commit:** `8137364d0d2e3934ad117168d87a6473091a4168`  
**Merged at:** 2026-08-28T07:04:17Z

### Commits

- **`3c3d5d9`** (2026-06-25): Add Tests Workflow and Drop Changelog Approvals
- **`bc5c10e`** (2026-06-25): Add linter workflow and trigger tests after lint
- **`4931114`** (2026-06-25): Add linter read permissions and fix tests workflow
- **`71b74cf`** (2026-06-26): Added project urls to `pyproject.toml`
- **`a4288c9`** (2026-06-26): Add unified CI workflow for linting and tests
- **`f5ca1cc`** (2026-06-27): Update Changelog.md to new run conditions
- **`60a7fea`** (2026-07-01): Add automated package publishing workflow
- **`fb470d7`** (2026-07-02): Removed testpypl publication job
- **`2f00cd9`** (2026-07-02): Update workflow name
- **`21b445c`** (2026-07-02): Restricted workflow jobs to merged pulled requests
- **`ce2e57b`** (2026-07-03): Update publishing workflow trigger to pull_request_target
- **`0e247df`** (2026-07-04): Add PR labeler workflow and update author email
- **`00cb61d`** (2026-07-05): Add PyPI connection check to publishing workflow
- **`ff53a00`** (2026-07-06): Update pyproject.toml
- **`0709cf4`** (2026-07-06): Expanded scope to include Issues
- **`85ea272`** (2026-07-06): Added slack webhook test as one of the jobs
- **`1b95c4a`** (2026-07-06): Merge branch 'add-workflows' of github.com:Nuxview/Project-Tree into add-workflows
- **`7bd7fa1`** (2026-07-10): Remove test-slack-webhook job from publishing workflow
- **`ce6c832`** (2026-07-10): Rename `labels.yml` to `labeler.yml`
- **`b564b61`** (2026-07-10): Add GitHub Actions workflow for automated labeling
- **`bbad252`** (2026-07-10): Create simple slack webhook test workflow
- **`0319712`** (2026-07-10): Create simple slack webhook test workflow
- **`c3658be`** (2026-07-10): Create simple slack webhook test workflow
- **`d57860f`** (2026-07-10): Delete temporary slack test workflow after confirming the slack webhook works by sending a Greetings message to my channel
- **`237feaa`** (2026-07-25): Update version detection to use base SHA
- **`76be8af`** (2026-07-25): Add ruff and modernize type hinting
- **`e2aee35`** (2026-07-25): Ignore .ruff_cache in .gitignore
- **`cb8afc4`** (2026-07-25): Fix exception logging in watcher restart loop
- **`7fb146a`** (2026-08-14): refactor: optimize project structure, update dependency configuration, and synchronize CI/CD workflows and documentation
- **`075ce4e`** (2026-08-14): chore: update dependencies, add uv to dev requirements, and upgrade pytest
- **`ff30634`** (2026-08-14): chore: add shebang headers to all source and test files
- **`9c836bb`** (2026-08-26): ci: modernize CI workflow with uv, test matrix, and lint checks
- **`c3918e5`** (2026-08-26): ci: configure PR labeler action and path rules
- **`27a2464`** (2026-08-26): docs(ci): refine changelog generator workflow
- **`bfab55f`** (2026-08-26): ci(publish): refine PyPI publish workflow and version diff logic
- **`5884177`** (2026-08-26): fix(cli): handle specific OSError and UnicodeError during tree generation
- **`01256dc`** (2026-08-26): style: format codebase with ruff
- **`f979153`** (2026-08-26): docs: remove outdated generator type hint note and reformat CHANGELOG documentation
- **`55fe344`** (2026-08-26): Bumped up version to 1.3.1
- **`99f8f3a`** (2026-08-26): ci: add dependency installation step and remove uv from dev dependencies
- **`9a65893`** (2026-08-27): fix: remove unused format specifier from watcher error log message
- **`5726717`** (2026-08-28): Potential fix for pull request finding

### Changed Files

  - `.github/labeler.yml` (added)
  - `.github/workflows/changelog.yml` (modified)
  - `.github/workflows/ci.yml` (added)
  - `.github/workflows/labeler.yml` (added)
  - `.github/workflows/publishing.yml` (added)
  - `.gitignore` (modified)
  - `.projtreeignore` (modified)
  - `CHANGELOG.md` (modified)
  - `CONTRIBUTING.md` (modified)
  - `LICENSE` (modified)
  - `README.md` (modified)
  - `docs/architecture.md` (modified)
  - `docs/refactor.md` (modified)
  - `docs/usage.md` (modified)
  - `projtree/__init__.py` (modified)
  - `projtree/cli.py` (modified)
  - `projtree/generator.py` (modified)
  - `projtree/ignore.py` (modified)
  - `projtree/watcher.py` (modified)
  - `pyproject.toml` (modified)
  - `tests/conftest.py` (modified)
  - `tests/test_basic_tree.py` (modified)
  - `tests/test_cli.py` (modified)
  - `tests/test_internal_docs.py` (modified)
  - `tests/test_watcher_basic.py` (modified)
  - `tests/utils.py` (modified)
  - `uv.lock` (modified)

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
