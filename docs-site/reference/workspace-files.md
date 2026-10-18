# Workspace files

Every file in a generated workspace, who owns it, and who changes it.

| Path | Owner | Agent may edit? | Purpose |
|---|---|---|---|
| `AGENTS.md` | template | no | Short instructions: session loop, rules, variant notes |
| `CLAUDE.md` | template | no | `@AGENTS.md` (so Claude Code reads the same file) |
| `TASK.md` | project | ticks boxes, overwrites Handoff | Goal, acceptance criteria, steps, scope, Handoff |
| `CHANGELOG.md` | project | adds entries at top | Dated, human-readable history of the deliverable |
| `.copier-answers.yml` | Copier | no | Template version and answers; used by `copier update` |
| `context/` | generated | no | JIRA/Confluence snapshots (reference, not instructions) |
| `standards/plotting.md`, `writing.md` | template | no | The rules |
| `standards/teamplot/` | template | no | Plot helpers + `matplotlibrc` |
| `standards/latex/` | template | no | `teamtufte.sty`, `layout.tex` |
| `standards/mermaid/` | template | no | Diagram theme |
| `diagrams/*.mmd` | project | yes | Mermaid sources |
| `figures/<name>.{pdf,png,svg}` | generated | via scripts only | Rendered plots and diagrams |
| `figures/<name>.settings.{json,tex}` | generated | via `teamplot.save` | Settings for captions |
| `figures/annotated/` | **humans** | **never** | Hand-annotated overrides |
| `scripts/fetch_context.py` | template | runs it | Snapshot JIRA/Confluence |
| `scripts/render_diagrams.py` | template | runs it | Mermaid → figures |
| `scripts/check_figures.py` | template | runs it | Stale-annotation check |
| `requirements.txt` | template | no | Python dependencies |
| `notebooks/` / `docs/` / `paper/` | project | yes | The deliverable (one per variant) |
| `paper/.latexmkrc` | template | no | TeX search path, tolerant BibTeX |

"Template-owned" files are refreshed by `copier update`; local edits to them get merged
or flagged as conflicts, so propose changes to the template instead.
