# 100-Point Viral Scoring Rubric & Auto-Critique

Every candidate short cut must be programmatically evaluated against this 100-point multi-modal critique rubric before rendering. Clips scoring below **80/100** are rejected or sent for automated parameter re-tuning.

---

## 1. Rubric Dimension Weights

$$\text{Total Score} = S_{\text{hook}} + S_{\text{coherence}} + S_{\text{linguistic}} + S_{\text{mobile}} + S_{\text{captions}} + S_{\text{audio}} + S_{\text{density}}$$

| Dimension | Max Points | Weight | Metric Evaluated | Pass Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **1. Hook Impact (0.0–1.0s)** | 20 pts | 20% | Opening energy, cold visual change, high-curiosity keyword in first 1.5s | $\ge 15/20$ |
| **2. Narrative Coherence** | 20 pts | 20% | Standalone thought structure (Hook $\to$ Context $\to$ Conflict $\to$ Punchline) | $\ge 16/20$ |
| **3. Linguistic Boundaries** | 15 pts | 15% | Clean sentence cold open (0 fillers) & terminal punctuation punchline | $\ge 12/15$ |
| **4. Mobile Composition** | 15 pts | 15% | Golden 54/46 framing, headroom clearance, zero UI/chrome clutter | $\ge 12/15$ |
| **5. Kinetic Typography** | 10 pts | 10% | Safe zone clearance ($MarginV=920$), 0 collision with seam/card, semantic chunks | $\ge 8/10$ |
| **6. Audio Dynamics** | 10 pts | 10% | EBU R128 loudness ($-14.0\text{ LUFS}$), peak $\le -1.0\text{ dBTP}$, room tone micro-fades | $\ge 8/10$ |
| **7. Information Density** | 10 pts | 10% | Zero dead air ($> 0.8\text{s}$ silence/freeze), continuous visual progression | $\ge 7/10$ |

---

## 2. Detailed Dimension Breakdown

### 1. Hook Impact (20 Points)
- **20 pts**: First spoken word occurs within $0.05\text{s} - 0.15\text{s}$. Spoken words introduce an immediate high-stakes claim, contrarian thesis, or provocative number. Top Curiosity Hook Pill badge renders at $y=135$.
- **15 pts**: Speech starts within $0.3\text{s}$. Hook is engaging but requires mild context.
- **10 pts**: Speech starts after $0.5\text{s}$ or opens with introductory transition ("So today...", "Well...").
- **0 pts**: Opening dead air $> 0.8\text{s}$ or incomprehensible mumble. Immediate disqualification.

### 2. Narrative Coherence (20 Points)
- **20 pts**: A complete, self-contained miniature story. The viewer needs zero context from the parent livestream to understand the thesis, conflict, and payoff.
- **15 pts**: Complete thought, but minor contextual pronouns ("he said", "that project") left slightly ambiguous.
- **10 pts**: Anecdote is understandable but punchline feels abrupt or unresolved.
- **0 pts**: Thought cuts off mid-argument or mid-sentence. Immediate disqualification.

### 3. Linguistic Boundaries & Sound Snapping (15 Points)
- **15 pts**:
  - **Start Snapping**: Snapped to initial phoneme of first meaningful word. Zero pre-speech conversational fillers (`um`, `uh`, `you know`, `like`). Pre-speech room tone padding: $60\text{ms} - 80\text{ms}$ with $35\text{ms}$ audio fade-in (`afade=t=in:d=0.035`).
  - **End Snapping**: Snapped strictly to terminal punctuation (`.`, `!`, `?`). Zero cutoffs of trailing syllables. Natural acoustic room decay padding: $120\text{ms} - 220\text{ms}$ with $80\text{ms}$ audio micro fade-out (`afade=t=out:d=0.08`).
- **10 pts**: Clean cut, but room tone decay is slightly tight ($< 100\text{ms}$) or contains a minor breath intake.
- **0 pts**: Clip cuts mid-word or ends on a conjunction/preposition (`and`, `but`, `because`, `which`).

### 4. Mobile Framing & Saliency (15 Points)
- **15 pts**: Speaker framed in upper 54% pane with natural headroom ($+0.32 \times fh$). Bottom supporting pane shows primary content centered at 1000 px width with 40 px side margins. Seam cleanly divider-lined. Zero browser tabs, taskbars, or fragmented UI scrollbars.
- **10 pts**: Clear split, but supporting content has minor margin imbalance ($< 25\text{px}$) or slight sidebar visibility.
- **0 pts**: Head/chin cutoff in speaker pane, or supporting content unreadable/clipped.

### 5. Kinetic Typography & Safe Zones (10 Points)
- **10 pts**: Subtitle baseline positioned at $y = 1000$ (`MarginV = 920`). Over $180\text{px}$ clearance above supporting content ($y \ge 1180$). 0.0 px collision with divider seam ($y = 1038$). 3 to 5 words per semantic chunk, kinetic punch animation on keyword, vector emoji rendering.
- **7 pts**: Legible subtitles in safe zone, but slight 1-2 word staccato rhythm.
- **0 pts**: Subtitle baseline $> 1030\text{px}$ (overlaps divider seam), horizontal margin $< 25\text{px}$, or overlapping burnt-in text.

### 6. Audio Dynamics & Mastering (10 Points)
- **10 pts**: Broadcast integrated loudness normalized to $-14.0\text{ LUFS} \pm 0.5\text{ LUFS}$. True peak clamped to $\le -1.0\text{ dBTP}$. Zero audio clicks, pops, or clipping.
- **7 pts**: Loudness between $-16.0$ and $-12.0\text{ LUFS}$, no audible clipping.
- **0 pts**: Distorted peaks ($> 0.0\text{ dBFS}$) or low volume ($< -20.0\text{ LUFS}$).

### 7. Information Density & Pacing (10 Points)
- **10 pts**: Total duration strictly within $18.0\text{s} - 22.5\text{s}$ (max $23.5\text{s}$). Visual transformation or punch-in every $2.5\text{s} - 3.5\text{s}$. Zero freeze frames $> 0.8\text{s}$.
- **7 pts**: Duration within $16\text{s} - 25\text{s}$, smooth pacing.
- **0 pts**: Duration $< 15\text{s}$ or $> 28\text{s}$, or frozen static video $> 1.0\text{s}$.

---

## 3. Disqualification Flags (Auto-Fail to 0 Points)
A candidate clip is immediately disqualified (`REJECTED_QUALITY`) if ANY of the following flags trip:
1. `HAS_BURNT_SUBTITLES`: Persistent hardcoded subtitles detected in subtitle band ($0.52 \le y \le 0.88$).
2. `BLURRY_FOOTAGE`: Multi-frame Laplacian variance $< 65.0$.
3. `DANGLING_END`: Terminal cut falls on a preposition, conjunction, or incomplete sentence clause.
4. `FILLER_COLD_OPEN`: Clip begins with filler syllable (`um`, `uh`, `like`).
5. `MISMATCHED_METADATA`: HUD headline or title does not match spoken discourse in the clip.
6. `COLLISION_SUBTITLES`: Subtitles collide with divider seam ($y = 1038$) or supporting visual cards.
