# Subskill: Thumbnail OCR and Semantic QA

Contrast and edge density do not prove a thumbnail communicates the idea.

---

## 1. Required Checks

| Check | Evidence |
| :--- | :--- |
| Text OCR | Actual OCR text, blocks, confidence |
| Headline count | One primary headline |
| Face/eye protection | Face bbox and overlap result |
| Semantic match | Reviewer explanation tying image to the story |
| Crop completeness | No clipped subject/object |
| Mobile readability | Test at 180px width |

`mobile_ocr_pass` and `semantic_match` must be real booleans. `not_checked` blocks PASS.

## 2. Composition

- One focal face or object.
- One headline in negative space.
- No subtitle fragments or HUD duplicate.
- The decisive object of the story should be recognizable at mobile size.
- Prefer the discovery image over a generic reaction.

## 3. Codes

- `THUMBNAIL_OCR_NOT_VERIFIED`
- `THUMBNAIL_SEMANTIC_NOT_VERIFIED`
- `THUMBNAIL_COMPOSITION_UNVERIFIED`
