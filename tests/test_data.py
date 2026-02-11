"""Tests for data file integrity."""

import json
import pytest
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


class TestChineseData:
    """Test Chinese witness data files."""

    @pytest.mark.parametrize("filename", [
        "T251.json", "t250.json", "t257.json",
    ])
    def test_taisho_files_valid_json(self, filename):
        path = DATA_DIR / "chinese" / "taisho" / filename
        assert path.exists(), f"Required witness file {filename} not found"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert "segments" in data, f"{filename} missing 'segments' key"

    def test_t256_valid_json(self):
        """T256 is a transliteration text with different structure."""
        path = DATA_DIR / "chinese" / "taisho" / "t256.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert "id" in data, "t256.json missing 'id' key"
        assert "title_chinese" in data, "t256.json missing 'title_chinese' key"

    def test_t251_has_segments(self):
        path = DATA_DIR / "chinese" / "taisho" / "T251.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data["segments"]) > 0

    def test_t251_segments_have_required_fields(self):
        path = DATA_DIR / "chinese" / "taisho" / "T251.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for seg in data["segments"]:
            assert "id" in seg, f"Segment missing 'id': {seg}"
            assert "text" in seg, f"Segment missing 'text': {seg}"
            assert "section" in seg, f"Segment missing 'section': {seg}"


class TestSanskritData:
    """Test Sanskrit witness data files."""

    def test_gretil_valid_json(self):
        path = DATA_DIR / "sanskrit" / "gretil" / "prajnaparamitahrdaya.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert "segments" in data

    def test_gretil_segments_have_iast(self):
        path = DATA_DIR / "sanskrit" / "gretil" / "prajnaparamitahrdaya.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for seg in data["segments"]:
            assert "iast" in seg, f"Sanskrit segment missing 'iast': {seg.get('id')}"


class TestTibetanData:
    """Test Tibetan witness data files."""

    def test_toh21_valid_json(self):
        path = DATA_DIR / "tibetan" / "kangyur" / "toh21.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert "segments" in data


class TestCollationData:
    """Test collation data files."""

    def test_variant_table_valid_json(self):
        path = DATA_DIR / "collation" / "variant_table.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert isinstance(data, dict), "variant_table.json should be a dict"
        assert "sections" in data, "variant_table.json missing 'sections' key"
        assert "provenance" in data, "variant_table.json missing 'provenance' key"


class TestAlignedData:
    """Test aligned/synoptic data files."""

    def test_synoptic_alignment_valid_json(self):
        path = DATA_DIR / "aligned" / "synoptic_alignment.json"
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert isinstance(data, dict), "synoptic_alignment.json should be a dict"
        assert "rows" in data, "synoptic_alignment.json missing 'rows' key"
        assert len(data["rows"]) > 0, "synoptic_alignment.json should have rows"
