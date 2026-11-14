---
name: clip-short
description: Format-aware Autonomous AI Short Clipper and Viral Video Production skill for Antigravity CLI (agy), Claude Code, Codex, Cursor, and multi-agent fleets. Ingests raw livestreams, podcasts, VODs, screen recordings, and narrated documentaries; classifies source visual archetype, narrative archetype, and editing treatment on three independent axes; routes to an adaptive layout engine (full-screen, dynamic speaker switching, adaptive split-screen, PiP, progressive diagram tracking, scene-by-storytelling) instead of a fixed recipe; enforces campaign-aware runtime and linguistic boundary snapping; verifies transcripts and terminology; generates separated HUD, title, caption, and thumbnail text layers; renders face-aware kinetic typography; proves the exported MP4 with an independent vision review, treatment-conformance checks, thumbnail QA, and evidence-backed gates; and requires human approval before any staged release. Use when the user wants to clip, edit, produce, package, score, QA, or automate viral vertical shorts, TikToks, Reels, or highlights from long-form video.
---

# Autonomous AI Short Clipper & Format-Aware Viral Video Production (clip-short v2.4)

An agentic video engineering skill that ingests long-form source material, understands the source format and the story, chooses a suitable visual treatment, renders a mobile-first vertical video, and then proves from the exported MP4 that the result is correct.

v2.4 keeps the three-axis router and closes the gap between claimed and visible quality: fail-closed QA, genuine multimodal semantic review, narration-to-visual timestamps, shot-level speaker checks, real object identity, diagram boundary validation, caption/object collision tests, thumbnail OCR, reproducible provenance, and campaign performance learning.

v2.0 replaced the fixed "one recipe for every source" model with three independent decisions:

1. **What is the source?** (visual archetype)
2. **What is the story?** (narrative archetype)
3. **What treatment serves that story?** (editing treatment)

The 54/46 split-screen is one strong preset within that system, not a universal law. No clip is marked ready until it passes the production quality gate against the actual rendered file.

---

## When to Use

- Ingesting and screening raw livestreams, conference talks, podcasts, and multi-hour VODs for high-retention short candidates
- Selecting candidates with the **Highest Expected Value (`EV`)** formula, gated by campaign eligibility
- Classifying source material along the **three independent axes** (`visual_archetype`, `narrative_archetype`, `editing_treatment`)
- Routing layout through the **Adaptive Layout Engine** (full-screen crop, speaker switching, adaptive split-screen, PiP, progressive diagram tracking, scene-by-scene storytelling, minimalist documentary)
- Enforcing **campaign-aware linguistic boundary snapping**: complete-sentence cold opens, zero fillers, terminal punctuation, and a runtime that follows campaign rules without truncating the payoff
- Verifying transcripts and domain terminology before packaging
- Rendering **face-aware kinetic typography** with safe-zone clearance
- Separating **five distinct text layers**: HUD headline, subtitles, YouTube title, thumbnail headline, campaign caption
- Running **full-frame post-render inspection** on the exported MP4 and failing closed to `REJECTED_RENDER`
- Scoring with a **pass/fail production gate** plus an **editorial performance-potential score**
- Recording real campaign metrics and feeding them back into future selection
- Preparing a verified submission package for **human-approved** staged release

---

## Architecture & Subskills Index

```
                        [ Raw 4K / 1440p Master Source ]
                                      |
                                      v
                    +-----------------------------------+
                    |   1. Campaign Preflight           | ---> [subskills/campaign-preflight.md]
                    |   - Duration / sound / content    |      Fail closed to HUMAN_REVIEW
                    |   - Rights & approved source      |      when rules are missing
                    +-----------------------------------+
                                      |
                                      v
                    +-----------------------------------+
                    |   2. Three-Axis Classification    | ---> [subskills/format-router-templates.md]
                    |   A. Visual source archetype      |      [references/clipper-format-archetypes.md]
                    |   B. Narrative archetype          |
                    |   C. Editing treatment            |
                    +-----------------------------------+
                                      |
              +-----------------------+-----------------------+
              |                                               |
              v                                               v
+-----------------------------+                 +-----------------------------+
|  3. Transcript Verification |                 |   4. Linguistic Snapping    |
|  - ASR confidence           |                 |  - Complete sentence open   |
|  - Domain terminology       |                 |  - 0 filler words           |
|  - Entity / acronym checks  |                 |  - Terminal punctuation     |
|  - Original subtitle diff   |                 |  - Campaign-aware runtime   |
|  [subskills/transcript-     |                 |  [subskills/linguistic-     |
|   verification.md]          |                 |   boundary-snapping.md]     |
+-----------------------------+                 +-----------------------------+
              |                                               |
              +-----------------------+-----------------------+
                                      |
                                      v
                    +-----------------------------------+
                    |   5. Adaptive Layout & Semantic   | ---> [subskills/pip-split-screen-geometry.md]
                    |      Beat Editing                 |
                    |   - Format-driven crop routing    |
                    |   - Subject-change visual focus   |
                    |   - Progressive diagram tracking  |
                    +-----------------------------------+
                                      |
                                      v
                    +-----------------------------------+
                    |   6. Typography & Metadata        | ---> [subskills/kinetic-typography-safe-zones.md]
                    |   - Face-aware safe zones         |      [subskills/faithful-metadata-packaging.md]
                    |   - 5 separated text layers        |
                    |   - Dedicated thumbnail build     |
                    +-----------------------------------+
                                      |
                                      v
                    +-----------------------------------+
                    |   7. Production Gate & Scoring    | ---> [subskills/pre-render-quality-gates.md]
                    |   - Pre-render technical gates    |      [references/viral-scoring-rubric.md]
                    |   - Full-frame post-render QA     |      [subskills/regression-fixtures.md]
                    |   - Pass/fail gate + editorial    |
                    +-----------------------------------+
                                      |
                                      v
                    +-----------------------------------+
                    |   8. Human-Approved Release       | ---> [subskills/fleet-staged-publishing.md]
                    |   - Submission package            |      [subskills/autonomous-10m-cadence-daemon.md]
                    |   - Human approval required       |      [subskills/performance-feedback.md]
                    |   - Metrics feedback loop         |
                    +-----------------------------------+
```

---

## Core Production Standards (MANDATORY)

### 1. Three-Axis Classification Is Mandatory

Never map a source straight to a fixed editing template. Classify independently:

- **Axis A — Visual source archetype**: What the footage physically is (solo talking head, multi-camera podcast, corner facecam + screen share, full-screen screen recording, whiteboard/diagram, slide deck, gaming + facecam, full-screen gaming, narrated illustration/animation, narrated documentary/B-roll, sports/action, live performance, product demonstration, dual-speaker debate).
- **Axis B — Narrative archetype**: What the story is (curiosity/mystery, contrarian opinion, explanation/education, debate/disagreement, personal story, demonstration/result, comedy/punchline, reaction, list/steps, emotional revelation).
- **Axis C — Editing treatment**: How this specific story should be shown (full-screen crop, dynamic speaker switching, adaptive split-screen, picture-in-picture, progressive diagram zoom, scene-by-scene storytelling, animated captions, contextual B-roll, minimalist documentary treatment).

The six legacy `FORMAT_*` templates remain valid **treatment presets** (named combinations of the three axes). They are not the classifier.

### 2. Adaptive Layout Engine (Golden 54/46 Is a Preset, Not a Law)

Layout is selected from source content, not applied by default:

| Source content | Layout |
| :--- | :--- |
| Portrait speaker / talking head | Full-screen portrait crop |
| Landscape podcast | Face-aware vertical crop |
| Two speakers | Dynamic speaker switching with minimum dwell time |
| Corner facecam + screen share | Adaptive 54/46 or PiP |
| Wide architecture diagram | Progressive horizontal tracking and component zoom |
| Screen recording | Active-window crop and zoom |
| Illustrated animation | Full-screen scene tracking |
| Narrated B-roll / documentary | Full-screen contextual visuals |
| Slide presentation | Slide isolation with speaker inset only when useful |
| Gaming / sports | Action-safe crop with facecam inset |
| Live performance | Full-stage framing with beat-matched cuts |
| Product demonstration | Object-focused crop with hands/result visibility |

The **Golden 54/46 Mobile Split** remains the default preset for corner-PiP streamer footage:
- Top pane: $1080 \times 1040$ ($54.17\%$), head-and-shoulders crop.
- Bottom pane: $1080 \times 880$ ($45.83\%$), saliency-isolated supporting card.
- Seam: 4px `#1E293B` at $y = 1038$.

It must not be forced onto panoramic diagrams, narrated illustration, full-screen documentary, or sources where the split shrinks labels below mobile readability. When the entire diagram only fits by shrinking it, split the diagram into semantic beats and zoom each component instead.

### 3. Semantic Beat Editing Replaces Fixed-Time Phases

Visual focus changes when the **subject or argument changes**, not when an arbitrary timestamp is reached:

- **Lex-style podcast**: show the asker on the question, the answerer on the explanation, the relevant speaker on the contradiction, and hold the conclusion on the speaker delivering it.
- **Veritasium-style mystery**: intriguing opening illustration, investigator and farmers during the setup, progressive reveal on the flies, hold the sickle and confession for the payoff.
- **Theo-style technical explainer**: speaker during the analogy, interface/harness diagram during the mechanism, targeted zoom during special syntax, final node during tool execution.

The 5-phase timestamp progression may be used only as a fallback when beat detection is unavailable. Fixed phases never override semantic focus.

### 4. Narrative-First Runtime and Campaign Compliance

Resolution order for duration:

1. **Campaign rule** (explicit `min_seconds` / `max_seconds`) — highest priority.
2. **Narrative completion** — never cut a terminal payoff to hit a default number. Compress the setup instead.
3. **Default target** $18.0\text{s} - 22.5\text{s}$; flexible ceiling $23.5\text{s}$ when required to finish a thought.

Campaign requirements override house defaults for duration, sound, content, hashtags, mentions, account, audience, and disclosure. Missing or ambiguous campaign rules fail closed to `HUMAN_REVIEW`.

### 5. Transcript Verification Before Packaging

Do not blindly trust Whisper or any ASR model. Before scoring or packaging:

- Verify domain terminology, acronyms, and named entities against dictionaries.
- Compare against original source subtitles when available.
- Check ASR confidence and flag unusual substitutions.
- Require human review of low-confidence terminology.
- Never publish a title or caption built on an unverified entity.

### 6. Face-Aware Typography and Five Separated Text Layers

Keep these layers semantically consistent but textually distinct:

1. **Video HUD headline** — top curiosity badge, 3–6 words, max 38 characters, no trailing punctuation, fades out after the hook.
2. **Spoken subtitles** — verbatim word-aligned captions.
3. **YouTube title** — searchable and faithful, may use a faithful paraphrase.
4. **Thumbnail headline** — one primary headline, built in a dedicated thumbnail stage.
5. **Campaign caption and hashtags** — campaign-specific requirements.

Face-aware placement: position headline and captions from detected facial landmarks, not a single fixed coordinate. Never cover eyes, mouth, or the speaker's key expression. Captions keep `MarginV = 920` (baseline $y = 1000$) in the 54/46 preset; adaptive layouts compute an equivalent safe zone that clears the subject's face and any source text.

Thumbnail rules: one headline only, no subtitle fragments, no duplicated headline card, face and eyes unobstructed, supporting image immediately communicates the subject, readable at mobile size.

### 7. Full-Frame Post-Render QA and Production Gate

All quality decisions are made against the **actual exported MP4**, not the render configuration. Reject (`REJECTED_RENDER`) on any critical failure:

- Debug overlay: code, filter expressions, or internal variables visible in any frame.
- Cursor: mouse cursor unintentionally visible.
- Crop integrity: important diagram, text, or subject cut off.
- Graphic readability: supporting visual unreadable at mobile size.
- Face occlusion: headline or captions obscure important facial features.
- Text collisions: captions overlap existing source text.
- Thumbnail integrity: duplicate headlines or excessive text.
- Caption accuracy: spoken words differ from displayed captions.
- Visual continuity: black frames, freezes, or accidental transitions.
- Campaign compliance: duration, sound, content, or account requirements violated.

Generate a contact sheet at 0.25s, 1.0s, every major scene transition, every major caption/graphic transition, the midpoint, and the final 2 seconds. Perform a complete playback review before marking ready.

### 8. Two Separate Scores

- **Production quality gate — pass/fail.** Campaign compliance, rendering integrity, caption accuracy, audio, visual readability, and rights. One critical failure rejects the export regardless of editorial score.
- **Editorial performance potential — 100 points.** Hook (15), standalone comprehension (15), narrative/payoff (20), visual relevance and progression (15), mobile framing (10), caption accuracy/readability (10), pacing and information density (10), originality and audience fit (5). This prioritizes edits; it is not a predicted probability of virality.

### 9. v2.4 Fail-Closed Semantic Quality

A treatment label is a claim that must be proven against the exported MP4.

- **Treatment conformance**: the planner writes a `TreatmentSpec` before rendering. After rendering, measure each semantic beat. A static diagram under a `PROGRESSIVE_DIAGRAM_ZOOM` label fails `TREATMENT_NOT_IMPLEMENTED`. A mic-only shot under `DYNAMIC_SPEAKER_SWITCHING` fails `MISSING_FACE`.
- **Independent vision review**: the reviewer sees only exported frames, the spec, and conformance measurements. It returns structured findings and `RENDER_REVISION` on major/critical defects. The planner never approves its own render.
- **Semantic frame utility**: empty, pale, or low-information beats fail the utility floor. Object-presence claims that need a vision model are recorded as `unverified_objects`, never silently passed.
- **Dedicated thumbnail QA**: one headline, no subtitle fragments, no face/eye occlusion, mobile-readable after downscaling.
- **Four statuses**: `TECHNICAL_PASS`, `EDITORIAL_PASS`, `CAMPAIGN_PASS`, `READY_FOR_APPROVAL`. One gate never compensates for another.
- **Evidence-backed reports**: sampled timestamps, frame hashes, per-beat utility/change/face area, campaign policy, and a reproducibility manifest (git SHA, skill/renderer/classifier versions, config hash, source hash).

A high editorial score cannot override a critical conformance, face, object, thumbnail, campaign, or rendering failure.

- **ROI, not whole frame**: diagram and split-screen treatments compare the supporting-visual ROI only. Speaker and caption regions are excluded from the change measurement.
- **Expected/observed objects**: every expected object is `verified`, `not_detected`, or `not_checked`. `object_checks: []` is never proof that the scene is correct.
- **Independent reviewer identity**: reports record `reviewer_id`, `reviewer_version`, and `independent: true`; an empty findings list is not accepted as evidence without them.
- **Thumbnail composition audit**: one declared text layer, detected face rectangle, face/headline collision check, and mobile readability.
- **Per-clip provenance**: git SHA, renderer version, campaign config hash, and source media hash are stored per clip, never only at batch level.
- **Batch validator**: `scripts/validate_clip_short_report.py` returns `REVIEW_REQUIRED` and `UNSUPPORTED_PASS` when a PASS lacks required evidence.
- **Format-aware art direction**: podcasts, diagrams, illustrations, screen recordings, slides, gaming, and performance each have explicit visual rules.
- **Speaker-to-face alignment**: every speaker-switch beat records active and visible speaker IDs, match confidence, shot type, and face box. Face area alone is not identity.
- **Diagram legibility**: diagram treatments record ROI, semantic state, ROI-only change, readable labels, and evidence-frame hash. Complete tool flow and arrows must stay in frame.
- **Object prominence**: illustrated narration records expected/observed objects, bbox, prominence, semantic relevance, and evidence-frame hash. Prediction without evidence is `not_checked`.
- **HUD/caption controls**: HUD establishes the premise then fades; persistent HUD is measured. Karaoke captions are optional per format.
- **Media inspection**: technical PASS records ffprobe, decode, black/freeze, loudness, A/V sync, SAR, and output SHA-256.
- **Human approval**: `READY_FOR_APPROVAL` is not `APPROVED`; publishing requires a human identity, timestamp, and output hash.
- **Fail-closed**: any required `not_checked` blocks PASS; a high editorial score never overrides a semantic failure.
- **Semantic reviewer**: a multimodal vision model must explain what is on screen and why it matches the narration. Heuristic frame scores cannot issue a semantic PASS.
- **Narration timeline**: every beat has a timestamp and expected visual event; an object cannot be credited before the narration introduces it.
- **Shot-level speaker QA**: every camera cut records active speaker, visible person, shot type, intentional cutaway, and decision. Unjustified microphone shots fail.
- **Diagram element checks**: every node, label, and arrow has a bbox; edge clipping, unreadable labels, indistinct states, and caption collisions fail.
- **Object identity**: dark blobs, text counts, and large shapes are not identity evidence. Use a vision model or validated detector classes with bboxes and normalized prominence.
- **Caption collision**: captions must avoid expected objects and diagram nodes, computed from bboxes.
- **Thumbnail OCR semantics**: actual OCR and semantic match are required; `not_checked` blocks PASS.
- **Reproducible provenance**: record clean/dirty worktree, renderer source hash, dependency lock hash, build config hash, and output hash. Reviewer version must match the artifact version.
- **Performance learning**: record qualified campaign results; do not equate editorial scores with performance.

### 10. Human-Approved Distribution and No Unsupported Payment Claims

- The core deliverable is a verified video plus its submission package.
- Automatic bulk distribution is **disabled by default**. Each publish requires explicit human approval.
- Keep publishing and financial operations outside the core editing skill. Do not claim automated bounty or payment collection unless a supported API and explicit authorization exist.
- When publishing is authorized, use official APIs only, staged private release, and platform safety limits.

### 11. Sole Model Critic: Muse Spark 1.3 Contributor

All model-based critique uses **`muse-spark-1.3-contributor`** via Meta Model API (`https://api.meta.ai/v1`, Responses API), requested at `max` reasoning effort.

- No Gemini, DeepSeek, GPT, Claude, or other model may provide critique, second opinions, ensembles, or fallback reviews.
- `model/critic.lock.json` is authoritative. Required effort is `max`; an unsupported `max` stops the run. Lower effort requires `--accept-lower-effort` and is an explicit experiment, not production.
- Contributor mode requires `CLIP_SHORT_ALLOW_CONTRIBUTOR_DATA_USE=1`. Only enable it with rights to upload the footage and acceptance of Meta's product-improvement data use.
- Native MP4 is uploaded through Meta Files API and referenced as an `input_file` in Responses API.
- Every critique records model/provider, requested and confirmed effort, prompt/schema versions, request ID, usage, video SHA-256, file ID, timestamps, and caller Git SHA.
- Deterministic tools (FFprobe, FFmpeg, OCR, ASR, geometry, hashes) may measure; they may not issue editorial or semantic critique.
- Reproducibility: use `python scripts/muse_spark_critic.py probe --effort max --video …` before a batch.

Invocation:

```bash
export MODEL_API_KEY="…"
export CLIP_SHORT_ALLOW_CONTRIBUTOR_DATA_USE=1
python scripts/muse_spark_critic.py critique   --video rendered.mp4 --transcript transcript.srt   --treatment treatment-spec.json --campaign campaign.json   --out critique.json
```

Persistence uses Cloudflare Workers + D1 + R2 under `cloudflare/clip-short-critic/`. The Worker stores critiques, findings, trajectories, preferences, and R2 asset metadata. It never stores API keys.

---

## Detailed Technical Guides

- [subskills/campaign-preflight.md](subskills/campaign-preflight.md) — Campaign rule extraction, config schema, and fail-closed validation.
- [subskills/format-router-templates.md](subskills/format-router-templates.md) — Three-axis classifier and the six treatment presets.
- [references/clipper-format-archetypes.md](references/clipper-format-archetypes.md) — Visual source archetypes and detection heuristics.
- [subskills/transcript-verification.md](subskills/transcript-verification.md) — ASR confidence, terminology, entity, and subtitle diff verification.
- [subskills/linguistic-boundary-snapping.md](subskills/linguistic-boundary-snapping.md) — Narrative-first runtime resolution, boundary snapping, acoustic decay.
- [subskills/pip-split-screen-geometry.md](subskills/pip-split-screen-geometry.md) — Adaptive layout routing, face framing, saliency, and progressive diagram tracking.
- [subskills/kinetic-typography-safe-zones.md](subskills/kinetic-typography-safe-zones.md) — Face-aware safe zones, collision avoidance, and animation.
- [subskills/faithful-metadata-packaging.md](subskills/faithful-metadata-packaging.md) — Five text layers, thumbnail construction, and curiosity gates.
- [subskills/pre-render-quality-gates.md](subskills/pre-render-quality-gates.md) — Pre-render technical gates and full-frame post-render inspection.
- [subskills/treatment-conformance.md](subskills/treatment-conformance.md) — TreatmentSpec, beat measurement, and conformance verdicts.
- [subskills/vision-review.md](subskills/vision-review.md) — Independent post-render reviewer and revision loop.
- [subskills/evidence-backed-qa.md](subskills/evidence-backed-qa.md) — Four gate statuses, evidence schema, and reproducibility manifest.
- [subskills/thumbnail-qa.md](subskills/thumbnail-qa.md) — Single-headline, face-clear, mobile-readable thumbnail gate.
- [subskills/speaker-camera-selection.md](subskills/speaker-camera-selection.md) — Face-first camera hierarchy and mic-only rejection.
- [subskills/art-direction.md](subskills/art-direction.md) — Format-specific visual grammar.
- [subskills/semantic-object-qa.md](subskills/semantic-object-qa.md) — Expected/observed object statuses and detectors.
- [subskills/report-validation.md](subskills/report-validation.md) — Batch evidence validator and unsupported-PASS rejection.
- [subskills/speaker-face-alignment.md](subskills/speaker-face-alignment.md) — Diarization-to-face-track alignment evidence.
- [subskills/diagram-legibility.md](subskills/diagram-legibility.md) — Diagram ROI, complete labels, honest treatment labels.
- [subskills/object-prominence.md](subskills/object-prominence.md) — Expected/observed object and prominence evidence.
- [subskills/hud-caption-style.md](subskills/hud-caption-style.md) — Format-specific HUD and caption controls.
- [subskills/media-inspection.md](subskills/media-inspection.md) — ffprobe/ffmpeg measurement contract.
- [subskills/human-approval.md](subskills/human-approval.md) — PENDING/APPROVED/REJECTED state separation.
- [subskills/fail-closed-qa.md](subskills/fail-closed-qa.md) — PASS/FAIL/NOT_CHECKED separation and no score compensation.
- [subskills/semantic-vision-reviewer.md](subskills/semantic-vision-reviewer.md) — Multimodal reviewer evidence and independence.
- [subskills/narration-visual-timeline.md](subskills/narration-visual-timeline.md) — Timestamped expected visual events.
- [subskills/shot-level-speaker-qa.md](subskills/shot-level-speaker-qa.md) — Every-cut speaker and microphone-shot validation.
- [subskills/diagram-state-validation.md](subskills/diagram-state-validation.md) — Diagram element bboxes, boundaries, and semantic states.
- [subskills/object-identity-and-collision.md](subskills/object-identity-and-collision.md) — Identity evidence, normalized prominence, edge and caption collisions.
- [subskills/provenance-reproducibility.md](subskills/provenance-reproducibility.md) — Clean/dirty state, source/lock/config hashes.
- [subskills/caption-style-system.md](subskills/caption-style-system.md) — Format-specific HUD and phrase captions.
- [subskills/thumbnail-ocr-semantics.md](subskills/thumbnail-ocr-semantics.md) — Actual OCR and semantic thumbnail validation.
- [subskills/performance-learning.md](subskills/performance-learning.md) — Qualified campaign results and cost-aware optimization.

## Muse Spark Critic and EditPolicy

- [model/critic.lock.json](model/critic.lock.json) — Locked sole critic identity and effort.
- [scripts/muse_spark_critic.py](scripts/muse_spark_critic.py) — Probe, critique, and blind comparison client.
- [scripts/train_edit_policy.py](scripts/train_edit_policy.py) — LightGBM LambdaRank action-selector training.
- [scripts/rank_edit_actions.py](scripts/rank_edit_actions.py) — Action ranking at inference time.
- [docs/model-management.md](docs/model-management.md) — Lock, versioning, API key, and contributor consent.
- [docs/opencode-integration.md](docs/opencode-integration.md) — OpenCode provider fragment and distinctions.
- [docs/invocation-guide.md](docs/invocation-guide.md) — Probe, critique, compare, and persistence.
- [docs/training-guide.md](docs/training-guide.md) — Trajectory labels, features, splits, and promotion.
- [docs/edit-policy-architecture.md](docs/edit-policy-architecture.md) — State/action loop and role separation.
- [docs/critic-explanation-guide.md](docs/critic-explanation-guide.md) — Required fields for every suggested edit.
- [schemas/critique.schema.json](schemas/critique.schema.json) — Timestamped critique/action schema.
- [schemas/comparison.schema.json](schemas/comparison.schema.json) — Blind comparison schema.
- [schemas/trajectory.schema.json](schemas/trajectory.schema.json) — EditPolicy training row.
- [cloudflare/clip-short-critic/](cloudflare/clip-short-critic/) — Worker + D1 schema + R2 bindings.
- [assets/treatment-spec.schema.json](assets/treatment-spec.schema.json) — TreatmentSpec JSON schema.
- [assets/qa-evidence.schema.json](assets/qa-evidence.schema.json) — QA evidence JSON schema.
- [assets/qa-evidence-v23.schema.json](assets/qa-evidence-v23.schema.json) — v2.3 evidence schema.
- [assets/qa-evidence-v24.schema.json](assets/qa-evidence-v24.schema.json) — v2.4 strict semantic evidence schema.
- [references/v2.4-quality-contract.md](references/v2.4-quality-contract.md) — v2.4 fail-closed semantic, timeline, shot, object, diagram, thumbnail, and provenance contract.
- [references/viral-scoring-rubric.md](references/viral-scoring-rubric.md) — Pass/fail production gate and calibrated editorial scoring.
- [subskills/regression-fixtures.md](subskills/regression-fixtures.md) — Lex, Theo, and Veritasium v2.4 regression checklist.
- [subskills/performance-feedback.md](subskills/performance-feedback.md) — Real campaign metrics and format-level learning.
- [subskills/fleet-staged-publishing.md](subskills/fleet-staged-publishing.md) — Human-approved staged private release and pod quotas.
- [subskills/autonomous-10m-cadence-daemon.md](subskills/autonomous-10m-cadence-daemon.md) — Production cadence with human approval gates.
- [assets/ffmpeg-filter-templates.md](assets/ffmpeg-filter-templates.md) — FFmpeg filter graphs for adaptive layouts, diagram tracking, and audio mastering.
- [references/dedicated-clip-channels.md](references/dedicated-clip-channels.md) — Channel manifest for authorized distribution.
- [assets/cockpit-dashboard.html](assets/cockpit-dashboard.html) — Cockpit UI for review, metrics, and quota.
