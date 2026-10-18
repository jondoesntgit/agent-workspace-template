# Installation

You need different tools depending on which variants you use. Everything is free
and runs on Windows, macOS, and Linux.

| Tool | Needed for | Required? |
|---|---|---|
| Python ≥ 3.9 + Copier | creating/updating workspaces | always |
| Git | versioning workspaces | always |
| Nimbus Sans font | plot text | always (plots fall back without it) |
| Python packages (`numpy`, `matplotlib`, `jupyterlab`) | plots, notebooks | `investigation`, plots in any variant |
| TeX distribution + `latexmk` | building papers | `paper` |
| Node.js + Mermaid CLI | rendering diagrams | if you use diagrams |
| Inkscape | annotating figures by hand | humans annotating |
| Atlassian access token | auto-pulling JIRA/Confluence | optional |

## Python and Copier

Install [pipx](https://pipx.pypa.io), then:

```bash
pipx install copier
copier --version   # 9.5 or newer
```

(`pip install copier` also works.) Inside a workspace, install the plotting stack:

```bash
pip install -r requirements.txt
```

## Fonts

The house style uses **Nimbus Sans** for all plot and caption text and
**Pagella** (a Palatino clone) for body text. LaTeX ships both; matplotlib
needs Nimbus Sans installed as a system font.

**Windows**
1. Download the `NimbusSans-*.otf` files from
   [ArtifexSoftware/urw-base35-fonts → fonts](https://github.com/ArtifexSoftware/urw-base35-fonts/tree/master/fonts)
   (Regular, Italic, Bold, BoldItalic).
2. Select them, right-click → **Install for all users**.
3. Clear matplotlib's font cache (below).

**macOS**: same download; double-click each file → **Install Font**.

**Debian/Ubuntu**: `sudo apt install fonts-urw-base35`

Then, once, clear matplotlib's cache so it notices the new font:

```bash
python -c "import matplotlib, shutil; shutil.rmtree(matplotlib.get_cachedir())"
```

Check it worked:

```bash
python -c "from matplotlib import font_manager as f; print(f.findfont('Nimbus Sans', fallback_to_default=False))"
```

`teamplot` prints a warning on first use if Nimbus Sans is missing; plots then fall
back to TeX Gyre Heros, Helvetica, or Arial and won't match the LaTeX captions.

## LaTeX (for `paper` workspaces)

Any modern TeX distribution works. The template uses pdfLaTeX with these packages:
`tufte-latex`, `newpx`, `helvet`, `beramono`, `microtype`, `siunitx`, `cleveref`,
`adjustbox`, `pdftexcmds`, `natbib`.

- **Windows:** [MiKTeX](https://miktex.org/download) (installs missing packages on first build)
  or [TeX Live](https://tug.org/texlive/windows.html). `latexmk` needs Perl; MiKTeX
  prompts for it, or install [Strawberry Perl](https://strawberryperl.com).
- **macOS:** [MacTeX](https://tug.org/mactex/).
- **Debian/Ubuntu:**
  `sudo apt install texlive-latex-extra texlive-fonts-extra texlive-science latexmk`

Build a paper from its folder:

```bash
cd paper && latexmk main.tex
```

## Mermaid CLI (for diagrams)

Install [Node.js](https://nodejs.org) (LTS), then:

```bash
npm install -g @mermaid-js/mermaid-cli@12
mmdc --version
```

The first run downloads a headless Chromium. **On locked-down machines** where that
download is blocked, point Mermaid at the browser you already have. Create a JSON file,
for example `%USERPROFILE%\mermaid-puppeteer.json`:

```json
{ "executablePath": "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" }
```

and set an environment variable so `scripts/render_diagrams.py` passes it along:

```powershell
setx MMDC_PUPPETEER_CONFIG "%USERPROFILE%\mermaid-puppeteer.json"
```

(On Linux containers you may also need `"args": ["--no-sandbox"]` in that JSON.)

If `mmdc` isn't on `PATH` but Node is, the script falls back to `npx @mermaid-js/mermaid-cli@12`.

## Inkscape (for annotating figures)

Install [Inkscape](https://inkscape.org/release/) 1.x. That's all; see {doc}`usage/annotations`.

## Atlassian credentials (optional)

To have the JIRA ticket and Confluence pages pulled in when a workspace is created,
set these environment variables (never commit them):

| Variable | Example | Notes |
|---|---|---|
| `ATLASSIAN_JIRA_URL` | `https://jira.example.com` | |
| `ATLASSIAN_CONFLUENCE_URL` | `https://confluence.example.com` | Cloud: `https://<site>.atlassian.net/wiki` |
| `ATLASSIAN_TOKEN` | `…` | Data Center: personal access token. Cloud: API token. |
| `ATLASSIAN_EMAIL` | `you@example.com` | **Cloud only** (switches to basic auth) |

On Windows: `setx ATLASSIAN_TOKEN "…"` (then open a new terminal). Without these,
workspace creation still succeeds and you fill in `TASK.md` by hand. See
{doc}`usage/jira-confluence`.
