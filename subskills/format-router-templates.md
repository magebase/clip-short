# Subskill: FormatRouter & The 6 Mega-Viral Template Complexes

Autonomous classification of stream segments and dynamic filter-complex generation for the 6 highest-converting Short formats.

---

## 1. The 6 Benchmark Short Formats

| Format Identifier | Benchmark Creator & Views | Genre & Mechanics | Dominant Visual Filter Complex |
| :--- | :--- | :--- | :--- |
| `FORMAT_1_PHONK_FREEZE` | **IShowSpeed** (53.3M views) | IRL Stunt / Climax + Phonk Freeze-Frame + Zoom Shake | Freezes frame on peak impact, drops color saturation, punches in 125%, plays Brazilian Phonk bass boost |
| `FORMAT_2_REACTION_STACK` | **CaseOh** (18.8M views) | 50/50 Top/Bottom Reaction Stack with Seam Captions | Top pane reactor ($1080 \times 960$), Bottom pane desktop clip ($1080 \times 960$), centered seam subtitles |
| `FORMAT_3_ACTION_TAG_SITCOM` | **IShowSpeed** (23.8M views) | Non-Verbal Action-Tag Sitcom Edit (*TAGS*) | Detects physical comedic gestures; renders neon italic action tags (`*STARES DISRESPECTFULLY*`, `*REALIZES*`) |
| `FORMAT_4_DISCORD_BROLL` | **xQc & Jynxzi** (7.3M views) | Voice Rant + Satisfying High-Engagement B-Roll | Renders speaker voice over dynamic satisfying gameplay (GTA ramps, Minecraft parkour, soap cutting) |
| `FORMAT_5_WHITEBOARD_EXPLAINER` | **PirateSoftware & Theo** (13.2M views) | High-Retention Code / Architecture / Mindset Monologue | Golden 54/46 Split, OpenCV diagram saliency, 5-phase motivated zoom progression, white hook card badge |
| `FORMAT_N3ON_PING_PONG` | **N3ON & Clavicular** (1.2M+ views) | Two-Speaker Sitcom IRL Ping-Pong Edit | Neural YuNet / BlazeFace tracking of 2 subjects in wide lens; rapid alternating cuts on speech turn |

---

## 2. Classification Engine (`classify_segment`)

The router analyzes video, audio, and transcript features to determine the optimal format:

```python
def classify_segment(
    words: List[dict],
    duration_sec: float,
    face_boxes: Optional[List[tuple]] = None,
    content_type: str = "general",
    audio_rms_peaks: Optional[List[float]] = None,
    broll_path: Optional[str] = None
) -> str:
    duration = max(1.0, float(duration_sec))
    wps = len(words) / duration
    boxes = face_boxes or []
    rms = audio_rms_peaks or []

    # 1. Corner Facecam Detection
    corner_faces = [
        f for f in boxes
        if (f[0] < 0.28 or f[0] > 0.72) and (f[1] < 0.30 or f[1] > 0.70) and f[2] < 0.24
    ]
    is_corner_facecam = len(boxes) > 0 and (len(corner_faces) / len(boxes)) >= 0.55

    # 2. Audio Tail Spike (Scream, crash, or impact in final 4s)
    median_rms = float(np.median(rms)) if rms else -30.0
    tail_rms = rms[-8:] if len(rms) >= 8 else rms
    tail_spike = (max(tail_rms) - median_rms) if tail_rms else 0.0

    # Rules
    if content_type in ("tutorial", "educational", "coding", "finance", "explainer") and is_corner_facecam:
        return "FORMAT_5_WHITEBOARD_EXPLAINER"

    if is_corner_facecam:
        return "FORMAT_2_REACTION_STACK"

    if tail_spike >= 14.0 and duration <= 22.0:
        return "FORMAT_1_PHONK_FREEZE"

    if wps < 0.80 and duration >= 25.0:
        return "FORMAT_3_ACTION_TAG_SITCOM"

    if broll_path and Path(broll_path).exists():
        return "FORMAT_4_DISCORD_BROLL"

    return "FORMAT_5_WHITEBOARD_EXPLAINER"
```

---

## 3. Top White Headline Pill Component (`build_modern_headline_pill`)

The modern viral card badge renders at safe zone $y = 135$:
- **Dimensions**: Adaptive width (420px to 860px), fixed height 76px.
- **Typography**: Anton Regular, 40pt bold, Title Case, pure black text (`#000000`).
- **Container**: Solid white card (`#FFFFFF`) with a subtle 2px dark border (`#000000@0.22`) and 12px rounded corners.
- **Lifecycle**: Smooth fade-out between 3.0s and 3.8s (`alpha='if(lte(t,3.0), 1, if(lte(t,3.8), (3.8-t)/0.8, 0))'`).

```bash
# Example FFmpeg overlay filter:
drawbox=x={PX}:y=135:w={DYNAMIC_W}:h=76:color=white@1.0:t=fill:enable='lte(t,3.8)',
drawbox=x={PX}:y=135:w={DYNAMIC_W}:h=76:color=black@0.22:t=2:enable='lte(t,3.8)',
drawtext=fontfile='Anton-Regular.ttf':text='{HEADLINE}':fontcolor=black:fontsize=40:x=(w-text_w)/2:y=153:alpha='if(lte(t,3.0), 1, if(lte(t,3.8), (3.8-t)/0.8, 0))'
```
