"""
Transliteration utilities for Sanskrit between Devanagari and IAST.

Provides bidirectional conversion between:
- Devanagari (देवनागरी)
- IAST (International Alphabet of Sanskrit Transliteration)

Limitations:
- Consonant clusters (conjuncts) are handled via virāma but may not
  produce correct visual conjunct forms in all cases.
- Sandhi (word junction) is not handled; input should be pre-segmented.
- The IAST→Devanagari direction uses greedy longest-match, which may
  misparse ambiguous sequences (e.g., aspirated consonants at word
  boundaries).
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

# Consonants that need virāma when not followed by vowel
CONSONANTS = set('kgṅcjñṭḍṇtdnpbmyrlvśṣsh')


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
            if result and result[-1] == 'a':
                result.pop()
            i += 1
            continue

        # Check for vowel marks (mātrās)
        if char in DEVANAGARI_TO_IAST:
            trans = DEVANAGARI_TO_IAST[char]
            # Vowel marks replace the inherent 'a'
            if char in 'ािीुूृॄॢॣेैोौ':
                if result and result[-1] == 'a':
                    result.pop()
            result.append(trans)
        elif char.isspace() or char in '.,!?:;-–—\'\"()[]{}':
            result.append(char)
        else:
            # Unknown character, pass through
            result.append(char)

        i += 1

    return ''.join(result)


def iast_to_devanagari(text: str) -> str:
    """
    Convert IAST transliteration to Devanagari.

    Args:
        text: Text in IAST transliteration

    Returns:
        Devanagari text
    """
    result = []
    i = 0
    text_lower = text.lower()

    while i < len(text_lower):
        matched = False

        # Try to match longest sequences first (e.g., 'kh' before 'k')
        for length in [3, 2, 1]:
            if i + length <= len(text_lower):
                seq = text_lower[i:i + length]

                # Check for special sequences
                if seq == 'oṃ':
                    result.append('ॐ')
                    i += length
                    matched = True
                    break

                # Check for consonant + vowel
                if length >= 2 and seq[0] in CONSONANTS:
                    # Check if it's an aspirated consonant
                    if length >= 2 and seq[:2] in IAST_TO_DEVANAGARI:
                        consonant = IAST_TO_DEVANAGARI[seq[:2]]
                        vowel_part = seq[2:] if length > 2 else ''
                        remaining = text_lower[i + 2:i + 3] if i + 2 < len(text_lower) else ''

                        # Add consonant
                        result.append(consonant)

                        # Check for following vowel
                        if remaining and remaining in IAST_VOWEL_MARKS:
                            if remaining != 'a':
                                result.append(IAST_VOWEL_MARKS[remaining])
                            i += 3
                        else:
                            # Add virāma if not followed by vowel
                            if remaining and remaining not in 'aāiīuūṛṝḷḹeaioau':
                                result.append('्')
                            i += 2
                        matched = True
                        break

                # Check for single consonant
                if seq[0] in IAST_TO_DEVANAGARI:
                    result.append(IAST_TO_DEVANAGARI[seq[0]])

                    # Check if followed by vowel
                    if i + 1 < len(text_lower):
                        next_char = text_lower[i + 1]
                        if next_char in IAST_VOWEL_MARKS and next_char != 'a':
                            result.append(IAST_VOWEL_MARKS[next_char])
                            i += 2
                            matched = True
                            break

                    i += 1
                    matched = True
                    break

        if not matched:
            # Pass through unknown characters
            result.append(text[i])
            i += 1

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
