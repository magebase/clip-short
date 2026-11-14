# Subskill: Format-Specific Caption and HUD Systems

One karaoke style for every source makes different formats feel identical.

---

## 1. Formats

| Format | HUD | Captions |
| :--- | :--- | :--- |
| Podcast | Minimal premise, fade by 3.8s | Restrained phrase-level, no per-word color cycling |
| Technical explainer | Compact title; diagram callouts take over | Phrase captions plus labels |
| Illustrated narration | No persistent HUD | Minimal phrase captions, preserve art style |

## 2. Adaptive Placement

- Captions must avoid faces, diagram nodes, and expected objects.
- Compute placement from detected bboxes, not a single fixed `MarginV`.
- Test collisions against the narration-visual timeline.

## 3. Phrase Captions

Allow word-by-word only when it adds meaning. Default to 3–6 word semantic phrases. Preserve contractions and natural punctuation.

## 4. Style Preservation

Do not apply neon streamer palettes to watercolor, historical, or documentary art. One type system and one accent per clip.
