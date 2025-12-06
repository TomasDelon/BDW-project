"""
Contrôleur pour la page Documentation.
Il convertit docs/documentation.md en HTML complet prêt à être affiché.
"""

from __future__ import annotations

import re
from html import unescape
from pathlib import Path
from typing import Optional

try:  # Markdown is optional but recommended; fallback to message if missing
    import markdown  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - only when dependency missing
    markdown = None  # type: ignore

try:  # Provide fallbacks when analysers import the module
    SESSION  # type: ignore  # noqa: F821
    REQUEST_VARS  # type: ignore  # noqa: F821
except NameError:  # pragma: no cover - executed only when server injects globals
    SESSION = {}
    REQUEST_VARS = {}


DOC_PATH = Path(__file__).resolve().parents[2] / "docs" / "documentation.md"
STYLE_BLOCK_RE = re.compile(r"<style.*?</style>", re.DOTALL | re.IGNORECASE)
MERMAID_BLOCK_RE = re.compile(
    r"<pre><code class=\"language-mermaid\">(.*?)</code></pre>",
    re.DOTALL,
)

_DOC_CACHE_HTML: str = ""
_DOC_CACHE_MTIME: Optional[float] = None


def _convert_mermaid_blocks(html: str) -> str:
    """Transforms fenced mermaid code blocks into <pre class="mermaid"> nodes."""

    def _replace(match: re.Match[str]) -> str:
        inner = unescape(match.group(1))
        return f'<pre class="mermaid">{inner}</pre>'

    return MERMAID_BLOCK_RE.sub(_replace, html)


def _render_documentation_html(source: str) -> str:
    """Render Markdown source to HTML string."""
    if markdown is None:
        return (
            "<p>"
            "Le module <code>Markdown</code> n'est pas installé. "
            "Exécutez <code>pip install Markdown</code> dans votre environnement pour "
            "afficher la documentation depuis le serveur."
            "</p>"
        )

    cleaned = STYLE_BLOCK_RE.sub("", source, count=1)
    html = markdown.markdown(
        cleaned,
        extensions=[
            "extra",
            "sane_lists",
            "toc",
            "fenced_code",
        ],
        output_format="html5",
    )
    return _convert_mermaid_blocks(html)


def _load_documentation_html() -> str:
    """Load and cache the rendered HTML for the documentation."""
    global _DOC_CACHE_HTML, _DOC_CACHE_MTIME

    try:
        mtime = DOC_PATH.stat().st_mtime
    except FileNotFoundError:
        return "<p>Le fichier de documentation est introuvable.</p>"

    if _DOC_CACHE_HTML and _DOC_CACHE_MTIME == mtime:
        return _DOC_CACHE_HTML

    source = DOC_PATH.read_text(encoding="utf-8")
    rendered = _render_documentation_html(source)
    _DOC_CACHE_HTML = rendered
    _DOC_CACHE_MTIME = mtime
    return rendered


REQUEST_VARS.setdefault("message", None)
REQUEST_VARS.setdefault("message_class", None)
REQUEST_VARS["documentation_html"] = _load_documentation_html()
