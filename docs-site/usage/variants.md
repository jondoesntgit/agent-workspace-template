# The three variants

All variants share `AGENTS.md`, `TASK.md`, `CHANGELOG.md`, `context/`,
`standards/`, `diagrams/`, `figures/`, and `scripts/`. They differ in the
deliverable folder and in the variant-specific section of `AGENTS.md`.

## `investigation`: notebook with a handful of plots

```
notebooks/01_analysis.ipynb
requirements.txt
```

- The notebook starts with a setup cell that moves to the workspace root and imports
  `teamplot`, plus a figure-pattern cell and a "Findings" cell.
- Each plot is followed by a markdown cell: the takeaway, then the settings line from
  `teamplot.settings_text(settings)`.
- The agent must leave the notebook runnable top to bottom (Restart & Run All).
- Display saved figures with `teamplot.figure_path(name)` so human annotations win.

## `docs`: Markdown grounded in Confluence

```
docs/writeup.md      Summary / Background / Details / Open questions
context/confluence-<id>-<title>.md
```

- Sources are snapshotted into `context/` at creation. The agent cites page titles,
  summarizes rather than copies, and lists gaps under "Open questions" instead of guessing.
- Figures: `![caption](../figures/name.png)` followed by an italic caption line
  with the settings. Run `python scripts/check_figures.py` before finishing.
- The Markdown converts cleanly to Confluence, Word, or PDF with pandoc if needed.

## `paper`: Tufte-style LaTeX

```
paper/main.tex           tufte-handout (article) or tufte-book (report)
paper/sections/*.tex     abstract, introduction, methods, results, conclusion
paper/references.bib
paper/.latexmkrc         finds standards/latex/, tolerates "no citations yet"
```

- Typography and layout come from `standards/latex/teamtufte.sty`; see {doc}`latex`.
- `report` style adds front matter, table of contents, and chapters.
- Build with `cd paper && latexmk main.tex`; the agent must leave it compiling cleanly.

```{figure} ../_static/img/handout-page2.png
:class: page
:width: 520px

A full-width figure (`figure*` + `teamplot.figure("full")`) spanning text and margin, with x/y/z colored by axis, and the bibliography appearing once something is cited.
```
