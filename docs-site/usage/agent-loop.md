# The agent session loop

Agents start every session with no memory of the last one. The workspace is
built so that a fresh session can pick up exactly where the previous one stopped,
and a human can see what happened, without anyone re-explaining.

## The loop

```{mermaid}
flowchart TB
  A[Read TASK.md<br/>goal, checklist, Handoff] --> B[Skim context/]
  B --> C[Do the next unchecked step]
  C --> D[Commit]
  D --> E{More time<br/>in session?}
  E -- yes --> C
  E -- no --> F[Tick items, overwrite Handoff,<br/>add CHANGELOG entry, commit]
```

`AGENTS.md` spells this out, so in practice you just say "start a session per AGENTS.md".

## `TASK.md`: what, and where we left off

```markdown
## Goal                  ← from JIRA (agent must not change)
## Background
## Acceptance criteria   ← checkboxes, the definition of done
## Steps                 ← small items, each finishable in one session
## Scope notes
## Handoff               ← overwritten every session
- **Next:** fit the temperature model to runs 3–7
- **Blocked / questions for a human:** run 5 looks mislabeled; confirm?
```

**Tip:** the quality of the Steps list drives everything. Before the first session,
either write the steps yourself or ask the agent to propose them and review the
result. Keep each step small enough to finish and commit in one sitting.

## `CHANGELOG.md`: what changed, for humans

Newest entry on top, one per session, Keep-a-Changelog headings:

```markdown
## 2026-10-21
### Added
- Bias-vs-temperature figure with linear fit (Fig. 2).
### Changed
- Conclusion: drift is temperature-driven, not time-driven (supersedes 2026-10-19).
```

This is the file a reviewer reads to see how the work evolved. Commit messages
hold the fine-grained detail; the changelog holds the story.

## Why not track progress in README or AGENTS.md?

- `AGENTS.md` is *instructions*. If agents rewrite it each session it fills with
  stale state and the instructions drift. It's template-owned and changes only via
  `copier update`.
- `README.md` is for people arriving at the repo, not a status log.
- A changelog alone mixes history with "what's next"; the Handoff section keeps
  current state separate and short.

## Working with JIRA

If the team tracks status in JIRA, ask the agent to post the session's changelog
entry as a ticket comment at the end of each session (via an Atlassian MCP
connection, if your agent has one). JIRA stays the team-facing source of truth;
the workspace stays the detailed record.

## Reviewing an agent's session

1. Read the top `CHANGELOG.md` entry and the Handoff section.
2. `git log --stat` since your last review.
3. Answer anything under "Blocked / questions" by editing `TASK.md` (the agent reads it next time).
4. Check for build warnings about stale annotations (see {doc}`annotations`).
