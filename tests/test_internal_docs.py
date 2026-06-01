import inspect

import projtree
import projtree.cli as cli
import projtree.generator as generator
import projtree.ignore as ignore
import projtree.watcher as watcher


def test_core_modules_have_docstrings():
    assert inspect.getdoc(projtree)
    assert inspect.getdoc(cli)
    assert inspect.getdoc(generator)
    assert inspect.getdoc(ignore)
    assert inspect.getdoc(watcher)


def test_core_functions_have_docstrings():
    assert inspect.getdoc(cli.parse_ignore)
    assert inspect.getdoc(cli.argparse_main)
    assert inspect.getdoc(cli.main)
    assert inspect.getdoc(generator.generate_markdown_tree)
    assert inspect.getdoc(ignore.load_ignore_file)
    assert inspect.getdoc(ignore.is_ignored)
    assert inspect.getdoc(watcher.watch_and_generate)
