# figures/annotated/ (human-owned)

Hand-annotated versions of generated figures. **Agents never write here.**

To annotate `figures/<name>.svg`:
1. Copy it here, keeping the name: `figures/annotated/<name>.svg`.
2. Edit in Inkscape: add arrows, callouts, labels (use Nimbus Sans 10 pt to match).
3. Export `annotated/<name>.pdf` (File → Save a Copy → PDF) for LaTeX, and
   `annotated/<name>.png` (Export → PNG, 300 dpi) for notebooks/docs. From a terminal:
   `inkscape <name>.svg --export-filename=<name>.pdf`

LaTeX's `\teamfig{<name>}` now uses your version. If the generated figure is later
regenerated, the build warns that your annotation may be stale.
