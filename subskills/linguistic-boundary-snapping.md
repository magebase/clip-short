# Subskill: Linguistic Boundary Snapping & Acoustic Decay

Autonomous speech transcript processing, phoneme-level audio alignment, conversational filler elimination, and natural thought boundary snapping for short-form clips.

---

## 1. Core Narrative Constraints

```
[Cold Open Sentence]               [Core Insight & Conflict]              [Terminal Punchline]
   t_start                                                                     t_end
      |==========================================================================|
  +60-80ms room tone                                                      +150-250ms decay
  +35ms fade-in                                                           +80ms fade-out
```

- **Target Runtime**: Strictly $18.0\text{s} - 22.5\text{s}$ (absolute hard ceiling at $23.5\text{s}$).
- **Single Standalone Thought**: Hook $\to$ Context $\to$ Insight $\to$ Satisfying Conclusion.

---

## 2. Cold Open Snapping Laws

### Zero Filler Words & Clean Word Onsets
Clips must NEVER start mid-clause, mid-stutter, or with conversational throat-clearing:
- **Forbidden Starters**: `um`, `uh`, `er`, `you know`, `like`, `so`, `basically`, `literally`, `and then`, `>>`, `-`.
- **Allowed Starters**: Direct pronoun/noun phrase ("The biggest mistake...", "You cannot build...", "When Apple released...", "Nobody realized...").

### Algorithm for Start Boundary Snapping
1. Search backward or forward from nominal candidate timestamp for nearest complete sentence beginning.
2. Locate Whisper word-level timestamp for first word $w_0$:
   $$t_{\text{word\_start}} = w_0.\text{start}$$
3. Add clean pre-speech room tone padding:
   $$t_{\text{clip\_start}} = \max(0.0, t_{\text{word\_start}} - 0.070)$$
4. Apply audio micro fade-in filter:
   $$\text{afade}=t=\text{in}:ss=0:d=0.035$$
   This eliminates frame-0 audio pops and breath clicks while ensuring immediate acoustic clarity.

---

## 3. Terminal Punchline Snapping & Acoustic Decay

### Zero Trailing Syllables or Mid-Clause Cuts
Clips must NEVER cut off while the speaker is mid-word, mid-breath, or introducing a continuation clause:
- **Forbidden Enders**: Prepositions (`in`, `at`, `to`, `for`, `with`), conjunctions (`and`, `but`, `or`, `because`, `which`, `that`), auxiliary verbs (`is`, `was`, `are`, `have`), or trailing filler words.
- **Mandatory Enders**: Terminal punctuation mark (`.`, `!`, `?`) accompanied by natural voice inflection drop or resolution.

### Algorithm for Terminal Snapping
1. Scan transcript words in the target duration window ($18.0\text{s} \le t_{\text{dur}} \le 22.5\text{s}$).
2. Identify words followed by terminal punctuation $[. ! ?]$.
3. Locate Whisper word-level end timestamp for terminal word $w_{\text{final}}$:
   $$t_{\text{word\_end}} = w_{\text{final}}.\text{end}$$
4. Add acoustic room tone decay padding:
   $$t_{\text{decay}} = 0.180\text{s} \quad (180\text{ms})$$
   $$t_{\text{clip\_end}} = t_{\text{word\_end}} + t_{\text{decay}}$$
5. Apply audio micro fade-out filter across final $80\text{ms}$:
   $$t_{\text{fade\_start}} = t_{\text{clip\_end}} - 0.080$$
   $$\text{afade}=t=\text{out}:st=t_{\text{fade\_start}}:d=0.080$$

This guarantees seamless loop playback on TikTok, YouTube Shorts, and Instagram Reels without harsh acoustic truncation.
