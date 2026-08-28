# Refactor Notes: Path-Based Ignore Semantics

## Context

The current ignore system matches exact names against path components (basenames) rather than full paths. This applies across the generator and watcher logic, so excluding the output file is done by adding its basename. That creates a known limitation when the output file name appears elsewhere in the tree.

## Motivation

A proposed change would allow ignores to target exact relative paths (e.g., "docs/structure.md") instead of only basenames. This would make it possible to exclude only the concrete output file under the root, without suppressing other files sharing the same name.

## Scope of the Change

This is a behavior change that affects core ignore semantics. It requires coordinated updates across:

- The ignore matching function in `projtree/ignore.py`
- The tree generator in `projtree/generator.py`
- Watcher ignore handling in `projtree/watcher.py`
- CLI behavior and any documentation describing ignore rules
- Tests that assume basename matching semantics

## High-Level Plan

1. Decide on the new ignore matching rules:
   - Support both basenames and relative paths, or
   - Move entirely to path-based matching
2. Update ignore evaluation to compare the correct form:
   - If path-based, compare against the relative path from root
   - Normalize to POSIX-style strings for consistency
3. Update watcher logic to exclude the output file by relative path only
4. Update documentation in README and architecture docs
5. Update and extend tests for both basename and relative path behavior

## Considerations

- Backward compatibility: basename-only ignores are currently documented
- Mixed mode support (basename + relative path) may be required to avoid breaking existing usage
- Path normalization must be deterministic across platforms
- Decide whether `.projtreeignore` accepts relative paths, basenames, or both

## Suggested Test Additions

- Ignore a file by relative path only and confirm only that file is excluded
- Ensure basename ignores still work if backwards compatibility is kept
- Verify watcher output exclusion does not hide other identically named files

## Status

Deferred: requires a larger refactor beyond incremental fixes.
