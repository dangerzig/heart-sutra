"""Tests for witness catalog."""

from hrdaya.witnesses import (
    get_witness,
    get_all_witnesses,
    get_witnesses_by_type,
    CHINESE_WITNESSES,
    SANSKRIT_WITNESSES,
    TIBETAN_WITNESSES,
)
from hrdaya.models import WitnessType, Script


class TestWitnessCatalog:
    """Test witness catalog completeness and correctness."""

    def test_t251_exists(self):
        w = get_witness("T251")
        assert w is not None
        assert w.witness_type == WitnessType.CHINESE

    def test_t250_exists(self):
        w = get_witness("T250")
        assert w is not None

    def test_pancavimsati_in_sanskrit(self):
        """The Large PP parallel text should be in Sanskrit witnesses."""
        assert "Pancavimsati_Gilgit" in SANSKRIT_WITNESSES

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

    def test_gilgit_uses_proto_sharada(self):
        """Gilgit manuscripts should use PROTO_SHARADA, not DEVANAGARI."""
        gilgit = SANSKRIT_WITNESSES["Gilgit"]
        assert gilgit.script == Script.PROTO_SHARADA

    def test_pancavimsati_gilgit_uses_proto_sharada(self):
        pp = SANSKRIT_WITNESSES["Pancavimsati_Gilgit"]
        assert pp.script == Script.PROTO_SHARADA

    def test_ce_has_explicit_script(self):
        """Feer Polyglot Edition should have an explicit script set."""
        ce = SANSKRIT_WITNESSES["Ce"]
        assert ce.script == Script.SIDDHAM

    def test_witness_id_matches_dict_key(self):
        """Every witness's .id field must match its dictionary key."""
        for siglum, w in get_all_witnesses().items():
            assert w.id == siglum, f"Key {siglum} != witness.id {w.id}"


class TestGetWitnessesByType:
    """Test get_witnesses_by_type (MJ11 coverage + MJ6 fix)."""

    def test_chinese_excludes_source(self):
        """get_witnesses_by_type(CHINESE) should NOT include T223 (SOURCE type)."""
        chinese = get_witnesses_by_type(WitnessType.CHINESE)
        assert "T251" in chinese
        assert "T223" not in chinese, "T223 is SOURCE type, should not be in CHINESE"

    def test_source_includes_t223(self):
        sources = get_witnesses_by_type(WitnessType.SOURCE)
        assert "T223" in sources

    def test_parallel_includes_pancavimsati(self):
        parallels = get_witnesses_by_type(WitnessType.PARALLEL)
        assert "Pancavimsati_Gilgit" in parallels

    def test_sanskrit_excludes_parallel(self):
        """get_witnesses_by_type(SANSKRIT) should NOT include parallel texts."""
        sanskrit = get_witnesses_by_type(WitnessType.SANSKRIT)
        assert "Pancavimsati_Gilgit" not in sanskrit

    def test_tibetan_returns_only_tibetan(self):
        tibetan = get_witnesses_by_type(WitnessType.TIBETAN)
        for w in tibetan.values():
            assert w.witness_type == WitnessType.TIBETAN


class TestGetWitness:
    """Test get_witness lookup and caching."""

    def test_known_witness(self):
        w = get_witness("T251")
        assert w is not None
        assert w.id == "T251"

    def test_unknown_witness(self):
        assert get_witness("NONEXISTENT") is None

    def test_caching(self):
        """get_witness should use cached dict."""
        import hrdaya.witnesses as wmod
        saved = wmod._ALL_WITNESSES_CACHE
        try:
            wmod._ALL_WITNESSES_CACHE = None  # reset
            w1 = get_witness("T251")
            assert wmod._ALL_WITNESSES_CACHE is not None
            w2 = get_witness("T251")
            assert w1 is w2
        finally:
            wmod._ALL_WITNESSES_CACHE = saved
