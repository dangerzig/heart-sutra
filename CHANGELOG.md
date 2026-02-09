# Changelog

All notable changes to this project are documented in this file.

## [1.2.0] - 2026-02-09

### Added
- Data distribution policy section in README.md
- Tibetan variant creation in collation engine (Tibetan vs Chinese base)
- CI check (`scripts/check_data_version.py`) enforcing DATA_VERSION bump when data/ changes
- Chinese witness discovery now scans all subdirectories (taisho, dunhuang, epigraphy, manuscripts)
- Fangshan stele (661 CE, earliest dated witness) now discoverable by collation engine

### Changed
- `load_chinese_witness()` searches all chinese/ subdirectories, not just taisho/
- Cross-linguistic variant position convention (`position=-1`) documented in model and code
- DATA_VERSION bumped to 1.1.0 to reflect data additions

### Tests
- New: `test_cross_linguistic_variants_use_minus_one` — verifies position=-1 for Sanskrit/Tibetan
- New: `test_tibetan_variants_created` — verifies Tibetan produces variants against Chinese base
- Updated: `test_available_chinese_witnesses` — now asserts Fangshan is discoverable

## [1.1.0] - 2026-02-08

### Added
- Word-by-word literal glosses and fluid English translations in all critical editions
- Word-by-word glossary appendix in synoptic editions
- English glosses (english_gloss) for all 14 Sanskrit GRETIL segments
- Dunhuang IOL Tib J 751 fully integrated into collation and synoptic pipelines

### Fixed
- Dunhuang witness pipeline gap: load_tibetan_witness() and load_witness() now search dunhuang/ directory
- Witness ID mismatch: IOL_Tib_J_751 aligned between witnesses.py and data file
- Tibetan critical edition now documents both short (Dunhuang) and long (Kangyur) recensions
- Stemmatic diagrams updated to show Tibetan short/long recension split

## [1.0.0] - 2026-02-08

### Added
- Complete critical editions in LaTeX (Chinese, Sanskrit, Tibetan, Parallel)
- Stemma codicum with visual diagram
- Variant table with 13 key textual variants
- Annotated English translation
- Full methodology documentation
- Original research findings documentation
- Witness catalog with 40+ witnesses
- Transliteration module (Devanagari ↔ IAST)
- 12-segment synoptic alignment

### Research Contributions
- T250/T251 parallel composition hypothesis
- Three vs. four epithet pattern analysis
- Late interpolation identification (oṃ, na-aprāptiḥ, maṅgala frames)
- Direction-of-dependence apparatus notation

## [0.9.0] - 2026-02-07

### Added
- Single-language critical editions (Chinese, Sanskrit, Tibetan)
- Complete parallel synoptic edition
- Stemma diagram with Greek character support

### Fixed
- Stemma updated to show T250/T251 as parallel compositions
- Greek font rendering in stemma diagram

## [0.8.0] - 2026-02-06

### Added
- JSON data files for all major witnesses
- Collation variant table
- Sanskrit manuscript documentation (Hōryū-ji, Nepalese)

## [0.1.0] - 2026-02-05

### Added
- Initial project structure
- Core Python data models
- Witness catalog framework
- Base text documentation (T251)
- Methodology documentation

---

The format is based on [Keep a Changelog](https://keepachangelog.com/).
