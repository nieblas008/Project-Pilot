# Legal and Ethics

> The hardest part of this project isn't the code. It's the ethics and the law.

## Why this matters for Project Pilot

A system that generates music in the style of a living, working artist sits in genuinely contested legal and ethical territory. Even when used purely for personal exploration, the design choices matter — what training data is used, what is generated, what is shared, what is monetized. Project Pilot takes this seriously not as a bolt-on disclaimer but as a constraint on design.

## Status

**Starter content. Update as the legal landscape changes — and it is changing.**

---

## The legal landscape (as of 2026)

### Training data

The central legal question for AI music: is training a model on copyrighted music a copyright infringement?

The current answer is **disputed and litigated**. The major cases:

- **RIAA v. Suno (2024–present)** — Major labels sued Suno over training on copyrighted recordings. Motions to dismiss denied in late 2024. The case is in active discovery as of spring 2026. ([overview](https://www.silvermansound.com/ai-music-copyright-legal-risks-content-creators))
- **Sony Music v. Suno (parallel/ongoing)** — Active litigation.
- **UMG v. Udio (2024) — settled October 2025**. Udio licensed UMG's catalog and is launching a jointly-licensed platform.

### Regulatory developments

- **EU AI Act** — Requires transparency about training data. AI providers must document consent from rights-holders.
- **US Copyright Office (2025 guidance)** — Models must differentiate between public domain, licensed, and proprietary works. AI-generated content without sufficient human authorship is not copyrightable.
- **UK** — Scrapped earlier plans to allow training on copyrighted music without permission.

The trend is clearly toward **explicit licensing required**. This is good for the long-term legitimacy of AI music; it complicates the short-term reality of small/personal projects.

### Output

Even if training is sorted, the output raises additional issues:
- **Derivative works.** Output that's "substantially similar" to a specific copyrighted work is infringement regardless of how it was made.
- **Voice and likeness.** Generating output that imitates an identifiable vocalist may implicate publicity rights (Tennessee's ELVIS Act, similar pending legislation elsewhere).
- **Authorship.** AI-generated material may not be copyrightable, depending on the level of human input.

### What this means for Project Pilot

- **Don't release generated material publicly** that imitates a real artist, especially commercially. This isn't conservative legalism — it's the most direct way to avoid causing harm.
- **Don't train on pirated audio.** Use legally obtained copies of music you have access to (purchased, licensed) for any audio analysis. Use lyrics from public/licensed sources.
- **Keep generated material personal.** Treat it as the AI equivalent of a sketchbook.
- **Don't enable bad actors.** If the system is ever opened up, build in friction against misuse (clear watermarking, opt-in artist consent, etc.).

---

## The ethical landscape

The law is the floor. The ethics are higher.

### Consent

Living artists haven't consented to be modeled. Even if it's legal, it may not be right to generate work in their voice. The strongest version of this is: **if you wouldn't want a stranger to do this with your work, don't do it with someone else's.**

Some artists have spoken publicly about AI music. Many oppose it strongly. Some are exploring it themselves. The consent question is not abstract — fans can often find out where their favorite artists stand.

Project Pilot's stance: **default to not using the system for an artist who has publicly opposed AI generation of their work, even though there is no legal mechanism to compel this.** Maintain a list. Respect it.

### Impact on the artist's economic interest

Even non-commercial fan-generated material can affect an artist:
- Diluting the perceived value of "the artist's real work."
- Misleading listeners about what the artist has said.
- Saturating streaming/social platforms.
- Damaging the artist's brand through low-quality output associated with them.

These are real harms even without legal infringement.

### Misrepresentation

Generated material that gets mistaken for the real artist's work is a misrepresentation. Even in personal use, share with care; clearly mark generated material as generated; never publish to platforms that might confuse listeners.

### The "honoring vs. exploiting" line

Project Pilot's framing is *honoring* — exploring why an artist's work matters, generating "what if" material in private, treating it as a form of close reading. The line between honoring and exploiting is real but blurry. Practical heuristics:
- Personal use → leaning honoring.
- Public sharing → leaning exploiting.
- Monetization → exploiting.
- Educational discussion of the *system* → fine, even publicly.
- Pretending generated work is real → exploiting.

### Data minimization

If lyrics are sufficient to do the work, don't ingest audio. If a few songs suffice for a prototype, don't ingest the whole catalog. The smallest possible data footprint that gets the job done is the safest.

### What about the artist's collaborators?

A song isn't just the artist. It includes producers, session musicians, co-writers (when applicable), and engineers. Modeling "the artist's style" partly models their collaborators too. This adds people to the ethical equation. Worth being mindful.

---

## Project Pilot's working principles

To make this concrete, the project commits to:

1. **No public releases of generated material that imitates a real artist.** Personal use only.
2. **No monetization** of generated material that imitates a real artist.
3. **Clear labeling** of any generated material that is shared, even privately.
4. **Use legally obtained source material** for training and analysis.
5. **Respect publicly stated artist positions** on AI generation; maintain an opt-out list.
6. **Be transparent** in this documentation about what data is being used and how.
7. **Treat the system as a learning tool** first — for the developer, primarily — and a generation tool second.
8. **Track the legal landscape.** Revisit these principles when major rulings or laws change.

If the project ever moves toward something other than personal use (e.g., demoing publicly, open-sourcing), these principles need to be revisited carefully. The current rules are calibrated to the current scope.

---

## What about non-real artists?

A separate, much cleaner application: generating music in the style of *fictional artists* — invent a band, define their identity, generate their work. No real-artist ethics, full creative freedom. This could be a useful intermediate testbed for the artist-modeling architecture without engaging the hardest ethical questions.

It's also possible to model **public-domain artists** (classical composers, etc.) with much weaker ethical concerns, though the data may be sparser for the audio modalities.

---

## Recommended reading

- [How AI Music Generators Source Training Data Legally in 2026](https://www.soundverse.ai/blog/article/how-ai-music-generators-source-training-data-legally-1038)
- [AI Music Copyright: Legal Risks Content Creators Must Know (2026)](https://www.silvermansound.com/ai-music-copyright-legal-risks-content-creators)
- The US Copyright Office's AI guidance documents (search for current versions).
- The EU AI Act text, particularly the sections on generative AI transparency.
- Statements from artist advocacy groups (RIAA, Artist Rights Alliance, Future of Music Coalition) — and statements from individual artists you intend to model.
