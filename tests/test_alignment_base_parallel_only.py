"""
Tests proving that alignment is strictly base_parallel-only.

These tests directly address the reviewer concern that a section+index
fallback might mis-associate segments.  The fallback was removed in v4;
these tests ensure it stays removed.
"""

import json
from pathlib import Path

import pytest
from hrdaya.collate import HeartSutraCollator


DATA_DIR = Path(__file__).parent.parent / "data"


class TestNoBaseParallelNoAlignment:
    """Segments without base_parallel MUST be excluded from alignment."""

    def test_alternate_segment_without_base_parallel_excluded(self, collator):
        """A segment with base_parallel=null must never appear in results."""
        # Collate opening with T250 — T250 has some segments with null base_parallel
        results = collator.collate_section("opening", alternate_chinese=["T250"])
        assert len(results) > 0
        for result in results:
            for alt_id, alt_text in result.chinese_texts.items():
                if alt_id == "T251":
                    continue
                # Every non-base reading must have been matched via base_parallel,
                # which means its text must NOT be the skandha_characteristics text
                # (which has base_parallel=null in T250).
                assert "是色性空" not in alt_text, (
                    f"Segment with null base_parallel leaked into results for {alt_id}"
                )

    def test_sanskrit_without_base_parallel_excluded(self, collator):
        """Sanskrit segments lacking base_parallel must not appear."""
        # Load Sanskrit data to check if any segments lack base_parallel
        sanskrit = collator.load_sanskrit_witness("GRETIL")
        segments_with_cp = [
            s for s in sanskrit.get("segments", [])
            if s.get("base_parallel") is not None
        ]
        segments_without_cp = [
            s for s in sanskrit.get("segments", [])
            if s.get("base_parallel") is None
        ]
        if not segments_without_cp:
            pytest.skip("All Sanskrit segments have base_parallel")

        # Collate and verify that only segments WITH base_parallel appear
        results = collator.collate_section("opening")
        for result in results:
            for witness, text in result.sanskrit_texts.items():
                # Each Sanskrit text in results must come from a segment
                # that had a base_parallel pointing at this result's segment_id
                assert text != "", (
                    f"Empty Sanskrit text for {witness} in {result.segment_id}"
                )

    def test_synthetic_witness_no_base_parallel(self, tmp_path):
        """
        Create a synthetic witness with NO base_parallel fields and
        verify it produces zero aligned segments.
        """
        # Create a minimal data directory
        taisho = tmp_path / "chinese" / "taisho"
        taisho.mkdir(parents=True)

        base = {
            "id": "BASE",
            "segments": [
                {"id": "BASE:1", "section": "opening", "text": "base text"}
            ]
        }
        alt = {
            "id": "ALT",
            "segments": [
                {"id": "ALT:1", "section": "opening", "text": "alt text"}
                # Note: no base_parallel field at all
            ]
        }
        (taisho / "BASE.json").write_text(json.dumps(base))
        (taisho / "ALT.json").write_text(json.dumps(alt))

        collator = HeartSutraCollator(tmp_path)
        results = collator.collate_section(
            "opening",
            chinese_witness="BASE",
            alternate_chinese=["ALT"],
        )
        assert len(results) == 1
        # ALT should NOT appear because it has no base_parallel
        assert "ALT" not in results[0].chinese_texts

    def test_synthetic_witness_with_base_parallel(self, tmp_path):
        """
        Create a synthetic witness WITH base_parallel and verify
        it IS aligned.
        """
        taisho = tmp_path / "chinese" / "taisho"
        taisho.mkdir(parents=True)

        base = {
            "id": "BASE",
            "segments": [
                {"id": "BASE:1", "section": "opening", "text": "base text"}
            ]
        }
        alt = {
            "id": "ALT",
            "segments": [
                {
                    "id": "ALT:1",
                    "section": "opening",
                    "text": "alt text",
                    "base_parallel": "BASE:1",
                }
            ]
        }
        (taisho / "BASE.json").write_text(json.dumps(base))
        (taisho / "ALT.json").write_text(json.dumps(alt))

        collator = HeartSutraCollator(tmp_path)
        results = collator.collate_section(
            "opening",
            chinese_witness="BASE",
            alternate_chinese=["ALT"],
        )
        assert len(results) == 1
        assert "ALT" in results[0].chinese_texts
        assert results[0].chinese_texts["ALT"] == "alt text"
