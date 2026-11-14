# Subskill: Independent Media Inspection

Technical PASS requires measurements, not configuration assumptions.

---

## 1. Required Measurements

| Check | Tool | Evidence |
| :--- | :--- | :--- |
| Container/streams | `ffprobe -show_streams -show_format` | codecs, resolution, fps, SAR, duration |
| Decode | `ffmpeg -v error -i file -f null -` | return code and error lines |
| Black/freeze | `blackdetect` + `freezedetect` | event timestamps |
| Loudness | `loudnorm=print_format=json` | integrated LUFS, true peak, LRA |
| A/V sync | stream `start_time` delta | milliseconds, pass ≤100ms |
| Output hash | SHA-256 | final MP4 digest |

## 2. Square Pixels

Normalize SAR to 1:1 unless a non-square SAR is intentional. A 9:16 output with SAR ≠ 1:1 fails the technical gate.

## 3. Script

```bash
python3 scripts/audit_clip_short_v23.py batch_report.json --inspect
```

The audit records measurements and blocks PASS when any field is missing.
