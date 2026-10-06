"""Guard against CARTO basemap tiles creeping back into the site.

Since ~Aug 2026 CARTO serves its keyless ``basemaps.cartocdn.com`` tiles with
an "API KEY REQUIRED" watermark while still returning HTTP 200, so the
``try/except`` around the basemap calls never fires. These tests fail if:

1. any rendered or source file references ``cartocdn`` without an API key, or
2. a source ``.qmd`` / ``.py`` / ``.ipynb`` re-introduces a CARTO tile provider
   (contextily or a folium CartoDB tile layer) — those bake a watermark into a
   static PNG where no text search could ever catch it.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
QUARTO = REPO / "quarto"
SELF = Path(__file__).resolve()

# Build caches, vendored JS libs, and VCS internals are not content we control.
_SKIP_DIRS = {
    "_freeze",
    ".quarto",
    "site_libs",
    "__pycache__",
    ".git",
    "node_modules",
    ".ruff_cache",
    ".pytest_cache",
    "_site",
}
_TEXT_SUFFIXES = {".qmd", ".html", ".js", ".yml", ".yaml", ".py"}
_PROVIDER_SUFFIXES = {".qmd", ".py", ".ipynb"}

# A cartocdn reference is only acceptable if it carries an API key.
_KEY_TOKENS = ("key=", "apikey", "api_key", "access_token")

# Source patterns that select a CARTO tile provider (→ watermarked output).
_CARTO_PROVIDER = re.compile(r"providers\.CartoDB|TileLayer\(\s*[\"']CartoDB")


def _scan(root, suffixes, skip_site=False):
    for path in root.rglob("*"):
        if path.suffix not in suffixes:
            continue
        if path.resolve() == SELF:
            continue
        parts = path.relative_to(root).parts
        skip = set(_SKIP_DIRS)
        if not skip_site:
            skip.discard("_site")
        if any(part in skip for part in parts):
            continue
        yield path


def _read(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def test_no_keyless_cartocdn_references():
    offenders = {}
    # Scan the rendered site and quarto sources (keep _site in scope here).
    for path in _scan(QUARTO, _TEXT_SUFFIXES, skip_site=False):
        hits = [
            line.strip()
            for line in _read(path).splitlines()
            if "cartocdn" in line.lower() and not any(tok in line.lower() for tok in _KEY_TOKENS)
        ]
        if hits:
            offenders[str(path.relative_to(REPO))] = hits[:3]
    assert not offenders, "Keyless CARTO tiles (watermarked since Aug 2026) found in: " + repr(
        offenders
    )


def test_no_carto_tile_provider_in_sources():
    offenders = {}
    # Scan all notebook/script/qmd sources across the repo (skip _site/build dirs).
    for path in _scan(REPO, _PROVIDER_SUFFIXES, skip_site=True):
        hits = [line.strip() for line in _read(path).splitlines() if _CARTO_PROVIDER.search(line)]
        if hits:
            offenders[str(path.relative_to(REPO))] = hits[:3]
    assert not offenders, (
        "CARTO tile provider reintroduced (bakes a watermark into static maps): " + repr(offenders)
    )
