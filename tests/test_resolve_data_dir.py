"""Tests for shared data directory resolution."""

import os
import tempfile
from pathlib import Path

import pytest
from hrdaya.data import resolve_data_dir


DATA_DIR = Path(__file__).parent.parent / "data"


class TestResolveDataDir:
    """Test resolve_data_dir() resolution order."""

    def test_explicit_path(self):
        result = resolve_data_dir(str(DATA_DIR))
        assert result == DATA_DIR

    def test_explicit_path_not_found_exits(self):
        with pytest.raises(SystemExit, match="not found"):
            resolve_data_dir("/nonexistent/path")

    def test_env_var(self, monkeypatch):
        monkeypatch.setenv("HRDAYA_DATA_DIR", str(DATA_DIR))
        result = resolve_data_dir()
        assert result == DATA_DIR

    def test_env_var_bad_path_exits(self, monkeypatch):
        monkeypatch.setenv("HRDAYA_DATA_DIR", "/nonexistent/path")
        with pytest.raises(SystemExit, match="HRDAYA_DATA_DIR"):
            resolve_data_dir()

    def test_dev_tree_fallback(self):
        """When run from the repo, the dev-tree path should resolve."""
        result = resolve_data_dir()
        assert result.is_dir()
        assert (result / "chinese").is_dir()

    def test_explicit_overrides_env(self, monkeypatch):
        """Explicit path takes priority over environment variable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            monkeypatch.setenv("HRDAYA_DATA_DIR", str(DATA_DIR))
            result = resolve_data_dir(tmpdir)
            assert result == Path(tmpdir)
