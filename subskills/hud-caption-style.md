# Subskill: HUD and Caption Style Controls

One visual identity is not one template for every source.

---

## 1. HUD

- Establish the premise, then disappear. Default persistence: fade out by 3.8s.
- Format-specific:
  - Podcast: minimal top headline, then clean frame.
  - Technical explainer: compact title, diagram callouts take over.
  - Illustrated narration: no persistent HUD; preserve the original composition.
- Record `hud_persistence` (seconds and coverage ratio) in QA. A persistent HUD must be justified.

## 2. Captions

- Word-by-word karaoke is optional, not default.
- Podcast: restrained phrase captions.
- Technical: phrase captions plus diagram labels.
- Illustrated narration: minimal phrase captions, no neon highlight palette.
- Preserve exact speech; re-segment at natural phrase boundaries. Do not display awkward function-word runs.

## 3. Style Consistency

Keep one type system and one accent color per clip. Do not cycle unrelated highlight colors across formats.
