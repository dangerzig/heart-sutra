"""Tests for the LaTeX critical edition generator."""

import json
import re
from pathlib import Path

import pytest

from hrdaya.latex_gen import (
    ApparatusAssembler,
    ApparatusEntry,
    ChineseCriticalGen,
    CombinedCriticalGen,
    DataLoader,
    FigureSnippetGen,
    LatexEditionBuilder,
    ParallelGen,
    SanskritCriticalGen,
    TibetanCriticalGen,
    _escape_latex,
    _provenance_header,
    _roman,
    _split_chinese_clauses,
    generate_editions,
)

DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture(scope="module")
def loader():
    return DataLoader(DATA_DIR)


@pytest.fixture(scope="module")
def assembler(loader):
    return ApparatusAssembler(loader)


@pytest.fixture(scope="module")
def generated_editions(tmp_path_factory):
    """Generate all editions once for the test module."""
    out = tmp_path_factory.mktemp("latex_gen")
    results = generate_editions(DATA_DIR, out)
    return results


# ============================================================================
# Utility tests
# ============================================================================

class TestEscapeLatex:
    def test_ampersand(self):
        assert _escape_latex("a & b") == r"a \& b"

    def test_percent(self):
        assert _escape_latex("100%") == r"100\%"

    def test_underscore(self):
        assert _escape_latex("foo_bar") == r"foo\_bar"

    def test_cjk_passthrough(self):
        text = "般若波羅蜜多"
        assert _escape_latex(text) == text

    def test_iast_diacritics_preserved(self):
        text = "prajñāpāramitā"
        assert _escape_latex(text) == text


class TestSplitChineseClauses:
    def test_basic_split(self):
        text = "觀自在菩薩，行深般若波羅蜜多時，照見五蘊皆空，度一切苦厄。"
        clauses = _split_chinese_clauses(text)
        assert len(clauses) == 4
        assert clauses[0] == "觀自在菩薩，"
        assert clauses[-1] == "度一切苦厄。"

    def test_no_punctuation(self):
        text = "菩提薩婆訶"
        clauses = _split_chinese_clauses(text)
        assert len(clauses) == 1
        assert clauses[0] == text


# ============================================================================
# DataLoader tests
# ============================================================================

class TestDataLoader:
    def test_load_variant_table(self, loader):
        vt = loader.load_variant_table()
        assert "sections" in vt
        assert "opening" in vt["sections"]

    def test_load_t251(self, loader):
        data = loader.load_witness("T251")
        assert data
        assert "segments" in data

    def test_load_gretil(self, loader):
        data = loader.load_witness("GRETIL")
        assert data
        assert "segments" in data

    def test_load_toh21(self, loader):
        data = loader.load_witness("Toh21")
        assert data
        assert "segments" in data

    def test_get_segment(self, loader):
        seg = loader.get_segment("T251", "T251:1")
        assert seg
        assert "text" in seg

    def test_get_segment_by_parallel(self, loader):
        seg = loader.get_segment_by_parallel("GRETIL", "T251:1")
        assert seg
        assert "iast" in seg

    def test_missing_witness_returns_empty(self, loader):
        data = loader.load_witness("NONEXISTENT")
        assert data == {}


# ============================================================================
# ApparatusAssembler tests
# ============================================================================

class TestApparatusAssembler:
    def test_chinese_apparatus_nonempty(self, assembler):
        entries = assembler.assemble_chinese("opening")
        # Opening section should have Chinese variants (T250, T257)
        assert len(entries) > 0

    def test_chinese_apparatus_has_witnesses(self, assembler):
        entries = assembler.assemble_chinese("opening")
        for entry in entries:
            for _, witnesses in entry.readings:
                assert len(witnesses) > 0

    def test_cross_linguistic_sanskrit(self, assembler):
        entries = assembler.assemble_cross_linguistic("opening", "sanskrit")
        assert len(entries) > 0

    def test_cross_linguistic_tibetan(self, assembler):
        entries = assembler.assemble_cross_linguistic("opening", "tibetan")
        assert len(entries) > 0


# ============================================================================
# Edition generation tests
# ============================================================================

class TestAllEditionsGenerate:
    def test_all_editions_generated(self, generated_editions):
        edition_names = {"chinese", "sanskrit", "tibetan", "parallel", "combined"}
        for name in edition_names:
            assert name in generated_editions, f"{name} not generated"
            assert generated_editions[name].exists()

    def test_edition_files_nonempty(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue  # Figures tested separately
            content = path.read_text(encoding="utf-8")
            assert len(content) > 1000, f"{name} too small: {len(content)} bytes"

    def test_figure_snippets_generated(self, generated_editions):
        figure_keys = [k for k in generated_editions if k.startswith("figure:")]
        assert len(figure_keys) == 3, f"Expected 3 figures, got {len(figure_keys)}"
        for key in figure_keys:
            assert generated_editions[key].exists()


class TestBracesBalanced:
    def test_all_editions_balanced(self, generated_editions):
        for name, path in generated_editions.items():
            content = path.read_text(encoding="utf-8")
            opens = content.count("{")
            closes = content.count("}")
            assert opens == closes, (
                f"{name}: unbalanced braces ({opens} opens, {closes} closes)"
            )


class TestChineseEdition:
    def test_has_12_sections(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        sections = re.findall(r"\\subsection\*\{Section", content)
        assert len(sections) == 12

    def test_has_pinyin(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert r"\pinyin{" in content

    def test_has_witness_descriptions(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert r"\wit{T251}" in content
        assert r"\wit{T250}" in content

    def test_has_apparatus_footnotes(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert r"\footnote{" in content
        assert r"\lemma{" in content


class TestSanskritEdition:
    def test_has_devanagari(self, generated_editions):
        content = generated_editions["sanskrit"].read_text(encoding="utf-8")
        assert r"\deva{" in content

    def test_has_iast(self, generated_editions):
        content = generated_editions["sanskrit"].read_text(encoding="utf-8")
        assert "prajñāpāramitā" in content.lower() or "Prajñāpāramitā" in content


class TestTibetanEdition:
    def test_has_tibetan_script(self, generated_editions):
        content = generated_editions["tibetan"].read_text(encoding="utf-8")
        assert r"\tib{" in content

    def test_has_wylie(self, generated_editions):
        content = generated_editions["tibetan"].read_text(encoding="utf-8")
        assert r"\wylie{" in content


class TestParallelEdition:
    def test_landscape(self, generated_editions):
        content = generated_editions["parallel"].read_text(encoding="utf-8")
        assert "landscape" in content

    def test_has_longtable(self, generated_editions):
        content = generated_editions["parallel"].read_text(encoding="utf-8")
        assert r"\begin{longtable}" in content

    def test_has_three_columns(self, generated_editions):
        content = generated_editions["parallel"].read_text(encoding="utf-8")
        assert "Chinese (T251)" in content
        assert "Sanskrit" in content
        assert "Tibetan" in content


class TestCombinedEdition:
    def test_has_apparatus_section(self, generated_editions):
        content = generated_editions["combined"].read_text(encoding="utf-8")
        assert "Critical Apparatus" in content

    def test_has_all_scripts(self, generated_editions):
        content = generated_editions["combined"].read_text(encoding="utf-8")
        assert r"\deva{" in content
        assert r"\tib{" in content


class TestEmptyNotes:
    """Verify that variants with empty notes don't produce broken footnotes."""

    def test_no_empty_footnote_notes(self, generated_editions):
        for name, path in generated_editions.items():
            content = path.read_text(encoding="utf-8")
            # Should not have "} }" at end of footnote (empty note)
            # But should not have broken LaTeX either
            assert r"\footnote{}" not in content


class TestProvenance:
    def test_all_have_provenance(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue  # Figure snippets have no preamble
            content = path.read_text(encoding="utf-8")
            assert "AUTO-GENERATED by hrdaya.latex_gen" in content
            assert "Data version: " in content

    def test_provenance_has_hash(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue
            content = path.read_text(encoding="utf-8")
            assert re.search(r"Hash: [0-9a-f]{12}", content), (
                f"{name}: missing data hash in provenance"
            )

    def test_provenance_has_timestamp(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue
            content = path.read_text(encoding="utf-8")
            assert re.search(r"Generated: \d{4}-\d{2}-\d{2}T", content), (
                f"{name}: missing timestamp in provenance"
            )

    def test_provenance_has_regenerate_command(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue
            content = path.read_text(encoding="utf-8")
            assert "Regenerate with: make latex-gen" in content


# ============================================================================
# Extended utility tests
# ============================================================================

class TestEscapeLatexExtended:
    """Edge cases for LaTeX escaping."""

    def test_empty_string(self):
        assert _escape_latex("") == ""

    def test_backslash(self):
        assert _escape_latex("a\\b") == r"a\textbackslash{}b"

    def test_hash(self):
        assert _escape_latex("#1") == r"\#1"

    def test_dollar(self):
        assert _escape_latex("$x$") == r"\$x\$"

    def test_tilde(self):
        assert _escape_latex("~") == r"\textasciitilde{}"

    def test_caret(self):
        assert _escape_latex("^") == r"\textasciicircum{}"

    def test_curly_braces(self):
        assert _escape_latex("{x}") == r"\{x\}"

    def test_multiple_specials(self):
        result = _escape_latex("a & b % c # d")
        assert r"\&" in result
        assert r"\%" in result
        assert r"\#" in result

    def test_tibetan_passthrough(self):
        text = "བཅོམ་ལྡན་འདས"
        assert _escape_latex(text) == text

    def test_devanagari_passthrough(self):
        text = "प्रज्ञापारमिता"
        assert _escape_latex(text) == text


class TestSplitChineseClausesExtended:
    """Edge cases for clause splitting."""

    def test_empty_string(self):
        assert _split_chinese_clauses("") == []

    def test_semicolon_split(self):
        clauses = _split_chinese_clauses("甲；乙")
        assert len(clauses) == 2
        assert clauses[0] == "甲；"
        assert clauses[1] == "乙"

    def test_colon_split(self):
        clauses = _split_chinese_clauses("甲：乙")
        assert len(clauses) == 2
        assert clauses[0] == "甲："
        assert clauses[1] == "乙"

    def test_multiple_sentence_ends(self):
        clauses = _split_chinese_clauses("甲。乙。")
        assert len(clauses) == 2
        assert clauses[0] == "甲。"
        assert clauses[1] == "乙。"

    def test_only_punctuation(self):
        """Whitespace-only clauses are filtered out."""
        clauses = _split_chinese_clauses("。")
        assert len(clauses) == 1


class TestRoman:
    """Tests for Roman numeral conversion."""

    def test_one(self):
        assert _roman(1) == "I"

    def test_four(self):
        assert _roman(4) == "IV"

    def test_nine(self):
        assert _roman(9) == "IX"

    def test_twelve(self):
        """12 sections in the Heart Sutra."""
        assert _roman(12) == "XII"

    def test_subtractive_notation(self):
        assert _roman(40) == "XL"
        assert _roman(90) == "XC"
        assert _roman(400) == "CD"
        assert _roman(900) == "CM"

    def test_zero_returns_empty(self):
        assert _roman(0) == ""


class TestProvenanceHeader:
    """Tests for provenance header generation."""

    def test_format_structure(self):
        header = _provenance_header("abc123def456")
        lines = header.strip().split("\n")
        assert len(lines) == 4
        assert lines[0].startswith("%%")
        assert "AUTO-GENERATED" in lines[0]

    def test_includes_hash(self):
        header = _provenance_header("abc123def456")
        assert "Hash: abc123def456" in header

    def test_includes_version(self):
        from hrdaya.data import DATA_VERSION
        header = _provenance_header("x" * 12)
        assert f"Data version: {DATA_VERSION}" in header

    def test_includes_iso_timestamp(self):
        header = _provenance_header("x" * 12)
        assert re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", header)


# ============================================================================
# Extended DataLoader tests
# ============================================================================

class TestDataLoaderExtended:
    """Extended DataLoader tests for edge cases and caching."""

    def test_variant_table_cached(self, loader):
        """Second call returns same object (caching)."""
        vt1 = loader.load_variant_table()
        vt2 = loader.load_variant_table()
        assert vt1 is vt2

    def test_witness_cached(self, loader):
        """Second call for same witness returns cached data."""
        d1 = loader.load_witness("T251")
        d2 = loader.load_witness("T251")
        assert d1 is d2

    def test_load_t250_lowercase_filename(self, loader):
        """T250.json has lowercase filename (t250.json)."""
        data = loader.load_witness("T250")
        assert data
        assert "segments" in data

    def test_load_fangshan(self, loader):
        data = loader.load_witness("Fangshan")
        assert data
        assert "segments" in data

    def test_get_segment_missing_segment_id(self, loader):
        """Missing segment ID returns empty dict."""
        seg = loader.get_segment("T251", "T251:999")
        assert seg == {}

    def test_get_segment_by_parallel_missing(self, loader):
        """Missing parallel reference returns empty dict."""
        seg = loader.get_segment_by_parallel("GRETIL", "NONEXISTENT:999")
        assert seg == {}

    def test_variant_table_missing_raises(self, tmp_path):
        """Missing variant table raises FileNotFoundError."""
        bad_loader = DataLoader(tmp_path)
        with pytest.raises(FileNotFoundError, match="variant_table"):
            bad_loader.load_variant_table()

    def test_variant_table_all_12_sections(self, loader):
        """Variant table has all 12 Heart Sutra sections."""
        vt = loader.load_variant_table()
        from hrdaya.latex_gen import SECTION_KEYS
        for key in SECTION_KEYS:
            assert key in vt["sections"], f"Missing section: {key}"

    def test_gretil_has_iast_fields(self, loader):
        """GRETIL segments have iast and devanagari fields."""
        seg = loader.get_segment_by_parallel("GRETIL", "T251:1")
        assert "iast" in seg
        assert "devanagari" in seg

    def test_toh21_has_tibetan_fields(self, loader):
        """Toh21 segments have tibetan and wylie fields."""
        seg = loader.get_segment_by_parallel("Toh21", "T251:1")
        assert "tibetan" in seg
        assert "wylie" in seg

    def test_t251_has_enrichment_fields(self, loader):
        """T251 segments have pinyin and english_gloss."""
        seg = loader.get_segment("T251", "T251:1")
        assert "pinyin" in seg
        assert "english_gloss" in seg


# ============================================================================
# Extended ApparatusAssembler tests
# ============================================================================

class TestApparatusAssemblerExtended:
    """Extended tests for apparatus assembly logic."""

    def test_chinese_entries_have_lemmas(self, assembler):
        entries = assembler.assemble_chinese("opening")
        for entry in entries:
            assert entry.lemma, "Apparatus entry should have a non-empty lemma"

    def test_chinese_entries_have_readings(self, assembler):
        entries = assembler.assemble_chinese("opening")
        for entry in entries:
            assert len(entry.readings) > 0

    def test_chinese_variant_reading_text(self, assembler):
        """Variant readings should contain actual text, not empty strings."""
        entries = assembler.assemble_chinese("opening")
        for entry in entries:
            for reading_text, _ in entry.readings:
                assert reading_text, "Variant reading text should not be empty"

    def test_cross_linguistic_empty_section(self, assembler):
        """Sections with no cross-linguistic variants return empty list."""
        # Some sections may have no Sanskrit cross-linguistic variants
        for section_key in ["negations_dhatus", "negations_truths"]:
            entries = assembler.assemble_cross_linguistic(section_key, "sanskrit")
            # Either empty or has valid entries (no crash)
            for entry in entries:
                assert entry.lemma

    def test_cross_linguistic_lemma_truncated(self, assembler):
        """Cross-linguistic entries use truncated base text as lemma."""
        entries = assembler.assemble_cross_linguistic("opening", "sanskrit")
        if entries:
            assert "…" in entries[0].lemma

    def test_mantra_section_has_variants(self, assembler):
        """Mantra section should have Chinese variants (well-known differences)."""
        entries = assembler.assemble_chinese("mantra")
        # Mantra has 揭諦/揭帝, 薩婆訶/僧莎訶 variants
        assert len(entries) > 0

    def test_extract_lemma_position_zero(self, assembler):
        """Lemma extraction at position 0."""
        lemma = assembler._extract_lemma(
            "觀自在菩薩", {"position": 0, "variant_reading": "觀世音"}
        )
        assert lemma.startswith("觀")

    def test_extract_lemma_negative_position(self, assembler):
        """Negative position (cross-linguistic) returns truncated base text."""
        lemma = assembler._extract_lemma(
            "觀自在菩薩行深般若波羅蜜多時", {"position": -1, "variant_reading": "x"}
        )
        assert "…" in lemma
        assert len(lemma) <= 11  # 10 chars + ellipsis

    def test_extract_lemma_beyond_text(self, assembler):
        """Position beyond text length returns truncated base text."""
        lemma = assembler._extract_lemma(
            "短", {"position": 100, "variant_reading": "x"}
        )
        assert lemma == "短"

    def test_extract_lemma_punct_trimming(self, assembler):
        """Lemma is trimmed at punctuation boundary."""
        lemma = assembler._extract_lemma(
            "甲乙，丙丁", {"position": 0, "variant_reading": "甲乙丙"}
        )
        assert "，" not in lemma


# ============================================================================
# Extended edition content tests
# ============================================================================

class TestChineseEditionExtended:
    def test_has_line_numbers(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert r"\linenum{1}" in content

    def test_has_gloss(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert r"\gloss{" in content

    def test_has_fluent_translation(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert r"\fluent{" in content

    def test_title_page_content(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert "般若波羅蜜多心經" in content
        assert "Chinese Critical Edition" in content
        assert "T251" in content

    def test_roman_numeral_sections(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert "Section I:" in content
        assert "Section XII:" in content

    def test_witness_list_includes_fangshan(self, generated_editions):
        content = generated_editions["chinese"].read_text(encoding="utf-8")
        assert r"\wit{Fangshan}" in content


class TestSanskritEditionExtended:
    def test_has_editorial_note(self, generated_editions):
        content = generated_editions["sanskrit"].read_text(encoding="utf-8")
        assert "back-translation from Chinese" in content

    def test_has_line_numbers(self, generated_editions):
        content = generated_editions["sanskrit"].read_text(encoding="utf-8")
        assert r"\linenum{1}" in content

    def test_title_page_content(self, generated_editions):
        content = generated_editions["sanskrit"].read_text(encoding="utf-8")
        assert "Sanskrit Critical Edition" in content
        assert r"\deva{" in content  # Devanagari in title


class TestTibetanEditionExtended:
    def test_has_transmission_note(self, generated_editions):
        content = generated_editions["tibetan"].read_text(encoding="utf-8")
        assert "Vimalamitra" in content

    def test_has_line_numbers(self, generated_editions):
        content = generated_editions["tibetan"].read_text(encoding="utf-8")
        assert r"\linenum{1}" in content

    def test_title_page_content(self, generated_editions):
        content = generated_editions["tibetan"].read_text(encoding="utf-8")
        assert "Tibetan Critical Edition" in content
        assert r"\tib{" in content  # Tibetan in title


class TestParallelEditionExtended:
    def test_has_segment_numbers(self, generated_editions):
        content = generated_editions["parallel"].read_text(encoding="utf-8")
        assert r"\segnum{1}" in content
        assert r"\segnum{12}" in content

    def test_has_romanization(self, generated_editions):
        content = generated_editions["parallel"].read_text(encoding="utf-8")
        assert r"\rom{" in content

    def test_has_english_translation(self, generated_editions):
        content = generated_editions["parallel"].read_text(encoding="utf-8")
        assert r"\eng{" in content

    def test_title_page(self, generated_editions):
        content = generated_editions["parallel"].read_text(encoding="utf-8")
        assert "Parallel Synoptic Edition" in content


class TestCombinedEditionExtended:
    def test_has_segment_numbers(self, generated_editions):
        content = generated_editions["combined"].read_text(encoding="utf-8")
        assert r"\segnum{1}" in content

    def test_has_variant_markers(self, generated_editions):
        """Combined edition should have numbered variant markers."""
        content = generated_editions["combined"].read_text(encoding="utf-8")
        assert r"\var{" in content or "Critical Apparatus" in content

    def test_has_multicols_apparatus(self, generated_editions):
        content = generated_editions["combined"].read_text(encoding="utf-8")
        assert r"\begin{multicols}" in content

    def test_title_has_all_three_titles(self, generated_editions):
        content = generated_editions["combined"].read_text(encoding="utf-8")
        assert "般若波羅蜜多心經" in content
        assert r"\deva{" in content


# ============================================================================
# Generation entry point tests
# ============================================================================

class TestGenerateEditionsSingle:
    """Test generating a single edition."""

    def test_single_chinese(self, tmp_path):
        results = generate_editions(DATA_DIR, tmp_path, edition="chinese")
        assert len(results) == 1
        assert "chinese" in results
        assert results["chinese"].exists()

    def test_single_sanskrit(self, tmp_path):
        results = generate_editions(DATA_DIR, tmp_path, edition="sanskrit")
        assert len(results) == 1
        assert results["sanskrit"].exists()

    def test_single_tibetan(self, tmp_path):
        results = generate_editions(DATA_DIR, tmp_path, edition="tibetan")
        assert len(results) == 1
        assert results["tibetan"].exists()


class TestLatexEditionBuilder:
    """Tests for the orchestrator class."""

    def test_invalid_edition_raises(self, tmp_path):
        builder = LatexEditionBuilder(DATA_DIR, tmp_path)
        with pytest.raises(ValueError, match="Unknown edition"):
            builder.generate_one("nonexistent")

    def test_output_dir_created(self, tmp_path):
        out = tmp_path / "new_subdir" / "latex"
        builder = LatexEditionBuilder(DATA_DIR, out)
        builder.generate_one("chinese")
        assert out.exists()


# ============================================================================
# LaTeX structural integrity tests
# ============================================================================

class TestDocumentStructure:
    """Verify LaTeX document structure is valid for full editions."""

    def test_all_have_begin_document(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue  # Figure snippets are fragments
            content = path.read_text(encoding="utf-8")
            assert r"\begin{document}" in content, f"{name}: missing \\begin{{document}}"

    def test_all_have_end_document(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue
            content = path.read_text(encoding="utf-8")
            assert r"\end{document}" in content, f"{name}: missing \\end{{document}}"

    def test_begin_before_end(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue
            content = path.read_text(encoding="utf-8")
            begin_pos = content.index(r"\begin{document}")
            end_pos = content.index(r"\end{document}")
            assert begin_pos < end_pos, f"{name}: \\end before \\begin"

    def test_documentclass_present(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue
            content = path.read_text(encoding="utf-8")
            assert r"\documentclass" in content, f"{name}: missing \\documentclass"

    def test_fontspec_loaded(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue
            content = path.read_text(encoding="utf-8")
            assert r"\usepackage{fontspec}" in content, f"{name}: missing fontspec"

    def test_xecjk_loaded(self, generated_editions):
        for name, path in generated_editions.items():
            if name.startswith("figure:"):
                continue
            content = path.read_text(encoding="utf-8")
            assert r"\usepackage{xeCJK}" in content, f"{name}: missing xeCJK"


class TestChineseFormatFootnote:
    """Test the Chinese edition footnote formatting."""

    def test_format_footnote_basic(self, loader, assembler):
        gen = ChineseCriticalGen(loader, assembler)
        entry = ApparatusEntry(
            lemma="觀自在",
            readings=[("觀世音", ["T250"])],
            note="Different transliteration of Avalokiteśvara",
        )
        result = gen._format_footnote(entry)
        assert r"\footnote{" in result
        assert r"\lemma{觀自在}" in result
        assert r"\reading{觀世音}" in result
        assert r"\wit{T250}" in result
        assert "Different transliteration" in result

    def test_format_footnote_long_reading_truncated(self, loader, assembler):
        gen = ChineseCriticalGen(loader, assembler)
        long_reading = "x" * 50
        entry = ApparatusEntry(
            lemma="test",
            readings=[(long_reading, ["T250"])],
            note="",
        )
        result = gen._format_footnote(entry)
        assert "…" in result  # Truncated

    def test_format_footnote_no_note(self, loader, assembler):
        """Footnote without a note should not have trailing empty space."""
        gen = ChineseCriticalGen(loader, assembler)
        entry = ApparatusEntry(
            lemma="甲",
            readings=[("乙", ["T250"])],
            note="",
        )
        result = gen._format_footnote(entry)
        assert result.endswith("}")
        assert r"\footnote{}" not in result  # Not empty

    def test_format_footnote_multiple_witnesses(self, loader, assembler):
        gen = ChineseCriticalGen(loader, assembler)
        entry = ApparatusEntry(
            lemma="揭諦",
            readings=[("揭帝", ["T250", "Fangshan"])],
            note="",
        )
        result = gen._format_footnote(entry)
        assert r"\wit{T250}" in result
        assert r"\wit{Fangshan}" in result


# ============================================================================
# Figure snippet tests
# ============================================================================

class TestFigureSnippets:
    @pytest.fixture(scope="class")
    def snippets(self, loader, assembler):
        gen = FigureSnippetGen(loader, assembler)
        return gen.generate_all()

    def test_all_three_generated(self, snippets):
        assert len(snippets) == 3
        assert "figure_chinese_mantra.tex" in snippets
        assert "figure_sanskrit_mantra.tex" in snippets
        assert "figure_tibetan_pratityasamutpada.tex" in snippets

    def test_snippets_nonempty(self, snippets):
        for name, content in snippets.items():
            assert len(content) > 100, f"{name} too small"

    def test_braces_balanced(self, snippets):
        for name, content in snippets.items():
            opens = content.count("{")
            closes = content.count("}")
            assert opens == closes, (
                f"{name}: unbalanced braces ({opens} opens, {closes} closes)"
            )

    def test_chinese_has_apparatus_marker(self, snippets):
        content = snippets["figure_chinese_mantra.tex"]
        assert r"\textsuperscript{\textbf{a}}" in content

    def test_chinese_has_witnesses(self, snippets):
        content = snippets["figure_chinese_mantra.tex"]
        assert r"\wit{Fangshan}" in content
        assert r"\wit{T250}" in content
        assert r"\wit{T257}" in content

    def test_chinese_has_base_text(self, snippets):
        content = snippets["figure_chinese_mantra.tex"]
        assert "揭帝揭帝" in content

    def test_sanskrit_has_devanagari(self, snippets):
        content = snippets["figure_sanskrit_mantra.tex"]
        assert "ॐ" in content
        assert r"\deva{" in content

    def test_sanskrit_has_iast(self, snippets):
        content = snippets["figure_sanskrit_mantra.tex"]
        assert "Oṃ" in content
        assert "pāragate" in content

    def test_sanskrit_has_apparatus_note(self, snippets):
        content = snippets["figure_sanskrit_mantra.tex"]
        assert "Hōryūji" in content or "absent" in content.lower()

    def test_tibetan_has_tibetan_script(self, snippets):
        content = snippets["figure_tibetan_pratityasamutpada.tex"]
        assert "མ་རིག་པ" in content
        assert r"\tib{" in content

    def test_tibetan_has_wylie(self, snippets):
        content = snippets["figure_tibetan_pratityasamutpada.tex"]
        assert "ma rig pa" in content

    def test_tibetan_has_ksaya_note(self, snippets):
        content = snippets["figure_tibetan_pratityasamutpada.tex"]
        assert "zad pa" in content
        assert "kṣaya" in content or "ksaya" in content.lower()

    def test_all_have_fbox_parbox(self, snippets):
        for name, content in snippets.items():
            assert r"\fbox{\parbox{" in content, f"{name} missing fbox/parbox"

    def test_all_have_rule(self, snippets):
        for name, content in snippets.items():
            assert r"\rule{" in content, f"{name} missing horizontal rule"
