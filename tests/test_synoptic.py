"""Tests for synoptic alignment builder."""

import pytest
from pathlib import Path
from hrdaya.synoptic import SynopticBuilder, SynopticAlignment, SynopticRow


DATA_DIR = Path(__file__).parent.parent / "data"


class TestSynopticBuilder:
    """Test synoptic alignment building."""

    @pytest.fixture
    def builder(self):
        return SynopticBuilder(DATA_DIR)

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
        assert len(md) > 0
        assert "Chinese" in md

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


class TestSynopticRow:
    """Test SynopticRow dataclass."""

    def test_defaults(self):
        row = SynopticRow(segment_id="test:1", section="opening")
        assert row.chinese == ""
        assert row.divergence_notes == []
