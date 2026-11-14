# Subskill: Object Identity and Collision

Dark blobs are not flies. Text labels are not a harness.

---

## 1. Identity Evidence

| Evidence kind | Allowed for identity? |
| :--- | :--- |
| `vision_model` | Yes |
| `detector_class` with class labels and confidence | Yes, if validated |
| `dark_blobs` | No |
| `text_labels` | No |
| `large_shape` | No |

Heuristic counts may support a pre-filter, but cannot produce `semantic_relevance: verified`.

## 2. Required Fields

- `expected_objects`
- `observed_objects`
- `evidence_kind`
- `semantic_relevance`
- `object_bbox_norm`
- `object_prominence` normalized 0..1
- `caption_collision`
- `evidence_frame_sha256`

## 3. Prominence

Use one normalized unit for all objects. Do not compare a blob count (49) with an area ratio (0.0521). Convert count-based prominence to a normalized score or report it separately.

## 4. Crop Safety

An object touching the 2% safe margin fails `OBJECT_EDGE_CLIPPING`. Make the object fully recognizable at the exact narration timestamp.

## 5. Codes

- `OBJECT_IDENTITY_UNVERIFIED`
- `OBJECT_NOT_SEMANTICALLY_VERIFIED`
- `OBJECT_EDGE_CLIPPING`
- `PROMINENCE_UNIT_INCONSISTENT`
- `CAPTION_OBJECT_COLLISION`
