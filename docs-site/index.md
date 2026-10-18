# Agent Workspace Template

A [Copier](https://copier.readthedocs.io) template that gives an AI coding agent
(Claude Code, Codex, Cursor, …) a ready-made workspace for **one task**, with
the goal pulled from JIRA, background pulled from Confluence, and **one shared
set of team standards** for plots, diagrams, typography, and writing.

```bash
pipx install copier
copier copy --trust gh:jondoesntgit/agent-workspace-template my-task
```

Pick one of three variants when asked:

| Variant | You get | Typical task |
|---|---|---|
| `investigation` | a Jupyter notebook | "Characterize gyro drift vs. temperature; a handful of plots." |
| `docs` | a Markdown writeup + Confluence snapshots | "Summarize the test-bench setup for the new hires." |
| `paper` | a Tufte-style LaTeX document (handout or book) | "Write up the filter design as a short paper / thesis-style report." |

```{figure} _static/img/handout-page1.png
:class: page
:width: 520px

A `paper` workspace: Pagella 12 pt body, sidenotes in the margin, Nimbus Sans
captions that match the plot text, and the plot's settings in its caption.
```

## Where to go next

- **New here?** Read {doc}`goal`, then {doc}`installation` and {doc}`usage/creating`.
- **Running an agent on a workspace?** See {doc}`usage/agent-loop`.
- **Making figures?** {doc}`usage/figures`, {doc}`usage/diagrams`, {doc}`usage/annotations`.
- **Maintaining the template for your team?** {doc}`maintenance`.

```{toctree}
:hidden:
:caption: Overview

goal
installation
```

```{toctree}
:hidden:
:caption: Using it

usage/creating
usage/agent-loop
usage/variants
usage/figures
usage/diagrams
usage/annotations
usage/latex
usage/jira-confluence
```

```{toctree}
:hidden:
:caption: Maintaining it

maintenance
troubleshooting
```

```{toctree}
:hidden:
:caption: Reference

reference/workspace-files
reference/standards
reference/changelog
```
