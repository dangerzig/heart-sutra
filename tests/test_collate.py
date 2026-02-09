"""Tests for collation engine."""

import pytest
from pathlib import Path
from hrdaya.collate import HeartSutraCollator, CollationResult, collate_full_text
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

    def test_alignment_uses_chinese_parallel(self, collator):
        """Alignment is strictly by chinese_parallel (no fallback)."""
        results = collator.collate_section("mantra_praise", alternate_chinese=["T250"])
        assert len(results) > 0
        result = results[0]
        # T250:11 has chinese_parallel=T251:11 (mantra_praise), verify it matched
        if "T250" in result.chinese_texts:
            assert "明呪" in result.chinese_texts["T250"]

    def test_variant_position_is_real_offset(self, collator):
        """Variants should have a real character offset, not always -1."""
        results = collator.collate_section("opening", alternate_chinese=["T250"])
        assert len(results) > 0
        result = results[0]
        # T250 opening starts with 觀世音 vs T251 觀自在 — differ at position 1
        for v in result.variants:
            if "T250" in v.variant_witnesses:
                assert v.position >= 0  # real offset, not -1

    def test_no_match_for_unparalleled_section(self, collator):
        """Sections unique to alternate witnesses should not produce false matches."""
        # T250 has 'skandha_characteristics' with chinese_parallel=null
        # When collating T251 sections, this should not appear
        results = collator.collate_section("opening", alternate_chinese=["T250"])
        assert len(results) > 0
        result = results[0]
        # The result text should be T250's opening, not skandha_characteristics
        if "T250" in result.chinese_texts:
            assert "觀世音" in result.chinese_texts["T250"]


class TestCollateFullText:
    """Test the high-level collate_full_text entry point."""

    def test_returns_dict_with_provenance(self):
        result = collate_full_text(DATA_DIR)
        prov = result["provenance"]
        assert prov["tool"] == "hrdaya.collate"
        assert prov["base_witness"] == "T251"
        assert "data_version" in prov
        assert "data_hash" in prov
        assert len(prov["data_hash"]) == 12

    def test_returns_sections(self):
        result = collate_full_text(DATA_DIR)
        assert "sections" in result
        assert "opening" in result["sections"]
        assert "mantra" in result["sections"]

    def test_sections_contain_apparatus_entries(self):
        result = collate_full_text(DATA_DIR)
        opening = result["sections"]["opening"]
        assert isinstance(opening, list)
        assert len(opening) > 0
        assert "segment_id" in opening[0]
