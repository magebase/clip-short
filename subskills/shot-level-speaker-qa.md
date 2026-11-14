# Subskill: Shot-Level Speaker Verification

Three representative turns do not validate a multicamera edit.

---

## 1. Shot Record

```json
{
  "start": 5.0,
  "end": 6.0,
  "active_speaker": "speaker_2",
  "visible_person": null,
  "shot_type": "MIC_ONLY",
  "intentional_cutaway": false,
  "decision": "REJECT"
}
```

## 2. Rules

- Validate every camera cut, not one sample per narrative turn.
- `MIC_ONLY` while speech is active is a critical failure unless `intentional_cutaway` is true and justified.
- A visible face must match the active speaker or be an intentional reaction shot.
- Record `decision` for every shot: `ACCEPT`, `REJECT`, `BROLL`.
- If diarization or face identity is unavailable, record `not_checked` and fail closed.

## 3. Codes

- `SHOT_LEVEL_SPEAKER_EVIDENCE_MISSING`
- `MIC_ONLY_ACCEPTED`
- `SPEAKER_MATCH_UNVERIFIED`
- `SHOT_DECISION_MISSING`
