# Subskill: Faithful Metadata Packaging & Curiosity Gates

Autonomous generation of high-CTR, 100% faithful YouTube titles, HUD headline banners, descriptions, and curiosity-gap validation.

---

## 1. Direct Transcript Grounding Law

### The Problem
Generic clickbait tables, cross-niche keyword templates, and hallucinated titles ruin channel trust and trigger high 3-second swipe-away rates. If a video is titled *"Shocking Bug Destroys Production!"* but the streamer is discussing PostgreSQL connection pooling, retention plummets.

### The Standard
All packaging metadata must be derived **strictly and directly from the literal words spoken** inside that specific $18.0\text{s} - 22.5\text{s}$ cut.

---

## 2. Top HUD Headline Specification
The HUD headline is the text displayed inside the top pill badge at $0.0\text{s}$:
- **Length**: Strictly 3 to 6 words.
- **Character Count**: Maximum 38 characters.
- **Casing**: Strict Title Case (`Why SQLite Beats Postgres`).
- **Punctuation**: Zero trailing punctuation (no periods, no trailing exclamation points, no question marks in HUD pill).
- **Grounding**: Must use core terms directly uttered by the speaker.

---

## 3. Curiosity-Gap Redundancy Gate (`resolve_redundant_headline`)

### The Redundancy Trap
If the streamer's first spoken sentence is *"I just deleted our production database"*, and the top HUD pill reads *"I Deleted Our Production Database"*, the viewer experiences $100\%$ cognitive redundancy. Retention suffers because no question was posed.

### Lexical Overlap Test
Let $T_{\text{spoken}}$ be the set of lemmatized words in the first $3.0\text{s}$ of spoken audio, and $T_{\text{headline}}$ be the set of words in the candidate HUD headline.

$$\text{Overlap Ratio} = \frac{|T_{\text{headline}} \cap T_{\text{spoken}}|}{|T_{\text{headline}}|}$$

### Gate Enforcement
- **If $\text{Overlap Ratio} \le 0.65$**: Approved. Headline complements audio without verbatim parroting.
- **If $\text{Overlap Ratio} > 0.65$**: **Redundancy Triggered**. The headline must be reformulated into a **Curiosity Thesis Question** or an **Impact Consequence** instead of verbatim repetition:
  - *Verbatim spoken*: "We rewrote the entire engine in Rust last month."
  - *Failed headline (100% overlap)*: "Rewrote The Engine In Rust"
  - *Reformulated headline (Curiosity gap)*: "Was The Rust Rewrite Worth It"

---

## 4. YouTube Title Architecture
Vertical Shorts titles must balance mobile feed readability with algorithmic search indexing:
- **Length**: $45 - 65$ characters.
- **Format**: `[Primary Dramatic Keyword / Hook] + [Contextual Specificity] + #Shorts`
- **Examples**:
  - `Why SQLite Beats PostgreSQL For 95% Of Apps #Shorts`
  - `The Silent Bug That Crashed CrowdStrike #Shorts`
  - `Why Senior Devs Refuse To Use ORMs #Shorts`
- **Tags & Description**: Ingest 5–8 high-relevance niche hashtags matching streamer and technical concepts. Include educational fair-use attribution notice.
