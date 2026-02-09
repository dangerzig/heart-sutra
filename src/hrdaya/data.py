"""
Shared data directory resolution for hrdaya tools.

Provides a consistent way to locate the data directory across
CLI tools and library usage.
"""

import os
from pathlib import Path


def resolve_data_dir(explicit_path: str | None = None) -> Path:
    """
    Resolve the data directory from the most specific source available.

    Resolution order:
    1. Explicit path argument (from CLI or API)
    2. HRDAYA_DATA_DIR environment variable
    3. Relative to source tree (development installs)
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
        "Error: cannot find data directory.\n"
        "Provide the path explicitly, or set the HRDAYA_DATA_DIR environment variable.\n"
        "  Example: hrdaya-collate /path/to/data\n"
        "  Example: HRDAYA_DATA_DIR=/path/to/data hrdaya-collate"
    )
