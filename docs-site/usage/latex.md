# LaTeX papers

`paper` workspaces use [tufte-latex](https://github.com/Tufte-LaTeX/tufte-latex)
(`tufte-handout` or `tufte-book`) with the team package
`standards/latex/teamtufte.sty` on top.

```{figure} ../_static/img/handout-page1.png
:class: page
:width: 520px

First page of a `tufte-handout` workspace.
```

## Typography

| Element | Font | Size |
|---|---|---|
| Body | Pagella (Palatino clone, `newpxtext`) | 10 pt / 14 pt leading (tufte-latex native) |
| Math | `newpxmath` (matched to Pagella) | 10 pt |
| Sidenotes, margin notes | Pagella | 8 pt (tufte default) |
| Captions | Nimbus Sans (`helvet`) | 10 pt |
| Plot and diagram text | Nimbus Sans | 10 pt |
| Code | Bera Mono, scaled 0.85 | |

Why these: Pagella is Tufte-latex's own default family and has complete matching
math (including bold math and blackboard bold) under pdfLaTeX and, via TeX Gyre
Pagella Math, under LuaLaTeX/XeLaTeX. Nimbus Sans is a free, metric-compatible
Helvetica that installs easily on Windows, and both fonts come from URW, so they
sit well together.

The body uses tufte-latex's native 10 pt size and page geometry, so everything
else in the class (margin notes, running heads, full-width figures) behaves as its
authors designed. Captions are set in 10 pt Nimbus Sans so they match plot text.

## Layout

Letter paper, tufte-latex's native geometry: 1 in left margin, 26 pc (312 pt) text
block, 2 pc gap, 12 pc (144 pt) margin column. Defined in
`standards/latex/layout.tex`, shared with `teamplot`.

## Writing in the Tufte style

```latex
Main argument goes here.\sidenote{Numbered aside, set in the margin.}
\marginnote{Unnumbered remark in the margin.}
Results agree with prior work.\cite{smith2024}   % a numbered sidenote, after punctuation
```

| Need | Use | `teamplot.figure(...)` |
|---|---|---|
| Normal figure (caption in margin) | `\begin{figure}` | `"column"` |
| Small figure in the margin | `\begin{marginfigure}` | `"margin"` |
| Wide figure | `\begin{figure*}` | `"full"` |
| Table | `\begin{table}` + `booktabs` | |
| Units | `\SI{30}{\minute}`, `\si{\degree\celsius}` | |
| Cross-reference | `\cref{fig:bias}` → "Fig. 1" | |
| Placeholder | `\todo{cite}` → red margin note | |
| Bibliography | `\teambibliography{references}` (already in `main.tex`) | hidden until the first `\cite` |

Always include figures with `\teamfig{name}` and put settings in the caption with
`\figsettingsof{name}`:

```latex
\begin{figure}
  \teamfig{bias_vs_temperature}
  \caption{Gyro bias rises roughly linearly with temperature.
    \figsettingsof{bias_vs_temperature}}
  \label{fig:bias}
\end{figure}
```

`\teamfig[<includegraphics keys>]{name}` uses `figures/annotated/name.pdf` if present,
else `figures/name.pdf`; includes it at natural size, capped at `\linewidth`; and warns
on stale annotations ({doc}`annotations`). `\figsettingsof{name}` reads
`figures/name.settings.tex` and shows a red marker if it's missing.

## Building

```bash
cd paper
latexmk main.tex      # pdfLaTeX, runs BibTeX as needed
latexmk -c            # clean auxiliary files
```

`paper/.latexmkrc` adds `../standards/latex//` to the TeX search path and lets
BibTeX's "no citations yet" error pass on fresh documents.

**Overleaf:** upload the workspace, set the main document to `paper/main.tex`,
and copy `standards/latex/*` and `figures/` alongside. Overleaf runs latexmk with the
same `.latexmkrc`.

## `article` vs `report`

- `article` → `tufte-handout`: title block, abstract, sections.
- `report` → `tufte-book`: title page, table of contents, front matter, chapters,
  alternating (two-sided) margins. Use it for dissertation-style writeups.
