"""Tests for collation engine."""

import pytest
from pathlib import Path
from hrdaya.collate import HeartSutraCollator, CollationResult
from hrdaya.models import VariantType, DependenceDirection


DATA_DIR = Path(__file__).parent.parent / "data"


class TestHeartSutraCollator:
    """Test collation functionality."""

    @pytest.fixture
    def collator(self):
        return HeartSutraCollator(DATA_DIR)

    def test_load_chinese_witness(self, collator):
        data = collator.load_chinese_witness("T251")
        assert "segments" in data

    def test_load_missing_witness_raises(self, collator):
        with pytest.raises(FileNotFoundError):
            collator.load_chinese_witness("NONEXISTENT")

    def test_classify_orthographic_variant(self, collator):
        vtype, direction = collator.classify_variant(
            "prajñāpāramitā", "prajnaparamita"
        )
        assert vtype == VariantType.ORTHOGRAPHIC

    def test_classify_back_translation(self, collator):
        vtype, direction = collator.classify_variant(
            "盡", "kṣaya",
            context={"tradition": "sanskrit"}
        )
        assert vtype == VariantType.BACK_TRANSLATION
        assert direction == DependenceDirection.CHINESE_TO_SANSKRIT

    def test_collate_section(self, collator):
        results = collator.collate_section("opening")
        assert isinstance(results, list)
        # Should have at least one result for the opening section
        assert len(results) > 0
        assert isinstance(results[0], CollationResult)

    def test_generate_apparatus(self, collator):
        results = collator.collate_section("opening")
        apparatus = collator.generate_apparatus(results)
        assert isinstance(apparatus, list)
        for entry in apparatus:
            assert "segment_id" in entry
            assert "base_text" in entry
            assert "readings" in entry

    def test_alternate_alignment_matches_correct_segment(self, collator):
        """Regression: alternate witnesses must align by segment position, not just section."""
        results = collator.collate_section("form_emptiness")
        assert len(results) > 0
        result = results[0]
        # T250 has a form_emptiness segment with 非色異空 (not the skandha_characteristics)
        if "T250" in result.chinese_texts:
            assert "非色異空" in result.chinese_texts["T250"] or "色即是空" in result.chinese_texts["T250"]

    def test_configurable_alternate_witnesses(self, collator):
        """Test that alternate_chinese parameter controls which witnesses are compared."""
        results = collator.collate_section("opening", alternate_chinese=["T250"])
        assert len(results) > 0
        result = results[0]
        assert "T250" in result.chinese_texts
        # T257 should NOT be present since we only asked for T250
        assert "T257" not in result.chinese_texts

    def test_available_chinese_witnesses(self, collator):
        """Test discovery of Chinese witnesses on disk."""
        available = collator._get_available_chinese_witnesses()
        assert "T251" in available
        assert "T250" in available
