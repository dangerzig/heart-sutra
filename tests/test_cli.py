"""Tests for CLI main() entry points."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


DATA_DIR = Path(__file__).parent.parent / "data"
PYTHON = sys.executable


class TestCollateCLI:
    """Test collate.main() via subprocess."""

    def test_collate_produces_json(self):
        result = subprocess.run(
            [PYTHON, "-m", "hrdaya.collate", str(DATA_DIR)],
            capture_output=True, text=True, timeout=30,
            env={"PYTHONPATH": str(Path(__file__).parent.parent / "src"),
                 "PATH": ""},
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "provenance" in data
        assert "sections" in data

    def test_collate_bad_path_fails(self):
        result = subprocess.run(
            [PYTHON, "-m", "hrdaya.collate", "/nonexistent/path"],
            capture_output=True, text=True, timeout=10,
            env={"PYTHONPATH": str(Path(__file__).parent.parent / "src"),
                 "PATH": ""},
        )
        assert result.returncode != 0


class TestSynopticCLI:
    """Test synoptic.main() via subprocess."""

    def test_synoptic_markdown(self):
        result = subprocess.run(
            [PYTHON, "-m", "hrdaya.synoptic", "markdown",
             "--data-dir", str(DATA_DIR)],
            capture_output=True, text=True, timeout=30,
            env={"PYTHONPATH": str(Path(__file__).parent.parent / "src"),
                 "PATH": ""},
        )
        assert result.returncode == 0
        assert "Chinese" in result.stdout

    def test_synoptic_json(self):
        result = subprocess.run(
            [PYTHON, "-m", "hrdaya.synoptic", "json",
             "--data-dir", str(DATA_DIR)],
            capture_output=True, text=True, timeout=30,
            env={"PYTHONPATH": str(Path(__file__).parent.parent / "src"),
                 "PATH": ""},
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "rows" in data

    def test_synoptic_help(self):
        result = subprocess.run(
            [PYTHON, "-m", "hrdaya.synoptic", "--help"],
            capture_output=True, text=True, timeout=10,
            env={"PYTHONPATH": str(Path(__file__).parent.parent / "src"),
                 "PATH": ""},
        )
        assert result.returncode == 0
        assert "format" in result.stdout.lower()


class TestValidateCLI:
    """Test validate.main() via subprocess."""

    def test_validate_passes(self):
        result = subprocess.run(
            [PYTHON, "-m", "hrdaya.validate", str(DATA_DIR)],
            capture_output=True, text=True, timeout=30,
            env={"PYTHONPATH": str(Path(__file__).parent.parent / "src"),
                 "PATH": ""},
        )
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "All data files valid" in output
