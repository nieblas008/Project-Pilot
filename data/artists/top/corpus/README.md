# Corpus data — legal & ethics reminder

This directory holds one JSON file per song, used to build the retrieval
index for the Phase 1 lyric generator (`project_pilot.retrieval`).

**Before adding real lyrics here, read [`docs/research/legal-and-ethics.md`](../../../../docs/research/legal-and-ethics.md).**
In short:

- Use official/licensed lyric sources, cross-checked against the band's own
  releases where possible — not scraped or pirated text.
- Keep this data, and anything generated from it, for personal,
  non-commercial use. Don't publish it.
- If the artist you're modeling has publicly opposed AI generation of their
  work, don't build a corpus for them — see the opt-out principle in
  `legal-and-ethics.md`.

The `_sample-*.json` files in this directory are **placeholder data** —
invented text used only to exercise the pipeline end-to-end (build an
index, retrieve, construct a prompt). They are **not real Twenty One
Pilots lyrics**. Delete them once you've added real, legally-sourced
material, or leave them out of any real generation run by filtering on
`era` (they use `"era": "sample"`, which doesn't match any real era in
`profile.json`).

## Schema

```json
{
  "id": "unique-slug",
  "title": "Song Title",
  "album": "Album Name",
  "era": "one of the era names in profile.json",
  "themes": ["theme-one", "theme-two"],
  "sections": [
    {"label": "verse", "lines": ["line one", "line two"]},
    {"label": "chorus", "lines": ["line one", "line two"]}
  ],
  "source": "where this text came from",
  "notes": "optional free text"
}
```

After adding or changing files here, rebuild the index:

```
python -m project_pilot.cli index --artist top
```
