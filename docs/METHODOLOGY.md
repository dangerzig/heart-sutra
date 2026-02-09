# Methodology: A Modern Critical Edition of the Heart Sūtra

## Purpose

This document outlines the methodological principles governing this critical edition of the Heart Sūtra (Prajñāpāramitāhṛdaya). Following current scholarship on the text's origin, transmission, and multilingual history, this edition adopts an approach fundamentally different from traditional Lachmannian textual criticism.

## 1. Abandoning the Single-Original-Text Assumption

This edition explicitly rejects the goal of reconstructing a single "Ur-text," especially an Ur-Sanskrit. Strong evidence indicates that the Heart Sūtra was likely composed in Chinese and only later rendered into Sanskrit and Tibetan.

### Stated Aim

To reconstruct the earliest recoverable **Chinese composition** and to document the subsequent multilingual textualization of that composition.

### Key Scholarship

- **Nattier, Jan (1992)**. "The Heart Sūtra: a Chinese apocryphal text?" *Journal of the International Association of Buddhist Studies* 15(2): 153-223.
- **Attwood, Jayarava (2017-2020)**. Series of articles in *Journal of the Oxford Centre for Buddhist Studies* extending Nattier's analysis.

## 2. The Object of Study: A Textual Complex

The Heart Sūtra is treated as a constellation of related but non-equivalent textual forms:

| Tradition | Status | Relationship |
|-----------|--------|--------------|
| Chinese extract-text | Compositionally prior | Analytical base |
| Chinese ritualized recensions | Secondary development | Short and long versions |
| Tibetan translation | Mediating witness | May preserve earlier Sanskrit forms |
| Sanskrit witnesses | Derived tradition | Evidence of back-translation |

These witnesses do not stand in equal relation to a single archetype and must not be treated as such.

## 3. Chinese Base Text

### Selection: Taishō 251 (T251)

The edition selects T251 (Xuanzang's translation, 649 CE) as the analytical base text:

- **260 characters** - the standard short recension
- **First to use "Heart" (心) in the title**
- **Most widely used** in East Asian Buddhist practice
- **Compositionally central** according to Nattier's analysis

### Clarification

The base text is:
- Compositionally central
- Historically prior in probability
- **NOT** privileged as doctrinally or ritually superior

## 4. Witness Classification

### Chinese Witnesses (Taishō Canon)

| Siglum | Title | Date | Recension |
|--------|-------|------|-----------|
| T250 | 摩訶般若波羅蜜大明咒經 | c. 402-412 | Long |
| T251 | 般若波羅蜜多心經 | 649 | Short (base) |
| T252 | 般若波羅蜜多心經 | c. 700 | Short |
| T253 | 般若波羅蜜多心經 | c. 700-730 | Long |
| T254 | 普遍智藏般若波羅蜜多心經 | c. 733 | Long |
| T255 | 般若波羅蜜多心經 | c. 790 | Long |
| T256 | 般若波羅蜜多心經 (唐梵翻對字音) | c. 7th-8th c. | Transliterated Sanskrit |
| T257 | 般若波羅蜜多心經 | c. 850-1000 | Long |

### Sanskrit Witnesses

Following Conze (1967) with updates:

**Japanese Provenance:**
- Ja: Hōryū-ji palm-leaf (c. 8th century)
- Jb: Hase-ji long text (c. 9th century)

**Nepalese Provenance:**
- Na-Nl: Various manuscripts (13th-19th centuries)

**Chinese Provenance:**
- Ca-Cg: Blockprints, inscriptions, Dunhuang manuscripts

**Central Asian:**
- Gilgit fragments (c. 6th-7th century)

### Tibetan Witnesses

- Toh 21: Degé Kangyur (Prajñāpāramitā section)
- Toh 531: Degé Kangyur (Tantra section)
- Stok Palace Kangyur (alternative recension)
- IOL Tib J 751: Dunhuang manuscript (c. 823 CE)

## 5. Sanskrit as Derived Tradition

Sanskrit witnesses are presented as evidence of **reception and re-Sanskritization**, not as controls for correcting Chinese readings.

### Evidence of Back-Translation

1. **Non-idiomatic vocabulary**: Uses *kṣaya* (destruction) instead of standard *nirodha* (cessation)
2. **Grammatical anomalies**: Unusual verb tenses for sūtra style
3. **Structural mismatches**: Segments that presuppose Chinese word order

### Editorial Practice

The apparatus will:
- Present Sanskrit texts synoptically
- Flag readings that presuppose Chinese syntax or idiom
- Annotate likely back-translations or misunderstandings

## 6. Tibetan as Mediating Witness

Tibetan witnesses serve as independent but mediating evidence:

- May reflect **earlier Sanskrit forms** than surviving Indic manuscripts
- Still participate in a **secondary transmission chain**
- Used to **triangulate stages of Sanskritization**

## 7. Direction-of-Dependence Annotation

The apparatus explicitly marks probable directions of borrowing:

| Code | Meaning |
|------|---------|
| PP→HS | Larger Prajñāpāramitā → Heart Sūtra extraction |
| ZH→SA | Chinese → Sanskrit (back-translation) |
| ZH→BO | Chinese → Tibetan |
| BO→SA | Tibetan → Sanskrit |
| SA→BO | Sanskrit → Tibetan |

This transforms the critical apparatus into an **argument about textual history** rather than a neutral list of variants.

## 8. Variant Classification

Variants are categorized, not merely listed:

| Type | Description |
|------|-------------|
| Orthographic | Spelling differences without semantic change |
| Scribal Error | Clear copying mistakes |
| Stylistic | Improvements to flow/readability |
| Doctrinal | Alignment with doctrinal norms |
| Extraction Artifact | Traces of source Prajñāpāramitā text |
| Back-translation | Evidence of translation from Chinese |
| Distinctive | Genuinely different textual reading |

## 9. Parallel Presentation

The edition includes two parallel components:

1. **Critically edited Chinese text** with full apparatus
2. **Multilingual synoptic alignment** (Chinese, Sanskrit, Tibetan) with commentary explaining divergences

Collapsing these into a single "clean" text would obscure the text's historical complexity.

## 10. Dual-Script Sanskrit

Sanskrit is presented in both:
- **Devanagari** (देवनागरी) - for traditional readability
- **IAST** (International Alphabet of Sanskrit Transliteration) - for scholarly precision

## 11. Commentary Focus

The commentary prioritizes questions of **composition and textual formation**:

- Why specific phrases were selected from larger PP texts
- Why register shifts occur
- How extraction and condensation function
- Why the mantra appears where it does

Doctrinal explanation is secondary to historical and philological analysis.

## 12. Transparency About Limits

This edition clearly states:
- Which conclusions are probabilistic
- Where evidence is insufficient
- What cannot be recovered or decided

The goal is not to resolve all questions, but to **stabilize scholarly discussion** with transparent methods and evidence.

## 13. Reproducible Collation Pipeline

The edition is supported by a computational pipeline that makes the chain from source data to scholarly claims explicit and reproducible.

### Data Layer

Witness texts are stored as structured JSON files under `data/`:

```
data/
├── chinese/
│   ├── taisho/          # T250.json, T251.json, T256.json, T257.json
│   ├── dunhuang/        # dunhuang_manuscripts.json (catalog)
│   └── epigraphy/       # fangshan_stele.json (661 CE)
├── sanskrit/
│   └── gretil/          # prajnaparamitahrdaya.json (IAST + Devanagari)
├── tibetan/
│   └── kangyur/         # toh21.json (Degé Kangyur)
└── collation/
    └── variant_table.json  # Pre-identified critical variants
```

Each witness file contains `segments` — discrete text units aligned by section and position. Segments carry parallel references (`chinese_parallel`) enabling cross-linguistic alignment.

### Collation Engine (`hrdaya.collate`)

The collation engine takes T251 as the analytical base and aligns witnesses in three dimensions:

1. **Inter-Chinese collation**: T251 vs T250 (and other Taishō witnesses) — matched by section name and segment position within section
2. **Cross-linguistic alignment**: Chinese segments matched to Sanskrit and Tibetan via `chinese_parallel` references
3. **Variant detection**: Automated classification of differences using the criteria in `research/VARIANT_CLASSIFICATION_CRITERIA.md`

**Variant detection steps:**
- Orthographic check: normalize (strip diacritics, lowercase), compare with SequenceMatcher (threshold > 0.9)
- Back-translation check: compare Sanskrit against standard Prajnaparamita vocabulary (kṣaya/nirodha indicators)
- Extraction artifact check: scan for dialogue markers and honorifics from larger PP texts
- Default: distinctive reading with uncertain direction of dependence

### Synoptic Alignment (`hrdaya.synoptic`)

The synoptic builder generates parallel presentations in three formats:
- **Markdown**: Human-readable, suitable for paper appendix
- **HTML**: Parallel-column table for interactive viewing
- **JSON**: Machine-readable with full provenance metadata

### Validation (`hrdaya.validate`)

All JSON witness files are validated against expected schemas:
- Chinese segments require: `id`, `section`, `text`
- Sanskrit segments require: `id`, `section`, `iast`
- Tibetan segments require: `id`, `section`, `tibetan`

### Reproducibility

All outputs include provenance metadata:
```json
{
  "provenance": {
    "generated": "2026-02-08T...",
    "tool": "hrdaya.collate",
    "version": "1.0.0",
    "base_witness": "T251"
  }
}
```

To reproduce from source:
```bash
# Install
pip install -e .

# Run collation
hrdaya-collate > collation_output.json

# Generate synoptic alignment
hrdaya-synoptic markdown > synoptic.md
hrdaya-synoptic html > synoptic.html
hrdaya-synoptic json > synoptic.json

# Validate data files
python -c "from hrdaya.validate import validate_data_dir; from pathlib import Path; print(validate_data_dir(Path('data')))"

# Run tests (61 tests)
PYTHONPATH=src pytest tests/ -v
```

### Limitations

- The pipeline operates on **published editions**, not primary manuscripts (see `research/PRIMARY_MANUSCRIPT_LIMITATIONS.md`)
- Variant classification uses heuristic rules, not a trained model; results should be reviewed by a scholar
- Cross-linguistic alignment relies on pre-annotated `chinese_parallel` references, not automatic alignment

## Summary

A genuinely modern critical edition of the Heart Sūtra is:
- **Multilingual** - Chinese, Sanskrit, Tibetan in parallel
- **Non-archetypal** - no single Ur-text assumed
- **Explicit about directionality** - apparatus encodes transmission history
- **Historically staged** - acknowledges compositional priority
- **Transparent about uncertainty** - probabilistic, not dogmatic

Such an edition functions less as a reconstruction of a lost original and more as a **documented history of how a sūtra was made**.

---

## Bibliography

### Primary Scholarship

- Conze, Edward (1967). "The Prajñāpāramitā-Hṛdaya Sūtra." In *Thirty Years of Buddhist Studies*, pp. 147-167.
- Müller, F. Max (1881). "The Ancient Palm Leaves." *Journal of the Royal Asiatic Society*.
- Nattier, Jan (1992). "The Heart Sūtra: a Chinese apocryphal text?" *JIABS* 15(2): 153-223.
- Silk, Jonathan A. (1994). *The Heart Sūtra in Tibetan: A Critical Edition of the Two Recensions Contained in the Kanjur*. Vienna.

### Recent Scholarship

- Attwood, Jayarava (2015). "Heart Murmurs: Some Problems with Conze's Prajñāpāramitāhṛdaya." *JOCBS* 12: 28-62.
- Attwood, Jayarava (2017). "Form is (Not) Emptiness: The Enigma at the Heart of the Heart Sutra." *JOCBS* 13: 52-80.
- Attwood, Jayarava (2018). "A Note on Nisthanirvana in the Heart Sutra." *JOCBS* 14: 10-17.
- Attwood, Jayarava (2020). "Ungarbling Section VI of the Sanskrit Heart Sutra." *JOCBS* 18: 11-41.
- Karashima, Seishi et al. (2016). *Gilgit Manuscripts in the National Archives of India*. Tokyo: Soka University.

### Digital Resources

- 84000: Translating the Words of the Buddha. https://84000.co/
- CBETA Chinese Electronic Tripiṭaka. https://cbetaonline.dila.edu.tw/
- Digital Sanskrit Buddhist Canon. https://www.dsbcproject.org/
- GRETIL. https://gretil.sub.uni-goettingen.de/

---

*Last updated: February 2026*
