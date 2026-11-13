# Subskill: PiP Split-Screen Geometry & Saliency Router

Autonomous spatial extraction, framing math, face detection, and active supporting content isolation for vertical $9:16$ short videos.

---

## 1. Golden 54/46 Split-Screen Blueprint

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

---

## 2. MediaPipe BlazeFace Speaker Tracking & Headroom Math
The camera crop for the speaker webcam must adapt dynamically to head movements without jitter:

### Bounding Box Calculations
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

### Edge Clutter Exclusion
To prevent browser tabs, red notification badges, or scrollbars from leaking into the speaker pane:
$$\text{min\_safe\_y} = \max\left(\text{int}(H_{\text{frame}} \times 0.055), 60\right)$$
$$\text{max\_safe\_x} = W_{\text{frame}} - \text{crop\_w} - 25$$

---

## 3. OpenCV Saliency & Primary Card Isolation
To extract the active supporting code, tweet, or architecture diagram from the desktop capture without showing OS taskbars or chat streams:

### Processing Algorithm
1. **Mask Speaker Region**: Black out the coordinates of the detected facecam overlay box.
2. **Exclude Chat Panels & Taskbars**: Chat panels are typically fixed columns ($x < 0.08 W_{\text{frame}}$ or $x > 0.85 W_{\text{frame}}$) and OS taskbars live at $y > 0.95 H_{\text{frame}}$. Mask these zones.
3. **Motion Energy & Sobel Gradient Density**:
   - Compute gradient magnitude $G = \sqrt{G_x^2 + G_y^2}$ using Sobel filters ($3 \times 3$).
   - Apply morphological closing with horizontal kernel ($25 \times 5$) to bridge code lines or sentences into cohesive text blocks.
4. **Primary Contour Extraction**:
   - Find external contours with area $A_{\text{contour}} \ge 0.15 \times (W_{\text{frame}} \times H_{\text{frame}})$.
   - Filter out contours where aspect ratio $W/H > 4.0$ (banner ads or status bars).
5. **Enclosure Verification**:
   - Ensure primary diagram or terminal block is enclosed with $\ge 40\text{px}$ padding.
   - Scale clamped width to $1000\text{px}$ inside the $1080\text{px}$ canvas ($40\text{px}$ gutter on each side).

---

## 4. Visual QA Gate (`VisualQAGate`)
Before rendering, verify candidate crops against automated visual rules:
- **No Floating UI Fragments**: Any crop contour with height $< 120\text{px}$ or area $< 5\%$ is rejected.
- **Dedicated Chat Column Check**: If chat box is selected instead of main content, reject.
- **Complete Diagram Enclosure**: Ensure bounding box includes all high-density edge clusters. If check fails, fall back to clean centered desktop crop.
