"""
Transliteration utilities for Sanskrit between Devanagari and IAST.

Delegates to the ``indic-transliteration`` library (Vishvas Vasuki et al.),
the standard package used across Sanskrit digital humanities projects.

Provides bidirectional conversion between:
- Devanagari (देवनागरी)
- IAST (International Alphabet of Sanskrit Transliteration)

Supported scope — everything the ``indic-transliteration`` library supports
for IAST ↔ Devanagari, including:
- All standard vowels, consonants, anusvāra, visarga, candrabindu
- Conjunct consonants (virāma stacking)
- Special characters: oṃ (→ ॐ), avagraha (ऽ), numerals

Limitations:
- Sandhi is NOT handled.  Input must be pre-segmented words.
- Vedic accents (udātta/svarita) are not supported by the IAST scheme.

Use ``validate_iast()`` to check whether a string contains only valid
IAST characters before conversion.
"""

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def devanagari_to_iast(text: str) -> str:
    """
    Convert Devanagari text to IAST transliteration.

    Args:
        text: Text in Devanagari script.

    Returns:
        IAST transliteration.
    """
    if not text:
        return ""
    return transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)


def iast_to_devanagari(text: str) -> str:
    """
    Convert IAST transliteration to Devanagari.

    Args:
        text: Text in IAST transliteration.

    Returns:
        Devanagari text.
    """
    if not text:
        return ""
    return transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)


# Characters that are valid in IAST text (lowercase).  Includes all
# consonant and vowel letters, diacritics, and common punctuation.
# ASCII letters f, q, w, x, z are deliberately excluded — they do not
# appear in standard IAST transliteration.
_VALID_IAST_CHARS = frozenset(
    "abcdeghijklmnoprstuvyāīūṛṝḷḹṃḥṁñṅṭḍṇśṣ"
    " .,;:!?-–—'\"()[]{}|"
    "0123456789"
    "\n\r\t"
)


def validate_iast(text: str) -> list[str]:
    """
    Check whether *text* contains only valid IAST characters.

    Returns a list of error strings (empty if input is valid IAST).
    Non-IAST characters (Chinese, Tibetan, Cyrillic, etc.) will be
    flagged with their position and Unicode codepoint.

    Args:
        text: Text to validate.

    Returns:
        List of error messages (empty means valid).
    """
    errors = []
    for i, ch in enumerate(text):
        if ch.lower() not in _VALID_IAST_CHARS:
            errors.append(
                f"position {i}: unexpected character '{ch}' (U+{ord(ch):04X})"
            )
    return errors


def normalize_iast(text: str) -> str:
    """
    Normalize IAST text to standard form.

    Handles common variations:
    - ṁ/ṃ normalization (anusvāra)
    - Smart/curly quote normalization
    """
    if not text:
        return text or ""
    # Normalize anusvāra (both cases)
    text = text.replace('ṁ', 'ṃ').replace('Ṁ', 'Ṃ')

    # Normalize curly/smart quotes to straight quotes
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")

    return text
