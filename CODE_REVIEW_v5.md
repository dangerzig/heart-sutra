# Code Review v5 — Heart Sūtra Critical Edition

**Date**: 2026-02-08
**Reviewer**: Claude (automated)
**Scope**: Full codebase review following v4 fixes
**Tests**: 95 passing at review start

---

## Issues Found and Resolved

### 1. Dead Code: `CONSONANT_CHARS` (transliterate.py:109)

**Severity**: Low
**File**: `src/hrdaya/transliterate.py:109`

`CONSONANT_CHARS` set is defined but never referenced anywhere in the codebase. Likely a leftover from an earlier implementation approach.

**Fix**: Remove the unused constant.

---

### 2. Dead Code: `prev_was_consonant` (transliterate.py:200,245,253,259)

**Severity**: Low
**File**: `src/hrdaya/transliterate.py`

The variable `prev_was_consonant` is assigned in `iast_to_devanagari()` but never read. It appears to be scaffolding for a future feature (e.g., context-sensitive handling) that was never implemented.

**Fix**: Remove all assignments to `prev_was_consonant`.

---

### 3. Dead Code: Unused `seg_index` in collation loop (collate.py:392)

**Severity**: Low
**File**: `src/hrdaya/collate.py:392`

`enumerate(chinese_segs)` provides `seg_index` which is never used — it was the old fallback alignment key, removed in v4.

**Fix**: Change `for seg_index, c_seg in enumerate(...)` to plain `for c_seg in ...`.

---

### 4. Dead Code: Unused `Optional` import (collate.py:16, synoptic.py:16)

**Severity**: Low
**File**: `src/hrdaya/collate.py:16`, `src/hrdaya/synoptic.py:16`

`from typing import Optional` is imported but never used in either file. Both files already use the `X | None` union syntax (Python 3.10+).

**Fix**: Remove the unused import.

---

### 5. Dead Code: Unused optional field sets (validate.py:19-21)

**Severity**: Low
**File**: `src/hrdaya/validate.py:19-21`

`CHINESE_OPTIONAL_FIELDS`, `SANSKRIT_OPTIONAL_FIELDS`, and `TIBETAN_OPTIONAL_FIELDS` are defined but never referenced in any validation logic.

**Fix**: Remove the unused constants.

---

### 6. Logger Created Inside Method (synoptic.py:93-94)

**Severity**: Medium
**File**: `src/hrdaya/synoptic.py:93-94`

`import logging` and `logger = logging.getLogger(__name__)` appear inside `SynopticBuilder.load_witness()`, recreating the logger on every call. This is wasteful and inconsistent with collate.py which uses a module-level logger.

**Fix**: Move to module level.

---

### 7. Import Ordering (collate.py:19)

**Severity**: Low
**File**: `src/hrdaya/collate.py:19`

`logger = logging.getLogger(__name__)` is placed between stdlib imports and local imports. Standard Python convention (PEP 8) places all executable code after all imports.

**Fix**: Move logger definition after all import blocks.

---

### 8. Version Mismatch (models.py:237 vs pyproject.toml and __init__.py)

**Severity**: Medium
**File**: `src/hrdaya/models.py:237`

`CriticalApparatus.version` defaults to `"0.1.0"`, but `pyproject.toml` and `__init__.py` both declare version `"1.0.0"`. A consumer constructing a `CriticalApparatus()` would get the wrong version.

**Fix**: Update default to `"1.0.0"`.

---

### 9. Unescaped HTML in Synoptic Output (synoptic.py:334)

**Severity**: Medium
**File**: `src/hrdaya/synoptic.py:334`

The `<h1>` tag uses `alignment.title` directly without `html_escape()`, while the `<title>` tag on line 317 correctly escapes it. The title contains diacritics (ñ, ā, ṛ) which are safe in UTF-8 HTML, but the inconsistency is a code hygiene issue — if the title ever contained `<` or `&` it would be an XSS vector.

**Fix**: Apply `html_escape()` to the `<h1>` content.

---

### 10. Bare `except Exception` in `collate_full_text()` (collate.py:539)

**Severity**: Medium
**File**: `src/hrdaya/collate.py:539`

`collate_full_text()` catches `Exception` per-section, converting errors to `{"error": str(e)}` in the output dict. This silently swallows programming errors (TypeError, AttributeError, KeyError) that should surface as bugs.

**Fix**: Narrow to `(ValueError, FileNotFoundError)` — the expected failure modes.

---

### 11. Redundant `_resolve_data_dir` Wrappers (collate.py:553-556, synoptic.py:476-479)

**Severity**: Low
**File**: `src/hrdaya/collate.py:553-556`, `src/hrdaya/synoptic.py:476-479`

Both files define a local `_resolve_data_dir` that does nothing but `from .data import resolve_data_dir; return resolve_data_dir(...)`. This unnecessary indirection adds cognitive overhead.

**Fix**: Import `resolve_data_dir` directly in `main()`.

---

### 12. Missing Test Coverage for High-Level Entry Points

**Severity**: Medium
**Files**: `tests/`

The following public functions have no test coverage:
- `hrdaya.data.resolve_data_dir()` — the shared data directory resolution
- `hrdaya.collate.collate_full_text()` — the full-text collation entry point
- `hrdaya.synoptic.build_synoptic()` — the synoptic generation entry point

**Fix**: Add tests for all three.

---

### 13. `typing.Optional` Used in models.py Where `X | None` Would Be Consistent

**Severity**: Low (cosmetic)
**File**: `src/hrdaya/models.py`

`models.py` uses `Optional[str]` throughout while the rest of the codebase uses `X | None`. Since Python 3.10+ is required, this is a style inconsistency.

**Fix**: Replace `Optional[X]` with `X | None` and remove the `typing` import.

---

## Summary

| # | Severity | Category | File | Status |
|---|----------|----------|------|--------|
| 1 | Low | Dead code | transliterate.py | Fixed |
| 2 | Low | Dead code | transliterate.py | Fixed |
| 3 | Low | Dead code | collate.py | Fixed |
| 4 | Low | Dead import | collate.py, synoptic.py | Fixed |
| 5 | Low | Dead code | validate.py | Fixed |
| 6 | Medium | Performance/style | synoptic.py | Fixed |
| 7 | Low | Style | collate.py | Fixed |
| 8 | Medium | Correctness | models.py | Fixed |
| 9 | Medium | Security hygiene | synoptic.py | Fixed |
| 10 | Medium | Error handling | collate.py | Fixed |
| 11 | Low | Redundancy | collate.py, synoptic.py | Fixed |
| 12 | Medium | Test coverage | tests/ | Fixed |
| 13 | Low | Style consistency | models.py | Fixed |

All issues resolved in this pass.
