# Subskill: Batch Report Validation

A batch report can be internally inconsistent. Validate it before accepting any PASS.

---

## 1. Required Per-Clip Evidence

| Field | Required |
| :--- | :--- |
| `manifest.git_sha` | Yes |
| `manifest.renderer_version` | Yes |
| `manifest.campaign_config_hash` | Yes |
| `manifest.source_media_hash` | Yes |
| `treatment_conformance.roi` | Yes for split/diagram/PiP treatments |
| `treatment_conformance.change_basis` | Yes |
| `treatment_conformance.object_checks` | Yes when objects are expected |
| `treatment_conformance.beats[].face_area` | Yes for speaker switching |
| `vision_review.reviewer_id` | Yes |
| `vision_review.reviewer_version` | Yes |
| `vision_review.independent` | Must be true |
| `thumbnail.status` | PASS |
| `thumbnail.metrics.text_blocks` | Yes |
| `thumbnail.metrics.face_rect` | Yes for face-led thumbnails |
| `campaign_policy.campaign_id` | Yes |
| `campaign_policy.min_seconds` / `max_seconds` | Yes |
| `campaign_policy.policy_source` | Yes |
| `gate_statuses.technical/editorial/campaign/ready_for_approval` | Yes |

## 2. Unsupported PASS

If `ready_for_approval` is true and any required evidence is missing, emit:

```
UNSUPPORTED_PASS: ready_for_approval is true but evidence is incomplete
```

The batch is `REVIEW_REQUIRED`, not `PASS`.

## 3. Provenance

Per-clip provenance is mandatory. A single batch-level renderer/source/config hash is insufficient because each clip may use a different renderer and campaign.

## 4. Validator

Run:

```bash
python3 scripts/validate_clip_short_report.py batch_report.json
```

Exit code `0` only when every PASS is supported. `1` means review required.


---

## v2.3 Audit

Use `scripts/audit_clip_short_v23.py batch_report.json --inspect`.

Critical codes:

- `PASS_STATUS_UNSUBSTANTIATED`
- `BATCH_PASS_UNSUBSTANTIATED`
- `OUTPUT_HASH_MISSING`
- `HUMAN_APPROVAL_STATE_MISSING`

Major codes include `SPEAKER_MATCH_UNVERIFIED`, `DIAGRAM_ROI_EVIDENCE_MISSING`, `SCENE_OBJECT_EVIDENCE_MISSING`, `INDEPENDENT_REVIEWER_UNIDENTIFIED`, `THUMBNAIL_COMPOSITION_UNVERIFIED`, `CAPTION_REVIEW_UNVERIFIED`, `TECHNICAL_PASS_WITHOUT_MEASUREMENTS`, and `CAMPAIGN_RULE_PROVENANCE_MISSING`.


---

## v2.4 Audit

Use `scripts/audit_clip_short_v24.py batch_report.json --inspect`.

Critical codes:

- `CRITIC_MODEL_POLICY_VIOLATION`
- `NOT_CHECKED_BLOCKS_PASS`
- `HEURISTIC_REVIEWER_NOT_SEMANTIC`
- `OBJECT_IDENTITY_UNVERIFIED`
- `THUMBNAIL_OCR_NOT_VERIFIED`
- `THUMBNAIL_SEMANTIC_NOT_VERIFIED`
- `MIC_ONLY_ACCEPTED`
- `PASS_STATUS_UNSUBSTANTIATED`
- `BATCH_PASS_UNSUBSTANTIATED`

Major codes include `SHOT_LEVEL_SPEAKER_EVIDENCE_MISSING`, `DIAGRAM_EDGE_CLIPPING`, `DIAGRAM_STATE_NOT_DISTINCT`, `OBJECT_EDGE_CLIPPING`, `CAPTION_OBJECT_COLLISION`, `PROMINENCE_UNIT_INCONSISTENT`, `PROVENANCE_INCOMPLETE`, `REVIEWER_VERSION_MISMATCH`, `ARTIFACT_VERSION_MISMATCH`.
