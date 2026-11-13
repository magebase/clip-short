# clip-short

> **Autonomous AI Short Clipper & Split-Screen Viral Video Production Skill for Agent CLIs (`agy`, `claude`, `codex`, `cursor`, `copilot`, `openhands`)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-magebase%2Fclip--short-181717.svg?logo=github)](https://github.com/magebase/clip-short)
[![Antigravity CLI](https://img.shields.io/badge/Antigravity%20CLI-Compatible-indigo.svg)](https://github.com/magebase/clip-short)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-orange.svg)](https://github.com/magebase/clip-short)
[![FFmpeg](https://img.shields.io/badge/Engine-FFmpeg%20%7C%20OpenCV%20%7C%20Whisper-green.svg)](assets/ffmpeg-filter-templates.md)

---

## 1. Overview

`clip-short` is an agent-native video engineering skill that enables AI developer agents to autonomously discover, trim, compose, package, and publish high-retention viral vertical short videos ($9:16$ for YouTube Shorts, TikTok, Instagram Reels) from multi-hour desktop livestreams, podcasts, keynotes, and coding broadcasts.

Unlike basic automated re-framing tools that naively stretch or center-crop landscape video, `clip-short` enforces strict **Golden 54/46 Split-Screen Mobile Geometry**, dynamic **MediaPipe BlazeFace speaker framing**, **OpenCV saliency edge-detection** to isolate active code/browser cards, **Whisper word-level linguistic snapping** (complete sentence cold opens, terminal punchline decay), **kinetic typography safe zones**, and **100% faithful transcript-driven packaging**.

---

## 2. Core Capabilities

### 1. Golden 54/46 Split-Screen Mobile Architecture ([`subskills/pip-split-screen-geometry.md`](subskills/pip-split-screen-geometry.md))
- **Top Dominant Speaker Pane ($1080 \times 1040$ / $54.17\%$)**: Aspect-locked $2.45 \times fh$ head-and-shoulders crop with $+0.32 \times fh$ natural headroom offset. Zero forehead or chin cutoffs.
- **Bottom Supporting Card Pane ($1080 \times 880$ / $45.83\%$)**: OpenCV Sobel edge-density contour extraction isolating primary tweets, terminal code, or architecture diagrams, scaled to 1000px with 40px side margins. Ultrawide inputs receive a dark blurred ambient canvas fallback.
- **Seam Separation**: 4px slate seam (`#1E293B`) at $y = 1038$ px.
- **5-Phase Motivated Progression**: $112\%$ speaker hook zoom $\to$ neutral split $\to$ $108\%$ supporting card zoom $\to$ neutral split $\to$ $110\%$ punchline zoom.

### 2. Linguistic Narrative & Acoustic Decay Snapping ([`subskills/linguistic-boundary-snapping.md`](subskills/linguistic-boundary-snapping.md))
- **Runtime Target**: Strictly $18.0\text{s} - 22.5\text{s}$ (max $23.5\text{s}$).
- **Cold Open**: Starts strictly at the beginning of a complete sentence or question. Eliminates conversational fillers (`um`, `uh`, `like`), adds $60 - 80\text{ms}$ room tone, and applies a $35\text{ms}$ audio micro fade-in (`afade=t=in:d=0.035`).
- **Terminal Snapping**: Cut points snap strictly to terminal punctuation (`.`, `!`, `?`). Adds $120 - 180\text{ms}$ acoustic decay padding with an $80\text{ms}$ audio micro fade-out (`afade=t=out:d=0.08`).

### 3. Kinetic Typography Safe Zones (`MarginV = 920`) ([`subskills/kinetic-typography-safe-zones.md`](subskills/kinetic-typography-safe-zones.md))
- Subtitle baseline locked at $y = 1000$ (`MarginV = 920`) over the speaker's torso.
- Over $180\text{px}$ clearance above supporting content ($y \ge 1180$) and divider ($y = 1038$) for guaranteed **0.0px collision**.
- 3 to 5 words per semantic chunk (no rapid 1-2 word staccato flashes), single-line buffer deduplication, neon accent word pops, and vector emojis.
- Top Curiosity Hook Pill badge at $y = 135$ (`Anton-Regular.ttf`, 2px outline, translucent pill container `#0F172A@0.92`), fading out smoothly at $3.0\text{s} - 3.8\text{s}$.

### 4. 100% Faithful Transcript Packaging ([`subskills/faithful-metadata-packaging.md`](subskills/faithful-metadata-packaging.md))
- Direct transcript grounding via LLM / deterministic NLP: Top HUD headline (3–6 words Title Case, max 38 chars, 0 trailing punctuation) and YouTube title derived strictly from literal spoken words.
- Curiosity-Gap Redundancy Gate: If headline lexical overlap with opening audio exceeds 65%, automatically reformulates into a curiosity thesis question.

### 5. Pre-Render & Post-Render Quality Defense ([`subskills/pre-render-quality-gates.md`](subskills/pre-render-quality-gates.md))
- Multi-Frame Pixel Sharpness: Laplacian variance $\sigma_L^2 \ge 65.0$. Muddy or upscaled 1080p crops fail-closed.
- Burnt-In Subtitle Gate: Scans subtitle band ($0.52 \le y \le 0.88$) for pre-existing hardcoded captions.
- Audio Loudness: EBU R128 integrated loudness normalized to $-14.0\text{ LUFS}$ ($\le -1.0\text{ dBTP}$).
- 100-Point Viral Rubric: Automated scoring across Hook, Coherence, Linguistic Boundaries, Mobile Framing, Captions, Audio, and Info Density.

### 6. Universal Staged Private Release ([`subskills/fleet-staged-publishing.md`](subskills/fleet-staged-publishing.md))
- Direct public uploads strictly forbidden. Uploads set `status.privacyStatus = "private"` with an explicit future `publishAt` timestamp.
- Minimum 2.5-hour (150-minute) transcode buffer for Content ID scans and VP9/AV1 processing.
- 3-Pod GCP architecture with an 85-upload daily safety headroom gate.

---

## 3. Installation Across All Agent CLIs

### Automatic One-Line Install
Run the included installation script:
```bash
git clone https://github.com/magebase/clip-short.git /home/aqua/skills/clip-short
cd /home/aqua/skills/clip-short
bash install.sh
```

### Supported Agent CLI Platforms
The installer automatically symlinks `clip-short` into every detected agent configuration:
- **Antigravity CLI (`agy`)**: `~/.gemini/antigravity-cli/skills/clip-short` & `~/.gemini/config/skills/clip-short`
- **Claude Code**: `~/.claude/skills/clip-short`
- **Universal Agent (`.agents`)**: `~/.agents/skills/clip-short`
- **Cursor IDE**: `~/.cursor/skills/clip-short`
- **OpenAI Codex**: `~/.codex/skills/clip-short`
- **GitHub Copilot**: `~/.copilot/skills/clip-short`
- **Factory Droid**: `~/.factory/skills/clip-short`
- **Windsurf / Codeium**: `~/.codeium/windsurf/skills/clip-short`
- **OpenHands**: `~/.openhands/skills/clip-short`
- **Devin CLI**: `~/.config/devin/skills/clip-short`
- **OpenCode**: `~/.config/opencode/skills/clip-short`
- **Goose CLI**: `~/.goose/skills/clip-short`
- **Continue.dev**: `~/.continue/skills/clip-short`

---

## 4. Usage Workflow Example

```python
# 1. Detect VOD layout & extract speaker + active card coordinates
from clip_short.pip_layout_router import PiPLayoutRouter
router = PiPLayoutRouter()
mode, face_box = router.detect_layout_mode(face_boxes, frame_w=1920, frame_h=1080)
cam_crop = router.get_facecam_crop(face_box, frame_w=1920, frame_h=1080, target_aspect=1080/1040)
card_crop, is_wide = router.find_active_screen_region("master_vod.mp4", start_sec=42.0, duration=20.0, cam_crop=cam_crop)

# 2. Build FFmpeg filter complex & render split
filter_str, inputs = router.build_pip_split_filtercomplex(
    cam_crop=cam_crop, card_crop=card_crop, is_wide=is_wide
)

# 3. Evaluate pre-render quality gate
from clip_short.quality_gate import ClipQualityGate
gate = ClipQualityGate()
assert gate.check_sharpness("master_vod.mp4") >= 65.0
assert not gate.detect_burnt_subtitles("master_vod.mp4")
```

---

## 5. License

MIT License. Copyright (c) 2026 Magebase.
