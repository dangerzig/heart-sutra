# Heart Sūtra Critical Edition

A multilingual electronic critical edition of the Prajñāpāramitāhṛdaya (Heart Sūtra) treating the text as a textual complex with Chinese compositional priority.

## Overview

This project creates a scholarly critical edition of the Heart Sūtra that:

- **Treats Chinese as compositionally prior** following Nattier (1992) and subsequent scholarship
- **Presents Sanskrit as derived tradition** - evidence of reception and back-translation
- **Uses Tibetan as mediating witness** for triangulating transmission stages
- **Provides dual-script Sanskrit** in both Devanagari and IAST
- **Annotates direction-of-dependence** in the critical apparatus

## Project Structure

```
heart-sutra/
├── src/
│   └── hrdaya/              # Core Python library
│       ├── __init__.py      # Package initialization
│       ├── models.py        # Data models (Witness, Segment, Variant, etc.)
│       ├── witnesses.py     # Witness catalog with full metadata
│       └── transliterate.py # Devanagari ↔ IAST conversion
├── data/
│   ├── chinese/
│   │   ├── taisho/          # Taishō Canon texts (T250-T257)
│   │   ├── dunhuang/        # Dunhuang manuscripts
│   │   └── manuscripts/     # Other Chinese manuscripts
│   ├── sanskrit/
│   │   ├── gretil/          # GRETIL edition
│   │   ├── dsbc/            # Digital Sanskrit Buddhist Canon
│   │   └── manuscripts/     # Manuscript transcriptions by provenance
│   │       ├── nepalese/
│   │       ├── japanese/
│   │       ├── chinese-inscriptions/
│   │       └── central-asian/
│   ├── tibetan/
│   │   ├── kangyur/         # Kangyur versions
│   │   └── dunhuang/        # Dunhuang Tibetan manuscripts
│   ├── prajnaparamita/      # Source texts (Large PP parallels)
│   ├── collation/           # Collation output
│   ├── critical/            # Critical edition output
│   └── aligned/             # Synoptic alignments
├── docs/
│   └── METHODOLOGY.md       # Full methodological framework
├── refs/                    # Scholarly references
└── scripts/                 # Utility scripts
```

## Methodology

This edition follows the methodological principles outlined in `docs/METHODOLOGY.md`:

1. **Abandon single-original-text assumption** - No Ur-Sanskrit reconstruction
2. **Define object as textual complex** - Multiple related but non-equivalent forms
3. **Chinese base text (T251)** - Analytical anchor, not authoritative text
4. **Exhaustive witness collation** - All traditions systematically compared
5. **Sanskrit as derived** - Evidence of reception, not origin
6. **Tibetan as mediating** - Triangulates transmission stages
7. **Direction-of-dependence annotation** - Apparatus encodes history
8. **Parallel presentation** - Chinese critical text + multilingual synoptic
9. **Composition-focused commentary** - Historical/philological priority
10. **Transparent about limits** - Probabilistic conclusions clearly marked

## Witnesses

### Chinese (Taishō Canon)

| ID | Title | Date | Type |
|----|-------|------|------|
| T251 | 般若波羅蜜多心經 | 649 CE | Base text |
| T250 | 摩訶般若波羅蜜大明咒經 | c. 402-412 | Long |
| T252-257 | Various | c. 700-1000 | Short/Long |

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
| Toh21 | Degé Kangyur | c. 9th c. (trans.) |
| IOL_J751 | Dunhuang | c. 823 CE |

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
  "chinese_parallel": "T251:2"
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

# No external dependencies required (standard library only)
```

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

## Key Scholarship

- **Nattier, Jan (1992)**. "The Heart Sūtra: a Chinese apocryphal text?" *JIABS* 15(2): 153-223.
- **Conze, Edward (1967)**. "The Prajñāpāramitā-Hṛdaya Sūtra." In *Thirty Years of Buddhist Studies*.
- **Attwood, Jayarava (2015-2020)**. Series of articles in *JOCBS* on Heart Sūtra textual problems.
- **Silk, Jonathan (1994)**. *The Heart Sūtra in Tibetan*. Vienna.

## Status

This project is under active development. Current status:

- [x] Project structure and data models
- [x] Witness catalog with metadata
- [x] Chinese base text (T251)
- [x] Sanskrit text (GRETIL) with dual script
- [x] Tibetan text (Kangyur Toh 21)
- [x] Transliteration utilities
- [x] Methodology documentation
- [ ] Full collation system
- [ ] Synoptic alignment tool
- [ ] Variant classification
- [ ] Critical apparatus generation
- [ ] Export formats (LaTeX, TEI-XML)

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
