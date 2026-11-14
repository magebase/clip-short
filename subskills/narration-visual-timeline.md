# Subskill: Narration-to-Visual Timeline

Every narrative beat gets a timestamp and an expected visual event.

---

## 1. Beat Schema

```json
{
  "start": 15.0,
  "end": 18.0,
  "narration": "flies begin to descend",
  "expected_objects": ["fly"],
  "required_visual": "a fly fully inside the frame, moving toward a sickle",
  "caption_safe_zone": "avoid the fly and sickle",
  "evidence_frame_sha256": "…"
}
```

## 2. Rules

- Do not claim an object is visible before its narration timestamp.
- A reveal may begin slightly before the narration finishes, but not before the setup exists.
- Match the expected object to the exact timestamp; measure the frame at that time.
- If the source has no shot containing the required object, mark the beat `not_checked` or change the treatment; never infer it from unrelated ink marks.
- Keep the decisive object on screen before moving to the confession or conclusion.

## 3. Temporal Mismatch

A frame at 12.5s showing farmers cannot satisfy a flies expectation for a 15.5s narration. Emit `TEMPORAL_OBJECT_MISMATCH`.

## 4. Caption Avoidance

Caption bounding boxes must not overlap the expected object or the diagram node required at that beat. Emit `CAPTION_OBJECT_COLLISION`.
