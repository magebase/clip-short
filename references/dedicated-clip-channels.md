# Dedicated CLIP Channels & Multi-Platform Routing Matrix

Autonomous distribution topology mapping stream genres, creator archetypes, and thematic tags to dedicated YouTube channels (`CLIP-01` through `CLIP-10`), Facebook Super-Channels, TikTok accounts, and Instagram pages.

---

## 1. Fleet Channel Manifest

| Channel ID | Handle | Channel Name | Core Niche & Tags | Assigned Super-Channel | Target RPM / Bounty Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CLIP-01` | `@BanterCentralDaily` | **Banter Central Daily** | IRL banter, podcast roasts, streamer drama, comedy | `super_01_scale_velocity` | View-gated creator bounties |
| `CLIP-02` | `@FinanceCrimeAutopsies` | **Finance Crime Autopsies** | Wall Street scams, crypto fraud, corporate autopsies | `super_03_macro_autopsy` | High-RPM finance ($18.00–$24.00) |
| `CLIP-03` | `@ScienceShockersDaily` | **Science Shockers Daily** | Astrophysics, paradoxes, biology, tech mysteries | `super_01_scale_velocity` | Broad algorithmic discovery |
| `CLIP-04` | `@StreamRageClutches` | **Stream Rage & Clutches** | Esports clutch plays, tournament rage, gaming drama | `super_01_scale_velocity` | High-velocity gaming CPM |
| `CLIP-05` | `@SiliconDramaDaily` | **Silicon Drama Daily** | Big Tech drama, CEO clashes, startup wars, dev fails | `super_02_silicon_biopulse` | Developer audience sponsorship |
| `CLIP-06` | `@FrontierAIDeepMinds` | **Frontier AI & Deep Minds** | LLMs, robotics, neural nets, AGI debates | `super_02_silicon_biopulse` | Frontier AI tech audience |
| `CLIP-07` | `@CourtroomBattlesDaily` | **Courtroom & Legal Battles** | High-stakes trials, cross-examinations, legal forensics | `super_03_macro_autopsy` | True crime & legal drama |
| `CLIP-08` | `@MacroPulseDailyclips` | **Macro Pulse & Geopolitics** | Currency wars, trade pacts, geopolitics, elections | `super_03_macro_autopsy` | High-income demographic |
| `CLIP-09` | `@DarkHistoryDaily` | **Dark History & Paradoxes** | Unsolved historical paradoxes, war blunders, archives | `super_02_silicon_biopulse` | Evergreen retention loops |
| `CLIP-10` | `@SpeedrunFeatsClutches` | **Speedrun Feats & Clutches** | World records, pixel-perfect skips, glitch exploits | `super_01_scale_velocity` | Gamer engagement & comments |

---

## 2. Super-Channel Syndication Topology (Facebook Reels)

To maximize cross-platform syndication leverage without managing 30 distinct brand pages, channels aggregate into 3 **Meta Super-Channels**:

1. **`super_01_scale_velocity` (Scale & Velocity Media)**:
   - Aggregates: `CLIP-01` (Banter), `CLIP-03` (Science), `CLIP-04` (Gaming), `CLIP-10` (Speedruns).
   - Content Profile: High kinetic energy, fast visual pacing, mass-market appeal.
2. **`super_02_silicon_biopulse` (Silicon & BioPulse Media)**:
   - Aggregates: `CLIP-05` (Silicon Tech), `CLIP-06` (Frontier AI), `CLIP-09` (Dark History).
   - Content Profile: Technical depth, intellectual curiosity, systems thinking.
3. **`super_03_macro_autopsy` (Macro & Forensic Media)**:
   - Aggregates: `CLIP-02` (Finance Crime), `CLIP-07` (Courtroom Legal), `CLIP-08` (Geopolitics).
   - Content Profile: Investigative autopsies, evidentiary breakdowns, forensic analysis.

---

## 3. Dynamic Keyword Tag Routing Matrix
When new stream moments are ingested, the system maps extracted keywords to the primary channel:

```python
NICHE_ROUTING = {
    "banter":      {"ch": "CLIP-01", "super": "super_01_scale_velocity"},
    "irl":         {"ch": "CLIP-01", "super": "super_01_scale_velocity"},
    "scam":        {"ch": "CLIP-02", "super": "super_03_macro_autopsy"},
    "fraud":       {"ch": "CLIP-02", "super": "super_03_macro_autopsy"},
    "finance":     {"ch": "CLIP-02", "super": "super_03_macro_autopsy"},
    "science":     {"ch": "CLIP-03", "super": "super_01_scale_velocity"},
    "physics":     {"ch": "CLIP-03", "super": "super_01_scale_velocity"},
    "gaming":      {"ch": "CLIP-04", "super": "super_01_scale_velocity"},
    "rage":        {"ch": "CLIP-04", "super": "super_01_scale_velocity"},
    "tech":        {"ch": "CLIP-05", "super": "super_02_silicon_biopulse"},
    "silicon":     {"ch": "CLIP-05", "super": "super_02_silicon_biopulse"},
    "ai":          {"ch": "CLIP-06", "super": "super_02_silicon_biopulse"},
    "legal":       {"ch": "CLIP-07", "super": "super_03_macro_autopsy"},
    "courtroom":   {"ch": "CLIP-07", "super": "super_03_macro_autopsy"},
    "macro":       {"ch": "CLIP-08", "super": "super_03_macro_autopsy"},
    "history":     {"ch": "CLIP-09", "super": "super_02_silicon_biopulse"},
    "speedrun":    {"ch": "CLIP-10", "super": "super_01_scale_velocity"}
}
```

---

## 4. Routing Preconditions

Keyword routing assigns a candidate to a channel; it does not authorize publishing.

1. The clip must pass the production gate and editorial threshold.
2. Campaign preflight must pass for the target platform and campaign.
3. The edit must be unique: no duplicate or near-identical output across channels.
4. A human must approve the submission.
5. Official APIs only; no browser automation on social platforms.

Cadence targets never justify publishing weak, duplicative, or non-compliant clips.
