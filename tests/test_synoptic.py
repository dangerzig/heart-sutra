"""Tests for synoptic alignment builder."""

import pytest
from pathlib import Path
from hrdaya.synoptic import SynopticBuilder, SynopticAlignment, SynopticRow, build_synoptic


DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture
def builder():
    return SynopticBuilder(DATA_DIR)


class TestSynopticBuilder:
    """Test synoptic alignment building."""

    def test_build_alignment(self, builder):
        alignment = builder.build_alignment()
        assert isinstance(alignment, SynopticAlignment)
        assert len(alignment.rows) > 0

    def test_alignment_has_chinese(self, builder):
        alignment = builder.build_alignment()
        for row in alignment.rows:
            assert row.chinese, f"Row {row.segment_id} missing Chinese text"

    def test_to_markdown(self, builder):
        alignment = builder.build_alignment()
        md = builder.to_markdown(alignment)
        assert isinstance(md, str)
        assert len(md) > 100, "Markdown should contain substantial content"
        assert "Chinese" in md
        assert "Sanskrit" in md
        assert "Tibetan" in md

    def test_to_json(self, builder):
        import json
        alignment = builder.build_alignment()
        result = builder.to_json(alignment)
        data = json.loads(result)
        assert "rows" in data

    def test_to_html(self, builder):
        alignment = builder.build_alignment()
        html = builder.to_html(alignment)
        assert "<html" in html
        assert "<table" in html

    def test_html_has_lang_attributes(self, builder):
        """HTML output should have lang attributes on multilingual spans (np3)."""
        alignment = builder.build_alignment()
        html = builder.to_html(alignment)
        assert "lang='lzh'" in html, "Chinese spans need lang='lzh'"
        assert "lang='sa-Latn'" in html or "lang='sa-Deva'" in html, "Sanskrit spans need lang attrs"
        assert "lang='bo'" in html, "Tibetan spans need lang='bo'"


class TestBuildSynoptic:
    """Test the high-level build_synoptic entry point."""

    def test_markdown_output(self):
        result = build_synoptic(DATA_DIR, "markdown")
        assert isinstance(result, str)
        assert "Chinese" in result
        assert "Sanskrit" in result

    def test_html_output(self):
        result = build_synoptic(DATA_DIR, "html")
        assert "<html" in result
        assert "<table" in result

    def test_json_output(self):
        import json
        result = build_synoptic(DATA_DIR, "json")
        data = json.loads(result)
        assert "rows" in data
        prov = data["provenance"]
        assert "data_version" in prov
        assert "data_hash" in prov
        assert len(prov["data_hash"]) == 12

    def test_unknown_format_raises(self):
        with pytest.raises(ValueError, match="Unknown format"):
            build_synoptic(DATA_DIR, "xml")


class TestSynopticErrorPaths:
    """Test error handling in synoptic builder."""

    def test_unknown_tradition_raises(self, builder):
        with pytest.raises(ValueError, match="Unknown tradition"):
            builder.load_witness("pali", "test")

    def test_missing_witness_returns_empty(self, builder):
        result = builder.load_witness("chinese", "NONEXISTENT_WITNESS")
        assert result == {}

    def test_malformed_json_returns_empty(self, tmp_path):
        """Synoptic builder handles malformed JSON gracefully."""
        chinese_dir = tmp_path / "chinese" / "taisho"
        chinese_dir.mkdir(parents=True)
        (chinese_dir / "bad.json").write_text("{invalid")
        builder = SynopticBuilder(tmp_path)
        result = builder.load_witness("chinese", "bad")
        assert result == {}


class TestAnchorTraditionValidation:
    """Test anchor_tradition parameter validation (CR3)."""

    def test_sanskrit_anchor_raises(self, builder):
        with pytest.raises(ValueError, match="not supported"):
            builder.build_alignment(anchor_tradition="sanskrit")

    def test_tibetan_anchor_raises(self, builder):
        with pytest.raises(ValueError, match="not supported"):
            builder.build_alignment(anchor_tradition="tibetan")

    def test_chinese_anchor_works(self, builder):
        alignment = builder.build_alignment(anchor_tradition="chinese")
        assert len(alignment.rows) > 0


class TestSynopticRow:
    """Test SynopticRow dataclass."""

    def test_defaults(self):
        row = SynopticRow(segment_id="test:1", section="opening")
        assert row.chinese == ""
        assert row.divergence_notes == []
