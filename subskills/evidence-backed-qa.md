# Subskill: Evidence-Backed QA & Reproducibility

A pass/fail verdict without evidence is not a quality gate. Every report must let a human reproduce the decision.

---

## 1. Required Evidence

| Evidence | Content |
| :--- | :--- |
| `sampled_frames[]` | Timestamp, utility score, frame hash |
| `treatment_conformance` | Treatment, beat table, utility/change/face per beat, unverified objects |
| `vision_review` | Findings with time, severity, issue, suggestion, decision |
| `thumbnail` | Status, failures, mobile readability metrics |
| `campaign` | Campaign ID, min/max duration, policy source, status |
| `gate_statuses` | `technical`, `editorial`, `campaign`, `ready_for_approval` |

## 2. Four Statuses

| Status | Meaning |
| :--- | :--- |
| `TECHNICAL_PASS` | Container, codecs, resolution, loudness, black/freeze checks pass |
| `EDITORIAL_PASS` | Conformance, vision review, semantic utility, thumbnail pass |
| `CAMPAIGN_PASS` | Duration, rights, disclosures, account, hashtag/content rules pass |
| `READY_FOR_APPROVAL` | All three pass; human approval still required |

One gate never compensates for another. A 95-point editorial score with a missing face is still `REJECTED_RENDER`.

## 3. Reproducibility Manifest

Every batch report records:

- Git commit SHA.
- Skill version.
- Renderer version.
- Classifier and layout versions.
- Campaign configuration hash.
- Source media hash.
- Fixture manifest hash.

## 4. Report Rule

If a metric cannot be measured (e.g., no face detector, no object detector), record `unverified` and fail closed to `HUMAN_REVIEW` when the missing check is critical. Never convert an unmeasured claim into a pass.
