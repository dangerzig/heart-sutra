"""
Prajñāpāramitāhṛdaya Critical Edition Library

A multilingual critical edition of the Heart Sūtra treating the text
as a textual complex with Chinese compositional priority.

Following the methodology of Nattier (1992) and subsequent scholarship,
this edition:
- Treats Chinese as the compositionally prior tradition
- Presents Sanskrit as evidence of reception and re-Sanskritization
- Uses Tibetan as mediating witness for triangulating transmission
- Explicitly annotates direction-of-dependence in variants

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
