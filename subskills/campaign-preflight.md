# Subskill: Campaign Preflight & Compliance Validation

Campaign rules are inputs, not assumptions. Load the specific campaign configuration before selecting, editing, scoring, or packaging a clip. Missing or ambiguous rules fail closed to `HUMAN_REVIEW`.

---

## 1. Why This Exists

Different clipping campaigns define different duration limits, required sounds, required content, prohibited content, hashtags, mentions, audience rules, and account requirements. A house default can violate a campaign even when the render is technically perfect.

Preflight runs before creative work so the edit is built for the actual submission target.

---

## 2. Campaign Configuration Schema

```yaml
campaign:
  platform: youtube            # youtube | tiktok | instagram | facebook
  campaign_id: REQUIRED
  source_url: REQUIRED
  approved_source: true        # must be true; false => HUMAN_REVIEW

  duration:
    min_seconds: null          # null means "not specified"; see fail-closed rules
    max_seconds: null

  requirements:
    required_hashtags: []
    required_mentions: []
    required_sound: null
    required_content: []
    prohibited_content: []
    audience_requirements: []

  submission:
    public_post_required: true
    linked_account_required: true
    human_approval_required: true
    bounty_tag: null

  quality:
    require_unique_edit: true
    require_post_render_qa: true
    require_caption_verification: true
```

### Extended Fields
```yaml
  rights:
    license: "fair_use_commentary"   # license | fair_use_commentary | permission | public_domain
    attribution_required: true
    attribution_text: null

  disclosure:
    required: false
    text: null
    placement: "description"

  format:
    aspect_ratio: "9:16"
    resolution: "1080x1920"
    max_file_size_mb: null

  tracking:
    platform_campaign_id: null
    submission_url_required: true
    metrics_source: null
```

---

## 3. Loading and Validation

```python
REQUIRED_FIELDS = [
    "platform",
    "campaign_id",
    "source_url",
    "approved_source",
    "submission.human_approval_required",
]

def load_campaign(path: str) -> dict:
    cfg = parse_yaml(path)

    missing = [f for f in REQUIRED_FIELDS if resolve(cfg, f) in (None, "", [])]
    if missing:
        return fail_closed("CAMPAIGN_RULES_MISSING", missing)

    if cfg["campaign"]["approved_source"] is not True:
        return fail_closed("SOURCE_NOT_APPROVED")

    if not cfg["campaign"]["submission"]["human_approval_required"]:
        return fail_closed("HUMAN_APPROVAL_MUST_BE_REQUIRED")

    return cfg
```

### Fail-Closed Rules
- Missing `campaign_id`, `platform`, or `source_url` $\to$ `HUMAN_REVIEW`.
- `approved_source != true` $\to$ `HUMAN_REVIEW`.
- Both `min_seconds` and `max_seconds` are `null` $\to$ use house defaults but record that the campaign duration is unspecified.
- A duration window that cannot contain a complete thought $\to$ `HUMAN_REVIEW`; do not cut the payoff.
- Required sound unavailable $\to$ `HUMAN_REVIEW`; never substitute silently.
- Required content absent from the source $\to$ choose another moment or `HUMAN_REVIEW`; never fake it in metadata.
- Prohibited content present in audio or visuals $\to$ reject the candidate.
- Rights unclear $\to$ `HUMAN_REVIEW`.
- Any rule that cannot be verified programmatically $\to$ `HUMAN_REVIEW` with the exact unresolved field.

---

## 4. Preflight Checklist

| Check | Pass condition |
| :--- | :--- |
| Campaign identity | `campaign_id`, platform, and source URL present |
| Source approval | `approved_source: true` |
| Duration | Campaign window loaded and feasible for a complete thought |
| Required sound | Available and licensed, or explicitly not required |
| Required content | Verified present in the selected transcript/visuals |
| Prohibited content | Verified absent |
| Hashtags / mentions | Exact strings loaded into packaging |
| Audience rules | Understood; may require content screening |
| Account rules | Linked account and public-post requirements recorded |
| Disclosure | Required text and placement recorded |
| Rights | License or fair-use basis recorded; attribution prepared |
| Quality requirements | Unique edit, post-render QA, caption verification enabled |
| Human approval | Required and enforced |

---

## 5. Submission Package

The preflight output is a frozen submission package containing:

```json
{
  "campaign_id": "string",
  "source_url": "string",
  "source_approved": true,
  "duration_rule": {"min_seconds": null, "max_seconds": null, "source": "campaign|house"},
  "required_hashtags": [],
  "required_mentions": [],
  "required_sound": null,
  "required_content": [],
  "prohibited_content": [],
  "rights": {"license": "string", "attribution_text": "string"},
  "disclosure": {"required": false, "text": null},
  "submission": {
    "public_post_required": true,
    "linked_account_required": true,
    "human_approval_required": true,
    "bounty_tag": null
  },
  "quality": {
    "require_unique_edit": true,
    "require_post_render_qa": true,
    "require_caption_verification": true
  },
  "validation": {"status": "PASS|HUMAN_REVIEW", "unresolved": []}
}
```

The package is immutable for the life of the edit. Any campaign change invalidates the package and requires a new preflight.

---

## 6. Compliance Validation Before Release

Re-check the final package against the exported deliverable:

1. Runtime inside the campaign window.
2. Required hashtags and mentions present exactly.
3. Required sound used, or absent if not required.
4. Required content visibly or audibly present in the cut.
5. Prohibited content absent from audio and visuals.
6. Disclosure text present at the required placement.
7. Attribution present when required.
8. Aspect ratio, resolution, and file-size limits satisfied.
9. Public-post and linked-account requirements acknowledged.
10. Human approval recorded.

Any failed row blocks `READY_FOR_APPROVAL`. Do not override campaign rules to publish a better story; choose a compliant story instead.
