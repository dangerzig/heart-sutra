"""
Shared data directory resolution and versioning for hrdaya tools.

Provides a consistent way to locate and verify the data directory
across CLI tools and library usage.

Data packaging strategy: The witness data files (JSON) live at the
repository root under data/ and are NOT shipped inside the Python
wheel. This is intentional — scholarly primary-source data should be
versioned alongside the code in git, not buried inside a wheel.
Users who install via pip must either:
  (a) clone the repository and use `pip install -e .`, or
  (b) download the data directory separately and set HRDAYA_DATA_DIR.
"""

import hashlib
import os
from pathlib import Path

# Data version: bump when witness files change in a way that affects
# collation or synoptic output. Follows semver:
#   major = structural schema change
#   minor = new witnesses or segments added
#   patch = corrections to existing data
DATA_VERSION = "1.1.0"


def compute_data_hash(data_dir: Path) -> str:
    """
    Compute a short SHA-256 hash over all JSON files in the data directory.

    This provides a reproducibility fingerprint: two runs with the same
    data_hash used the same input files.

    Args:
        data_dir: Path to the data directory.

    Returns:
        First 12 hex characters of the SHA-256 digest.
    """
    h = hashlib.sha256()
    for p in sorted(data_dir.rglob("*.json")):
        h.update(str(p.relative_to(data_dir)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def resolve_data_dir(explicit_path: str | None = None) -> Path:
    """
    Resolve the data directory from the most specific source available.

    Resolution order:
    1. Explicit path argument (from CLI or API)
    2. HRDAYA_DATA_DIR environment variable
    3. Relative to source tree (development / editable installs)
    4. Current working directory / data

    Args:
        explicit_path: Optional explicit path to the data directory.

    Returns:
        Path to the data directory.

    Raises:
        SystemExit: If no valid data directory can be found.
    """
    # 1. Explicit argument
    if explicit_path:
        p = Path(explicit_path)
        if p.is_dir():
            return p
        raise SystemExit(f"Error: data directory not found: {p}")

    # 2. Environment variable
    env_dir = os.environ.get("HRDAYA_DATA_DIR")
    if env_dir:
        p = Path(env_dir)
        if p.is_dir():
            return p
        raise SystemExit(
            f"Error: HRDAYA_DATA_DIR is set to '{env_dir}' but that directory does not exist."
        )

    # 3. Relative to source tree (development / editable install)
    dev_path = Path(__file__).parent.parent.parent / "data"
    if dev_path.is_dir():
        return dev_path

    # 4. Current working directory
    cwd_path = Path.cwd() / "data"
    if cwd_path.is_dir():
        return cwd_path

    raise SystemExit(
        "Error: cannot locate the hrdaya data directory.\n"
        "\n"
        "The witness data files are not packaged inside the Python wheel.\n"
        "To provide data, use one of these methods:\n"
        "\n"
        "  1. Clone the repository and install in editable mode:\n"
        "       git clone <repo-url> && cd heart-sutra && pip install -e .\n"
        "\n"
        "  2. Set the HRDAYA_DATA_DIR environment variable:\n"
        "       export HRDAYA_DATA_DIR=/path/to/heart-sutra/data\n"
        "\n"
        "  3. Pass the path directly on the command line:\n"
        "       hrdaya-collate /path/to/data\n"
    )
