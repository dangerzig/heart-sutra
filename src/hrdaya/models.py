"""
Data models for the Heart Sūtra multilingual critical edition.

Design Principles:
1. T251 as default alignment anchor - pragmatic analytical base
2. Direction-of-dependence annotation - apparatus encodes textual history
3. Configurable anchor tradition - any witness can serve as base
4. Multi-script support - Sanskrit, Chinese, and Tibetan scripts
5. Neutrality regarding compositional priority - treated as a hypothesis, not an axiom
"""

from dataclasses import dataclass, field
from enum import Enum


class WitnessType(Enum):
    """Type of textual witness by language tradition and function."""
    # Heart Sūtra witnesses by language
    CHINESE = "chinese"
    SANSKRIT = "sanskrit"
    TIBETAN = "tibetan"
    # Functional types (used with language witnesses)
    SOURCE = "source"  # Source text from which Heart Sūtra was extracted (e.g., T223)
    PARALLEL = "parallel"  # Comparative parallel text (e.g., Sanskrit Pañcaviṃśatisāhasrikā)


class Script(Enum):
    """Script/writing system for text representation."""
    # Chinese scripts
    TRADITIONAL_CHINESE = "hant"  # Traditional Chinese characters
    SIMPLIFIED_CHINESE = "hans"  # Simplified Chinese

    # Sanskrit scripts
    DEVANAGARI = "deva"  # देवनागरी
    IAST = "iast"  # International Alphabet of Sanskrit Transliteration
    SIDDHAM = "sidd"  # 悉曇 - used in East Asian Buddhist manuscripts
    RANJANA = "ranj"  # Rañjana/Newari script
    BHUJIMOL = "bhuj"  # Bhujimol/Nepalese hooked script
    PROTO_SHARADA = "shrd"  # Proto-Śāradā (Gilgit manuscripts)

    # Tibetan scripts
    TIBETAN = "tibt"  # Uchen script
    WYLIE = "wylie"  # Wylie transliteration

    # Other
    ROMANIZED = "latn"  # Generic romanization


class VariantType(Enum):
    """Classification of textual variants following the methodology."""
    # Mechanical/scribal
    ORTHOGRAPHIC = "orthographic"  # Spelling differences without semantic change
    SCRIBAL_ERROR = "scribal_error"  # Clear copying mistakes

    # Stylistic
    STYLISTIC_SMOOTHING = "stylistic"  # Improvements to flow/readability
    REGISTER_SHIFT = "register"  # Change in formality/style level

    # Doctrinal/content
    DOCTRINAL_HARMONIZATION = "doctrinal"  # Alignment with doctrinal norms
    EXPANSION = "expansion"  # Added material
    ABBREVIATION = "abbreviation"  # Shortened/condensed

    # Extraction-related
    EXTRACTION_ARTIFACT = "extraction"  # Traces of source Prajñāpāramitā text

    # Translation-related
    RETRANSLATION = "retranslation"  # Evidence of retranslation between traditions
    TRANSLATION_CHOICE = "translation_choice"  # Different rendering of same meaning
    GRAMMATICAL_ADAPTATION = "grammatical"  # Adaptation to target language grammar

    # Genuine variants
    DISTINCTIVE_READING = "distinctive"  # Genuinely different textual reading

    # Unknown/unclear
    UNCERTAIN = "uncertain"


class DependenceDirection(Enum):
    """Direction of textual dependence/borrowing."""
    # Primary directions
    PRAJNAPARAMITA_TO_HEART = "pp→hs"  # Larger PP text → Heart Sūtra
    CHINESE_TO_SANSKRIT = "zh→sa"  # Chinese → Sanskrit
    CHINESE_TO_TIBETAN = "zh→bo"  # Chinese → Tibetan
    TIBETAN_TO_SANSKRIT = "bo→sa"  # Tibetan → Sanskrit
    SANSKRIT_TO_TIBETAN = "sa→bo"  # Sanskrit → Tibetan
    SANSKRIT_TO_CHINESE = "sa→zh"  # Sanskrit → Chinese
    TIBETAN_TO_CHINESE = "bo→zh"  # Tibetan → Chinese

    # Uncertain/complex
    SHARED_SOURCE = "shared"  # Both derive from common source
    UNCERTAIN = "uncertain"
    INDEPENDENT = "independent"  # Independent development


@dataclass
class Token:
    """A single word/morpheme with linguistic analysis."""
    # Surface form
    text: str

    # Alternative script representations
    devanagari: str | None = None  # For Sanskrit
    iast: str | None = None  # For Sanskrit

    # Linguistic analysis
    lemma: str | None = None
    pos: str | None = None  # Part of speech
    morphology: dict | None = None  # Case, number, gender, etc.

    # For Chinese
    pinyin: str | None = None

    # Notes
    note: str | None = None


@dataclass
class Segment:
    """A text segment in a single language/witness."""
    id: str  # Unique segment identifier
    text: str  # Primary text representation

    # Witness information
    witness_id: str  # Which manuscript/edition
    witness_type: WitnessType = WitnessType.CHINESE  # Override for non-Chinese segments
    script: Script = Script.TRADITIONAL_CHINESE  # Override for non-Chinese segments

    # Alternative representations
    alt_scripts: dict[Script, str] = field(default_factory=dict)

    # Tokenization
    tokens: list[Token] | None = None

    # Source reference (folio, page, etc.)
    source_ref: str | None = None

    # Notes
    notes: list[str] = field(default_factory=list)


@dataclass
class Variant:
    """A textual variant with full critical apparatus annotation."""
    # Position in base text
    segment_id: str
    position: int  # Character offset (-1 = whole-segment or cross-linguistic variant)

    # Readings
    base_reading: str  # Reading in base text
    variant_reading: str  # Alternative reading

    # Witness support
    base_witnesses: list[str] = field(default_factory=list)
    variant_witnesses: list[str] = field(default_factory=list)

    # Classification
    variant_type: VariantType = VariantType.UNCERTAIN
    dependence: DependenceDirection = DependenceDirection.UNCERTAIN

    # Cross-linguistic evidence: these record which parallel passage in
    # each tradition is relevant to this variant.  They are distinct from
    # the segment-level base_parallel field used for alignment.
    chinese_parallel: str | None = None
    sanskrit_parallel: str | None = None
    tibetan_parallel: str | None = None
    prajnaparamita_parallel: str | None = None

    # Commentary
    note: str | None = None
    scholarly_refs: list[str] = field(default_factory=list)

    # Confidence
    confidence: float = 0.5  # 0.0 to 1.0

    def __post_init__(self):
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                f"confidence must be between 0.0 and 1.0, got {self.confidence}"
            )


@dataclass
class Witness:
    """A textual witness (manuscript, edition, inscription)."""
    id: str  # Short siglum (e.g., "Ja", "Nb", "T251")
    name: str  # Full name
    witness_type: WitnessType

    # Dating
    date: str | None = None  # Date or date range
    date_circa: bool = True  # Is date approximate?

    # Location/provenance
    location: str | None = None  # Current repository
    provenance: str | None = None  # Origin

    # Physical description
    material: str | None = None  # Palm leaf, paper, stone, etc.
    script: Script = Script.IAST

    # Scholarly information
    first_published: str | None = None  # When first published/described
    edition_used: str | None = None  # Which edition transcription follows

    # Relationship to other witnesses
    derived_from: str | None = None  # Parent witness if known

    # Notes
    description: str | None = None
    scholarly_refs: list[str] = field(default_factory=list)


@dataclass
class MultilingualSegment:
    """Aligned segments across all language traditions."""
    id: str  # Segment identifier (e.g., "hs:1.1")

    # Chinese
    chinese: Segment | None = None
    chinese_variants: list[Variant] = field(default_factory=list)

    # Sanskrit
    sanskrit: Segment | None = None
    sanskrit_devanagari: str | None = None  # Devanagari rendering
    sanskrit_variants: list[Variant] = field(default_factory=list)

    # Tibetan
    tibetan: Segment | None = None
    tibetan_wylie: str | None = None  # Wylie transliteration
    tibetan_variants: list[Variant] = field(default_factory=list)

    # Source Prajñāpāramitā parallel (if applicable)
    prajnaparamita_ref: str | None = None
    prajnaparamita_text: str | None = None

    # Cross-linguistic analysis
    dependence_notes: list[str] = field(default_factory=list)
    translation_notes: list[str] = field(default_factory=list)

    # Commentary
    philological_note: str | None = None


@dataclass
class CriticalApparatus:
    """Complete critical apparatus for the Heart Sūtra."""
    # Metadata
    version: str = "1.0.0"
    methodology: str = "T251-anchored-multilingual"

    # Base text
    base_text_id: str = "T251"  # Taishō 251 as default base
    base_text_justification: str = ""

    # Witnesses by tradition
    chinese_witnesses: list[Witness] = field(default_factory=list)
    sanskrit_witnesses: list[Witness] = field(default_factory=list)
    tibetan_witnesses: list[Witness] = field(default_factory=list)

    # Aligned segments
    segments: list[MultilingualSegment] = field(default_factory=list)

    # Global notes
    introduction: str = ""
    methodology_notes: str = ""
    limitations: list[str] = field(default_factory=list)

    # Bibliography
    scholarly_refs: list[str] = field(default_factory=list)
