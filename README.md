# agent-workspace-template

A [Copier](https://copier.readthedocs.io) template that scaffolds a workspace for
an AI agent (Claude Code, Codex, Cursor, …) to work a single task, with shared
team standards for plots, diagrams, typography, and writing.

**Full documentation: https://jondoesntgit.github.io/agent-workspace-template/**

| Variant | Deliverable |
|---|---|
| `investigation` | Jupyter notebook with a handful of plots |
| `docs` | Markdown writeup grounded in pulled Confluence pages |
| `paper` | Tufte-style LaTeX: `tufte-handout` (paper) or `tufte-book` (dissertation-style report) |

## Quick start

```bash
pipx install copier
copier copy --trust gh:jondoesntgit/agent-workspace-template my-task
cd my-task && git init && git add -A && git commit -m "Scaffold workspace"
```

Then point your agent at the folder; it starts from `AGENTS.md`. Set
`ATLASSIAN_*` environment variables first to have the ticket and Confluence pages
pulled in automatically ([installation docs](https://jondoesntgit.github.io/agent-workspace-template/installation.html)).

## What's inside a workspace

```
AGENTS.md        how to work here (template-owned, short)
TASK.md          goal, acceptance criteria, steps, Handoff (project-owned)
CHANGELOG.md     dated, human-readable history of the deliverable (project-owned)
context/         JIRA/Confluence snapshots
standards/       plotting.md, writing.md, teamplot/, latex/, mermaid/ (shared by all variants)
diagrams/        Mermaid sources → figures/
figures/         generated PDF/PNG/SVG + settings; annotated/ = human overrides
scripts/         fetch_context.py, render_diagrams.py, check_figures.py
notebooks/ | docs/ | paper/
```

## House style at a glance

- Body: Pagella (Palatino) 10 pt (tufte-latex native) with newpxmath; captions and
  all plot/diagram text: Nimbus Sans 10 pt.
- Vector components: x = `tab:red`, y = `tab:green`, z = `tab:blue`, always.
- Figures are drawn at the exact LaTeX column width (`standards/latex/layout.tex`
  is read by both LaTeX and Python) and included at natural size.
- Tufte-style plots: no top/right spines, no grid, direct labels, muted palette.
- Every setting needed to reproduce a plot appears in its caption or a nearby note.
- Humans can annotate any generated figure in Inkscape (`figures/annotated/`); builds
  warn when an annotation goes stale.

## Maintaining

Edit `template/`, log the change in [`CHANGELOG.md`](CHANGELOG.md), and push a release
commit to `main`; the release workflow tags it from the changelog. Then run
`copier update --trust` in each project.
See the [maintenance docs](https://jondoesntgit.github.io/agent-workspace-template/maintenance.html).

## Repo layout

- `copier.yml`: questions, variant logic, post-create tasks
- `template/`: everything that gets copied (folders named `{% if kind == '…' %}…`
  render only for that variant)
- `docs-site/`: Sphinx source for the documentation site
- `CHANGELOG.md`: template release history
