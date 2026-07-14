"""Prompt construction for the Phase 1 lyric generator.

Implements the "Prompt construction" stage from the pipeline sketch in
docs/research/ai-lyric-generation.md: artist context + retrieved examples +
structural target + theme + mood, requesting section-labeled structured
output.
"""

from __future__ import annotations

from .artist_profile import ArtistProfile
from .corpus import Song

OUTPUT_SCHEMA_HINT = """
Respond with ONLY a JSON object (no markdown fences, no commentary) matching this shape:
{
  "title": "string",
  "sections": [
    {"label": "verse|pre-chorus|chorus|bridge|outro", "lines": ["line 1", "line 2", ...]}
  ],
  "notes": "1-3 sentences on the intended subtext/theme choices, for the human reviewer"
}
"""


def build_system_prompt(profile: ArtistProfile) -> str:
    return (
        "You are a careful songwriting collaborator helping a fan explore what a specific "
        "artist's lyrics might sound like, for personal, non-commercial study. This output "
        "will not be published or presented as the artist's own work.\n\n"
        "Write lyrics that feel true to this artist's documented voice, themes, and habits. "
        "Stay inside the artist's known themes and avoid the artist's anti-themes. Favor "
        "lyrics that work on two levels: legible emotionally on first read, and rewarding on "
        "a second, closer read — avoid flat, single-level lyrics.\n\n"
        f"{profile.as_context_block()}"
    )


def build_user_prompt(
    retrieved: list[Song],
    theme: str,
    mood: str,
    structure: list[str],
    era: str | None,
) -> str:
    parts: list[str] = []
    if retrieved:
        parts.append(
            "Reference examples from the artist's own catalog (for voice/structure — "
            "do not copy lines verbatim):"
        )
        for song in retrieved:
            excerpt = "\n\n".join(f"[{s.label}]\n{s.text()}" for s in song.sections)
            parts.append(f"--- {song.title} ({song.era or 'unknown era'}) ---\n{excerpt}")
    else:
        parts.append(
            "No reference examples were retrieved (the corpus may be empty or sparse "
            "for this era/theme). Rely on the artist context above."
        )

    parts.append("\nGeneration request:")
    parts.append(f"- Theme: {theme}")
    parts.append(f"- Mood: {mood}")
    parts.append(f"- Structure: {' -> '.join(structure)}")
    if era:
        parts.append(f"- Target era: {era}")
    parts.append(OUTPUT_SCHEMA_HINT)
    return "\n".join(parts)
