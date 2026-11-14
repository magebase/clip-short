# Production Gate & Editorial Scoring Rubric

Two independent systems:

1. **Production quality gate — pass/fail.** One critical failure rejects the export regardless of editorial score.
2. **Editorial performance potential — 100 points.** Prioritizes edits for review; it is not a predicted probability of virality.

Never blend them into one number. A beautifully told clip with a debug overlay is not an 85/100; it is `REJECTED_RENDER`.

---

## 1. Production Quality Gate (Pass/Fail)

Each row must pass. No averaging, no compensation.

| Area | Pass condition | Critical failure |
| :--- | :--- | :--- |
| **Campaign compliance** | Duration, sound, hashtags, mentions, content, disclosure, account, and audience rules validated against the loaded campaign config | Any missing or violated rule $\to$ `HUMAN_REVIEW` or `REJECTED_RENDER` |
| **Rights and source** | Approved source URL, license/fair-use basis, attribution present | Unclear rights $\to$ `HUMAN_REVIEW` |
| **Render integrity** | Exported MP4 passes `ffprobe`; no debug overlay; no cursor; no black frames | Any visual artifact $\to$ `REJECTED_RENDER` |
| **Crop integrity** | Important subjects, labels, arrows, hands, and results fully in frame | Cropped diagram/action $\to$ `REJECTED_RENDER` |
| **Readability** | Primary labels $\ge 24\text{px}$, secondary $\ge 18\text{px}$ at $1080$ width | Unreadable at mobile size $\to$ `REJECTED_RENDER` |
| **Caption accuracy** | Displayed captions match re-transcribed exported audio; negations, entities, numbers intact | Mismatch $\to$ `REJECTED_RENDER` |
| **Caption collisions** | No overlap with face, source text, diagram labels, or divider | Collision $\to$ `REJECTED_RENDER` |
| **Audio** | Integrated loudness within campaign/house spec; true peak $\le -1.0\text{ dBTP}$; no clipping | Clipping or out-of-spec loudness $\to$ `REJECTED_RENDER` |
| **Visual continuity** | No unintended freezes $> 0.8\text{s}$, no dead air $> 0.6\text{s}$, no broken transitions | Failure $\to$ `REJECTED_RENDER` |
| **A/V sync** | Drift $\le 80\text{ms}$ | Failure $\to$ `REJECTED_RENDER` |
| **Thumbnail** | One headline, unobstructed face, no subtitle fragments | Failure $\to$ `REJECTED_RENDER` |
| **Metadata** | Five text layers distinct and semantically consistent | Duplicate or contradictory layers $\to$ `RENDERED_PACKAGING_HOLD` |

Production verdict: `PASS` or `REJECTED_RENDER` / `HUMAN_REVIEW`. There is no partial pass.

---

## 2. Editorial Performance-Potential Score (100 Points)

Apply only after the production gate passes.

| Dimension | Weight | What earns points |
| :--- | :--- | :--- |
| **Hook strength** | 15 | First frame and first words create an immediate claim, question, or number; speech starts within $0.15\text{s}$; no throat-clearing |
| **Standalone comprehension** | 15 | A viewer with zero parent-VOD context understands the premise, subject, and stakes |
| **Narrative / payoff quality** | 20 | Complete arc: tension, development, resolution. The ending lands and is not truncated. The story is worth the runtime |
| **Visual relevance and progression** | 15 | Every visual change explains or advances the story; layout suits the source archetype; no decorative split-screen on a source that does not need it |
| **Mobile framing** | 10 | Subject readable, headroom correct, no UI clutter, no cut-off subject, captions clear of face |
| **Caption accuracy and readability** | 10 | Verbatim, well-chunked, readable on a phone, emphasis supports meaning |
| **Pacing and information density** | 10 | No dead air, meaningful visual event every 1.5–3.5s, runtime efficient for the story |
| **Originality and audience fit** | 5 | The edit has a distinct angle and fits the channel/campaign audience |

### Thresholds
- $\ge 85$: strong publish candidate.
- $70 - 84$: publishable after addressing the weakest dimension.
- $55 - 69$: `EDITORIAL_HOLD`; rework hook, story, or visuals.
- $< 55$: reject the edit; choose a different moment.

### Calibration Warning
These scores prioritize work. They are not calibrated probabilities of virality. Actual campaign metrics from [performance-feedback.md](../subskills/performance-feedback.md) are the authority for format, hook, runtime, and treatment decisions.

---

## 3. Dimension Scoring Anchors

### Hook Strength (15)
- **15**: First frame contains the strongest visual or number; speech starts within $0.15\text{s}$; the claim is legible without setup.
- **10**: Speech starts within $0.4\text{s}$; hook requires mild context.
- **5**: Slow intro or definitional opening.
- **0**: Dead air $> 0.8\text{s}$ or no hook.

### Standalone Comprehension (15)
- **15**: No unresolved references; names and stakes are clear from the cut.
- **10**: One minor unresolved pronoun or reference.
- **5**: Requires parent-stream context to follow.
- **0**: Incomprehensible without external context.

### Narrative / Payoff (20)
- **20**: Clear tension, meaningful development, satisfying terminal payoff; setup compressed rather than payoff cut.
- **15**: Complete but slightly rushed or uneven.
- **10**: Abrupt or unresolved ending.
- **0**: No arc or clipped mid-thought.

### Visual Relevance and Progression (15)
- **15**: Layout follows the source archetype; each visual beat maps to the spoken beat; progressive diagram or scene tracking where appropriate; no filler split-screen.
- **10**: Mostly relevant, one gratuitous or static stretch.
- **5**: Generic treatment applied to a source that does not fit it.
- **0**: Visuals obscure or contradict the story.

### Mobile Framing (10)
- **10**: Subject clear, face unobstructed, no clutter, labels readable.
- **7**: Minor margin or clutter issue.
- **0**: Cut-off subject or unreadable content.

### Caption Accuracy and Readability (10)
- **10**: Verbatim, natural 3–5 word chunks, emphasis supports meaning, no collisions.
- **7**: Legible but staccato or one weak cue.
- **0**: Wrong words, dropped negation, or collisions.

### Pacing and Information Density (10)
- **10**: No dead air; meaningful visual event every 1.5–3.5s; runtime matched to story.
- **7**: One static stretch or slightly loose pacing.
- **0**: Frozen visuals, dead air, or runtime padded far beyond the story.

### Originality and Audience Fit (5)
- **5**: Distinct angle, appropriate for the channel and campaign audience.
- **3**: Competent but generic.
- **0**: Duplicative of an existing edit or wrong audience.

---

## 4. Auto-Fail Flags (Production Gate)

Any of these is a hard failure:

1. `DEBUG_OVERLAY_VISIBLE`
2. `CURSOR_VISIBLE`
3. `HAS_BURNT_SUBTITLES`
4. `BLURRY_FOOTAGE` (Laplacian variance $< 65.0$)
5. `CAPTION_AUDIO_MISMATCH`
6. `DANGLING_END`
7. `FILLER_COLD_OPEN`
8. `CROPPED_DIAGRAM_OR_ACTION`
9. `UNREADABLE_MOBILE_TEXT`
10. `FACE_OCCLUSION`
11. `SOURCE_TEXT_COLLISION`
12. `THUMBNAIL_DUPLICATE_OR_OCCLUDED`
13. `CAMPAIGN_RULE_VIOLATION`
14. `RIGHTS_UNCLEAR`
15. `AUDIO_OUT_OF_SPEC`
16. `AV_SYNC_DRIFT`

---

## 5. Scoring Record

Each evaluated candidate stores:

```json
{
  "clip_id": "string",
  "production_gate": "PASS | REJECTED_RENDER | HUMAN_REVIEW",
  "critical_failures": [],
  "editorial": {
    "hook": 0,
    "standalone_comprehension": 0,
    "narrative_payoff": 0,
    "visual_relevance": 0,
    "mobile_framing": 0,
    "captions": 0,
    "pacing_density": 0,
    "originality_fit": 0,
    "total": 0
  },
  "format": {
    "visual_archetype": "string",
    "narrative_archetype": "string",
    "editing_treatment": "string",
    "layout_mode": "string"
  },
  "runtime_seconds": 0.0,
  "campaign_id": "string",
  "metrics_hook": null
}
```

Real performance metrics are joined later by [performance-feedback.md](../subskills/performance-feedback.md) using `clip_id`.

---

## v2.1 Gate Separation

The 100-point editorial score is secondary. It cannot compensate for a failed gate.

| Gate | Verdict | Evidence |
| :--- | :--- | :--- |
| Technical | `TECHNICAL_PASS` | Probe, loudness, true peak, black/freeze, codec, resolution |
| Editorial | `EDITORIAL_PASS` | Treatment conformance, vision review, frame utility, thumbnail |
| Campaign | `CAMPAIGN_PASS` | Duration, rights, disclosures, account, hashtags, content |
| Approval | `READY_FOR_APPROVAL` | All three pass; human approval still required |

Critical failures that force `REJECTED_RENDER` regardless of score:

- `TREATMENT_NOT_IMPLEMENTED`
- `MISSING_FACE` on an active-speaker beat
- `LOW_FRAME_UTILITY` on a setup or reveal beat
- Thumbnail face/eye overlap or secondary text layer
- Campaign duration or rights violation
- Debug overlay, cursor, or accidental crop
