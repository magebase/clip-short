# Subskill: Autonomous 10-Minute Cadence Engine & Multi-Platform Syndication

Architecture of the continuous 600-second clipping, rendering, CDN ingestion, multi-platform publishing, bounty claiming, and cockpit telemetry loop.

---

## 1. 10-Minute Cadence Execution Pipeline

```
  +-------------------------------------------------------------------------------+
  |                        10-MINUTE AUTONOMOUS CADENCE ENGINE                    |
  |                        (scripts/clipfactory_daemon_10m.py)                    |
  +-------------------------------------------------------------------------------+
                                          |
  [00:00] Non-Blocking File Lock Acquisition (/tmp/clipfactory_python.lock)
                                          |
  [00:02] Self-Healing UTC Date Check & Quota Counter Reset (Daily Ceilings)
                                          |
  [00:05] Highest-EV Candidate Selection (Viral Score x Freshness x Bounty)
                                          |
  [00:10] Master Render with Kinetic Spring Captions (\fscx124) & Vector Emojis
                                          |
  [02:30] Cloudflare R2 CDN Ingestion via Wrangler (video-factory-renders/clips)
                                          |
  [03:00] Multi-Platform Fleet Syndication:
          ├── 1. YouTube Shorts: Pod 03 CLIP Channel (Staged Private, 150m buffer)
          ├── 2. TikTok: Official Content Posting API
          ├── 3. Instagram Reels: Meta Graph API Video Container
          └── 4. Facebook Reels: Meta Super-Channel Page Feed
                                          |
  [04:30] View-Gated Bounty Payout Claiming -> Lili Business Checking
                                          |
  [05:00] Live SQLite Ingest Sync & Cloudflare Workers Cockpit Redeployment
                                          |
  [10:00] Next Cycle Trigger (CADENCE_SECONDS = 600)
```

---

## 2. Highest Expected Value (EV) Ranking Formula

Instead of processing clips chronologically, the daemon computes the Expected Value ($EV$) of each unrendered candidate:

$$EV = S_{\text{viral}} \times M_{\text{streamer\_tier}} \times M_{\text{format}} \times M_{\text{freshness}} \times M_{\text{bounty\_rate}}$$

Where:
- $S_{\text{viral}} \in [0.0, 1.0]$: Scored by Gemini Flash viral evaluation.
- $M_{\text{streamer\_tier}}$: Tier 1 ($1.5\times$ for Theo, Primeagen, Speed, CaseOh), Tier 2 ($1.2\times$).
- $M_{\text{format}}$: Bonus multiplier for high-converting formats ($1.3\times$ for Whiteboard Explainer & Phonk Freeze).
- $M_{\text{freshness}} = e^{-\lambda \Delta t}$: Exponential decay favoring moments from streams in the last 24h.
- $M_{\text{bounty\_rate}}$: Payout multiplier for active sponsor/streamer bounties ($1.4\times$).

---

## 3. Cloudflare R2 CDN Ingestion

Local MP4 renders are uploaded directly to the edge CDN using Wrangler CLI:
```bash
wrangler r2 object put video-factory-renders/clips/clip_{clip_id}.mp4 \
  --file=/path/to/renders/clip_{clip_id}.mp4 \
  --remote
```
- CDN Public Endpoint: `https://video-factory.adstim.net/renders/clips/clip_{clip_id}.mp4`
- Ensures low-latency, zero-cost bandwidth streaming to social platform ingest servers.

---

## 4. Multi-Platform Syndication Protocol

```python
# Multi-platform publication sequence executed each cycle
def syndicate_clip_across_fleet(clip_id, r2_url, metadata, channel_info):
    # 1. YouTube Shorts (Pod-Clips)
    if not is_channel_on_cooldown(channel_info["youtube_id"]):
        publish_youtube_staged_private(
            channel_id=channel_info["youtube_id"],
            title=metadata["youtube_title"],
            description=metadata["description"],
            tags=metadata["tags"],
            publish_delay_min=150  # 2.5 hour transcode buffer
        )

    # 2. TikTok Content Posting API
    publish_tiktok_direct(
        video_url=r2_url,
        title=metadata["hud_headline"],
        privacy="PUBLIC_TO_EVERYONE"
    )

    # 3. Instagram Reels
    publish_instagram_reel(
        video_url=r2_url,
        caption=metadata["instagram_caption"]
    )

    # 4. Facebook Reels Super-Channel
    publish_facebook_super_channel_reel(
        super_channel=channel_info["super_channel"],
        video_url=r2_url,
        description=metadata["facebook_description"]
    )
```

---

## 5. Commercial Accounting & Bounty Claiming

- **Automated Payout Engine (`bounty_claimer.py`)**: Interrogates streamer platform APIs (e.g. Whop, CreatorBounty) for view-gate milestones ($10\text{k}, 50\text{k}, 100\text{k}$ views).
- **Direct ACH Deposit**: Claims payouts into Lili Business Checking.
- **Form 5472 Tax Ledger (`accounting.py`)**: Logs gross receipts, foreign-owned US single-member LLC transaction codes, and platform deductions into SQLite.
