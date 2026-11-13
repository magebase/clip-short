# Subskill: Adaptive Layout Engine, Speaker Framing & Saliency

Spatial decision layer for vertical $9:16$ composition. Selects a layout from the source format, frames the subject, isolates supporting content, and tracks diagrams across semantic beats.

The Golden 54/46 split is a proven preset for corner-facecam streamer footage. It is not a universal template.

---

## 1. Layout Decision Matrix

| Source content | `layout_mode` | Composition |
| :--- | :--- | :--- |
| Portrait speaker / talking head | `FULLSCREEN_PORTRAIT` | Single $1080 \times 1920$ face-aware crop |
| Landscape podcast, one speaker at a time | `DYNAMIC_SPEAKER` | Full-screen crop with cuts on speaker changes |
| Two speakers, alternating | `DYNAMIC_SPEAKER` | Cut to the active speaker; $\ge 1.8\text{s}$ dwell |
| Corner facecam + desktop | `ADAPTIVE_SPLIT` / `PIP_SPLIT` | 54/46 split or picture-in-picture |
| Screen recording, one active window | `ACTIVE_WINDOW` | Crop to active window, zoom to content |
| Wide architecture diagram | `PROGRESSIVE_DIAGRAM` | Horizontal tracking plus component zoom across beats |
| Whiteboard / hand-drawn diagram | `PROGRESSIVE_DIAGRAM` | Follow drawing order, hold on completed regions |
| Slide presentation | `SLIDE_ISOLATION` | Isolate slide; speaker inset only when it adds meaning |
| Illustrated animation | `SCENE_TRACKING` | Full-screen scene crop with motivated pans |
| Narrated documentary / B-roll | `FULLSCREEN_CONTEXT` | Full-screen contextual visuals |
| Gaming + facecam | `ACTION_SAFE` | Action-aware crop plus facecam inset |
| Full-screen gaming | `FULLSCREEN_ACTION` | Crop to action centroid with motion padding |
| Sports / action | `FULLSCREEN_ACTION` | Track play; never crop the ball/athlete out |
| Live performance | `FULLSCREEN_STAGE` | Stage framing with beat-matched cuts |
| Product demonstration | `OBJECT_FOCUS` | Crop to hands/product/result |
| Dual-speaker debate | `SPEAKER_SWITCH` | Cut on turn changes; hold on the speaker making the point |

**Hard rule:** if the layout requires shrinking the primary content below mobile readability, change the layout. Never force the source into the preset.

---

## 2. Golden 54/46 Preset Blueprint

```
+------------------------------------------------------+ y = 0
|                                                      |
|                 TOP SPEAKER PANE                     |
|                 1080 x 1040 px                       |
|               (54.17% Total Canvas)                  |
|                                                      |
|     * Head-and-Shoulders aspect-locked crop          |
|     * Target padding: 2.45 x fh                      |
|     * Headroom offset: +0.32 x fh                    |
|                                                      |
|    [ Kinetic Typography Safe Zone: MarginV = 920 ]   |
|         Baseline: y = 1000 over speaker torso        |
+------------------------------------------------------+ y = 1038
|================= 4px Slate Seam =====================| (#1E293B)
+------------------------------------------------------+ y = 1042
|                                                      |
|            BOTTOM SUPPORTING CONTENT PANE            |
|                 1080 x 880 px                        |
|               (45.83% Total Canvas)                  |
|                                                      |
|     * Primary Saliency Box (Code/Tweet/Diagram)      |
|     * Horizontal width clamped to 1000 px            |
|     * Side margins: 40 px left / 40 px right         |
|     * Clearance: Subtitles to content > 180 px       |
|                                                      |
+------------------------------------------------------+ y = 1920
```

Use this preset only when the source has a corner facecam and a supporting visual that is readable at this scale. Otherwise route to another layout.

---

## 3. MediaPipe BlazeFace Speaker Tracking & Headroom Math

Given detected face box $[x_1, y_1, x_2, y_2]$:
$$f_w = x_2 - x_1, \quad f_h = y_2 - y_1$$
$$c_x = x_1 + \frac{f_w}{2}, \quad c_y = y_1 + \frac{f_h}{2}$$

Target pane aspect ratio:
$$A_{top} = \frac{1080}{1040} \approx 1.0385$$

Crop dimensions:
$$\text{crop\_h} = 2.45 \times f_h$$
$$\text{crop\_w} = \text{crop\_h} \times A_{top} \approx 2.544 \times f_h$$

Headroom shift ($+0.32 \times f_h$ downward shift to leave natural breathing space above the crown):
$$\text{cam\_x} = \text{clamp}\left(c_x - \frac{\text{crop\_w}}{2}, 0, W_{\text{frame}} - \text{crop\_w}\right)$$
$$\text{cam\_y} = \text{clamp}\left(c_y - \frac{\text{crop\_h}}{2} - 0.32 \times f_h, 0, H_{\text{frame}} - \text{crop\_h}\right)$$

For full-screen portrait layouts, compute the same body-framing box directly on the $1080 \times 1920$ canvas. For speaker-switch layouts, use exponential smoothing:
$$c_x^{(t)} = \alpha c_x^{(t)} + (1 - \alpha) c_x^{(t-1)}, \quad \alpha = 0.15$$
but snap hard on a scene cut.

### Edge Clutter Exclusion
To prevent browser tabs, red notification badges, or scrollbars from leaking into the speaker pane:
$$\text{min\_safe\_y} = \max\left(\text{int}(H_{\text{frame}} \times 0.055), 60\right)$$
$$\text{max\_safe\_x} = W_{\text{frame}} - \text{crop\_w} - 25$$

---

## 4. OpenCV Saliency & Primary Card Isolation

1. **Mask Speaker Region**: black out the detected facecam overlay box.
2. **Exclude Chat Panels & Taskbars**: chat panels are typically fixed columns ($x < 0.08 W_{\text{frame}}$ or $x > 0.85 W_{\text{frame}}$) and OS taskbars live at $y > 0.95 H_{\text{frame}}$. Mask these zones.
3. **Motion Energy & Sobel Gradient Density**:
   - Compute gradient magnitude $G = \sqrt{G_x^2 + G_y^2}$ using Sobel filters ($3 \times 3$).
   - Apply morphological closing with horizontal kernel ($25 \times 5$) to bridge code lines or sentences into cohesive text blocks.
4. **Primary Contour Extraction**:
   - Find external contours with area $A_{\text{contour}} \ge 0.15 \times (W_{\text{frame}} \times H_{\text{frame}})$.
   - Filter out contours where aspect ratio $W/H > 4.0$ (banner ads or status bars).
5. **Enclosure Verification**:
   - Ensure the primary diagram or terminal block is enclosed with $\ge 40\text{px}$ padding.
   - Scale clamped width to $1000\text{px}$ inside the $1080\text{px}$ canvas ($40\text{px}$ gutter on each side).

---

## 5. Progressive Diagram Tracking (`PROGRESSIVE_DIAGRAM`)

When content is wider than the pane, do not shrink the entire diagram. Track it across semantic beats.

### Beat Extraction
1. Detect the diagram bounding box.
2. Compute column-wise edge density to find distinct components (boxes, labels, arrows).
3. Cluster components into 2–4 beats based on spoken references and left-to-right/top-to-bottom reading order.
4. Assign each beat a time window from the transcript. Hold each shot until the speaker moves to the next referenced component.
5. Pan between component centers with a short $150\text{–}250\text{ms}$ eased move, or hard-cut when the beat changes.

### Framing Rule
For a component of width $w_c$:
$$\text{zoom}_c = \min\left(1.35, \frac{1080 - 2 \times 40}{w_c}\right)$$
Keep the component plus its label and its incoming/outgoing arrows in frame. Never crop the connection that explains the mechanism.

### Example: Theo Technical Explainer
| Beat | Spoken focus | Visual |
| :--- | :--- | :--- |
| 1 | Human interface / kitchen analogy | Speaker full-screen or top pane |
| 2 | Harness as communication layer | Zoom on interface + harness nodes |
| 3 | Special syntax | Zoom on the syntax node and its connections |
| 4 | Tool execution | Zoom on the final execution node |

This replaces permanent display of the entire diagram at unreadable scale.

---

## 6. Cursor and Debug-Overlay Avoidance

- Track cursor position across the selected beat. If it sits inside the crop for more than $0.5\text{s}$, choose a different crop or beat.
- Exclude the region under a persistent cursor from the sharp card crop when possible.
- Never render phase labels, conditional expressions, or tracking boxes into the frame. Text overlays come only from validated metadata fields.
- OCR a dry-run frame before the full render; abort the render on any debug-like token.

---

## 7. Visual QA Gate (`VisualQAGate`)

Before rendering, verify candidate crops against automated visual rules:
- **No Floating UI Fragments**: Any crop contour with height $< 120\text{px}$ or area $< 5\%$ is rejected.
- **Dedicated Chat Column Check**: If a chat box is selected instead of main content, reject.
- **Complete Diagram Enclosure**: Ensure the bounding box includes all high-density edge clusters. If the check fails, fall back to a clean centered desktop crop or `HUMAN_REVIEW`.
- **Mobile Readability**: Primary labels must render at $\ge 24\text{px}$ and secondary labels at $\ge 18\text{px}$ in the final $1080$-wide canvas.
- **Source-Text Collision**: Captions must not overlap detected source text regions.
- **Face Occlusion**: Text must not intersect the eye or mouth region of the speaker.
- **Cursor Free**: No visible cursor in the supporting pane for the selected beat.
- **Campaign Aspect**: Output is exactly $1080 \times 1920$ with square pixels unless the campaign specifies otherwise.
