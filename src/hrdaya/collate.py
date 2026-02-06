"""
Collation system for the Heart Sūtra critical edition.

Implements multilingual collation with:
- Direction-of-dependence annotation
- Variant classification
- Cross-linguistic alignment
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from difflib import SequenceMatcher

from .models import (
    Variant,
    VariantType,
    DependenceDirection,
    WitnessType,
    MultilingualSegment,
    Segment,
)


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

    Follows the Chinese-priority methodology:
    - Chinese T251 as analytical base
    - Sanskrit as derived tradition
    - Tibetan as mediating witness
    """

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

    def load_chinese_witness(self, witness_id: str) -> dict:
        """Load a Chinese witness from JSON."""
        if witness_id in self._chinese_cache:
            return self._chinese_cache[witness_id]

        # Try Taishō first
        path = self.chinese_dir / "taisho" / f"{witness_id}.json"
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._chinese_cache[witness_id] = data
                return data

        raise FileNotFoundError(f"Chinese witness {witness_id} not found")

    def load_sanskrit_witness(self, witness_id: str) -> dict:
        """Load a Sanskrit witness from JSON."""
        if witness_id in self._sanskrit_cache:
            return self._sanskrit_cache[witness_id]

        # Try GRETIL first
        path = self.sanskrit_dir / "gretil" / f"{witness_id.lower()}.json"
        if not path.exists():
            path = self.sanskrit_dir / "gretil" / "prajnaparamitahrdaya.json"

        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._sanskrit_cache[witness_id] = data
                return data

        raise FileNotFoundError(f"Sanskrit witness {witness_id} not found")

    def load_tibetan_witness(self, witness_id: str) -> dict:
        """Load a Tibetan witness from JSON."""
        if witness_id in self._tibetan_cache:
            return self._tibetan_cache[witness_id]

        # Try Kangyur first
        path = self.tibetan_dir / "kangyur" / f"{witness_id.lower()}.json"
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._tibetan_cache[witness_id] = data
                return data

        raise FileNotFoundError(f"Tibetan witness {witness_id} not found")

    def align_segments(
        self,
        chinese_seg: dict,
        sanskrit_seg: dict | None = None,
        tibetan_seg: dict | None = None
    ) -> MultilingualSegment:
        """
        Create aligned multilingual segment.

        Args:
            chinese_seg: Chinese segment (required, base)
            sanskrit_seg: Sanskrit segment (optional)
            tibetan_seg: Tibetan segment (optional)

        Returns:
            MultilingualSegment with aligned texts
        """
        seg_id = chinese_seg.get("id", "unknown")

        # Create Chinese segment
        chinese = Segment(
            id=seg_id,
            text=chinese_seg.get("text", ""),
            witness_id="T251",
            witness_type=WitnessType.CHINESE,
        )

        # Create Sanskrit segment if provided
        sanskrit = None
        sanskrit_deva = None
        if sanskrit_seg:
            sanskrit = Segment(
                id=sanskrit_seg.get("id", seg_id),
                text=sanskrit_seg.get("iast", ""),
                witness_id="GRETIL",
                witness_type=WitnessType.SANSKRIT,
            )
            sanskrit_deva = sanskrit_seg.get("devanagari")

        # Create Tibetan segment if provided
        tibetan = None
        tibetan_wylie = None
        if tibetan_seg:
            tibetan = Segment(
                id=tibetan_seg.get("id", seg_id),
                text=tibetan_seg.get("tibetan", ""),
                witness_id="Toh21",
                witness_type=WitnessType.TIBETAN,
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

        # Check for likely back-translation indicators
        if tradition == "sanskrit":
            if self._indicates_back_translation(base_reading, variant_reading):
                return VariantType.BACK_TRANSLATION, DependenceDirection.CHINESE_TO_SANSKRIT

        # Check for extraction artifacts
        if self._is_extraction_artifact(variant_reading):
            return VariantType.EXTRACTION_ARTIFACT, DependenceDirection.PRAJNAPARAMITA_TO_HEART

        # Default to distinctive reading with uncertain direction
        return VariantType.DISTINCTIVE_READING, DependenceDirection.UNCERTAIN

    def _is_orthographic_variant(self, text1: str, text2: str) -> bool:
        """Check if two readings are orthographic variants."""
        # Normalize and compare
        t1 = text1.lower().strip()
        t2 = text2.lower().strip()

        # Check similarity ratio
        ratio = SequenceMatcher(None, t1, t2).ratio()
        return ratio > 0.9

    def _indicates_back_translation(self, chinese: str, sanskrit: str) -> bool:
        """
        Check if Sanskrit reading indicates back-translation from Chinese.

        Key indicators (from Nattier 1992):
        - Use of kṣaya instead of nirodha
        - Non-standard terminology
        - Chinese word-order traces
        """
        # Known back-translation indicators
        indicators = [
            ("kṣaya", "nirodha"),  # kṣaya used instead of standard nirodha
            ("avidyā-kṣaya", "avidyā-nirodha"),
        ]

        sanskrit_lower = sanskrit.lower()
        for indicator, standard in indicators:
            if indicator in sanskrit_lower:
                return True

        return False

    def _is_extraction_artifact(self, text: str) -> bool:
        """Check if reading shows extraction from larger PP text."""
        # Phrases that indicate extraction from larger Prajñāpāramitā
        extraction_markers = [
            "evam ukte",  # "thus spoken" - dialogue marker
            "āyuṣmān",   # "venerable" - honorific often in larger texts
        ]

        text_lower = text.lower()
        return any(marker in text_lower for marker in extraction_markers)

    def collate_section(
        self,
        section_name: str,
        chinese_witness: str = "T251",
        sanskrit_witness: str = "GRETIL",
        tibetan_witness: str = "Toh21"
    ) -> list[CollationResult]:
        """
        Collate a section across all traditions.

        Args:
            section_name: Name of section to collate
            chinese_witness: Chinese witness ID (default T251)
            sanskrit_witness: Sanskrit witness ID (default GRETIL)
            tibetan_witness: Tibetan witness ID (default Toh21)

        Returns:
            List of CollationResult objects
        """
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

        # Get segments for the section
        chinese_segs = [
            s for s in chinese.get("segments", [])
            if s.get("section") == section_name
        ]

        for c_seg in chinese_segs:
            seg_id = c_seg.get("id")

            # Find corresponding Sanskrit segment
            s_seg = None
            if sanskrit:
                for s in sanskrit.get("segments", []):
                    if s.get("chinese_parallel") == seg_id:
                        s_seg = s
                        break

            # Find corresponding Tibetan segment
            t_seg = None
            if tibetan:
                for t in tibetan.get("segments", []):
                    if t.get("chinese_parallel") == seg_id:
                        t_seg = t
                        break

            # Create collation result
            result = CollationResult(
                segment_id=seg_id,
                base_text=c_seg.get("text", ""),
                base_witness=chinese_witness,
            )

            result.chinese_texts[chinese_witness] = c_seg.get("text", "")

            if s_seg:
                result.sanskrit_texts[sanskrit_witness] = s_seg.get("iast", "")

            if t_seg:
                result.tibetan_texts[tibetan_witness] = t_seg.get("tibetan", "")

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
        except Exception as e:
            all_results[section] = {"error": str(e)}

    return all_results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        data_dir = Path(sys.argv[1])
    else:
        data_dir = Path(__file__).parent.parent.parent / "data"

    results = collate_full_text(data_dir)

    # Output as JSON
    print(json.dumps(results, ensure_ascii=False, indent=2))
