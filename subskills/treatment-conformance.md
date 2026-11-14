# Subskill: Treatment Conformance

The planner writes a `TreatmentSpec` before rendering. After rendering, an independent pass compares the exported frames against that spec. A treatment label is a claim that must be proven, not a description of intent.

---

## 1. Spec Model

| Field | Meaning |
| :--- | :--- |
| `treatment` | Planned editing treatment |
| `beats[]` | Semantic beats with `start`, `end`, `label`, `requires_change`, `required_objects` |
| `requires_face` | A relevant face must be visible in every beat |
| `face_roi` | Region where the face is expected (top pane, active speaker area) |
| `supporting_roi` | Diagram/card region used for beat-change measurement |
| `min_frame_utility` | Minimum information density per beat |
| `min_beat_change` | Minimum normalized change between consecutive beats |

## 2. Required Conformance Rules

| Treatment | Must prove |
| :--- | :--- |
| `PROGRESSIVE_DIAGRAM_ZOOM` | At least two meaningful diagram states; supporting ROI changes at the semantic beat boundary |
| `DYNAMIC_SPEAKER_SWITCHING` | A relevant face is visible in every beat; no mic-only shot while a speaker is active |
| `SCENE_BY_SCENE` | Scene changes align with narrative beats; no low-information shot during setup/reveal |
| `ADAPTIVE_SPLIT_SCREEN` / `PICTURE_IN_PICTURE` | Both panes carry information; supporting pane is readable |
| `FULL_SCREEN_CROP` | Subject remains in frame; no accidental crop of face or key object |

## 3. Measurement

- Resize each sampled frame to a fixed canvas (270×480) and convert to grayscale.
- **Frame utility** = 0.5 × normalized luminance variance + 0.5 × normalized edge density.
- **Beat change** = mean absolute difference between consecutive beat representatives, normalized to 0–1, measured only inside `supporting_roi` when present.
- Face area is measured with YuNet on the BGR frame inside `face_roi`; area is relative to the full frame.

## 4. Verdicts

| Verdict | Condition |
| :--- | :--- |
| `PASS` | No conformance failures |
| `TREATMENT_NOT_IMPLEMENTED` | Supporting visual change below threshold at a beat that requires change |
| `MISSING_FACE` | Active-speaker beat has no relevant face |
| `LOW_FRAME_UTILITY` | Beat is visually empty or uninformative |
| `NO_EVIDENCE` | No sampled frame exists for a planned beat |

`TREATMENT_NOT_IMPLEMENTED` and `MISSING_FACE` are critical failures. A high editorial score cannot override them.

## 5. Object Presence

Object presence that requires a vision model is recorded as `unverified_objects` and surfaced to human review. Never silently pass "the flies are visible" or "the harness is readable" without evidence.
