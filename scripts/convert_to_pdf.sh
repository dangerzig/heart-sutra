#!/bin/bash
# Convert Markdown documents to PDF with full Unicode support
# Usage: ./convert_to_pdf.sh input.md [output.pdf]

set -e

# Add TeX to PATH
export PATH="/Library/TeX/texbin:$PATH"

INPUT="$1"
OUTPUT="${2:-${INPUT%.md}.pdf}"

if [ -z "$INPUT" ]; then
    echo "Usage: $0 input.md [output.pdf]"
    exit 1
fi

if [ ! -f "$INPUT" ]; then
    echo "Error: $INPUT not found"
    exit 1
fi

echo "Converting $INPUT to $OUTPUT..."

pandoc "$INPUT" \
    -o "$OUTPUT" \
    --pdf-engine=xelatex \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V documentclass=article \
    -V mainfont="Noto Serif" \
    -V sansfont="Noto Sans" \
    -V monofont="Noto Sans Mono" \
    -V CJKmainfont="Noto Serif CJK SC" \
    -V CJKsansfont="Noto Sans CJK SC" \
    -V CJKmonofont="Noto Sans CJK SC" \
    --toc \
    --toc-depth=3 \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    2>&1 | grep -v "^\[WARNING\]" || true

echo "Created: $OUTPUT"
