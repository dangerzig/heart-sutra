"""Shared test fixtures for the Heart Sūtra critical edition."""

import pytest
from pathlib import Path


@pytest.fixture
def data_dir():
    """Path to the project data directory."""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def src_dir():
    """Path to the project src directory."""
    return Path(__file__).parent.parent / "src"
