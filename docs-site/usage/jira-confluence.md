# JIRA and Confluence

`scripts/fetch_context.py` snapshots the task and its background into the
workspace. It runs once automatically at creation (if you gave a ticket key or
page IDs and credentials are set) and can be re-run any time.

```bash
python scripts/fetch_context.py --jira ABC-123 --confluence 12345,67890
```

## What it writes

| Source | Destination |
|---|---|
| JIRA summary, type, status, priority, description | `TASK.md`, between `<!-- jira:start -->` and `<!-- jira:end -->` |
| Raw JIRA issue JSON | `context/jira-ABC-123.json` |
| Each Confluence page | `context/confluence-<id>-<title>.md` (HTML converted to Markdown-ish text) |

Only the marked block of `TASK.md` is replaced, so re-fetching never overwrites
your acceptance criteria, steps, or Handoff notes.

## Why snapshots instead of live access?

- **Reproducible and reviewable:** the exact text the agent worked from is in git.
- **Works offline** and on restricted networks.
- **No credentials in the agent's hands.** The script runs with your token; the agent only reads files.
- Content in `context/` is labeled as reference material, not instructions, which
  protects against instructions accidentally embedded in a wiki page.

If your agent also has an Atlassian MCP connection, it can still post progress comments
back to the ticket; see {doc}`agent-loop`.

## Credentials

See {doc}`../installation` for the environment variables. Data Center / Server instances
use a personal access token (bearer auth); Atlassian Cloud uses an API token plus
`ATLASSIAN_EMAIL` (basic auth). The script uses only the Python standard library and
never fails workspace creation: missing credentials or network errors print a warning
and skip.

## Finding page IDs

Confluence page IDs appear in the URL (`…/pages/12345/Page+Title`) or under
**⋯ → Page information**.
