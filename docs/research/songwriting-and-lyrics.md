# Songwriting and Lyrics

> How songs are constructed and how lyrics are written. The Phase 1 implementation of Project Pilot lives in this domain.

## Why this matters for Project Pilot

Lyrics are the most tractable part of "artist-style generation" because they're text — and we have very mature tools (LLMs) for generating text in a style. The Phase 1 system will be a lyric generator. That makes deep understanding of lyric craft directly load-bearing for the first real implementation.

Song structure matters because lyrics don't exist in isolation — a chorus lyric works differently from a verse lyric, and a generated chorus that reads like a verse is broken even if the words are individually fine.

## Status

**Outline + research notes.** Expand as you study and as you analyze specific songs.

---

## 1. Song structure

### Standard pop/rock structure

The most common modern pop structure is:

```
intro → verse 1 → pre-chorus → chorus → verse 2 → pre-chorus → chorus → bridge → chorus → outro
```

Or in shorthand: ABABCB, where A = verse, B = chorus, C = bridge. ([source](https://www.masterclass.com/articles/songwriting-101-learn-common-song-structures))

### What each section does

- **Intro** — sets mood and tempo; introduces a hook or signature element.
- **Verse** — narrative, lyric-heavy, lower melodic tension, more space. New lyrics each time.
- **Pre-chorus** — builds tension, often lifts melody/dynamics toward the chorus. Lyrics often repeat or vary slightly.
- **Chorus** — emotional and melodic climax; contains the hook; lyrics repeat exactly each time. This is the "main event."
- **Bridge** — appears once, typically before the final chorus. Provides contrast — lyrically a turn or revelation, musically a change of key/dynamics/instrumentation. Jolts the listener out of the established pattern. ([source](https://www.elizabethrecords.net/blog/the-science-of-song-structure-verse-chorus-bridge-explained))
- **Outro** — winds the song down or ends abruptly. Sometimes restates the hook with new energy.

### Other structures

- **AABA** — older, common in jazz standards and some folk. A = verse-with-hook, B = bridge.
- **Through-composed** — no repeating sections; common in prog and some indie/experimental work.
- **Loop-based** — common in hip-hop and electronic; small repeated unit with variation.

### How TØP plays with structure

Twenty One Pilots routinely:
- Compresses or skips pre-choruses.
- Has multiple distinct "hooks" within a single song.
- Switches genres mid-song (rap verse → sung chorus → reggae-inflected bridge).
- Modulates keys between sections.

Any artist-faithful generator for TØP has to be able to *deviate* from the standard structure in characteristic ways — not in random ways.

---

## 2. Lyric writing craft

### Rhyme schemes

How line endings rhyme. Notated by letter:
- AABB — couplets.
- ABAB — alternating.
- ABCB — only lines 2 and 4 rhyme (very common in pop).
- AAAA — monorhyme; rare, intentional.

Modern lyrics often use **slant rhymes** (near-rhymes like "time"/"mind") which sound more conversational than perfect rhymes. They also use **internal rhyme** (within a line) and **multisyllabic rhymes** (especially in rap).

### Meter

The pattern of stressed and unstressed syllables. Strict meter (iambic, trochaic, etc.) is rarer in modern lyrics than in poetry, but lyrics still have rhythm and the best lyricists are obsessive about syllable counts per line because it determines how the words fit the melody.

### Imagery and concrete language

The classic songwriting advice: **be specific**. "I sat in the kitchen waiting for the phone" beats "I felt anxious that day." Specifics let listeners project; abstractions push them away. (This is itself an artist-by-artist thing — some artists work in abstraction effectively. Bon Iver. Some TØP songs.)

### Narrative perspective

- **First person ("I")** — most common; intimate.
- **Second person ("you")** — direct address; can feel accusatory or romantic.
- **Third person ("he/she/they")** — narrative songs, character pieces.
- **Mixed/shifting** — sophisticated; common in story songs.

TØP frequently uses first and second person, with the "you" often ambiguous (a person? a feeling? the listener? Tyler himself?).

### Subtext and double meanings

The thing that separates great lyrics from competent ones. Tyler Joseph is a master of writing lyrics that *work* on first listen as emotional sketches but reward repeated listening with revealed meaning. Examples:
- Lines that read literally as personal but map onto the Dema/Clancy mythology.
- Lyrics that seem like love songs but are about mental illness, or vice versa.
- Wordplay that points two ways at once.

A lyric generator that only produces literal lyrics is half the system. A lyric generator that produces lyrics with deliberate subtext is the real goal.

### What to avoid (mostly)

- Forced rhymes that distort meaning.
- Clichés ("heart on my sleeve," "stars in the sky") — unless used self-consciously.
- Mixed metaphors that don't cohere.
- Hooks that don't actually hook (vague, abstract, or unmemorable choruses).

---

## 3. How melody and lyrics interact (prosody)

### Stress alignment

Stressed syllables should fall on strong beats; important words should fall on melodically prominent notes. Bad prosody: "*the* CAT sat *on* the MAT" with the wrong syllables emphasized — it fights the listener's ear.

### Vowel sounds

Open vowels (ah, oh) carry better at high notes; closed vowels (ee, oo) are harder to sing loud. Skilled lyricists rewrite words specifically to put the right vowel sound on the climactic note.

### Singability

Lyrics that look good on paper aren't always singable. Repeated hard consonants are hard to deliver fast; tongue-twisting phrases break in live performance. The test is always reading aloud — or better, singing along to the intended melody.

---

## 4. Lyrics as artist identity

This is the part that matters most for Project Pilot.

### Themes and preoccupations

Every artist with a strong identity has a small number of themes they return to repeatedly. Examples:
- **Twenty One Pilots:** mental health, faith, identity, doubt, anxiety, suicide, hope-against-evidence, fictional mythology (Dema, Clancy, Nico).
- **Phoebe Bridgers:** mortality, religion, depression, queer longing.
- **Kendrick Lamar:** race, fame, religion, the city, lineage.
- **Radiohead:** alienation, technology, dread, fragility.

The artist's identity is partly defined by what they *don't* write about. TØP doesn't write party songs. Phoebe Bridgers doesn't write triumphalism. A generator that drifts toward generic topics has failed.

### Voice and diction

The specific word choices, level of formality, sentence structure, and rhetorical habits that make a lyric recognizable as a specific artist's. Tyler Joseph uses a lot of conditional and questioning constructions; he addresses an unspecified "you" frequently; he uses second-person commands ("don't you stop"); his vocabulary tilts toward emotional abstraction interleaved with concrete imagery.

### Recurring imagery and motifs

The vocabulary of objects, places, and metaphors an artist returns to. TØP: yellow (especially in the Trench/Clancy era), bandits, walls and cities, masks, hands and gloves, sleep/waking.

### Worldbuilding

Some artists construct ongoing fictional universes. TØP's Dema/Clancy mythology spans multiple albums. A faithful generator for TØP needs to know this exists and be able to use it consistently.

---

## 5. Implications for the Phase 1 lyric generator

What the Phase 1 system needs:

1. A **corpus** of the artist's complete published lyrics, annotated by song, album, era.
2. An understanding of which **themes** the artist works in (potentially extracted via topic modeling or LLM-based analysis of the corpus).
3. A representation of **structural conventions** (does this artist write 4-line verses or 8-line verses? AABB or ABCB?).
4. A **rhyme/meter** constraint system so generated output is singable.
5. (Eventually) a **subtext layer** — the ability to write a lyric that operates on two levels.
6. An **artist-knowledge layer** for ongoing mythologies/characters/imagery so generated lyrics don't violate canon.

See [`ai-lyric-generation.md`](ai-lyric-generation.md) for the technical side.

---

## Recommended next reads

- *Tunesmith* by Jimmy Webb — songwriter's-eye view of the craft.
- *Writing Better Lyrics* by Pat Pattison — exercises and analysis.
- Genius.com annotations of songs you admire — even when the annotations are fan-level, the act of comparing your read with others' is the exercise.
- Search "[favorite artist] lyrical analysis" essays — the better ones model how to read for craft.
