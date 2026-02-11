"""Check that LaTeX apparatus reflects all witnesses in the variant table.

Compares witness IDs found in data/collation/variant_table.json against
those mentioned in the apparatus footnotes of the LaTeX editions.
Flags any witness that has variant readings in the data but is not
mentioned in the corresponding tex file's footnotes.

Usage:
    PYTHONPATH=src python scripts/check_latex_staleness.py
    # or: make check-stale
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
VARIANT_TABLE = ROOT / "data" / "collation" / "variant_table.json"

# Map from variant table tradition keys to tex files that should cite them.
# Each tex file covers a specific tradition's apparatus.
TEX_FILES = {
    "chinese": ROOT / "output" / "latex" / "chinese_critical.tex",
}


def extract_variant_witnesses(variant_table: dict) -> dict[str, set[str]]:
    """Return {tradition: {witness_ids with non-base readings}} from variant table."""
    result: dict[str, set[str]] = {}
    for _section, entries in variant_table.get("sections", {}).items():
        for entry in entries:
            base = entry.get("base_witness", "")
            readings = entry.get("readings", {})
            for tradition, witnesses in readings.items():
                if not isinstance(witnesses, dict):
                    continue
                for wit_id, text in witnesses.items():
                    if wit_id == base:
                        continue
                    # Only flag if the reading actually differs from base
                    base_text = witnesses.get(base, "")
                    if text != base_text:
                        result.setdefault(tradition, set()).add(wit_id)
    return result


def extract_tex_witnesses(tex_path: Path) -> set[str]:
    """Return set of witness IDs cited in apparatus footnotes via \\wit{} commands.

    Only counts \\wit{} inside \\footnote{} blocks — the witness description
    list at the top of the file is excluded so that merely listing a witness
    does not suppress the staleness warning.
    """
    if not tex_path.exists():
        return set()
    content = tex_path.read_text(encoding="utf-8")
    # Extract all \footnote{...} blocks (handling nested braces)
    witnesses = set()
    for match in re.finditer(r"\\footnote\{", content):
        start = match.end()
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            if content[i] == "{":
                depth += 1
            elif content[i] == "}":
                depth -= 1
            i += 1
        footnote_text = content[start : i - 1]
        witnesses.update(re.findall(r"\\wit\{([^}]+)\}", footnote_text))
    return witnesses


def main() -> int:
    if not VARIANT_TABLE.exists():
        print(f"ERROR: Variant table not found: {VARIANT_TABLE}")
        print("  Run 'make collation' first.")
        return 1

    vt = json.loads(VARIANT_TABLE.read_text(encoding="utf-8"))
    variant_witnesses = extract_variant_witnesses(vt)

    stale = False
    for tradition, tex_path in TEX_FILES.items():
        if not tex_path.exists():
            print(f"SKIP: {tex_path.name} not found")
            continue

        data_wits = variant_witnesses.get(tradition, set())
        tex_wits = extract_tex_witnesses(tex_path)

        # Witnesses with variants in data but not mentioned in tex footnotes
        missing = data_wits - tex_wits
        if missing:
            stale = True
            print(f"STALE: {tex_path.name} is missing apparatus entries for:")
            for wit in sorted(missing):
                print(f"  - {wit}")

    if not stale:
        print("OK: All LaTeX editions are up to date with variant table.")
        return 0

    print()
    print("Witnesses listed above have variant readings in the data")
    print("but are not cited in the LaTeX apparatus footnotes.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
