# Goal and design

## The problem

Handing a task to an AI agent works best when three things are clear and separate:

1. **What** to do: the goal and acceptance criteria (usually a JIRA ticket).
2. **Background**: reference material the agent should read but not obey
   (Confluence pages, ticket history).
3. **How** to do it: the team's standing rules (plot style, writing style,
   document layout) that apply to *every* task.

When all of this gets pasted into one long instruction file, it rots. The rules
drift between projects, the instructions grow until the agent skims them, and
nobody can tell which project has the latest plotting conventions.

## The approach

Each concern lives in its own file, with a clear owner:

| Concern | File | Owner | Changes when |
|---|---|---|---|
| How to work here (short index) | `AGENTS.md` | template | template is updated |
| What to do + where we left off | `TASK.md` | project | every session (checklist, Handoff) |
| History of the deliverable | `CHANGELOG.md` | project | every session (one dated entry) |
| Background | `context/` | generated | at creation (or on re-fetch) |
| Team standards | `standards/` | template | template is updated |
| Human figure edits | `figures/annotated/` | humans only | when someone annotates a figure |

`AGENTS.md` stays short (about 50 lines) because it mostly *points*: "before any plot,
read `standards/plotting.md`". The agent loads detail only when it needs it.

```{mermaid}
flowchart LR
  T[Template repo<br/>tagged releases] -- copier copy --> W[Workspace]
  J[JIRA ticket] -- fetch_context.py --> W
  C[Confluence pages] -- fetch_context.py --> W
  W -- agent sessions --> D[Deliverable<br/>notebook / doc / paper]
  T -- copier update --> W
  H[Human] -- annotates figures,<br/>reviews CHANGELOG --> W
```

## Why one template with three variants

The three kinds of task (quick investigation, documentation, major writeup)
need different scaffolding but **identical standards**. Copier renders only the
chosen variant's folders and instructions, while every variant gets the same
`standards/` directory. Change a plotting rule once, release, and every project
picks it up with `copier update`.

Copier was chosen over cookiecutter because it can **update** existing projects
from newer template versions with a three-way merge. That's what keeps the shared
standards in sync without submodules.

## Why the standards are code, not just prose

Agents follow `teamplot.figure("column")` far more reliably than a paragraph
describing font sizes. So every rule that *can* be enforced in code is:

- `standards/teamplot/matplotlibrc`: fonts, sizes, spines, colors.
- `standards/latex/layout.tex`: the page geometry, read by **both** LaTeX and Python,
  so figures are drawn at exactly the column width.
- `standards/latex/teamtufte.sty`: typography and the `\teamfig` include macro.
- `standards/mermaid/`: the diagram theme.

The Markdown files in `standards/` explain intent and cover what code can't
(for example, "every setting needed to reproduce a plot goes in its caption").

## Two changelogs, two audiences

- The **template's** `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com)
  with semantic versions that match git tags. It tells maintainers what changed in
  the standards.
- Each **project's** `CHANGELOG.md` is dated, newest first, written for a human
  reviewer: how the deliverable evolved. When a project takes a template update, it
  records one line, e.g. `Template 1.0.0 → 1.1.0`, so the two histories link
  without mixing.
- Agent-to-agent handoff ("next step", "blocked on") is *current state*, not history,
  so it lives in `TASK.md` → Handoff and is overwritten each session.

## Design principles

- **Reproducible figures.** Settings in every caption; generated files are never hand-edited.
- **Humans can always override.** Annotated figures win over generated ones, and the build
  warns when the two drift apart.
- **Nothing silently fails the build.** Missing credentials, fonts, or citations produce
  warnings, not broken workspaces.
- **Plain files.** Everything is Markdown, YAML, LaTeX, JSON, or Python in git, with no
  service to run.
