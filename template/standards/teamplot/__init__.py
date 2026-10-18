"""Team plotting helpers: the one place plot styling lives.

    import teamplot
    fig, ax = teamplot.figure("column")          # exactly the LaTeX text width
    ax.plot(t, x)
    teamplot.label(ax, x="Time", x_unit="s", y="Position", y_unit="m")
    teamplot.save(fig, "position_vs_time",
                  settings={"Sample rate": "100 Hz", "Filter": "4th-order Butterworth, 5 Hz"})

Style comes from `matplotlibrc` next to this file. Widths come from
`standards/latex/layout.tex`, the same file the LaTeX template reads.
"""
from __future__ import annotations

import json
import re
import warnings
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

_HERE = Path(__file__).resolve().parent
_RC = _HERE / "matplotlibrc"
_LAYOUT = _HERE.parent / "latex" / "layout.tex"

GOLDEN = 0.618  # default height / width


# ---- Layout ---------------------------------------------------------------------

def _read_layout(path: Path = _LAYOUT) -> dict[str, float]:
    """Parse `\\def\\teamNAME{<x>in}` lines from layout.tex into inches."""
    vals = {m[1]: float(m[2]) for m in re.finditer(r"\\def\\team(\w+)\{([\d.]+)in\}", path.read_text())}
    return {
        "column": vals["textwidth"],
        "margin": vals["marginwidth"],
        "full": vals["textwidth"] + vals["marginsep"] + vals["marginwidth"],
    }


WIDTHS = _read_layout()  # inches: {"column", "margin", "full"}


# ---- Style ----------------------------------------------------------------------

def use() -> None:
    """Apply the team matplotlibrc. Called automatically by figure()."""
    mpl.rc_file(_RC)
    _check_font()


_font_checked = False


def _check_font() -> None:
    global _font_checked
    if _font_checked:
        return
    _font_checked = True
    try:
        font_manager.findfont("Nimbus Sans", fallback_to_default=False)
    except ValueError:
        warnings.warn(
            "Nimbus Sans is not installed; plots will fall back to another sans font and "
            "won't match LaTeX captions. See the README section 'Fonts'.",
            stacklevel=3,
        )


def figure(width: str | float = "column", height: float | None = None,
           aspect: float = GOLDEN, nrows: int = 1, ncols: int = 1, **kwargs):
    """Create a styled figure sized to the LaTeX layout.

    width:  "column" (main text), "margin" (marginfigure), "full" (figure*), or inches.
    height: inches; defaults to width * aspect (scaled by nrows/ncols).
    """
    use()
    w = WIDTHS[width] if isinstance(width, str) else float(width)
    h = height if height is not None else w * aspect * nrows / ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(w, h), **kwargs)
    for ax in (axes.flat if hasattr(axes, "flat") else [axes]):
        offset_spines(ax)
    return fig, axes


# ---- Tufte helpers -----------------------------------------------------------------

def offset_spines(ax, points: float = 4) -> None:
    """Move left/bottom spines outward so they don't collide with data."""
    for side in ("left", "bottom"):
        ax.spines[side].set_position(("outward", points))


def rangeframe(ax, x=None, y=None) -> None:
    """Tufte range frame: spines span only the data range.
    Pass the data arrays, or omit to use the plotted data limits."""
    import numpy as np
    if x is None or y is None:
        xy = np.vstack([l.get_xydata() for l in ax.get_lines()] or [[0, 0]])
        x = xy[:, 0] if x is None else x
        y = xy[:, 1] if y is None else y
    ax.spines["bottom"].set_bounds(np.nanmin(x), np.nanmax(x))
    ax.spines["left"].set_bounds(np.nanmin(y), np.nanmax(y))


def direct_labels(ax, pad: float = 4, spacing: float = 1.25, **text_kw) -> None:
    """Label each line at its right end in its own color (instead of a legend).

    Labels whose ends are close are nudged apart vertically so they don't overlap.
    `spacing` is the minimum gap between label centers, in multiples of the font size.
    """
    import numpy as np
    lines = [l for l in ax.get_lines() if l.get_label() and not l.get_label().startswith("_")]
    if not lines:
        return
    fontsize = text_kw.get("fontsize", mpl.rcParams["legend.fontsize"])
    fontsize = mpl.font_manager.FontProperties(size=fontsize).get_size_in_points()
    ax.figure.draw_without_rendering()  # settle constrained layout before measuring
    # Line end points in display points (1/72 in), so spacing is in typographic units.
    to_pts = 72.0 / ax.figure.dpi
    ends = []
    for l in lines:
        x, y = np.asarray(l.get_xdata(), float), np.asarray(l.get_ydata(), float)
        ok = np.isfinite(x) & np.isfinite(y)
        x, y = x[ok][-1], y[ok][-1]
        ends.append((l, x, y, ax.transData.transform((x, y))[1] * to_pts))
    ends.sort(key=lambda e: e[3])
    # Push labels upward until each is at least `gap` above the previous one, then
    # shift the whole stack down so it stays centered on the original positions.
    gap = spacing * fontsize
    placed = []
    for _, _, _, yp in ends:
        placed.append(max(yp, placed[-1] + gap) if placed else yp)
    shift = (sum(e[3] for e in ends) - sum(placed)) / len(placed)
    for (l, x, y, yp), yp_new in zip(ends, placed):
        ax.annotate(l.get_label(), (x, y), xytext=(pad, yp_new + shift - yp),
                    textcoords="offset points", va="center", color=l.get_color(),
                    annotation_clip=False, **text_kw)


def label(ax, x: str, y: str, x_unit: str | None = None, y_unit: str | None = None) -> None:
    """Label axes as `Name [unit]`. Leave the unit None only for dimensionless quantities."""
    ax.set_xlabel(f"{x} [{x_unit}]" if x_unit else x)
    ax.set_ylabel(f"{y} [{y_unit}]" if y_unit else y)


# ---- Saving + settings capture ----------------------------------------------------

_TEX_ESCAPE = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}"}


def _tex(s: str) -> str:
    return "".join(_TEX_ESCAPE.get(c, c) for c in str(s))


def settings_text(settings: dict) -> str:
    """'Key: value; Key: value' (plain text, for notebook/Markdown captions)."""
    return "; ".join(f"{k}: {v}" for k, v in settings.items())


def save(fig, name: str, settings: dict | None = None, outdir: str | Path = "figures",
         formats=("pdf", "png", "svg")) -> list[Path]:
    """Save figures/<name>.pdf/.png/.svg plus the settings that produced the plot.

    The SVG keeps text as editable text so a human can annotate a copy in
    figures/annotated/ (see standards/plotting.md). Never write into annotated/.

    settings: every parameter needed to reproduce the figure (data source, sample
    rate, filter, fit model, N, seeds, ...). Written to <name>.settings.json and
    <name>.settings.tex (used by \\figsettingsof{<name>} in the caption).
    """
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    paths = [outdir / f"{name}.{ext}" for ext in formats]
    for p in paths:
        fig.savefig(p)

    if not settings:
        warnings.warn(f"teamplot.save('{name}'): no settings given. Every setting needed to "
                      "reproduce a plot must appear in its caption or a nearby note.", stacklevel=2)
        settings = {}
    (outdir / f"{name}.settings.json").write_text(json.dumps(settings, indent=2, default=str) + "\n")
    tex = "; ".join(f"{_tex(k)}: {_tex(v)}" for k, v in settings.items())
    (outdir / f"{name}.settings.tex").write_text(f"\\figsettings{{{tex}}}%\n")
    return paths


# ---- Human annotations (figures/annotated/) -----------------------------------------
# A human may copy figures/<name>.svg to figures/annotated/<name>.svg, add arrows and
# callouts in Inkscape, and export annotated/<name>.pdf (and .png for notebooks/docs).
# Agents never write to annotated/. These helpers pick the right file and flag drift.

STALE_TOLERANCE_MIN = 60  # keep in sync with \teamfigtolerance in teamtufte.sty


def figure_path(name: str, ext: str = "png", figdir: str | Path = "figures") -> Path:
    """Path to show for a figure: the annotated version if a human made one, else generated.
    Annotated SVGs are used directly for ext="svg"; for "png"/"pdf" the exported copy is used."""
    figdir = Path(figdir)
    ann = figdir / "annotated" / f"{name}.{ext}"
    if ann.exists():
        stale = check_annotations(figdir, names=[name], quiet=True)
        for msg in stale:
            warnings.warn(msg, stacklevel=2)
        return ann
    return figdir / f"{name}.{ext}"


def check_annotations(figdir: str | Path = "figures", names=None,
                      tolerance_min: float = STALE_TOLERANCE_MIN, quiet: bool = False) -> list[str]:
    """Return (and print unless quiet) warnings for annotations that may be stale:
    generated <name>.png newer than annotated/<name>.svg, or annotated svg newer than
    its exported pdf/png."""
    figdir = Path(figdir)
    ann_dir = figdir / "annotated"
    msgs = []
    svgs = sorted(ann_dir.glob("*.svg")) if names is None else [ann_dir / f"{n}.svg" for n in names]
    for svg in svgs:
        if not svg.exists():
            continue
        name = svg.stem
        gen = figdir / f"{name}.png"
        if gen.exists() and gen.stat().st_mtime - svg.stat().st_mtime > tolerance_min * 60:
            msgs.append(f"Figure '{name}': generated {name}.png is newer than annotated/{name}.svg; "
                        "re-check the annotations against the new figure, then re-save the SVG.")
        for ext in ("pdf", "png"):
            out = ann_dir / f"{name}.{ext}"
            if out.exists() and svg.stat().st_mtime - out.stat().st_mtime > 60:
                msgs.append(f"Figure '{name}': annotated/{name}.svg was edited after "
                            f"annotated/{name}.{ext} was exported; re-export it from Inkscape.")
        if not (ann_dir / f"{name}.pdf").exists():
            msgs.append(f"Figure '{name}': annotated/{name}.svg has no exported annotated/{name}.pdf; "
                        "LaTeX will keep using the generated figure until it's exported.")
    if not quiet:
        for m in msgs:
            print(f"[teamplot] WARNING: {m}")
    return msgs
