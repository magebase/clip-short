#!/usr/bin/env python3
"""Run the locked Muse Spark critic over a batch manifest."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--effort", default="max")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    jobs = json.loads(args.manifest.read_text())
    if not args.dry_run:
        if not os.environ.get("MODEL_API_KEY"):
            raise SystemExit("MODEL_API_KEY is not set")
        if os.environ.get("CLIP_SHORT_ALLOW_CONTRIBUTOR_DATA_USE") != "1":
            raise SystemExit("CLIP_SHORT_ALLOW_CONTRIBUTOR_DATA_USE=1 is required")
    results = []
    for job in jobs:
        out = args.out_dir / f"{job['id']}.critique.json"
        cmd = [
            sys.executable, str(ROOT / "scripts/muse_spark_critic.py"), "critique",
            "--video", job["video"], "--effort", args.effort, "--out", str(out),
        ]
        for key, flag in (("transcript", "--transcript"), ("treatment", "--treatment"), ("campaign", "--campaign")):
            if job.get(key):
                cmd += [flag, job[key]]
        print(" ".join(cmd), flush=True)
        if not args.dry_run:
            subprocess.run(cmd, check=True)
            payload = json.loads(out.read_text())
            results.append({"id": job["id"], "decision": payload["critique"]["overall"]["decision"], "out": str(out)})
    if results:
        (args.out_dir / "batch_summary.json").write_text(json.dumps(results, indent=2) + "\n")
        if any(item["decision"] != "PASS" for item in results):
            raise SystemExit(2)


if __name__ == "__main__":
    main()
