# Plotting standards

Apply to every workspace type. **`standards/teamplot/` is the enforcement; this
page explains the intent.** If they disagree, the code wins.

## How to plot
```python
import sys; sys.path.insert(0, "standards")   # run from the workspace root
import teamplot

fig, ax = teamplot.figure("column")           # "column" | "margin" | "full"
ax.plot(t, x, label="Measured")
ax.plot(t, x_hat, label="Filtered")
teamplot.label(ax, x="Time", x_unit="s", y="Position", y_unit="m")
teamplot.direct_labels(ax)                    # instead of a legend
teamplot.save(fig, "position_vs_time", settings={
    "Data": "run_2026-10-12.csv",
    "Sample rate": "100 Hz",
    "Filter": "Kalman, Q = 0.01, R = 0.25",
})
```

## The reproducibility rule
**Every setting needed to reproduce a plot must appear in its caption, or in a
margin note/footnote next to it.** That means the data source, sample sizes,
sample rates, filter/fit parameters, model choices, random seeds, and any
preprocessing (decimation, outlier removal, normalization).
- Pass these as `settings=` to `teamplot.save()`. It writes
  `figures/<name>.settings.json` and `figures/<name>.settings.tex`.
- LaTeX: `\figsettingsof{<name>}` inside the `\caption{}` (reads `figures/<name>.settings.tex`).
- Notebooks / Markdown: put `teamplot.settings_text(settings)` in the caption line
  directly under the figure.
- `save()` warns when `settings` is empty. Treat that warning as an error.

## Size: figures are drawn at final size
- Widths come from `standards/latex/layout.tex`, the same file the LaTeX layout uses:
  `"column"` = main text width, `"margin"` = margin figure, `"full"` = text + margin.
- In LaTeX, include every figure with `\teamfig{name}` (natural size, never
  `width=...`). Scaling would break the 10 pt text match. `\teamfig` only shrinks
  a figure if it is wider than the column, which a `teamplot` figure never is.
- Saving uses `bbox="standard"` so the file is exactly the requested width.
  Don't pass `bbox_inches="tight"`.
- `teamplot.save()` writes PDF (for LaTeX), PNG (for notebooks/docs) and SVG
  (editable text, for human annotation).

## Diagrams: Mermaid
- Write diagrams as Mermaid source in `diagrams/<name>.mmd`, then run
  `python scripts/render_diagrams.py` → `figures/<name>.{svg,pdf,png}`.
- The shared style (`standards/mermaid/`) sets Nimbus Sans 10 pt, thin gray
  strokes, no shadows, and real SVG text (no HTML labels) so humans can edit the SVG.
- Mark the one element the reader should notice with `class <node> accent`.
  Don't set colors or styles inline in the `.mmd`.
- Prefer `flowchart TB` (top-to-bottom) so diagrams fit the column at natural size;
  use `LR` only for short chains or `figure*` (full width).
- Keep diagrams small: one idea per diagram, ≤ ~10 nodes, short labels.
- If Mermaid can't express a layout well, say so in TASK.md → Handoff rather than
  fighting it; a human may switch that diagram to Graphviz or annotate it by hand.
- Diagrams are included and annotated exactly like plots (below).

## Human annotations (`figures/annotated/`)
Generated figures can be improved by hand without giving up regeneration:
1. A human copies `figures/<name>.svg` to `figures/annotated/<name>.svg`, adds
   arrows, callouts, or labels in Inkscape, and exports `annotated/<name>.pdf`
   (and `annotated/<name>.png` for notebooks/docs).
2. `\teamfig{name}` (LaTeX) and `teamplot.figure_path(name)` (Python) automatically
   prefer the annotated version.
3. If a figure is regenerated after it was annotated (its PNG is more than an hour
   newer than the annotated SVG), LaTeX logs a warning and prints a red "Annotation may be
   stale" note under the figure; `python scripts/check_figures.py` reports the same.
   It also flags an annotated SVG that was edited but not re-exported.

**Agents: never create, edit, or delete anything in `figures/annotated/`.** If
regenerating a figure makes an annotation stale, say so in TASK.md → Handoff and
let a human update it. Don't regenerate an annotated figure unless the task needs it.

## Style (Tufte: maximize data ink)
- Style comes from `standards/teamplot/matplotlibrc`. Don't set rcParams or call
  `plt.style.use` yourself.
- No top or right spines; left/bottom spines offset outward; no grid.
- Consider `teamplot.rangeframe(ax)` so axes span only the data range.
- No titles inside the figure; the caption carries the message.
- Label lines directly (`teamplot.direct_labels`) rather than with a legend
  whenever there are ≤ 4 series.
- Use the color cycle in order: near-black first, then muted accents. Avoid
  ad-hoc colors, 3-D effects, shadows, and decorative fills.
- **x/y/z data always uses `tab:red` for x, `tab:green` for y, `tab:blue` for z**
  (`teamplot.XYZ_COLORS`, or `teamplot.xyz_color("x")`). This applies to any vector
  components: position, velocity, acceleration, angular rate, magnetic field, axes
  of a coordinate frame. It overrides the color cycle so components read the same
  in every figure.
- Every axis has a label with units in brackets, `Time [s]` (`teamplot.label`).
- Show uncertainty (error bars or light shaded bands) whenever it's known.
- Filenames: lowercase snake_case describing the content (`bias_vs_temperature`).

## Typography
| Element | Font | Size |
|---|---|---|
| Body text (LaTeX) | Pagella (Palatino) + newpxmath | 10 pt (tufte-latex native) |
| Sidenotes, margin notes | Pagella | 8 pt (tufte default) |
| Captions | Nimbus Sans | 10 pt |
| All text inside plots, incl. math | Nimbus Sans | 10 pt |

Nimbus Sans must be installed for matplotlib to use it (see README → Fonts);
`teamplot` warns if it's missing.
