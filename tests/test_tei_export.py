"""Tests for TEI-XML export module."""

import re
import tempfile
from pathlib import Path

import pytest
from lxml import etree

from hrdaya.tei_export import (
    TEI_NS,
    XML_NS,
    export_tei,
    generate_chinese_text,
    generate_sanskrit_text,
    generate_standoff_alignment,
    generate_tei_header,
    generate_tibetan_text,
    _load_tradition_witnesses,
    _seg_xml_id,
)


@pytest.fixture
def data_dir():
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def tei_tree(data_dir):
    """Generate the full TEI document and parse it."""
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
        output_path = Path(f.name)
    try:
        export_tei(output_path=output_path, data_dir=data_dir)
        tree = etree.parse(str(output_path))
    finally:
        output_path.unlink(missing_ok=True)
    return tree


NS = {"tei": TEI_NS}


class TestWellFormed:
    """Verify the generated XML is well-formed and parseable."""

    def test_export_produces_valid_xml(self, data_dir):
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
            output_path = Path(f.name)
        path = export_tei(output_path=output_path, data_dir=data_dir)
        assert path.exists()
        # Must parse without error
        tree = etree.parse(str(path))
        assert tree.getroot() is not None
        path.unlink()

    def test_root_element_is_tei(self, tei_tree):
        root = tei_tree.getroot()
        assert root.tag == f"{{{TEI_NS}}}TEI"


class TestStructure:
    """Verify the TEI document has the expected structure."""

    def test_has_tei_header(self, tei_tree):
        headers = tei_tree.xpath("//tei:teiHeader", namespaces=NS)
        assert len(headers) == 1

    def test_has_standoff(self, tei_tree):
        standoffs = tei_tree.xpath("//tei:standOff", namespaces=NS)
        assert len(standoffs) == 1

    def test_has_group_with_three_texts(self, tei_tree):
        groups = tei_tree.xpath("//tei:group", namespaces=NS)
        assert len(groups) == 1
        texts = groups[0].xpath("tei:text", namespaces=NS)
        assert len(texts) == 3

    def test_language_codes(self, tei_tree):
        texts = tei_tree.xpath("//tei:group/tei:text", namespaces=NS)
        langs = [t.get(f"{{{XML_NS}}}lang") for t in texts]
        assert "lzh" in langs
        assert "sa" in langs
        assert "bo" in langs

    def test_header_has_list_wit(self, tei_tree):
        list_wits = tei_tree.xpath(
            "//tei:teiHeader//tei:listWit", namespaces=NS
        )
        assert len(list_wits) == 1
        witnesses = list_wits[0].xpath("tei:witness", namespaces=NS)
        assert len(witnesses) > 0

    def test_header_has_variant_encoding(self, tei_tree):
        enc = tei_tree.xpath(
            "//tei:encodingDesc/tei:variantEncoding", namespaces=NS
        )
        assert len(enc) == 1
        assert enc[0].get("method") == "parallel-segmentation"


class TestCrossReferences:
    """Verify that internal references resolve correctly."""

    def test_link_targets_resolve(self, tei_tree):
        """Every target in <link> should reference an existing xml:id."""
        all_ids = set()
        for el in tei_tree.iter():
            xml_id = el.get(f"{{{XML_NS}}}id")
            if xml_id:
                all_ids.add(xml_id)

        links = tei_tree.xpath(
            "//tei:standOff//tei:link", namespaces=NS
        )
        assert len(links) > 0, "No alignment links found"

        unresolved = []
        for link in links:
            targets = link.get("target", "").split()
            for target in targets:
                target_id = target.lstrip("#")
                if target_id not in all_ids:
                    unresolved.append(target_id)

        assert unresolved == [], (
            f"Unresolved link targets: {unresolved[:5]}"
        )

    def test_wit_attributes_resolve(self, tei_tree):
        """Every @wit in <lem>/<rdg> should reference a witness in <listWit>."""
        wit_ids = set()
        for w in tei_tree.xpath("//tei:listWit/tei:witness", namespaces=NS):
            xml_id = w.get(f"{{{XML_NS}}}id")
            if xml_id:
                wit_ids.add(xml_id)

        unresolved = []
        for el in tei_tree.xpath("//tei:lem | //tei:rdg", namespaces=NS):
            wit = el.get("wit", "")
            for ref in wit.split():
                ref_id = ref.lstrip("#")
                if ref_id not in wit_ids:
                    unresolved.append(ref_id)

        assert unresolved == [], (
            f"Unresolved witness refs: {set(unresolved)}"
        )


class TestChineseText:
    """Test the Chinese text section."""

    def test_chinese_has_segments(self, tei_tree):
        segs = tei_tree.xpath(
            "//tei:text[@xml:lang='lzh']//tei:seg", namespaces=NS
        )
        assert len(segs) >= 12

    def test_chinese_has_apparatus(self, tei_tree):
        apps = tei_tree.xpath(
            "//tei:text[@xml:lang='lzh']//tei:app", namespaces=NS
        )
        assert len(apps) > 0, "Chinese text should have apparatus entries"

    def test_apparatus_has_lem_and_rdg(self, tei_tree):
        app = tei_tree.xpath(
            "//tei:text[@xml:lang='lzh']//tei:app", namespaces=NS
        )[0]
        lems = app.xpath("tei:lem", namespaces=NS)
        rdgs = app.xpath("tei:rdg", namespaces=NS)
        assert len(lems) == 1
        assert len(rdgs) >= 1


class TestSanskritText:
    """Test the Sanskrit text section."""

    def test_sanskrit_has_segments(self, tei_tree):
        segs = tei_tree.xpath(
            "//tei:text[@xml:lang='sa']//tei:seg", namespaces=NS
        )
        assert len(segs) >= 12


class TestTibetanText:
    """Test the Tibetan text section."""

    def test_tibetan_has_segments(self, tei_tree):
        segs = tei_tree.xpath(
            "//tei:text[@xml:lang='bo']//tei:seg", namespaces=NS
        )
        assert len(segs) >= 12


class TestEmptyInputs:
    """Test behavior with empty or missing witness data."""

    def test_empty_tradition_returns_empty_list(self, tmp_path):
        """Loading a nonexistent tradition directory returns empty list."""
        witnesses = _load_tradition_witnesses(tmp_path, "nonexistent")
        assert witnesses == []

    def test_chinese_text_with_no_witnesses(self, data_dir):
        """generate_chinese_text with empty witness list returns minimal element."""
        el = generate_chinese_text(data_dir, [])
        assert el.tag.endswith("text")

    def test_sanskrit_text_with_no_witnesses(self):
        """generate_sanskrit_text with empty witness list returns minimal element."""
        el = generate_sanskrit_text([])
        assert el.tag.endswith("text")

    def test_tibetan_text_with_no_witnesses(self):
        """generate_tibetan_text with empty witness list returns minimal element."""
        el = generate_tibetan_text([])
        assert el.tag.endswith("text")

    def test_standoff_with_no_chinese_base(self):
        """standoff with empty Chinese witnesses returns element with no links."""
        el = generate_standoff_alignment([], [], [])
        assert el.tag.endswith("standOff")

    def test_malformed_json_skipped(self, tmp_path):
        """Malformed JSON files are skipped without crashing."""
        tradition_dir = tmp_path / "chinese" / "taisho"
        tradition_dir.mkdir(parents=True)
        (tradition_dir / "bad.json").write_text("{invalid json")
        witnesses = _load_tradition_witnesses(tmp_path, "chinese")
        assert witnesses == []


class TestLinkTargetAttribute:
    """Verify <link> uses 'target' (singular), not 'targets' (CR1)."""

    def test_link_uses_target_not_targets(self, tei_tree):
        links = tei_tree.xpath("//tei:standOff//tei:link", namespaces=NS)
        for link in links:
            assert link.get("target") is not None, "link should have 'target' attribute"
            assert link.get("targets") is None, "link should NOT have 'targets' (plural)"


class TestHeaderWitnessIds:
    """Verify header witness IDs are properly sanitized (MJ8)."""

    def test_witness_ids_are_valid_xml(self, tei_tree):
        """All witness xml:id attributes should be valid (no spaces/colons)."""
        for w in tei_tree.xpath("//tei:listWit/tei:witness", namespaces=NS):
            xml_id = w.get(f"{{{XML_NS}}}id")
            if xml_id:
                assert " " not in xml_id, f"Space in witness id: {xml_id}"
                assert ":" not in xml_id, f"Colon in witness id: {xml_id}"


class TestSegXmlId:
    """Test the XML ID generation helper."""

    def test_basic_id(self):
        assert _seg_xml_id("T251") == "T251"

    def test_spaces_replaced(self):
        assert _seg_xml_id("IOL Tib J 751:3") == "IOL_Tib_J_751-3"

    def test_colons_replaced(self):
        assert _seg_xml_id("T251:1") == "T251-1"
