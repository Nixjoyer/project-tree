"""Tests ensuring internal documentation coverage."""

import inspect

import projtree
import projtree.cli as cli
import projtree.generator as generator
import projtree.ignore as ignore
import projtree.watcher as watcher
import tests.conftest as test_conftest
import tests.test_basic_tree as test_basic_tree
import tests.test_cli as test_cli
import tests.test_watcher_basic as test_watcher_basic
import tests.utils as test_utils


def test_core_modules_have_docstrings():
    """Ensure core modules carry docstrings."""
    assert inspect.getdoc(projtree)
    assert inspect.getdoc(cli)
    assert inspect.getdoc(generator)
    assert inspect.getdoc(ignore)
    assert inspect.getdoc(watcher)


def test_core_functions_have_docstrings():
    """Ensure core functions carry docstrings."""
    assert inspect.getdoc(cli.parse_ignore)
    assert inspect.getdoc(cli.argparse_main)
    assert inspect.getdoc(cli.main)
    assert inspect.getdoc(generator.generate_markdown_tree)
    assert inspect.getdoc(ignore.load_ignore_file)
    assert inspect.getdoc(ignore.is_ignored)
    assert inspect.getdoc(watcher.watch_and_generate)


def test_test_modules_have_docstrings():
    """Ensure test modules carry docstrings."""
    assert inspect.getdoc(test_basic_tree)
    assert inspect.getdoc(test_cli)
    assert inspect.getdoc(test_watcher_basic)
    assert inspect.getdoc(test_utils)
    assert inspect.getdoc(test_conftest)


def test_test_helpers_have_docstrings():
    """Ensure test helpers carry docstrings."""
    assert inspect.getdoc(test_utils.touch)
