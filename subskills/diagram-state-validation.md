# Subskill: Diagram State Validation

A diagram state describes what it communicates, not merely how different its pixels are.

---

## 1. State Schema

```json
{
  "beat": "tool_execution",
  "semantic_state": "TOOL_CALL",
  "required_elements": [
    {"name": "harness", "bbox_norm": [0.08, 0.1, 0.3, 0.5]},
    {"name": "llm", "bbox_norm": [0.55, 0.2, 0.3, 0.4]},
    {"name": "request_arrow", "bbox_norm": [0.4, 0.35, 0.12, 0.05]},
    {"name": "response_arrow", "bbox_norm": [0.4, 0.55, 0.12, 0.05]}
  ],
  "checks": {
    "all_elements_visible": true,
    "all_labels_readable": true,
    "no_edge_clipping": true,
    "semantic_state_distinct": true,
    "caption_collision": false
  }
}
```

## 2. Rules

- Every required node, label, and arrow must have a normalized bbox.
- Any bbox touching the 2% safe margin fails `DIAGRAM_EDGE_CLIPPING`.
- Labels must be readable at 360px-wide playback.
- Adjacent states must communicate a new concept, not just a different crop.
- Captions must not cover a required element.
- If the source cannot support the sequence, use `STATIC_DIAGRAM_WITH_CALLOUTS` and say so.

## 3. Codes

- `DIAGRAM_ELEMENTS_MISSING`
- `DIAGRAM_EDGE_CLIPPING`
- `DIAGRAM_STATE_NOT_DISTINCT`
- `CAPTION_OBJECT_COLLISION`
