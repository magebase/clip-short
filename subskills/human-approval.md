# Subskill: Human Approval State

Automated QA never publishes. Each clip carries an explicit approval state.

---

## 1. States

| State | Meaning |
| :--- | :--- |
| `PENDING` | Awaiting human review |
| `APPROVED` | Human approved video, campaign eligibility, account, title, disclosure |
| `REJECTED` | Human rejected; do not publish |
| `CHANGES_REQUESTED` | Human requested a revision |

## 2. Rules

- `READY_FOR_APPROVAL` is not `APPROVED`.
- No publish action without `APPROVED`.
- Approval must record reviewer identity, timestamp, and the exact output SHA-256.
- Campaign eligibility, payout claims, and account selection are human decisions.
