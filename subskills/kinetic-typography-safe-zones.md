# Subskill: Face-Aware Kinetic Typography & Safe Zones

Typography placement, safe-zone computation, collision avoidance, kinetic animation, and text-layer separation for vertical short clips.

Safe zones are computed from the layout and the subject's face, not hardcoded to one absolute coordinate. `MarginV = 920` is the canonical value for the 54/46 split preset only.

---

## 1. Safe Zone Geometry (54/46 Preset)

```
y = 0     +---------------------------------------------------+
          |  Top Edge Clutter Safe Buffer (>60px)             |
y = 135   |  [ CURIOSITY HOOK PILL ] (Fades out at 3.0s-3.8s)  |
          |                                                   |
          |                 SPEAKER WEBCAM                    |
          |                                                   |
y = 920   |  ===============================================  | <-- Subtitle Box Top MarginV
y = 1000  |     KINETIC SUBTITLES BASELINE OVER TORSO         |
          |  ===============================================  |
y = 1038  |---------------- 4px Seam Divider -----------------| <-- 0.0px Collision Boundary
y = 1042  |                                                   |
          |            SUPPORTING DESKTOP / CODE CARD         |
y = 1180  |            Active Supporting Content Top          | <-- >180px Clearance Buffer
          +---------------------------------------------------+
y = 1920
```

### Critical Thresholds
1. **Vertical Baseline**: $y = 1000\text{px}$ (`MarginV = 920`).
2. **Maximum Safe Baseline**: $y \le 1030\text{px}$. Any text at $y > 1030\text{px}$ is `COLLISION_DIVIDER`.
3. **Clearance to Supporting Content**: supporting content begins at $y \ge 1180\text{px}$, providing $\ge 180\text{px}$ of clean space.
4. **Horizontal Margins**: minimum $40\text{px}$ left and right ($x \in [40, 1040]$).

---

## 2. Face-Aware Placement Rule

For every sampled frame containing text:

1. Detect face landmarks (eyes, nose, mouth, chin, crown).
2. Build the **protected region**: bounding box around eyes and mouth expanded by $12\%$.
3. Reject or reposition any text bounding box that intersects the protected region.
4. For the top HUD pill, prefer the side of the frame opposite the face centroid. If the pill cannot clear the face, shorten it or reduce the y-offset within the top safe buffer.
5. For subtitles, place the baseline over the torso below the chin. If no torso space exists in the chosen layout, move captions to the lower third that clears both face and source text.

### Adaptive Layout Baselines
| Layout | Caption rule |
| :--- | :--- |
| `FULLSCREEN_PORTRAIT` | Baseline below chin, above bottom UI; never over eyes/mouth |
| `DYNAMIC_SPEAKER` | Recompute per shot from the active speaker's landmarks |
| `ADAPTIVE_SPLIT` | 54/46 preset safe zone (`MarginV = 920`) |
| `PROGRESSIVE_DIAGRAM` | Captions must not cover diagram labels or arrows |
| `SCENE_TRACKING` / `MINIMAL_DOCUMENTARY` | Lower third that avoids key subject and source text |
| `SLIDE_ISOLATION` | Captions outside the slide content or in a reserved strip |
| `FULLSCREEN_ACTION` | Captions must not cover the ball, athlete, or score bug |

---

## 3. Kinetic Typography Formatting Laws

### 1. 3–5 Word Semantic Chunks (Zero Staccato Flashes)
- **Forbidden**: single-word or two-word rapid flashing cues ($< 250\text{ms}$). This causes cognitive fatigue.
- **Enforced**: natural syntactic phrase groups (3 to 5 words, e.g., `"The entire backend was"`, `"completely rewritten in Rust"`).
- **Contractions preserved**: never break `don't`, `can't`, `it's`.

### 2. Single-Line Buffer Deduplication
- Consecutive cues must never duplicate words or overlap.
- Subtitle cues render as single-line or tight two-line blocks with centered alignment.
- Use the verified transcript. Captions must match spoken words, including negations and entities.

### 3. Kinetic Animation Grammar
- **Level 1 (Narrative Text)**: clean white sans-serif (`Montserrat-Black` or `Inter-Bold`), 48–54px, 3px black stroke, subtle shadow.
- **Level 2 (Emphasis Words)**: high-contrast neon accents:
  - Electric Yellow: `#FACC15`
  - Neon Cyan: `#06B6D4`
  - Emerald Green: `#10B981`
  - Amber Gold: `#F59E0B`
  - Punch scale: $115\%$ spring pop on emphasized word onset.
- **Level 3 (Vector Emojis)**: rendered inline adjacent to emotion/tech keywords, only when the tone supports it. No emojis in historical or documentary narration.

---

## 4. Top Safe-Zone Curiosity Hook Pill

At the cold open, viewers decide whether to swipe within about $1.2\text{s}$. The pill reinforces the verbal thesis without repeating it.

- **Position**: near $y = 135\text{px}$, horizontally face-aware.
- **Typography**: `Anton-Regular.ttf`, 32px, Title Case, white text with 2px black outline.
- **Container**: translucent dark slate pill (`#0F172A@0.92`), 24px horizontal and 12px vertical padding.
- **Lifecycle**:
  - $0.0\text{s} - 3.0\text{s}$: fully opaque.
  - $3.0\text{s} - 3.8\text{s}$: linear fade to $0\%$.
  - $> 3.8\text{s}$: gone; the frame is clean for facial expression.
- **Content**: verified headline only. No debug tokens, no phase labels, no unresolved placeholders.

---

## 5. Five Separated Text Layers

Do not reuse one string everywhere. Each layer has a distinct job:

| Layer | Function | Length | Source |
| :--- | :--- | :--- | :--- |
| HUD headline | Hook curiosity in the first seconds | 3–6 words, $\le 38$ chars | Verified transcript + paraphrase |
| Subtitles | Verbatim comprehension | 3–5 word cues | Verified transcript |
| YouTube title | Search and feed discovery | 45–65 chars | Faithful paraphrase of the cut |
| Thumbnail headline | One visual promise | 2–5 words | Independent thumbnail stage |
| Campaign caption | Submission requirements | Campaign config | Campaign rules |

Consistency is semantic, not verbatim. The thumbnail must not duplicate the HUD headline, and the YouTube title must not simply repeat the first spoken sentence.

---

## 6. Collision and Readability QA

Reject (`REJECTED_RENDER`) when any of these occur:

- Caption baseline $> 1030\text{px}$ in the 54/46 preset.
- Horizontal margin $< 25\text{px}$.
- Text intersects the face protected region.
- Captions overlap source text, diagram labels, tickers, or slide content.
- Staccato 1–2 word cues or duplicate consecutive cues.
- Terminal phrase truncated at the cut.
- Headline or thumbnail covers eyes or mouth.
- Font size unreadable at mobile preview size.
- More than one headline block on the thumbnail.
