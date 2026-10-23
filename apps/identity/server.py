"""Uvicorn entry for Force Fab Identity on port 8095."""
from __future__ import annotations

import os
from pathlib import Path

from apps.identity.app import create_app

app = create_app(state_dir=os.environ.get("FF_STATE_DIR") or Path(".run") / "identity")
