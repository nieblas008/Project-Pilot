# AI Lyric Generation

> The technical side of generating lyrics. This is the most tractable corner of the problem and the planned Phase 1 implementation.

## Why this matters for Project Pilot

Lyrics are text, and LLMs are extremely good at text. A lyric generator is therefore the cheapest starting point and the place where the artist-modeling concept can be validated before committing to expensive audio work. Phase 1 of Project Pilot is a lyric generator.

## Status

**Starter content — most active document for Phase 1.** Expand heavily.

---

## The basic problem

You want to generate text that:
1. **Reads like song lyrics** (not prose, not poetry, not a treatise).
2. **Fits a musical structure** (verse, chorus, bridge with appropriate length per section).
3. **Respects rhyme and meter** (so it's singable).
4. **Captures a specific artist's voice, themes, and habits.**
5. **Operates with subtext** where the artist does.
6. **Stays inside the artist's worldbuilding** (e.g., doesn't violate Dema canon if generating for TØP).

LLMs out of the box do (1) okay and (2)–(6) badly without help. The work is in the scaffolding.

---

## Approaches

### Approach A: Pure prompt engineering on a strong base model

Use a frontier LLM (Claude, GPT, Gemini) with a detailed prompt that includes artist context, theme requirements, structural requirements, and examples.

**Pros:** Zero training cost. Easy to iterate. State-of-the-art models are quite good at style mimicry from examples.

**Cons:** Limited by context window. Hard to enforce strict rhyme/meter. Style mimicry often becomes pastiche. May be filtered by safety policies for sensitive themes (TØP writes about suicide, etc.).

**Verdict:** Good for prototyping and as a fallback. Not the long-term answer.

### Approach B: Fine-tuned open LLM

Take an open model (Llama 3.x, Mistral, etc.) and fine-tune on the artist's catalog plus structural metadata.

**Pros:** Captures voice more deeply than prompting. Cheaper at inference. No content filtering. Can be updated when the artist releases new material.

**Cons:** Requires the catalog as training data (copyright complications). Fine-tuning quality varies. Small catalogs (a few hundred songs) may not be enough.

**Verdict:** Probably the right Phase 1.5 approach once prompting hits its ceiling. The [Lyre-LM project](https://github.com/Christianfoley/LLMLyricGen) is a worked example.

### Approach C: Retrieval-augmented generation

Keep the artist's catalog as an embedded corpus. For each generation request, retrieve the most relevant examples (by theme, structure, era) and include them in the prompt to a base LLM.

**Pros:** Cheaper than fine-tuning. Easier to update (just re-index). Natural fit for "in the style of a specific era/album."

**Cons:** Quality depends on retrieval quality and base model. Doesn't capture deep stylistic patterns as well as fine-tuning.

**Verdict:** Strong Phase 1 candidate. Probably the right *first* implementation.

### Approach D: Hybrid (RAG + fine-tune)

Fine-tuned model with RAG-injected context for specific generations. Best of both worlds at the cost of complexity.

**Verdict:** Phase 1.5 or Phase 2 evolution.

---

## Handling rhyme and meter

LLMs are notoriously bad at strict rhyme and syllable counts. Approaches:

### Constraint-based sampling

Use a base LLM but at sampling time, constrain the vocabulary at line endings to words that rhyme with the previous line ending. The [Phyme module](https://pypi.org/project/Phyme/) and similar tools provide rhyme dictionaries.

### Rhyme-first prompting

Generate the line-ending word first (constrained to rhyme), then generate the rest of the line working backward or filling toward it. ([reference paper](https://arxiv.org/pdf/2405.05176))

### Train with explicit rhyme tokens

During fine-tuning, prepend each line with its line-ending word, so the model learns to write toward a known target. At generation time, sample line endings from a rhyme dictionary then generate.

### Post-hoc rewriting

Generate freely, then use a second LLM pass to rewrite for rhyme/meter. Cheap and often effective but can lose meaning.

### What about meter?

Harder. Syllable counting is a feature, but stress patterns and prosody don't have clean computational shortcuts. Probably handle meter approximately (target syllable counts per line, with a window of tolerance) and accept that perfect prosody is a melody-coupling problem to solve in Phase 2.

---

## Theme and topic conditioning

The artist's themes are part of identity. To generate lyrics on the right themes:

- **Curate a theme list** from the artist's catalog (manually, or via topic modeling like BERTopic). For TØP: mental health, faith, doubt, identity, fictional mythology.
- **Pass a target theme as a generation parameter.** "Write a verse about X in the style of [artist]."
- **For each artist, also track *anti-themes*** — things they reliably don't write about. Use this as a filter.

Research has shown that adding theme/topic conditioning to lyric generators improves output quality with no real downside. ([source](https://arxiv.org/pdf/2009.14375))

---

## Subtext and double meanings

The hard part. A lyric that hits two levels — emotional on the surface, narrative/symbolic underneath — is the gold standard for artists like Tyler Joseph.

**Possible approaches:**

- **Two-pass generation.** Generate a literal lyric first, then prompt the model to add a second layer of meaning using the artist's recurring symbols/mythology.
- **Symbol library.** Maintain a structured list of the artist's recurring symbols (TØP: yellow, bandits, Dema, hands, sleep). Generation prompts can specify "use [symbol] meaningfully."
- **Critic model.** Train or prompt a second model to evaluate generated lyrics for surface and deep meaning, and reject/regenerate when only one level is present.

None of this is solved. It's research territory and one of the most interesting parts of the project.

---

## Worldbuilding consistency

For artists with ongoing mythologies (TØP's Clancy/Nico/Dema), generated lyrics shouldn't violate canon — wrong characters acting wrong, fabricated places, mistakes about who did what.

**Approach:** Maintain a structured knowledge document about the artist's universe. Inject relevant sections into the prompt. Have a verification pass that checks generated lyrics for canon violations.

For TØP specifically, the fan wiki has extensive lore documentation that could seed this. (Use responsibly — fan content is owned by fans.)

---

## Evaluation

Standard NLP metrics (BLEU, ROUGE, perplexity) are nearly useless for lyric quality. Real evaluation:

1. **Held-out test.** Train on most of the catalog, evaluate by trying to generate songs you didn't show the model and comparing to the real held-out songs. Useful but noisy.
2. **Human blind test.** Mix generated lyrics with real lesser-known songs by the artist; have fans guess which is which. The gold standard.
3. **Subjective rubric.** Score generated lyrics on: voice match, theme appropriateness, structural correctness, rhyme/meter, subtext, canon consistency.
4. **Negative tests.** Verify the model refuses to (or naturally avoids) producing things outside the artist's identity.

---

## Pipeline sketch for Phase 1

```
Input: artist, era (album/period), target theme, structure (e.g., "verse-chorus-verse"), mood
   ↓
Retrieval: pull N most relevant songs from artist's embedded catalog by theme + era
   ↓
Prompt construction: artist context + retrieved examples + structural target + theme + mood
   ↓
LLM generation (with rhyme constraints at line endings)
   ↓
Filters: canon check, anti-theme check, profanity/safety check appropriate to artist
   ↓
(Optional) Second-pass subtext pass
   ↓
Output: structured lyrics with section labels (verse/chorus/bridge), with metadata
```

This is achievable with off-the-shelf tools (a frontier LLM API + an embedding model + a vector DB + a rhyme dictionary library) within a few weeks of focused work.

---

## Open questions

- How small can the artist's corpus be and still produce convincing lyrics? (TØP has ~80 released songs. Is that enough?)
- Does fine-tuning beat retrieval at that scale, or does retrieval win because there's not enough data to fine-tune meaningfully?
- How do you train/induce the subtext capability if your model is a base LLM that has no concept of it?
- How do you handle artist *evolution*? Early-era TØP is very different from current TØP. Should there be one model per era?

---

## Recommended next reads

- The [Lyre-LM repo](https://github.com/Christianfoley/LLMLyricGen) — concrete fine-tuning code for lyric generation.
- [Generation of lyrics lines conditioned on music audio clips](https://arxiv.org/pdf/2009.14375) — a research example of theme conditioning.
- [Conditional LSTM-GAN for Melody Generation from Lyrics](https://arxiv.org/pdf/1908.05551) — the inverse problem, but the architectural ideas transfer.
- HuggingFace's text-generation docs once you start fine-tuning.
