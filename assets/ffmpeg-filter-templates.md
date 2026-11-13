# Production FFmpeg FilterComplex Templates

Deterministic, battle-tested FFmpeg filter graphs for vertical short rendering, 54/46 mobile split-screen compositing, 5-phase animated camera punch-ins, kinetic typography overlay, and broadcast audio mastering.

---

## 1. Golden 54/46 Split-Screen with Divider Seam
Constructs a $1080 \times 1920$ canvas with top speaker ($1080 \times 1040$) and bottom supporting card ($1080 \times 880$) separated by a 4px dark slate line at $y = 1038$.

```bash
ffmpeg -y \
  -ss {START_SEC} -to {END_SEC} -i "{INPUT_VIDEO}" \
  -filter_complex "
    [0:v]crop={CAM_W}:{CAM_H}:{CAM_X}:{CAM_Y},scale=1080:1040:flags=lanczos[top_speaker];
    [0:v]crop={CARD_W}:{CARD_H}:{CARD_X}:{CARD_Y},scale=1000:-1:flags=lanczos[scaled_card];
    color=c=#0B0F17:s=1080x880[bottom_bg];
    [bottom_bg][scaled_card]overlay=(W-w)/2:(H-h)/2[bottom_pane];
    color=c=#0B0F17:s=1080x1920[canvas];
    [canvas][top_speaker]overlay=0:0[canvas_top];
    [canvas_top][bottom_pane]overlay=0:1040[canvas_split];
    color=c=#1E293B:s=1080x4[seam];
    [canvas_split][seam]overlay=0:1038[v_out]
  " \
  -map "[v_out]" -map 0:a \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "{OUTPUT_MP4}"
```

---

## 2. Motivated Camera Progression (Semantic Beats Preferred)

Visual focus should change on semantic beats. Use the timestamp version below only as a fallback when beat detection is unavailable. Never let an arbitrary phase boundary cut a sentence or hide the speaker who is delivering the point.

Fallback 5-phase progression:
- **Phase 1 (0.0s – 3.2s)**: $112\%$ punch-in on Speaker.
- **Phase 2 (3.2s – 9.0s)**: Standard Golden Split ($100\%$).
- **Phase 3 (9.0s – 14.5s)**: $108\%$ punch-in on Supporting Card.
- **Phase 4 (14.5s – 18.0s)**: Standard Golden Split ($100\%$).
- **Phase 5 (18.0s – End)**: $110\%$ punch-in on Speaker for Punchline Delivery.

```bash
# Speaker Zoom Expression (top pane):
# If t <= 3.2: 1.12x; if t >= 18.0: 1.10x; else 1.00x
scale='if(lte(t,3.2), 1.12*iw, if(gte(t,18.0), 1.10*iw, iw))':-1:eval=frame

# Supporting Card Zoom Expression (bottom pane):
# If 9.0 <= t <= 14.5: 1.08x; else 1.00x
scale='if(between(t,9.0,14.5), 1.08*iw, iw)':-1:eval=frame
```

---

## 3. Dark Ambient Ultrawide Background Fallback
When supporting visual is ultrawide ($> 16:9$), fill negative space with a heavily blurred, darkened version of the supporting content instead of stark empty black:

```bash
ffmpeg -y \
  -ss {START_SEC} -to {END_SEC} -i "{INPUT_VIDEO}" \
  -filter_complex "
    [0:v]crop={CAM_W}:{CAM_H}:{CAM_X}:{CAM_Y},scale=1080:1040:flags=lanczos[top_speaker];
    [0:v]crop={CARD_W}:{CARD_H}:{CARD_X}:{CARD_Y}[card_raw];
    [card_raw]scale=1080:880:flags=bicubic,boxblur=40:20,eq=brightness=-0.25[blurred_bg];
    [card_raw]scale=1000:-1:flags=lanczos[sharp_card];
    [blurred_bg][sharp_card]overlay=(W-w)/2:(H-h)/2[bottom_pane];
    color=c=#0B0F17:s=1080x1920[canvas];
    [canvas][top_speaker]overlay=0:0[canvas_top];
    [canvas_top][bottom_pane]overlay=0:1040[canvas_split];
    color=c=#1E293B:s=1080x4[seam];
    [canvas_split][seam]overlay=0:1038[v_out]
  " \
  -map "[v_out]" -map 0:a \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  "{OUTPUT_MP4}"
```

---

## 4. Top Safe-Zone Curiosity Hook Pill Badge
Generates the curiosity hook pill badge at $y = 135$ in bold condensed typography (`Anton.ttf`) with a translucent slate background container (`#0F172A@0.92`) and smooth fade-out at $3.0\text{s} - 3.8\text{s}$:

```bash
drawbox=x=(w-text_w-48)/2:y=135:w=text_w+48:h=64:color=#0F172A@0.92:t=fill:enable='lte(t,3.8)',
drawtext=fontfile='/fonts/Anton-Regular.ttf':text='{HOOK_HEADLINE}':fontcolor=white:fontsize=32:borderw=2:bordercolor=black:x=(w-text_w)/2:y=149:alpha='if(lte(t,3.0), 1, if(lte(t,3.8), (3.8-t)/0.8, 0))'
```

---

## 5. EBU R128 Loudness Normalization & Micro-Fade Filtering
Applies $35\text{ms}$ pre-speech audio fade-in to eliminate frame-0 clicks, $80\text{ms}$ terminal fade-out for clean acoustic decay, and two-pass EBU R128 integrated loudness normalization:

```bash
# Pass 1: Measure loudness parameters
ffmpeg -ss {START_SEC} -to {END_SEC} -i "{INPUT_VIDEO}" \
  -af "afade=t=in:ss=0:d=0.035,afade=t=out:st={FADE_OUT_START}:d=0.08,loudnorm=I=-14:TP=-1:LRA=7:print_format=json" \
  -f null -

# Pass 2: Apply linear normalization with measured parameters
ffmpeg -ss {START_SEC} -to {END_SEC} -i "{INPUT_VIDEO}" \
  -af "afade=t=in:ss=0:d=0.035,afade=t=out:st={FADE_OUT_START}:d=0.08,loudnorm=I=-14.0:TP=-1.0:LRA=7.0:measured_I={MEASURED_I}:measured_TP={MEASURED_TP}:measured_LRA={MEASURED_LRA}:measured_thresh={MEASURED_THRESH}:offset={OFFSET}:linear=true" \
  -c:a aac -b:a 192k \
  "{OUTPUT_AUDIO}"
```


---

## 6. Adaptive Layout Routing

Choose the graph from the source archetype and story beat; do not default to a split.

| Layout | Filter recipe |
| :--- | :--- |
| `FULLSCREEN_PORTRAIT` | `crop=...` face-aware window, `scale=1080:1920`, no split |
| `DYNAMIC_SPEAKER` | One full-frame source per shot; hard cuts at speaker turns |
| `ADAPTIVE_SPLIT` | Section 1 Golden 54/46 preset |
| `PIP` | Full-frame action + small facecam overlay in a clear corner |
| `PROGRESSIVE_DIAGRAM` | Section 7 diagram tracking |
| `SCENE_TRACKING` | Full-frame scene, slow pan/zoom, cuts on story beats |
| `MINIMAL_DOCUMENTARY` | Full-frame contextual footage, restrained motion |

### Full-Screen Face-Aware Crop
```bash
# Compute CROP_X/CROP_Y from face landmarks before building the graph.
# Keep eyes in the upper third and preserve headroom.
ffmpeg -y -ss {START_SEC} -to {END_SEC} -i "{INPUT_VIDEO}" \
  -filter_complex "
    [0:v]crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y},scale=1080:1920:flags=lanczos[v_out]
  " \
  -map "[v_out]" -map 0:a \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k "{OUTPUT_MP4}"
```

### Picture-in-Picture for Action + Facecam
```bash
ffmpeg -y -ss {START_SEC} -to {END_SEC} -i "{INPUT_VIDEO}" \
  -filter_complex "
    [0:v]crop={ACTION_W}:{ACTION_H}:{ACTION_X}:{ACTION_Y},scale=1080:1920:flags=lanczos[action];
    [0:v]crop={CAM_W}:{CAM_H}:{CAM_X}:{CAM_Y},scale=320:-1:flags=lanczos[cam];
    [action][cam]overlay=W-w-32:160[v_out]
  " \
  -map "[v_out]" -map 0:a \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k "{OUTPUT_MP4}"
```

---

## 7. Progressive Diagram Tracking

For panoramic architecture diagrams, do not permanently shrink the whole canvas into a pane. Split the diagram into semantic beats and track each referenced component.

1. Detect the diagram bounds and component boxes (interface, harness, LLM, tools).
2. Assign each component to the spoken beat that references it.
3. For each beat, crop a readable window around the component with padding.
4. Animate a slow pan between components within a beat; cut between beats.

```bash
# One beat: readable component crop with mild punch-in and horizontal drift.
# CROP_X(t) moves from START_X to END_X across the beat.
ffmpeg -y -ss {BEAT_START} -to {BEAT_END} -i "{INPUT_VIDEO}" \
  -filter_complex "
    [0:v]crop={COMP_W}:{COMP_H}:'{START_X}+({END_X}-{START_X})*min(t/{BEAT_DUR},1)':{COMP_Y},
         scale=1080:-1:flags=lanczos,
         crop=1080:1920:0:'max(0,(ih-1920)/2)'[v_out]
  " \
  -map "[v_out]" -map 0:a \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k "{OUTPUT_MP4}"
```

Readability gate before rendering:
- Primary labels $\ge 24	ext{px}$ at $1080$ width; secondary $\ge 18	ext{px}$.
- No arrow or label clipped at either horizontal edge.
- If a beat needs more width than the pane allows, use full-screen for that beat instead of shrinking further.

---

## 8. Debug Overlay and Cursor Prevention

### Debug Overlay Prevention
The Theo failure came from filter expressions or phase labels reaching the video. Enforce a strict boundary:

1. Render display text only from the verified transcript and metadata records.
2. Never interpolate source code, filter expressions, or internal variables into `drawtext`.
3. Reject any text containing `if(`, `tt(`, `{`, `}`, `None`, `null`, or an unresolved `{PLACEHOLDER}` before building the graph.
4. Escape `:`, `'`, `\`, and `%` in all drawtext strings; prefer generating an ASS subtitle file over inline `drawtext` for dynamic text.
5. Re-inspect the exported MP4 with OCR and a contact sheet; a debug string anywhere is `REJECTED_RENDER`.

```python
FORBIDDEN_TEXT = ("if(", "tt(", "{", "}", "None", "null", "REQUIRED")

def safe_overlay_text(value: str) -> str:
    if not value or any(tok in value for tok in FORBIDDEN_TEXT):
        raise ValueError(f"unsafe overlay text: {value!r}")
    return value.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
```

### Cursor Prevention
- Track the cursor path across the beat; if it sits inside the chosen crop for more than $0.5	ext{s}$, move the crop, punch into the component (cursor outside frame), or choose another beat.
- When editing screen recordings, prefer `crop` windows that exclude the cursor travel area.
- Never rely on a downstream blur to hide a cursor; verify in the exported MP4.
- If cursor-free framing would destroy the content, fail closed to `HUMAN_REVIEW`.
