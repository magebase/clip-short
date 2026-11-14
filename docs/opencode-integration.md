# OpenCode integration

Meta's official OpenCode setup recommends the `@ai-sdk/openai` adapter against the Responses API at `https://api.meta.ai/v1`, with the model configured for text/image/PDF/video modalities and encrypted reasoning continuity. This package provides `opencode/opencode.provider.fragment.json` using the operator-selected Contributor model ID and requested `max` effort.

Merge the fragment into your `opencode.json` rather than replacing the full configuration. Confirm the exact schema accepted by your installed OpenCode version. Keep `MODEL_API_KEY` out of the config file.

Important distinctions:
- OpenCode model selection does not prove that video is actually being attached to the request.
- The canonical local MP4 route for this skill is `scripts/muse_spark_critic.py`, which uploads the video through Meta Files API and references its `file_id` in a Responses API `input_file` block.
- OpenCode can orchestrate the skill and inspect the resulting critique JSON, but the script owns video upload and model invocation.
- Run `python scripts/muse_spark_critic.py probe --effort max --video path/to/short.mp4` after setup.
- If the provider rejects `max` for the Contributor model, do not switch to standard Muse Spark or another model. Stop and resolve the provider/runtime compatibility explicitly.

Meta docs currently describe `muse-spark-1.3-contributor` as the Contributor-mode model ID. The official Model API reasoning docs state that max is unavailable for that API variant; Muse Code release notes separately mention max defaults in Contributor sessions. These statements concern different runtime surfaces. This skill's strict probe prevents assuming they are interchangeable.
