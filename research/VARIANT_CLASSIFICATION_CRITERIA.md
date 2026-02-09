# Variant Classification Criteria: Formal Definitions and Worked Examples

*Phase 4, TODO #7 — February 2026*

---

## Purpose

This document defines explicit, replicable criteria for classifying textual variants in the Heart Sutra critical edition. The goal is that another scholar, applying these criteria to the same data, would reach the same classifications.

---

## Classification Framework

### 1. Orthographic Variant

**Definition:** Two readings that represent the same word or phrase with different spelling, character forms, or transliteration conventions. No semantic difference.

**Criteria (all must be met):**
- The two readings refer to the same morpheme or word
- No change in meaning, doctrinal content, or syntactic structure
- Difference is explicable by scribal convention, regional orthography, or transliteration standard

**Worked Examples:**

| Base (T251) | Variant | Source | Classification | Reasoning |
|-------------|---------|--------|---------------|-----------|
| 無 (wú) | 无 | Fangshan Stele | Orthographic | Simplified form of same character; both mean "without/not" |
| 咒 (zhòu) | 呪 | Fangshan Stele | Orthographic | Character variant for "mantra"; same pronunciation and meaning |
| prajñāpāramitā | prajnaparamita | Various | Orthographic | With/without diacritical marks in IAST; same word |

**Decision procedure:**
1. Normalize both readings (strip diacritics, normalize character forms)
2. If normalized forms are identical or SequenceMatcher ratio > 0.9: orthographic
3. Otherwise: proceed to other categories

---

### 2. Back-Translation Indicator

**Definition:** A Sanskrit reading that shows evidence of having been translated from Chinese rather than composed originally in Sanskrit. Following Nattier (1992).

**Criteria (at least one must be met):**
- **Non-standard vocabulary:** Sanskrit uses a word not standard in Prajnaparamita literature where the Chinese could motivate the choice
- **Chinese word order:** Sanskrit follows Chinese syntactic patterns rather than standard Sanskrit
- **Semantic calque:** Sanskrit renders a Chinese idiom literally rather than using the conventional Sanskrit equivalent

**Worked Examples:**

| Chinese | Sanskrit | Standard Sanskrit | Classification | Reasoning |
|---------|----------|-------------------|---------------|-----------|
| 盡 (jìn, "exhaustion") | kṣaya | nirodha | Back-translation | Standard PP Sanskrit uses *nirodha* for cessation. The Chinese 盡 can mean either "exhaustion" or "cessation." A back-translator chose *kṣaya* (exhaustion), the more literal rendering of 盡, rather than the conventional *nirodha*. This is Nattier's central evidence. |
| 無老死 (wú lǎo sǐ) | na jarāmaraṇam | na jarāmaraṇa-nirodho (standard) | Back-translation | The Chinese negates "old-age-death" directly. Sanskrit follows this Chinese pattern rather than the standard PP formula which negates the *nirodha* (cessation) of old-age-and-death. |
| 度一切苦厄 (dù yīqiè kǔ'è) | (absent in Sanskrit) | — | Extraction artifact (see below) | Present in Chinese T251 but absent from Sanskrit — suggests this phrase was part of the Chinese composition and was not back-translated. |

**Decision procedure:**
1. Compare Sanskrit term against standard Prajnaparamita usage (T223 Sanskrit parallel, Pañcaviṃśatisāhasrikā)
2. If Sanskrit deviates from standard AND the deviation is explicable by Chinese source: back-translation
3. If multiple back-translation indicators cluster in the same passage: high confidence

---

### 3. Extraction Artifact

**Definition:** A textual feature that reveals the Heart Sutra passage was extracted from a larger Prajnaparamita text, preserving traces of the source context.

**Criteria (at least one must be met):**
- **Dialogue markers** present that assume a larger sutra context (e.g., "evam ukte" = "thus spoken")
- **Contextual references** to characters or situations from the larger sutra not present in the Heart Sutra itself
- **Structural seams** where extracted material was joined, producing grammatical or logical discontinuities

**Worked Examples:**

| Feature | Location | Classification | Reasoning |
|---------|----------|---------------|-----------|
| "evam ukte" (thus spoken) | Sanskrit long recension opening | Extraction artifact | This dialogue formula presupposes a conversational setting from the Aṣṭasāhasrikā/Pañcaviṃśatisāhasrikā, not present in the short recension |
| "āyuṣmān Śāriputra" (venerable Śāriputra) | Sanskrit long recension | Extraction artifact | The honorific "āyuṣmān" is a standard discourse marker in larger PP texts |
| T250 includes 色不異空 + individual skandha characteristics | T250 form_emptiness section | Extraction artifact | T250 preserves more of the T223 source passage; T251 condensed it. The "extra" material in T250 matches T223 exactly. |

**Decision procedure:**
1. Check if the feature has a parallel in T223 (Kumārajīva's Large PP)
2. If the feature is present in T223 but absent from the shorter Heart Sutra version: extraction artifact
3. If it contains dialogue markers or honorifics from the larger sutra context: extraction artifact

---

### 4. Distinctive Reading

**Definition:** A genuine textual variant where two witnesses preserve different substantive readings that cannot be explained by orthography, back-translation, or extraction.

**Criteria:**
- Not orthographic (semantic difference exists)
- Not explicable as back-translation artifact
- Not explicable as extraction trace
- Represents a genuine divergence in textual tradition

**Worked Examples:**

| T251 | T250 | Classification | Reasoning |
|------|------|---------------|-----------|
| 觀自在菩薩 (Guānzìzài Púsà) | 觀世音菩薩 (Guānshìyīn Púsà) | Distinctive reading | Different name for Avalokiteśvara. T250 uses older Kumārajīva-era translation; T251 uses Xuanzang's new translation. This reflects different translation conventions, not a scribal error. |
| 五蘊 (wǔyùn) | 五陰 (wǔyīn) | Distinctive reading | Different Chinese translations of *skandha*. 五蘊 is Xuanzang's standard; 五陰 is Kumārajīva's standard. Systematic: T250 consistently uses Kumārajīva-era terms, T251 uses Xuanzang-era terms. |
| 色不異空 (sè bù yì kōng) | 非色異空 (fēi sè yì kōng) | Distinctive reading | Different syntactic construction expressing the same meaning ("form is not different from emptiness" vs "it is not the case that form differs from emptiness"). The T250 phrasing matches T223 more closely. |
| 遠離 (yuǎnlí) | 離 (lí) | Distinctive reading | T251 uses compound form "far-remove"; T250 uses simple form matching T223. |
| Four epithets (大神呪, 大明呪, 無上呪, 無等等呪) | Three epithets (大明呪, 無上明呪, 無等等明呪) | Distinctive reading | T251 has four epithets; T250 has three with consistent 明呪 terminology. The three-epithet pattern matches T223. |

**Decision procedure:**
1. Verify the reading difference is not orthographic (different meaning or syntax)
2. Check whether the difference correlates with known translation convention differences (Kumārajīva vs Xuanzang)
3. If both readings are meaningful and neither is clearly an error: distinctive reading

---

### 5. Scribal Error

**Definition:** A reading that is clearly the result of a copying mistake, not intentional.

**Criteria (at least one must be met):**
- Reading produces nonsensical text
- Reading is a known scribal confusion (e.g., similar-looking characters)
- Reading is corrected in a later hand in the same manuscript
- Reading is unique to one witness and contradicts all others

**Worked Examples:**

| Reading | Expected | Source | Classification | Reasoning |
|---------|----------|--------|---------------|-----------|
| pañcaskandhāḥ (nominative) | pañcaskandhāṃs (accusative) | Conze's edition | Scribal error / editorial error | Grammatical error: Avalokiteśvara "saw" (accusative required) the five aggregates, not "the five aggregates" (nominative). Huifeng (2014) corrects. |

**Decision procedure:**
1. Does the reading make grammatical or semantic sense?
2. Is it unique to one witness or a small family?
3. If nonsensical and isolated: scribal error

---

### 6. Doctrinal Harmonization

**Definition:** A reading that has been adjusted to conform to doctrinal expectations or standard formulations.

**Criteria:**
- Reading differs from source in a way that improves doctrinal consistency
- The change aligns the text with standard Buddhist doctrine or common formulations

**Worked Examples:**

| Feature | Classification | Reasoning |
|---------|---------------|-----------|
| Sanskrit long recension adds elaborate Tantric maṅgala salutation | Doctrinal harmonization | Later Nepalese manuscripts added a Tantric-style invocation to align the text with Tantric ritual practice. The Hōryū-ji manuscript has the simpler "namaḥ sarvajñāya." |
| "yad rūpaṃ sā śūnyatā" (form itself is emptiness) line in Sanskrit | Possible doctrinal harmonization | This line is absent from ALL Chinese texts. It may have been added in the Sanskrit tradition to make the emptiness doctrine more explicit. |

---

### 7. Stylistic Smoothing

**Definition:** A change that improves literary quality without altering meaning.

**Criteria:**
- No semantic change
- The variant reading is more euphonious, balanced, or rhetorically polished
- The change is consistent with known stylistic preferences of the translator/editor

**Worked Examples:**

| T250 | T251 | Classification | Reasoning |
|------|------|---------------|-----------|
| 亦如是 (yì rúshì) | 亦復如是 (yì fù rúshì) | Stylistic smoothing | Both mean "likewise." T251 adds the intensifier 復, a common Xuanzang stylistic preference for four-character phrases. |

---

## Application Procedure

When classifying a variant between two witnesses:

1. **Normalize** both readings (strip orthographic variation)
2. **If identical after normalization:** Orthographic variant
3. **If one is Chinese and the other Sanskrit:** Check for back-translation indicators
4. **If one preserves more T223 material:** Check for extraction artifact
5. **If both are meaningful Chinese readings:** Check for known translation convention patterns (Kumārajīva vs Xuanzang)
6. **If the reading makes no sense:** Scribal error
7. **If the reading adjusts doctrinal content:** Doctrinal harmonization
8. **Otherwise:** Distinctive reading with direction of dependence set to UNCERTAIN

## Confidence Levels

| Confidence | Criteria |
|-----------|---------|
| **High (0.8-1.0)** | Multiple independent indicators; matches known pattern; confirmed by secondary literature |
| **Medium (0.5-0.8)** | Single indicator; plausible but not conclusive; one supporting scholarly reference |
| **Low (0.2-0.5)** | Classification uncertain; multiple interpretations possible; noted as provisional |
| **Minimal (0.0-0.2)** | Best guess only; insufficient evidence to classify with any confidence |

---

*This document addresses PAPER_TODOS #7 and PEER_REVIEW Specific Issue 2.*
