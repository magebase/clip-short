# Subskill: Autonomous Production Cadence & Human-Gated Distribution

Autonomous work means the daemon prepares, renders, and verifies candidates without a human at the keyboard. It does not mean it publishes them. Human approval and campaign compliance gate every release.

---

## 1. Design Principles

- **Unique edits only**: every submitted clip is a distinct edit, not a duplicated mass-produced output.
- **Human approval required**: publishing is a human action unless a campaign explicitly and lawfully authorizes otherwise; this skill never assumes authorization.
- **Campaign-aware**: duration, sound, required content, hashtags, and audience rules come from the loaded campaign config, not from defaults.
- **Fail closed**: missing rights, ambiguous rules, failed QA, or low confidence goes to `HUMAN_REVIEW`, never to `READY`.
- **No low-effort volume**: cadence cannot override quality or originality.

---

## 2. Autonomy Boundary

| Stage | Allowed autonomously | Blocked |
| :--- | :--- | :--- |
| Source discovery | Yes, within approved sources | Unapproved or unlicensed sources |
| Campaign preflight | Yes, with fail-closed | Inventing missing rules |
| Candidate selection | Yes, transcript-grounded | Fabricating claims |
| Editing and rendering | Yes | Publishing during render |
| Post-render QA | Yes, fail-closed | Waiving a failed gate |
| Packaging | Yes, five layers | Reusing one string across layers |
| Thumbnail | Yes, with verification | Duplicate or occluding text |
| Upload / publish | No, unless explicitly authorized by campaign and human | Bulk auto-distribution |
| Bounty / payment claims | No | Unsupported financial automation |

Uploading to social platforms must use official APIs only. No browser automation against social platforms.

---

## 3. Production Cadence

The cadence is a target, not a quota that justifies weak work.

```yaml
cadence:
  production_interval_minutes: 10
  max_candidates_per_cycle: 1
  min_editorial_score: 70
  require_unique_edit: true
  require_campaign_preflight: true
  require_post_render_qa: true
  require_caption_verification: true
  human_approval_before_publish: true
```

Each cycle:

1. Pick one approved source segment.
2. Run campaign preflight; stop on failure.
3. Classify the source along the three axes.
4. Cut with narrative-first boundaries.
5. Render with the correct layout and treatment.
6. Run the production gate on the exported MP4.
7. Only if the gate passes, run editorial scoring.
8. Build the five text layers and the verified thumbnail.
9. Place the candidate in the human approval queue.
10. Record the performance record linkage for the future submission.

If any step fails, write the failure reason and continue with the next candidate. Never retry the same failed render indefinitely.

---

## 4. Distribution Rules

- **Default**: no automatic publication.
- A campaign may require a public post on a linked account. Even then, the human submits or explicitly approves the submission.
- Duplicate submissions, near-identical reposts, and low-effort volumes are prohibited.
- Respect per-platform and per-account cadence limits.
- Space posts according to campaign and platform rules; do not burst.
- If an upload is rejected or the platform reports a limit, stop and hold as a local artifact; do not hammer the API.
- All uploads use official REST/Graph APIs with authorized tokens.

---

## 5. Campaign and Rights Preflight

Refuse to produce when:

- Campaign rules are missing or contradictory.
- Source is not approved.
- Rights are unclear.
- Required sound is unavailable.
- Required content is absent from the source.
- Prohibited content is present.
- The campaign duration cannot contain a complete thought.

Refusal produces a clear `HUMAN_REVIEW` record, not a silent skip.

---

## 6. Quality and Feedback

- Production gate failures reject the export regardless of editorial score.
- Editorial scores prioritize the human review queue.
- Actual performance metrics are recorded per clip and joined to format, runtime, and hook type in [performance-feedback.md](performance-feedback.md).
- Learned preferences never override accuracy, originality, rights, or campaign rules.

---

## 7. Approval Queue

Each candidate in the queue includes:

- Exported MP4 path.
- Contact sheet and QA report.
- Production gate verdict and any failures.
- Editorial score and dimension breakdown.
- Five text layers.
- Verified thumbnail.
- Campaign preflight package.
- Recommended publish window, if the campaign specifies one.
- Explicit `APPROVE` / `REJECT` human decision field.

Only a human `APPROVE` moves a candidate to submission. Rejection records the reason and feeds editorial learning.
