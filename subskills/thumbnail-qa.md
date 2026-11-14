# Subskill: Dedicated Thumbnail QA

The thumbnail is a separate deliverable, not a frame grab with captions. It gets its own composition and its own gate.

---

## 1. Rules

1. Exactly one primary headline.
2. No subtitle fragments, transcript text, or duplicated HUD headline.
3. Headline does not overlap eyes, mouth, or the key facial expression.
4. Supporting image communicates the subject without reading the title.
5. Readable after downscaling to mobile display size (180px wide test).
6. No black empty bands or accidental letterboxing.

## 2. Checks

| Check | Failure |
| :--- | :--- |
| Headline count | More than one headline or any secondary text layer |
| Headline length | Not 3–6 words or over 38 characters |
| Face collision | Headline rectangle intersects the face/eye rectangle |
| Mobile readability | Downscaled standard deviation < 8 or edge ratio < 0.01 |
| Duplicate layer | Thumbnail text repeats the HUD or a subtitle fragment |

## 3. Composition Guidance

- Choose a topic-relevant frame with a clear subject.
- Place the headline in negative space, not over the face.
- Use one type system and one accent color.
- Keep the face and eyes unobstructed.
- Prefer a frame that shows the object of the story (sickle, harness, speaker) over a generic reaction.

## 4. Verdict

Any failed check is `REJECTED_THUMBNAIL`; the video may still be approved only after a corrected thumbnail is supplied.
