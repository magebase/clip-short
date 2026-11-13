# Subskill: Pre-Render Quality Gates & Video Defense

Automated pre-render and post-render defensive gates to reject blurry footage, detect pre-existing burnt-in subtitles, prevent A/V desync, and ensure broadcast loudness.

---

## 1. Zero Burnt-In Subtitles Gate

### The Risk
Re-clipping content that already contains hardcoded open captions, Chinese/English translation subtitles, or third-party viral stamps creates overlapping typography artifacts and immediate disqualification on Shorts feeds.

### Detection Algorithm
1. Extract candidate frames across the clip timeline ($t = 0.25 D, 0.50 D, 0.75 D$).
2. Crop the **Subtitle Sensitive Band**:
   $$0.52 \times H_{\text{frame}} \le y \le 0.88 \times H_{\text{frame}}$$
3. Run OCR glyph contour detection and high-frequency edge clustering:
   - Compute gradient density in the band.
   - Run Tesseract OCR or contour character-height clustering ($18\text{px} \le h_{\text{glyph}} \le 60\text{px}$).
4. **Action**: If persistent text glyphs or dialog lines are detected in $\ge 2$ sampled frames, flag as `HAS_BURNT_SUBTITLES` and fail-closed to `REJECTED_QUALITY`. Do not render.

---

## 2. Multi-Frame Pixel Sharpness Bar (Laplacian Variance)

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

## 3. High-Resolution Source Requirement (4K / 1440p Preferred)
When fetching VODs via `yt-dlp`, always prioritize high-resolution master streams:
```bash
yt-dlp -f "bestvideo[height<=2160]+bestaudio/best[height<=2160]" ...
```
Cropping a 9:16 slice from a 4K frame ($1215 \times 2160$) downsamples crisply into retina-grade $1080 \times 1920$, eliminating pixelation entirely.

---

## 4. Broadcast Audio Normalization (EBU R128)
- **Target Integrated Loudness**: $-14.0\text{ LUFS} \pm 0.5\text{ LUFS}$.
- **True Peak Ceiling**: $\le -1.0\text{ dBTP}$ to eliminate inter-sample clipping on mobile DACs.
- **Loudness Range (LRA)**: Target $7.0\text{ LU}$ for punchy mobile vocal presence.
- **Pre-Speech Fade-In**: $35\text{ms}$ (`afade=t=in:ss=0:d=0.035`).
- **Post-Speech Decay Fade-Out**: $80\text{ms}$ (`afade=t=out:st={FADE_OUT}:d=0.080`).

---

## 5. Freeze Frame & Dead Air Detection
- Scan video track for duplicate frame runs:
  $$\text{Max Freeze Duration} \le 0.8\text{s}$$
- Scan audio track for silent passages ($< -45\text{ dBFS}$):
  $$\text{Max Audio Silence} \le 0.6\text{s}$$
- Clips violating these thresholds fail-closed to prevent publishing dead air.
