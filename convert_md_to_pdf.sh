#!/bin/bash

# Exit on error
set -e

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ Error: pandoc is not installed. Please install it first:"
    echo "   brew install pandoc  # macOS"
    echo "   sudo apt-get install pandoc  # Ubuntu/Debian"
    exit 1
fi

# Find all .md files and convert them to PDF using pandoc
echo "🔍 Finding Markdown files..."
find . -type f -name "*.md" | while read -r md_file; do
    pdf_file="${md_file%.md}.pdf"
    echo "Converting: $md_file → $pdf_file"
    
    # Convert with better formatting options
    pandoc "$md_file" -o "$pdf_file" \
        --pdf-engine=xelatex \
        --variable geometry:margin=1in \
        --variable fontsize=11pt \
        --variable colorlinks=true \
        --toc \
        2>/dev/null || {
        # Fallback to basic conversion if advanced options fail
        echo "⚠️  Advanced formatting failed, using basic conversion..."
        pandoc "$md_file" -o "$pdf_file"
    }
done

echo "✅ All Markdown files converted to PDF."