# Creating a workspace

## Interactive

```bash
copier copy --trust gh:jondoesntgit/agent-workspace-template my-task
```

Copier asks:

| Question | Notes |
|---|---|
| `kind` | `investigation`, `docs`, or `paper`. Decides which folders and instructions you get. |
| `project_name` | Used in titles; defaults to the folder name. |
| `author` | For document bylines. |
| `jira_key` | e.g. `ABC-123`. Blank = fill in `TASK.md` yourself. |
| `confluence_pages` | Comma-separated page IDs (not asked for `investigation`). |
| `paper_style` | `article` → `tufte-handout`; `report` → `tufte-book` with chapters (only for `paper`). |

`--trust` allows the template's one-time post-creation steps: date-stamping the
first `CHANGELOG.md` entry and running `scripts/fetch_context.py`.

## Non-interactive

Useful in scripts, or to have an agent create its own workspace:

```bash
copier copy --trust gh:jondoesntgit/agent-workspace-template ABC-123-drift \
  --data kind=investigation --data jira_key=ABC-123 --defaults
```

Pin a template version with `--vcs-ref v1.0.0`.

## Then put it in git

```bash
cd ABC-123-drift
git init && git add -A && git commit -m "Scaffold workspace from agent-workspace-template"
```

Git is what makes the agent's step-by-step commits, `copier update`, and the
annotation timestamps meaningful, so do this before the first agent session.

## Which variant?

- **investigation**: the answer is a few plots and a paragraph. Throwaway-ish, fast.
- **docs**: the answer is prose grounded in existing Confluence material.
- **paper**: the answer is a document someone will cite, review, or archive.
  Choose `report` for chapter-length work (dissertation style), `article` otherwise.

You can't switch variants with `copier update`; create a new workspace and move content over.

## Kicking off the agent

Open the folder in your agent and give it a one-line instruction; `AGENTS.md`
supplies the rest:

> Start a session per AGENTS.md. Work the next unchecked step in TASK.md.

Claude Code reads `CLAUDE.md`, which simply imports `AGENTS.md`; other agents read
`AGENTS.md` directly. See {doc}`agent-loop` for what happens next.
