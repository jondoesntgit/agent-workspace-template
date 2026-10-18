#!/usr/bin/env python3
"""Render diagrams/<name>.mmd -> figures/<name>.{svg,pdf,png} with the team Mermaid style.

    python scripts/render_diagrams.py            # render all diagrams that changed
    python scripts/render_diagrams.py --all      # force re-render
    python scripts/render_diagrams.py flow       # just diagrams/flow.mmd

Needs Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli@12` (provides `mmdc`), or
Node.js on PATH, in which case `npx @mermaid-js/mermaid-cli` is used. Set
MMDC_PUPPETEER_CONFIG to a puppeteer JSON to reuse an installed Chrome/Edge. Labels are
real SVG text (htmlLabels off) so the SVG stays editable in Inkscape.
Never edit figures/annotated/; that's for humans (see standards/plotting.md).
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE = ROOT / "standards" / "mermaid"
SRC, OUT = ROOT / "diagrams", ROOT / "figures"


def mmdc_cmd() -> list[str]:
    exe = shutil.which("mmdc")
    if exe:
        return [exe]
    npx = shutil.which("npx")
    if npx:
        return [npx, "-y", "@mermaid-js/mermaid-cli@12"]
    sys.exit("Mermaid CLI not found. Install Node.js, then: npm install -g @mermaid-js/mermaid-cli@12")


def render(src: Path, base: list[str]) -> None:
    common = ["-i", str(src), "-c", str(STYLE / "config.json"), "-C", str(STYLE / "style.css"),
              "-b", "white", "-q"]
    # Locked-down machines: point Mermaid at an existing Chrome/Edge instead of a download,
    # e.g. a JSON file containing {"executablePath": "C:/Program Files/.../msedge.exe"}.
    pptr = os.environ.get("MMDC_PUPPETEER_CONFIG")
    if pptr:
        common += ["-p", pptr]
    targets = [
        (OUT / f"{src.stem}.svg", []),
        (OUT / f"{src.stem}.pdf", []),  # mmdc >= 12 fits the page to the diagram
        (OUT / f"{src.stem}.png", ["-s", "3"]),  # ~300 dpi equivalent
    ]
    for out, extra in targets:
        subprocess.run(base + common + ["-o", str(out)] + extra, check=True)
    print(f"[render_diagrams] {src.name} -> figures/{src.stem}.{{svg,pdf,png}}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="diagram names (default: all)")
    ap.add_argument("--all", action="store_true", help="re-render even if outputs are newer")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    sources = [SRC / f"{n}.mmd" for n in args.names] if args.names else sorted(SRC.glob("*.mmd"))
    base = None
    for src in sources:
        if not src.exists():
            print(f"[render_diagrams] missing {src}", file=sys.stderr)
            continue
        png = OUT / f"{src.stem}.png"
        if not args.all and not args.names and png.exists() and png.stat().st_mtime >= src.stat().st_mtime:
            continue  # up to date; don't bump timestamps (that would flag annotations as stale)
        base = base or mmdc_cmd()
        render(src, base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
