"""
Prajñāpāramitāhṛdaya Critical Edition Library

A multilingual critical edition of the Heart Sūtra treating the text
as a textual complex with T251 as the default alignment anchor.

Following the methodology of Nattier (1992) and subsequent scholarship,
this edition:
- Uses T251 as the default alignment anchor (configurable)
- Presents witnesses from Chinese, Sanskrit, and Tibetan traditions
- Explicitly annotates direction-of-dependence in variants
- Remains neutral regarding the direction of textual dependence

Requires: Python 3.10+
"""

from .models import (
    Witness,
    WitnessType,
    Script,
    Segment,
    Token,
    Variant,
    VariantType,
    DependenceDirection,
    MultilingualSegment,
    CriticalApparatus,
)

__version__ = "1.0.0"
__all__ = [
    "Witness",
    "WitnessType",
    "Script",
    "Segment",
    "Token",
    "Variant",
    "VariantType",
    "DependenceDirection",
    "MultilingualSegment",
    "CriticalApparatus",
]
