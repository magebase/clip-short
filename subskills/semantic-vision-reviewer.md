# Subskill: Genuine Semantic Vision Reviewer

Heuristic frame scores cannot answer "does this frame communicate the narration?"

---

## 1. Reviewer Requirements

| Field | Requirement |
| :--- | :--- |
| `provider` | `Meta Model API` |
| `method` | `muse_responses_video` (native MP4 via Responses API) |
| `model` | `muse-spark-1.3-contributor` only |
| `reviewer_version` | Must match the artifact version |
| `reviewed_output_sha256` | Hash of the exact MP4 reviewed |
| `inspected_frames` | Time, hash, and a short crop/reference for each inspected frame |
| `explanation` | Written rationale tying the frame to the narration and edit plan |
| `findings` | Structured findings; empty findings require inspected-frame provenance |

## 2. What the Reviewer Must Answer

For each critical beat:

- What is on screen?
- What does the narration say at this timestamp?
- Is the expected object/person/diagram element visible and readable?
- Does the visual match the intended treatment?
- Is anything clipped, obscured, or contradicted?

## 3. Sole Model Policy

Muse Spark 1.3 Contributor is the **only** permitted model-based critic. Gemini, DeepSeek, GPT, Claude, local heuristics, and any other model may not critique, provide second opinions, form ensembles, or serve as fallback.

Deterministic tools may measure, but cannot issue semantic/editorial verdicts.

The reviewer must not be the planner. It receives the rendered video, treatment spec, campaign rules, and narration timeline. It does not receive the planner's rationale as an answer key.

## 4. Failure Language

- `CRITIC_MODEL_POLICY_VIOLATION`
- `HEURISTIC_REVIEWER_NOT_SEMANTIC`
- `REVIEW_EVIDENCE_MISSING`
- `EMPTY_REVIEW_PASS`
- `REVIEWER_VERSION_MISMATCH`

Heuristic checks may remain as pre-filters, but they cannot issue a semantic PASS.
