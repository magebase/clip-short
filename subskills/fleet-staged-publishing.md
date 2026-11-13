# Subskill: Fleet Staged Publishing & Pod Quota Architecture

Automated multi-channel fleet scheduling, staged private release protocol, YouTube Data API quota management, and platform safety rules.

---

## 1. Universal Staged Private Release Standard

### The Law
**Strictly forbid direct `privacyStatus="public"` uploads.**
Direct public bursts trigger YouTube anti-spam heuristics (`uploadLimitExceeded` HTTP 400), ruin initial view velocity with 360p draft playback while VP9/AV1 processing is pending, and risk project-wide quota blackouts.

### The Standard
Every YouTube upload payload must set:
1. `status.privacyStatus = "private"`
2. An explicit future `status.publishAt` ISO-8601 timestamp.
3. **Mandatory Minimum 2.5-Hour (150-Minute) Transcode Buffer**:
   $$t_{\text{publishAt}} \ge t_{\text{upload}} + 150\text{ minutes}$$
   This allows YouTube's backend to complete Content ID copyright scans, 1080p60 VP9/AV1 multi-resolution transcodes, and automatic thumbnail indexing before the video goes public.

---

## 2. 3-Pod GCP Quota Architecture & 85-Upload Headroom Gate

YouTube Data API v3 enforces a 100-upload/24h ceiling per GCP Project. To prevent cross-factory starvation and expand fleet capacity to **300 uploads/day**, operate in 3 isolated project pods:

```
+-----------------------------------------------------------------------------------+
|                            ENTERPRISE FLEET TOPOLOGY                              |
+-----------------------------------------------------------------------------------+
|  POD 01: pod-video         |  POD 02: pod-music         |  POD 03: pod-clips      |
|  Channels: CH-01 to CH-10  |  Channels: MC-01 to MC-10  |  Channels: CLIP-01..10  |
|  AI Long-Form & Shorts     |  Ambient Lofi / EPs        |  Streamer & Tech Clips  |
|  Daily Quota: 100 uploads  |  Daily Quota: 100 uploads  |  Daily Quota: 100 uploads|
+-----------------------------------------------------------------------------------+
```

### The 85-Upload Safety Headroom Rule
Every publishing script must check `QuotaManager.get_status(pod_id)` before calling `videos.insert`:
$$\text{If } N_{\text{uploads}}(\text{pod}) \ge 85 \implies \text{HALT POD UPLOADS}$$
- Any pending videos must be staged locally as `STAGED_LOCAL`.
- Resumes upload queue at midnight Pacific Time ($00:00\text{ PT}$) when the GCP quota window resets.

---

## 3. Channel Cadence Ceilings
- **Clip Factory Channels**: Max 2 to 3 clips per channel per 24h rolling cycle.
- **Minimum Publish Window**: Spaced at least $\ge 4.0\text{ hours}$ apart via `compute_staged_publish_time()`.
- **Fail-Closed Cooldown**: If YouTube returns `uploadLimitExceeded`, mark the asset as `STAGED_LOCAL`, engage a 24-hour channel cooldown, and proceed with other non-conflicting tasks.

---

## 4. Zero Browser Automation on Social Platforms
Strictly forbid any headless or automated browser sessions (Playwright, Puppeteer, Selenium, Camoufox) from interacting with YouTube Studio, Meta Business Suite, Instagram, or TikTok. Automated browser clicks on social login interfaces trigger account bans (`Inauthentic Behavior`). All publishing operations run strictly via official REST APIs with official OAuth credentials stored in `TokenVault`.
