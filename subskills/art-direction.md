# Subskill: Format-Aware Art Direction

Every treatment gets a visual grammar derived from the source, not a universal recipe.

---

## 1. Podcast / Conversation

- Show the active speaker, not the microphone. Face-first camera hierarchy.
- A listener reaction is valid only when intentional and held for at least 0.8s.
- No mic-only or empty-chair shot while speech is active. A face-free run longer than 1.0s fails `MISSING_FACE_INTERVAL`.
- Keep the headline above the eyes; captions below the mouth.
- Thumbnail: clean face crop, one headline, one conceptual accent.

## 2. Diagram / Screen Share

- Compare the **diagram-only ROI**, not the whole frame. Mask the speaker pane, captions, and HUD before measuring change.
- Require at least two semantic states. A crop/zoom with no new information is not progressive explanation.
- Keep labels inside the ROI and legible at 360px-wide playback.
- If the source has no demonstration, downgrade to `STATIC_DIAGRAM_WITH_CALLOUTS`; do not claim `PROGRESSIVE_DIAGRAM_ZOOM`.
- Use empty diagram space for callouts instead of covering labels.
- Thumbnail: face + diagram, one headline, no caption fragments.

## 3. Narrated Illustration / Documentary

- Synchronize scene changes with narrative events, not fixed timestamps.
- The decisive evidence must be on screen before the confession or conclusion.
- When narration names an object (flies, sickle, document), the object must occupy enough frame area to be recognizable.
- Avoid pale, low-information shots during discovery and reveal.
- Preserve the source art style; do not add neon streamer graphics to watercolor or historical illustration.

## 4. Screen Recording / Product Demo

- Crop the active window; exclude browser chrome, sidebars, and taskbars.
- Zoom the region where the action happens.
- Cursor and debug overlays are critical failures.
- Thumbnail: the result, not the UI chrome.

## 5. Slides

- Isolate the slide; add the speaker only when the face adds meaning.
- Do not shrink slide text below mobile readability.

## 6. Gaming / Sports / Performance

- Action-safe crop; keep the ball, car, or performer in frame.
- Facecam inset only when the reaction matters.
- Beat-match cuts to natural action, not arbitrary timestamps.

## 7. Thumbnail Composition

- One primary headline; no HUD duplicate, no subtitle fragment, no transcript text.
- Face and eyes unobstructed; headline in negative space.
- One accent color and one type system.
- Test at 180px width, not just 1080p.
