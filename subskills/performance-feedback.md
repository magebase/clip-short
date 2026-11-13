# Subskill: Performance Feedback & Format Learning

Editorial scoring prioritizes work. Actual campaign performance decides what the system should make next. Record outcomes against every submitted clip and learn per campaign, format, hook, and runtime without overfitting.

---

## 1. Why This Exists

A preset used by a popular streamer is not proof of effectiveness. Originality matters, campaigns differ in audience and economics, and a hook that works for gaming can fail for documentary narration. The feedback loop replaces inherited assumptions with measured results.

---

## 2. Metrics to Record

Record only what the platform or campaign actually reports, with the retrieval timestamp.

| Metric | Field | Why it matters |
| :--- | :--- | :--- |
| Impressions / views | `views` | Reach |
| Viewed vs swiped away | `viewed_rate` | Hook effectiveness |
| Average view duration | `avg_view_duration_sec` | Actual viewing depth |
| Average percentage viewed | `avg_percent_viewed` | Runtime efficiency |
| Completion rate | `completion_rate` | Narrative payoff |
| Engaged views | `engaged_views` | Platform-weighted interest |
| Shares per 1,000 views | `shares_per_1k` | Resonance |
| Comments per 1,000 views | `comments_per_1k` | Discussion potential |
| Followers gained | `followers_gained` | Audience conversion |
| Confirmed campaign views | `confirmed_campaign_views` | Economic performance |
| Payout / earnings | `payout` | Campaign outcome, when reported |
| Submission status | `submission_status` | Rejected, pending, accepted |

Do not invent metrics. If a platform does not report a field, store `null`.

---

## 3. Feedback Record Schema

```json
{
  "clip_id": "string",
  "campaign_id": "string",
  "platform": "youtube",
  "published_url": "string",
  "published_at": "2026-11-13T18:00:00Z",
  "retrieved_at": "2026-11-15T00:00:00Z",
  "metrics": {
    "views": null,
    "viewed_rate": null,
    "avg_view_duration_sec": null,
    "avg_percent_viewed": null,
    "completion_rate": null,
    "engaged_views": null,
    "shares_per_1k": null,
    "comments_per_1k": null,
    "followers_gained": null,
    "confirmed_campaign_views": null,
    "payout": null
  },
  "format": {
    "visual_archetype": "string",
    "narrative_archetype": "string",
    "editing_treatment": "string",
    "layout_mode": "string"
  },
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
  "runtime_seconds": 0.0,
  "hook_type": "string",
  "submission_status": "string"
}
```

Store one record per clip per retrieval. Never overwrite history; append and keep the latest snapshot per timestamp.

---

## 4. Metric Maturity Windows

Metrics are immature early. Compare only at consistent ages:

- **1 hour**: hook signal only (viewed vs swiped).
- **24 hours**: short-form primary window.
- **7 days**: stable comparative window.
- **Campaign lag**: some campaigns update confirmed views and payout periodically, sometimes days later.

Do not conclude a format is bad from a 1-hour sample. Record `retrieved_at` and evaluate at the 7-day window unless the campaign specifies otherwise.

---

## 5. Learning Loop

### Per-Clip Diagnosis
| Pattern | Likely cause | Next action |
| :--- | :--- | :--- |
| High impressions, low viewed rate | Weak first frame or hook | Test stronger opening visual/number |
| High viewed rate, low completion | Setup too long, payoff weak or late | Compress setup; move payoff earlier |
| High completion, low shares | Low resonance or no quotable moment | Strengthen the payoff line or insight |
| Good metrics, low followers | No reason to return to the channel | Strengthen channel identity |
| Good views, low confirmed campaign views | Packaging or campaign mismatch | Re-check required content and tagging |
| Payout far below views | Wrong campaign or audience | Re-evaluate campaign fit |

### Format-Level Learning
Aggregate by campaign and format axes, never globally without splitting:

```
For each campaign:
  For each (visual_archetype, narrative_archetype, editing_treatment):
    compare median viewed_rate, completion_rate, shares_per_1k at 7 days
    require n >= 5 clips before treating a difference as a signal
    prefer the treatment with the best completion and resonance, not raw views
```

### Runtime Learning
- Compare completion rate and average percentage viewed within the campaign's allowed window.
- Do not assume shorter is always better; a complete story can outperform a truncated one.
- Test setup compression before reducing the payoff.

### Hook Learning
- Classify the first three seconds: number claim, question, contradiction, visual reveal, story cold open.
- Compare viewed rate per hook type per campaign and per audience.
- Require repeated evidence before changing a default.

---

## 6. Guardrails Against Overfitting

1. **Small samples are noise.** Require at least 5 comparable clips before changing a default, and prefer 15+.
2. **Campaign-specific.** Never generalize a winning format from one campaign to another without a test.
3. **Audience-specific.** Gaming, finance, history, and tech audiences differ.
4. **No clickbait ratchet.** Do not learn toward misleading hooks. Accuracy and originality remain hard constraints.
5. **No duplicate flooding.** Do not mass-produce the same edit to chase a metric; campaign and platform rules prohibit duplicate or low-effort submissions.
6. **Payout is not the only signal.** Community rules, rights, and audience trust are non-negotiable.
7. **Metrics gaps are not zero.** Missing data is `null`, never 0.

---

## 7. Reporting

Produce a periodic report per campaign:

- Top and bottom performers with format and runtime.
- Hook-type comparison at 7 days.
- Completion and resonance trends.
- Submission acceptance and payout status.
- Recommended next tests, with sample-size caveats.

Reports inform editorial defaults. They never automatically authorize publishing. Human approval remains mandatory.
