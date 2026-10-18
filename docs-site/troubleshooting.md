# Troubleshooting

## Creating and updating workspaces

**"Template uses potentially unsafe features" / tasks didn't run.**
Add `--trust`. Without it Copier skips the post-creation steps (changelog date, JIRA fetch).

**`copier update` says there are uncommitted changes.**
Commit or stash first; Copier needs a clean tree to merge safely.

**`copier update` errors with "Unknown revision".**
The project was created from a local path that no longer exists or wasn't a tagged
git repo. Fix `_src_path` in `.copier-answers.yml` to
`gh:jondoesntgit/agent-workspace-template`, then update.

**TASK.md wasn't filled from JIRA.**
Check the creation output for `[fetch_context]` warnings. Usually `ATLASSIAN_TOKEN` or
the URL variables aren't set in that terminal. Set them and re-run
`python scripts/fetch_context.py --jira ABC-123`.

## Plots

**Warning: "Nimbus Sans is not installed".**
Install the font ({doc}`installation`), then clear matplotlib's cache:
`python -c "import matplotlib, shutil; shutil.rmtree(matplotlib.get_cachedir())"`.

**Text in the PDF is the wrong size.**
The figure was scaled. Use `\teamfig{name}` (no `width=`) and create it with
`teamplot.figure("column" | "margin" | "full")`. Don't use `bbox_inches="tight"`.

**Direct labels run off the right edge.**
Constrained layout reserves room for them; if a label is very long, shorten it or
use `teamplot.figure("full")`.

## Diagrams

**`Could not find chrome-headless-shell` / Chromium download fails.**
Point Mermaid at an installed browser with `MMDC_PUPPETEER_CONFIG` ({doc}`installation`).

**`No usable sandbox` (Linux/containers).**
Add `"args": ["--no-sandbox"]` to the puppeteer JSON.

**Diagram text is tiny in the PDF.**
The diagram is wider than the column and got scaled down. Switch to `flowchart TB`,
shorten labels, or use `figure*`.

## LaTeX

**`File 'teamtufte.sty' not found`.**
Build from `paper/` with `latexmk` so `.latexmkrc` adds `../standards/latex/` to the search path.
Running plain `pdflatex` needs `TEXINPUTS=../standards/latex//:` set.

**`File 'newpxtext.sty' not found` (or `tufte-handout.cls`, `binhex.tex`).**
Install the missing packages: MiKTeX does it on demand; on TeX Live use
`tlmgr install newpx tufte-latex kastrup` or the Debian packages in {doc}`installation`.

**Red "Annotation may be stale" text under a figure.**
Working as intended; see {doc}`usage/annotations`. Update the annotated SVG and
re-export, or raise `\teamfigtolerance`.

**`latexmk` fails on a document with no citations.**
Make sure the workspace's `paper/.latexmkrc` is present; it tolerates BibTeX's
"no \citation commands" error.

**Margin notes collide or float to the next page.**
Tufte margins are finite. Move long asides into the text, shorten sidenotes, or use
`\marginnote[<offset>]{…}` to nudge one vertically.
