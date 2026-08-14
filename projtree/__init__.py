#!/usr/bin/env python3

"""Project Tree package metadata."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("project-tree")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
