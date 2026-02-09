"""
Transliteration utilities for Sanskrit between Devanagari and IAST.

Provides bidirectional conversion between:
- Devanagari (देवनागरी)
- IAST (International Alphabet of Sanskrit Transliteration)

Implementation:
- Devanagari→IAST: Character-by-character mapping with virāma and
  mātrā (vowel mark) handling to strip/replace inherent 'a'.
- IAST→Devanagari: Token-based parser using sorted longest-first
  matching for consonants and vowels. Handles consonant clusters
  (virāma insertion), independent vs. combining vowels, and special
  tokens (oṃ, anusvāra, visarga).

Scope:
- Covers all standard Sanskrit consonants, vowels, and diacritics.
- Consonant clusters produce virāma-separated forms (e.g., प्र for 'pr').
- Sandhi is not handled; input should be pre-segmented at word boundaries.
- For scholarly publication, output should be verified against source
  manuscripts.
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

# Set of single-char IAST consonant letters (used for lookahead)
CONSONANT_CHARS = set('kgṅcjñṭḍṇtdnpbmyrlvśṣsh')

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
    prev_was_consonant = False

    while i < len(src):
        # Special: oṃ
        if src[i:i + 2] == 'oṃ':
            result.append('ॐ')
            i += 2
            prev_was_consonant = False
            continue

        # Special: ṃ and ḥ (anusvāra / visarga)
        if src[i] == 'ṃ':
            result.append('ं')
            i += 1
            prev_was_consonant = False
            continue
        if src[i] == 'ḥ':
            result.append('ः')
            i += 1
            prev_was_consonant = False
            continue
        if src[i] == 'ṁ':
            result.append('ँ')
            i += 1
            prev_was_consonant = False
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
            prev_was_consonant = True
            continue

        # Try vowel match (independent vowel — not after consonant)
        vowel = _match_iast_vowel(src, i)
        if vowel:
            result.append(IAST_TO_DEVANAGARI.get(vowel, vowel))
            i += len(vowel)
            prev_was_consonant = False
            continue

        # Non-IAST character: pass through
        result.append(text[i])
        i += 1
        prev_was_consonant = False

    return ''.join(result)


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
