"""Tests for data validation."""

import json
import tempfile
from pathlib import Path

import pytest
from hrdaya.validate import (
    validate_witness_file,
    validate_data_dir,
    validate_cross_references,
    KNOWN_SECTIONS,
)


DATA_DIR = Path(__file__).parent.parent / "data"


class TestValidateWitnessFile:
    """Test individual witness file validation."""

    def test_valid_chinese_file(self):
        path = DATA_DIR / "chinese" / "taisho" / "T251.json"
        errors = validate_witness_file(path, "chinese")
        assert errors == []

    def test_valid_sanskrit_file(self):
        path = DATA_DIR / "sanskrit" / "gretil" / "prajnaparamitahrdaya.json"
        errors = validate_witness_file(path, "sanskrit")
        assert errors == []

    def test_valid_tibetan_file(self):
        path = DATA_DIR / "tibetan" / "kangyur" / "toh21.json"
        errors = validate_witness_file(path, "tibetan")
        assert errors == []

    def test_valid_tibetan_dunhuang_file(self):
        path = DATA_DIR / "tibetan" / "dunhuang" / "iol_tib_j_751.json"
        errors = validate_witness_file(path, "tibetan")
        assert errors == []

    def test_missing_file(self):
        errors = validate_witness_file(Path("/nonexistent.json"), "chinese")
        assert len(errors) == 1
        assert "not found" in errors[0].lower()

    def test_invalid_json(self):
        with tempfile.NamedTemporaryFile(suffix=".json", mode='w', delete=False) as f:
            f.write("{bad json")
            path = Path(f.name)
        errors = validate_witness_file(path, "chinese")
        assert len(errors) == 1
        assert "Invalid JSON" in errors[0]
        path.unlink()

    def test_alternate_structure_accepted(self):
        """T256 has id/title_chinese instead of segments."""
        path = DATA_DIR / "chinese" / "taisho" / "t256.json"
        if path.exists():
            errors = validate_witness_file(path, "chinese")
            assert errors == []

    def test_kangyur_editions_accepted(self):
        """kangyur_editions.json has editions key instead of segments."""
        path = DATA_DIR / "tibetan" / "kangyur" / "kangyur_editions.json"
        if path.exists():
            errors = validate_witness_file(path, "tibetan")
            assert errors == []


class TestSchemaValidation:
    """Test schema-level checks added in v6."""

    def test_unknown_section_flagged(self):
        with tempfile.NamedTemporaryFile(suffix=".json", mode='w', delete=False) as f:
            json.dump({"segments": [
                {"id": "X:1", "section": "nonexistent_section", "text": "abc"}
            ]}, f)
            path = Path(f.name)
        errors = validate_witness_file(path, "chinese")
        assert any("unknown section" in e for e in errors)
        path.unlink()

    def test_bad_base_parallel_format_flagged(self):
        with tempfile.NamedTemporaryFile(suffix=".json", mode='w', delete=False) as f:
            json.dump({"segments": [
                {"id": "X:1", "section": "opening", "text": "abc",
                 "base_parallel": "bad-format"}
            ]}, f)
            path = Path(f.name)
        errors = validate_witness_file(path, "chinese")
        assert any("does not match expected pattern" in e for e in errors)
        path.unlink()

    def test_valid_base_parallel_accepted(self):
        with tempfile.NamedTemporaryFile(suffix=".json", mode='w', delete=False) as f:
            json.dump({"segments": [
                {"id": "X:1", "section": "opening", "text": "abc",
                 "base_parallel": "T251:1"}
            ]}, f)
            path = Path(f.name)
        errors = validate_witness_file(path, "chinese")
        assert errors == []
        path.unlink()

    def test_empty_required_field_flagged(self):
        with tempfile.NamedTemporaryFile(suffix=".json", mode='w', delete=False) as f:
            json.dump({"segments": [
                {"id": "X:1", "section": "opening", "text": ""}
            ]}, f)
            path = Path(f.name)
        errors = validate_witness_file(path, "chinese")
        assert any("is empty" in e for e in errors)
        path.unlink()

    def test_known_sections_includes_long_recension(self):
        """Long recension sections must be recognized."""
        assert "nidana" in KNOWN_SECTIONS
        assert "colophon" in KNOWN_SECTIONS
        assert "buddha_approval" in KNOWN_SECTIONS


class TestValidateCrossReferences:
    """Test cross-file reference validation."""

    def test_cross_references_valid(self):
        errors = validate_cross_references(DATA_DIR)
        assert errors == [], f"Cross-reference errors: {errors}"


class TestUnknownWitnessType:
    """Test that unknown witness_type raises ValueError (MJ4)."""

    def test_unknown_type_raises(self, tmp_path):
        path = tmp_path / "test.json"
        path.write_text(json.dumps({"segments": [
            {"id": "X:1", "section": "opening", "text": "abc"}
        ]}))
        with pytest.raises(ValueError, match="Unknown witness_type"):
            validate_witness_file(path, "pali")

    def test_typo_type_raises(self, tmp_path):
        path = tmp_path / "test.json"
        path.write_text(json.dumps({"segments": [
            {"id": "X:1", "section": "opening", "text": "abc"}
        ]}))
        with pytest.raises(ValueError, match="Unknown witness_type"):
            validate_witness_file(path, "sanskri")


class TestDuplicateSegmentIds:
    """Test that duplicate segment IDs are caught."""

    def test_duplicate_id_flagged(self, tmp_path):
        path = tmp_path / "dup.json"
        path.write_text(json.dumps({"segments": [
            {"id": "X:1", "section": "opening", "text": "a"},
            {"id": "X:1", "section": "opening", "text": "b"},
        ]}))
        errors = validate_witness_file(path, "chinese")
        assert any("duplicate" in e for e in errors)


class TestAlternateStructureValidation:
    """Test tightened alternate structure detection (mn12)."""

    def test_only_id_rejected(self, tmp_path):
        """A JSON with only 'id' and no other recognized key is rejected."""
        path = tmp_path / "only_id.json"
        path.write_text(json.dumps({"id": "test", "random_key": "value"}))
        errors = validate_witness_file(path, "chinese")
        assert any("missing 'segments'" in e for e in errors)

    def test_id_plus_description_accepted(self, tmp_path):
        """A JSON with 'id' + 'description' (both recognized) is accepted."""
        path = tmp_path / "alt.json"
        path.write_text(json.dumps({"id": "test", "description": "something"}))
        errors = validate_witness_file(path, "chinese")
        assert errors == []


class TestValidateDataDir:
    """Test full data directory validation."""

    def test_data_dir_validates(self):
        errors = validate_data_dir(DATA_DIR)
        assert errors == {}, f"Validation errors: {errors}"
