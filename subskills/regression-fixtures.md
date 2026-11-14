# Subskill: Regression Fixtures & Release Acceptance

The three reviewed renders are permanent regression fixtures. Every skill change must re-run them before release. A change that reintroduces the Theo debug overlay, regresses the Lex edit, or truncates the Veritasium payoff is rejected.

---

## 1. Fixture Set

| Fixture | Source archetype | Narrative archetype | Treatment | Key regression |
| :--- | :--- | :--- | :--- | :--- |
| `clip_688_lex` | `MULTICAM_PODCAST` | `CONTRARIAN_OPINION` | `DYNAMIC_SPEAKER_SWITCHING` | Camera follows speaker turns; headline does not cover face; thumbnail has one headline |
| `clip_37_theo` | `CORNER_PIP_SCREEN` | `EXPLANATION` | `PROGRESSIVE_DIAGRAM_ZOOM` | No debug overlay; no cursor; diagram readable and not cropped; one thumbnail headline |
| `clip_794_veritasium` | `NARRATED_ILLUSTRATION` | `CURIOSITY_MYSTERY` | `SCENE_BY_SCENE` | Mystery-to-confession intact; runtime respects campaign config; no duplicated thumbnail/caption idea |

Fixtures are inputs plus expected outputs plus acceptance assertions, not just videos.

---

## 2. Fixture Manifest

```json
{
  "fixture_id": "clip_37_theo",
  "source": {
    "url": "REQUIRED",
    "approved": true,
    "rights": "fair_use_commentary"
  },
  "campaign": "campaigns/clipping-default.yaml",
  "expected": {
    "format": {
      "visual_archetype": "CORNER_PIP_SCREEN",
      "narrative_archetype": "EXPLANATION",
      "editing_treatment": "PROGRESSIVE_DIAGRAM_ZOOM"
    },
    "runtime": {"min": 18.0, "max": null},
    "must_preserve": [
      "complete explanation of harness -> LLM -> syntax -> tools",
      "speaker visible during the analogy"
    ],
    "must_not_contain": [
      "debug overlay",
      "visible cursor",
      "cropped diagram labels",
      "duplicate thumbnail headline"
    ]
  },
  "acceptance": [
    "production_gate == PASS",
    "editorial.total >= 80",
    "debug_overlay_absent",
    "cursor_absent",
    "diagram_labels_readable",
    "thumbnail_single_headline",
    "caption_audio_match"
  ]
}
```

---

## 3. Acceptance Assertions

### All Fixtures
- `production_gate == PASS`.
- Resolution $1080 \times 1920$; H.264/AAC; no black frames; no unintended freezes $> 0.8\text{s}$.
- Loudness inside campaign/house spec; true peak $\le -1.0\text{ dBTP}$.
- Captions match re-transcribed exported audio.
- No text intersects the face protected region.
- Five text layers are semantically consistent and not verbatim duplicates.
- Thumbnail: one headline, unobstructed face, no subtitle fragments, readable at mobile preview size.

### Theo-Specific
- No filter expression, debug text, phase label, or internal variable visible in any sampled frame.
- No mouse cursor visible.
- Every diagram beat used in the edit is readable: primary labels $\ge 24\text{px}$ at $1080$ width.
- No important node, label, or arrow cropped at any tracked position.
- No permanent full-diagram bottom pane if labels would become unreadable.
- Supporting content uses the diagram, not a chat column or sidebar.

### Lex-Specific
- The active speaker is visible during the concluding exchange.
- Camera cuts occur on question/answer/trade-off/payoff beats, not arbitrary times.
- Headline pill clears the speaker's head and hair.
- Thumbnail does not stack HUD headline, a second headline, and a subtitle fragment.

### Veritasium-Specific
- The story reaches the confession: summons $\to$ sickles placed $\to$ flies gather $\to$ owner admits.
- The confession is not cut to satisfy a default runtime; setup is compressed first.
- If the campaign allows it, runtime may exceed the house default up to the campaign ceiling.
- Opening may tease the sickle/flies but must not spoil the confession.
- Thumbnail does not repeat the caption's idea verbatim.

---

## 4. Run Procedure

```bash
# 1. Load campaign preflight
python -m clip_short.preflight --campaign campaigns/clipping-default.yaml

# 2. Classify each fixture source
python -m clip_short.classify --fixture fixtures/clip_37_theo.json

# 3. Render each fixture
python -m clip_short.render --fixture fixtures/clip_37_theo.json --out renders/regression/

# 4. Run the production gate on the exported MP4
python -m clip_short.qa --mp4 renders/regression/clip_37_theo.mp4 \
  --fixture fixtures/clip_37_theo.json --contact-sheet

# 5. Run editorial scoring after the gate passes
python -m clip_short.score --mp4 renders/regression/clip_37_theo.mp4 \
  --fixture fixtures/clip_37_theo.json

# 6. Compare against expected
python -m clip_short.regress --fixture fixtures/clip_37_theo.json \
  --actual renders/regression/clip_37_theo.qa.json
```

### Contact Sheet Sampling
At minimum:
- $0.25\text{s}$
- $1.0\text{s}$
- Every major scene transition
- Every caption/graphic transition
- Midpoint
- Final $2.0\text{s}$

Inspect the exported MP4, not the render configuration or an intermediate file.

---

## 5. Result File

```json
{
  "fixture_id": "clip_37_theo",
  "render_path": "string",
  "production_gate": "PASS | REJECTED_RENDER | HUMAN_REVIEW",
  "failures": [],
  "editorial_total": 0,
  "assertions": [
    {"name": "debug_overlay_absent", "pass": true, "evidence": "contact_sheet"},
    {"name": "cursor_absent", "pass": true, "evidence": "contact_sheet"},
    {"name": "diagram_labels_readable", "pass": true, "evidence": "ocr+font_height"},
    {"name": "thumbnail_single_headline", "pass": true, "evidence": "ocr"},
    {"name": "caption_audio_match", "pass": true, "evidence": "re_asr_diff"}
  ]
}
```

A single failed assertion fails the release. No waivers for known bugs.

---

## 6. Release Gating

Before merging or publishing a skill change:

1. All three fixtures pass production gate.
2. All fixture-specific assertions pass.
3. Editorial totals do not drop more than 5 points from the recorded baseline without a recorded reason.
4. New failure modes are added to the production gate and to this fixture set.
5. The regression results are stored with the release.

The fixtures stay in the repository permanently. New source archetypes get new fixtures; existing ones are never deleted to make a release pass.

---

## 7. v2.1 Acceptance Checklist

A release is not approved until all fourteen checks pass and evidence is attached.

| # | Fixture | Check |
| ---: | :--- | :--- |
| 1 | Lex 688 | No microphone-only shot while an identifiable active speaker is available |
| 2 | Lex 688 | Camera switching follows speaker turns and intentional reactions |
| 3 | Lex 688 | HUD, captions, and thumbnail do not obscure the face |
| 4 | Theo 37 | At least two meaningful, semantically justified diagram changes |
| 5 | Theo 37 | Harness, model, and tool interaction readable at 360px-wide playback |
| 6 | Theo 37 | Every diagram state matches the accompanying explanation |
| 7 | Veritasium 794 | No long low-information shots during discovery and reveal |
| 8 | Veritasium 794 | Flies and sickle clearly visible when referenced |
| 9 | Veritasium 794 | Confession receives sufficient visual emphasis |
| 10 | All three | Duration passes the actual campaign configuration |
| 11 | All three | No caption transcription or synchronization failures |
| 12 | All three | No duplicated or obstructive thumbnail headline |
| 13 | All three | Automated QA attaches actual evidence from the exported video |
| 14 | All three | Failed semantic or rendering tests cannot be overridden by a high editorial score |

## 8. Required Evidence Per Fixture

- `treatment_conformance.beats[]` with timestamp, utility, change, face area.
- `vision_review.findings[]` with time, severity, issue, suggestion, decision.
- `thumbnail.status` and mobile readability metrics.
- `campaign` policy evidence with `campaign_id`, `min_seconds`, `max_seconds`, `policy_source`.
- `gate_statuses` with all four statuses.
- Reproducibility manifest with git SHA, skill version, renderer version, config hash, source hash.


---

## 9. v2.2 Evidence Acceptance

A PASS is valid only when the batch validator returns `PASS`. Required per-clip evidence:

- Per-clip manifest with git SHA, renderer version, campaign config hash, source media hash.
- Diagram/supporting ROI, change basis, and object checks for diagram/split/PiP treatments.
- Speaker face area per beat for speaker switching.
- Independent reviewer ID/version with `independent: true`.
- Thumbnail status, text-block evidence, and face rectangle for face-led thumbnails.
- Campaign ID, duration window, and policy source.
- All four gate statuses.

`UNSUPPORTED_PASS` is a release blocker. `not_checked` is not a pass.

---

## 10. v2.3 Evidence Gates

A v2.3 PASS requires:

- Speaker switching: per-beat `active_speaker_id`, `visible_speaker_id`, `speaker_match_confidence`, `shot_type`, `face_bbox_norm`.
- Diagram: per-beat `diagram_roi`, `semantic_state`, `roi_only_change`, `readable_labels`, `evidence_frame_sha256`.
- Illustration: per-beat `expected_objects`, `observed_objects`, `semantic_relevance`, `object_bbox_norm`, `object_prominence`, `evidence_frame_sha256`.
- Reviewer: provider, method, model, reviewer ID/version, reviewed output hash, timestamps, evidence hashes.
- Thumbnail: headline count/bbox, focal bbox, face/eye overlap, mobile OCR, semantic match, crop completeness, thumbnail hash.
- HUD persistence, caption review, technical inspection, campaign rule provenance, output hash, human approval state.

Missing evidence is `REVIEW_REQUIRED`; contradictory PASS is `BLOCKED`.


---

## v2.4 Acceptance Checklist

- Lex: every camera cut validated; no unjustified microphone-only shot; final shot justified or replaced.
- Lex: thumbnail OCR and semantic checks are real, not `not_checked`.
- Theo: every diagram node, label, and arrow has a bbox inside the 2% safe margin.
- Theo: object checks use semantic identity, not text-label counts.
- Theo: syntax and execution states communicate different concepts.
- Theo: thumbnail does not obscure the speaker's face.
- Veritasium: no false fly detection in the farmer scene.
- Veritasium: the fly at the descent beat is fully inside frame.
- Veritasium: captions do not collide with the sickle reveal.
- Veritasium: thumbnail communicates the fly-related discovery.
- All: required checks distinguish PASS, FAIL, and NOT_CHECKED.
- All: renderer and reviewer versions match and are reproducible.
- All: human approval remains separate from automated readiness.
- All: any `not_checked` blocks PASS.
