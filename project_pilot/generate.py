"""End-to-end Phase 1 lyric generation.

Wires together retrieval -> prompt construction -> LLM generation -> filters,
matching the pipeline sketch in docs/research/ai-lyric-generation.md.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from .artist_profile import load_profile
from .filters import anti_theme_check, canon_check
from .prompt import build_system_prompt, build_user_prompt
from .retrieval import load_index_for_artist

DEFAULT_MODEL = os.environ.get("PROJECT_PILOT_MODEL", "claude-sonnet-5")


class GenerationParseError(Exception):
    """Raised when the model's response couldn't be parsed as the expected JSON shape."""


def _extract_json(text: str) -> dict[str, Any]:
    """The model is asked for raw JSON; be lenient about how it might wrap it anyway.

    Tries, in order: the whole response as-is, a fenced ```json ... ``` block, and
    finally the outermost {...} substring (in case the model added stray prose before
    or after the object despite instructions not to).
    """
    stripped = text.strip()
    candidates = [stripped]

    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", stripped, re.DOTALL)
    if fenced:
        candidates.append(fenced.group(1))

    first_brace, last_brace = stripped.find("{"), stripped.rfind("}")
    if first_brace != -1 and last_brace > first_brace:
        candidates.append(stripped[first_brace : last_brace + 1])

    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise GenerationParseError(
        f"Could not parse a JSON object out of the model's response:\n{text}"
    )


def generate_lyrics(
    data_dir: Path,
    artist_slug: str,
    theme: str,
    mood: str,
    structure: list[str],
    era: str | None = None,
    top_k: int = 5,
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    profile = load_profile(data_dir, artist_slug)
    index = load_index_for_artist(data_dir, artist_slug)
    retrieved = index.retrieve(query=f"{theme} {mood}", top_k=top_k, era=era)

    system_prompt = build_system_prompt(profile)
    user_prompt = build_user_prompt(retrieved, theme, mood, structure, era)

    import anthropic  # deferred: only needed once we actually call the API

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    response = client.messages.create(
        model=model,
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw_text = "".join(block.text for block in response.content if block.type == "text")
    parsed = _extract_json(raw_text)

    full_text = "\n".join(
        line for section in parsed.get("sections", []) for line in section.get("lines", [])
    )
    warnings = anti_theme_check(full_text, profile.anti_themes)
    warnings += canon_check(full_text, profile.mythology_notes)

    return {
        "artist": profile.name,
        "request": {"theme": theme, "mood": mood, "structure": structure, "era": era},
        "retrieved_song_ids": [song.id for song in retrieved],
        "generated": parsed,
        "filter_warnings": warnings,
        "model": model,
    }
