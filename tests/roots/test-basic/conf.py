"""Sphinx config for functional tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

project = "test-basic"
master_doc = "index"
extensions = ["sphinxcontrib.hexdump"]
exclude_patterns = ["_build"]
