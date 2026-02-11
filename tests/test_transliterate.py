"""Tests for Devanagari ↔ IAST transliteration."""

import pytest
from hrdaya.transliterate import (
    devanagari_to_iast,
    iast_to_devanagari,
    normalize_iast,
    validate_iast,
)


class TestDevanagariToIAST:
    """Test Devanagari to IAST conversion."""

    def test_om(self):
        assert devanagari_to_iast("ॐ") == "oṃ"

    @pytest.mark.parametrize("devanagari,expected", [
        ("शून्यता", "śūnyatā"),
        ("गते गते पारगते", "gate gate pāragate"),
        ("बोधि स्वाहा", "bodhi svāhā"),
        ("प्रज्ञापारमिता", "prajñāpāramitā"),
        ("निरोध", "nirodha"),
        ("क्षय", "kṣaya"),
        ("अविद्या", "avidyā"),
    ])
    def test_complex_words(self, devanagari, expected):
        assert devanagari_to_iast(devanagari) == expected

    def test_empty_string(self):
        assert devanagari_to_iast("") == ""

    def test_spaces_preserved(self):
        result = devanagari_to_iast("गते गते")
        assert " " in result

    def test_punctuation_preserved(self):
        result = devanagari_to_iast("गते।")
        # indic-transliteration renders danda as | (standard ASCII representation)
        assert result.endswith("|") or result.endswith(".")

    def test_independent_vowels(self):
        """Independent vowels at word start."""
        assert devanagari_to_iast("अ") == "a"
        assert devanagari_to_iast("आ") == "ā"
        assert devanagari_to_iast("इ") == "i"
        assert devanagari_to_iast("उ") == "u"
        assert devanagari_to_iast("ए") == "e"

    def test_anusvara_visarga(self):
        """Anusvāra and visarga."""
        assert devanagari_to_iast("ं") == "ṃ"
        assert devanagari_to_iast("ः") == "ḥ"

    def test_retroflexes(self):
        """Retroflex consonants."""
        assert devanagari_to_iast("ट") == "ṭa"
        assert devanagari_to_iast("ण") == "ṇa"
        assert devanagari_to_iast("ष") == "ṣa"


class TestIASTToDevanagari:
    """Test IAST to Devanagari conversion."""

    def test_empty_string(self):
        assert iast_to_devanagari("") == ""

    def test_om(self):
        assert iast_to_devanagari("oṃ") == "ॐ"

    def test_spaces_preserved(self):
        result = iast_to_devanagari("gate gate")
        assert " " in result

    @pytest.mark.parametrize("iast,expected", [
        ("gate gate pāragate", "गते गते पारगते"),
        ("bodhi", "बोधि"),
        ("svāhā", "स्वाहा"),
        ("prajñā", "प्रज्ञा"),
        ("śūnyatā", "शून्यता"),
        ("prajñāpāramitā", "प्रज्ञापारमिता"),
        ("nirodha", "निरोध"),
        ("kṣaya", "क्षय"),
        ("avidyā", "अविद्या"),
    ])
    def test_complex_words(self, iast, expected):
        assert iast_to_devanagari(iast) == expected

    def test_independent_vowel_start(self):
        """Independent vowels at start of word."""
        assert iast_to_devanagari("a") == "अ"
        assert iast_to_devanagari("ā") == "आ"
        assert iast_to_devanagari("i") == "इ"
        assert iast_to_devanagari("u") == "उ"

    def test_consonant_cluster_triple(self):
        """Triple consonant cluster."""
        result = iast_to_devanagari("stra")
        assert "स्त्र" in result

    def test_anusvara_after_vowel(self):
        """Anusvāra following a vowel."""
        result = iast_to_devanagari("saṃ")
        assert "सं" in result

    def test_visarga(self):
        """Visarga after vowel."""
        result = iast_to_devanagari("duḥkha")
        assert "दुःख" in result

    def test_roundtrip_gate(self):
        """Test Devanagari→IAST→Devanagari roundtrip."""
        original = "गते"
        iast = devanagari_to_iast(original)
        assert iast == "gate"
        back = iast_to_devanagari(iast)
        assert back == original

    @pytest.mark.parametrize("iast", [
        "prajñāpāramitāhṛdaya",
        "gate gate pāragate pārasaṃgate bodhi svāhā",
        "śūnyatā",
        "avalokiteśvara",
        "rūpa",
        "vedanā",
        "saṃjñā",
    ])
    def test_roundtrip_key_terms(self, iast):
        """Roundtrip IAST→Devanagari→IAST for key Heart Sutra terms."""
        deva = iast_to_devanagari(iast)
        back = devanagari_to_iast(deva)
        assert back == iast, f"{iast} → {deva} → {back}"


class TestValidateIAST:
    """Test IAST input validation."""

    def test_valid_iast_no_errors(self):
        assert validate_iast("prajñāpāramitāhṛdaya") == []

    def test_valid_iast_with_spaces(self):
        assert validate_iast("gate gate pāragate") == []

    def test_chinese_character_flagged(self):
        errors = validate_iast("般若")
        assert len(errors) == 2
        assert "U+" in errors[0]

    def test_tibetan_character_flagged(self):
        errors = validate_iast("ཤེས")
        assert len(errors) > 0

    def test_empty_string_valid(self):
        assert validate_iast("") == []

    def test_punctuation_accepted(self):
        assert validate_iast("gate, gate.") == []

    def test_danda_accepted(self):
        """Pipe/danda separator used in Sanskrit manuscripts is valid IAST."""
        assert validate_iast("namas sarvajñāya |") == []

    def test_all_consonants_valid(self):
        consonants = "k kh g gh ṅ c ch j jh ñ ṭ ṭh ḍ ḍh ṇ t th d dh n p ph b bh m y r l v ś ṣ s h"
        assert validate_iast(consonants) == []

    def test_all_vowels_valid(self):
        vowels = "a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au"
        assert validate_iast(vowels) == []


class TestNormalizeIAST:
    """Test IAST normalization."""

    def test_anusvara_normalization(self):
        assert "ṃ" in normalize_iast("oṁ")

    def test_curly_quotes_normalized(self):
        result = normalize_iast("the \u2018text\u2019")
        assert "\u2018" not in result
        assert "\u2019" not in result

    def test_plain_text_unchanged(self):
        text = "prajnaparamita"
        assert normalize_iast(text) == text

    def test_empty_string(self):
        assert normalize_iast("") == ""


class TestNewlineHandling:
    """Test that newlines in IAST text are handled (mn9)."""

    def test_newline_in_iast_accepted(self):
        """Multi-line IAST should not produce errors for newline chars."""
        errors = validate_iast("gate gate\npāragate")
        assert errors == []

    def test_tab_in_iast_accepted(self):
        errors = validate_iast("gate\tgate")
        assert errors == []

    def test_carriage_return_accepted(self):
        errors = validate_iast("gate\r\ngate")
        assert errors == []
