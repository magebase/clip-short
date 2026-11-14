#!/usr/bin/env python3
"""Train the LightGBM LambdaRank edit-action selector. Not a critic."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import lightgbm as lgb
    import numpy as np
except ImportError:  # pragma: no cover
    lgb = None
    np = None

from jsonschema import validate


def read_rows(path: Path, include_weak: bool) -> List[Dict[str, Any]]:
    schema = json.loads(Path(__file__).parents[1].joinpath("schemas/trajectory.schema.json").read_text())
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        validate(row, schema)
        if row["label_provenance"] == "model_weak_label" and not include_weak:
            continue
        rows.append(row)
    return rows


def split_by_video(rows: List[Dict[str, Any]], test_ratio: float = 0.2) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    videos = sorted({row["video_id"] for row in rows})
    if len(videos) < 2:
        raise ValueError("Need at least two video_id groups for a held-out split.")
    cut = max(1, int(round(len(videos) * (1.0 - test_ratio))))
    train_videos = set(videos[:cut])
    return [row for row in rows if row["video_id"] in train_videos], [row for row in rows if row["video_id"] not in train_videos]


def grouped(rows: List[Dict[str, Any]]) -> Tuple[List[str], List[List[float]], List[int], List[int]]:
    by_query: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_query[row["query_id"]].append(row)
    feature_names = sorted(rows[0]["features"].keys())
    X, y, groups = [], [], []
    for query_id in sorted(by_query):
        candidates = by_query[query_id]
        groups.append(len(candidates))
        for row in candidates:
            X.append([float(row["features"].get(name, 0.0)) for name in feature_names])
            y.append(int(row["label"]))
    return feature_names, X, y, groups


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model-card", type=Path, required=True)
    parser.add_argument("--include-weak-labels", action="store_true")
    parser.add_argument("--test-ratio", type=float, default=0.2)
    args = parser.parse_args()
    if lgb is None:
        raise SystemExit("lightgbm is required: pip install lightgbm scikit-learn joblib")

    rows = read_rows(args.input, args.include_weak_labels)
    train_rows, test_rows = split_by_video(rows, args.test_ratio)
    feature_names, X_train, y_train, groups_train = grouped(train_rows)
    _, X_test, y_test, groups_test = grouped(test_rows)

    ranker = lgb.LGBMRanker(
        objective="lambdarank", metric="ndcg", eval_at=[3],
        n_estimators=300, learning_rate=0.05, num_leaves=31,
        min_child_samples=5, random_state=42,
    )
    ranker.fit(X_train, y_train, group=groups_train, eval_set=[(X_test, y_test)], eval_group=[groups_test])
    ndcg = ranker.best_score_["valid_0"]["ndcg@3"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    ranker.booster_.save_model(str(args.out))
    card = {
        "model_type": "lightgbm_lambdarank",
        "purpose": "edit_action_ranker_not_critic",
        "features": feature_names,
        "dataset_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "rows_train": len(train_rows), "rows_test": len(test_rows),
        "queries_train": len(groups_train), "queries_test": len(groups_test),
        "ndcg_at_3": float(ndcg),
        "include_weak_labels": bool(args.include_weak_labels),
        "test_video_ids": sorted({row["video_id"] for row in test_rows}),
        "created_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    }
    args.model_card.write_text(json.dumps(card, indent=2) + "\n")
    print(json.dumps(card, indent=2))


if __name__ == "__main__":
    main()
