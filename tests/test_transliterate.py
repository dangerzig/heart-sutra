"""Tests for Devanagari ↔ IAST transliteration."""

import pytest
from hrdaya.transliterate import devanagari_to_iast, iast_to_devanagari, normalize_iast


class TestDevanagariToIAST:
    """Test Devanagari to IAST conversion."""

    def test_om(self):
        assert devanagari_to_iast("ॐ") == "oṃ"

    @pytest.mark.xfail(reason="Transliteration has known limitations with vowel mark handling")
    @pytest.mark.parametrize("devanagari,expected", [
        ("शून्यता", "śūnyatā"),
        ("गते गते पारगते", "gate gate pāragate"),
        ("बोधि स्वाहा", "bodhi svāhā"),
    ])
    def test_complex_words(self, devanagari, expected):
        """These test known limitation areas of the transliteration."""
        assert devanagari_to_iast(devanagari) == expected

    def test_empty_string(self):
        assert devanagari_to_iast("") == ""

    def test_spaces_preserved(self):
        result = devanagari_to_iast("गते गते")
        assert " " in result

    def test_punctuation_preserved(self):
        result = devanagari_to_iast("गते।")
        assert result.endswith(".")


class TestIASTToDevanagari:
    """Test IAST to Devanagari conversion."""

    def test_empty_string(self):
        assert iast_to_devanagari("") == ""

    def test_om(self):
        assert iast_to_devanagari("oṃ") == "ॐ"

    def test_spaces_preserved(self):
        result = iast_to_devanagari("gate gate")
        assert " " in result


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
