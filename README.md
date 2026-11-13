# clip-short v2.0

> **Format-aware AI Short Clipper & Vertical Video Production Skill for Agent CLIs (`agy`, `claude`, `codex`, `cursor`, `copilot`, `openhands`)**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-magebase%2Fclip--short-181717.svg?logo=github)](https://github.com/magebase/clip-short)
[![FFmpeg](https://img.shields.io/badge/Engine-FFmpeg%20%7C%20OpenCV%20%7C%20Whisper-green.svg)](assets/ffmpeg-filter-templates.md)

---

## 1. Overview

`clip-short` turns long-form video into verified vertical shorts ($9:16$ for YouTube Shorts, TikTok, Instagram Reels, Facebook Reels). v2.0 is a general editing system, not a single streamer recipe:

1. **Three-axis classification** — visual source archetype, narrative archetype, editing treatment.
2. **Adaptive layouts** — full-screen, speaker switching, adaptive split, PiP, progressive diagram zoom, scene tracking, or minimalist documentary.
3. **Narrative-first boundaries** — complete thought arcs with campaign-aware runtime. Payoff is never truncated for an arbitrary duration target.
4. **Verified transcription** — domain lexicons, entity checks, source-subtitle diff, human review of low-confidence terms.
5. **Five distinct text layers** — HUD headline, subtitles, YouTube title, thumbnail headline, campaign caption.
6. **Pass/fail production gate plus editorial scoring** — one critical render defect rejects the export regardless of editorial score.
7. **Human-gated distribution** — production may be autonomous; publishing requires approval. Bulk auto-distribution is off by default.
8. **Permanent regression fixtures** — Lex, Theo, and Veritasium renders guard against known failures.

---

## 2. Core Capabilities

### 1. Three-Axis Format Router ([`subskills/format-router-templates.md`](subskills/format-router-templates.md))
- **Axis A**: 14 visual source archetypes (`MULTICAM_PODCAST`, `CORNER_PIP_SCREEN`, `NARRATED_ILLUSTRATION`, `SLIDE_DECK`, `SPORTS_ACTION`, and others).
- **Axis B**: 10 narrative archetypes (`CURIOSITY_MYSTERY`, `CONTRARIAN_OPINION`, `EXPLANATION`, `DEBATE`, `PERSONAL_STORY`, and others).
- **Axis C**: 9 editing treatments (`FULLSCREEN_CROP`, `DYNAMIC_SPEAKER_SWITCHING`, `ADAPTIVE_SPLIT`, `PROGRESSIVE_DIAGRAM_ZOOM`, `SCENE_BY_SCENE`, and others).
- Legacy viral presets remain as named treatment combinations; they are not the classifier.

### 2. Adaptive Layout Engine ([`subskills/pip-split-screen-geometry.md`](subskills/pip-split-screen-geometry.md))
- **Golden 54/46 split preset** for corner-PiP streamers: $1080 \times 1040$ speaker pane and $1080 \times 880$ supporting pane, 4px seam at $y = 1038$.
- **Layout decision matrix**: portrait speaker, landscape podcast, two speakers, corner facecam, panoramic diagram, screen recording, illustration, B-roll.
- **Progressive diagram tracking** for panoramic architecture diagrams: zoom and pan to the referenced node instead of shrinking the whole diagram into a pane.
- **Saliency isolation** that excludes chat columns and sidebars.
- **Semantic beats**: visual focus changes with the subject, not with arbitrary timestamps.

### 3. Campaign-Aware Narrative Boundaries ([`subskills/linguistic-boundary-snapping.md`](subskills/linguistic-boundary-snapping.md))
- Runtime resolution order: campaign rule $\to$ narrative completion $\to$ house range.
- House default $18.0\text{s} - 22.5\text{s}$ with a flexible ceiling up to $23.5\text{s}$; a longer complete story may pass when the campaign allows it.
- Complete-sentence cold opens, zero fillers, $35\text{ms}$ fade-in, terminal punctuation snapping, $150 - 250\text{ms}$ decay, $80\text{ms}$ fade-out.
- Compress setup before cutting payoff.

### 4. Face-Aware Kinetic Typography ([`subskills/kinetic-typography-safe-zones.md`](subskills/kinetic-typography-safe-zones.md))
- Caption baseline computed from face landmarks and layout; `MarginV = 920` is the 54/46 preset value, not a universal law.
- Rejects caption collisions with faces, source text, diagram labels, and dividers.
- 3–5 word semantic chunks, zero staccato flashes, zero duplicate cues.
- Spring pop animation, accent colors, and tone-appropriate vector emojis.
- Top curiosity pill at $y = 135$, fading out at $3.0\text{s} - 3.8\text{s}$.

### 5. Transcript Verification & Five-Layer Packaging ([`subskills/transcript-verification.md`](subskills/transcript-verification.md), [`subskills/faithful-metadata-packaging.md`](subskills/faithful-metadata-packaging.md))
- Domain dictionaries, acronym and entity checks, forced alignment, source-subtitle diff, anomaly detection.
- Five separate layers: HUD headline, subtitles, YouTube title, thumbnail headline, campaign caption.
- Faithful paraphrase allowed; every entity, number, and claim must be supported by the cut.
- Curiosity-gap overlap gate ($\le 0.65$) prevents the headline from repeating the opening line.
- Dedicated thumbnail stage: one headline, unobstructed face, no subtitle fragments.

### 6. Production Gate & Editorial Scoring ([`references/viral-scoring-rubric.md`](references/viral-scoring-rubric.md), [`subskills/pre-render-quality-gates.md`](subskills/pre-render-quality-gates.md))
- **Production gate (pass/fail)**: campaign compliance, rights, render integrity, crop integrity, readability, caption accuracy, caption collisions, audio, continuity, A/V sync, thumbnail, metadata.
- **Editorial score (100)**: hook 15, standalone comprehension 15, narrative/payoff 20, visual relevance 15, mobile framing 10, captions 10, pacing 10, originality 5.
- Rejection tests include debug overlays, visible cursors, cropped diagrams, face occlusion, source-text collisions, and unreadable mobile text.
- Inspect the exported MP4, not the render configuration. Contact sheet at $0.25\text{s}$, $1.0\text{s}$, transitions, midpoint, and final $2.0\text{s}$.

### 7. Campaign Preflight ([`subskills/campaign-preflight.md`](subskills/campaign-preflight.md))
- Per-campaign duration, required sound, required/prohibited content, hashtags, mentions, audience, account, rights, and disclosure rules.
- Missing or ambiguous rules fail closed to `HUMAN_REVIEW`.
- Submission package is immutable for the edit and re-validated before release.

### 8. Human-Gated Production & Performance Feedback ([`subskills/autonomous-10m-cadence-daemon.md`](subskills/autonomous-10m-cadence-daemon.md), [`subskills/performance-feedback.md`](subskills/performance-feedback.md))
- A 10-minute loop may prepare candidates; it does not publish every 10 minutes.
- Human approval before publishing; bulk auto-distribution disabled by default; unique edits only.
- Official REST/Graph APIs only; zero browser automation on social platforms.
- Records viewed rate, average view duration, completion, shares, comments, followers, confirmed campaign views, and payout at consistent maturity windows.
- Learns per campaign and format with sample-size guardrails; never learns toward misleading hooks.

### 9. Regression Fixtures ([`subskills/regression-fixtures.md`](subskills/regression-fixtures.md))
- `clip_688_lex`, `clip_37_theo`, and `clip_794_veritasium` are permanent fixtures.
- Theo: no debug overlay, no cursor, readable uncropped diagram, one thumbnail headline.
- Lex: correct speaker during the conclusion, face-aware headline, clean thumbnail.
- Veritasium: complete mystery-to-confession story retained.

### 10. Fleet Publishing Constraints ([`subskills/fleet-staged-publishing.md`](subskills/fleet-staged-publishing.md))
- Staged private release with `publishAt` and a $\ge 150$-minute transcode buffer, for authorized operations only.
- Three GCP pods with an 85-upload safety headroom gate.
- Clip channels cap at 2–3 clips per channel per day, spaced $\ge 4.0$ hours.
- Bounty/payment automation is out of scope unless a documented API and explicit authorization exist.

---

## 3. Pipeline

```
Load campaign preflight
  -> Verify transcript (lexicon, entities, source subtitles)
  -> Classify three axes
  -> Select narrative boundaries and runtime
  -> Choose layout and treatment
  -> Render
  -> Production gate on exported MP4 (fail closed)
  -> Editorial score
  -> Build five text layers + verified thumbnail
  -> Human approval queue
  -> Authorized submission only
  -> Record performance feedback
```

---

## 4. Installation Across All Agent CLIs

```bash
bash install.sh
```

Automatically links `clip-short` across all active agent CLI environments:
- **Antigravity CLI (`agy`)**: `~/.gemini/antigravity-cli/skills/clip-short` & `~/.gemini/config/skills/clip-short`
- **Universal Agent (`.agents`)**: `~/.agents/skills/clip-short`
- **Claude Code**: `~/.claude/skills/clip-short`
- **Cursor IDE, Codex, Copilot, Factory Droid, Windsurf, OpenHands, Devin**: All supported.

---

## 5. License

MIT License. Copyright (c) 2026 Magebase.
