"""Post-generation filters.

This is a deliberately naive first pass at the "Filters" stage in the
Phase 1 pipeline (docs/research/ai-lyric-generation.md). It's a starting
point, not a solved problem — see that doc's "Worldbuilding consistency"
and "Subtext and double meanings" sections for what a real version needs
to handle (canon checks, critic-model subtext scoring, etc).
"""

from __future__ import annotations

import re

_STOPWORDS = {
    "a", "an", "the", "as", "primary", "subject", "topics", "and", "or", "of",
    "to", "for", "about", "directly", "mostly", "some", "commentary",
}


def _keywords(phrase: str) -> list[str]:
    words = re.findall(r"[a-zA-Z']+", phrase.lower())
    return [w for w in words if w not in _STOPWORDS and len(w) > 3]


def anti_theme_check(lyrics_text: str, anti_themes: list[str]) -> list[str]:
    """Flag naive keyword overlap between generated lyrics and the artist's anti-themes.

    This is intentionally crude (keyword overlap, not semantic understanding) — a
    real version needs a second-pass LLM judge, per the "Critic model" idea in
    docs/research/ai-lyric-generation.md.
    """
    lowered = lyrics_text.lower()
    warnings = []
    for anti_theme in anti_themes:
        hits = [kw for kw in _keywords(anti_theme) if kw in lowered]
        if hits:
            warnings.append(
                f"Possible anti-theme drift toward '{anti_theme}' (matched: {', '.join(hits)})"
            )
    return warnings


def canon_check(lyrics_text: str, mythology_notes: str | None) -> list[str]:
    """Placeholder for worldbuilding/canon consistency checking.

    TODO: this needs an actual structured knowledge base of the artist's
    mythology (characters, places, established events) and a verification
    pass — not a stub. See docs/research/ai-lyric-generation.md's
    "Worldbuilding consistency" section.
    """
    del lyrics_text, mythology_notes  # unused until the real check is built
    return []
