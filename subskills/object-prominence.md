# Subskill: Object Prominence for Illustrated Storytelling

Narration naming an object does not prove the object is visible. v2.3 requires expected/observed object evidence with prominence.

---

## 1. Required Per Beat

| Field | Meaning |
| :--- | :--- |
| `expected_objects` | Objects named or implied by the narration |
| `observed_objects` | Objects detected in the frame |
| `semantic_relevance` | `verified`, `not_detected`, or `not_checked` |
| `object_bbox_norm` | Normalized bounding box of the decisive object |
| `object_prominence` | Area ratio or equivalent prominence score |
| `evidence_frame_sha256` | Hash of the exact frame inspected |

## 2. Thresholds

- The decisive object should occupy enough frame area to be recognizable at mobile size.
- Flies/dots: minimum count and minimum cluster area, not just dark pixels.
- Sickle/tool: minimum area ratio and aspect/shape check.
- If a detector is unavailable, record `not_checked` and fail closed.

## 3. Editorial Rule

Make the flies and sickle immediately recognizable when the narration introduces them. Hold the decisive evidence before moving to the confession or conclusion. Do not add unsupported visual facts.
