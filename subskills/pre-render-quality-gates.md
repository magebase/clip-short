# Subskill: Pre-Render Gates & Full-Frame Post-Render QA

Two-stage quality defense. Stage 1 protects the source and render inputs. Stage 2 inspects the actual exported MP4 and is the only authority allowed to mark a clip ready.

The QA verdict is pass/fail. A single critical failure is `REJECTED_RENDER` and cannot be offset by a high editorial score.

v2.1 adds four independent gate statuses: `TECHNICAL_PASS`, `EDITORIAL_PASS`, `CAMPAIGN_PASS`, and `READY_FOR_APPROVAL`. Treatment conformance, independent vision review, semantic frame utility, thumbnail QA, and campaign policy evidence are part of the editorial/campaign gates. See [treatment-conformance.md](treatment-conformance.md), [vision-review.md](vision-review.md), [evidence-backed-qa.md](evidence-backed-qa.md), and [thumbnail-qa.md](thumbnail-qa.md).

---

## 1. QA Verdict Model

| Verdict | Meaning | Next Action |
| :--- | :--- | :--- |
| `REJECTED_QUALITY` | Source footage fails technical eligibility | Select a different candidate; never render |
| `REJECTED_RENDER` | Exported MP4 contains a critical visual, audio, caption, or packaging defect | Re-edit or re-render; never submit |
| `HUMAN_REVIEW` | Campaign rules missing, rights unclear, or low-confidence terminology | Human decision required |
| `EDITORIAL_HOLD` | Production gate passes but editorial score is below publish bar | Improve hook, story, or packaging |
| `READY_FOR_APPROVAL` | Production gate passes and editorial score meets bar | Present package to human |

`READY_FOR_APPROVAL` is not `PUBLISHED`. Distribution requires explicit human approval.

---

# Stage 1 — Pre-Render Gates

## 2. Zero Burnt-In Subtitles Gate

### The Risk
Re-clipping content that already contains hardcoded open captions, translation subtitles, or third-party viral stamps creates overlapping typography artifacts and immediate disqualification on Shorts feeds.

### Detection Algorithm
1. Extract candidate frames across the clip timeline ($t = 0.25 D, 0.50 D, 0.75 D$).
2. Crop the **Subtitle Sensitive Band**:
   $$0.52 \times H_{\text{frame}} \le y \le 0.88 \times H_{\text{frame}}$$
3. Run OCR glyph contour detection and high-frequency edge clustering:
   - Compute gradient density in the band.
   - Run Tesseract OCR or contour character-height clustering ($18\text{px} \le h_{\text{glyph}} \le 60\text{px}$).
4. **Action**: If persistent text glyphs or dialog lines are detected in $\ge 2$ sampled frames, flag as `HAS_BURNT_SUBTITLES` and fail-closed to `REJECTED_QUALITY`. Do not render.

Exception: source graphics such as chart labels or slide titles that are part of the subject — not dialogue captions — are handled by the text-collision test in Stage 2, not by auto-rejection.

---

## 3. Multi-Frame Pixel Sharpness Bar (Laplacian Variance)

### The Risk
Cropping a vertical $1080 \times 1920$ slice from a $1080\text{p}$ landscape source requires an optical upscale ($1.78\times$), resulting in muddy, pixelated, blurry footage that triggers algorithmic low-engagement suppression.

### Sharpness Measurement
1. Sample 5 evenly spaced frames from uncropped source material.
2. Convert frames to grayscale.
3. Compute the Laplacian convolution:
   $$L(x, y) = \frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2}$$
4. Compute the variance of the Laplacian:
   $$\sigma^2_L = \text{Var}(L(x, y))$$
5. **Threshold**:
   $$\sigma^2_L \ge 65.0$$
   - $\sigma^2_L \ge 100.0$: Razor-sharp 4K / 1440p master source.
   - $65.0 \le \sigma^2_L < 100.0$: Crisp 1080p source.
   - $\sigma^2_L < 65.0$: **REJECTED_QUALITY** (blurry/muddy video stream).

---

## 4. High-Resolution Source Requirement (4K / 1440p Preferred)
When fetching VODs via `yt-dlp`, always prioritize high-resolution master streams:
```bash
yt-dlp -f "bestvideo[height<=2160]+bestaudio/best[height<=2160]" ...
```
Cropping a 9:16 slice from a 4K frame ($1215 \times 2160$) downsamples crisply into retina-grade $1080 \times 1920$, eliminating pixelation entirely.

---

## 5. Broadcast Audio Normalization (EBU R128)
- **Target Integrated Loudness**: $-14.0\text{ LUFS} \pm 1.0\text{ LUFS}$ (campaign rules may override).
- **True Peak Ceiling**: $\le -1.0\text{ dBTP}$ to eliminate inter-sample clipping on mobile DACs.
- **Loudness Range (LRA)**: Target $7.0\text{ LU}$ for punchy mobile vocal presence.
- **Pre-Speech Fade-In**: $35\text{ms}$ (`afade=t=in:ss=0:d=0.035`).
- **Post-Speech Decay Fade-Out**: $80\text{ms}$ (`afade=t=out:st={FADE_OUT}:d=0.080`).

---

## 6. Freeze Frame & Dead Air Detection
- Scan video track for duplicate frame runs:
  $$\text{Max Freeze Duration} \le 0.8\text{s}$$
- Scan audio track for silent passages ($< -45\text{ dBFS}$):
  $$\text{Max Audio Silence} \le 0.6\text{s}$$
- Clips violating these thresholds fail-closed to prevent publishing dead air.

---

## 7. Caption Audio Fidelity Gate (Pre-Render)
Before rendering, compare the caption plan against the aligned transcript:
- Every displayed word must exist in the verified transcript for that cut.
- No dropped negations (`not`, `never`, `no`) and no substituted entities.
- Numbers, units, and acronyms must match the verified transcript exactly.
- Any mismatch is `REJECTED_QUALITY`; fix the transcript or the caption plan before spending render time.

---

# Stage 2 — Full-Frame Post-Render Inspection

## 8. Inspection Target

Inspect the **exported MP4**, not the render script, still frames from the source, or the FFmpeg configuration. The rendered file is the deliverable and the only valid evidence.

Required inputs:
- Final MP4 with audio.
- Final ASS/embedded captions.
- Final thumbnail image.
- Submission metadata JSON.

---

## 9. Mandatory Contact Sheet

Generate a contact sheet from the exported MP4 at:

| Sample | Timestamp |
| :--- | :--- |
| Cold open | $0.25\text{s}$ |
| First full second | $1.00\text{s}$ |
| Every major scene transition | detected cut / layout change |
| Every major caption or graphic transition | first frame of each new full-screen text event |
| Midpoint | $0.50 \times D$ |
| Final payoff | last $2.0\text{s}$ |

Contact-sheet command:

```bash
ffmpeg -y -i "{RENDER_MP4}" -vf "fps=2,scale=270:480,tile=5x6" -frames:v 1 contact_sheet.jpg
```

Also export one full-resolution frame at each sampled timestamp for OCR and face-occlusion checks.

---

## 10. Critical Rejection Tests

| Test | Failure condition | Detection method |
| :--- | :--- | :--- |
| **Debug overlay** | Code, filter expressions, internal variables, or phase labels visible | OCR the full frame for tokens such as `if(`, `tt(`, `enable=`, `between(`, `filter`, `overlay`, variable names, and unresolved placeholders; compare OCR text against the expected caption/metadata text |
| **Cursor detection** | Mouse cursor unintentionally visible in the supporting pane | Detect small high-contrast moving blobs across frames in the screen region; confirm with edge + motion persistence. If persistent, re-crop/zoom to exclude the cursor path or choose a different beat |
| **Crop integrity** | Important diagram, labels, subject, hands, or key objects cut off | Edge-density continuity at crop borders; verify diagram bounding box plus 40px padding is inside the pane; human visual check on full-resolution frames |
| **Graphic readability** | Supporting text or labels unreadable at mobile size | Estimate rendered glyph height; require $\ge 24\text{px}$ at $1080$ width for primary labels and $\ge 18\text{px}$ for secondary labels; reject full-diagram shrink that fails |
| **Face occlusion** | Headline, pill, or captions cover eyes, mouth, or key expression | Run face landmarks on sampled frames; reject if any text bounding box intersects the eye or mouth region |
| **Text collisions** | Captions overlap source text, tickers, or existing graphics | OCR source regions; reject if caption bounding boxes intersect detected source-text regions |
| **Thumbnail integrity** | Duplicate headlines, subtitle fragments, excessive text, or covered face | OCR thumbnail; require exactly one headline block; reject if subtitle text or duplicate headline detected; face landmark check |
| **Caption accuracy** | Spoken words differ from displayed captions | Re-transcribe the exported audio; diff against displayed captions; reject on dropped negation, changed entity, or changed number |
| **Visual continuity** | Black frames, unintended freezes, flash frames, broken transitions | Frame-difference and black-frame scan across the full render |
| **Campaign compliance** | Duration, sound, hashtags, mentions, disclosure, account, or audience rule violated | Validate submission metadata against the loaded campaign config |
| **A/V sync** | Lips and speech visibly offset | Audio onset vs. mouth-motion correlation; reject drift $> 80\text{ms}$ |
| **Resolution / cadence** | Not $1080 \times 1920$, wrong SAR, or broken frame rate | `ffprobe` stream validation |

A failure in any row above produces `REJECTED_RENDER` until fixed and re-inspected.

---

## 11. Debug Overlay Detection Detail

The Theo regression proved that layout code can leak into the picture. Treat any of these as a critical defect:

- Literal conditional expressions: `if(tt(...))`, `between(t,...)`, `enable=`.
- Phase labels that read like code or state names (`1 HARNESS & TOOLS`, `2 HARNESS TO LLM`).
- Unresolved template placeholders: `{HEADLINE}`, `{PX}`, `{DYNAMIC_W}`, `None`, `null`.
- Debug counters, FPS overlays, bounding boxes, or tracking dots.

Mitigation: build text overlays only from validated metadata fields, never from filter-graph source strings. Render a dry-run frame before the full render and OCR it.

---

## 12. Cursor and Screen-Clutter Detail

For screen-share and diagram sources:

1. Mask known chat columns, taskbars, and browser chrome before saliency selection.
2. Track the cursor path across the beat. If the cursor sits inside the chosen crop for more than $0.5\text{s}$, either:
   - choose a crop that excludes the cursor path,
   - punch in on the target component so the cursor is outside the frame, or
   - select another beat.
3. Never include a visible cursor in a submitted clip when it distracts from the diagram.

If cursor removal is impossible without damaging the content, fail closed to `HUMAN_REVIEW`.

---

## 13. Contact-Sheet and Playback Review Procedure

1. Generate the contact sheet and full-resolution sampled frames.
2. Run OCR on every sampled full-resolution frame; compare against expected text.
3. Run face landmark occlusion checks on every frame containing text.
4. Watch the full MP4 end to end with audio at normal speed. Do not skip the middle.
5. Re-transcribe the exported audio and diff it against the displayed captions.
6. Confirm the thumbnail at mobile size (approximately 120px wide preview).
7. Record findings in the QA JSON with timestamp, test, and verdict.
8. Only then assign `READY_FOR_APPROVAL`.

---

## 14. Production Gate Checklist

| Area | Required Evidence |
| :--- | :--- |
| Campaign compliance | Loaded campaign config and validated submission metadata |
| Rights and source | Approved source URL, license/fair-use basis, and attribution |
| Render integrity | `ffprobe` pass, full-frame contact sheet, OCR pass, no debug overlay |
| Crop and readability | Full diagram enclosed, labels $\ge$ minimum size, no cursor |
| Captions | Displayed captions match re-transcribed exported audio |
| Audio | Integrated loudness and true peak within spec |
| Visual continuity | No black frames, unintended freezes, or broken transitions |
| Typography | No face occlusion, no source-text collision, safe-zone pass |
| Thumbnail | One headline, unobstructed face, mobile-readable |
| Packaging | Five text layers distinct and semantically consistent |

All rows must pass before `READY_FOR_APPROVAL`.
