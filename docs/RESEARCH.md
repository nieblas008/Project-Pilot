# Research Roadmap

This is the opinionated learning path for Project Pilot. It's organized so that each phase teaches you what you need to evaluate the next phase. The order matters: studying AI music generation before you understand what "good music" means is how you end up building something that benchmarks well and sounds soulless.

## How to use this document

- Each section lists **topics to learn**, **why they matter for Project Pilot**, and **recommended starting points**.
- Don't try to master everything before writing code. The point is to develop enough fluency to make informed decisions and evaluate outputs.
- As you learn things, drop notes into the relevant document under [`research/`](research/). Those documents are the long-term knowledge base; this file is the index and curriculum.

## Estimated time

If you're treating this as a serious side project (~5–10 hours a week), expect the documentation/learning phase to take **3–6 months** before you have enough to start meaningful implementation. Most people grasp foundational music theory in 6–12 months of consistent practice; you don't need full mastery, just functional literacy. ([source](https://www.iconcollective.edu/basic-music-theory))

---

## Phase 1 — Music fundamentals (start here)

You cannot evaluate AI-generated music if you don't know how music works. This is the foundation.

### 1.1 Music theory basics

**Topics:**
- Notes, scales (major, minor, modal scales like Dorian/Mixolydian).
- Intervals and their emotional character.
- Triads, seventh chords, chord extensions.
- Diatonic chord progressions (I–IV–V–vi etc.), Roman numeral analysis.
- Keys, key signatures, modulation.
- Rhythm: meter, time signatures, syncopation, polyrhythm.
- Melody: contour, phrasing, motif, repetition vs. variation.
- Harmony: voice leading, cadences, tension and resolution.

**Why it matters:** Every decision the AI makes — what chord comes next, where a melody resolves, whether a rhythm feels "off" — happens inside the language of music theory. You need to be able to look at generated output and say "this is in the key of D minor and the chord progression is i–VI–III–VII, which is why it feels like a TØP verse."

**Starting points:**
- [`research/music-theory.md`](research/music-theory.md) — the project's growing notes.
- Free PDF: [Music Theory for the 21st-Century Classroom](https://musictheory.pugetsound.edu/hw/MusicTheory.pdf).
- LANDR's [basic music theory guide](https://blog.landr.com/music-theory/).
- Hands-on: noodle on a piano or use a free DAW like GarageBand to actually hear the concepts.

### 1.2 Songwriting and song structure

**Topics:**
- Standard song forms: verse–chorus, verse–chorus–bridge (ABABCB), AABA, through-composed.
- The role of intro, verse, pre-chorus, chorus, bridge, outro.
- Hooks and what makes them work.
- Lyric writing: rhyme schemes, meter (syllable counts, stress patterns), imagery, narrative perspective.
- How melody interacts with lyrics (syllabic vs. melismatic, prosody).
- Subtext and how songs operate on multiple levels at once.

**Why it matters:** This is what your system actually has to produce. Knowing what's *normal* lets the AI deliberately deviate when the artist deviates (TØP often blurs verse/chorus boundaries; that's part of their signature).

**Starting points:**
- [`research/songwriting-and-lyrics.md`](research/songwriting-and-lyrics.md).
- MasterClass: [Songwriting 101: Common Song Structures](https://www.masterclass.com/articles/songwriting-101-learn-common-song-structures).
- Read lyrics-with-analysis from artists you admire. Genius.com annotations are a starting point but go deeper — search "[artist] lyrical analysis" essays.

### 1.3 Instruments, arrangement, and production

**Topics:**
- The standard rock/pop instrument set and what each contributes.
- Synthesis basics: oscillators, envelopes, filters, modulation.
- Drum programming and groove.
- Arrangement: layering, frequency separation, dynamics across a song.
- DAWs: what they are, how they work, why Ableton/FL/Logic/Pro Tools each have a culture.
- Mixing: levels, panning, EQ, compression, reverb, delay.
- Mastering: loudness, stereo width, final polish.

**Why it matters:** A great melody with bad arrangement is a bad song. The artist-fidelity problem is mostly a *production* problem — TØP and a session musician could play the same chords and you'd still know which is which from the production.

**Starting points:**
- [`research/instruments-and-production.md`](research/instruments-and-production.md).
- LANDR: [How to Mix for Beginners](https://blog.landr.com/how-to-mix-for-beginners/).
- Try recording one song in GarageBand or Reaper (free). Even badly. The point is to develop intuition.

---

## Phase 2 — The AI music generation landscape

Now that you have a frame of reference for what "good music" means, you can evaluate what existing systems do.

### 2.1 Survey of generative music systems

**Topics:**
- **OpenAI Jukebox (2020)** — raw audio, hierarchical VQ-VAE, artist/genre conditioning. The first credible artist-conditioned system. ([paper](https://arxiv.org/abs/2005.00341))
- **Meta MusicGen (2023)** — EnCodec + transformer LM, text-and-melody conditioning, open source. The current reference model for research. ([HF model](https://huggingface.co/facebook/musicgen-large))
- **AudioLDM / Stable Audio** — latent diffusion approaches, faster and more controllable. ([Stable Audio paper](https://arxiv.org/pdf/2402.04825))
- **Suno** — closed-source, end-to-end song generation including vocals, currently the market leader.
- **Udio** — closed-source, emphasis on instrument fidelity, inpainting, and recently licensed under a UMG deal.
- **Riffusion** — clever hack using image diffusion on spectrograms.
- **AIVA, Soundraw, Beatoven** — closed-source, focused on instrumental/background music.

**Why it matters:** Don't reinvent. Understand which approaches are credible, which are dead ends, and what's open-source enough to actually build on.

**Starting points:**
- [`research/ai-music-generation.md`](research/ai-music-generation.md).
- Read the Jukebox paper (or at least the architecture section).
- Skim the MusicGen paper — it's the most directly useful for an artist-modeling system.

### 2.2 Symbolic vs. audio generation

**Topics:**
- MIDI-based / symbolic generation (Music Transformer, MuseNet, Magenta).
- Raw audio / waveform generation (WaveNet, Jukebox).
- Latent / tokenized audio (EnCodec, SoundStream, then transformer on top).
- Tradeoffs: symbolic is editable and structured but loses timbre and vocals; audio captures everything but is computationally expensive and hard to edit. ([overview](https://pupuweb.com/why-is-midi-better-than-wav-for-symbolic-music-generation/))

**Why it matters:** Your Phase 2 implementation is probably symbolic. Your Phase 3 implementation is probably audio. Knowing the tradeoffs lets you plan.

### 2.3 Lyric generation

**Topics:**
- LLM-based lyric generation (fine-tuned GPT/Llama/etc.).
- Rhyme and meter constraints (Phyme module, rhyme-first prompting).
- Theme and topic conditioning.
- Voice/style transfer for lyrics.
- Evaluation: BLEU/ROUGE are useless here; this is a taste problem.

**Why it matters:** Phase 1 of Project Pilot's implementation is a lyric generator. This is the most tractable starting point.

**Starting points:**
- [`research/ai-lyric-generation.md`](research/ai-lyric-generation.md).
- The [Lyre-LM repo](https://github.com/Christianfoley/LLMLyricGen) is a useful working example of a fine-tuned LLM for lyric generation.

---

## Phase 3 — Artist style modeling

This is the original contribution of Project Pilot. There is real research in this area but the artist-fidelity problem is far from solved.

### 3.1 Music Information Retrieval (MIR)

**Topics:**
- Audio features: spectrograms, mel-spectrograms, MFCCs, chroma features.
- Tempo, key, and beat tracking.
- Genre and mood classification.
- Instrument identification and source separation.
- Artist classification (yes, this is a real task with benchmarks).
- Audio fingerprinting (Shazam-style).
- Modern embeddings: CLAP, MERT, MusicNN, CLaMP. ([Wikipedia overview](https://en.wikipedia.org/wiki/Music_information_retrieval))

**Why it matters:** MIR gives you the computational vocabulary to describe what makes an artist sonically distinctive. The artist-modeling layer is essentially an MIR problem turned generative.

**Starting points:**
- [`research/artist-style-modeling.md`](research/artist-style-modeling.md).
- The `librosa` Python library tutorials — get hands-on with feature extraction.
- The ISMIR conference proceedings if you want depth.

### 3.2 Style transfer and conditioning

**Topics:**
- Conditioning generative models on metadata (artist, genre, era).
- Fine-tuning vs. retrieval-augmented generation for style.
- LoRA / adapter approaches for cheap artist-specific fine-tunes.
- How Jukebox's artist conditioning actually worked, and why it was limited.

**Why it matters:** This is the technical core of the project.

---

## Phase 4 — Adjacent topics worth knowing

These don't fit neatly in a phase but you'll need them eventually.

### 4.1 Legal and ethical

**Topics:**
- Copyright on training data.
- Derivative work doctrine.
- Voice and likeness rights.
- Active litigation (Sony v. Suno, the UMG v. Udio settlement). ([overview](https://www.silvermansound.com/ai-music-copyright-legal-risks-content-creators))
- EU AI Act transparency requirements for training data.
- The ethical question of imitating living artists without consent.

**Starting points:**
- [`research/legal-and-ethics.md`](research/legal-and-ethics.md).

### 4.2 Evaluation

**Topics:**
- Why standard ML metrics fail for creative output.
- A/B blind tests with knowledgeable listeners.
- Frechet Audio Distance and its limitations.
- Building a "fan turing test" rubric for your specific artist.

### 4.3 Practical ML

**Topics:**
- Audio data pipelines (loading, resampling, augmentation).
- Working with HuggingFace models (Transformers, Diffusers).
- GPU / compute budgeting for audio (much more expensive than text).
- Model serving and inference latency.

---

## Suggested first three weeks

If you want a concrete on-ramp:

1. **Week 1:** Skim music theory basics (Phase 1.1). Pick a free DAW and load some loops. Play with chord progressions.
2. **Week 2:** Watch/read song-structure analyses of three TØP songs you know well. Try writing lyrics in their style by hand — no AI. Notice what's hard.
3. **Week 3:** Read the MusicGen paper. Run the open-source MusicGen model on HuggingFace with a few prompts. Notice what it does well and where it fails for artist-specific output.

By the end of week 3 you'll have a much clearer sense of which direction Project Pilot should take.
