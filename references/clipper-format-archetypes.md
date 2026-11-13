# Clipper Format Archetypes & Detection Heuristics

Automated viral short clipping requires classifying source VOD compositions into deterministic visual archetypes before assigning crop geometry, motion progression, and typography zones.

---

## 1. Format Classification Matrix

| Format Code | Format Name | Typical Source Creators / Shows | Visual Structure | Automated Detection Heuristic | Target Composition |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ARCH-01` | **Corner PiP Streamer** | Theo (t3.gg), Primeagen, PirateSoftware, MoistCr1TiKaL | Corner webcam (top/bottom corner) + Desktop browser/code/tweet | Small face bounding box ($A_{rel} < 0.045$) anchored in corner ($C_x \notin [0.35, 0.65]$) | **Golden 54/46 Split-Screen** |
| `ARCH-02` | **Solo Speaker / Monologue** | Huberman Lab, Lex Fridman (monologue), Diary of a CEO, TED | Single centered subject speaking directly to camera | Centered face ($C_x \in [0.40, 0.60]$), large face area ($A_{rel} \ge 0.08$) | **Dynamic 9:16 Centered Crop with Motivated Punch-Ins** |
| `ARCH-03` | **Dual Multi-Cam Podcast** | Joe Rogan Experience, Lex Fridman Interview, All-In, Flagrant | Two or three camera angles switching between host and guest | Multiple face detections across frames or alternating single large faces | **Speaker-Switched 9:16 or Stacked Reaction Split** |
| `ARCH-04` | **Gaming Streamer** | Shroud, Tarik, TimTheTatman, xQc (gaming) | Fullscreen gameplay with webcam overlay box | High optical flow / motion vector density + static face box overlay | **Split-Screen or Dynamic Floating Facecam Overlay** |
| `ARCH-05` | **Presentation / Deck** | Apple Keynotes, Tech Conferences, Investor Days | Slide projection with speaker podium or floating pip | Dominant rectangular high-contrast slide ($W_{slide} \ge 0.70 W$) + speaker | **Slide Isolation + Bottom/Top Anchor** |

---

## 2. Corner PiP Streamer Architecture (`ARCH-01`)
The corner webcam + desktop setup is the highest-volume streamer format on YouTube and Twitch.

### Detection Heuristics
A video frame sequence is classified as `PIP_SPLIT` when MediaPipe BlazeFace reports:
1. **Relative Face Area**: $A_{rel} = \frac{W_{face} \times H_{face}}{W_{frame} \times H_{frame}} < 0.045$
2. **Centroid Coordinates**:
   $$\text{Horizontal: } C_x \le 0.35 \quad \text{or} \quad C_x \ge 0.65$$
   $$\text{Vertical: } C_y \le 0.35 \quad \text{or} \quad C_y \ge 0.65$$
3. **Centroid Stability**: Standard deviation $\sigma_C < 0.08$ across consecutive seconds (indicating a fixed physical webcam overlay).

### Composition Standard: Golden 54/46 Split
- **Canvas Resolution**: $1080 \times 1920$ vertical ($9:16$).
- **Top Dominant Speaker Pane**:
  - Dimensions: $1080 \times 1040$ ($54.17\%$ of total vertical height).
  - Crop: Aspect-locked $2.45 \times fh$ framing centered on face centroid with $+0.32 \times fh$ natural headroom offset.
  - Zero cutoff of forehead, chin, or shoulder posture.
- **Seam Separation**:
  - Horizontal divider line at $y = 1038$ px.
  - Thickness: 4 px.
  - Color: `#1E293B` (Dark slate gray) to provide crisp optical separation without bright jarring glare.
- **Bottom Supporting Card Pane**:
  - Dimensions: $1080 \times 880$ ($45.83\%$ of total vertical height).
  - Content: Saliency-isolated active tweet, terminal code, diagram, or article.
  - Framing: Primary card scaled to width 1000 px with 40 px left and right margins.
  - Ultrawide Fallback: Dark blurred ambient canvas (`boxblur=40:20, eq=brightness=-0.25`).

---

## 3. Solo Speaker Architecture (`ARCH-02`)
- **Composition**: $1080 \times 1920$ single-pane vertical crop.
- **Centroid Tracking**: Smooth exponential moving average ($\alpha = 0.15$) to prevent jerky lateral panning.
- **Motivated Punch-Ins**:
  - Phase 1 (0.0s – 3.0s Hook): $110\%$ punch-in to maximize intimacy and visual impact.
  - Neutral Phase: $100\%$ baseline framing.
  - Punchline / Climax: $112\%$ punch-in synchronized with speaker emphasis.

---

## 4. Multi-Cam Podcast Architecture (`ARCH-03`)
- **Mode A: Active Speaker Cut**:
  - Snaps cut to exact audio onset timestamp when host/guest alternates.
  - Retains $\ge 1.8$s minimum dwell time to eliminate nauseating rapid switching.
- **Mode B: Stacked Split**:
  - Top Pane ($1080 \times 960$): Active speaker.
  - Bottom Pane ($1080 \times 960$): Listening guest / reactor.
  - Seam: 4 px `#1E293B` at $y = 960$.
