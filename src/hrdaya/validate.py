"""
Data validation for Heart Sūtra witness files.

Validates that JSON data files conform to expected schemas
for Chinese, Sanskrit, and Tibetan witnesses. Includes
cross-file consistency checks for chinese_parallel references.
"""

import json
from pathlib import Path


# Required fields per witness type
CHINESE_SEGMENT_FIELDS = {"id", "section", "text"}
SANSKRIT_SEGMENT_FIELDS = {"id", "section", "iast"}
TIBETAN_SEGMENT_FIELDS = {"id", "section", "tibetan"}

# Optional but recognized fields per witness type
CHINESE_OPTIONAL_FIELDS = {"pinyin", "english_gloss", "variants_from_T251", "chinese_parallel", "notes"}
SANSKRIT_OPTIONAL_FIELDS = {"devanagari", "chinese_parallel", "note", "english_gloss"}
TIBETAN_OPTIONAL_FIELDS = {"wylie", "chinese_parallel", "note", "english_gloss"}


def validate_witness_file(path: Path, witness_type: str) -> list[str]:
    """
    Validate a witness JSON file.

    Args:
        path: Path to the JSON file
        witness_type: One of 'chinese', 'sanskrit', 'tibetan'

    Returns:
        List of error messages (empty if valid)
    """
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
        # Some files (e.g., T256, kangyur_editions) have alternate structures
        if "id" in data or "title_chinese" in data or "editions" in data:
            return []  # Valid alternate structure
        errors.append(f"{path.name}: missing 'segments' key")
        return errors

    if not isinstance(segments, list):
        errors.append(f"{path.name}: 'segments' must be a list")
        return errors

    required = {
        "chinese": CHINESE_SEGMENT_FIELDS,
        "sanskrit": SANSKRIT_SEGMENT_FIELDS,
        "tibetan": TIBETAN_SEGMENT_FIELDS,
    }.get(witness_type, CHINESE_SEGMENT_FIELDS)

    seen_ids = set()
    for i, seg in enumerate(segments):
        if not isinstance(seg, dict):
            errors.append(f"{path.name}: segment {i} is not a dict")
            continue
        missing = required - set(seg.keys())
        if missing:
            errors.append(
                f"{path.name}: segment {seg.get('id', i)} missing fields: {missing}"
            )

        # Check for duplicate segment IDs
        seg_id = seg.get("id")
        if seg_id is not None:
            if seg_id in seen_ids:
                errors.append(f"{path.name}: duplicate segment id '{seg_id}'")
            seen_ids.add(seg_id)

        # Check that required fields are non-empty strings
        for fld in required:
            val = seg.get(fld)
            if val is not None and not isinstance(val, str):
                errors.append(
                    f"{path.name}: segment {seg.get('id', i)} field '{fld}' "
                    f"should be str, got {type(val).__name__}"
                )

        # Check chinese_parallel format when present (should be "WitnessID:N" or null)
        cp = seg.get("chinese_parallel")
        if cp is not None and not isinstance(cp, str):
            errors.append(
                f"{path.name}: segment {seg.get('id', i)} chinese_parallel "
                f"should be str or null, got {type(cp).__name__}"
            )

    return errors


def _collect_segment_ids(data_dir: Path) -> set[str]:
    """Collect all segment IDs from Chinese Taishō witness files."""
    ids: set[str] = set()
    taisho_dir = data_dir / "chinese" / "taisho"
    if not taisho_dir.exists():
        return ids
    for f in taisho_dir.glob("*.json"):
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            for seg in data.get("segments", []):
                seg_id = seg.get("id")
                if seg_id:
                    ids.add(seg_id)
        except (json.JSONDecodeError, KeyError):
            pass
    return ids


def validate_cross_references(data_dir: Path) -> list[str]:
    """
    Validate that chinese_parallel references point to real segment IDs.

    Checks all witnesses (Chinese alternates, Sanskrit, Tibetan) that have
    chinese_parallel fields and verifies the target IDs exist in the base
    Chinese witness files.

    Returns:
        List of error messages (empty if all references are valid)
    """
    errors = []
    chinese_ids = _collect_segment_ids(data_dir)
    if not chinese_ids:
        return errors

    # Check all witness directories
    dirs_to_check = [
        (data_dir / "chinese" / "taisho", "chinese"),
        (data_dir / "sanskrit" / "gretil", "sanskrit"),
        (data_dir / "tibetan" / "kangyur", "tibetan"),
        (data_dir / "tibetan" / "dunhuang", "tibetan"),
    ]

    for d, _wtype in dirs_to_check:
        if not d.exists():
            continue
        for f in d.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
            except (json.JSONDecodeError, KeyError):
                continue
            for seg in data.get("segments", []):
                cp = seg.get("chinese_parallel")
                if cp and cp not in chinese_ids:
                    errors.append(
                        f"{f.name}: segment {seg.get('id', '?')} has "
                        f"chinese_parallel='{cp}' which does not match any "
                        f"Chinese segment ID"
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

    # Chinese witness directories
    chinese_dirs = [
        data_dir / "chinese" / "taisho",
        data_dir / "chinese" / "dunhuang",
        data_dir / "chinese" / "epigraphy",
        data_dir / "chinese" / "manuscripts",
    ]
    for d in chinese_dirs:
        if d.exists():
            for f in d.glob("*.json"):
                errors = validate_witness_file(f, "chinese")
                if errors:
                    results[str(f)] = errors

    # Sanskrit witness directories
    sanskrit_dirs = [
        data_dir / "sanskrit" / "gretil",
        data_dir / "sanskrit" / "manuscripts",
    ]
    for d in sanskrit_dirs:
        if d.exists():
            for f in d.glob("*.json"):
                errors = validate_witness_file(f, "sanskrit")
                if errors:
                    results[str(f)] = errors

    # Tibetan witness directories
    tibetan_dirs = [
        data_dir / "tibetan" / "kangyur",
        data_dir / "tibetan" / "dunhuang",
    ]
    for d in tibetan_dirs:
        if d.exists():
            for f in d.glob("*.json"):
                errors = validate_witness_file(f, "tibetan")
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
