# Clipper Visual Source Archetypes & Detection Heuristics

Visual source truth comes before editing. Classify what the footage physically is (Axis A), then route layout and treatment.

This file covers visual archetypes only. Narrative archetype and editing treatment live in [../subskills/format-router-templates.md](../subskills/format-router-templates.md).

---

## 1. Archetype Matrix

| Code | Archetype | Typical sources | Visual structure | Detection heuristic | Default layout |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ARCH-01` | **Corner PiP Streamer** | Theo, Primeagen, PirateSoftware, MoistCr1TiKaL | Corner webcam plus desktop/code/tweet | Relative face area $A_{rel} < 0.045$; centroid in a corner; stable position | `ADAPTIVE_SPLIT` / `PIP_SPLIT` |
| `ARCH-02` | **Solo Talking Head** | Huberman Lab, TED, Diary of a CEO | One centered subject to camera | Centered face $C_x \in [0.40, 0.60]$, $A_{rel} \ge 0.08$ | `FULLSCREEN_PORTRAIT` |
| `ARCH-03` | **Multi-Cam Podcast** | Lex Fridman, JRE, All-In, Flagrant | Two or three camera angles cutting between speakers | Alternating large faces or hard camera cuts with one face per shot | `DYNAMIC_SPEAKER` |
| `ARCH-04` | **Gaming + Facecam** | Shroud, Tarik, xQc | Gameplay plus webcam overlay | High optical-flow density plus static face box | `ACTION_SAFE` / `PIP` |
| `ARCH-05` | **Slide Presentation** | Keynotes, investor days | Slide with podium or floating speaker | High-contrast rectangle $\ge 0.70W$, low internal motion | `SLIDE_ISOLATION` |
| `ARCH-06` | **Full-Screen Screen Recording** | Tutorials, coding demos | Active window, terminal, or code | Low face area, high edge density, stable window chrome | `ACTIVE_WINDOW` |
| `ARCH-07` | **Whiteboard / Diagram** | Excalidraw, whiteboard, architecture talks | Hand-drawn or vector diagram canvas | Stroke motion, sparse color, large unoccluded canvas | `PROGRESSIVE_DIAGRAM` |
| `ARCH-08` | **Full-Screen Gaming** | Esports, gameplay VODs | Game fills frame, no facecam | Motion field plus HUD elements, no persistent face | `FULLSCREEN_ACTION` |
| `ARCH-09` | **Narrated Illustration / Animation** | Veritasium illustrated stories, Kurzgesagt | Painted or animated scenes with voiceover | Low live-action face area, scene-to-scene cuts, narration-only audio | `SCENE_TRACKING` |
| `ARCH-10` | **Narrated Documentary / B-Roll** | Documentaries, video essays | Archival or contextual footage with voiceover | Voiceover plus non-speaking visuals, scene cuts, no host face | `FULLSCREEN_CONTEXT` |
| `ARCH-11` | **Sports / Action** | Highlights, match footage | Playing surface, athletes, scoreboard | Fast global motion, play-region tracking, score bug | `FULLSCREEN_ACTION` |
| `ARCH-12` | **Live Performance** | Concerts, stand-up, stage shows | Stage lighting, performer, crowd | Stage geometry, lighting changes, applause audio | `FULLSCREEN_STAGE` |
| `ARCH-13` | **Product Demonstration** | Reviews, unboxings, how-to | Hands, product, result close-ups | Hand/object saliency, tabletop framing, close-up cuts | `OBJECT_FOCUS` |
| `ARCH-14` | **Dual-Speaker Debate** | Split-stage debates, interviews in one frame | Two large faces in one wide shot | Two persistent face boxes with similar area | `SPEAKER_SWITCH` or stacked split |

---

## 2. Detection Features

Compute per sampled second, then aggregate:

- `face_count`, `face_boxes`, relative face area, centroid, centroid variance.
- Optical-flow magnitude and variance.
- Sobel edge density map.
- High-contrast rectangle detection for slides.
- Static overlay rectangles for facecams, score bugs, and lower thirds.
- Transcript presence and speaker-turn structure.

### Corner PiP (`ARCH-01`)
A sequence is `PIP_SPLIT` when MediaPipe BlazeFace reports:
1. $A_{rel} = \frac{W_{face} \times H_{face}}{W_{frame} \times H_{frame}} < 0.045$
2. $C_x \le 0.35$ or $C_x \ge 0.65$; $C_y \le 0.35$ or $C_y \ge 0.65$
3. Centroid stability $\sigma_C < 0.08$ across consecutive seconds.

### Multi-Cam (`ARCH-03`)
- Multiple hard cuts in the source window.
- Exactly one dominant face per shot.
- Speaker changes correlate with camera changes.

### Narrated Illustration (`ARCH-09`)
- No persistent live-action face.
- Scene-to-scene visual discontinuity.
- Continuous narration over visuals.
- Illustration detection: low photographic texture, flat color regions, painted edges.

### Slide Deck (`ARCH-05`)
- Rectangular high-contrast region with mostly static pixels.
- Text-like edge density inside the rectangle.
- Presenter may be absent, inset, or on a separate camera.

---

## 3. Layout and Treatment Constraints

| Archetype | Must do | Must not do |
| :--- | :--- | :--- |
| `ARCH-01` | Keep speaker readable; isolate the active card | Shrink a panoramic diagram into the bottom pane |
| `ARCH-02` | Face-aware crop and motivated punch-ins | Add empty split-screen chrome |
| `ARCH-03` | Cut on speaker turns; dwell $\ge 1.8\text{s}$ | Rapid arbitrary cuts |
| `ARCH-04` | Keep action and facecam readable | Crop the play area out of frame |
| `ARCH-05` | Isolate the slide; preserve all labels | Crop slide edges or shrink below readability |
| `ARCH-06` | Track the active window and zoom to the referenced control | Show full desktop with unreadable text |
| `ARCH-07` | Follow the diagram's semantic beats | Permanently display the entire diagram |
| `ARCH-08` | Track action centroid with padding | Cut off the objective or HUD |
| `ARCH-09` | Full-screen scene tracking with story-order pacing; optional 0.5–1.0s cold-open teaser of the key object or reveal, then return to the investigation setup | Apply streamer split-screen or meme chrome; spoil the reveal in the teaser |
| `ARCH-10` | Full-screen contextual visuals | Shrink footage into a decorative pane |
| `ARCH-11` | Track the play; keep score context when relevant | Crop the ball/athlete out |
| `ARCH-12` | Preserve stage composition and performance energy | Over-crop to a face-only frame for the whole clip |
| `ARCH-13` | Show hands, product, and result | Obscure the demonstration with captions |
| `ARCH-14` | Hold the speaker making the argument | Cut away mid-point |

---

## 4. Known Failure Modes

- Forcing `ARCH-01` split geometry onto `ARCH-09` illustration sources.
- Treating `ARCH-05` slides as a bottom-pane card and shrinking titles below readability.
- Choosing `ARCH-07` supporting content by largest contour when the largest contour is a chat column.
- Cutting `ARCH-03` before the speaker finishes the point.
- Cropping `ARCH-11` action so the decisive play leaves the frame.
- Reusing one creator's visual recipe across unrelated source archetypes.

### Narrative Pacing Notes
- A cold-open teaser may preview the central object or mystery, but it must not reveal the resolution.
- Rising action should not become visually quiet: keep illustration pans, reveals, or motivated cuts active through the setup so the middle does not stall.
- Preserve the complete reveal-and-conclusion sequence; compress investigation setup before trimming the payoff.

Any of these is a production-gate failure, not a stylistic preference.
