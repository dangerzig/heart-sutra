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

    def test_classify_retranslation(self, collator):
        vtype, direction = collator.classify_variant(
            "盡", "kṣaya",
            context={"tradition": "sanskrit"}
        )
        assert vtype == VariantType.RETRANSLATION
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
        assert "T250" in result.chinese_texts, "T250 must be present in form_emptiness results"
        assert "非色異空" in result.chinese_texts["T250"], (
            f"Expected T250 form_emptiness text to contain '非色異空', got: {result.chinese_texts['T250']!r}"
        )

    def test_configurable_alternate_witnesses(self, collator):
        """Test that alternate_chinese parameter controls which witnesses are compared."""
        results = collator.collate_section("opening", alternate_chinese=["T250"])
        assert len(results) > 0
        result = results[0]
        assert "T250" in result.chinese_texts
        # T257 should NOT be present since we only asked for T250
        assert "T257" not in result.chinese_texts

    def test_available_chinese_witnesses(self, collator):
        """Test discovery of Chinese witnesses on disk across all subdirectories."""
        available = collator._get_available_chinese_witnesses()
        assert "T251" in available
        assert "T250" in available
        # Fangshan stele (epigraphy) has segments and should be discovered
        assert "Fangshan" in available

    def test_alignment_uses_base_parallel(self, collator):
        """Alignment is strictly by base_parallel (no fallback)."""
        results = collator.collate_section("mantra_praise", alternate_chinese=["T250"])
        assert len(results) > 0
        result = results[0]
        # T250:11 has base_parallel=T251:11 (mantra_praise), verify it matched
        assert "T250" in result.chinese_texts, "T250 must be present in mantra_praise results"
        assert "明呪" in result.chinese_texts["T250"]

    def test_variant_position_is_real_offset(self, collator):
        """Variants should have a real character offset, not always -1."""
        results = collator.collate_section("opening", alternate_chinese=["T250"])
        assert len(results) > 0
        result = results[0]
        # T250 opening starts with 觀世音 vs T251 觀自在 — differ at position 1
        found = False
        for v in result.variants:
            if "T250" in v.variant_witnesses:
                assert v.position >= 0  # real offset, not -1
                found = True
        assert found, "Expected at least one T250 variant in opening"

    def test_cross_linguistic_variants_use_minus_one(self, collator):
        """Cross-linguistic variants (Sanskrit/Tibetan vs Chinese) use position=-1."""
        results = collator.collate_section("form_emptiness")
        assert len(results) > 0
        found = False
        for result in results:
            for v in result.variants:
                # Variants where witnesses span different scripts should be -1
                is_sanskrit = any(w.startswith("GRETIL") for w in v.variant_witnesses)
                is_tibetan = any(w.startswith("Toh") or w.startswith("IOL") for w in v.variant_witnesses)
                if is_sanskrit or is_tibetan:
                    assert v.position == -1, (
                        f"Cross-linguistic variant should use position=-1, got {v.position}"
                    )
                    found = True
        assert found, "Expected at least one cross-linguistic variant"

    def test_tibetan_variants_created(self, collator):
        """Tibetan witnesses should produce variants against Chinese base."""
        results = collator.collate_section("form_emptiness")
        assert len(results) > 0
        tibetan_variants = [
            v for result in results for v in result.variants
            if any(w.startswith("Toh") or w.startswith("IOL") for w in v.variant_witnesses)
        ]
        assert len(tibetan_variants) > 0, "Expected at least one Tibetan variant"

    def test_no_match_for_unparalleled_section(self, collator):
        """Sections unique to alternate witnesses should not produce false matches."""
        # T250 has 'skandha_characteristics' with base_parallel=null
        # When collating T251 sections, this should not appear
        results = collator.collate_section("opening", alternate_chinese=["T250"])
        assert len(results) > 0
        result = results[0]
        # The result text should be T250's opening, not skandha_characteristics
        assert "T250" in result.chinese_texts, "T250 must be present in opening results"
        assert "觀世音" in result.chinese_texts["T250"]


class TestAlignSegments:
    """Test the align_segments method (MJ11 coverage gap)."""

    @pytest.fixture
    def collator(self):
        return HeartSutraCollator(DATA_DIR)

    def test_chinese_only(self, collator):
        seg = {"id": "T251:1", "text": "觀自在菩薩", "section": "opening"}
        result = collator.align_segments(seg)
        assert result.chinese is not None
        assert result.chinese.text == "觀自在菩薩"
        assert result.sanskrit is None
        assert result.tibetan is None

    def test_all_three_traditions(self, collator):
        zh = {"id": "T251:1", "text": "觀自在菩薩", "section": "opening"}
        sa = {"id": "GRETIL:1", "iast": "avalokiteśvara", "devanagari": "अवलोकितेश्वर"}
        bo = {"id": "Toh21:1", "tibetan": "སྤྱན་རས་གཟིགས་", "wylie": "spyan ras gzigs"}
        result = collator.align_segments(zh, sa, bo)
        assert result.chinese is not None
        assert result.sanskrit is not None
        assert result.tibetan is not None
        assert result.sanskrit_devanagari == "अवलोकितेश्वर"
        assert result.tibetan_wylie == "spyan ras gzigs"

    def test_correct_witness_ids(self, collator):
        zh = {"id": "T251:1", "text": "test"}
        result = collator.align_segments(zh, chinese_witness="T250")
        assert result.chinese.witness_id == "T250"

    def test_correct_script_assignments(self, collator):
        from hrdaya.models import Script
        zh = {"id": "T251:1", "text": "test"}
        sa = {"id": "GRETIL:1", "iast": "test"}
        bo = {"id": "Toh21:1", "tibetan": "test"}
        result = collator.align_segments(zh, sa, bo)
        assert result.chinese.script == Script.TRADITIONAL_CHINESE
        assert result.sanskrit.script == Script.IAST
        assert result.tibetan.script == Script.TIBETAN


class TestLoadTibetanWitness:
    """Test load_tibetan_witness (MJ11 coverage gap)."""

    @pytest.fixture
    def collator(self):
        return HeartSutraCollator(DATA_DIR)

    def test_load_toh21(self, collator):
        data = collator.load_tibetan_witness("Toh21")
        assert "segments" in data
        assert len(data["segments"]) > 0

    def test_load_dunhuang_witness(self, collator):
        data = collator.load_tibetan_witness("IOL_Tib_J_751")
        assert "segments" in data

    def test_missing_tibetan_raises(self, collator):
        with pytest.raises(FileNotFoundError):
            collator.load_tibetan_witness("NONEXISTENT")

    def test_caching(self, collator):
        data1 = collator.load_tibetan_witness("Toh21")
        data2 = collator.load_tibetan_witness("Toh21")
        assert data1 is data2  # same object from cache


class TestLoadSanskritWitness:
    """Test load_sanskrit_witness edge cases (mn3)."""

    @pytest.fixture
    def collator(self):
        return HeartSutraCollator(DATA_DIR)

    def test_load_gretil(self, collator):
        data = collator.load_sanskrit_witness("GRETIL")
        assert "segments" in data

    def test_nonexistent_sanskrit_raises(self, collator):
        """Non-GRETIL unknown IDs should raise, not silently return GRETIL."""
        with pytest.raises(FileNotFoundError):
            collator.load_sanskrit_witness("NONEXISTENT_SANSKRIT")


class TestAnchorTraditionValidation:
    """Test that non-Chinese anchor_tradition raises ValueError."""

    @pytest.fixture
    def collator(self):
        return HeartSutraCollator(DATA_DIR)

    def test_sanskrit_anchor_raises(self, collator):
        with pytest.raises(ValueError, match="not supported"):
            collator.collate_section("opening", anchor_tradition="sanskrit")

    def test_tibetan_anchor_raises(self, collator):
        with pytest.raises(ValueError, match="not supported"):
            collator.collate_section("opening", anchor_tradition="tibetan")


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
        for section in ("opening", "form_emptiness", "mantra_praise", "mantra"):
            assert section in result["sections"], f"Missing section: {section}"

    def test_sections_contain_apparatus_entries(self):
        result = collate_full_text(DATA_DIR)
        opening = result["sections"]["opening"]
        assert isinstance(opening, list)
        assert len(opening) > 0
        assert "segment_id" in opening[0]
