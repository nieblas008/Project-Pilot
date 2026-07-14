# Project Pilot

> An AI system for generating music that stays true to the artistic identity of a chosen artist or band.

## What this is

Project Pilot is an early-stage research project exploring how an AI system might generate music — full songs, lyrics, instrumentation, production choices — that feels authentically inspired by a specific artist. Not a generic "song in the style of X," but something that respects the artist's themes, sonic signatures, lyrical voice, and creative tendencies.

The project is named after twenty one pilots, which serves as the canonical case study (see [`docs/case-studies/twenty-one-pilots.md`](docs/case-studies/twenty-one-pilots.md)), but the system is being designed to generalize: any artist with enough available material (catalog, interviews, public writing) should be modelables

## What this is *not*

- **Not a replacement for human artists.** The goal is to fill the gap between releases, not to compete with the artists themselves.
- **Not a "make a hit" tool.** Project Pilot is built around fidelity to an artist's identity, not chart performance.
- **Not a clone-and-publish system.** Generated material is treated as fan output / personal use. Legal and ethical questions around training data, derivative works, and likeness are taken seriously — see [`docs/research/legal-and-ethics.md`](docs/research/legal-and-ethics.md).

## Why this exists

Good music takes time. Artists with cohesive identities — twenty one pilots, Radiohead, Phoebe Bridgers, Kendrick Lamar, etc. — release on the order of one album every few years. Fans wait. Project Pilot is an experiment in whether an AI system can produce additional material that feels truthful to an artist's identity in those gaps, in a way that respects what made the original work meaningful.

## Current status: theory and research, Phase 1 scaffold started

The project spent its first stretch in a **documentation-and-learning phase**, building theoretical grounding in:

1. **Music** — theory, composition, production, instrumentation, songwriting.
2. **AI music generation** — what's been tried, what works, what doesn't.
3. **Artist style modeling** — how to capture and reproduce an artist's identity computationally.

A first-pass implementation of **Phase 1 (lyrics)** now exists in [`project_pilot/`](project_pilot/): a retrieval-augmented lyric generator following the pipeline in [`docs/research/ai-lyric-generation.md`](docs/research/ai-lyric-generation.md) — structured artist profile + embedded catalog retrieval + prompt construction + LLM generation + naive filters. See that directory and [`data/artists/top/`](data/artists/top/) to get started; the seeded corpus is placeholder data only (see [`data/artists/top/corpus/README.md`](data/artists/top/corpus/README.md)) pending real, legally-sourced lyrics per [`docs/research/legal-and-ethics.md`](docs/research/legal-and-ethics.md). The research documentation continues to grow alongside it — theory and implementation are proceeding together now rather than strictly sequentially.

## Documentation map

All documentation lives in [`docs/`](docs/). Read in roughly this order:

| Document | What it covers |
|---|---|
| [`docs/VISION.md`](docs/VISION.md) | The full project vision, principles, and what success looks like. |
| [`docs/RESEARCH.md`](docs/RESEARCH.md) | The opinionated learning roadmap — what to study, in what order, and why. |
| [`docs/research/music-theory.md`](docs/research/music-theory.md) | Music theory fundamentals (scales, chords, rhythm, harmony, form). |
| [`docs/research/songwriting-and-lyrics.md`](docs/research/songwriting-and-lyrics.md) | How songs are structured, how lyrics are written, rhyme/meter/theme. |
| [`docs/research/instruments-and-production.md`](docs/research/instruments-and-production.md) | Instrumentation, arrangement, DAWs, mixing, mastering. |
| [`docs/research/ai-music-generation.md`](docs/research/ai-music-generation.md) | Survey of AI music systems (Jukebox, MusicGen, Suno, Udio, AudioLDM, Stable Audio, etc.) and the architectures behind them. |
| [`docs/research/ai-lyric-generation.md`](docs/research/ai-lyric-generation.md) | LLM-based lyric generation, rhyme/meter conditioning, theme control. |
| [`docs/research/artist-style-modeling.md`](docs/research/artist-style-modeling.md) | Music Information Retrieval, embeddings, and how to capture an artist's "essence." |
| [`docs/research/legal-and-ethics.md`](docs/research/legal-and-ethics.md) | Copyright, training data, derivative works, artist consent. |
| [`docs/case-studies/twenty-one-pilots.md`](docs/case-studies/twenty-one-pilots.md) | The canonical test case — what makes TØP TØP, and what the system would need to capture. |
| [`docs/architecture/system-design-notes.md`](docs/architecture/system-design-notes.md) | Early thinking about how the components might fit together. Mostly placeholder for now. |

## Roadmap

- **Phase 0 — Documentation & learning.** Fill out the research docs. Build personal understanding of music theory, songwriting, and the AI music landscape. Ongoing, in parallel with Phase 1 now.
- **Phase 1 — Lyrics first (in progress).** Build a system that generates lyrics in the voice of a chosen artist. This is the cheaper, more tractable starting point and validates the artist-modeling approach. Initial scaffold: [`project_pilot/`](project_pilot/).
- **Phase 2 — Symbolic music (MIDI).** Generate chord progressions and melodies in an artist's style using symbolic representations. Cheaper than audio, easier to evaluate, gives compositional control.
- **Phase 3 — Audio generation.** Either integrate with an existing model (MusicGen, Stable Audio) or build a thinner layer on top. Likely artist-conditioning via fine-tuning or retrieval.
- **Phase 4 — End-to-end system.** Lyrics + melody + arrangement + production, with the artist-modeling layer steering all of it.

The roadmap is provisional. It will change as the research clarifies what's actually feasible.

## How to contribute

If you're reading this and find the project interesting, please reach out, all help will be greatly appreciated.

The documents are meant to grow. They are the source code for the eventual implementation.

[![Get in touch](https://img.shields.io/badge/Get%20in%20touch-hello@ricardonieblas.com-2450D6?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hello@ricardonieblas.com)