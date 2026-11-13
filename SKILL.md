---
name: clip-short
description: End-to-end Autonomous AI Short Clipper and Split-Screen Viral Video Production skill for Antigravity CLI (agy), Claude Code, Codex, Cursor, and multi-agent fleets. Ingests raw livestreams/podcasts/VODs in 4K, executes MediaPipe BlazeFace tracking with dynamic split-screen layout routing (Golden 54/46 Mobile Split, corner portrait webcam extraction, OpenCV saliency edge-detection for primary cards/code/diagrams), enforces strict linguistic narrative boundary snapping (cold open on complete sentence, terminal punctuation punchline snapping with acoustic decay, 0 filler words), generates 100% faithful transcript-driven packaging and curiosity-gap headlines, renders kinetic typography with safe-zone clearance and vector emojis, and gates final quality via multi-frame Laplacian sharpness, burnt-in caption rejection, and a 100-point viral critique scoring engine. Use when the user wants to clip, edit, produce, package, score, or automate viral vertical shorts, TikToks, Reels, or split-screen streamer/podcast highlights from long-form video.
---

# Autonomous AI Short Clipper & Split-Screen Viral Video Production (clip-short)

An agentic video engineering skill designed to autonomously ingest long-form livestreams, podcasts, keynote speeches, and coding VODs, extract high-retention narrative moments, compose mobile-first split-screen vertical videos ($9:16$), master broadcast audio, composite kinetic typography, and package high-CTR metadata.

---

## When to Use

- Ingesting and screening raw livestreams, conference talks, and multi-hour podcasts for high-virality short candidates
- Generating mobile-first vertical shorts ($1080 \times 1920$) from landscape desktop/streamer recordings (Theo, Primeagen, PirateSoftware, Lex Fridman, Huberman)
- Executing the **Golden 54/46 Mobile Split-Screen Architecture** with dynamic MediaPipe BlazeFace tracking and OpenCV card saliency
- Enforcing **Strict Linguistic Boundary Snapping**: Cold open on complete sentences (0 filler words) and terminal punchline decay snapping (18.0s – 22.5s duration)
- Rendering **Kinetic Typography with Safe-Zone Clearance** (`MarginV = 920`, baseline $y = 1000$, 0.0px seam collision, vector emojis)
- Generating **100% Faithful Transcript-Derived Packaging**: HUD headlines, Curiosity-Gap redundancy checking, and YouTube titles
- Running **Automated Pre-Render & Post-Render Quality Defense**: Multi-frame Laplacian sharpness ($\sigma_L^2 \ge 65.0$), burnt-in caption rejection, freeze-frame detection, and 100-point viral rubric scoring
- Managing multi-channel fleet publishing via **Universal Staged Private Release** and 3-pod GCP quota gates

---

## Architecture & Subskills Index

```
                                [ Raw 4K / 1440p Master VOD ]
                                              |
                                              v
                              +-------------------------------+
                              |    1. Format Classification   | ---> [references/clipper-format-archetypes.md]
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
                              |  - 0.0px Seam Collision       |
                              |  - 3-5 Word Semantic Chunks   |
                              |  - Top Hook Pill at y = 135   |
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
                              |   7. Fleet Staged Release     | ---> [subskills/fleet-staged-publishing.md]
                              |  - Private status + publishAt |
                              |  - 150-Min Transcode Buffer   |
                              |  - 3-Pod 85-Upload Headroom   |
                              +-------------------------------+
```

---

## Core Production Standards (MANDATORY)

### 1. The Golden 54/46 Mobile Split-Screen Standard
When clipping streamers sharing desktop/browser/editor/whiteboard with a corner portrait/webcam feed:
- **Top Pane ($1080 \times 1040$ / $54.17\%$ Height)**: High-resolution crop of corner webcam, framed in head-and-shoulders $2.45 \times fh$ aspect-locked crop with $+0.32 \times fh$ natural headroom shift. Zero chin/forehead cutoffs.
- **Bottom Pane ($1080 \times 880$ / $45.83\%$ Height)**: High-resolution saliency crop of active tweet card, diagram, or code block. Clamped to card bounds, scaled horizontally to 1000px with 40px left/right margins. Ultrawide fallback uses dark blurred ambient canvas (`boxblur=40:20, eq=brightness=-0.25`).
- **Seam Separation**: 4px dark slate dividing line (`#1E293B`) at $y = 1038$.

### 2. 5-Phase Motivated Camera Progression
1. **Phase 1 ($0.0\text{s} - 3.2\text{s}$)**: $112\%$ punch-in on speaker (dramatic hook).
2. **Phase 2 ($3.2\text{s} - 9.0\text{s}$)**: Standard Golden Split ($100\%$).
3. **Phase 3 ($9.0\text{s} - 14.5\text{s}$)**: $108\%$ punch-in on supporting card (content deep-dive).
4. **Phase 4 ($14.5\text{s} - 18.0\text{s}$)**: Standard Golden Split ($100\%$).
5. **Phase 5 ($18.0\text{s} - \text{End}$)**: $110\%$ punch-in on speaker for punchline delivery.

### 3. Linguistic Narrative & Complete Thought Standard
- **Runtime**: Strictly $18.0\text{s} - 22.5\text{s}$ (flexible $23.5\text{s}$ ceiling if needed to finish a thought).
- **Cold Open**: Start points must snap strictly to complete sentence or question beginnings. Zero conversational fillers (`um`, `uh`, `you know`), 60–80ms of clean pre-speech room tone, and a 35ms micro audio fade-in (`afade=t=in:d=0.035`).
- **Terminal Snapping**: Cut points must snap strictly to terminal punctuation (`.`, `!`, `?`) where a complete thought resolves. Forbids cutting on prepositions, conjunctions, pronouns, or trailing fillers. Adds 120–180ms natural acoustic decay padding with an 80ms gentle audio micro fade-out (`afade=t=out:d=0.08`).

### 4. Kinetic Typography Safe Zone (`MarginV = 920`)
- Subtitles positioned at `MarginV = 920` (baseline $y = 1000$) over speaker's torso.
- $> 180\text{px}$ clearance above supporting content ($y \ge 1180$) and above divider ($y = 1038$), ensuring **0.0px collision**.
- Natural 3–5 word semantic units, zero 1–2 word staccato flashes, zero duplicate consecutive phrases. Contractions preserved.
- Safe Zone Curiosity Hook Pill Badge at $y = 135$ in Anton with 2px stroke and translucent slate pill (`#0F172A@0.92`), fading out smoothly at $3.0\text{s} - 3.8\text{s}$.

### 5. 100% Faithful Transcript-Driven Packaging
- Both HUD headline and YouTube title must be generated directly from literal spoken words in that 18–22s cut via LLM / deterministic semantic NLP.
- Top HUD headline must be 3 to 6 words in Title Case, max 38 characters, NO trailing punctuation.
- Curiosity-Gap Redundancy Gate: If headline lexical overlap with opening spoken text exceeds 65%, reformulates into a curiosity thesis question.

### 6. Zero Burnt-In Subtitles & Multi-Frame Sharpness Bar
- Subtitle Band Scan ($0.52 \le y \le 0.88$): Persistent speech subtitles or text glyph clusters immediately fail-closed to `REJECTED_QUALITY`.
- Multi-Frame Pixel Sharpness Bar: Laplacian variance threshold strictly $\ge 65.0$.
- High-Resolution Master Downloads: `yt-dlp` requests `bestvideo[height<=2160]`.

### 7. Universal Staged Private Release Protocol
- YouTube upload payload sets `status.privacyStatus = "private"` with an explicit future `status.publishAt`.
- Minimum 2.5-hour (150-minute) transcode buffer before going public.
- 3-Pod GCP Architecture with 85-upload safety headroom gate.

---

## Detailed Technical Guides

- [references/clipper-format-archetypes.md](references/clipper-format-archetypes.md) — 5 streamer and podcast visual formats and detection heuristics.
- [references/viral-scoring-rubric.md](references/viral-scoring-rubric.md) — 100-point viral assessment rubric and auto-critique standards.
- [assets/ffmpeg-filter-templates.md](assets/ffmpeg-filter-templates.md) — Copy-pasteable FFmpeg filter graphs for split-screens, zooms, and EBU R128 audio.
- [subskills/pip-split-screen-geometry.md](subskills/pip-split-screen-geometry.md) — MediaPipe face framing math and OpenCV saliency card isolation.
- [subskills/linguistic-boundary-snapping.md](subskills/linguistic-boundary-snapping.md) — Whisper timestamp alignment and acoustic decay algorithms.
- [subskills/kinetic-typography-safe-zones.md](subskills/kinetic-typography-safe-zones.md) — Collision-free subtitle positioning and animation.
- [subskills/faithful-metadata-packaging.md](subskills/faithful-metadata-packaging.md) — Direct transcript grounding and curiosity gates.
- [subskills/pre-render-quality-gates.md](subskills/pre-render-quality-gates.md) — Laplacian sharpness, burnt subtitle OCR, and audio defense.
- [subskills/fleet-staged-publishing.md](subskills/fleet-staged-publishing.md) — Multi-channel pod architecture and private staged scheduling.
