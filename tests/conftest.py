"""Shared test fixtures for the Heart Sūtra critical edition."""

import pytest
from pathlib import Path

from hrdaya.collate import HeartSutraCollator


DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture
def data_dir():
    """Path to the project data directory."""
    return DATA_DIR


@pytest.fixture
def collator():
    """Shared HeartSutraCollator instance for tests."""
    return HeartSutraCollator(DATA_DIR)
