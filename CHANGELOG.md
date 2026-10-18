# Changelog

All notable changes to this **template** are documented here. Projects created
from it keep their own `CHANGELOG.md` for the history of their deliverable.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Each release is a git tag (`v1.0.0`), which is what `copier update` pulls.

- **MAJOR**: breaking changes to workspace layout or questions (projects may need manual migration)
- **MINOR**: new rules, helpers, or variant features
- **PATCH**: fixes and wording

## [Unreleased]
### Added
- Release workflow: each dated version heading in `CHANGELOG.md` is tagged and
  published as a GitHub release automatically, so releases need no manual `git tag`.

## [1.1.0] - 2026-10-18
### Changed
- Body text is now tufte-latex's native 10 pt (was a 12 pt override), and the page
  layout is back to tufte's native geometry: 26 pc text, 2 pc gap, 12 pc margin.
  `layout.tex` now accepts TeX units (in, pt, pc, bp, cm, mm) so widths match exactly.
  Figure widths follow automatically; **regenerate existing figures** after updating.
- Sidenotes and margin notes use tufte's default size again. Captions stay 10 pt Nimbus Sans.

### Added
- x/y/z color rule: x = `tab:red`, y = `tab:green`, z = `tab:blue` for any vector
  components (`teamplot.XYZ_COLORS`, `teamplot.xyz_color()`), in the plotting
  standard and `AGENTS.md`.
- `\teambibliography{}`: the References section stays hidden until the first `\cite`.

## [1.0.0] - 2026-10-18
### Added
- Copier template with three variants: `investigation` (Jupyter), `docs` (Markdown
  from Confluence context), `paper` (Tufte LaTeX: `tufte-handout` or `tufte-book`).
- Shared `standards/`: plotting and writing rules, `teamplot` helpers, `matplotlibrc`,
  `teamtufte.sty`, and `layout.tex` as the single source of column widths for LaTeX and Python.
- Typography: Pagella 12 pt body with newpxmath, 10 pt Pagella sidenotes,
  10 pt Nimbus Sans captions and plot text.
- Reproducibility rule: plot settings are captured by `teamplot.save(settings=...)`
  and placed in captions via `\figsettingsof{<name>}`.
- `scripts/fetch_context.py`: snapshots a JIRA ticket into `TASK.md` and Confluence
  pages into `context/`.
- Session loop for agents: `TASK.md` checklist + Handoff, project `CHANGELOG.md`.
- Mermaid diagrams: `diagrams/*.mmd` rendered by `scripts/render_diagrams.py` with a
  shared Tufte-style theme (`standards/mermaid/`), editable SVG text.
- Human annotation workflow: `figures/annotated/` overrides, `\teamfig{}` in LaTeX and
  `teamplot.figure_path()` in Python, with stale-annotation warnings at LaTeX compile
  time and in `scripts/check_figures.py`.
- Sphinx documentation site published to GitHub Pages.

[Unreleased]: https://github.com/jondoesntgit/agent-workspace-template/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/jondoesntgit/agent-workspace-template/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/jondoesntgit/agent-workspace-template/releases/tag/v1.0.0
