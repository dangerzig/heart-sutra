"""
Synoptic alignment tool for parallel presentation of Heart Sūtra traditions.

Generates side-by-side views of:
- Chinese (base text)
- Sanskrit (IAST and Devanagari)
- Tibetan (Tibetan script and Wylie)
- English gloss
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html import escape as html_escape
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SynopticRow:
    """A single row in the synoptic alignment."""
    segment_id: str
    section: str

    # Chinese
    chinese: str = ""
    chinese_pinyin: str = ""

    # Sanskrit
    sanskrit_iast: str = ""
    sanskrit_devanagari: str = ""

    # Tibetan
    tibetan: str = ""
    tibetan_wylie: str = ""

    # English gloss
    english: str = ""

    # Notes on divergences
    divergence_notes: list[str] = field(default_factory=list)

    # Direction of dependence for this segment
    dependence: str = ""


@dataclass
class SynopticAlignment:
    """Complete synoptic alignment of the Heart Sūtra."""
    title: str = "Prajñāpāramitāhṛdaya Synoptic Alignment"
    methodology: str = "T251-anchored"

    # Witness information
    chinese_witness: str = "T251"
    sanskrit_witness: str = "GRETIL"
    tibetan_witness: str = "Toh21"

    # Aligned rows
    rows: list[SynopticRow] = field(default_factory=list)

    # Metadata
    notes: list[str] = field(default_factory=list)


class SynopticBuilder:
    """
    Builder for synoptic alignments of the Heart Sūtra.
    """

    def __init__(self, data_dir: Path):
        """
        Initialize builder with data directory.

        Args:
            data_dir: Path to data directory
        """
        from .data import DATA_VERSION, compute_data_hash

        self.data_dir = Path(data_dir)
        self._data_version = DATA_VERSION
        self._data_hash = compute_data_hash(self.data_dir)

    def load_witness(self, tradition: str, witness_id: str) -> dict:
        """
        Load a witness file.

        Args:
            tradition: "chinese", "sanskrit", or "tibetan"
            witness_id: Witness identifier (e.g., "T251", "GRETIL", "Toh21")

        Returns:
            Parsed JSON data, or empty dict if witness file not found

        Raises:
            ValueError: If tradition is unknown
        """
        if tradition == "chinese":
            # Search all subdirectories under chinese/
            path = None
            chinese_dir = self.data_dir / "chinese"
            if chinese_dir.exists():
                for subdir in sorted(chinese_dir.iterdir()):
                    if not subdir.is_dir():
                        continue
                    candidate = subdir / f"{witness_id.lower()}.json"
                    if candidate.exists():
                        path = candidate
                        break
                    candidate = subdir / f"{witness_id}.json"
                    if candidate.exists():
                        path = candidate
                        break
            if path is None:
                logger.warning(
                    "Witness file not found: %s/%s. "
                    "This witness will be omitted from the alignment.",
                    tradition, witness_id,
                )
                return {}
        elif tradition == "sanskrit":
            if witness_id == "GRETIL":
                path = self.data_dir / "sanskrit" / "gretil" / "prajnaparamitahrdaya.json"
            else:
                path = self.data_dir / "sanskrit" / "manuscripts" / f"{witness_id.lower()}.json"
        elif tradition == "tibetan":
            path = self.data_dir / "tibetan" / "kangyur" / f"{witness_id.lower()}.json"
            if not path.exists():
                path = self.data_dir / "tibetan" / "dunhuang" / f"{witness_id.lower()}.json"
        else:
            raise ValueError(f"Unknown tradition: {tradition}")

        if not path.exists():
            logger.warning(
                "Witness file not found: %s/%s (expected at %s). "
                "This witness will be omitted from the alignment.",
                tradition, witness_id, path
            )
            return {}

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(
                "Malformed JSON in %s: %s. "
                "This witness will be omitted from the alignment.",
                path, e,
            )
            return {}

    # Default witness IDs for the standard alignment
    DEFAULT_CHINESE = "T251"
    DEFAULT_SANSKRIT = "GRETIL"
    DEFAULT_TIBETAN = "Toh21"

    def build_alignment(
        self,
        chinese_id: str = DEFAULT_CHINESE,
        sanskrit_id: str = DEFAULT_SANSKRIT,
        tibetan_id: str = DEFAULT_TIBETAN,
        anchor_tradition: str = "chinese",
    ) -> SynopticAlignment:
        """
        Build synoptic alignment from specified witnesses.

        Args:
            chinese_id: Chinese witness ID (default: T251)
            sanskrit_id: Sanskrit witness ID (default: GRETIL)
            tibetan_id: Tibetan witness ID (default: Toh21)
            anchor_tradition: Tradition to use as anchor
                ("chinese", "sanskrit", or "tibetan"; default "chinese")

        Returns:
            SynopticAlignment object
        """
        if anchor_tradition != "chinese":
            raise ValueError(
                f"anchor_tradition={anchor_tradition!r} is not supported. "
                f"Only 'chinese' is currently implemented."
            )

        # Load witnesses
        chinese = self.load_witness("chinese", chinese_id)
        if not chinese or not chinese.get("segments"):
            raise ValueError(
                f"Base Chinese witness '{chinese_id}' not found or has no segments. "
                f"Check that data/chinese/taisho/{chinese_id.lower()}.json exists."
            )
        sanskrit = self.load_witness("sanskrit", sanskrit_id)
        tibetan = self.load_witness("tibetan", tibetan_id)

        alignment = SynopticAlignment(
            chinese_witness=chinese_id,
            sanskrit_witness=sanskrit_id,
            tibetan_witness=tibetan_id,
        )

        # Build segment index for Sanskrit
        sanskrit_by_parallel = {}
        for seg in sanskrit.get("segments", []):
            parallel = seg.get("base_parallel")
            if parallel:
                if parallel in sanskrit_by_parallel:
                    logger.warning(
                        "%s: duplicate base_parallel=%r in Sanskrit, "
                        "later segment overwrites earlier",
                        sanskrit_id, parallel,
                    )
                sanskrit_by_parallel[parallel] = seg

        # Build segment index for Tibetan
        tibetan_by_parallel = {}
        for seg in tibetan.get("segments", []):
            parallel = seg.get("base_parallel")
            if parallel:
                if parallel in tibetan_by_parallel:
                    logger.warning(
                        "%s: duplicate base_parallel=%r in Tibetan, "
                        "later segment overwrites earlier",
                        tibetan_id, parallel,
                    )
                tibetan_by_parallel[parallel] = seg

        # Iterate through Chinese segments (base)
        for c_seg in chinese.get("segments", []):
            seg_id = c_seg.get("id", "")
            section = c_seg.get("section", "")

            row = SynopticRow(
                segment_id=seg_id,
                section=section,
                chinese=c_seg.get("text", ""),
                chinese_pinyin=c_seg.get("pinyin", ""),
                english=c_seg.get("english_gloss", ""),
            )

            # Add Sanskrit if available
            s_seg = sanskrit_by_parallel.get(seg_id)
            if s_seg:
                row.sanskrit_iast = s_seg.get("iast", "")
                row.sanskrit_devanagari = s_seg.get("devanagari", "")

                # Check for divergence notes
                if s_seg.get("note"):
                    row.divergence_notes.append(f"Sanskrit: {s_seg['note']}")

            # Add Tibetan if available
            t_seg = tibetan_by_parallel.get(seg_id)
            if t_seg:
                row.tibetan = t_seg.get("tibetan", "")
                row.tibetan_wylie = t_seg.get("wylie", "")

                if t_seg.get("note"):
                    row.divergence_notes.append(f"Tibetan: {t_seg['note']}")

            alignment.rows.append(row)

        return alignment

    def to_markdown(self, alignment: SynopticAlignment) -> str:
        """
        Convert alignment to Markdown format.

        Args:
            alignment: SynopticAlignment object

        Returns:
            Markdown string
        """
        lines = [
            f"# {alignment.title}",
            "",
            "## Methodology",
            "",
            f"- **Base text**: {alignment.chinese_witness} (Chinese)",
            f"- **Sanskrit witness**: {alignment.sanskrit_witness}",
            f"- **Tibetan witness**: {alignment.tibetan_witness}",
            "",
            "---",
            "",
        ]

        current_section = ""

        for row in alignment.rows:
            # Section header
            if row.section != current_section:
                current_section = row.section
                section_title = current_section.replace("_", " ").title()
                lines.extend([
                    f"## {section_title}",
                    "",
                ])

            # Segment
            lines.extend([
                f"### {row.segment_id}",
                "",
                "**Chinese (Base)**",
                f"> {row.chinese}",
                "",
            ])

            if row.chinese_pinyin:
                lines.extend([
                    f"*Pinyin*: {row.chinese_pinyin}",
                    "",
                ])

            if row.sanskrit_iast:
                lines.extend([
                    "**Sanskrit (IAST)**",
                    f"> {row.sanskrit_iast}",
                    "",
                ])

            if row.sanskrit_devanagari:
                lines.extend([
                    "**Sanskrit (Devanagari)**",
                    f"> {row.sanskrit_devanagari}",
                    "",
                ])

            if row.tibetan:
                lines.extend([
                    "**Tibetan**",
                    f"> {row.tibetan}",
                    "",
                ])

            if row.tibetan_wylie:
                lines.extend([
                    f"*Wylie*: {row.tibetan_wylie}",
                    "",
                ])

            if row.english:
                lines.extend([
                    "**English Gloss**",
                    f"> {row.english}",
                    "",
                ])

            if row.divergence_notes:
                lines.append("**Notes on Divergences**")
                for note in row.divergence_notes:
                    lines.append(f"- {note}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def to_html(self, alignment: SynopticAlignment) -> str:
        """
        Convert alignment to HTML format with parallel columns.

        Args:
            alignment: SynopticAlignment object

        Returns:
            HTML string
        """
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            f"  <title>{html_escape(alignment.title)}</title>",
            "  <style>",
            "    body { font-family: 'Noto Sans', sans-serif; margin: 2em; }",
            "    .synoptic-table { width: 100%; border-collapse: collapse; }",
            "    .synoptic-table th, .synoptic-table td { ",
            "      border: 1px solid #ccc; padding: 0.5em; vertical-align: top; ",
            "    }",
            "    .synoptic-table th { background: #f5f5f5; }",
            "    .chinese { font-size: 1.2em; }",
            "    .sanskrit { font-family: 'Noto Sans Devanagari', serif; }",
            "    .tibetan { font-family: 'Noto Sans Tibetan', serif; }",
            "    .pinyin, .wylie, .iast { font-style: italic; color: #666; }",
            "    .section-header { background: #e0e0e0; font-weight: bold; }",
            "    .notes { font-size: 0.9em; color: #666; }",
            "  </style>",
            "</head>",
            "<body>",
            f"  <h1>{html_escape(alignment.title)}</h1>",
            "  <table class='synoptic-table'>",
            "    <thead>",
            "      <tr>",
            "        <th>ID</th>",
            "        <th>Chinese (Base)</th>",
            "        <th>Sanskrit</th>",
            "        <th>Tibetan</th>",
            "        <th>English</th>",
            "      </tr>",
            "    </thead>",
            "    <tbody>",
        ]

        current_section = ""

        for row in alignment.rows:
            # Section header row
            if row.section != current_section:
                current_section = row.section
                section_title = current_section.replace("_", " ").title()
                html_parts.append(
                    f"      <tr class='section-header'>"
                    f"<td colspan='5'>{html_escape(section_title)}</td></tr>"
                )

            # Data row (all text values HTML-escaped, lang attrs for accessibility)
            chinese_cell = f"<span class='chinese' lang='lzh'>{html_escape(row.chinese)}</span>"
            if row.chinese_pinyin:
                chinese_cell += f"<br><span class='pinyin' lang='zh-Latn'>{html_escape(row.chinese_pinyin)}</span>"

            sanskrit_cell = ""
            if row.sanskrit_devanagari:
                sanskrit_cell += f"<span class='sanskrit' lang='sa-Deva'>{html_escape(row.sanskrit_devanagari)}</span><br>"
            if row.sanskrit_iast:
                sanskrit_cell += f"<span class='iast' lang='sa-Latn'>{html_escape(row.sanskrit_iast)}</span>"

            tibetan_cell = ""
            if row.tibetan:
                tibetan_cell += f"<span class='tibetan' lang='bo'>{html_escape(row.tibetan)}</span>"
            if row.tibetan_wylie:
                tibetan_cell += f"<br><span class='wylie' lang='bo-Latn'>{html_escape(row.tibetan_wylie)}</span>"

            english_cell = html_escape(row.english)
            if row.divergence_notes:
                english_cell += "<div class='notes'>"
                for note in row.divergence_notes:
                    english_cell += f"<br>• {html_escape(note)}"
                english_cell += "</div>"

            html_parts.append(
                f"      <tr>"
                f"<td>{html_escape(row.segment_id)}</td>"
                f"<td>{chinese_cell}</td>"
                f"<td>{sanskrit_cell}</td>"
                f"<td>{tibetan_cell}</td>"
                f"<td>{english_cell}</td>"
                f"</tr>"
            )

        html_parts.extend([
            "    </tbody>",
            "  </table>",
            "</body>",
            "</html>",
        ])

        return "\n".join(html_parts)

    def to_json(self, alignment: SynopticAlignment) -> str:
        """
        Convert alignment to JSON format.

        Args:
            alignment: SynopticAlignment object

        Returns:
            JSON string
        """
        data = {
            "title": alignment.title,
            "methodology": alignment.methodology,
            "witnesses": {
                "chinese": alignment.chinese_witness,
                "sanskrit": alignment.sanskrit_witness,
                "tibetan": alignment.tibetan_witness,
            },
            "rows": [
                {
                    "id": row.segment_id,
                    "section": row.section,
                    "chinese": {
                        "text": row.chinese,
                        "pinyin": row.chinese_pinyin,
                    },
                    "sanskrit": {
                        "iast": row.sanskrit_iast,
                        "devanagari": row.sanskrit_devanagari,
                    },
                    "tibetan": {
                        "text": row.tibetan,
                        "wylie": row.tibetan_wylie,
                    },
                    "english": row.english,
                    "divergence_notes": row.divergence_notes,
                }
                for row in alignment.rows
            ],
            "notes": alignment.notes,
            "provenance": {
                "generated": datetime.now(timezone.utc).isoformat(),
                "tool": "hrdaya.synoptic",
                "version": "1.0.0",
                "data_version": self._data_version,
                "data_hash": self._data_hash,
            },
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


def build_synoptic(data_dir: Path, output_format: str = "markdown") -> str:
    """
    Build synoptic alignment and return in specified format.

    Args:
        data_dir: Path to data directory
        output_format: Output format ('markdown', 'html', or 'json')

    Returns:
        Formatted string
    """
    builder = SynopticBuilder(data_dir)
    alignment = builder.build_alignment()

    if output_format == "markdown":
        return builder.to_markdown(alignment)
    elif output_format == "html":
        return builder.to_html(alignment)
    elif output_format == "json":
        return builder.to_json(alignment)
    else:
        raise ValueError(f"Unknown format: {output_format}")


def main():
    """CLI entry point for synoptic alignment."""
    import argparse
    from .data import resolve_data_dir

    parser = argparse.ArgumentParser(
        description="Generate synoptic alignment of the Heart Sūtra."
    )
    parser.add_argument(
        "format", nargs="?", default="markdown",
        choices=["markdown", "html", "json"],
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--data-dir", default=None,
        help="Path to data directory (auto-detected if not specified)",
    )
    args = parser.parse_args()

    data_dir = resolve_data_dir(args.data_dir)
    print(build_synoptic(data_dir, args.format))


if __name__ == "__main__":
    main()
