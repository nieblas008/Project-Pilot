# Music Theory

> The foundational language of music. This document grows as the project's understanding deepens.

## Why this matters for Project Pilot

Every generated note, chord, and rhythm is a choice that lives inside the rules (or deliberate violations) of music theory. To evaluate whether the AI's output is "good," let alone whether it's true to a specific artist, requires reading the output in this language. This document is the project's working notes on that language.

## Status

**Sparse but seeded.** This is a starting outline with summary notes from initial research. Expand each section as you study it.

---

## 1. The basics

### Notes and the chromatic scale

Western music divides the octave into 12 equal semitones (the chromatic scale): A, A#/B♭, B, C, C#/D♭, D, D#/E♭, E, F, F#/G♭, G, G#/A♭. An octave is the interval between a note and the next note of the same name — a 2:1 frequency ratio.

### Intervals

The distance between two notes. Each interval has a characteristic emotional feel:
- **Perfect 5th** — stable, open (power chords).
- **Major 3rd** — bright, "happy."
- **Minor 3rd** — dark, "sad."
- **Tritone** — dissonant, unresolved.
- **Octave** — same note, different register.

Learning to *hear* intervals (ear training) is more useful than memorizing names. Apps like Functional Ear Trainer help.

### Scales

A scale is an ordered subset of the 12 chromatic notes. The two that matter most in popular music:
- **Major scale** — W-W-H-W-W-W-H (where W = whole step, H = half step). Bright. C major: C D E F G A B.
- **Natural minor scale** — W-H-W-W-H-W-W. Dark. A minor: A B C D E F G.

Modal scales (Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian) are reorderings of the major scale starting from different notes. They give different emotional flavors and matter more in some genres than others (Dorian is everywhere in folk and rock; Phrygian shows up in metal).

> **TODO:** Add sections on modes with audio examples once you've internalized them.

---

## 2. Chords and harmony

### Triads

The most basic chord: three notes stacked in thirds. The most basic triads:
- **Major** — root, major 3rd, perfect 5th (e.g., C major: C-E-G).
- **Minor** — root, minor 3rd, perfect 5th (e.g., A minor: A-C-E).
- **Diminished** — root, minor 3rd, diminished 5th.
- **Augmented** — root, major 3rd, augmented 5th.

### Seventh chords and extensions

Add the 7th, 9th, 11th, 13th for more color. Maj7 is dreamy/jazz; m7 is smooth; dom7 is bluesy/tense.

### Diatonic chords and Roman numeral analysis

In any key, you can build a chord on each scale degree. In C major:
- I = C major
- ii = D minor
- iii = E minor
- IV = F major
- V = G major
- vi = A minor
- vii° = B diminished

Uppercase = major, lowercase = minor, ° = diminished. This notation is **portable across keys** — a I–V–vi–IV in C is C-G-Am-F; in G it's G-D-Em-C. The same emotional structure, different absolute notes.

### Common progressions

- **I–V–vi–IV** — the "four chord song." Probably the most-used progression in pop.
- **I–vi–IV–V** — the '50s progression.
- **ii–V–I** — the backbone of jazz.
- **vi–IV–I–V** — the same chords as I–V–vi–IV in a different order; melancholy.
- **i–VI–III–VII** (minor key) — common in alt/rock; sad-but-driving feel.

### Voice leading

The way individual notes in chords move when chords change. Smooth voice leading (each voice moves by small intervals) sounds natural; large jumps sound jarring. This is partly why simple guitar chord changes work even though theory makes them look unrelated.

### Cadences

Standard chord motions that signal phrase endings:
- **Authentic (V–I)** — strongest sense of resolution.
- **Plagal (IV–I)** — "amen" cadence.
- **Half (anything–V)** — leaves things hanging.
- **Deceptive (V–vi)** — sets up resolution then dodges it.

---

## 3. Rhythm

### Meter and time signatures

The top number tells you how many beats per measure; the bottom tells you what kind of note gets the beat. 4/4 is by far the most common; 3/4 is waltz time; 6/8 has a flowing triplet feel; 7/8 and 5/4 are "odd meters" that show up in prog and parts of TØP's catalog.

### Tempo

Beats per minute (BPM). 60-80 = ballad, 90-120 = mid-tempo pop/rock, 120-140 = upbeat, 140+ = dance/punk/etc.

### Subdivision, syncopation, swing

How you divide each beat (eighths, sixteenths, triplets) creates the *feel* of the rhythm. Syncopation — accenting off-beats — is where groove lives. Swing is a deliberate uneven subdivision common in jazz, hip-hop, and shuffle.

### Polyrhythm

Two rhythms running at once (e.g., 3 against 4). Less common in pop but a fingerprint in some artists.

---

## 4. Melody

### Contour

The up-and-down shape of a melodic line. Arch shapes (rise, peak, fall) are extremely common because they feel like a complete gesture.

### Motif and development

A motif is a small melodic idea (3–7 notes) that gets repeated, transposed, inverted, or extended. Songwriters lean on motifs because human ears love recognition.

### Phrasing

Melodies are organized into phrases roughly the length of a comfortable breath. Phrases often come in pairs (call and response).

### Prosody

How the melody fits the lyrics. Good prosody puts stressed syllables on strong beats and important words on high notes. Bad prosody is when a melody fights the words.

---

## 5. Song-level structure

> Covered in more depth in [`songwriting-and-lyrics.md`](songwriting-and-lyrics.md).

Standard forms: intro → verse → (pre-chorus) → chorus → verse → (pre-chorus) → chorus → bridge → chorus → outro. The chorus is melodically/harmonically the climax; the verse builds tension; the bridge provides contrast.

---

## 6. Why "rules" get broken

Music theory is descriptive, not prescriptive. The "rules" describe what most pleasant-sounding Western music has done historically. Breaking rules deliberately is how genres differentiate:
- Jazz adds extensions that classical "forbids."
- Rock leans on power chords (no 3rd) that simplify harmony.
- Hip-hop borrows from anywhere.
- Twenty One Pilots routinely modulates within a song, blurs verse/chorus lines, and uses meter changes — all "rule breaks" that are part of their identity.

The system has to know the rules to know when an artist is breaking them on purpose.

---

## Recommended next reads

- [Music Theory for the 21st-Century Classroom (free PDF)](https://musictheory.pugetsound.edu/hw/MusicTheory.pdf) — comprehensive academic text.
- LANDR's [music theory guide](https://blog.landr.com/music-theory/) — friendlier, songwriter-oriented.
- Adam Neely on YouTube — deep dives into theory through pop music examples.
- 8bitMusicTheory on YouTube — particularly good on modes and "why does this sound like X" questions.
