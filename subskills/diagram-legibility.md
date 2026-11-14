# Subskill: Diagram ROI, Cropping, and Legibility

Diagram treatments must prove the diagram itself changed and remained readable.

---

## 1. Required Per Beat

| Field | Meaning |
| :--- | :--- |
| `diagram_roi` | Normalized ROI used for the comparison |
| `semantic_state` | Named state (`INTERFACE`, `HARNESS`, `SYNTAX`, `TOOL_CALL`) |
| `roi_only_change` | Change measured inside the ROI only |
| `readable_labels` | OCR/readability result and label evidence |
| `evidence_frame_sha256` | Hash of the exact frame inspected |

## 2. Crop Rules

- Include complete harness/LLM boundaries, incoming and outgoing arrows, and labels.
- Do not crop a diagram edge to remove a cursor or UI handle; mask the artifact or choose a different beat.
- If the full diagram cannot fit without shrinking labels below mobile readability, split it into semantic beats and zoom each component.
- Empty pane space must be used for callouts, not left as dead area.

## 3. Treatment Honesty

If the source contains a static conceptual sketch rather than a real syntax/tool demonstration:

- Use `STATIC_DIAGRAM_WITH_CALLOUTS`.
- Do not label the clip `PROGRESSIVE_DIAGRAM_ZOOM`.
- State the limitation in the report.

## 4. Label Legibility

At 360px-wide playback, labels must remain readable. The report records the label count, OCR status, and the frame hash used to verify it.
