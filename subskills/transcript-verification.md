# Subskill: Transcript Verification & Terminology Assurance

ASR output is evidence, not truth. A clip's packaging, captions, and scoring are only as reliable as the transcript beneath them. Verify before cutting, packaging, or publishing.

---

## 1. The Failure This Prevents

A previous Theo edit displayed `LMM` where the speaker said `LLM`. The error propagated into the title and captions. A second batch leaked debug filter text into the render because unvalidated strings reached the overlay.

Verification must catch:

- Acronym and term substitutions (`LLM`/`LMM`, `Postgres`/`PostgresQL`).
- Named-entity errors (people, products, companies, places).
- Dropped negations (`not`, `never`, `no`).
- Number, unit, and date errors.
- Low-confidence ASR spans that were silently accepted.
- Unresolved template placeholders or internal variable names in display text.

---

## 2. Verification Pipeline

```
[ Raw audio ]
     |
     v
[ Primary ASR (Whisper) + word timestamps + confidence ]
     |
     v
[ Forced alignment / re-score against corrected text ]
     |
     +--> [ Domain terminology dictionary ]
     +--> [ Entity and acronym checks ]
     +--> [ Original source subtitle diff, if available ]
     +--> [ Anomaly detection for unusual substitutions ]
     |
     v
[ Verified transcript + confidence map + flagged spans ]
     |
     v
[ Human review of low-confidence terminology ]
```

### Step 1 — Primary ASR
- Transcribe with word-level timestamps and per-word confidence where available.
- Preserve punctuation and casing hypotheses for boundary snapping.
- Never discard the raw ASR output; keep it for diffing.

### Step 2 — Domain Dictionary
Load a domain lexicon before transcription scoring:

```yaml
domains:
  software:
    terms: [LLM, API, Postgres, PostgreSQL, React, TypeScript, Rust, SQLite, ORM, harness]
    case_sensitive: [LLM, API, PostgreSQL, TypeScript]
  science:
    terms: [entomology, forensic, myiasis, Diptera]
  history:
    terms: [sickle, magistrate, coroner, Song Dynasty]
```

- Build per-creator lexicons from previous verified transcripts when available.
- Apply dictionary-constrained re-scoring: a high-edit-distance match to a known term outranks a plausible but wrong common word.

### Step 3 — Entity and Acronym Checks
- Extract named entities from the transcript.
- Confirm each entity against the dictionary, source title/description, or a trusted reference.
- Flag any acronym that is not in the domain lexicon.
- Flag any entity that appears once and has low ASR confidence.

### Step 4 — Original Subtitle Diff
When the source video has captions or subtitles:
1. Download or extract them.
2. Align by timestamp.
3. Diff generated transcript against source subtitles.
4. Treat disagreements as flags, not automatic corrections; source captions can also be wrong.
5. Human-review unresolved disagreements that affect meaning, names, or numbers.

### Step 5 — Anomaly Detection
Flag spans that look wrong even with high confidence:

- Acronym with unusual casing or letter substitution.
- Technical term adjacent to a common word with no semantic link.
- Number followed by an implausible unit.
- Sudden topic shift inside one sentence.
- Repeated word or stutter that changes meaning.

### Step 6 — Human Review
Send to `HUMAN_REVIEW` when:
- A low-confidence span contains a name, number, negation, or technical term.
- The original subtitle diff disagrees on meaning.
- A required campaign mention cannot be verified.
- The transcript cannot support the intended title without speculation.

---

## 3. Confidence Thresholds

| Condition | Action |
| :--- | :--- |
| Word confidence $\ge 0.90$ and term in dictionary | Accept |
| $0.70 \le$ confidence $< 0.90$, no critical term | Accept with flag |
| Confidence $< 0.70$ on a critical term | Human review |
| Any unresolved negation or number conflict | Human review |
| Required campaign phrase unverified | Human review |

Critical terms: names, products, companies, numbers, units, negations, and domain terminology.

---

## 4. Verified Transcript Contract

The verified transcript is the only text source allowed downstream:

```json
{
  "clip_id": "string",
  "language": "en",
  "words": [
    {"text": "LLM", "start": 0.42, "end": 0.61, "confidence": 0.97, "verified": true}
  ],
  "entities": [
    {"text": "Theo", "type": "PERSON", "verified": true, "evidence": "source_title"}
  ],
  "flags": [
    {"span": "0.42-0.61", "term": "LLM", "reason": "acronym_confirmed", "action": "accepted"}
  ],
  "source_subtitle_diff": {"available": true, "unresolved": []},
  "verification_status": "PASS | HUMAN_REVIEW"
}
```

- Captions, HUD headlines, titles, and thumbnails may only use verified words or faithful paraphrases of verified meaning.
- Overlay strings must be rendered from this structured data, never from raw filter-graph source text.
- Any placeholder token (`{HEADLINE}`, `None`, `null`) is a render-blocking defect.

---

## 5. Packaging Integration

Before generating metadata:

1. Confirm `verification_status == "PASS"`.
2. Pull entities and numbers only from verified fields.
3. Run the curiosity-gap overlap test on verified tokens.
4. Validate that no title or thumbnail claim exceeds what the verified cut supports.
5. Record the evidence trail for every entity and number in the packaging JSON.

If verification fails, stop. Do not let a plausible-sounding hallucination become a title.
