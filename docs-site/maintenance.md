# Maintenance

This page is for whoever owns the template for the team.

## Repository layout

```
copier.yml           questions, variant logic, post-create tasks, files projects own
template/            everything copied into a workspace
  AGENTS.md.jinja    the agent's instructions (per-variant sections)
  standards/         shared rules + enforcement code (the part you'll edit most)
  scripts/           fetch_context.py, render_diagrams.py, check_figures.py
  {% if kind == 'paper' %}paper{% endif %}/   variant-only folders (empty name = skipped)
docs-site/           this documentation (Sphinx + MyST)
.github/workflows/   docs deployment and template tests
CHANGELOG.md         template release history (Keep a Changelog + semver)
```

Folder names wrapped in `{% if … %}` render only for that variant. Files ending in
`.jinja` are templated; everything else is copied verbatim.

## Changing a standard

Typical examples: new color, different figure aspect ratio, a new writing rule.

1. Edit the file under `template/standards/`.
2. Render a test workspace and check the result (see *Testing* below).
3. Add a line under `## [Unreleased]` in `CHANGELOG.md`.
4. Release (below).

Where things live:

| To change… | Edit |
|---|---|
| Plot fonts, sizes, spines, colors | `standards/teamplot/matplotlibrc` |
| Figure helpers, settings capture | `standards/teamplot/__init__.py` |
| Page geometry / figure widths | `standards/latex/layout.tex` (LaTeX **and** Python read it) |
| Document fonts, sizes, captions, `\teamfig` | `standards/latex/teamtufte.sty` |
| Diagram theme | `standards/mermaid/config.json`, `style.css` |
| Rules agents read | `standards/plotting.md`, `standards/writing.md` |
| Agent workflow | `template/AGENTS.md.jinja` |
| Questions asked at creation | `copier.yml` |

Keep `AGENTS.md.jinja` short. If you're adding more than a line or two, the detail
probably belongs in a `standards/*.md` file that `AGENTS.md` points to.

### Changing the page layout

`layout.tex` must keep the format `\def\teamNAME{<number><unit>}` (unit `in`, `pt`,
`pc`, `bp`, `cm`, or `mm`) because `teamplot` parses it with a regex. Existing figures won't resize themselves: projects must
regenerate figures after updating, so treat a layout change as a **minor** release and say
so in the changelog.

### Changing the stale-annotation tolerance

It's defined twice, deliberately kept in sync: `\teamfigtolerance` in
`teamtufte.sty` and `STALE_TOLERANCE_MIN` in `teamplot/__init__.py`.

## Releasing

Copier updates projects to **git tags**, so every release is a tag.

1. In `CHANGELOG.md`, rename `## [Unreleased]` to `## [1.2.0] - YYYY-MM-DD`, add a fresh
   empty `## [Unreleased]`, and update the compare links at the bottom.
2. Update `release` in `docs-site/conf.py`.
3. Commit and push to `main`:

   ```bash
   git commit -am "Release 1.2.0"
   git push
   ```

   You don't tag by hand. The `release` workflow (`.github/workflows/release.yml`) runs
   when `CHANGELOG.md` changes on `main`. For each `## [X.Y.Z] - YYYY-MM-DD` heading
   without a tag, it tags `vX.Y.Z` on the commit that added the heading and publishes a
   GitHub release with that changelog section as its notes. It also warns if
   `docs-site/conf.py` names a different version. To re-run it, use **Run workflow**
   on the workflow's Actions page; existing tags and releases are left alone.

Version numbers:

- **MAJOR**: a project needs manual migration (renamed/moved files, changed questions,
  removed helpers).
- **MINOR**: new rules, helpers, variant features, layout changes.
- **PATCH**: fixes and wording.

## Updating existing projects

In each workspace (with a clean git tree):

```bash
copier update --trust              # to the latest tag
copier update --trust --vcs-ref v1.2.0   # or a specific one
```

Copier re-renders the template with the project's saved answers
(`.copier-answers.yml`) and three-way-merges the result:

- **Template-owned files** (`AGENTS.md`, `standards/`, `scripts/`, `.latexmkrc`) update.
- **`TASK.md` and `CHANGELOG.md` are never touched** (`_skip_if_exists` in `copier.yml`).
- **Deliverables** (notebook, writeup, `main.tex`) keep local edits; template changes
  to them are merged in.
- Conflicts appear as inline conflict markers (or `.rej` files); resolve them like a git merge.

Then add a line to the project's `CHANGELOG.md`:

```markdown
### Changed
- Template 1.1.0 → 1.2.0 (see agent-workspace-template CHANGELOG).
```

and regenerate figures if the release notes say the style or layout changed.

## Adding a variant

1. Add the choice to `kind` in `copier.yml`.
2. Create `template/{% if kind == 'newkind' %}folder{% endif %}/` with its starter files.
3. Add an `{%- elif kind == 'newkind' -%}` section to `AGENTS.md.jinja`.
4. Document it in `docs-site/usage/variants.md`, test, release as **minor**.

## Testing

The `test-template` workflow renders every variant, runs the Python helpers, builds
both paper styles with LaTeX, and checks the stale-annotation logic. To test locally:

```bash
copier copy --trust --defaults --vcs-ref HEAD --data kind=paper . /tmp/t-paper
cd /tmp/t-paper/paper && latexmk main.tex
```

`--vcs-ref HEAD` renders your latest commit; commit first, since uncommitted changes
aren't included.

## The documentation site

Source is in `docs-site/` (Sphinx with MyST Markdown and the Furo theme). The
`docs` workflow builds it on every push to `main` and deploys to GitHub Pages.

- **One-time setup:** repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
- **Local preview:**

  ```bash
  pip install -r docs-site/requirements.txt
  sphinx-build -W -b html docs-site docs-site/_build/html
  ```

- `reference/standards.md` includes `template/standards/*.md` directly, so the
  rules are documented from a single source and never drift.
- Example images live in `docs-site/_static/img/`; regenerate them when the house style changes.
