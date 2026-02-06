#!/usr/bin/env python3
"""
Generate synoptic alignment outputs for the Heart Sūtra critical edition.
"""

import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from hrdaya.synoptic import SynopticBuilder


def main():
    """Generate synoptic alignment in multiple formats."""
    data_dir = Path(__file__).parent.parent / "data"
    output_dir = Path(__file__).parent.parent / "data" / "aligned"
    output_dir.mkdir(exist_ok=True)

    print("Building synoptic alignment...")
    builder = SynopticBuilder(data_dir)
    alignment = builder.build_alignment()

    print(f"  - {len(alignment.rows)} segments aligned")

    # Generate Markdown
    md_output = output_dir / "synoptic_alignment.md"
    md_content = builder.to_markdown(alignment)
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"  - Markdown: {md_output}")

    # Generate HTML
    html_output = output_dir / "synoptic_alignment.html"
    html_content = builder.to_html(alignment)
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"  - HTML: {html_output}")

    # Generate JSON
    json_output = output_dir / "synoptic_alignment.json"
    json_content = builder.to_json(alignment)
    with open(json_output, 'w', encoding='utf-8') as f:
        f.write(json_content)
    print(f"  - JSON: {json_output}")

    print("\nDone!")


if __name__ == "__main__":
    main()
