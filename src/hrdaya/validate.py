"""
Data validation for Heart Sūtra witness files.

Validates that JSON data files conform to expected schemas
for Chinese, Sanskrit, and Tibetan witnesses.
"""

import json
from pathlib import Path


# Required fields per witness type
CHINESE_SEGMENT_FIELDS = {"id", "section", "text"}
SANSKRIT_SEGMENT_FIELDS = {"id", "section", "iast"}
TIBETAN_SEGMENT_FIELDS = {"id", "section", "tibetan"}


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
        # Some files (e.g., T256) have alternate structures
        if "id" in data or "title_chinese" in data:
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

    for i, seg in enumerate(segments):
        if not isinstance(seg, dict):
            errors.append(f"{path.name}: segment {i} is not a dict")
            continue
        missing = required - set(seg.keys())
        if missing:
            errors.append(
                f"{path.name}: segment {seg.get('id', i)} missing fields: {missing}"
            )

    return errors


def validate_data_dir(data_dir: Path) -> dict[str, list[str]]:
    """
    Validate all witness files in a data directory.

    Scans all known subdirectories for JSON witness files.

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
                import json
                with open(f, 'r', encoding='utf-8') as fh:
                    json.load(fh)
            except json.JSONDecodeError as e:
                results[str(f)] = [f"Invalid JSON in {f.name}: {e}"]

    return results
