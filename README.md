# clip-short

> **Autonomous AI Short Clipper & Split-Screen Viral Video Production Skill for Agent CLIs (`agy`, `claude`, `codex`, `cursor`, `copilot`, `openhands`)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-magebase%2Fclip--short-181717.svg?logo=github)](https://github.com/magebase/clip-short)
[![Antigravity CLI](https://img.shields.io/badge/Antigravity%20CLI-Compatible-indigo.svg)](https://github.com/magebase/clip-short)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-orange.svg)](https://github.com/magebase/clip-short)
[![FFmpeg](https://img.shields.io/badge/Engine-FFmpeg%20%7C%20OpenCV%20%7C%20Whisper-green.svg)](assets/ffmpeg-filter-templates.md)
[![Daemon](https://img.shields.io/badge/Production-10m%20Autonomous%20Cadence-emerald.svg)](subskills/autonomous-10m-cadence-daemon.md)

---

## 1. Overview

`clip-short` is an agent-native video engineering skill designed to autonomously discover, score, cut, compose, package, and publish high-retention viral vertical short videos ($9:16$ for YouTube Shorts, TikTok, Instagram Reels, Facebook Reels) from multi-hour desktop livestreams, podcasts, keynotes, and coding broadcasts.

Unlike basic re-framing scripts, `clip-short` mirrors the production-tested ClipFactory architecture:
1. **The 6 Mega-Viral Format Templates** (`FormatRouter`) modeling IShowSpeed, CaseOh, PirateSoftware, Theo, and N3ON.
2. **Golden 54/46 Split-Screen Mobile Geometry** with dynamic MediaPipe BlazeFace speaker framing and OpenCV primary card saliency.
3. **Linguistic Boundary & Acoustic Snapping** with Whisper word-level timestamps (complete sentence cold opens, terminal punchline decay).
4. **Kinetic Spring Bounce Captions (`\fscx124`)** with vector emojis (`\fnSymbola`) and top white headline cards.
5. **Continuous 10-Minute Cadence Engine** with Expected Value ($EV$) candidate ranking, Cloudflare R2 CDN ingestion, and multi-platform fleet distribution.
6. **Automated View-Gated Bounty Claims** into business bank accounts and tax accounting.

---

## 2. Core Capabilities

### 1. The 6 Mega-Viral Format Templates ([`subskills/format-router-templates.md`](subskills/format-router-templates.md))
- `FORMAT_1_PHONK_FREEZE`: IRL Physical Stunt + Phonk Freeze-Frame + Camera Shake (IShowSpeed 53.3M benchmark).
- `FORMAT_2_REACTION_STACK`: 50/50 Top/Bottom Reaction Stack with Seam Captions (CaseOh 18.8M benchmark).
- `FORMAT_3_ACTION_TAG_SITCOM`: Non-Verbal Action-Tag Sitcom Edit with Neon *TAGS* (IShowSpeed 23.8M benchmark).
- `FORMAT_4_DISCORD_BROLL`: Discord Voice Rant + Satisfying High-Engagement B-Roll (xQc & Jynxzi 7.3M benchmark).
- `FORMAT_5_WHITEBOARD_EXPLAINER`: High-Retention Code / Architecture Monologue (PirateSoftware & Theo 13.2M benchmark).
- `FORMAT_N3ON_PING_PONG`: IRL Two-Speaker Sitcom Ping-Pong Edit with Neural YuNet tracking (N3ON & Clavicular 1.2M+ benchmark).

### 2. Golden 54/46 Split-Screen Mobile Architecture ([`subskills/pip-split-screen-geometry.md`](subskills/pip-split-screen-geometry.md))
- **Top Dominant Speaker Pane ($1080 \times 1040$ / $54.17\%$)**: Aspect-locked $2.45 \times fh$ head-and-shoulders crop with $+0.32 \times fh$ natural headroom offset. Zero forehead or chin cutoffs.
- **Bottom Supporting Card Pane ($1080 \times 880$ / $45.83\%$)**: OpenCV Sobel edge-density contour extraction isolating primary tweets, terminal code, or architecture diagrams, scaled to 1000px with 40px side margins. Ultrawide inputs receive a dark blurred ambient canvas fallback.
- **Seam Separation**: 4px slate seam (`#1E293B`) at $y = 1038$ px.
- **5-Phase Motivated Progression**: $112\%$ speaker hook zoom $\to$ neutral split $\to$ $108\%$ supporting card zoom $\to$ neutral split $\to$ $110\%$ punchline zoom.

### 3. Linguistic Narrative & Acoustic Decay Snapping ([`subskills/linguistic-boundary-snapping.md`](subskills/linguistic-boundary-snapping.md))
- **Runtime Target**: Strictly $18.0\text{s} - 22.5\text{s}$ (max $23.5\text{s}$).
- **Cold Open**: Starts strictly at the beginning of a complete sentence or question. Eliminates conversational fillers (`um`, `uh`, `like`), adds $60 - 80\text{ms}$ room tone, and applies a $35\text{ms}$ audio micro fade-in (`afade=t=in:d=0.035`).
- **Terminal Snapping**: Cut points snap strictly to terminal punctuation (`.`, `!`, `?`). Adds $120 - 180\text{ms}$ acoustic decay padding with an $80\text{ms}$ audio micro fade-out (`afade=t=out:d=0.08`).

### 4. Kinetic Typography Safe Zones & Vector Emojis ([`subskills/kinetic-typography-safe-zones.md`](subskills/kinetic-typography-safe-zones.md))
- Subtitle baseline locked at $y = 1000$ (`MarginV = 920`) over the speaker's torso.
- Over $180\text{px}$ clearance above supporting content ($y \ge 1180$) and divider ($y = 1038$) for guaranteed **0.0px collision**.
- 3 to 5 words per semantic chunk, spring pop animation (`\fscx124\fscy124\t(0,75,\fscx108\fscy108)`), multi-tier neon palettes, and vector emojis (`\fnSymbola`).
- Top White Headline Card Badge at $y = 135$ (`Anton-Regular.ttf`, 40pt, solid white card container with 2px dark border), fading out smoothly at $3.0\text{s} - 3.8\text{s}$.

### 5. 100% Faithful Transcript Packaging ([`subskills/faithful-metadata-packaging.md`](subskills/faithful-metadata-packaging.md))
- Direct transcript grounding via LLM / deterministic NLP: Top HUD headline (3–6 words Title Case, max 38 chars, 0 trailing punctuation) and YouTube title derived strictly from literal spoken words.
- Curiosity-Gap Redundancy Gate: If headline lexical overlap with opening audio exceeds 65%, automatically reformulates into a curiosity thesis question.

### 6. Pre-Render & Post-Render Quality Defense ([`subskills/pre-render-quality-gates.md`](subskills/pre-render-quality-gates.md))
- Multi-Frame Pixel Sharpness: Laplacian variance $\sigma_L^2 \ge 65.0$. Muddy or upscaled 1080p crops fail-closed.
- Burnt-In Subtitle Gate: Scans subtitle band ($0.52 \le y \le 0.88$) for pre-existing hardcoded captions.
- Audio Loudness: EBU R128 integrated loudness normalized to $-14.0\text{ LUFS}$ ($\le -1.0\text{ dBTP}$).
- 100-Point Viral Rubric: Automated scoring across Hook, Coherence, Linguistic Boundaries, Mobile Framing, Captions, Audio, and Info Density.

### 7. Autonomous 10-Minute Cadence & Fleet Distribution ([`subskills/autonomous-10m-cadence-daemon.md`](subskills/autonomous-10m-cadence-daemon.md))
- Continuous 600-second loop with non-blocking file locks.
- Cloudflare R2 CDN Ingestion via Wrangler (`wrangler r2 object put video-factory-renders/clips/clip_{id}.mp4`).
- Syndication across 10 Dedicated CLIP Channels (`CLIP-01` to `CLIP-10`), 3 Meta Super-Channels, TikTok, and Instagram Reels.
- Universal Staged Private Release with 150-minute transcode buffer and 85-upload safety headroom gate.
- Automated view-gated bounty claiming into Lili Business Checking and Form 5472 tax ledger accounting.
- Interactive Cockpit Dashboard UI ([`assets/cockpit-dashboard.html`](assets/cockpit-dashboard.html)).

---

## 3. Installation Across All Agent CLIs

Run the included universal installer:
```bash
bash install.sh
```

Automatically links `clip-short` across all active agent CLI environments:
- **Antigravity CLI (`agy`)**: `~/.gemini/antigravity-cli/skills/clip-short` & `~/.gemini/config/skills/clip-short`
- **Universal Agent (`.agents`)**: `~/.agents/skills/clip-short`
- **Claude Code**: `~/.claude/skills/clip-short`
- **Cursor IDE, Codex, Copilot, Factory Droid, Windsurf, OpenHands, Devin**: All supported.

---

## 4. License

MIT License. Copyright (c) 2026 Magebase.
