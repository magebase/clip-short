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

## 2. 5-Phase Motivated Camera Progression
Dynamically alternates focus between dominant speaker, standard split, and supporting card across 5 phases:
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
