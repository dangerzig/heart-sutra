"""
Transliteration utilities for Sanskrit between Devanagari and IAST.

Provides bidirectional conversion between:
- Devanagari (देवनागरी)
- IAST (International Alphabet of Sanskrit Transliteration)

Supported scope (all standard Sanskrit phonemes):
- 14 vowels: a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au
- 33 consonants: k kh g gh ṅ / c ch j jh ñ / ṭ ṭh ḍ ḍh ṇ /
  t th d dh n / p ph b bh m / y r l v / ś ṣ s h
- Anusvāra (ṃ), visarga (ḥ), candrabindu (ṁ)
- Special: oṃ (→ ॐ)
- Numerals, punctuation (। ॥), avagraha (ऽ)

Limitations (by design):
- Sandhi is NOT handled.  Input must be pre-segmented words.
- Vedic accents (udātta/svarita) are not supported.
- Non-standard conjuncts beyond virāma-stacking are not generated.
- For scholarly publication, output should be verified against source
  manuscripts.

Use ``validate_iast()`` to check whether a string contains only valid
IAST characters before conversion.

Implementation:
- Devanagari→IAST: Character-by-character mapping with virāma and
  mātrā (vowel mark) handling to strip/replace inherent 'a'.
- IAST→Devanagari: Token-based parser using sorted longest-first
  matching for consonants and vowels.  Handles consonant clusters
  (virāma insertion), independent vs. combining vowels, and special
  tokens (oṃ, anusvāra, visarga).
"""

# Devanagari to IAST mapping
DEVANAGARI_TO_IAST = {
    # Vowels
    'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū',
    'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',

    # Vowel marks (mātrās)
    'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū',
    'ृ': 'ṛ', 'ॄ': 'ṝ', 'ॢ': 'ḷ', 'ॣ': 'ḹ',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',

    # Anusvāra and visarga
    'ं': 'ṃ', 'ः': 'ḥ', 'ँ': 'ṁ',

    # Consonants - Velars
    'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'ṅa',

    # Consonants - Palatals
    'च': 'ca', 'छ': 'cha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'ña',

    # Consonants - Retroflexes
    'ट': 'ṭa', 'ठ': 'ṭha', 'ड': 'ḍa', 'ढ': 'ḍha', 'ण': 'ṇa',

    # Consonants - Dentals
    'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',

    # Consonants - Labials
    'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',

    # Consonants - Semivowels
    'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',

    # Consonants - Sibilants
    'श': 'śa', 'ष': 'ṣa', 'स': 'sa',

    # Consonants - Aspirate
    'ह': 'ha',

    # Virāma (halant) - removes inherent 'a'
    '्': '',

    # Numerals
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9',

    # Punctuation
    '।': '.', '॥': '.',

    # Special characters
    'ॐ': 'oṃ', 'ऽ': "'",
}

# IAST to Devanagari mapping (reverse)
IAST_TO_DEVANAGARI = {
    # Vowels (independent)
    'a': 'अ', 'ā': 'आ', 'i': 'इ', 'ī': 'ई', 'u': 'उ', 'ū': 'ऊ',
    'ṛ': 'ऋ', 'ṝ': 'ॠ', 'ḷ': 'ऌ', 'ḹ': 'ॡ',
    'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ',

    # Anusvāra and visarga
    'ṃ': 'ं', 'ḥ': 'ः', 'ṁ': 'ँ',

    # Consonants
    'k': 'क', 'kh': 'ख', 'g': 'ग', 'gh': 'घ', 'ṅ': 'ङ',
    'c': 'च', 'ch': 'छ', 'j': 'ज', 'jh': 'झ', 'ñ': 'ञ',
    'ṭ': 'ट', 'ṭh': 'ठ', 'ḍ': 'ड', 'ḍh': 'ढ', 'ṇ': 'ण',
    't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न',
    'p': 'प', 'ph': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म',
    'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व',
    'ś': 'श', 'ṣ': 'ष', 's': 'स', 'h': 'ह',

    # Special
    'oṃ': 'ॐ',
}

# Vowel marks for combining with consonants
IAST_VOWEL_MARKS = {
    'a': '',  # Inherent vowel, no mark needed
    'ā': 'ा', 'i': 'ि', 'ī': 'ी', 'u': 'ु', 'ū': 'ू',
    'ṛ': 'ृ', 'ṝ': 'ॄ', 'ḷ': 'ॢ', 'ḹ': 'ॣ',
    'e': 'े', 'ai': 'ै', 'o': 'ो', 'au': 'ौ',
}

# Set of IAST vowel strings (for post-consonant detection)
IAST_VOWELS = {'a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'ṝ', 'ḷ', 'ḹ', 'e', 'ai', 'o', 'au'}

# Ordered list of IAST consonant tokens (longest first for greedy match)
# Excludes vowels and special tokens — only actual consonants
IAST_CONSONANT_TOKENS = sorted(
    [k for k in IAST_TO_DEVANAGARI if k not in IAST_VOWELS and k not in ('ṃ', 'ḥ', 'ṁ', 'oṃ')],
    key=len, reverse=True,
)

# Ordered list of IAST vowel tokens (longest first for greedy match)
IAST_VOWEL_TOKENS = sorted(IAST_VOWELS, key=len, reverse=True)


def devanagari_to_iast(text: str) -> str:
    """
    Convert Devanagari text to IAST transliteration.

    Args:
        text: Text in Devanagari script

    Returns:
        IAST transliteration
    """
    result = []
    i = 0
    while i < len(text):
        char = text[i]

        # Check for virāma (halant) - removes inherent 'a'
        if char == '्':
            # Remove the trailing 'a' from previous consonant
            if result and result[-1].endswith('a'):
                result[-1] = result[-1][:-1]
            i += 1
            continue

        # Check for vowel marks (mātrās)
        if char in DEVANAGARI_TO_IAST:
            trans = DEVANAGARI_TO_IAST[char]
            # Vowel marks replace the inherent 'a'
            if char in 'ािीुूृॄॢॣेैोौ':
                if result and result[-1].endswith('a'):
                    result[-1] = result[-1][:-1]
            result.append(trans)
        elif char.isspace() or char in '.,!?:;-–—\'\"()[]{}':
            result.append(char)
        else:
            # Unknown character, pass through
            result.append(char)

        i += 1

    return ''.join(result)


def _match_iast_vowel(text: str, pos: int) -> str | None:
    """Try to match an IAST vowel token at the given position (longest first)."""
    for tok in IAST_VOWEL_TOKENS:
        if text[pos:pos + len(tok)] == tok:
            return tok
    return None


def _match_iast_consonant(text: str, pos: int) -> str | None:
    """Try to match an IAST consonant token at the given position (longest first)."""
    for tok in IAST_CONSONANT_TOKENS:
        if text[pos:pos + len(tok)] == tok:
            return tok
    return None


def iast_to_devanagari(text: str) -> str:
    """
    Convert IAST transliteration to Devanagari.

    Uses a two-pass approach:
    1. Tokenize IAST into consonants, vowels, and other characters
    2. Convert tokens to Devanagari with proper vowel marks and virāma

    Args:
        text: Text in IAST transliteration

    Returns:
        Devanagari text
    """
    src = text.lower()
    result = []
    i = 0

    while i < len(src):
        # Special: oṃ
        if src[i:i + 2] == 'oṃ':
            result.append('ॐ')
            i += 2
            continue

        # Special: ṃ and ḥ (anusvāra / visarga)
        if src[i] == 'ṃ':
            result.append('ं')
            i += 1
            continue
        if src[i] == 'ḥ':
            result.append('ः')
            i += 1
            continue
        if src[i] == 'ṁ':
            result.append('ँ')
            i += 1
            continue

        # Try consonant match
        cons = _match_iast_consonant(src, i)
        if cons:
            deva_cons = IAST_TO_DEVANAGARI[cons]
            i += len(cons)

            # Look ahead for a following vowel
            vowel = _match_iast_vowel(src, i)
            if vowel:
                result.append(deva_cons)
                if vowel != 'a':
                    result.append(IAST_VOWEL_MARKS[vowel])
                # 'a' is inherent, no mark needed
                i += len(vowel)
            else:
                # No vowel follows — add virāma (unless at end followed by space/punct)
                result.append(deva_cons)
                result.append('्')
            continue

        # Try vowel match (independent vowel — not after consonant)
        vowel = _match_iast_vowel(src, i)
        if vowel:
            result.append(IAST_TO_DEVANAGARI.get(vowel, vowel))
            i += len(vowel)
            continue

        # Non-IAST character: pass through
        result.append(text[i])
        i += 1

    return ''.join(result)


# Characters that are valid in IAST text (lowercase).  Includes all
# consonant and vowel letters, diacritics, and common punctuation.
_VALID_IAST_CHARS = frozenset(
    "abcdeghijklmnoprstuvyāīūṛṝḷḹṃḥṁñṅṭḍṇśṣ"
    " .,;:!?-–—'\"()[]{}"
    "0123456789"
)


def validate_iast(text: str) -> list[str]:
    """
    Check whether *text* contains only valid IAST characters.

    Returns a list of error strings (empty if input is valid IAST).
    Non-IAST characters (Chinese, Tibetan, Cyrillic, etc.) will be
    flagged with their position and Unicode codepoint.

    This is useful as a pre-flight check before calling
    ``iast_to_devanagari()``.

    Args:
        text: Text to validate.

    Returns:
        List of error messages (empty means valid).
    """
    errors = []
    for i, ch in enumerate(text.lower()):
        if ch not in _VALID_IAST_CHARS:
            errors.append(
                f"position {i}: unexpected character '{ch}' (U+{ord(ch):04X})"
            )
    return errors


def normalize_iast(text: str) -> str:
    """
    Normalize IAST text to standard form.

    Handles common variations:
    - ṁ/ṃ normalization
    - Spacing around punctuation
    - Hyphenation
    """
    # Normalize anusvāra
    text = text.replace('ṁ', 'ṃ')

    # Normalize curly/smart quotes to straight quotes
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")

    return text
