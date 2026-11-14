# Subskill: Semantic Object Verification

Object presence is evidence, not an assumption. Every expected object gets one of three statuses.

---

## 1. Status Model

| Status | Meaning | Gate |
| :--- | :--- | :--- |
| `verified` | A registered detector found the object above threshold | Pass |
| `not_detected` | Detector ran and found insufficient evidence | Fail / `HUMAN_REVIEW` |
| `not_checked` | No detector registered | Fail closed; never a silent pass |

`object_checks: []` is not proof that the scene is correct. If a beat expects an object and no check exists, the report must say so.

## 2. Detectors

| Detector | Use | Evidence |
| :--- | :--- | :--- |
| `text_labels` | Diagram labels, code blocks, slide text | MSER cluster count |
| `dark_blobs` | Flies, dots, small objects on pale art | Contour count in area band |
| `large_shape` | Sickle, tool, product, dominant object | Largest contour area ratio |
| `face` | Active speaker, reaction shot | YuNet face area inside ROI |
| vision model | Semantic identity and relevance | Structured finding with confidence |

## 3. Beat Expectations

Each `TreatmentBeat` declares expected objects:

```json
{
  "label": "discovery",
  "objects": [
    {"name": "flies", "detector": "dark_blobs", "min_count": 20},
    {"name": "sickle", "detector": "large_shape", "min_area_ratio": 0.02}
  ]
}
```

The check runs on the **supporting ROI**, not the whole frame.

## 4. Object-Aware Reviewer

A deterministic detector is useful but not sufficient. The independent reviewer may call a vision model with the exported frame, the beat label, and the expected object list. It must return `verified`, `not_detected`, or `not_checked`, plus confidence and a short evidence string. The planner cannot edit the reviewer prompt after seeing the render.

## 5. Failure Language

- `OBJECT_NOT_DETECTED`: object expected, detector found insufficient evidence.
- `OBJECT_NOT_CHECKED`: object expected, no detector registered.
- `SEMANTIC_UNVERIFIED`: a vision model was unavailable; human review required.

Never convert an unmeasured claim into a pass.
