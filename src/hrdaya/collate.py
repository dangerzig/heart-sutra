"""
Collation system for the Heart Sūtra critical edition.

Implements multilingual collation with:
- Direction-of-dependence annotation
- Variant classification
- Cross-linguistic alignment
"""

import json
import logging
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

from .models import (
    Variant,
    VariantType,
    DependenceDirection,
    WitnessType,
    MultilingualSegment,
    Segment,
)

logger = logging.getLogger(__name__)


@dataclass
class CollationResult:
    """Result of collating multiple witnesses."""
    segment_id: str
    base_text: str
    base_witness: str

    # Aligned texts from each tradition
    chinese_texts: dict[str, str] = field(default_factory=dict)
    sanskrit_texts: dict[str, str] = field(default_factory=dict)
    tibetan_texts: dict[str, str] = field(default_factory=dict)

    # Identified variants
    variants: list[Variant] = field(default_factory=list)

    # Notes
    notes: list[str] = field(default_factory=list)


class HeartSutraCollator:
    """
    Collator for Heart Sūtra witnesses across traditions.

    Uses T251 as the default alignment anchor. The anchor tradition
    is configurable via ``collate_section()`` parameters.
    """

    # Default witness IDs
    DEFAULT_CHINESE = "T251"
    DEFAULT_SANSKRIT = "GRETIL"
    DEFAULT_TIBETAN = "Toh21"

    def __init__(self, data_dir: Path):
        """
        Initialize collator with data directory.

        Args:
            data_dir: Path to data directory containing witness files
        """
        self.data_dir = Path(data_dir)
        self.chinese_dir = self.data_dir / "chinese"
        self.sanskrit_dir = self.data_dir / "sanskrit"
        self.tibetan_dir = self.data_dir / "tibetan"

        # Cache loaded witnesses
        self._chinese_cache: dict[str, dict] = {}
        self._sanskrit_cache: dict[str, dict] = {}
        self._tibetan_cache: dict[str, dict] = {}
        self._available_chinese: list[str] | None = None

    def load_chinese_witness(self, witness_id: str) -> dict:
        """Load a Chinese witness from JSON.

        Searches all subdirectories under chinese/ (taisho, dunhuang,
        epigraphy, manuscripts) for a matching file by ID or filename.
        """
        if witness_id in self._chinese_cache:
            return self._chinese_cache[witness_id]

        # Search all subdirectories for a file matching this witness
        if not self.chinese_dir.exists():
            raise FileNotFoundError(f"Chinese witness {witness_id} not found")
        for subdir in sorted(self.chinese_dir.iterdir()):
            if not subdir.is_dir():
                continue
            # Try both lowercased and original-case filenames in each subdir
            candidates = [
                subdir / f"{witness_id.lower()}.json",
                subdir / f"{witness_id}.json",
            ]
            for path in candidates:
                if not path.exists():
                    continue
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except json.JSONDecodeError as e:
                    logger.warning("Malformed JSON in %s: %s", path, e)
                    continue
                self._chinese_cache[witness_id] = data
                return data

        raise FileNotFoundError(f"Chinese witness {witness_id} not found")

    def load_sanskrit_witness(self, witness_id: str) -> dict:
        """Load a Sanskrit witness from JSON.

        Searches gretil/ directory by witness ID.  For 'GRETIL', loads the
        canonical prajnaparamitahrdaya.json file.
        """
        if witness_id in self._sanskrit_cache:
            return self._sanskrit_cache[witness_id]

        # Try exact witness ID match first
        path = self.sanskrit_dir / "gretil" / f"{witness_id.lower()}.json"
        if not path.exists() and witness_id.upper() == "GRETIL":
            # GRETIL is the canonical Sanskrit source
            path = self.sanskrit_dir / "gretil" / "prajnaparamitahrdaya.json"

        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                logger.warning("Malformed JSON in %s: %s", path, e)
                raise FileNotFoundError(
                    f"Sanskrit witness {witness_id} not found (malformed JSON)"
                ) from e
            self._sanskrit_cache[witness_id] = data
            return data

        raise FileNotFoundError(f"Sanskrit witness {witness_id} not found")

    def load_tibetan_witness(self, witness_id: str) -> dict:
        """Load a Tibetan witness from JSON."""
        if witness_id in self._tibetan_cache:
            return self._tibetan_cache[witness_id]

        # Try Kangyur first, then Dunhuang
        for subdir in ("kangyur", "dunhuang"):
            path = self.tibetan_dir / subdir / f"{witness_id.lower()}.json"
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except json.JSONDecodeError as e:
                    logger.warning("Malformed JSON in %s: %s", path, e)
                    continue
                self._tibetan_cache[witness_id] = data
                return data

        raise FileNotFoundError(f"Tibetan witness {witness_id} not found")

    def align_segments(
        self,
        chinese_seg: dict,
        sanskrit_seg: dict | None = None,
        tibetan_seg: dict | None = None,
        chinese_witness: str = DEFAULT_CHINESE,
        sanskrit_witness: str = DEFAULT_SANSKRIT,
        tibetan_witness: str = DEFAULT_TIBETAN,
    ) -> MultilingualSegment:
        """
        Create aligned multilingual segment.

        Args:
            chinese_seg: Chinese segment (required, base)
            sanskrit_seg: Sanskrit segment (optional)
            tibetan_seg: Tibetan segment (optional)
            chinese_witness: Chinese witness ID (default T251)
            sanskrit_witness: Sanskrit witness ID (default GRETIL)
            tibetan_witness: Tibetan witness ID (default Toh21)

        Returns:
            MultilingualSegment with aligned texts
        """
        from .models import Script

        seg_id = chinese_seg.get("id", "unknown")

        # Create Chinese segment
        chinese = Segment(
            id=seg_id,
            text=chinese_seg.get("text", ""),
            witness_id=chinese_witness,
            witness_type=WitnessType.CHINESE,
            script=Script.TRADITIONAL_CHINESE,
        )

        # Create Sanskrit segment if provided
        sanskrit = None
        sanskrit_deva = None
        if sanskrit_seg:
            sanskrit = Segment(
                id=sanskrit_seg.get("id", seg_id),
                text=sanskrit_seg.get("iast", ""),
                witness_id=sanskrit_witness,
                witness_type=WitnessType.SANSKRIT,
                script=Script.IAST,
            )
            sanskrit_deva = sanskrit_seg.get("devanagari")

        # Create Tibetan segment if provided
        tibetan = None
        tibetan_wylie = None
        if tibetan_seg:
            tibetan = Segment(
                id=tibetan_seg.get("id", seg_id),
                text=tibetan_seg.get("tibetan", ""),
                witness_id=tibetan_witness,
                witness_type=WitnessType.TIBETAN,
                script=Script.TIBETAN,
            )
            tibetan_wylie = tibetan_seg.get("wylie")

        return MultilingualSegment(
            id=seg_id,
            chinese=chinese,
            sanskrit=sanskrit,
            sanskrit_devanagari=sanskrit_deva,
            tibetan=tibetan,
            tibetan_wylie=tibetan_wylie,
        )

    def classify_variant(
        self,
        base_reading: str,
        variant_reading: str,
        context: dict | None = None
    ) -> tuple[VariantType, DependenceDirection]:
        """
        Classify a variant and determine direction of dependence.

        Args:
            base_reading: Reading in base text
            variant_reading: Alternative reading
            context: Additional context (tradition, position, etc.)

        Returns:
            Tuple of (VariantType, DependenceDirection)
        """
        context = context or {}
        tradition = context.get("tradition", "unknown")

        # Simple heuristics for classification
        # These would be refined with more sophisticated analysis

        # Check for orthographic variants
        if self._is_orthographic_variant(base_reading, variant_reading):
            return VariantType.ORTHOGRAPHIC, DependenceDirection.UNCERTAIN

        # Check for likely retranslation indicators
        if tradition == "sanskrit":
            if self._indicates_retranslation(variant_reading):
                return VariantType.RETRANSLATION, DependenceDirection.CHINESE_TO_SANSKRIT

        # Check for extraction artifacts
        if self._is_extraction_artifact(variant_reading):
            return VariantType.EXTRACTION_ARTIFACT, DependenceDirection.PRAJNAPARAMITA_TO_HEART

        # Default to distinctive reading with uncertain direction
        return VariantType.DISTINCTIVE_READING, DependenceDirection.UNCERTAIN

    @staticmethod
    def _strip_diacritics(text: str) -> str:
        """Strip diacritical marks for orthographic comparison."""
        nfkd = unicodedata.normalize('NFD', text)
        return ''.join(c for c in nfkd if unicodedata.category(c) != 'Mn')

    def _is_orthographic_variant(self, text1: str, text2: str) -> bool:
        """Check if two readings are orthographic variants."""
        # Normalize: lowercase, strip whitespace and diacritics
        t1 = self._strip_diacritics(text1.lower().strip())
        t2 = self._strip_diacritics(text2.lower().strip())

        # Check similarity ratio
        ratio = SequenceMatcher(None, t1, t2).ratio()
        return ratio > 0.9

    def _indicates_retranslation(self, sanskrit: str) -> bool:
        """
        Check if Sanskrit reading indicates retranslation from Chinese.

        Key indicators (from Nattier 1992):
        - Use of kṣaya instead of nirodha
        - Non-standard terminology
        - Chinese word-order traces
        """
        # Known retranslation indicators (from Nattier 1992):
        # kṣaya used instead of standard nirodha
        indicators = ["kṣaya", "avidyā-kṣaya"]

        sanskrit_lower = sanskrit.lower()
        for indicator in indicators:
            if indicator in sanskrit_lower:
                return True

        return False

    def _get_available_chinese_witnesses(self) -> list[str]:
        """
        Return IDs of segment-based Chinese witnesses on disk.

        Scans all subdirectories under chinese/ (taisho, dunhuang,
        epigraphy, manuscripts). Only files containing a 'segments'
        array are included — catalog files and non-segment structures
        are excluded because they cannot participate in segment-level
        collation.

        Results are cached for the lifetime of this collator instance.
        """
        if self._available_chinese is not None:
            return self._available_chinese
        available = []
        if not self.chinese_dir.exists():
            return available
        for subdir in sorted(self.chinese_dir.iterdir()):
            if not subdir.is_dir():
                continue
            for f in subdir.glob("*.json"):
                try:
                    with open(f, 'r', encoding='utf-8') as fh:
                        data = json.load(fh)
                    if not isinstance(data.get("segments"), list):
                        continue
                except (json.JSONDecodeError, OSError):
                    continue
                # Use the 'id' field from the JSON if available,
                # otherwise derive from filename
                wid = data.get("id")
                if not wid:
                    stem = f.stem
                    wid = stem if stem.startswith("T") else stem.upper()
                available.append(wid)
        self._available_chinese = sorted(available)
        return self._available_chinese

    def _is_extraction_artifact(self, text: str) -> bool:
        """Check if reading shows extraction from larger PP text."""
        # Phrases that indicate extraction from larger Prajñāpāramitā
        extraction_markers = [
            "evam ukte",  # "thus spoken" - dialogue marker
            "āyuṣmān",   # "venerable" - honorific often in larger texts
        ]

        text_lower = text.lower()
        return any(marker in text_lower for marker in extraction_markers)

    @staticmethod
    def _first_diff_position(base: str, variant: str) -> int:
        """Return the character index where two strings first diverge, or -1 if identical."""
        for i, (a, b) in enumerate(zip(base, variant)):
            if a != b:
                return i
        if len(base) != len(variant):
            return min(len(base), len(variant))
        return -1

    def collate_section(
        self,
        section_name: str,
        chinese_witness: str = DEFAULT_CHINESE,
        sanskrit_witness: str = DEFAULT_SANSKRIT,
        tibetan_witness: str = DEFAULT_TIBETAN,
        alternate_chinese: list[str] | None = None,
        anchor_tradition: str = "chinese",
    ) -> list[CollationResult]:
        """
        Collate a section across all traditions.

        Alignment is strictly by ``base_parallel`` reference — there is
        no section+index fallback.  Segments in alternate witnesses that
        lack a ``base_parallel`` field are silently excluded (logged at
        DEBUG level).  This is the correct scholarly behaviour: we never
        guess at correspondences.

        Args:
            section_name: Name of section to collate
            chinese_witness: Chinese witness ID (default T251)
            sanskrit_witness: Sanskrit witness ID (default GRETIL)
            tibetan_witness: Tibetan witness ID (default Toh21)
            alternate_chinese: Additional Chinese witnesses to compare
                (default: all segment-based Taisho witnesses except the base)
            anchor_tradition: Tradition of the anchor witness
                ("chinese", "sanskrit", or "tibetan"; default "chinese")

        Returns:
            List of CollationResult objects
        """
        if anchor_tradition != "chinese":
            raise ValueError(
                f"anchor_tradition={anchor_tradition!r} is not supported. "
                f"Only 'chinese' is currently implemented."
            )

        results = []

        # Load witnesses
        try:
            chinese = self.load_chinese_witness(chinese_witness)
        except FileNotFoundError:
            chinese = None

        try:
            sanskrit = self.load_sanskrit_witness(sanskrit_witness)
        except FileNotFoundError:
            sanskrit = None

        try:
            tibetan = self.load_tibetan_witness(tibetan_witness)
        except FileNotFoundError:
            tibetan = None

        if not chinese:
            raise ValueError("Chinese base text is required for collation")

        # Pre-build Sanskrit and Tibetan indices keyed by base_parallel.
        # Segments without base_parallel are excluded — no fallback.
        sanskrit_by_parallel: dict[str, dict] = {}
        if sanskrit:
            skipped = 0
            for s in sanskrit.get("segments", []):
                cp = s.get("base_parallel")
                if cp:
                    if cp in sanskrit_by_parallel:
                        logger.warning(
                            "%s: duplicate base_parallel=%r in Sanskrit, "
                            "later segment overwrites earlier",
                            sanskrit_witness, cp,
                        )
                    sanskrit_by_parallel[cp] = s
                else:
                    skipped += 1
            if skipped:
                logger.debug(
                    "%s: %d Sanskrit segment(s) lack base_parallel, excluded from alignment",
                    sanskrit_witness, skipped,
                )

        tibetan_by_parallel: dict[str, dict] = {}
        if tibetan:
            skipped = 0
            for t in tibetan.get("segments", []):
                cp = t.get("base_parallel")
                if cp:
                    if cp in tibetan_by_parallel:
                        logger.warning(
                            "%s: duplicate base_parallel=%r in Tibetan, "
                            "later segment overwrites earlier",
                            tibetan_witness, cp,
                        )
                    tibetan_by_parallel[cp] = t
                else:
                    skipped += 1
            if skipped:
                logger.debug(
                    "%s: %d Tibetan segment(s) lack base_parallel, excluded from alignment",
                    tibetan_witness, skipped,
                )

        # Determine alternate witness IDs
        alt_ids = alternate_chinese if alternate_chinese is not None else [
            wid for wid in self._get_available_chinese_witnesses()
            if wid != chinese_witness
        ]

        # Pre-build alternate witness indices keyed by base_parallel
        alt_indices: dict[str, dict[str, dict]] = {}  # alt_id -> {base_seg_id -> alt_seg}
        for alt_id in alt_ids:
            try:
                alt = self.load_chinese_witness(alt_id)
            except FileNotFoundError:
                continue
            by_parallel: dict[str, dict] = {}
            unmapped = 0
            for alt_seg in alt.get("segments", []):
                cp = alt_seg.get("base_parallel")
                if cp:
                    if cp in by_parallel:
                        logger.warning(
                            "%s: duplicate base_parallel '%s' — "
                            "later segment overwrites earlier",
                            alt_id, cp,
                        )
                    by_parallel[cp] = alt_seg
                else:
                    unmapped += 1
            if unmapped:
                logger.debug(
                    "%s: %d segment(s) lack base_parallel and will not be aligned",
                    alt_id, unmapped,
                )
            alt_indices[alt_id] = by_parallel

        # Get segments for the section
        chinese_segs = [
            s for s in chinese.get("segments", [])
            if s.get("section") == section_name
        ]

        for c_seg in chinese_segs:
            seg_id = c_seg.get("id")
            if not seg_id:
                logger.warning("Skipping segment with missing id in section %s", section_name)
                continue

            # Find corresponding Sanskrit segment
            s_seg = sanskrit_by_parallel.get(seg_id)

            # Find corresponding Tibetan segment
            t_seg = tibetan_by_parallel.get(seg_id)

            # Create collation result
            result = CollationResult(
                segment_id=seg_id,
                base_text=c_seg.get("text", ""),
                base_witness=chinese_witness,
            )

            result.chinese_texts[chinese_witness] = c_seg.get("text", "")

            if s_seg:
                result.sanskrit_texts[sanskrit_witness] = s_seg.get("iast", "")

                # Classify Sanskrit variants against Chinese base.
                # position=-1 signals a whole-segment cross-linguistic variant:
                # character-level offsets are meaningless across scripts
                # (IAST vs hanzi), so we use -1 by convention.
                s_text = s_seg.get("iast", "")
                if s_text:
                    vtype, direction = self.classify_variant(
                        c_seg.get("text", ""), s_text,
                        context={"tradition": "sanskrit"}
                    )
                    if vtype != VariantType.ORTHOGRAPHIC:
                        result.variants.append(Variant(
                            segment_id=seg_id,
                            position=-1,
                            base_reading=c_seg.get("text", ""),
                            variant_reading=s_text,
                            variant_type=vtype,
                            dependence=direction,
                            base_witnesses=[chinese_witness],
                            variant_witnesses=[sanskrit_witness],
                            note=s_seg.get("note", ""),
                        ))

            if t_seg:
                result.tibetan_texts[tibetan_witness] = t_seg.get("tibetan", "")

                # Classify Tibetan variants against Chinese base.
                # Same convention: position=-1 for cross-linguistic variants.
                t_text = t_seg.get("tibetan", "")
                if t_text:
                    vtype, direction = self.classify_variant(
                        c_seg.get("text", ""), t_text,
                        context={"tradition": "tibetan"}
                    )
                    if vtype != VariantType.ORTHOGRAPHIC:
                        result.variants.append(Variant(
                            segment_id=seg_id,
                            position=-1,
                            base_reading=c_seg.get("text", ""),
                            variant_reading=t_text,
                            variant_type=vtype,
                            dependence=direction,
                            base_witnesses=[chinese_witness],
                            variant_witnesses=[tibetan_witness],
                            note=t_seg.get("note", ""),
                        ))

            # Match alternate Chinese witnesses using base_parallel only
            for alt_id in alt_indices:
                alt_seg = alt_indices[alt_id].get(seg_id)
                if alt_seg is None:
                    continue

                alt_text = alt_seg.get("text", "")
                result.chinese_texts[alt_id] = alt_text
                base_text = c_seg.get("text", "")
                if alt_text != base_text:
                    pos = self._first_diff_position(base_text, alt_text)
                    result.variants.append(Variant(
                        segment_id=seg_id,
                        position=pos,
                        base_reading=base_text,
                        variant_reading=alt_text,
                        variant_type=VariantType.DISTINCTIVE_READING,
                        dependence=DependenceDirection.UNCERTAIN,
                        base_witnesses=[chinese_witness],
                        variant_witnesses=[alt_id],
                        note=alt_seg.get("note", ""),
                    ))

            results.append(result)

        return results

    def generate_apparatus(
        self,
        collation_results: list[CollationResult]
    ) -> list[dict]:
        """
        Generate critical apparatus from collation results.

        Args:
            collation_results: List of CollationResult objects

        Returns:
            List of apparatus entries as dictionaries
        """
        apparatus = []

        for result in collation_results:
            entry = {
                "segment_id": result.segment_id,
                "base_text": result.base_text,
                "base_witness": result.base_witness,
                "readings": {
                    "chinese": result.chinese_texts,
                    "sanskrit": result.sanskrit_texts,
                    "tibetan": result.tibetan_texts,
                },
                "variants": [
                    {
                        "position": v.position,
                        "base_reading": v.base_reading,
                        "variant_reading": v.variant_reading,
                        "type": v.variant_type.value,
                        "dependence": v.dependence.value,
                        "witnesses": v.variant_witnesses,
                        "note": v.note,
                    }
                    for v in result.variants
                ],
                "notes": result.notes,
            }
            apparatus.append(entry)

        return apparatus


def collate_full_text(data_dir: Path) -> dict:
    """
    Collate the full Heart Sūtra text across all traditions.

    Args:
        data_dir: Path to data directory

    Returns:
        Dictionary with full collation results
    """
    collator = HeartSutraCollator(data_dir)

    # Verify the base Chinese witness is loadable before iterating sections.
    # A missing/corrupt base witness is fatal — don't silently produce empty output.
    collator.load_chinese_witness(HeartSutraCollator.DEFAULT_CHINESE)

    sections = [
        "opening",
        "form_emptiness",
        "characteristics",
        "negations_skandhas",
        "negations_ayatanas",
        "negations_dhatus",
        "negations_pratityasamutpada",
        "negations_truths",
        "bodhisattva_result",
        "buddha_result",
        "mantra_praise",
        "mantra",
    ]

    all_results = {}

    for section in sections:
        try:
            results = collator.collate_section(section)
            all_results[section] = collator.generate_apparatus(results)
        except (ValueError, FileNotFoundError) as e:
            logger.warning("Section %s failed: %s", section, e)
            all_results[section] = []

    from .data import DATA_VERSION, compute_data_hash

    return {
        "provenance": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "tool": "hrdaya.collate",
            "version": "1.0.0",
            "data_version": DATA_VERSION,
            "data_hash": compute_data_hash(data_dir),
            "base_witness": HeartSutraCollator.DEFAULT_CHINESE,
        },
        "sections": all_results,
    }


def main():
    """CLI entry point for collation."""
    import sys
    from .data import resolve_data_dir

    data_dir = resolve_data_dir(sys.argv[1] if len(sys.argv) > 1 else None)
    results = collate_full_text(data_dir)

    # Output as JSON
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
