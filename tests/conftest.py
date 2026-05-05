from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_LIB = REPO_ROOT / "build" / "lib"

# Ensure tests import the in-repo package, not a built or installed copy.
if str(BUILD_LIB) in sys.path:
    sys.path.remove(str(BUILD_LIB))

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
