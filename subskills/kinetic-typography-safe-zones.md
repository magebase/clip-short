# Subskill: Kinetic Typography Safe Zones & Visual Hierarchy

Autonomous typography placement, safe zone boundaries, collision avoidance, kinetic word animation, and vector emoji rendering for vertical short clips.

---

## 1. Safe Zone Coordinate Geometry

In a 54/46 Split-Screen composition ($1080 \times 1920$), typography must reside strictly in the **Speaker Safe Zone** over the speaker's torso, with guaranteed zero collision with interface dividers or supporting desktop cards.

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
2. **Maximum Safe Baseline**: $y \le 1030\text{px}$. Any text rendering at $y > 1030\text{px}$ is an instant rejection flag (`COLLISION_DIVIDER`).
3. **Clearance to Supporting Content**: The top of the active supporting content begins at $y \ge 1180\text{px}$, providing $\ge 180\text{px}$ of clean, unoccluded breathing room.
4. **Horizontal Margins**: Minimum $40\text{px}$ left and right clearance ($x \in [40, 1040]$).

---

## 2. Kinetic Typography Formatting Laws

### 1. 3–5 Word Semantic Chunks (Zero Staccato Flashes)
- **Forbidden**: Single-word or two-word rapid flashing cues ($< 250\text{ms}$ duration). This causes cognitive fatigue.
- **Enforced**: Natural syntactic phrase groups (3 to 5 words, e.g., `"The entire backend was"`, `"completely rewritten in Rust"`).
- **Contractions Preserved**: Never break apart contractions (`don't`, `can't`, `it's`).

### 2. Single-Line Buffer Deduplication
- Consecutive cues must never duplicate words or overlap.
- Subtitle cues must render as single-line or tight two-line blocks with centered alignment.

### 3. Kinetic Animation Grammar
- **Level 1 (Narrative Text)**: Clean white sans-serif (`Montserrat-Black` or `Inter-Bold`), 48–54px font size, 3px solid black stroke (`#000000`), subtle drop shadow (`#000000@0.65`).
- **Level 2 (Emphasis Words)**: Dynamically highlighted in high-contrast neon accents based on channel branding:
  - Electric Yellow: `#FACC15`
  - Neon Cyan: `#06B6D4`
  - Emerald Green: `#10B981`
  - Amber Gold: `#F59E0B`
  - Punch scale: $115\%$ spring pop on emphasized word onset.
- **Level 3 (Vector Emojis)**: Rendered inline adjacent to emotion/tech keywords (e.g., 🚀, 💻, 🔥, 💀, ⚡).

---

## 3. Top Safe-Zone Curiosity Hook Pill Badge

At the video cold open ($0.0\text{s}$), viewers make a swipe-away decision within $1.2\text{s}$. A prominent Curiosity Hook Pill badge reinforces the verbal thesis:

- **Position**: Centered horizontally at $y = 135\text{px}$.
- **Typography**: `Anton-Regular.ttf`, 32px font size, Title Case, white text with 2px black outline.
- **Container**: Translucent dark slate pill (`#0F172A@0.92`), padding 24px horizontal, 12px vertical.
- **Animation Life Cycle**:
  - $0.0\text{s} - 3.0\text{s}$: Fully opaque ($100\%$).
  - $3.0\text{s} - 3.8\text{s}$: Linear fade-out to $0\%$ opacity via FFmpeg alpha interpolation.
  - $> 3.8\text{s}$: Disappears completely, leaving the frame 100% clean for speaker facial expressions.
