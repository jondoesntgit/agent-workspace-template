# Diagrams

Block diagrams, flowcharts, state machines, and sequence diagrams are written as
[Mermaid](https://mermaid.js.org) text and rendered with a shared house style.
Agents write Mermaid reliably, it diffs cleanly in git, and every diagram looks
the same without anyone touching Inkscape.

## The pattern

`diagrams/example_pipeline.mmd`:

```text
flowchart TB
  raw[Raw IMU data] --> cal[Calibration]
  cal --> kf[Kalman filter]
  ref[Reference track] --> err
  kf --> err[Error analysis]
  class kf accent
```

```bash
python scripts/render_diagrams.py          # renders diagrams that changed
python scripts/render_diagrams.py --all    # force everything
```

→ `figures/example_pipeline.{svg,pdf,png}`

```{figure} ../_static/img/example_pipeline.png
:width: 300px

Rendered with the team theme: Nimbus Sans, thin gray strokes, no shadows,
one accent color for the element the reader should notice.
```

Include it exactly like a plot: `\teamfig{example_pipeline}` in LaTeX, or the PNG in Markdown.

## Rules

- **Style comes from `standards/mermaid/`** (`config.json` theme + `style.css`). No inline
  `style` or `classDef` color overrides in `.mmd` files.
- **One accent per diagram:** `class <node> accent` marks the thing to notice.
- **Fit the column:** prefer `flowchart TB`. A diagram narrower than the column is
  included at natural size, so its text is 10 pt like everything else. Wider diagrams
  are scaled down to fit, and their text shrinks. Use `LR` only for short chains,
  or put wide diagrams in `figure*`.
- **Small:** one idea per diagram, roughly ten nodes at most, short labels.
- The renderer only re-renders diagrams whose `.mmd` is newer than their PNG, so
  unchanged diagrams keep their timestamps and don't trigger stale-annotation warnings.

## Why labels are SVG text, not HTML

Mermaid's default puts node labels in HTML `<foreignObject>` elements. Inkscape
and PDF converters mangle those. The team config sets `htmlLabels: false`, so labels are
real SVG `<text>` in Nimbus Sans that a human can edit, restyle, or annotate
(see {doc}`annotations`).

## When Mermaid isn't enough

Mermaid's automatic layout struggles with dense signal-flow block diagrams, feedback
loops that need specific placement, or anything needing exact geometry. Options,
in order of preference:

1. Render with Mermaid, then have a human adjust it as an annotation ({doc}`annotations`).
2. Use [Graphviz](https://graphviz.org) (`dot -Tsvg`, `-Tpdf`) with Nimbus Sans 10 pt,
   writing output to `figures/<name>.{svg,pdf,png}`. Everything downstream works the same.
3. Draw it by hand in Inkscape and save it directly as `figures/annotated/<name>.svg/.pdf`.

## Mermaid on Windows and locked-down machines

See {doc}`../installation`: install `@mermaid-js/mermaid-cli@12` with npm; if its
Chromium download is blocked, set `MMDC_PUPPETEER_CONFIG` to a JSON file pointing at
Edge or Chrome.
