# EditPolicy architecture

## Roles

1. **Muse Spark 1.3 Contributor** is the only model-based critic. It receives native video and structured context, returns timestamped defects, explanations and typed action proposals.
2. **State builder** assembles machine-measurable current state: timeline, crops, layout, transcript alignment, audio stats, face tracks, object tracks, diagram/screen ROIs, captions, HUD and campaign constraints. Deterministic extractors do not editorially judge.
3. **Action generator** turns Muse critique into bounded, typed candidates and adds `NO_OP`. Every action has preconditions, parameters, risk, expected effects and reversibility.
4. **Renderer** applies the actions and creates low-resolution proxy candidates before expensive final renders.
5. **Muse Spark critic** reviews the actual candidate videos at the same locked model and requested reasoning effort. It compares the candidates against the baseline and target; no other model critic is permitted.
6. **Human reviewer** supplies stronger preference/approval labels. Human approval remains a separate release gate.
7. **LightGBM LambdaRank** learns which action to rank highest from structured numeric state/action features. It is an action selector, not a critic and does not replace Muse.

## State-action loop

`S_t -> candidate actions + NO_OP -> rank -> proxy render -> Muse critique/compare -> human/outcome label -> S_(t+1)`

The ranker should initially propose only the top few candidates. Stop when no action gives a meaningful improvement, constraints are met, the iteration budget is reached, or the critic marks the remaining state unverified.

## State representation

Store visual state by timestamp/beat: speaker boxes and active speaker identity, diagram ROI and visible nodes, object boxes and area ratios, caption boxes, HUD boxes, crop bounds, scene/shot IDs, transcript beat, expected visual entities, and measured quality features. Keep all coordinates normalized to [0,1]. Store raw video/hash references outside feature vectors.

## Action representation

Initial families: `speaker_switch`, `speaker_crop`, `pip_resize`, `diagram_reframe`, `diagram_step_reveal`, `object_reframe`, `caption_reposition`, `caption_style`, `hud_hide`, `hud_reposition`, `broll_insert_source_grounded`, `trim_silence`, `extend_reveal_hold`, `thumbnail_recompose`, and `NO_OP`.

Reject any generated action whose source grounding is absent, whose preconditions are false, or which breaks campaign constraints. The LLM may suggest only actions in this finite vocabulary; the renderer executes only validated action JSON.

## Training and promotion

Train an LGBMRanker on candidate actions grouped by `query_id`. Use human preferences and verified before/after outcomes as strong labels; exclude Muse-only weak labels by default. Split by `video_id` and creator to avoid leakage. Evaluate NDCG@3, human top-action acceptance, no-op calibration, correction rate, cost per accepted edit and format-specific regression tests. Model rollout is shadow -> human-approved canary -> default; retain the previous model for rollback.

Do not optimize directly for raw views alone. Track retention, completion, qualified campaign views, approval and cost separately. Campaign differences and source creator effects must be accounted for.
