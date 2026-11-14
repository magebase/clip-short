# Model management — single critic

## Locked identity

`model/critic.lock.json` is the single source of truth. The only permitted model-based critic is `muse-spark-1.3-contributor` through Meta Model API. No fallback, ensemble, or alternative LLM reviewer is allowed.

The operator-supplied catalog label `Muse Spark 1.3 Contributor | 45,300` is preserved as display metadata. Meta's public model documentation lists a 1,048,576-token context window; do not interpret `45,300` as its context limit without a source from the actual model catalog that defines that number.

## Runtime and effort

Use the Responses API at `https://api.meta.ai/v1`. Request `reasoning.effort="max"` for critique. Important: Meta's current Model API reasoning page explicitly excludes `muse-spark-1.3-contributor` from `max`; Meta's Muse Code changelog says its Contributor sessions default to max. Therefore provider/runtime behavior must be probed. The wrapper uses strict mode and stops on unsupported `max`; it never silently lowers effort or substitutes a model. To use `max` on the public Model API, Meta's documentation lists the standard `muse-spark-1.3`, but this project intentionally does not switch to it because the operator selected Contributor.

## Versioning

Record for each critique:
- model ID and provider;
- endpoint/API surface;
- requested and confirmed reasoning effort;
- prompt version and schema version;
- caller script version and git commit;
- API request ID and timestamp;
- input MP4 SHA-256;
- file ID (do not treat it as durable asset identity);
- usage fields returned by provider.

Never log API keys, hidden reasoning, or secrets. Do not assume model weights or provider aliases are immutable; periodically run the smoke test and a frozen critique benchmark, but only with the locked model ID.

## API key

Use `MODEL_API_KEY` from a secrets manager or environment variable. Do not put it in `opencode.json`, YAML, `.env` committed to Git, or any report.

## Contributor mode consent

The Contributor variant is discounted because prompts, files and responses may be used to improve Meta products. Require `CLIP_SHORT_ALLOW_CONTRIBUTOR_DATA_USE=1` before upload. This is a deliberate policy gate, not an API requirement. The operator must confirm rights to upload each source video and acceptance of Contributor data handling. File deletion after inference is hygiene only; it does not reverse data-use permission.
