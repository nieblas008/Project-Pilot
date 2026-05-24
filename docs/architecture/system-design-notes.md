# System Design Notes

> Early architectural thinking. Mostly placeholder. Will become a real design document once the theory phase has settled the unknowns.

## Why this document is light right now

Architectural decisions made before you understand the problem space tend to be wrong, and worse, *committed*. The point of the long documentation phase is to defer these decisions until the research justifies them.

This file's job for now is to capture **architectural intuitions as they form**, so they're not lost — not to prescribe them.

## Status

**Sketch only. Update as research clarifies tradeoffs.**

---

## High-level component sketch

A first guess at the system shape — to be revised:

```
┌──────────────────────────────────────────────────────────────┐
│                       Artist Profile                          │
│  (structured: themes, instruments, eras, mythology, etc.)     │
│         + Embedded catalog (vector DB of songs)               │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    Generation Request                         │
│  (artist, era, theme, mood, target structure)                 │
└──────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼──────────────────┐
        ▼                   ▼                  ▼
   ┌─────────┐        ┌─────────┐        ┌──────────┐
   │ Lyrics  │        │ Symbolic│        │  Audio   │
   │   Gen   │───────▶│Music Gen│───────▶│ Renderer │
   │ (LLM +  │        │ (chords,│        │ (MusicGen│
   │  RAG)   │        │ melody, │        │  / Stable│
   │         │        │ structure)       │  Audio)  │
   └─────────┘        └─────────┘        └──────────┘
                            │
                            ▼
                  ┌─────────────────────┐
                  │   Final song bundle │
                  │ (audio + lyrics +   │
                  │  metadata)          │
                  └─────────────────────┘
```

The three generation stages are decoupled so each can be improved independently and so the cheap stages (lyrics) can be iterated without paying for expensive ones (audio).

## Architectural questions to resolve before committing

These are the questions the research phase should make answerable.

### Q1: Symbolic intermediate, or end-to-end?

Should there be an explicit symbolic (MIDI-ish) intermediate step between lyrics and audio? Pros: editability, inspectability, music-theory-aware control. Cons: extra system complexity, possible quality ceiling.

End-to-end is simpler but harder to control. Suno is end-to-end; that's why it can't be artist-controlled.

**Current intuition:** Symbolic intermediate is worth the complexity. Project Pilot needs control more than it needs simplicity.

### Q2: One artist model, or one model with artist conditioning?

Per-artist fine-tuned models scale badly but capture style deeply. Single conditioning-capable models scale well but may not capture as much.

**Current intuition:** Single base model + structured artist profiles + RAG. Per-artist fine-tunes only when the base approach proves insufficient.

### Q3: Build from scratch, or wrap existing models?

Build = control, originality, infinite time investment. Wrap = ship faster, depend on others' decisions, may need to switch when the wrapped model changes.

**Current intuition:** Wrap, heavily. Project Pilot's contribution is the artist-modeling layer and the orchestration, not the audio generation itself. Use MusicGen or Stable Audio as the audio backend.

### Q4: What does "the artist profile" actually look like in storage?

Options:
- A JSON document with structured fields.
- A directory of markdown files plus a vector DB.
- A custom data model with a query API.

**Current intuition:** Hybrid — markdown for human-readable parts (themes, mythology, era notes), JSON for structured features (instrument frequencies, era boundaries), vector DB for the embedded catalog.

### Q5: Where does evaluation live?

Evaluation needs to be a first-class component, not an afterthought. The fan-turing-test approach implies a human-in-the-loop. The system should make evaluation easy — A/B blind tests, scoring rubrics, side-by-side comparisons.

**Current intuition:** Build evaluation tooling in parallel with generation, not after. Even a simple "store generated songs in a labeled DB and provide a blind comparison UI" is enough for Phase 1.

---

## Tech stack guesses (highly provisional)

| Layer | Likely choice | Why |
|---|---|---|
| Language | Python | The entire ML ecosystem is Python; no real alternative for the kind of work this needs. |
| LLM access | Anthropic or OpenAI API for prototyping; local Llama via Ollama/vLLM for fine-tuning experiments | Frontier API for fast iteration, local for cost and control once approach is settled |
| Embeddings | sentence-transformers (text), CLAP/MERT (audio) | Mature, open, well-supported |
| Vector DB | Qdrant or LanceDB | Local-first, good Python support |
| Audio analysis | librosa, demucs (source separation) | Standard tools |
| Audio generation | MusicGen (HuggingFace), Stable Audio Open | Open source, controllable |
| Symbolic music | music21, mido, Magenta | Standard symbolic music libraries |
| Storage | Files + SQLite | Don't need a real DB yet |
| UI | Probably just CLI initially, maybe a small Gradio app for evaluation | Don't pre-optimize UI |

None of this is committed. The point of writing it is to have something concrete to push back on later.

---

## What this document should become

By the end of the documentation phase, this file (or a successor) should contain:

- A finalized component diagram.
- Justified tech stack choices.
- A schema for the artist profile.
- An API design for the generation request and response.
- A clear story for evaluation.
- A staged implementation plan that names files, classes, and roughly orders the work.

Until then, this is a notebook.

---

## Related documents

- [`../VISION.md`](../VISION.md) for what this system is supposed to *do*.
- [`../RESEARCH.md`](../RESEARCH.md) for what to learn before locking architecture.
- [`../research/ai-music-generation.md`](../research/ai-music-generation.md) for the menu of generation approaches.
- [`../research/artist-style-modeling.md`](../research/artist-style-modeling.md) for the artist-profile design space.
