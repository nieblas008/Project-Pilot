"""Persisting generated songs for later evaluation.

Implements the minimal version of "build evaluation tooling in parallel with
generation, not after" from docs/architecture/system-design-notes.md (Q5):
every generation gets archived as a labeled, timestamped file so a human can
later browse them or set up a blind comparison against real catalog songs.
This is intentionally simple (flat JSON files, no UI) — see Q5 for what a
fuller version (a real labeled DB + comparison UI) should grow into.

Archived generations are gitignored: this is a public repo, and
docs/research/legal-and-ethics.md is explicit that generated material
imitating a real artist should stay personal, not be published.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "untitled"


def save_generation(data_dir: Path, artist_slug: str, result: dict[str, Any]) -> Path:
    generations_dir = data_dir / "artists" / artist_slug / "generations"
    generations_dir.mkdir(parents=True, exist_ok=True)

    request = result.get("request", {})
    label = _slugify(f"{request.get('theme', '')}-{request.get('mood', '')}")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    path = generations_dir / f"{timestamp}__{label}.json"
    path.write_text(json.dumps({"generated_at": timestamp, **result}, indent=2))
    return path
