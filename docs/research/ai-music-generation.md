# AI Music Generation: Survey

> A working survey of the current AI music generation landscape — what's been built, how it works, and what's relevant to Project Pilot.

## Why this matters for Project Pilot

You can't build the right system if you don't know what other people have already built. This document is the reference map: the major systems, the approaches that work, the dead ends, and which of these can be borrowed from for an artist-fidelity system.

## Status

**Solid starting survey, needs ongoing updates.** The field is moving fast — expect this to be partially outdated within a year of writing. Re-check before making architectural decisions.

---

## The two paradigms

Almost every AI music system is one of two things:

1. **Symbolic** — generates MIDI-like representations (note events: pitch, start time, duration, velocity, instrument).
2. **Audio** — generates raw waveforms or compressed audio tokens directly.

The tradeoffs are large enough that they deserve their own section.

### Symbolic systems

**Pros:**
- Small representation. A song is hundreds or thousands of note events, not millions of audio samples.
- Editable. You can render it on any instrument; you can change the key; you can manually fix things.
- Structurally clean. Music theory concepts (chords, keys, modes) are visible in the representation.

**Cons:**
- Loses everything that isn't a note event: timbre, microtiming, expressive performance, vocals.
- You still need a synthesis step to *hear* the output, and that step is non-trivial.
- Hard to capture artist identity that lives in production (which is most of it).

### Audio systems

**Pros:**
- Capture everything — timbre, vocals, production, microtiming, vibe.
- The output is the deliverable. No render step.

**Cons:**
- Enormously larger representation. 1 second of CD-quality stereo audio = 88,200 samples.
- Generation is computationally expensive (minutes of GPU time per song).
- Hard to edit; usually you regenerate rather than modify.
- Easier to get unnatural artifacts.

### The middle ground: tokenized audio

Modern systems (MusicGen, AudioLM, Suno, Udio) sidestep the raw-audio problem by using **neural audio codecs** (EnCodec, SoundStream) to compress audio into a discrete token stream that a language model can predict. This is the closest the field has come to "GPT but for music." It gets you most of the benefits of audio with much of the tractability of symbolic.

For Project Pilot, the likely path is **symbolic in Phase 2, tokenized audio in Phase 3**.

---

## The major systems

### OpenAI Jukebox (2020)

The first system to credibly generate full songs *including singing* in the raw audio domain, with conditioning on artist and genre.

**How it works:** Hierarchical VQ-VAE (three levels of compression) plus an autoregressive Sparse Transformer over the discrete codes. Conditions on artist/genre metadata via a learned embedding. ([paper](https://arxiv.org/abs/2005.00341))

**Why it mattered:** First proof that audio-domain generation could capture singing voices and song structure. Artist-conditioning was a genuine novel contribution.

**Why it's mostly a historical reference now:** Generation is extremely slow (~9 hours of GPU for ~1 minute of audio). Quality is below modern standards. But the *idea* of conditioning generation on artist identity is exactly the Project Pilot problem, so the paper is worth reading carefully.

### Meta MusicGen (2023)

The current open-source reference model for text-to-music.

**How it works:** Uses EnCodec to tokenize audio at 32kHz with 4 codebooks at 50Hz. A single transformer LM predicts the next codes autoregressively. Conditions on text via a T5 text encoder and (optionally) on a melody via chromagram features extracted from reference audio. ([architecture overview](https://medium.com/@AIBites/musicgen-from-meta-ai-model-architecture-vector-quantization-and-model-conditining-explained-f9a030382f7d))

**Why it matters for Project Pilot:** It's open source, runnable on consumer GPUs (the small/medium models), and the melody-conditioning capability is exactly the kind of hook you want for artist-style work. Fine-tuning MusicGen on a specific artist's catalog is a plausible Phase 3 approach.

**Limitations:** Instrumental only — no singing vocals. 30-second clips by default. Quality lags behind closed-source systems.

### Suno (current)

The market leader as of 2026. Generates full songs including realistic vocals, in a single end-to-end pass. ([overview](https://www.chartlex.com/blog/marketing/ai-music-generator-comparison-2026))

**Why it matters:** This is the bar. Anything Project Pilot generates will be implicitly compared against Suno output by listeners. The v5 release closed most of the "AI vocal" gap.

**Why it's not a direct path forward:** Closed source. Active litigation. No artist-fidelity controls — you can prompt for a style but you can't tell it "in the voice of X" without violating the platform's terms.

**What to learn from it:** The end-to-end approach (lyrics + melody + arrangement + vocals + production in one pass) is clearly viable. But it sacrifices the kind of control Project Pilot needs.

### Udio (current)

Closer competitor to Suno, with a different emphasis: instrument fidelity, controllable editing (inpainting), and a recent UMG licensing deal that suggests a cleaner legal future. ([overview](https://www.tldl.io/blog/suno-vs-udio-comparison))

**Why it matters for Project Pilot:** The inpainting capability — fixing a specific section without regenerating the whole track — is the kind of editing workflow Project Pilot eventually wants. The UMG deal also suggests a precedent for legitimate artist-licensed generation, which is the world Project Pilot would ideally exist in.

### AudioLDM / Stable Audio (latent diffusion approaches)

Different paradigm: latent diffusion models for audio.

**AudioLDM** uses a VAE to compress audio into a latent space, then runs a U-Net diffusion model over those latents, conditioned on CLAP text embeddings. Decoded with HiFi-GAN. ([paper](https://arxiv.org/abs/2301.12503))

**Stable Audio** (from Stability AI) is a timing-conditioned latent diffusion model that can generate up to 95 seconds of 44.1kHz stereo in ~8 seconds on an A100. Much faster than autoregressive approaches. ([paper](https://arxiv.org/pdf/2402.04825))

**Why these matter:** Diffusion is fundamentally different from autoregressive generation. It's much faster, can be conditioned with more control (you can do classifier-free guidance, you can edit), and is the dominant paradigm in image generation. Whether it eclipses autoregressive in audio is still an open question.

### Riffusion

A clever hack: train Stable Diffusion (the image model) on spectrogram images of music. Generate spectrograms, convert back to audio. Works surprisingly well for short clips.

**Why it's relevant:** Demonstrates that spectrogram-based representations open the door to using the entire image-generation toolkit for audio. Probably not the right path for Project Pilot but worth knowing about.

### Symbolic-domain systems

- **Magenta (Google)** — long-running research project; has produced MusicVAE, MelodyRNN, Music Transformer, etc. Mostly symbolic/MIDI.
- **MuseNet (OpenAI, 2019)** — transformer-based symbolic music generation; predates Jukebox. Could generate 4-minute pieces with up to 10 instruments.
- **AIVA, Soundraw, Beatoven, Mubert** — commercial symbolic-ish tools for background/stock music.

**Why these matter:** For Phase 2 of Project Pilot (symbolic generation), the Magenta toolkit and Music Transformer paper are the right starting points.

### Lyric-to-song systems

A growing class of systems generate lyrics first, then condition the music on them (or vice versa). Suno does this implicitly. Some research systems do it explicitly. ([example](https://github.com/CodeName-Detective/Prompt-to-Song-Generation-using-Large-Language-Models))

**Why this matters for Project Pilot:** This is probably the right architecture. The lyric generator (Phase 1) outputs lyrics; a downstream model conditions a melody and arrangement on those lyrics; a final stage produces the audio. Each stage can be artist-conditioned independently.

---

## The artist-conditioning problem

The specific thing Project Pilot needs — generating *in the style of a specific artist* — is partially solved in existing systems:

- **Jukebox** had explicit artist embeddings, but the artists were limited to a fixed training set and the per-artist quality varied wildly.
- **Suno** doesn't expose artist controls; you can prompt with descriptive style language but not "make this sound like Twenty One Pilots."
- **Fine-tuning** any of the open models on an artist's catalog is the obvious approach but expensive and produces models that are hard to update.
- **Retrieval-augmented generation** — keeping an embedded catalog and pulling the closest examples to condition on — is cheaper and more flexible. Probably the right Project Pilot approach.

See [`artist-style-modeling.md`](artist-style-modeling.md) for deeper treatment.

---

## What Project Pilot can borrow

| Component | Likely source |
|---|---|
| Lyric generation | Fine-tuned open LLM (Llama 3.x family, etc.) on artist catalog |
| Symbolic melody/chord generation | Music Transformer / Magenta-style model |
| Audio rendering | MusicGen or Stable Audio, possibly fine-tuned |
| Artist embedding | CLAP / MERT embeddings over the artist's catalog, plus metadata |
| Editing / iteration | Inpainting approach borrowed from Udio's playbook |

This is a credible architecture sketch. The work is in the integration, the artist-modeling layer, and the evaluation.

---

## What's worth tracking

- **Open-source vocal-capable models.** Right now Suno/Udio are closed. The moment a credible open model handles vocals, Project Pilot's Phase 3 becomes much easier.
- **Diffusion vs. autoregressive for audio.** If diffusion wins, the Project Pilot architecture changes.
- **Licensed-training-data systems.** If a model trained legally on a major catalog opens up an API for artist-specific generation, that may be the right substrate to build on rather than rolling everything from scratch.
- **The Sony v. Suno case and similar litigation.** The legal landscape will shape what's possible.

---

## Recommended next reads

- The MusicGen paper (start there — most directly relevant).
- The Jukebox paper (architecture is dated but the artist-conditioning thinking is foundational).
- Stable Audio paper (modern diffusion approach).
- A survey paper like [A Survey on Music Generation from Single-Modal, Cross-Modal and Multi-Modal Perspectives](https://arxiv.org/html/2504.00837v2) for a wide view.
