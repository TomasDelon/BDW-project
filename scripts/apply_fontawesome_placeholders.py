#!/usr/bin/env python3
"""Replace Font Awesome placeholders inside Markdown files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PLACEHOLDER_MAP = {
    "::html": '<i class="fa-brands fa-html5" aria-hidden="true"></i>',
}


def build_pattern() -> re.Pattern[str]:
    escaped = (re.escape(key) for key in PLACEHOLDER_MAP)
    return re.compile("|".join(escaped))


def replace_placeholders(text: str, pattern: re.Pattern[str]) -> str:
    def repl(match: re.Match[str]) -> str:
        placeholder = match.group(0)
        return PLACEHOLDER_MAP.get(placeholder, placeholder)

    return pattern.sub(repl, text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Substitute Font Awesome placeholders.")
    parser.add_argument(
        "path",
        nargs="?",
        default=Path("docs/cosas.md"),
        type=Path,
        help="Markdown file to process (default: docs/cosas.md)",
    )
    args = parser.parse_args()

    if not args.path.exists():
        raise SystemExit(f"{args.path} does not exist.")

    pattern = build_pattern()
    content = args.path.read_text(encoding="utf-8")
    updated = replace_placeholders(content, pattern)

    if updated == content:
        print("No placeholders found; nothing to do.")
        return

    args.path.write_text(updated, encoding="utf-8")
    print(f"Applied {len(PLACEHOLDER_MAP)} placeholder(s) to {args.path}.")


if __name__ == "__main__":
    main()
