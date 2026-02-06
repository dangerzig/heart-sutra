#!/usr/bin/env python3
"""
Convert Markdown to print-ready HTML (open in browser and print to PDF).
"""

import markdown
import sys
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm;
        }}

        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #333;
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }}

        h1 {{
            font-size: 24pt;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
            margin-top: 0;
        }}

        h2 {{
            font-size: 16pt;
            border-bottom: 1px solid #666;
            padding-bottom: 5px;
            margin-top: 30px;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 13pt;
            margin-top: 20px;
            page-break-after: avoid;
        }}

        h4 {{
            font-size: 11pt;
            font-style: italic;
            margin-top: 15px;
            page-break-after: avoid;
        }}

        p {{
            margin: 10px 0;
            text-align: justify;
        }}

        code {{
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }}

        pre {{
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
            page-break-inside: avoid;
        }}

        pre code {{
            background: none;
            padding: 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}

        th, td {{
            border: 1px solid #999;
            padding: 8px 10px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            background: #f0f0f0;
            font-weight: bold;
        }}

        tr:nth-child(even) {{
            background: #fafafa;
        }}

        blockquote {{
            border-left: 3px solid #666;
            margin: 15px 0;
            padding: 10px 20px;
            background: #f9f9f9;
            font-style: italic;
        }}

        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}

        li {{
            margin: 5px 0;
        }}

        hr {{
            border: none;
            border-top: 1px solid #ccc;
            margin: 30px 0;
        }}

        strong {{
            font-weight: bold;
        }}

        em {{
            font-style: italic;
        }}

        /* Sanskrit/Tibetan text styling */
        .devanagari {{
            font-family: 'Noto Sans Devanagari', serif;
        }}

        .tibetan {{
            font-family: 'Noto Sans Tibetan', serif;
        }}

        /* Print-specific */
        @media print {{
            body {{
                padding: 0;
            }}

            h1 {{
                page-break-before: avoid;
            }}

            h2, h3, h4 {{
                page-break-after: avoid;
            }}

            pre, table, blockquote {{
                page-break-inside: avoid;
            }}

            a {{
                color: #333;
                text-decoration: none;
            }}

            a[href]:after {{
                content: none;
            }}
        }}
    </style>
</head>
<body>
{content}
<footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 9pt; color: #666; text-align: center;">
    <p>Heart Sūtra Critical Edition Project</p>
</footer>
</body>
</html>
"""


def convert_md_to_html(md_path: Path, html_path: Path):
    """Convert Markdown file to print-ready HTML."""

    # Read markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract title from first heading
    title = "Document"
    for line in md_content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break

    # Convert to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'toc']
    )

    # Create full HTML document
    full_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content
    )

    # Write HTML file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    return html_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <input.md> [output.html]")
        sys.exit(1)

    md_path = Path(sys.argv[1])

    if len(sys.argv) > 2:
        html_path = Path(sys.argv[2])
    else:
        html_path = md_path.with_suffix('.html')

    if not md_path.exists():
        print(f"Error: {md_path} not found")
        sys.exit(1)

    output = convert_md_to_html(md_path, html_path)
    print(f"Created: {output}")
    print(f"\nTo create PDF: Open {output} in a browser and print to PDF (Cmd+P)")


if __name__ == "__main__":
    main()
