"""
Data validation for Heart Sūtra witness files.

Validates that JSON data files conform to expected schemas
for Chinese, Sanskrit, and Tibetan witnesses.  Includes
cross-file consistency checks for base_parallel references.
"""

import json
import re
from pathlib import Path


# Required fields per witness type
CHINESE_SEGMENT_FIELDS = {"id", "section", "text"}
SANSKRIT_SEGMENT_FIELDS = {"id", "section", "iast"}
TIBETAN_SEGMENT_FIELDS = {"id", "section", "tibetan"}

_REQUIRED_BY_TYPE = {
    "chinese": CHINESE_SEGMENT_FIELDS,
    "sanskrit": SANSKRIT_SEGMENT_FIELDS,
    "tibetan": TIBETAN_SEGMENT_FIELDS,
}

# Keys that signal a valid alternate (non-segment) witness structure.
# Files with at least 2 of these keys are accepted without "segments".
_ALTERNATE_KEYS = {"id", "title_chinese", "title_english", "editions",
                   "title", "source", "description"}

# Witness directory layout — single source of truth for validate_data_dir
# and validate_cross_references.
_WITNESS_DIRS: list[tuple[str, str]] = [
    ("chinese/taisho", "chinese"),
    ("chinese/dunhuang", "chinese"),
    ("chinese/epigraphy", "chinese"),
    ("chinese/manuscripts", "chinese"),
    ("sanskrit/gretil", "sanskrit"),
    ("sanskrit/manuscripts", "sanskrit"),
    ("tibetan/kangyur", "tibetan"),
    ("tibetan/dunhuang", "tibetan"),
]

# Known section names used in the Heart Sūtra data files.
# Segments with section values not in this set will be flagged.
KNOWN_SECTIONS = {
    # Short recension (T251) sections
    "title",
    "opening",
    "form_emptiness",
    "characteristics",
    "skandha_characteristics",
    "negations_skandhas",
    "negations_ayatanas",
    "negations_dhatus",
    "negations_pratityasamutpada",
    "negations_truths",
    "bodhisattva_result",
    "buddha_result",
    "mantra_praise",
    "mantra",
    "closing",
    # Long recension (T257) additional sections
    "nidana",
    "shariputra_question",
    "avalokiteshvara_response",
    "avalokiteshvara_conclusion",
    "buddha_approval",
    "audience_rejoicing",
    "colophon",
    # Variant section names used across witnesses
    "negations",              # collapsed negation section (Hōryū-ji, T257)
    "temporal_negation",      # T250-specific
    "invocation",             # Sanskrit namo opening
    "mangala",                # Sanskrit/Hōryū-ji maṅgala verse
}

# Pattern for base_parallel values: WitnessID:Number  (e.g. "T251:1")
_BASE_PARALLEL_RE = re.compile(r"^[A-Za-z0-9_]+:\d+$")


def validate_witness_file(path: Path, witness_type: str) -> list[str]:
    """
    Validate a witness JSON file against the expected schema.

    Checks:
    - File exists and is valid JSON
    - Top-level is a dict with 'segments' (or recognized alternate structure)
    - Each segment has required fields of the correct type
    - Required string fields are non-empty
    - No duplicate segment IDs
    - base_parallel format is valid when present
    - Section values are from the known set

    Args:
        path: Path to the JSON file
        witness_type: One of 'chinese', 'sanskrit', 'tibetan'

    Returns:
        List of error messages (empty if valid)
    """
    # Validate witness_type before any file I/O
    if witness_type not in _REQUIRED_BY_TYPE:
        raise ValueError(
            f"Unknown witness_type={witness_type!r}. "
            f"Must be one of: {', '.join(sorted(_REQUIRED_BY_TYPE))}"
        )

    errors = []

    if not path.exists():
        return [f"File not found: {path}"]

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON in {path.name}: {e}"]

    if not isinstance(data, dict):
        return [f"{path.name}: top-level must be a dict, got {type(data).__name__}"]

    segments = data.get("segments")
    if segments is None:
        # Some files (e.g., T256, kangyur_editions) have alternate structures.
        # Require at least two recognized metadata keys to accept.
        if len(_ALTERNATE_KEYS & set(data.keys())) >= 2:
            return []  # Valid alternate structure
        errors.append(f"{path.name}: missing 'segments' key")
        return errors

    if not isinstance(segments, list):
        errors.append(f"{path.name}: 'segments' must be a list")
        return errors

    required = _REQUIRED_BY_TYPE[witness_type]

    seen_ids = set()
    for i, seg in enumerate(segments):
        seg_label = seg.get("id", i) if isinstance(seg, dict) else i

        if not isinstance(seg, dict):
            errors.append(f"{path.name}: segment {i} is not a dict")
            continue

        # --- Required fields ---
        missing = required - set(seg.keys())
        if missing:
            errors.append(
                f"{path.name}: segment {seg_label} missing fields: {missing}"
            )

        for fld in required:
            val = seg.get(fld)
            if val is not None and not isinstance(val, str):
                errors.append(
                    f"{path.name}: segment {seg_label} field '{fld}' "
                    f"should be str, got {type(val).__name__}"
                )
            elif isinstance(val, str) and val == "":
                errors.append(
                    f"{path.name}: segment {seg_label} field '{fld}' is empty"
                )

        # --- Duplicate IDs ---
        seg_id = seg.get("id")
        if seg_id is not None:
            if seg_id in seen_ids:
                errors.append(f"{path.name}: duplicate segment id '{seg_id}'")
            seen_ids.add(seg_id)

        # --- Section value ---
        section = seg.get("section")
        if isinstance(section, str) and section not in KNOWN_SECTIONS:
            errors.append(
                f"{path.name}: segment {seg_label} has unknown section '{section}'"
            )

        # --- base_parallel format ---
        cp = seg.get("base_parallel")
        if cp is not None:
            if not isinstance(cp, str):
                errors.append(
                    f"{path.name}: segment {seg_label} base_parallel "
                    f"should be str or null, got {type(cp).__name__}"
                )
            elif not _BASE_PARALLEL_RE.match(cp):
                errors.append(
                    f"{path.name}: segment {seg_label} base_parallel='{cp}' "
                    f"does not match expected pattern WitnessID:N"
                )

    return errors


def _collect_segment_ids(data_dir: Path) -> set[str]:
    """Collect all segment IDs from Chinese witness files across all subdirs."""
    ids: set[str] = set()
    chinese_dir = data_dir / "chinese"
    if not chinese_dir.exists():
        return ids
    for subdir in sorted(chinese_dir.iterdir()):
        if not subdir.is_dir():
            continue
        for f in subdir.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
                for seg in data.get("segments", []):
                    seg_id = seg.get("id")
                    if seg_id:
                        ids.add(seg_id)
            except json.JSONDecodeError:
                pass
    return ids


def validate_cross_references(data_dir: Path) -> list[str]:
    """
    Validate that base_parallel references point to real segment IDs.

    Checks all witnesses (Chinese alternates, Sanskrit, Tibetan) that have
    base_parallel fields and verifies the target IDs exist in the base
    witness files.

    Returns:
        List of error messages (empty if all references are valid)
    """
    errors = []
    chinese_ids = _collect_segment_ids(data_dir)
    if not chinese_ids:
        return errors

    for relpath, _wtype in _WITNESS_DIRS:
        d = data_dir / relpath
        if not d.exists():
            continue
        for f in d.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
            except json.JSONDecodeError:
                continue
            for seg in data.get("segments", []):
                cp = seg.get("base_parallel")
                if cp and cp not in chinese_ids:
                    errors.append(
                        f"{f.name}: segment {seg.get('id', '?')} has "
                        f"base_parallel='{cp}' which does not match any "
                        f"base witness segment ID"
                    )

    return errors


def validate_data_dir(data_dir: Path) -> dict[str, list[str]]:
    """
    Validate all witness files in a data directory.

    Scans all known subdirectories for JSON witness files and
    checks cross-file reference consistency.

    Returns:
        Dict mapping file paths to lists of errors
    """
    results = {}

    # Validate witness files across all tradition directories
    for relpath, wtype in _WITNESS_DIRS:
        d = data_dir / relpath
        if not d.exists():
            continue
        for f in d.glob("*.json"):
            errors = validate_witness_file(f, wtype)
            if errors:
                results[str(f)] = errors

    # Collation data (not a witness, but validate JSON structure)
    collation_dir = data_dir / "collation"
    if collation_dir.exists():
        for f in collation_dir.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    json.load(fh)
            except json.JSONDecodeError as e:
                results[str(f)] = [f"Invalid JSON in {f.name}: {e}"]

    # Cross-file reference checks
    xref_errors = validate_cross_references(data_dir)
    if xref_errors:
        results["cross_references"] = xref_errors

    return results


def main():
    """CLI entry point for data validation."""
    import sys
    from .data import resolve_data_dir, DATA_VERSION, compute_data_hash

    data_dir = resolve_data_dir(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"Data directory: {data_dir}")
    print(f"Data version:   {DATA_VERSION}")
    print(f"Data hash:      {compute_data_hash(data_dir)}")
    print()

    errors = validate_data_dir(data_dir)
    if errors:
        for path, errs in errors.items():
            for e in errs:
                print(f"ERROR: {e}")
        n_file = sum(1 for k in errors if k != "cross_references")
        n_xref = len(errors.get("cross_references", []))
        parts = []
        if n_file:
            parts.append(f"{n_file} file(s) with validation errors")
        if n_xref:
            parts.append(f"{n_xref} cross-reference error(s)")
        raise SystemExit(f"\n{'; '.join(parts)}")
    else:
        print("All data files valid.")


if __name__ == "__main__":
    main()
