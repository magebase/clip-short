# Muse Spark invocation guide

## Environment

```bash
export MODEL_API_KEY="…"                    # Meta Model API key
export CLIP_SHORT_ALLOW_CONTRIBUTOR_DATA_USE=1
export CLIP_SHORT_CRITIC_WORKER_URL="https://clip-short-critic.<account>.workers.dev"  # optional D1/R2 persistence
export CLIP_SHORT_CRITIC_TOKEN="…"          # optional Worker bearer token
```

Contributor mode permits prompts, uploaded files, and responses to be used to improve Meta products. Enable it only when you have rights to upload the footage and accept the data-use terms.

## Probe

```bash
python scripts/muse_spark_critic.py probe --effort max
python scripts/muse_spark_critic.py probe --effort max --video test-short.mp4
```

The probe uses the same locked model and effort. It verifies image input by default, or native video when `--video` is supplied. If the provider rejects `max`, the command stops; it never switches model or silently lowers effort.

## Critique

```bash
python scripts/muse_spark_critic.py critique \
  --video rendered.mp4 \
  --transcript transcript.srt \
  --treatment treatment-spec.json \
  --campaign campaign.json \
  --out critique.json
```

Output: `record` (model identity, provider, effort, request ID, usage, hashes, timestamps) plus validated `critique`.

## Blind comparison

```bash
python scripts/muse_spark_critic.py compare \
  --baseline baseline.mp4 \
  --candidate edit-a.mp4 \
  --candidate edit-b.mp4 \
  --out comparison.json
```

Labels are randomized before submission; the label mapping is stored after the response.

## Persistence

With `CLIP_SHORT_CRITIC_WORKER_URL` and `CLIP_SHORT_CRITIC_TOKEN`, the script uploads the MP4 to R2 and inserts the critique/findings into D1. Without them, the output stays local.

## Prohibited

- Do not call Gemini, DeepSeek, GPT, Claude, or any other model for critique, second opinion, ensemble, or fallback.
- Do not change `model/critic.lock.json` at runtime.
- Do not claim a successful live invocation unless `probe` actually returned a provider response.
