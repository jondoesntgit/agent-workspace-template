#!/usr/bin/env python3
"""Flag human-annotated figures that may be stale. Exit code 1 if any are.

    python scripts/check_figures.py

Same check LaTeX runs in \\teamfig (standards/latex/teamtufte.sty), for the
notebook and docs workspaces, or for CI. See standards/plotting.md.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "standards"))
import teamplot  # noqa: E402

msgs = teamplot.check_annotations(ROOT / "figures")
if not msgs:
    print("[check_figures] all annotated figures are up to date")
sys.exit(1 if msgs else 0)
