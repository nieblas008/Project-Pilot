# Vision

## The core idea

Project Pilot is an attempt to build an AI system that can generate music — songs, lyrics, instrumentation, production — in the artistic voice of a specific chosen artist. The output should feel like the artist *could* have made it. Not necessarily *would* have, but *could* have, given what they've shown the world about who they are creatively.

This is different from existing AI music tools in a specific way: most current systems (Suno, Udio, MusicGen) are optimized for prompt-to-song generation across the broadest possible space of styles. Project Pilot is the opposite — narrow and deep. The goal isn't "any song from any prompt." It's "a song that feels right coming from this one specific artist."

## Why this matters (the personal version)

Artists with cohesive identities release slowly. Twenty One Pilots — the band this project is named after — has put out roughly one album every 2–3 years over the course of their career. The wait is meaningful, because the work is meaningful. But it's still a wait.

Most AI-generated music in 2026 has the opposite problem: infinite supply, near-zero artistic specificity. A song that sounds vaguely like "indie pop" or "alt-rock" isn't satisfying in the way that a song that sounds like *that band* is. The promise of artist-specific generation is that, done well, it could give fans a way to spend more time inside an artist's universe — between releases, or after a band has stopped making music, or as a creative tool for someone to interrogate what they actually love about an artist's work.

## Principles

These are the design commitments that should guide everything downstream.

### 1. Fidelity over flexibility

The system is allowed to produce a narrow range of outputs as long as those outputs are deeply true to the chosen artist. It is *not* allowed to drift toward generic "good music." If the chosen artist wouldn't release something, the system shouldn't produce it.

This implies real tradeoffs. The system will be worse at "popular" output than Suno or Udio. That is the point.

### 2. The artist's "essence" is multi-dimensional

An artist isn't just a sonic fingerprint. It's:

- **Instrumentation and arrangement** — what instruments they use, how they layer them, what they deliberately leave out (TØP famously omits guitar from many songs).
- **Vocal delivery** — the range, the techniques, the stylistic switches (Tyler Joseph's transition between rap, clean vocals, falsetto, and screams within a single track).
- **Lyrical themes** — what they write about, what they avoid, how they treat sensitive topics, whether they have ongoing narrative threads (Clancy, Nico, the Dema universe).
- **Production aesthetic** — texture, density, mix choices, signature effects, the overall "sonic world."
- **Structural tendencies** — how their songs are built, where they break expected song-structure conventions.
- **Collaborative footprint** — Tyler writes alone; other artists co-write extensively. This shapes the output in ways the system has to respect.
- **Career arc and evolution** — what era of the artist are we generating from? An artist's identity shifts; the system should know whether it's modeling early-career, mid-career, or current-era output.

The artist model has to capture all of these, not just the audio.

### 3. Subtlety is part of the craft

Tyler Joseph's lyrics work on two levels: they're singable and emotionally legible without analysis, *and* they reward deep reading. The system has to respect this. Generating lyrics that hit only one level — either too literal or too obscure — is failure.

This is a high bar. It's part of why this project requires real understanding of songwriting, not just a fine-tuned LLM.

### 4. Generalizable, not just one band

Twenty One Pilots is the test case because it's what I know best and have the most data on. But the system architecture should let any artist with sufficient material (catalog, interviews, public writing) be modeled. The artist-modeling layer should be data-driven enough that adding a new artist doesn't require re-architecting the system.

### 5. Theory before code

Documentation is the artifact during this phase of the project. The eventual code will be much better if the docs are deep first. This is partly because:
- Music has 400+ years of theory behind it; ignoring it means rediscovering the wheel badly.
- AI music generation has 10+ years of research behind it; ignoring it means re-running failed experiments.
- The artist-fidelity problem is *new*. The only way to be original about it is to be informed about everything around it.

### 6. Respect for the artists being modeled

Project Pilot is not designed to release or commercialize generated material, especially material that imitates real artists. The output is for personal use, exploration, and learning. The project takes seriously the legal and ethical questions about training data and derivative work — see [`research/legal-and-ethics.md`](research/legal-and-ethics.md) for a fuller treatment.

## What success looks like

The minimum bar for success is qualitative, and probably evaluable only by people who know the chosen artist well. Concretely:

- **Lyrics test:** A fan of the artist, shown a generated set of lyrics alongside real (but lesser-known) lyrics from the artist, should be unable to consistently distinguish them. The generated lyrics should also pass the artist's own subtext-and-theme tests — e.g., not violating things the artist would never say.
- **Style test:** A generated song, played to a fan, should be identified as "in the style of [artist]" without hesitation. Bonus if it's mistaken for a deep cut.
- **Coherence test:** The generated work should hold together internally — lyrics should match the mood of the music, the production should match the era, etc. No frankenstein outputs.

These are aspirational. The first version of the system will fail all of them. The point is that we know what we're aiming at.

## What this project will probably teach me

Even if Project Pilot never produces a single passable song, the process should leave me with:

- Real fluency in music theory and songwriting.
- A working knowledge of the AI music generation field.
- Experience designing systems where the "evaluation" is taste-based rather than benchmark-based.
- A much deeper understanding of why my favorite band sounds like my favorite band.

That's a reasonable outcome by itself.

## Related documents

- [`RESEARCH.md`](RESEARCH.md) — the learning roadmap.
- [`case-studies/twenty-one-pilots.md`](case-studies/twenty-one-pilots.md) — the canonical artist case study.
- [`architecture/system-design-notes.md`](architecture/system-design-notes.md) — early architectural sketches.
