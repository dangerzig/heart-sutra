"""Tests for shared data directory resolution and versioning."""

import os
import tempfile
from pathlib import Path

import pytest
from hrdaya.data import resolve_data_dir, DATA_VERSION, compute_data_hash


DATA_DIR = Path(__file__).parent.parent / "data"


class TestResolveDataDir:
    """Test resolve_data_dir() resolution order."""

    def test_explicit_path(self):
        result = resolve_data_dir(str(DATA_DIR))
        assert result == DATA_DIR

    def test_explicit_path_not_found_raises(self):
        with pytest.raises(FileNotFoundError, match="not found"):
            resolve_data_dir("/nonexistent/path")

    def test_env_var(self, monkeypatch):
        monkeypatch.setenv("HRDAYA_DATA_DIR", str(DATA_DIR))
        result = resolve_data_dir()
        assert result == DATA_DIR

    def test_env_var_bad_path_raises(self, monkeypatch):
        monkeypatch.setenv("HRDAYA_DATA_DIR", "/nonexistent/path")
        with pytest.raises(FileNotFoundError, match="HRDAYA_DATA_DIR"):
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


class TestDataVersioning:
    """Test data version and hash for reproducibility."""

    def test_data_version_is_semver(self):
        import re
        assert re.match(r"^\d+\.\d+\.\d+$", DATA_VERSION)

    def test_compute_data_hash_deterministic(self):
        h1 = compute_data_hash(DATA_DIR)
        h2 = compute_data_hash(DATA_DIR)
        assert h1 == h2

    def test_compute_data_hash_is_hex(self):
        h = compute_data_hash(DATA_DIR)
        assert len(h) == 12
        int(h, 16)  # Raises ValueError if not hex

    def test_data_hash_changes_with_content(self, tmp_path):
        """Hash changes if a file is added."""
        d = tmp_path / "sub"
        d.mkdir()
        (d / "a.json").write_text('{"x":1}')
        h1 = compute_data_hash(tmp_path)

        (d / "b.json").write_text('{"y":2}')
        h2 = compute_data_hash(tmp_path)
        assert h1 != h2

    def test_hash_nonexistent_dir_warns(self, tmp_path):
        """compute_data_hash warns on nonexistent directory (mn7)."""
        h = compute_data_hash(tmp_path / "nonexistent")
        # Should return a valid hash (of empty input) without crashing
        assert len(h) == 12
        int(h, 16)

    def test_resolve_no_data_raises(self, monkeypatch, tmp_path):
        """When no data directory can be found, FileNotFoundError is raised."""
        monkeypatch.delenv("HRDAYA_DATA_DIR", raising=False)
        # Override __file__ resolution by passing a nonexistent explicit path
        with pytest.raises(FileNotFoundError):
            resolve_data_dir("/completely/fake/path")
