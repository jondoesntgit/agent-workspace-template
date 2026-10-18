"""Sphinx configuration for the agent-workspace-template documentation."""
import datetime

project = "agent-workspace-template"
author = "Jonathan Wheeler"
copyright = f"{datetime.date.today().year}, {author}"
release = "1.1.0"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinxcontrib.mermaid",
    "sphinx.ext.githubpages",  # writes .nojekyll for GitHub Pages
]

myst_enable_extensions = ["colon_fence", "deflist", "tasklist", "attrs_inline"]
myst_heading_anchors = 3
source_suffix = {".md": "markdown"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "requirements.txt"]

html_theme = "furo"
html_title = "Agent Workspace Template"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "source_repository": "https://github.com/jondoesntgit/agent-workspace-template",
    "source_branch": "main",
    "source_directory": "docs-site/",
    "light_css_variables": {"color-brand-primary": "#B2182B", "color-brand-content": "#2166AC"},
    "dark_css_variables": {"color-brand-primary": "#E3656F", "color-brand-content": "#6FA8DC"},
}

mermaid_version = "11"
mermaid_init_js = "mermaid.initialize({startOnLoad: true, theme: 'neutral'});"
