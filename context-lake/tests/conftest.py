"""Pytest path setup for the lake tests."""
from __future__ import annotations

import sys
from pathlib import Path

LAKE_ROOT = Path(__file__).resolve().parents[1]
if str(LAKE_ROOT) not in sys.path:
    sys.path.insert(0, str(LAKE_ROOT))
