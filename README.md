# Heart Sūtra Critical Edition

A multilingual electronic critical edition of the Prajñāpāramitāhṛdaya (Heart Sūtra) treating the text as a textual complex with T251 as the default alignment anchor.

## Overview

This project creates a scholarly critical edition of the Heart Sūtra that:

- **Uses T251 as default alignment anchor** following Nattier (1992) and subsequent scholarship
- **Presents all three traditions** (Chinese, Sanskrit, Tibetan) with explicit direction-of-dependence annotations
- **Remains neutral on compositional priority** -- treated as a hypothesis, not an axiom
- **Provides dual-script Sanskrit** in both Devanagari and IAST
- **Annotates direction-of-dependence** in the critical apparatus

## Project Structure

```
heart-sutra/
├── src/hrdaya/              # Core Python library (3.10+)
│   ├── models.py            # Data models (Witness, Segment, Variant)
│   ├── witnesses.py         # Witness catalog (40+ witnesses)
│   ├── transliterate.py     # Devanagari ↔ IAST conversion
│   ├── collate.py           # Collation engine
│   └── synoptic.py          # Parallel presentation builder
├── data/
│   ├── chinese/
│   │   ├── taisho/          # T250-T257 with full metadata
│   │   ├── dunhuang/        # Dunhuang manuscripts
│   │   └── epigraphy/       # Fangshan stele, inscriptions
│   ├── sanskrit/
│   │   ├── gretil/          # GRETIL edition
│   │   └── manuscripts/     # Hōryū-ji, Nepalese MSS
│   ├── tibetan/kangyur/     # Kangyur editions
│   ├── prajnaparamita/      # Large PP source parallels
│   ├── collation/           # Variant table
│   ├── stemma/              # Stemma codicum
│   └── aligned/             # 12-segment synoptic alignment
├── output/
│   ├── latex/               # Critical editions (PDF)
│   └── translation/         # Annotated English translation
├── scripts/                 # Utility scripts
├── tests/                   # Test suite
├── docs/                    # Methodology, architecture
└── research/                # Original findings documentation
```

## Methodology

This edition follows the methodological principles outlined in `docs/METHODOLOGY.md`:

1. **Abandon single-original-text assumption** - No Ur-Sanskrit reconstruction
2. **Define object as textual complex** - Multiple related but non-equivalent forms
3. **Chinese base text (T251)** - Analytical anchor, not authoritative text
4. **Exhaustive witness collation** - All traditions systematically compared
5. **Sanskrit tradition** - Presented with direction-of-dependence annotations
6. **Tibetan tradition** - Presented with direction-of-dependence annotations
7. **Direction-of-dependence annotation** - Apparatus encodes history
8. **Parallel presentation** - Chinese critical text + multilingual synoptic
9. **Composition-focused commentary** - Historical/philological priority
10. **Transparent about limits** - Probabilistic conclusions clearly marked

## Witnesses

### Chinese (Taishō Canon)

| ID | Title | Date | Notes |
|----|-------|------|-------|
| T251 | 般若波羅蜜多心經 | 649 CE | Xuanzang; base text |
| T250 | 摩訶般若波羅蜜大明咒經 | 649 CE | Parallel composition (attr. Kumārajīva) |
| T256 | 唐梵翻對字音般若波羅蜜多心經 | 788 CE | Bilingual transliteration |
| T257 | 佛說聖佛母般若波羅蜜多經 | 1005 CE | Long recension, Dānapāla |

### Sanskrit

| ID | Name | Date | Provenance |
|----|------|------|------------|
| Ja | Hōryū-ji palm-leaf | c. 8th c. | Japan |
| Nb | Cambridge Add. 1485 | 1677 CE | Nepal |
| Nk | Cambridge Add. 1680 | c. 13th c. | Nepal |
| Gilgit | Gilgit fragments | c. 6th-7th c. | Central Asia |

### Tibetan

| ID | Name | Date |
|----|------|------|
| Toh21 | Degé Kangyur (long recension) | c. 9th c. (trans.) |
| IOL_Tib_J_751 | Dunhuang IOL Tib J 751 (short recension) | c. 823 CE |

## Data Formats

### Source Texts (JSON)

```json
{
  "id": "T251",
  "title_chinese": "般若波羅蜜多心經",
  "translator": "Xuanzang",
  "date": "649 CE",
  "recension": "short",
  "text": "觀自在菩薩...",
  "segments": [
    {
      "id": "T251:1",
      "section": "opening",
      "text": "觀自在菩薩，行深般若波羅蜜多時...",
      "pinyin": "Guānzìzài púsà...",
      "english_gloss": "When Avalokiteśvara Bodhisattva..."
    }
  ]
}
```

### Sanskrit with Dual Script

```json
{
  "id": "GRETIL:3",
  "section": "form_emptiness",
  "iast": "Iha Śāriputra rūpaṃ śūnyatā...",
  "devanagari": "इह शारिपुत्र रूपं शून्यता...",
  "base_parallel": "T251:2"
}
```

## Installation

```bash
# Clone repository
git clone <repository-url>
cd heart-sutra

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Requires Python 3.10+
# Core library uses standard library only
# Optional: pip install -r requirements.txt  (for scripts)
```

## Data Files

The witness data files (JSON) are **not shipped in the Python wheel**. This is intentional — scholarly primary-source data is versioned alongside the code in git, not packaged inside a wheel. You must either:

1. **Clone the repo and install in editable mode** (recommended):
   ```bash
   git clone <repository-url> && cd heart-sutra && pip install -e .
   ```

2. **Or download the `data/` directory separately** and point to it:
   ```bash
   export HRDAYA_DATA_DIR=/path/to/heart-sutra/data
   ```

The data directory is resolved automatically for editable installs. See `src/hrdaya/data.py` for the full resolution logic.

## Usage

```python
from hrdaya import Witness, WitnessType
from hrdaya.witnesses import get_witness, CHINESE_WITNESSES

# Get witness information
t251 = get_witness("T251")
print(f"{t251.name} ({t251.date})")

# List all Sanskrit witnesses
from hrdaya.witnesses import SANSKRIT_WITNESSES
for siglum, witness in SANSKRIT_WITNESSES.items():
    print(f"{siglum}: {witness.name}")
```

## Original Research Findings

This edition documents several original contributions:

1. **T250/T251 Parallel Composition** — Evidence that T250 and T251 are independent sibling compositions from *Mokṣala's Large Sūtra (T223)*, not successive recensions. T250 preserves material absent from T251 (skandha characteristics, temporal negation) suggesting parallel development rather than linear revision.

2. **Three vs. Four Epithet Pattern** — T250's three-epithet formula (不生不滅, 不垢不淨, 不增不減) matches T223 exactly; T251 innovates with four epithets matching Sanskrit witnesses, suggesting independent back-translation.

3. **Late Interpolations Identified** — The *oṃ* in the Sanskrit mantra, *na-aprāptiḥ*, and elaborate *maṅgala* frames represent post-9th century accretions absent from earliest Chinese witnesses.

See `research/FINDINGS.md` for full documentation.

## Key Scholarship

- **Nattier, Jan (1992)**. "The Heart Sūtra: a Chinese apocryphal text?" *JIABS* 15(2): 153-223.
- **Conze, Edward (1967)**. "The Prajñāpāramitā-Hṛdaya Sūtra." In *Thirty Years of Buddhist Studies*.
- **Attwood, Jayarava (2015)**. "Heart Murmurs." *JOCBS* 8: 28-48.
- **Attwood, Jayarava (2017)**. "Epithets of the Mantra." *JOCBS* 12: 26-57.
- **Attwood, Jayarava (2023)**. "Heart to Heart: A Comparative Study." *Buddhist Studies Review* 40(2): 159-188.
- **Attwood, Jayarava (2024)**. "Revised Editions of the Prajñāpāramitāhṛdaya." *Asian Literature and Translation* 11(1): 1-42.
- **Silk, Jonathan (1994)**. *The Heart Sūtra in Tibetan*. Vienna.

## Status

**Publication Ready** — Core scholarly work complete.

### Completed

- [x] Project structure and data models
- [x] Witness catalog with full metadata (40+ witnesses)
- [x] Chinese base texts (T250, T251, T256, T257)
- [x] Sanskrit texts with dual script (Devanagari/IAST)
- [x] Tibetan text (Kangyur Toh 21)
- [x] Transliteration utilities (Devanagari ↔ IAST)
- [x] Methodology documentation
- [x] Full collation system with variant table
- [x] Synoptic alignment (12-segment parallel structure)
- [x] Variant classification with direction-of-dependence
- [x] Critical apparatus generation
- [x] Stemma codicum with analysis
- [x] LaTeX critical editions (Chinese, Sanskrit, Tibetan, Parallel)
- [x] Annotated English translation

### In Progress

- [ ] TEI-XML export
- [x] Formal consolidated bibliography
- [x] Publication front matter (introduction, indices)

## Limitations

This edition has significant limitations that users should understand:

1. **Not a traditional critical edition.** We have worked primarily from published editions and digital texts rather than conducting fresh manuscript collation. A full critical edition would require examination of physical manuscripts and rubbings.

2. **Dunhuang Chinese manuscripts are cataloged but not fully collated.** Character-by-character comparison of Dunhuang Chinese witnesses (S.2464, S.700, P.2323) has not been performed. The Dunhuang Tibetan witness (IOL Tib J 751) is fully segmented and integrated into the collation pipeline.

3. **Witness coverage is incomplete.** Korean Tripiṭaka, Japanese manuscript traditions (beyond Hōryū-ji), Xixia, Khotanese, and Uyghur traditions are not included.

4. **Chinese priority remains debated.** While we adopt this as our working hypothesis based on the weight of evidence, scholars including Fukui Fumimasa have questioned aspects of the argument.

5. **The T250/T251 parallel composition hypothesis is tentative.** Alternative interpretations exist and have not been definitively ruled out.

We describe this work as a **preliminary critical apparatus** rather than a definitive critical edition. It is intended as a foundation for further research.

## License

This project is for scholarly use. Individual texts may have their own licensing terms from their respective sources (GRETIL, CBETA, 84000, etc.).

## Acknowledgments

- GRETIL (Göttingen Register of Electronic Texts in Indian Languages)
- CBETA (Chinese Buddhist Electronic Text Association)
- 84000: Translating the Words of the Buddha
- Digital Sanskrit Buddhist Canon
- Jayarava Attwood's Heart Sūtra research at prajnaparamitahrdaya.wordpress.com

---

*February 2026*
