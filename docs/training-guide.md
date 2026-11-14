# EditPolicy training guide

## Purpose

Train a small editing-action ranker from structured trajectories. Muse Spark 1.3 Contributor remains the sole model-based critic. The LightGBM model is not a video critic: it ranks typed actions from numeric state/action features and must not generate semantic judgments or natural-language reviews.

## Training unit

One `query_id` represents one current video state. Each row represents one candidate editing action available from that state. All candidates for the same query share the same `query_id` and should have a relevance label:

- `4`: human-selected best action / verified strong improvement;
- `3`: clearly beneficial action;
- `2`: neutral or small improvement;
- `1`: weak improvement or risky/low-value action;
- `0`: rejected, harmful, or `NO_OP` when an alternative is clearly better.

Use `NO_OP` as a candidate in every state. If no action is worthwhile, human reviewers can label it as best.

## Label provenance

The script trains on `human_preference` and `verified_outcome` by default. `model_weak_label` rows are excluded. Only use `--include-weak-labels` for experiments, and never mix those rows with human labels without recording that choice in the model card.

A `verified_outcome` requires a rendered before/after pair plus independent deterministic measurements and explicit reviewer confirmation. Muse's own action recommendation is not an observed outcome. Do not let a model validate its own suggestion and then treat that as ground truth.

## Feature design

Use bounded, normalized numeric features. Good examples:

- state composition: subject area ratio, headroom ratio, face occlusion ratio;
- diagram: ROI clipped-edge ratio, OCR label legibility, node visibility ratio;
- narrative: beat confidence, object-to-narration alignment confidence, payoff coverage ratio;
- captions: caption-object overlap ratio, subtitle safe-zone occupancy;
- editing action: action family one-hot fields, zoom delta, pan delta, panel-ratio delta, duration delta, expected render cost, action reversibility;
- context: source archetype one-hot, narrative archetype one-hot, campaign duration slack.

Do not put raw creator IDs, source URLs, output hashes, or post-publication view counts into model features. Keep identifiers for grouping and audit only. Normalize all ratios to [0,1]; clamp invalid values and track missingness explicitly.

## Data format

JSONL: one record per candidate action, validated against `schemas/trajectory.schema.json`. A state with four candidate actions should have four rows with the same `query_id` and different `action_id` values.

## Train

```bash
python scripts/train_edit_policy.py \
  --input training/trajectories.jsonl \
  --out models/edit-policy-lgbm.txt \
  --model-card models/edit-policy-lgbm.model-card.json
```

Requirements:

```bash
python -m pip install lightgbm scikit-learn joblib
```

The script splits by `video_id`, not by row, to reduce leakage. It reports NDCG@3 on held-out videos. Use many distinct creators and source videos; do not tune against only Lex 688, Theo 37 and Veritasium 794.

## Promotion criteria

Promote a new ranker only if:
- held-out NDCG improves over the baseline;
- its top-ranked action is accepted more often by human reviewers;
- the no-op rate is sensible and the model does not over-edit;
- critical technical/campaign gates never regress;
- each source archetype has enough validation examples;
- results are reproducible from the model card and dataset hashes.

Keep the previous model version for rollback. Never retrain or deploy automatically on a single batch.

## Rank actions at inference time

Prepare candidate action rows as JSONL with `query_id`, `action_id`, and a numeric `features` object using the same feature names as the model card. Then run:

```bash
python scripts/rank_edit_actions.py \
  --model models/edit-policy-lgbm.txt \
  --model-card models/edit-policy-lgbm.model-card.json \
  --candidates candidate-actions.jsonl \
  --out ranked-actions.json
```

The output score is a relative ranking score, not a probability, predicted view count, or calibrated quality score. The renderer must still validate action preconditions and hard constraints before execution.
