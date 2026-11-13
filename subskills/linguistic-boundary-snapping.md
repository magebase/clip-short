# Subskill: Narrative-First Boundary Snapping & Acoustic Decay

Autonomous speech transcript processing, phoneme-level alignment, filler elimination, terminal punchline snapping, and campaign-aware duration resolution.

---

## 1. Duration Resolution Order

Runtime is a campaign decision constrained by narrative completeness, not a fixed house number applied to every source.

1. **Campaign rule** — if the loaded campaign config defines `min_seconds` / `max_seconds`, that range is binding.
2. **Narrative completion** — the selected cut must reach a terminal punctuation boundary where the thought resolves.
3. **Default house range** — $18.0\text{s} - 22.5\text{s}$ with a flexible ceiling up to $23.5\text{s}$ when required to finish a thought.

### Do Not Destroy the Payoff
If the story needs $24.3\text{s}$ to reach the confession, do not cut the confession to satisfy $23.5\text{s}$. First compress the setup by removing redundant investigation beats. Only if the campaign hard-limits duration and compression cannot preserve the payoff should the candidate be rejected or sent to `HUMAN_REVIEW`.

### Resolution Algorithm
```python
def resolve_duration(campaign, sentence_boundaries):
    lo, hi = campaign.min_seconds, campaign.max_seconds
    if lo is None or hi is None:
        lo, hi = 18.0, 23.5

    candidates = [b for b in sentence_boundaries if lo <= b.duration <= hi and b.is_terminal]
    if candidates:
        return max(candidates, key=lambda b: b.narrative_completeness).duration

    if campaign.max_seconds is None:
        completed = [b for b in sentence_boundaries if b.duration >= lo and b.is_terminal]
        if completed:
            return min(completed, key=lambda b: b.duration).duration

    return None  # fail closed; compress setup or choose another candidate
```

---

## 2. Core Narrative Constraints

```
[Cold Open Sentence]               [Core Insight & Conflict]              [Terminal Punchline]
   t_start                                                                     t_end
      |==========================================================================|
  +60-80ms room tone                                                      +150-250ms decay
  +35ms fade-in                                                           +80ms fade-out
```

- **Single Standalone Thought**: Hook $\to$ Context $\to$ Insight $\to$ Satisfying Conclusion.
- **No setup-only cuts**: a clip that ends before the consequence is rejected on narrative grounds even if all technical gates pass.

---

## 3. Cold Open Snapping Laws

### Zero Filler Words & Clean Word Onsets
Clips must NEVER start mid-clause, mid-stutter, or with conversational throat-clearing:
- **Forbidden Starters**: `um`, `uh`, `er`, `you know`, `like`, `so`, `basically`, `literally`, `and then`, `>>`, `-`.
- **Allowed Starters**: direct pronoun/noun phrase ("The biggest mistake...", "You cannot build...", "When Apple released...", "Nobody realized...").

### Algorithm for Start Boundary Snapping
1. Search backward or forward from the nominal candidate timestamp for the nearest complete sentence beginning.
2. Locate the word-level timestamp for first word $w_0$:
   $$t_{\text{word\_start}} = w_0.\text{start}$$
3. Add clean pre-speech room tone padding:
   $$t_{\text{clip\_start}} = \max(0.0, t_{\text{word\_start}} - 0.070)$$
4. Apply audio micro fade-in filter:
   $$\text{afade}=t=\text{in}:ss=0:d=0.035$$
   This eliminates frame-0 audio pops and breath clicks while ensuring immediate acoustic clarity.

---

## 4. Terminal Punchline Snapping & Acoustic Decay

### Zero Trailing Syllables or Mid-Clause Cuts
Clips must NEVER cut off while the speaker is mid-word, mid-breath, or introducing a continuation clause:
- **Forbidden Enders**: prepositions (`in`, `at`, `to`, `for`, `with`), conjunctions (`and`, `but`, `or`, `because`, `which`, `that`), auxiliary verbs (`is`, `was`, `are`, `have`), or trailing filler words.
- **Mandatory Enders**: a terminal punctuation mark (`.`, `!`, `?`) accompanied by natural voice inflection drop or resolution.

### Algorithm for Terminal Snapping
1. Scan transcript words in the campaign duration window.
2. Identify words followed by terminal punctuation `[. ! ?]`.
3. Locate the word-level end timestamp for terminal word $w_{\text{final}}$:
   $$t_{\text{word\_end}} = w_{\text{final}}.\text{end}$$
4. Add acoustic room tone decay padding:
   $$t_{\text{decay}} = 0.180\text{s} \quad (180\text{ms})$$
   $$t_{\text{clip\_end}} = t_{\text{word\_end}} + t_{\text{decay}}$$
5. Apply audio micro fade-out across the final $80\text{ms}$:
   $$t_{\text{fade\_start}} = t_{\text{clip\_end}} - 0.080$$
   $$\text{afade}=t=\text{out}:st=t_{\text{fade\_start}}:d=0.080$$

This guarantees clean playback on TikTok, YouTube Shorts, and Instagram Reels without harsh acoustic truncation.

---

## 5. Campaign-Aware Boundary Constraints

| Campaign rule | Effect on boundary snapping |
| :--- | :--- |
| `min_seconds` / `max_seconds` | Defines the search window; never violated silently |
| `required_mentions` / `required_hashtags` | Must be present in the submission package; may require choosing a different cut that contains the required phrase |
| `required_content` | The cut must actually contain it; do not add it only in metadata |
| `prohibited_content` | Any occurrence in audio or visuals fails the cut |
| `required_sound` | Audio bed selection changes; speech boundaries still rule |
| `audience_requirements` | May force a shorter setup or stricter content screen |
| `public_post_required` / `linked_account_required` | Packaging and publishing constraints, not editorial ones |

If campaign rules contradict narrative completeness and no compliant cut exists, fail closed to `HUMAN_REVIEW`; do not publish a non-compliant or story-broken clip.

---

## 6. Transition and Loop Behavior

- The first frame must contain the strongest visual or spoken claim. No slow intros.
- The final frame should resolve visually and acoustically; if the campaign encourages loops, end on a visual that naturally reconnects to the opening.
- Never add a fake loop seam that cuts mid-word. The loop is a consequence of a complete thought, not a substitute for one.
