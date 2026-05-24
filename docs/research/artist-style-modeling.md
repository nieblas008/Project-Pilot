# Artist Style Modeling

> The original contribution of Project Pilot. How do you capture, represent, and reuse the "essence" of an artist computationally?

## Why this matters for Project Pilot

This is the heart of the project. The other docs cover what already exists. This one is about the gap: existing systems don't really model individual artists with fidelity. Jukebox tried it crudely. Suno doesn't try. Building this layer well is what makes Project Pilot different from "Suno but worse."

## Status

**Sketch + research notes.** This is the most open-ended part of the project.

---

## What "an artist's style" actually contains

For computational modeling, it helps to enumerate the dimensions. An artist's identity is a composite of at least:

| Dimension | What it captures | Where it can be extracted from |
|---|---|---|
| **Lyrical voice** | Word choice, sentence structure, rhetorical habits | The text of the lyrics |
| **Lyrical themes** | What they write about (and don't) | Topic modeling over lyrics, interviews |
| **Worldbuilding** | Ongoing mythology, characters, recurring symbols | Albums-as-narratives, fan wikis, interviews |
| **Sonic palette** | Instruments used, timbres, synth sounds | Audio analysis (MIR) over catalog |
| **Production aesthetic** | Mix style, reverb/space, dynamics, density | Audio analysis, ideally with isolated stems |
| **Structural habits** | Song forms, section lengths, deviations from norms | Annotated song structure data |
| **Harmonic/melodic tendencies** | Key choices, chord vocabulary, melodic shapes | Symbolic analysis (transcription → MIDI) |
| **Rhythmic feel** | Tempo ranges, groove, meter use, syncopation | MIR (tempo/beat tracking) |
| **Vocal style** | Range, techniques, delivery types, effects | Isolated vocal stem analysis |
| **Collaborative footprint** | Solo writer, frequent collaborators, producers | Discography metadata |
| **Career arc** | Era-to-era evolution | Catalog organized by time |

This is the *target representation* the system needs. Each row is a sub-problem.

---

## Music Information Retrieval (MIR): the tool kit

MIR is the academic discipline that gives us computational tools for analyzing music. Anything Project Pilot does at the audio level rests on MIR. ([Wikipedia overview](https://en.wikipedia.org/wiki/Music_information_retrieval))

### Core audio features

- **Spectrograms / mel-spectrograms** — frequency content over time. The fundamental representation for most modern audio ML.
- **MFCCs (Mel-Frequency Cepstral Coefficients)** — compressed timbre representation. Workhorse feature for genre/instrument classification.
- **Chroma features** — energy per pitch class (C, C#, D, ...). Useful for harmonic analysis without caring about octave.
- **Tempo / beat tracking** — detect BPM and beat positions.
- **Key detection** — identify the key of a piece.
- **Onset detection** — find note start times.
- **Pitch tracking** — extract melodic pitch over time.

The `librosa` Python library implements all of these. Start there.

### Higher-level MIR tasks

- **Genre classification** — predict genre from audio.
- **Mood/emotion classification** — sad, happy, energetic, calm, etc.
- **Instrument identification** — what instruments are playing.
- **Source separation** — isolate vocals, drums, bass, other (Spleeter, Demucs).
- **Artist classification** — given an audio clip, predict the artist. Yes, this is a real task with benchmarks.
- **Cover song detection.**
- **Audio fingerprinting** (Shazam).

### Modern embeddings

The current best practice for representing audio is learned embeddings:

- **CLAP (Contrastive Language-Audio Pretraining)** — joint text-audio embedding space. Lets you do "find audio that matches this description" or vice versa.
- **MERT** — Music understanding model with strong embeddings for music-specific tasks.
- **MusicNN** — Earlier CNN-based music tagging model with usable intermediate embeddings.
- **CLaMP 3** — Aligns sheet music, MIDI, audio, and multilingual text in a joint embedding space.
- **Wav2Vec2 / HuBERT** — Speech-focused but useful starting points for vocal analysis.

For Project Pilot, embeddings are the substrate of the artist-modeling layer: every song in an artist's catalog becomes a vector (or set of vectors), and "the artist" becomes a distribution in embedding space.

---

## Approaches to capturing an artist computationally

### Approach 1: Direct fine-tuning

Take an existing generative model (MusicGen for audio, an LLM for lyrics) and fine-tune on the artist's catalog. The model learns the artist's style implicitly in its weights.

**Pros:** Conceptually simple. End-to-end. Captures style deeply.

**Cons:** Computationally expensive. Hard to update incrementally. One model per artist doesn't scale. Hard to inspect what the model "knows" about the artist.

### Approach 2: Conditioning on artist embeddings

Train a single model that takes an "artist embedding" as input. The embedding is learned from the artist's catalog (e.g., averaged CLAP embeddings of their songs, or learned via metric learning over a multi-artist corpus).

**Pros:** Scales across artists. Cheap to add new artists (just compute their embedding). Conceptually clean.

**Cons:** Embeddings may not be expressive enough to capture deep style. Quality is bottlenecked by how well the embedding represents the artist.

This is roughly what Jukebox did. It worked but unevenly.

### Approach 3: Retrieval-augmented generation (RAG)

Keep the artist's catalog as a structured corpus. For each generation request, retrieve relevant examples and condition the generator on them.

**Pros:** No training. Easy to update. Naturally handles era/style filtering. Inspectable.

**Cons:** Quality bottlenecked by retrieval. Less stylistically "deep" than fine-tuning.

### Approach 4: Structured artist model + base generator

Don't bury the artist in weights. Instead, build an explicit, structured representation of the artist (the table at the top of this doc, filled in) and use that to construct prompts/conditions for a base generative model.

**Pros:** Inspectable, editable, debuggable. Lets human knowledge augment data-driven analysis (you can manually add "TØP's mythology includes Clancy"). Composable — you can ask "what would this artist do *if* their producer changed?".

**Cons:** Requires a lot of manual structuring. Probably can't capture everything the data contains.

### Approach 5: Hybrid

In practice, the right system probably combines: a structured artist model (Approach 4) for inspectability and worldbuilding, RAG (Approach 3) for cheap stylistic grounding, and lightweight fine-tuning (Approach 1) where the data supports it.

This is the architecture Project Pilot should aim for.

---

## A proposed artist-modeling pipeline

For any new artist, the system should be able to ingest their catalog and produce a structured artist model. Sketch:

```
Input: artist name, catalog (audio + lyrics + metadata)
   ↓
Audio analysis (MIR pipeline):
   - Extract embeddings per song (CLAP, MERT)
   - Extract tempo, key, time signature
   - Extract instrumentation features
   - Run source separation; analyze vocal stems separately
   - Aggregate to artist-level statistics
   ↓
Lyric analysis:
   - Embed all lyrics
   - Topic modeling (themes)
   - Vocabulary and rhetorical analysis
   - Detect recurring symbols/imagery
   - Detect named entities (characters, places — mythology)
   ↓
Structural analysis:
   - Section detection (verse/chorus/bridge)
   - Section-length distributions
   - Common structural templates
   ↓
Metadata analysis:
   - Collaborators, producers
   - Era timeline
   ↓
Output: structured artist profile (JSON/document) + embedded catalog (vector DB)
```

The structured profile is human-readable and editable; the embedded catalog enables retrieval. Together, they're the input to the generation system.

---

## Open research questions

- **How few songs is enough?** TØP has ~80 released songs. Some artists have 500+. Some have 12. Where's the floor for credible style capture?
- **How do you handle artist evolution?** A single profile averages over eras, possibly badly. Per-era profiles add complexity but probably better fidelity.
- **Can the structured profile capture subtext?** Probably not directly. May need a separate symbolic/narrative layer.
- **How do you evaluate the profile itself?** Not just the generated output, but whether the profile captures what fans intuit.
- **Cross-artist transfer.** Can a profile learned from a well-studied artist help bootstrap a profile for a less-studied one?

---

## Implications for the broader system

The artist-modeling layer is what differentiates Project Pilot from existing tools. It should be:

- **Inspectable.** A user can read the profile and understand what the system thinks the artist is.
- **Editable.** A human expert can override or augment the data-driven analysis.
- **Composable.** The same profile feeds the lyric generator, melody generator, and audio renderer.
- **Versioned.** As artists release new material, profiles update; old versions should be retrievable.
- **Portable.** A profile shouldn't be locked to one generation backend. As models change, profiles should still work.

---

## Recommended next reads

- [Music information retrieval — Wikipedia overview](https://en.wikipedia.org/wiki/Music_information_retrieval) — start broad.
- The `librosa` library docs and tutorials.
- The ISMIR (International Society for Music Information Retrieval) conference proceedings — open access; the source of most modern MIR research.
- The CLAP paper for understanding modern audio embeddings.
- The MERT paper for a music-specific embedding model.
