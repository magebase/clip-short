# Subskill: Speaker-to-Face Alignment

A visible face is not proof that the active speaker is on screen. v2.3 requires beat-level alignment evidence.

---

## 1. Required Per Beat

| Field | Meaning |
| :--- | :--- |
| `active_speaker_id` | Diarization speaker for the audio turn |
| `visible_speaker_id` | Identity of the face currently on screen |
| `speaker_match_confidence` | 0.0–1.0 confidence of the match |
| `shot_type` | `ACTIVE_SPEAKER`, `REACTION`, `BROLL`, `WIDE`, `MIC_ONLY` |
| `face_bbox_norm` | Face box normalized to the output frame |

## 2. Rules

- `shot_type == MIC_ONLY` while speech is active is a critical failure, even for 0.5s.
- `visible_speaker_id != active_speaker_id` is allowed only for an intentional `REACTION` shot with minimum dwell time.
- If diarization or face identity is unavailable, record `not_checked` and fail closed to `HUMAN_REVIEW`; never infer identity from face area alone.
- Face area proves presence, not identity.

## 3. Renderer Contract

The renderer must emit speaker tracks and camera assignments before QA. QA compares the two; it does not guess.
