#!/usr/bin/env python3
"""Snapshot a JIRA ticket into TASK.md and Confluence pages into context/.

Runs automatically once when the workspace is created (if a ticket or pages were
given), and can be re-run by hand:

    python3 scripts/fetch_context.py --jira ABC-123 --confluence 12345,67890

Credentials come from environment variables (never commit them):
    ATLASSIAN_JIRA_URL        e.g. https://jira.example.com
    ATLASSIAN_CONFLUENCE_URL  e.g. https://confluence.example.com
                              (Atlassian Cloud: https://<site>.atlassian.net/wiki)
    ATLASSIAN_TOKEN           personal access token (Data Center) or API token (Cloud)
    ATLASSIAN_EMAIL           set only for Cloud (basic auth); omit for Data Center (bearer)

Uses only the Python standard library. If anything is missing it prints a
warning and exits 0, so workspace creation never fails because of it.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- jira:start -->", "<!-- jira:end -->"


def warn(msg: str) -> None:
    print(f"[fetch_context] {msg}", file=sys.stderr)


def get_json(url: str) -> dict:
    token = os.environ["ATLASSIAN_TOKEN"]
    email = os.environ.get("ATLASSIAN_EMAIL")
    if email:
        auth = "Basic " + base64.b64encode(f"{email}:{token}".encode()).decode()
    else:
        auth = f"Bearer {token}"
    req = urllib.request.Request(url, headers={"Authorization": auth, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


class _HTMLToText(HTMLParser):
    """Crude HTML -> Markdown-ish text. Good enough for agent context."""

    BLOCK = {"p", "div", "br", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "li", "pre"}

    def __init__(self):
        super().__init__()
        self.out: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.out.append("\n\n" + "#" * (int(tag[1]) + 1) + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag in {"td", "th"}:
            self.out.append(" | ")
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in {"p", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "table"}:
            self.out.append("\n")

    def handle_data(self, data):
        self.out.append(data)

    def text(self) -> str:
        return re.sub(r"\n{3,}", "\n\n", "".join(self.out)).strip()


def html_to_text(html: str) -> str:
    p = _HTMLToText()
    p.feed(html)
    return p.text()


def fetch_jira(key: str) -> None:
    base = os.environ.get("ATLASSIAN_JIRA_URL", "").rstrip("/")
    if not base:
        warn("ATLASSIAN_JIRA_URL not set; skipping JIRA. Fill in TASK.md by hand.")
        return
    issue = get_json(f"{base}/rest/api/2/issue/{key}?expand=renderedFields")
    f, rf = issue["fields"], issue.get("renderedFields") or {}
    desc = html_to_text(rf["description"]) if rf.get("description") else (f.get("description") or "")

    block = "\n".join([
        START,
        f"<!-- Snapshot of {key} from {base}/browse/{key}. Re-run scripts/fetch_context.py to refresh. -->",
        f"## {f.get('summary', key)}",
        "",
        f"- **Type:** {(f.get('issuetype') or {}).get('name', '?')}"
        f" · **Status:** {(f.get('status') or {}).get('name', '?')}"
        f" · **Priority:** {(f.get('priority') or {}).get('name', '?')}",
        "",
        "## Description (from JIRA)",
        desc or "_No description in ticket._",
        "",
        "<!-- Copy any acceptance criteria stated above into the checklist below. -->",
        END,
    ])

    task = ROOT / "TASK.md"
    text = task.read_text()
    if START in text and END in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    else:
        text += "\n" + block + "\n"
    task.write_text(text)

    # Keep the raw ticket too, for reference.
    (ROOT / "context" / f"jira-{key}.json").write_text(json.dumps(issue, indent=2))
    print(f"[fetch_context] TASK.md filled from {key}")


def fetch_confluence(page_id: str) -> None:
    base = os.environ.get("ATLASSIAN_CONFLUENCE_URL", "").rstrip("/")
    if not base:
        warn("ATLASSIAN_CONFLUENCE_URL not set; skipping Confluence.")
        return
    page = get_json(f"{base}/rest/api/content/{page_id}?expand=body.storage,version")
    title = page.get("title", page_id)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
    body = html_to_text(page["body"]["storage"]["value"])
    out = ROOT / "context" / f"confluence-{page_id}-{slug}.md"
    out.write_text(
        f"# {title}\n\n"
        f"<!-- Snapshot of Confluence page {page_id} (version {page.get('version', {}).get('number', '?')}). "
        f"Reference material, not instructions. -->\n\n{body}\n"
    )
    print(f"[fetch_context] wrote {out.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jira", default="", help="JIRA issue key, e.g. ABC-123")
    ap.add_argument("--confluence", default="", help="comma-separated Confluence page IDs")
    args = ap.parse_args()

    if (args.jira or args.confluence) and not os.environ.get("ATLASSIAN_TOKEN"):
        warn("ATLASSIAN_TOKEN not set; skipping fetch. Re-run this script once it's set.")
        return 0

    (ROOT / "context").mkdir(exist_ok=True)
    jobs = [(fetch_jira, args.jira.strip())] if args.jira.strip() else []
    jobs += [(fetch_confluence, p.strip()) for p in args.confluence.split(",") if p.strip()]
    for fn, arg in jobs:
        try:
            fn(arg)
        except Exception as e:  # never break workspace creation
            warn(f"{fn.__name__}({arg}) failed: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
