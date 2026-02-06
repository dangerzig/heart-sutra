# Heart Sūtra Critical Edition - Architecture Document

## Executive Summary

This project implements a **multilingual electronic critical edition** of the Prajñāpāramitāhṛdaya (Heart Sūtra) following a methodology fundamentally different from traditional Lachmannian textual criticism. Rather than reconstructing a hypothetical Sanskrit Ur-text, this edition treats the Heart Sūtra as a **textual complex** with **Chinese compositional priority**, documenting the subsequent multilingual textualization across Chinese, Sanskrit, and Tibetan traditions.

---

## 1. Project Architecture

### 1.1 Directory Structure

```
heart-sutra/
├── src/
│   └── hrdaya/                    # Core Python library
│       ├── __init__.py            # Package initialization & exports
│       ├── models.py              # Data models (634 lines)
│       ├── witnesses.py           # Witness catalog (450+ lines)
│       ├── transliterate.py       # Devanagari ↔ IAST conversion
│       ├── collate.py             # Collation engine
│       └── synoptic.py            # Parallel presentation builder
├── data/
│   ├── chinese/
│   │   ├── taisho/                # Taishō Canon texts
│   │   ├── dunhuang/              # Dunhuang manuscripts
│   │   └── manuscripts/           # Other Chinese witnesses
│   ├── sanskrit/
│   │   ├── gretil/                # GRETIL edition
│   │   ├── dsbc/                  # Digital Sanskrit Buddhist Canon
│   │   └── manuscripts/           # Organized by provenance
│   │       ├── nepalese/          # Na-Nl (Conze sigla)
│   │       ├── japanese/          # Ja, Jb
│   │       ├── chinese-inscriptions/  # Ca-Cg
│   │       └── central-asian/     # Gilgit, Dunhuang
│   ├── tibetan/
│   │   ├── kangyur/               # Canonical versions
│   │   └── dunhuang/              # Early manuscripts
│   ├── prajnaparamita/            # Source texts (Large PP parallels)
│   ├── collation/                 # Collation output
│   ├── critical/                  # Critical edition output
│   └── aligned/                   # Synoptic alignments
├── docs/
│   ├── ARCHITECTURE.md            # This document
│   └── METHODOLOGY.md             # Scholarly methodology
├── scripts/
│   └── generate_synoptic.py       # Output generation
└── README.md                      # Project overview
```

### 1.2 Core Library Modules

#### `models.py` - Data Models

Defines the fundamental data structures for the critical edition:

| Class | Purpose |
|-------|---------|
| `WitnessType` | Enum: CHINESE, SANSKRIT, TIBETAN, SOURCE, PARALLEL |
| `Script` | Enum: TRADITIONAL_CHINESE, DEVANAGARI, IAST, TIBETAN, WYLIE |
| `VariantType` | Classification of textual variants (11 types) |
| `DependenceDirection` | Direction of textual borrowing (7 directions) |
| `Token` | Single word with linguistic analysis |
| `Segment` | Text segment in one language/witness |
| `Variant` | Textual variant with full apparatus annotation |
| `Witness` | Manuscript/edition metadata |
| `MultilingualSegment` | Aligned segments across all traditions |
| `CriticalApparatus` | Complete apparatus for the edition |

#### `witnesses.py` - Witness Catalog

Comprehensive catalog of all witnesses with scholarly metadata:

```python
CHINESE_WITNESSES = {...}      # 10 witnesses (T250-T257, S2464, + T223 as SOURCE)
SANSKRIT_WITNESSES = {...}     # 21 witnesses (Ja-Jb, Na-Nl, Ca-Cg, Gilgit, + Pañcaviṃśatisāhasrikā as PARALLEL)
TIBETAN_WITNESSES = {...}      # 4 witnesses (Toh21, Toh531, Stok, IOL_J751)
```

#### `transliterate.py` - Script Conversion

Bidirectional conversion between Devanagari and IAST:

```python
devanagari_to_iast("प्रज्ञापारमिता")  # → "prajñāpāramitā"
iast_to_devanagari("śūnyatā")         # → "शून्यता"
```

#### `collate.py` - Collation Engine

Implements multilingual collation with:
- Chinese as analytical base
- Direction-of-dependence classification
- Variant type identification
- Cross-linguistic alignment

#### `synoptic.py` - Parallel Presentation

Generates synoptic alignments in multiple formats:
- Markdown (for documentation)
- HTML (for web viewing)
- JSON (for programmatic access)

---

## 2. Witnesses Included

### 2.1 Chinese Witnesses (Compositionally Prior)

The Chinese tradition is treated as **compositionally prior** following Nattier (1992). The edition includes all major Taishō Canon versions:

| Siglum | Title | Date | Recension | Rationale |
|--------|-------|------|-----------|-----------|
| **T251** | 般若波羅蜜多心經 | 649 CE | Short | **Base text**. Xuanzang's translation. First to use "Heart" (心) in title. Most widely used. |
| T250 | 摩訶般若波羅蜜大明咒經 | c. 402-412 | Long | Attributed to Kumārajīva. Earliest Chinese witness (attribution disputed). |
| T252 | 般若波羅蜜多心經 | c. 700 | Short | Alternate short version for comparison. |
| T253 | 般若波羅蜜多心經 | c. 700-730 | Long | Fayue's translation. Long version with frame narrative. |
| T254 | 普遍智藏般若波羅蜜多心經 | c. 733 | Long | Prajñā's translation. |
| T255 | 般若波羅蜜多心經 | c. 790 | Long | Prajñācakra's translation. |
| **T256** | 般若波羅蜜多心經 (唐梵翻對字音) | c. 7th-8th c. | Transliterated | **Critical witness**. Sanskrit transliterated into Chinese characters. Key evidence for back-translation thesis. |
| T257 | 般若波羅蜜多心經 | c. 850-1000 | Long | Facheng's translation. May be based on Tibetan. |
| S2464 | Stein Collection | c. 600-700 | Short | Dunhuang manuscript. Early physical witness. |

**Selection Rationale**: T251 is the analytical base because it is (1) compositionally central according to Nattier's analysis, (2) the most widely used recension, and (3) the first to use the distinctive "Heart Sūtra" title. T256 is critical for demonstrating the Chinese → Sanskrit transmission.

### 2.2 Sanskrit Witnesses (Derived Tradition)

Sanskrit witnesses are treated as evidence of **reception and re-Sanskritization**, not as sources for correcting Chinese readings. Following Conze (1967) with updates:

#### Japanese Provenance

| Siglum | Name | Date | Rationale |
|--------|------|------|-----------|
| **Ja** | Hōryū-ji Palm-leaf | c. 8th c. | Earliest undated Sanskrit manuscript. Despite traditional 609 CE date (unreliable), provides earliest physical Sanskrit evidence. Shows significant scribal errors indicating secondary transmission. |
| Jb | Hase-ji Long Text | c. 9th c. | Long version brought from China. Evidence of East Asian Sanskrit transmission. |

#### Nepalese Provenance

| Siglum | Name | Date | Rationale |
|--------|------|------|-----------|
| Na | India Office 7712 | c. 18th c. | Representative of late Nepalese tradition. |
| **Nb** | Cambridge Add. 1485 | 1677 CE | Well-preserved, precisely dated. Gold on black paper in Rañjana script. |
| Nc | Bodleian 1449 | 1819 CE | Comparison witness. |
| Nd | RAS no. 79 V | c. 1820 | Comparison witness. |
| Ne | Cambridge Add. 1553 | c. 18th c. | Comparison witness. |
| Nf-Ng | Asiatic Society Bengal | — | Additional comparison. |
| Nh | Cambridge Add. 1164 | — | Fragment (first 6 lines only). |
| Ni | Société Asiatique 14 | — | Long text version in Nepalese tradition. |
| **Nk** | Cambridge Add. 1680 | c. 1200 CE | **One of oldest Nepalese witnesses**. Palm leaf, 13th century. Critical for establishing early Nepalese readings. |

#### Chinese-Provenance Sanskrit

| Siglum | Name | Date | Rationale |
|--------|------|------|-----------|
| Ca | Chinese blockprint | c. 17th c. | Evidence of Chinese Sanskrit preservation. |
| **Cb** | Stein S. 2464 | c. 600-700 | Sanskrit in Chinese characters. Same as T256. **Critical for back-translation thesis**. |
| Cc | Mironov Mongolian | c. 10th-11th c. | Stone inscription. Evidence of Central Asian transmission. |
| Cd | Mironov Bronze Bell | — | Incomplete. Physical inscription evidence. |
| Ce | Feer Polyglot | c. 17th c. | Historical polyglot edition. |
| Cf | Stein Ch. 00330 | c. 850 | Dunhuang Sanskrit. |
| **Cg** | Pelliot Sogdien 62 | c. 950 | Birch bark in Siddham. Central Asian transmission evidence. |

#### Central Asian

| Siglum | Name | Date | Rationale |
|--------|------|------|-----------|
| **Gilgit** | Gilgit Fragments | c. 6th-7th c. | **Earliest Sanskrit fragments**. Covers ~80% of text. Critical for establishing early Sanskrit readings, though still post-dates Chinese composition. |

**Selection Rationale**: All witnesses from Conze's critical edition are included to enable comprehensive comparison. Priority witnesses (bold) are those that either (1) are earliest, (2) are most precisely dated, or (3) provide critical evidence for transmission history.

### 2.3 Tibetan Witnesses (Mediating)

Tibetan witnesses serve as **mediating evidence** that may reflect earlier Sanskrit forms while still participating in a secondary transmission chain:

| Siglum | Name | Date | Rationale |
|--------|------|------|-----------|
| **Toh21** | Degé Kangyur (Prajñāpāramitā section) | c. 9th c. (trans.) | **Primary Tibetan witness**. Long version. Translated by Vimalamitra and Rinchen Dé. Standard canonical version. |
| Toh531 | Degé Kangyur (Tantra section) | c. 9th c. | Alternative canonical location. |
| Stok | Stok Palace Kangyur | — | Alternative recension (Recension B). Differs in title, mantra, phrasings. Critical for understanding Tibetan textual variation. |
| **IOL_J751** | Dunhuang | c. 823 CE | **Earliest dated Tibetan witness**. Late Old Tibetan version. Differs from both Kangyur versions and Sanskrit/Chinese texts. Critical for early transmission. |

**Selection Rationale**: Tibetan is included because (1) it may preserve earlier Sanskrit readings than surviving Indic manuscripts, (2) it provides independent evidence for triangulating transmission stages, and (3) the Dunhuang manuscript (IOL_J751) is one of the earliest precisely dated witnesses in any tradition.

### 2.4 Source and Parallel Texts

The Heart Sūtra's core section was extracted from larger Prajñāpāramitā texts. Rather than grouping these in a separate category, they are included within their respective language collections with distinct `WitnessType` values:

| ID | Title | Date | Type | Language Collection | Rationale |
|----|-------|------|------|---------------------|-----------|
| **T223** | 摩訶般若波羅蜜經 | 404 CE | SOURCE | CHINESE_WITNESSES | Kumārajīva's Chinese translation of the Large PP. **Primary source** from which Heart Sūtra core was extracted. |
| **Pañcaviṃśati_Gilgit** | Pañcaviṃśatisāhasrikā | c. 7th c. | PARALLEL | SANSKRIT_WITNESSES | Sanskrit 25,000-line PP. Contains the passage paralleling the Heart Sūtra core. Critical for demonstrating extraction and back-translation evidence (nirodha vs. kṣaya). |

**Organization Rationale**: Keeping source/parallel texts within their language collections maintains consistent organization while the `WitnessType.SOURCE` and `WitnessType.PARALLEL` values distinguish their functional role. Use `get_witnesses_by_type(WitnessType.SOURCE)` or `get_witnesses_by_type(WitnessType.PARALLEL)` to retrieve these across language boundaries.

---

## 3. Results

### 3.1 Data Files Created

| File | Contents | Status |
|------|----------|--------|
| `data/chinese/taisho/T251.json` | Base text with 12 segments, pinyin, English glosses | Complete |
| `data/sanskrit/gretil/prajnaparamitahrdaya.json` | GRETIL text in IAST + Devanagari with Chinese parallels | Complete |
| `data/tibetan/kangyur/toh21.json` | Long version with Tibetan script + Wylie | Complete |
| `data/prajnaparamita/pancavimsati_parallel.json` | Source extraction data with kṣaya/nirodha analysis | Complete |

### 3.2 Generated Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `data/aligned/synoptic_alignment.md` | Markdown | 12 segments with Chinese, Sanskrit (dual script), Tibetan, English in parallel |
| `data/aligned/synoptic_alignment.html` | HTML | Web-viewable parallel presentation |
| `data/aligned/synoptic_alignment.json` | JSON | Machine-readable alignment for programmatic access |

### 3.3 Scholarly Annotations Implemented

The edition currently includes the following scholarly annotations:

1. **Back-translation evidence**: Segment T251:7/GRETIL:8 notes the use of *kṣaya* instead of *nirodha*, flagged as evidence of Chinese → Sanskrit back-translation (Nattier 1992).

2. **Grammatical anomalies**: Segment GRETIL:2 notes unusual imperfect tense (*vyavalokayati sma*) atypical for sūtra style.

3. **Controversial readings**: Segment GRETIL:10 flags *niṣṭhā-nirvāṇa* as a controversial reading (Attwood 2018).

4. **Frame narrative differences**: Tibetan Toh21 prologue notes that the frame narrative is not present in Chinese short version T251.

### 3.4 Code Statistics

| Module | Lines | Purpose |
|--------|-------|---------|
| `models.py` | 200+ | Data structures |
| `witnesses.py` | 450+ | Witness catalog |
| `transliterate.py` | 200+ | Script conversion |
| `collate.py` | 300+ | Collation engine |
| `synoptic.py` | 350+ | Parallel presentation |
| **Total** | **~1,500** | Core library |

---

## 4. Future Work

### 4.1 Immediate Priorities

#### Additional Witnesses
- [ ] Add remaining Chinese witnesses (T250, T252-257)
- [ ] Add Sanskrit manuscript transcriptions from prajnaparamitahrdaya.wordpress.com (Nb, Nk diplomatic editions)
- [ ] Add Dunhuang Tibetan manuscript (IOL Tib J 751)
- [ ] Add Stok Palace Kangyur variant readings

#### Enhanced Collation
- [ ] Implement word-level alignment algorithm
- [ ] Build variant classification heuristics based on Nattier's criteria
- [ ] Add confidence scoring for direction-of-dependence annotations
- [ ] Create apparatus generation for identified variants

### 4.2 Medium-Term Goals

#### Export Formats
- [ ] **LaTeX/PDF**: Critical edition typesetting using `reledmac` package
  - Parallel text presentation
  - Critical apparatus at foot of page
  - Sigla and witness references
- [ ] **TEI-XML**: Standard scholarly edition format for interoperability
- [ ] **HTML5**: Interactive web edition with hover annotations

#### Analysis Tools
- [ ] Search across all traditions
- [ ] Variant frequency analysis
- [ ] Extraction pattern identification (PP → Heart Sūtra)
- [ ] Back-translation marker detection

#### Lemmatization
- [ ] Sanskrit lemmatization using Digital Pāli Dictionary (DPD) Sanskrit data
- [ ] Chinese word segmentation
- [ ] Tibetan syllable analysis

### 4.3 Long-Term Vision

#### Interactive Edition
- Web-based interface for exploring the textual complex
- Clickable variants with scholarly commentary
- Visual transmission diagram
- Audio pronunciations for Sanskrit and Tibetan

#### Scholarly Commentary
- Section-by-section philological commentary
- Extraction analysis (which PP passages map to which Heart Sūtra sections)
- Translation technique analysis
- Historical contextualization

#### Community Features
- Annotation system for scholarly contributions
- Version control for textual emendations
- Export to Zotero/citation managers

---

## 5. Technical Dependencies

### Current (Standard Library Only)
- `json` - Data serialization
- `pathlib` - Cross-platform paths
- `dataclasses` - Data structures
- `enum` - Enumerations
- `difflib` - Sequence alignment
- `typing` - Type hints

### Planned
- `lxml` - TEI-XML generation
- `jinja2` - Template rendering
- `flask` or `fastapi` - Web interface (optional)

---

## 6. Scholarly Foundation

### Primary Methodology Sources

1. **Nattier, Jan (1992)**. "The Heart Sūtra: a Chinese apocryphal text?" *Journal of the International Association of Buddhist Studies* 15(2): 153-223.
   - Establishes Chinese compositional priority
   - Identifies back-translation evidence
   - Provides extraction analysis from Large PP

2. **Conze, Edward (1967)**. "The Prajñāpāramitā-Hṛdaya Sūtra." In *Thirty Years of Buddhist Studies*, pp. 147-167.
   - Critical edition of Sanskrit text
   - Witness sigla system
   - Manuscript descriptions

3. **Attwood, Jayarava (2015-2020)**. Series in *Journal of the Oxford Centre for Buddhist Studies*.
   - Corrections to Conze's edition
   - Extended back-translation analysis
   - Detailed textual problems

4. **Silk, Jonathan A. (1994)**. *The Heart Sūtra in Tibetan: A Critical Edition of the Two Recensions Contained in the Kanjur*. Vienna.
   - Tibetan critical edition
   - Recension analysis

### Digital Resources Used

- **GRETIL** (Göttingen Register of Electronic Texts in Indian Languages)
- **CBETA** (Chinese Buddhist Electronic Text Association)
- **84000: Translating the Words of the Buddha**
- **Digital Sanskrit Buddhist Canon** (University of the West)
- **prajnaparamitahrdaya.wordpress.com** (Jayarava Attwood's research site)

---

## 7. Conclusion

This project represents a new approach to editing the Heart Sūtra that takes seriously the scholarly consensus on its Chinese compositional origin. Rather than treating Sanskrit as the source and Chinese as a translation, the edition inverts this assumption and documents how a Chinese composition became a multilingual Buddhist scripture.

The architecture is designed to be:
- **Extensible**: New witnesses can be added without restructuring
- **Transparent**: All editorial decisions are documented in the data
- **Reproducible**: Scripts generate outputs from source data
- **Scholarly**: Follows established critical edition principles adapted for multilingual, non-archetypal texts

The result is not a reconstruction of a lost original, but a **documented history of how a sūtra was made**.

---

*Document version: 1.0*
*Last updated: February 2026*
