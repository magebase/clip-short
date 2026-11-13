---
name: clip-short
description: End-to-end Autonomous AI Short Clipper and Split-Screen Viral Video Production skill for Antigravity CLI (agy), Claude Code, Codex, Cursor, and multi-agent fleets. Ingests raw livestreams/podcasts/VODs in 4K, executes MediaPipe BlazeFace tracking with dynamic split-screen layout routing (Golden 54/46 Mobile Split, corner portrait webcam extraction, OpenCV saliency edge-detection for primary cards/code/diagrams), enforces strict linguistic narrative boundary snapping (cold open on complete sentence, terminal punctuation punchline snapping with acoustic decay, 0 filler words), generates 100% faithful transcript-driven packaging and curiosity-gap headlines, renders kinetic typography with safe-zone clearance and vector emojis, and gates final quality via multi-frame Laplacian sharpness, burnt-in caption rejection, and a 100-point viral critique scoring engine. Use when the user wants to clip, edit, produce, package, score, or automate viral vertical shorts, TikToks, Reels, or split-screen streamer/podcast highlights from long-form video.
---

# Autonomous AI Short Clipper & Split-Screen Viral Video Production (clip-short)

An agentic video engineering skill designed to autonomously ingest long-form livestreams, podcasts, keynote speeches, and coding VODs, extract high-retention moments using Expected Value ($EV$) scoring, classify into 6 battle-tested viral format templates, compose mobile-first split-screen vertical videos ($9:16$), master broadcast audio, composite kinetic spring typography with vector emojis, ingest to Cloudflare R2 CDN, syndicate across multi-platform fleets (YouTube Shorts, TikTok, Instagram Reels, Facebook Reels Super-Channels), claim view-gated bounties into business checking, and maintain an automated live Cockpit dashboard.

---

## When to Use

- Ingesting and screening raw livestreams, conference talks, and multi-hour podcasts for high-virality short candidates
- Selecting candidate clips using the **Highest Expected Value ($EV$) Formula** ($S_{\text{viral}} \times \text{Freshness} \times \text{Format} \times \text{Bounty}$)
- Routing video moments through the **6 Mega-Viral Format Templates** (`FORMAT_1_PHONK_FREEZE`, `FORMAT_2_REACTION_STACK`, `FORMAT_3_ACTION_TAG_SITCOM`, `FORMAT_4_DISCORD_BROLL`, `FORMAT_5_WHITEBOARD_EXPLAINER`, `FORMAT_N3ON_PING_PONG`)
- Executing the **Golden 54/46 Mobile Split-Screen Architecture** with dynamic MediaPipe BlazeFace tracking and OpenCV card saliency
- Enforcing **Strict Linguistic Boundary Snapping**: Cold open on complete sentences (0 filler words) and terminal punchline decay snapping (18.0s – 22.5s duration)
- Rendering **Kinetic Spring Bounce Captions (`\fscx124`) with Vector Emojis (`\fnSymbola`)** and safe-zone clearance (`MarginV = 920`, baseline $y = 1000$, 0.0px seam collision)
- Generating **100% Faithful Transcript-Derived Packaging**: HUD headlines, Curiosity-Gap redundancy checking, and YouTube titles
- Running **Automated Pre-Render & Post-Render Quality Defense**: Multi-frame Laplacian sharpness ($\sigma_L^2 \ge 65.0$), burnt-in caption rejection, freeze-frame detection, and 100-point viral rubric scoring
- Managing continuous production via the **Autonomous 10-Minute Cadence Daemon (`CADENCE_SECONDS = 600`)**
- Uploading master renders directly to **Cloudflare R2 CDN** via Wrangler CLI
- Syndicating across **10 Dedicated CLIP Channels** (`CLIP-01` to `CLIP-10`), **3 Meta Super-Channels**, TikTok, and Instagram Reels
- Automating **View-Gated Bounty Claims** into business bank accounts and logging to tax ledgers

---

## Architecture & Subskills Index

```
                                [ Raw 4K / 1440p Master VOD ]
                                              |
                                              v
                              +-------------------------------+
                              |    1. Format Classification   | ---> [references/clipper-format-archetypes.md]
                              |       (6 Viral Templates)     |      [subskills/format-router-templates.md]
                              +-------------------------------+
                                              |
               +------------------------------+------------------------------+
               |                                                             |
               v                                                             v
+-----------------------------+                               +-----------------------------+
|  2. Linguistic Snapping     |                               |   3. Spatial Split-Screen   |
|  - Complete Sentence Open   |                               |  - Golden 54/46 Top/Bottom  |
|  - 0 Filler Words           |                               |  - MediaPipe BlazeFace Crop |
|  - Terminal Punchline Decay |                               |  - OpenCV Card Saliency     |
| [subskills/linguistic-      |                               |  - 5-Phase Punch-In Zooms   |
|  boundary-snapping.md]      |                               | [subskills/pip-split-screen-|
+-----------------------------+                               |  geometry.md]               |
               |                                              +-----------------------------+
               |                                                             |
               +------------------------------+------------------------------+
                                              |
                                              v
                              +-------------------------------+
                              |    4. Typography & Safe Zone  | ---> [subskills/kinetic-typography-safe-zones.md]
                              |  - MarginV = 920, y = 1000    |
                              |  - Kinetic Pop (\fscx124)     |
                              |  - Vector Emojis (\fnSymbola) |
                              |  - Top White Card at y = 135  |
                              +-------------------------------+
                                              |
                                              v
                              +-------------------------------+
                              |    5. Transcript Packaging    | ---> [subskills/faithful-metadata-packaging.md]
                              |  - Grounded HUD Headlines     |
                              |  - Curiosity-Gap Check        |
                              |  - High-CTR Title Generation  |
                              +-------------------------------+
                                              |
                                              v
                              +-------------------------------+
                              |   6. Pre-Render Quality Gate  | ---> [subskills/pre-render-quality-gates.md]
                              |  - Laplacian Var >= 65.0      |      [references/viral-scoring-rubric.md]
                              |  - Burnt Subtitle Detection   |
                              |  - EBU R128 (-14 LUFS) Audio  |
                              |  - 100-Point Viral Rubric     |
                              +-------------------------------+
                                              |
                                              v
                              +-------------------------------+
                              |  7. 10-Minute Daemon & Fleet  | ---> [subskills/autonomous-10m-cadence-daemon.md]
                              |  - Continuous 600s Cadence    |      [subskills/fleet-staged-publishing.md]
                              |  - Cloudflare R2 CDN Upload   |      [references/dedicated-clip-channels.md]
                              |  - 10 CLIP Channels + 3 Meta  |      [assets/cockpit-dashboard.html]
                              |  - Automated Bounty Claims    |
                              +-------------------------------+
```

---

## Core Production Standards (MANDATORY)

### 1. The 6 Mega-Viral Format Templates (`FormatRouter`)
Every stream moment is classified into one of six high-converting formats:
1. `FORMAT_1_PHONK_FREEZE`: IRL Physical Stunt + Phonk Freeze-Frame + Camera Shake (IShowSpeed 53.3M benchmark).
2. `FORMAT_2_REACTION_STACK`: 50/50 Top/Bottom Reaction Stack with Seam Captions (CaseOh 18.8M benchmark).
3. `FORMAT_3_ACTION_TAG_SITCOM`: Non-Verbal Action-Tag Sitcom Edit with Neon *ASTERISK TAGS* (IShowSpeed 23.8M benchmark).
4. `FORMAT_4_DISCORD_BROLL`: Discord Voice Rant + Satisfying High-Engagement B-Roll (xQc & Jynxzi 7.3M benchmark).
5. `FORMAT_5_WHITEBOARD_EXPLAINER`: High-Retention Code / Architecture Monologue (PirateSoftware & Theo 13.2M benchmark).
6. `FORMAT_N3ON_PING_PONG`: IRL Two-Speaker Sitcom Ping-Pong Edit with Neural YuNet tracking (N3ON & Clavicular 1.2M+ benchmark).

### 2. The Golden 54/46 Mobile Split-Screen Standard
- **Top Pane ($1080 \times 1040$ / $54.17\%$ Height)**: High-resolution crop of corner webcam, framed in head-and-shoulders $2.45 \times fh$ aspect-locked crop with $+0.32 \times fh$ natural headroom shift. Zero chin/forehead cutoffs.
- **Bottom Pane ($1080 \times 880$ / $45.83\%$ Height)**: High-resolution saliency crop of active tweet card, diagram, or code block. Clamped to card bounds, scaled horizontally to 1000px with 40px left/right margins. Ultrawide fallback uses dark blurred ambient canvas (`boxblur=40:20, eq=brightness=-0.25`).
- **Seam Separation**: 4px dark slate dividing line (`#1E293B`) at $y = 1038$.

### 3. 5-Phase Motivated Camera Progression
1. **Phase 1 ($0.0\text{s} - 3.2\text{s}$)**: $112\%$ punch-in on speaker (dramatic hook).
2. **Phase 2 ($3.2\text{s} - 9.0\text{s}$)**: Standard Golden Split ($100\%$).
3. **Phase 3 ($9.0\text{s} - 14.5\text{s}$)**: $108\%$ punch-in on supporting card (content deep-dive).
4. **Phase 4 ($14.5\text{s} - 18.0\text{s}$)**: Standard Golden Split ($100\%$).
5. **Phase 5 ($18.0\text{s} - \text{End}$)**: $110\%$ punch-in on speaker for punchline delivery.

### 4. Linguistic Narrative & Complete Thought Standard
- **Runtime**: Strictly $18.0\text{s} - 22.5\text{s}$ (flexible $23.5\text{s}$ ceiling if needed to finish a thought).
- **Cold Open**: Start points must snap strictly to complete sentence or question beginnings. Zero conversational fillers (`um`, `uh`, `you know`), 60–80ms of clean pre-speech room tone, and a 35ms micro audio fade-in (`afade=t=in:d=0.035`).
- **Terminal Snapping**: Cut points must snap strictly to terminal punctuation (`.`, `!`, `?`) where a complete thought resolves. Forbids cutting on prepositions, conjunctions, pronouns, or trailing fillers. Adds 120–180ms natural acoustic decay padding with an 80ms gentle audio micro fade-out (`afade=t=out:d=0.08`).

### 5. Kinetic Typography Safe Zone (`MarginV = 920`) & Vector Emojis
- Subtitles positioned at `MarginV = 920` (baseline $y = 1000$) over speaker's torso.
- $> 180\text{px}$ clearance above supporting content ($y \ge 1180$) and above divider ($y = 1038$), ensuring **0.0px collision**.
- Word-level spring pop animation: `{\fscx124\fscy124\t(0,75,\fscx108\fscy108)}`.
- Vector emojis: Rendered via `\fnSymbola` in multi-tier neon palettes (`#FACC15`, `#06B6D4`, `#10B981`, `#F59E0B`).
- Modern White Headline Card Badge at $y = 135$ (`Anton-Regular.ttf`, 40pt, solid white card container with 2px dark border), fading out smoothly at $3.0\text{s} - 3.8\text{s}$.

### 6. 100% Faithful Transcript-Driven Packaging
- Both HUD headline and YouTube title must be generated directly from literal spoken words in that 18–22s cut via LLM / deterministic semantic NLP.
- Top HUD headline must be 3 to 6 words in Title Case, max 38 characters, NO trailing punctuation.
- Curiosity-Gap Redundancy Gate: If headline lexical overlap with opening spoken text exceeds 65%, reformulates into a curiosity thesis question.

### 7. Zero Burnt-In Subtitles & Multi-Frame Sharpness Bar
- Subtitle Band Scan ($0.52 \le y \le 0.88$): Persistent speech subtitles or text glyph clusters immediately fail-closed to `REJECTED_QUALITY`.
- Multi-Frame Pixel Sharpness Bar: Laplacian variance threshold strictly $\ge 65.0$.
- High-Resolution Master Downloads: `yt-dlp` requests `bestvideo[height<=2160]`.

### 8. Autonomous 10-Minute Cadence & Fleet Distribution
- Operates via continuous 600s loop with non-blocking file locks.
- Master renders ingested directly to **Cloudflare R2 CDN** (`video-factory-renders`).
- Multi-channel fleet syndication across **10 Dedicated CLIP Channels** (`CLIP-01` to `CLIP-10`), **3 Meta Super-Channels**, TikTok, and Instagram Reels.
- YouTube uploads enforce **Universal Staged Private Release** with a 150-minute transcode buffer and an 85-upload safety headroom gate.
- Automated view-gated bounty claiming into business checking and Form 5472 tax ledger accounting.

---

## Detailed Technical Guides

- [subskills/format-router-templates.md](subskills/format-router-templates.md) — The 6 viral templates and classification matrix.
- [subskills/autonomous-10m-cadence-daemon.md](subskills/autonomous-10m-cadence-daemon.md) — 10-minute cadence daemon, R2 ingest, and bounty claiming.
- [references/dedicated-clip-channels.md](references/dedicated-clip-channels.md) — Manifest for 10 CLIP channels and 3 Meta Super-Channels.
- [assets/cockpit-dashboard.html](assets/cockpit-dashboard.html) — Interactive Cockpit UI for multi-platform views, bounties, and quota.
- [references/clipper-format-archetypes.md](references/clipper-format-archetypes.md) — 5 streamer and podcast visual formats and detection heuristics.
- [references/viral-scoring-rubric.md](references/viral-scoring-rubric.md) — 100-point viral assessment rubric and auto-critique standards.
- [assets/ffmpeg-filter-templates.md](assets/ffmpeg-filter-templates.md) — Copy-pasteable FFmpeg filter graphs for split-screens, zooms, and EBU R128 audio.
- [subskills/pip-split-screen-geometry.md](subskills/pip-split-screen-geometry.md) — MediaPipe face framing math and OpenCV saliency card isolation.
- [subskills/linguistic-boundary-snapping.md](subskills/linguistic-boundary-snapping.md) — Whisper timestamp alignment and acoustic decay algorithms.
- [subskills/kinetic-typography-safe-zones.md](subskills/kinetic-typography-safe-zones.md) — Collision-free subtitle positioning and animation.
- [subskills/faithful-metadata-packaging.md](subskills/faithful-metadata-packaging.md) — Direct transcript grounding and curiosity gates.
- [subskills/pre-render-quality-gates.md](subskills/pre-render-quality-gates.md) — Laplacian sharpness, burnt subtitle OCR, and audio defense.
- [subskills/fleet-staged-publishing.md](subskills/fleet-staged-publishing.md) — Multi-channel pod architecture and private staged scheduling.
