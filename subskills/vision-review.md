# Subskill: Independent Post-Render Vision Review

The agent that planned the edit must not approve its own render. The vision reviewer receives only the exported frames, the treatment spec, and the conformance measurements. It does not receive the planner's rationale.

---

## 1. Review Contract

```json
{
  "clip": "clip_37",
  "review": [
    {
      "time": 12.0,
      "severity": "MAJOR",
      "issue": "Diagram does not illustrate the spoken concept",
      "suggestion": "Introduce a visual representation of the special syntax"
    }
  ],
  "decision": "RENDER_REVISION"
}
```

## 2. Severity Model

| Severity | Meaning | Action |
| :--- | :--- | :--- |
| `CRITICAL` | Broken frame, missing subject, debug artifact, policy breach | Re-render immediately |
| `MAJOR` | Treatment not implemented, wrong speaker, empty reveal, face occlusion | Re-render or human review |
| `MINOR` | Weak framing, minor clutter, low-value beat | Improve if time allows |

## 3. Deterministic Reviewer

`HeuristicVisionReviewer` checks:

- Frame utility below the spec floor.
- Missing face on active-speaker beats.
- Supporting visual unchanged across diagram beats.
- No evidence for a planned beat.

It returns `RENDER_REVISION` on any major/critical finding and attaches per-frame utility evidence.

## 4. Vision-Model Adapter

A vision model may replace the heuristic reviewer. It must return the same structured schema, use the exported MP4 frames only, and be independent of the planning agent. The planner cannot edit the reviewer prompt after seeing the render.

## 5. Iteration Limit

At most 2–3 render/review cycles. Stop when all critical/major findings are resolved or escalate to `HUMAN_REVIEW`. Never loop indefinitely adding graphics.
