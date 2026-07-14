"""Structured artist profile.

This is the "structured artist model" described in
docs/research/artist-style-modeling.md (Approach 4 / Approach 5) and
docs/architecture/system-design-notes.md (Q4): a human-readable,
human-editable document capturing an artist's identity across the
dimensions in that doc's table (themes, symbols, instrumentation, vocal
style, structural tendencies, eras, etc). It's the non-audio half of the
artist model; the embedded catalog (see retrieval.py) is the other half.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel


class Era(BaseModel):
    name: str
    albums: list[str] = []
    years: str | None = None
    notes: str | None = None


class Symbol(BaseModel):
    symbol: str
    meaning: str


class ArtistProfile(BaseModel):
    name: str
    slug: str
    sole_writer: bool = False
    eras: list[Era] = []
    themes: list[str] = []
    anti_themes: list[str] = []
    symbols: list[Symbol] = []
    instrumentation_present: list[str] = []
    instrumentation_absent: list[str] = []
    vocal_styles: list[str] = []
    rhetorical_habits: list[str] = []
    structural_tendencies: list[str] = []
    mythology_notes: str | None = None
    data_sources_note: str | None = None

    def as_context_block(self) -> str:
        """Render the profile into a compact text block for prompt injection."""
        lines = [f"Artist: {self.name}"]
        if self.sole_writer:
            lines.append(
                "Lyrics are written by a single, sole-credited writer — one "
                "consistent voice, no co-writer noise."
            )
        if self.eras:
            era_bits = "; ".join(
                f"{e.name} ({e.years or 'unknown years'}): {e.notes or ''}".strip()
                for e in self.eras
            )
            lines.append(f"Eras: {era_bits}")
        if self.themes:
            lines.append("Themes to draw from: " + ", ".join(self.themes))
        if self.anti_themes:
            lines.append(
                "Themes to AVOID (this artist reliably does not write about these): "
                + ", ".join(self.anti_themes)
            )
        if self.symbols:
            sym_bits = "; ".join(f"{s.symbol} = {s.meaning}" for s in self.symbols)
            lines.append(f"Recurring symbols/imagery: {sym_bits}")
        if self.instrumentation_present:
            lines.append("Sonic palette includes: " + ", ".join(self.instrumentation_present))
        if self.instrumentation_absent:
            lines.append("Notably avoids: " + ", ".join(self.instrumentation_absent))
        if self.vocal_styles:
            lines.append("Vocal delivery styles: " + ", ".join(self.vocal_styles))
        if self.rhetorical_habits:
            lines.append("Rhetorical/voice habits: " + ", ".join(self.rhetorical_habits))
        if self.structural_tendencies:
            lines.append("Structural tendencies: " + ", ".join(self.structural_tendencies))
        if self.mythology_notes:
            lines.append(f"Worldbuilding/mythology: {self.mythology_notes}")
        return "\n".join(lines)


def load_profile(data_dir: Path, artist_slug: str) -> ArtistProfile:
    path = data_dir / "artists" / artist_slug / "profile.json"
    if not path.exists():
        raise FileNotFoundError(f"No artist profile at {path}")
    raw = json.loads(path.read_text())
    return ArtistProfile(**raw)
