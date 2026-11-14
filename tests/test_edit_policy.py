from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import validate

from scripts.rank_edit_actions import rank_rows
from scripts.train_edit_policy import grouped

ROOT = Path(__file__).resolve().parents[1]


class EditPolicyTests(unittest.TestCase):
    def test_trajectory_schema_accepts_valid_row(self):
        schema = json.loads((ROOT / "schemas/trajectory.schema.json").read_text())
        row = {
            "video_id": "v1", "query_id": "q1", "action_id": "a1",
            "features": {"zoom_delta": 0.1, "subject_area": 0.4},
            "label": 3, "label_provenance": "human_preference", "created_at": "2026-11-14T00:00:00Z",
        }
        validate(row, schema)

    def test_grouped_preserves_query_order_and_features(self):
        rows = [
            {"query_id": "q1", "features": {"b": 2.0, "a": 1.0}, "label": 4},
            {"query_id": "q1", "features": {"b": 1.0, "a": 0.0}, "label": 1},
            {"query_id": "q2", "features": {"b": 0.5, "a": 0.2}, "label": 0},
        ]
        names, X, y, groups = grouped(rows)
        self.assertEqual(names, ["a", "b"])
        self.assertEqual(groups, [2, 1])
        self.assertEqual(X, [[1.0, 2.0], [0.0, 1.0], [0.2, 0.5]])
        self.assertEqual(y, [4, 1, 0])

    def test_rank_rows_sorts_by_score_per_query(self):
        rows = [
            {"query_id": "q1", "action_id": "a"},
            {"query_id": "q1", "action_id": "b"},
            {"query_id": "q2", "action_id": "c"},
        ]
        ranked = rank_rows(rows, [0.2, 0.9, 0.5])
        self.assertEqual([(r["query_id"], r["action_id"], r["rank"]) for r in ranked], [("q1", "b", 1), ("q1", "a", 2), ("q2", "c", 1)])


if __name__ == "__main__":
    unittest.main()
