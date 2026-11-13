# Subskill: Faithful Metadata Packaging & Five Text Layers

Packaging is five distinct layers built from one verified understanding of the cut. They must be semantically consistent without repeating identical text.

---

## 1. The Five Text Layers

| Layer | Purpose | Constraint | Verification |
| :--- | :--- | :--- | :--- |
| **1. HUD headline** | On-video curiosity badge at the cold open | 3–6 words, Title Case, max 38 chars, no trailing punctuation | Grounded in the verified transcript; no unresolved placeholders |
| **2. Subtitles** | Verbatim spoken-word captions | 3–5 word semantic cues | Diffed against re-transcribed exported audio |
| **3. YouTube title** | Search and feed discovery | 45–65 chars, faithful paraphrase | Every entity, number, and claim supported by the cut |
| **4. Thumbnail headline** | Single visual promise | 2–5 words, one headline block | Face unobstructed; no subtitle fragments; no duplicate headline |
| **5. Campaign caption / hashtags** | Submission compliance | Per campaign config | Validated against `campaign-preflight` |

Never generate one string and reuse it across layers. Never place subtitle fragments on the thumbnail.

---

## 2. Grounding and Faithful Paraphrase

### The Standard
Packaging must accurately reflect what the source establishes. The old rule requiring every title to consist exclusively of literal spoken words is too restrictive. Use either:

- **Literal grounding** — words spoken in the cut.
- **Faithful paraphrase** — accurate restatement of the cut's claim, with no new entity, number, outcome, or certainty.

### Forbidden
- Invented numbers, names, products, or outcomes.
- Stronger certainty than the speaker used (`might` $\to$ `will`, `some` $\to$ `all`).
- Claims from outside the cut that the viewer cannot verify in the clip.
- Contradicting the speaker's stance to manufacture a hook.

### Allowed
- `"The trade-off nobody wants to make"` for a speaker explaining a security-versus-impact trade-off.
- `"Why the flies found the murderer"` for a narrated historical mystery.
- `"The harness is the missing layer"` for a technical explanation of harnesses.

---

## 3. Top HUD Headline Specification

- **Length**: strictly 3 to 6 words.
- **Character count**: maximum 38 characters.
- **Casing**: Title Case (`Why SQLite Beats Postgres`).
- **Punctuation**: zero trailing punctuation.
- **Content**: verified transcript terms or a faithful paraphrase; no debug tokens or template placeholders.
- **Redundancy**: checked against the opening spoken text (Section 4).

---

## 4. Curiosity-Gap Redundancy Gate (`resolve_redundant_headline`)

If the first spoken sentence is *"I just deleted our production database"* and the HUD reads *"I Deleted Our Production Database"*, the viewer experiences full redundancy and no question is posed.

### Lexical Overlap Test
Let $T_{\text{spoken}}$ be the lemmatized words in the first $3.0\text{s}$, and $T_{\text{headline}}$ the words in the candidate headline.

$$\text{Overlap Ratio} = \frac{|T_{\text{headline}} \cap T_{\text{spoken}}|}{|T_{\text{headline}}|}$$

### Gate Enforcement
- **If $\text{Overlap Ratio} \le 0.65$**: approved.
- **If $\text{Overlap Ratio} > 0.65$**: redundancy triggered. Reformulate into a **Curiosity Thesis Question** or an **Impact Consequence**:
  - Verbatim spoken: "We rewrote the entire engine in Rust last month."
  - Failed headline: "Rewrote The Engine In Rust"
  - Reformulated headline: "Was The Rust Rewrite Worth It"

Apply the same test between the YouTube title and the HUD headline. Different layers may share one key term, but not the same phrasing.

---

## 5. YouTube Title Architecture

- **Length**: 45–65 characters.
- **Shape**: primary hook or question + contextual specificity + `#Shorts`.
- **Accuracy**: every entity, number, and outcome must be supported by the cut.
- **Examples**:
  - `Why SQLite Beats PostgreSQL For 95% Of Apps #Shorts`
  - `The Silent Bug That Crashed CrowdStrike #Shorts`
  - `How Flies Solved A Medieval Murder #Shorts`

### Tags and Description
- 5–8 high-relevance niche hashtags matching the creator and subject.
- Educational fair-use attribution when required.
- Campaign-required mentions and hashtags from the loaded config.

---

## 6. Dedicated Thumbnail Stage

The thumbnail is built separately from the video overlays.

### Rules
- Exactly one primary headline.
- No subtitle fragments.
- No duplicated headline card.
- Face and eyes unobstructed.
- Supporting image immediately communicates the subject.
- Campaign branding only when required or permitted.
- Readable at small mobile display size (about 120px wide preview).
- Semantically consistent with the video, not a verbatim copy of the HUD.

### Construction
1. Select a frame at the strongest visual moment, or build a clean composition.
2. Keep the face in the clear; reserve a text zone with sufficient contrast.
3. Place one headline of 2–5 words.
4. If a supporting graphic is needed, use one simple subject cue (sickle and flies, architecture node, trade-off diagram).
5. Export at $1080 \times 1920$ (or the campaign-required size).
6. Run OCR to confirm exactly one headline and no subtitle text.
7. Run face landmarks to confirm eyes and mouth are clear.

### Rejection
`THUMBNAIL_DUPLICATE_HEADLINE`, `THUMBNAIL_SUBTITLE_FRAGMENT`, `THUMBNAIL_FACE_OCCLUDED`, `THUMBNAIL_UNREADABLE`.

---

## 7. Packaging QA Checklist

- HUD headline: 3–6 words, $\le 38$ chars, no trailing punctuation, overlap $\le 0.65$.
- YouTube title: 45–65 chars, faithful, entities verified.
- Thumbnail: one headline, no subtitle fragments, face clear, mobile-readable.
- Captions: verbatim from verified transcript.
- Campaign caption and hashtags: validated against config.
- No layer contains debug text, placeholders, or internal variable names.
- Packaging JSON records the evidence for each entity and number.
