#!/usr/bin/env python3
"""Rank typed edit actions with a trained LightGBM EditPolicy. Not a critic."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from jsonschema import validate


def load_candidates(path: Path) -> List[Dict[str, Any]]:
    schema = json.loads(Path(__file__).parents[1].joinpath("schemas/candidate-actions.schema.json").read_text())
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            validate(row, schema)
            rows.append(row)
    return rows


def rank_rows(rows: List[Dict[str, Any]], scores: List[float]) -> List[Dict[str, Any]]:
    by_query: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row, score in zip(rows, scores):
        item = dict(row); item["score"] = float(score)
        by_query[row["query_id"]].append(item)
    output = []
    for query_id in sorted(by_query):
        ranked = sorted(by_query[query_id], key=lambda item: item["score"], reverse=True)
        for position, item in enumerate(ranked, 1):
            item["rank"] = position
            output.append(item)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--model-card", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        import lightgbm as lgb
    except ImportError:
        raise SystemExit("lightgbm is required: pip install lightgbm")
    card = json.loads(args.model_card.read_text())
    rows = load_candidates(args.candidates)
    booster = lgb.Booster(model_file=str(args.model))
    features = [[float(row["features"].get(name, 0.0)) for name in card["features"]] for row in rows]
    scores = booster.predict(features)
    ranked = rank_rows(rows, list(scores))
    args.out.write_text(json.dumps({"model_card": str(args.model_card), "ranking": ranked}, indent=2) + "\n")
    print(json.dumps({"queries": len({row['query_id'] for row in rows}), "actions": len(rows)}))


if __name__ == "__main__":
    main()
