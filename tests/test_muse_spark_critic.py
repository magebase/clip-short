from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.muse_spark_critic as critic


class FakeFile:
    id = "file_test"


class FakeUsage:
    def model_dump(self):
        return {"input_tokens": 10, "output_tokens": 20}


class FakeResponse:
    id = "resp_test"
    usage = FakeUsage()

    def __init__(self, text: str):
        self.output_text = text


CRITIQUE = {
    "summary": "The rendering is coherent but one diagram label is clipped.",
    "findings": [
        {"timestamp_sec": 12.5, "severity": "MAJOR", "category": "diagram", "evidence": "Label at right edge", "explanation": "The harness label is cut by the crop."}
    ],
    "actions": [
        {"action_id": "a1", "action_type": "diagram_reframe", "params": {"dx": -0.04}, "expected_effect": "Show the full node", "risk": "Slightly smaller labels"}
    ],
    "overall": {"decision": "RENDER_REVISION", "editorial_score": 78, "rationale": "Fix the clipped node before approval."},
}

COMPARISON = {
    "ranking": ["candidate_2", "candidate_1", "candidate_3"],
    "rationale": "Candidate 2 keeps the full diagram and speaker in frame.",
    "findings": [{"label": "candidate_1", "issue": "Clipped node", "evidence": "Right edge at 12.5s", "severity": "MAJOR"}],
}


class FakeFiles:
    def create(self, file, purpose):
        return FakeFile()


class FakeResponses:
    def __init__(self, payload):
        self.payload = payload

    def create(self, **kwargs):
        self.last = kwargs
        return FakeResponse(json.dumps(self.payload))


class FakeOpenAI:
    payload = CRITIQUE

    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.files = FakeFiles()
        self.responses = FakeResponses(self.payload)


class CriticTests(unittest.TestCase):
    def setUp(self):
        FakeOpenAI.payload = CRITIQUE
        self.tmp = tempfile.TemporaryDirectory()
        self.video = Path(self.tmp.name) / "clip.mp4"
        self.video.write_bytes(b"fake-mp4-bytes")
        self.env = patch.dict(os.environ, {"MODEL_API_KEY": "test-key", "CLIP_SHORT_ALLOW_CONTRIBUTOR_DATA_USE": "1"}, clear=False)
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def test_lock_is_single_model_no_fallback(self):
        lock = critic.load_lock()
        self.assertEqual(lock["model_id"], "muse-spark-1.3-contributor")
        self.assertEqual(lock["base_url"], "https://api.meta.ai/v1")
        self.assertFalse(lock["fallback"])
        self.assertFalse(lock["ensembles"])

    def test_consent_is_required(self):
        with patch.dict(os.environ, {"CLIP_SHORT_ALLOW_CONTRIBUTOR_DATA_USE": ""}):
            with self.assertRaises(critic.CriticConfigurationError):
                critic.require_consent(critic.load_lock())

    def test_lower_effort_requires_explicit_acknowledgement(self):
        lock = critic.load_lock()
        with self.assertRaises(critic.CriticPolicyViolation):
            critic.resolve_effort(lock, "high", False)
        self.assertEqual(critic.resolve_effort(lock, "high", True), "high")
        self.assertEqual(critic.resolve_effort(lock, "max", False), "max")

    def test_critique_uses_locked_model_and_validates_schema(self):
        args = type("Args", (), {"video": str(self.video), "transcript": None, "treatment": None, "campaign": None, "effort": "max", "accept_lower_effort": False, "file_purpose": "assistants", "out": None})()
        with patch.object(critic, "OpenAI", FakeOpenAI):
            result = critic.critique(args)
        self.assertEqual(result["record"]["model"], "muse-spark-1.3-contributor")
        self.assertEqual(result["record"]["confirmed_effort"], "max")
        self.assertFalse(result["record"]["fallback_used"])
        self.assertEqual(result["critique"]["overall"]["decision"], "RENDER_REVISION")


    def test_probe_uses_same_locked_model(self):
        args = type("Args", (), {"video": None, "effort": "max", "accept_lower_effort": False, "file_purpose": "assistants", "out": None})()
        with patch.object(critic, "OpenAI", FakeOpenAI):
            result = critic.probe(args)
        self.assertEqual(result["record"]["model"], "muse-spark-1.3-contributor")
        self.assertEqual(result["record"]["confirmed_effort"], "max")
        self.assertFalse(result["record"]["fallback_used"])

    def test_compare_randomizes_labels_and_keeps_mapping(self):
        second = Path(self.tmp.name) / "clip2.mp4"
        second.write_bytes(b"fake-mp4-two")
        args = type("Args", (), {"baseline": str(self.video), "candidate": [str(self.video), str(second)], "effort": "max", "accept_lower_effort": False, "file_purpose": "assistants", "out": None})()
        with patch.object(critic, "OpenAI", FakeOpenAI):
            FakeOpenAI.payload = COMPARISON
            result = critic.compare(args)
        self.assertEqual(result["record"]["model"], "muse-spark-1.3-contributor")
        self.assertEqual(len(result["label_mapping"]), 3)
        self.assertEqual(sorted(result["comparison"]["ranking"]), sorted(result["label_mapping"].values()))

    def test_probe_still_requires_explicit_effort_ack(self):
        args = type("Args", (), {"video": None, "effort": "low", "accept_lower_effort": False, "file_purpose": "assistants", "out": None})()
        with patch.object(critic, "OpenAI", FakeOpenAI):
            with self.assertRaises(critic.CriticPolicyViolation):
                critic.probe(args)


if __name__ == "__main__":
    unittest.main()
