# Subskill: Fail-Closed QA

A PASS is a claim. Missing evidence is not a pass.

---

## 1. Result States

| State | Meaning |
| :--- | :--- |
| `PASS` | Every required check ran and produced positive evidence |
| `FAIL` | A check ran and found a defect |
| `NOT_CHECKED` | A check did not run; never a pass |
| `HUMAN_REVIEW` | Ambiguity or missing capability |

`not_checked` in any required field blocks `PASS`, `READY_FOR_APPROVAL`, and batch approval.

## 2. Required Boolean Evidence

These must be actual booleans, not `not_checked`:

- Thumbnail `mobile_ocr_pass`
- Thumbnail `semantic_match`
- Diagram `no_edge_clipping`
- Diagram `semantic_state_distinct`
- Object `caption_collision` (must be false)
- Object `semantic_relevance` (must be `verified`)

## 3. No Score Compensation

A high editorial score never overrides a failed semantic, object, speaker, thumbnail, campaign, or technical check.

## 4. Contradictions

If a gate says PASS while any required evidence is missing or contradictory, emit `PASS_STATUS_UNSUBSTANTIATED` and block the batch.
