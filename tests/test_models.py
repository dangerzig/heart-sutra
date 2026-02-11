"""Tests for data models."""

import pytest

from hrdaya.models import (
    WitnessType,
    VariantType,
    DependenceDirection,
    Script,
    Witness,
    Segment,
    Variant,
    MultilingualSegment,
    CriticalApparatus,
)


class TestEnums:
    """Test enum definitions."""

    def test_witness_types(self):
        assert WitnessType.CHINESE.value == "chinese"
        assert WitnessType.SANSKRIT.value == "sanskrit"
        assert WitnessType.TIBETAN.value == "tibetan"
        assert WitnessType.SOURCE.value == "source"

    def test_variant_types_complete(self):
        # Ensure all expected variant types exist
        expected = [
            "orthographic", "scribal_error", "stylistic", "register",
            "doctrinal", "expansion", "abbreviation", "extraction",
            "retranslation", "translation_choice", "grammatical",
            "distinctive", "uncertain",
        ]
        actual = [vt.value for vt in VariantType]
        for e in expected:
            assert e in actual, f"Missing VariantType: {e}"

    def test_dependence_directions(self):
        assert DependenceDirection.CHINESE_TO_SANSKRIT.value == "zh→sa"
        assert DependenceDirection.PRAJNAPARAMITA_TO_HEART.value == "pp→hs"

    def test_script_includes_ranjana_and_bhujimol(self):
        assert Script.RANJANA.value == "ranj"
        assert Script.BHUJIMOL.value == "bhuj"

    def test_script_includes_proto_sharada(self):
        assert Script.PROTO_SHARADA.value == "shrd"


class TestWitness:
    """Test Witness dataclass."""

    def test_create_witness(self):
        w = Witness(id="T251", name="Heart Sūtra", witness_type=WitnessType.CHINESE)
        assert w.id == "T251"
        assert w.witness_type == WitnessType.CHINESE
        assert w.date is None

    def test_witness_with_date(self):
        w = Witness(
            id="Ja", name="Hōryū-ji",
            witness_type=WitnessType.SANSKRIT,
            date="c. 8th c.",
        )
        assert w.date == "c. 8th c."
        assert w.date_circa is True


class TestSegment:
    """Test Segment dataclass."""

    def test_create_segment(self):
        s = Segment(id="T251:1", text="觀自在菩薩", witness_id="T251")
        assert s.id == "T251:1"
        assert s.witness_type == WitnessType.CHINESE


class TestVariant:
    """Test Variant dataclass."""

    def test_create_variant(self):
        v = Variant(
            segment_id="T251:2",
            position=0,
            base_reading="五蘊",
            variant_reading="五陰",
        )
        assert v.variant_type == VariantType.UNCERTAIN
        assert v.confidence == 0.5

    def test_confidence_too_high(self):
        with pytest.raises(ValueError, match="confidence must be between"):
            Variant(
                segment_id="T251:1", position=0,
                base_reading="a", variant_reading="b",
                confidence=1.5,
            )

    def test_confidence_too_low(self):
        with pytest.raises(ValueError, match="confidence must be between"):
            Variant(
                segment_id="T251:1", position=0,
                base_reading="a", variant_reading="b",
                confidence=-0.1,
            )

    def test_confidence_boundary_values(self):
        v0 = Variant(
            segment_id="T251:1", position=0,
            base_reading="a", variant_reading="b",
            confidence=0.0,
        )
        assert v0.confidence == 0.0
        v1 = Variant(
            segment_id="T251:1", position=0,
            base_reading="a", variant_reading="b",
            confidence=1.0,
        )
        assert v1.confidence == 1.0


class TestCriticalApparatus:
    """Test CriticalApparatus dataclass."""

    def test_defaults(self):
        ca = CriticalApparatus()
        assert ca.base_text_id == "T251"
        assert ca.methodology == "T251-anchored-multilingual"
        assert ca.segments == []
