"""Tests for data validation."""

import json
import tempfile
from pathlib import Path

import pytest
from hrdaya.validate import validate_witness_file, validate_data_dir


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


class TestValidateDataDir:
    """Test full data directory validation."""

    def test_data_dir_validates(self):
        errors = validate_data_dir(DATA_DIR)
        assert errors == {}, f"Validation errors: {errors}"
