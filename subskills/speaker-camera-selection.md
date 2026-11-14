# Subskill: Speaker & Camera Selection

A speaker-switching edit must follow the voice. Never show a microphone, empty chair, or listener reaction because the router failed to find a face.

---

## 1. Selection Hierarchy

1. **Active speaker face** — mouth moving, face detected, audio energy aligned with the turn.
2. **Intentional reaction** — listener face with a deliberate reaction beat, minimum dwell time.
3. **Relevant B-roll** — only when explicitly planned and visually informative.
4. **Wide shot** — only when no face is available and the wide shot carries context.
5. **Never** — microphone-only, empty chair, back of head, or blocked face while a speaker is talking.

## 2. Shot Quality Signals

| Signal | Penalty |
| :--- | :--- |
| No face detected while speech active | Critical |
| Face area below 0.5% of frame | Major |
| Face occluded by hand/mic | Major |
| Cut to listener without reaction intent | Minor |
| Cut duration below 0.8s | Minor |
| Cut duration above 6s on a static listener | Minor |

## 3. Conformance

`DYNAMIC_SPEAKER_SWITCHING` requires a face in every beat. The reviewer measures face area with YuNet inside the active speaker region and records per-beat evidence. A dense scan also checks every sampled frame; a face-free run of 1.0s or longer fails `MISSING_FACE_INTERVAL`. A mic-only beat fails `MISSING_FACE` and triggers `RENDER_REVISION`.

## 4. Stabilization

- Smooth crop coordinates across frames; never jitter on face detection noise.
- Hold a shot for at least 0.8s after a cut.
- Prefer a slightly wider stable crop over a tight crop that clips the forehead or chin.
