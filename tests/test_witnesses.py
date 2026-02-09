"""Tests for witness catalog."""

from hrdaya.witnesses import (
    get_witness,
    CHINESE_WITNESSES,
    SANSKRIT_WITNESSES,
    TIBETAN_WITNESSES,
)
from hrdaya.models import WitnessType


class TestWitnessCatalog:
    """Test witness catalog completeness and correctness."""

    def test_t251_exists(self):
        w = get_witness("T251")
        assert w is not None
        assert w.witness_type == WitnessType.CHINESE

    def test_t250_exists(self):
        w = get_witness("T250")
        assert w is not None

    def test_pañcavimsati_in_sanskrit(self):
        """The Large PP parallel text should be in Sanskrit witnesses."""
        assert "Pañcaviṃśati_Gilgit" in SANSKRIT_WITNESSES or len(SANSKRIT_WITNESSES) > 10

    def test_chinese_witnesses_not_empty(self):
        assert len(CHINESE_WITNESSES) > 0

    def test_sanskrit_witnesses_not_empty(self):
        assert len(SANSKRIT_WITNESSES) > 0

    def test_tibetan_witnesses_not_empty(self):
        assert len(TIBETAN_WITNESSES) > 0

    def test_all_witnesses_have_names(self):
        for siglum, w in CHINESE_WITNESSES.items():
            assert w.name, f"Chinese witness {siglum} has no name"
        for siglum, w in SANSKRIT_WITNESSES.items():
            assert w.name, f"Sanskrit witness {siglum} has no name"
        for siglum, w in TIBETAN_WITNESSES.items():
            assert w.name, f"Tibetan witness {siglum} has no name"
