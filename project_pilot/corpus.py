"""Loading and representing an artist's lyric corpus.

Each song is one JSON file inside data/artists/<slug>/corpus/. See the
README.md in that directory for the schema and for the legal/ethical
reminder about sourcing lyrics (docs/research/legal-and-ethics.md).
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel


class Section(BaseModel):
    label: str  # e.g. "verse", "pre-chorus", "chorus", "bridge", "outro"
    lines: list[str]

    def text(self) -> str:
        return "\n".join(self.lines)


class Song(BaseModel):
    id: str
    title: str
    album: str | None = None
    era: str | None = None
    themes: list[str] = []
    sections: list[Section]
    source: str | None = None
    notes: str | None = None

    def full_text(self) -> str:
        """Flatten the song into a single string for embedding."""
        parts = [self.title]
        if self.themes:
            parts.append("Themes: " + ", ".join(self.themes))
        for section in self.sections:
            parts.append(f"[{section.label}]\n{section.text()}")
        return "\n\n".join(parts)


def load_corpus(corpus_dir: Path) -> list[Song]:
    songs = []
    for path in sorted(corpus_dir.glob("*.json")):
        raw = json.loads(path.read_text())
        songs.append(Song(**raw))
    return songs
