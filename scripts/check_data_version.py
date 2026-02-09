#!/usr/bin/env python3
"""CI guard: ensure DATA_VERSION is bumped when data/ files change.

Compares the current branch against the merge base with the default
branch. If any file under data/ has been added, modified, or deleted
AND src/hrdaya/data.py is unchanged, the script exits with an error
reminding the developer to bump DATA_VERSION.

Usage (in CI):
    python scripts/check_data_version.py

Exit codes:
    0  No data change, or DATA_VERSION was also touched.
    1  Data changed but DATA_VERSION was not bumped.
"""

import subprocess
import sys


def main() -> int:
    # Determine the merge base with the default branch.
    # In a PR this is the branch point; on main pushes it is HEAD~1.
    for base_ref in ("origin/main", "origin/master", "HEAD~1"):
        result = subprocess.run(
            ["git", "merge-base", "HEAD", base_ref],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            merge_base = result.stdout.strip()
            break
    else:
        # Shallow clone or initial commit — nothing to compare
        print("check_data_version: could not determine merge base, skipping.")
        return 0

    # Get the list of changed files since the merge base
    diff_result = subprocess.run(
        ["git", "diff", "--name-only", merge_base, "HEAD"],
        capture_output=True, text=True,
    )
    if diff_result.returncode != 0:
        print("check_data_version: git diff failed, skipping.")
        return 0

    changed = diff_result.stdout.strip().splitlines()

    data_changed = any(f.startswith("data/") for f in changed)
    version_touched = "src/hrdaya/data.py" in changed

    if data_changed and not version_touched:
        print(
            "ERROR: Files under data/ were modified but "
            "src/hrdaya/data.py (DATA_VERSION) was not updated.\n"
            "Please bump DATA_VERSION in src/hrdaya/data.py.",
            file=sys.stderr,
        )
        return 1

    if data_changed and version_touched:
        print("check_data_version: data changed and DATA_VERSION was updated. OK.")
    else:
        print("check_data_version: no data changes detected. OK.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
