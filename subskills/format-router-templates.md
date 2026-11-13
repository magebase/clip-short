# Subskill: Three-Axis Format Router & Treatment Presets

Classifies a source segment along three independent axes, then selects a layout and editing treatment. The six legacy viral templates are retained as named treatment presets, not as the classifier itself.

---

## 1. The Three Axes

### Axis A — Visual Source Archetype
What the footage physically is. See [../references/clipper-format-archetypes.md](../references/clipper-format-archetypes.md) for detection heuristics.

`SOLO_TALKING_HEAD`, `MULTICAM_PODCAST`, `CORNER_PIP_SCREEN`, `FULLSCREEN_SCREEN`, `WHITEBOARD_DIAGRAM`, `SLIDE_DECK`, `GAMING_FACECAM`, `FULLSCREEN_GAMING`, `NARRATED_ILLUSTRATION`, `NARRATED_BROLL`, `SPORTS_ACTION`, `LIVE_PERFORMANCE`, `PRODUCT_DEMO`, `DUAL_DEBATE`.

### Axis B — Narrative Archetype
What the story is.

`CURIOSITY_MYSTERY`, `CONTRARIAN_OPINION`, `EXPLANATION`, `DEBATE`, `PERSONAL_STORY`, `DEMONSTRATION`, `COMEDY`, `REACTION`, `LIST_STEPS`, `EMOTIONAL_REVELATION`.

### Axis C — Editing Treatment
How this story should be shown.

`FULLSCREEN_CROP`, `DYNAMIC_SPEAKER_SWITCHING`, `ADAPTIVE_SPLIT`, `PICTURE_IN_PICTURE`, `PROGRESSIVE_DIAGRAM_ZOOM`, `SCENE_BY_SCENE`, `ANIMATED_CAPTIONS`, `CONTEXTUAL_BROLL`, `MINIMAL_DOCUMENTARY`.

A treatment is a hypothesis. It must be validated against the source content before rendering.

---

## 2. Classifier Output Contract

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SegmentClassification:
    visual_archetype: str
    narrative_archetype: str
    editing_treatment: str
    layout_mode: str
    confidence: float
    evidence: dict

def classify_segment(
    words: List[dict],
    duration_sec: float,
    face_boxes: Optional[List[tuple]] = None,
    frame_features: Optional[dict] = None,
    audio_features: Optional[dict] = None,
    transcript_entities: Optional[List[str]] = None,
) -> SegmentClassification:
    ...
```

Rules:
- Never return a single "format" string that merges the axes.
- If confidence is below $0.60$, return `HUMAN_REVIEW`.
- Evidence must include the features that justified each axis.
- The classifier never decides runtime or campaign compliance; those come from campaign preflight.

---

## 3. Classification Rules

### Visual Archetype
| Signal | Archetype |
| :--- | :--- |
| Small face box in a corner, desktop content behind | `CORNER_PIP_SCREEN` |
| One large centered face, no screen content | `SOLO_TALKING_HEAD` |
| Multiple cameras alternating between speakers | `MULTICAM_PODCAST` |
| Two large faces in the same wide frame | `DUAL_DEBATE` |
| Active window / code / terminal fills the frame | `FULLSCREEN_SCREEN` |
| Hand-drawn strokes or diagram canvas | `WHITEBOARD_DIAGRAM` |
| High-contrast slide rectangle occupying $\ge 70\%$ width | `SLIDE_DECK` |
| Gameplay motion field plus facecam overlay | `GAMING_FACECAM` |
| Gameplay motion field without facecam | `FULLSCREEN_GAMING` |
| Narrated painted/animated scenes | `NARRATED_ILLUSTRATION` |
| Narrated real footage and archival material | `NARRATED_BROLL` |
| Ball/athlete motion, scoreboard, playing surface | `SPORTS_ACTION` |
| Stage, instruments, crowd, performance lighting | `LIVE_PERFORMANCE` |
| Hands manipulating a product, result close-ups | `PRODUCT_DEMO` |

### Narrative Archetype
Use transcript semantics plus structure:
- Question that withholds an answer $\to$ `CURIOSITY_MYSTERY`.
- Thesis stated against consensus $\to$ `CONTRARIAN_OPINION`.
- Mechanism, cause, or how-to $\to$ `EXPLANATION`.
- Alternating disagreement with turn-taking $\to$ `DEBATE`.
- First-person chronology with stakes $\to$ `PERSONAL_STORY`.
- Claim followed by result $\to$ `DEMONSTRATION`.
- Setup and punchline $\to$ `COMEDY`.
- Stimulus and response $\to$ `REACTION`.
- Enumerated items or steps $\to$ `LIST_STEPS`.
- Reveal with strong personal stakes $\to$ `EMOTIONAL_REVELATION`.

### Editing Treatment
| Combination | Treatment |
| :--- | :--- |
| `MULTICAM_PODCAST` + `CONTRARIAN_OPINION` | `DYNAMIC_SPEAKER_SWITCHING` |
| `CORNER_PIP_SCREEN` + `EXPLANATION` | `ADAPTIVE_SPLIT` or `PROGRESSIVE_DIAGRAM_ZOOM` |
| `WHITEBOARD_DIAGRAM` + `EXPLANATION` | `PROGRESSIVE_DIAGRAM_ZOOM` |
| `NARRATED_ILLUSTRATION` + `CURIOSITY_MYSTERY` | `SCENE_BY_SCENE` |
| `NARRATED_BROLL` + `PERSONAL_STORY` / `CURIOSITY_MYSTERY` | `MINIMAL_DOCUMENTARY` |
| `SOLO_TALKING_HEAD` + `CONTRARIAN_OPINION` | `FULLSCREEN_CROP` |
| `GAMING_FACECAM` + `REACTION` | `PICTURE_IN_PICTURE` |
| `SPORTS_ACTION` + `DEMONSTRATION` | `FULLSCREEN_CROP` |
| `PRODUCT_DEMO` + `DEMONSTRATION` | `FULLSCREEN_CROP` with `OBJECT_FOCUS` |
| Any + `LIST_STEPS` | `ANIMATED_CAPTIONS` with step tracker only if spoken |

The treatment must be consistent with the source. A narrated illustrated story does not receive streamer split-screen chrome. A technical diagram does not receive permanent full-frame display if its labels become unreadable.

---

## 4. Legacy Treatment Presets

These remain supported as named presets. They are combinations, not classifier outputs.

| Preset | Axis combination | Core mechanic |
| :--- | :--- | :--- |
| `FORMAT_1_PHONK_FREEZE` | Action source + impact narrative + kinetic montage | Freeze on peak impact, punch-in, phonk bed |
| `FORMAT_2_REACTION_STACK` | Reaction source + reaction narrative + split | Top reactor / bottom stimulus with seam captions |
| `FORMAT_3_ACTION_TAG_SITCOM` | Performance/IRL + comedy + animated captions | Non-verbal action tags |
| `FORMAT_4_DISCORD_BROLL` | Voice + contextual B-roll | Speaker audio over relevant B-roll |
| `FORMAT_5_WHITEBOARD_EXPLAINER` | Screen/diagram + explanation + progressive diagram | Split or diagram zoom with semantic beats |
| `FORMAT_N3ON_PING_PONG` | Two-speaker IRL + banter + speaker switching | Turn-synced cuts with minimum dwell |

A preset may be rejected by the source. For example, `FORMAT_5_WHITEBOARD_EXPLAINER` must not force an entire panoramic diagram into a permanent bottom pane.

---

## 5. Worked Examples

| Source | Axis A | Axis B | Axis C | Layout |
| :--- | :--- | :--- | :--- | :--- |
| Lex / Harari podcast | `MULTICAM_PODCAST` | `CONTRARIAN_OPINION` | `DYNAMIC_SPEAKER_SWITCHING` | Full-screen face-aware crop, cuts on question/answer/trade-off/payoff |
| Theo architecture explainer | `CORNER_PIP_SCREEN` | `EXPLANATION` | `PROGRESSIVE_DIAGRAM_ZOOM` | Speaker pane plus sequenced diagram beats, or full-screen speaker during analogy |
| Veritasium flies story | `NARRATED_ILLUSTRATION` | `CURIOSITY_MYSTERY` | `SCENE_BY_SCENE` | Full-screen illustration tracking, tease, investigation, reveal, confession |

---

## 6. Top Headline Pill Builder

The HUD pill is a separate text layer from the YouTube title and the thumbnail headline.

- **Position**: safe zone $y = 135$, face-aware horizontally. If the face landmark box intersects the pill, move the pill to the nearest clear side or shorten it.
- **Dimensions**: adaptive width 420–860px, fixed height 76px.
- **Typography**: Anton Regular, 32px, Title Case, white text with a 2px black outline.
- **Container**: translucent dark slate pill (`#0F172A@0.92`) with 24px horizontal and 12px vertical padding.
- **Lifecycle**: fade out between 3.0s and 3.8s.
- **Content**: 3–6 words, max 38 characters, no trailing punctuation, verified against the transcript.

```bash
drawbox=x={PX}:y=135:w={DYNAMIC_W}:h=76:color=#0F172A@0.92:t=fill:enable='lte(t,3.8)',
drawtext=fontfile='Anton-Regular.ttf':text='{HEADLINE}':fontcolor=white:fontsize=32:borderw=2:bordercolor=black:x=(w-text_w)/2:y=153:alpha='if(lte(t,3.0), 1, if(lte(t,3.8), (3.8-t)/0.8, 0))'
```
