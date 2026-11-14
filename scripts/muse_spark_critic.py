#!/usr/bin/env python3
"""Sole model-based critic: Meta Muse Spark 1.3 Contributor.

No fallback, no ensemble, no alternate model. The model lock is authoritative.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import random
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "model" / "critic.lock.json"
CRITIQUE_SCHEMA = ROOT / "schemas" / "critique.schema.json"
COMPARISON_SCHEMA = ROOT / "schemas" / "comparison.schema.json"

try:
    from jsonschema import validate as jsonschema_validate
except ImportError:  # pragma: no cover
    jsonschema_validate = None

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


class CriticConfigurationError(RuntimeError):
    pass


class CriticPolicyViolation(RuntimeError):
    pass


def load_lock() -> Dict[str, Any]:
    return json.loads(LOCK_PATH.read_text())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def require_consent(lock: Dict[str, Any]) -> None:
    if os.environ.get(lock["consent_env"]) != "1":
        raise CriticConfigurationError(
            f"Contributor data-use consent required: export {lock['consent_env']}=1 after confirming rights."
        )


def resolve_effort(lock: Dict[str, Any], effort: str, accept_lower: bool) -> str:
    requested = lock["requested_effort"]
    if effort != requested and not accept_lower:
        raise CriticPolicyViolation(
            f"Requested effort {effort!r} differs from the locked {requested!r}. "
            "Production critique requires max; pass --accept-lower-effort only for an explicit experiment."
        )
    return effort


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


def load_json(value: str) -> Dict[str, Any]:
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text())
    return json.loads(value)


def extract_text(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text
    chunks: List[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            candidate = getattr(content, "text", None)
            if candidate:
                chunks.append(candidate)
    return "\n".join(chunks).strip()


def parse_json_response(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise CriticPolicyViolation("Critic returned no JSON object.")
    return json.loads(text[start:end + 1])


def validate_schema(payload: Dict[str, Any], schema_path: Path) -> None:
    if jsonschema_validate is None:
        raise CriticConfigurationError("jsonschema is required: pip install jsonschema")
    jsonschema_validate(payload, json.loads(schema_path.read_text()))


def client_for(lock: Dict[str, Any]) -> Any:
    if OpenAI is None:
        raise CriticConfigurationError("openai>=1.60 is required: pip install 'openai>=1.60'")
    key = os.environ.get(lock["api_key_env"])
    if not key:
        raise CriticConfigurationError(f"Missing {lock['api_key_env']}.")
    return OpenAI(api_key=key, base_url=lock["base_url"])


def upload_file(client: Any, path: Path, purpose: str = "assistants") -> str:
    with path.open("rb") as handle:
        uploaded = client.files.create(file=handle, purpose=purpose)
    return getattr(uploaded, "id", None) or uploaded["id"]


def response_call(client: Any, lock: Dict[str, Any], content: List[Dict[str, Any]], effort: str) -> Any:
    return client.responses.create(
        model=lock["model_id"],
        input=[{"role": "user", "content": content}],
        reasoning={"effort": effort},
    )


def usage_payload(response: Any) -> Dict[str, Any]:
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        return usage.model_dump()
    return dict(usage)


def base_record(lock: Dict[str, Any], effort: str, video_hash: str, video_path: Path, file_id: Optional[str]) -> Dict[str, Any]:
    return {
        "model": lock["model_id"],
        "model_display_name": lock["display_name"],
        "provider": lock["provider"],
        "base_url": lock["base_url"],
        "api_surface": lock["api_surface"],
        "requested_effort": lock["requested_effort"],
        "confirmed_effort": effort,
        "effort_override": effort != lock["requested_effort"],
        "fallback_used": False,
        "ensemble_used": False,
        "prompt_version": lock["prompt_version"],
        "critique_schema_version": lock["critique_schema_version"],
        "caller_git_sha": git_sha(),
        "lock_sha256": sha256_file(LOCK_PATH),
        "video_sha256": video_hash,
        "video_path": str(video_path),
        "file_id": file_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def critic_prompt(transcript: str, treatment: Dict[str, Any], campaign: Dict[str, Any], mode: str) -> str:
    schema = json.loads(CRITIQUE_SCHEMA.read_text())
    return (
        "You are Muse Spark 1.3 Contributor, the sole model-based video critic for clip-short v2.4. "
        "Inspect the attached native video. Be evidence-grounded and timestamp-specific. "
        "Do not invent objects, speakers, or narration. Do not praise without evidence. "
        "Distinguish technical validity from editorial quality. "
        "Return ONLY JSON matching this schema:\n"
        + json.dumps(schema)
        + "\n\nMode: " + mode
        + "\nCampaign rules:\n" + json.dumps(campaign)
        + "\nTreatment spec:\n" + json.dumps(treatment)
        + "\nTranscript (may be partial):\n" + transcript[:120000]
    )


def persist_record(record: Dict[str, Any], critique: Dict[str, Any], video: Path) -> Optional[str]:
    worker = os.environ.get("CLIP_SHORT_CRITIC_WORKER_URL")
    token = os.environ.get("CLIP_SHORT_CRITIC_TOKEN")
    if not worker or not token:
        return None
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    asset_key = f"critiques/{record['video_sha256'][:16]}/{video.name}"
    put = urllib.request.Request(
        f"{worker.rstrip('/')}/api/assets/{asset_key}",
        data=video.read_bytes(), method="PUT",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "video/mp4"},
    )
    urllib.request.urlopen(put, timeout=120).read()
    payload = {"record": record, "critique": critique, "r2_key": asset_key}
    req = urllib.request.Request(
        f"{worker.rstrip('/')}/api/critiques",
        data=json.dumps(payload).encode(), method="POST", headers=headers,
    )
    body = json.loads(urllib.request.urlopen(req, timeout=60).read())
    return body.get("id")


def critique(args: argparse.Namespace) -> Dict[str, Any]:
    lock = load_lock()
    require_consent(lock)
    effort = resolve_effort(lock, args.effort, args.accept_lower_effort)
    video = Path(args.video)
    if not video.exists():
        raise FileNotFoundError(video)
    client = client_for(lock)
    file_id = upload_file(client, video, args.file_purpose)
    transcript = Path(args.transcript).read_text(errors="ignore") if args.transcript else ""
    treatment = load_json(args.treatment) if args.treatment else {}
    campaign = load_json(args.campaign) if args.campaign else {}
    content = [
        {"type": "input_text", "text": critic_prompt(transcript, treatment, campaign, "critique")},
        {"type": "input_file", "file_id": file_id},
    ]
    started = time.time()
    response = response_call(client, lock, content, effort)
    critique_payload = parse_json_response(extract_text(response))
    validate_schema(critique_payload, CRITIQUE_SCHEMA)
    record = base_record(lock, effort, sha256_file(video), video, file_id)
    record.update({
        "request_id": getattr(response, "id", None),
        "latency_sec": round(time.time() - started, 3),
        "usage": usage_payload(response),
        "transcript_sha256": sha256_text(transcript) if transcript else None,
        "treatment_sha256": sha256_text(json.dumps(treatment, sort_keys=True)),
        "campaign_sha256": sha256_text(json.dumps(campaign, sort_keys=True)),
    })
    persisted = persist_record(record, critique_payload, video)
    output = {"record": record, "critique": critique_payload, "persisted_id": persisted}
    if args.out:
        Path(args.out).write_text(json.dumps(output, indent=2) + "\n")
    return output


def probe(args: argparse.Namespace) -> Dict[str, Any]:
    lock = load_lock()
    require_consent(lock)
    effort = resolve_effort(lock, args.effort, args.accept_lower_effort)
    client = client_for(lock)
    if args.video:
        file_id = upload_file(client, Path(args.video), args.file_purpose)
        content = [{"type": "input_text", "text": "Return compact JSON {\"ok\":true,\"video_seen\":true}."}, {"type": "input_file", "file_id": file_id}]
        video_hash = sha256_file(Path(args.video))
    else:
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII=")
        image_b64 = base64.b64encode(png).decode()
        content = [
            {"type": "input_text", "text": "Return compact JSON {\"ok\":true,\"image_seen\":true}."},
            {"type": "input_image", "image_url": f"data:image/png;base64,{image_b64}"},
        ]
        video_hash = sha256_text(image_b64)
    started = time.time()
    response = response_call(client, lock, content, effort)
    text = extract_text(response)
    record = base_record(lock, effort, video_hash, Path(args.video or "probe-image.png"), None)
    record.update({"request_id": getattr(response, "id", None), "latency_sec": round(time.time() - started, 3), "usage": usage_payload(response)})
    output = {"record": record, "probe_text": text}
    if args.out:
        Path(args.out).write_text(json.dumps(output, indent=2) + "\n")
    return output


def compare(args: argparse.Namespace) -> Dict[str, Any]:
    lock = load_lock()
    require_consent(lock)
    effort = resolve_effort(lock, args.effort, args.accept_lower_effort)
    client = client_for(lock)
    paths = [Path(args.baseline)] + [Path(item) for item in args.candidate]
    labels = [f"candidate_{index + 1}" for index in range(len(paths))]
    shuffled = labels[:]
    random.SystemRandom().shuffle(shuffled)
    mapping = dict(zip(labels, shuffled))
    content = [{
        "type": "input_text",
        "text": (
            "Compare these rendered clips against the baseline. Treat labels as anonymous; do not infer intent. "
            "Return JSON with fields ranking (best to worst), rationale, and findings. Ranking must use these labels: "
            + json.dumps(shuffled)
        ),
    }]
    for label, path in zip(shuffled, paths):
        content.append({"type": "input_text", "text": f"Label {label}"})
        content.append({"type": "input_file", "file_id": upload_file(client, path, args.file_purpose)})
    started = time.time()
    response = response_call(client, lock, content, effort)
    payload = parse_json_response(extract_text(response))
    validate_schema(payload, COMPARISON_SCHEMA)
    record = base_record(lock, effort, sha256_file(paths[0]), paths[0], None)
    record.update({"request_id": getattr(response, "id", None), "latency_sec": round(time.time() - started, 3), "usage": usage_payload(response), "label_mapping": mapping})
    output = {"record": record, "comparison": payload, "label_mapping": mapping}
    if args.out:
        Path(args.out).write_text(json.dumps(output, indent=2) + "\n")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--effort", default="max")
        p.add_argument("--accept-lower-effort", action="store_true")
        p.add_argument("--file-purpose", default="assistants")
        p.add_argument("--out")

    c = sub.add_parser("critique")
    c.add_argument("--video", required=True); c.add_argument("--transcript"); c.add_argument("--treatment"); c.add_argument("--campaign")
    common(c); c.set_defaults(func=critique)

    p = sub.add_parser("probe")
    p.add_argument("--video")
    common(p); p.set_defaults(func=probe)

    m = sub.add_parser("compare")
    m.add_argument("--baseline", required=True); m.add_argument("--candidate", action="append", required=True)
    common(m); m.set_defaults(func=compare)

    args = parser.parse_args()
    result = args.func(args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
