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
    
    # Get the directory of the markdown file for relative image paths
    md_dir=$(dirname "$md_file")
    
    # Create a temporary file with emojis removed and relative links converted to GitHub URLs
    temp_file=$(mktemp)
    
    # Remove emojis for better PDF compatibility and convert .md links to GitHub URLs
    sed 's/[🧠🔄🗂️🎯🧪🏋️‍♂️📦🧾🤖🚀🏅🏗️📱📉⚡📊🤔📌📐]//g' "$md_file" | \
    # Convert only markdown file links to GitHub URLs (leave images and anchor links unchanged)
    sed 's|\](\([^#h)][^)]*\.md\))|\](https://github.com/brandon-benge/InterviewPrep/blob/main/\1)|g' > "$temp_file"
    
    # Convert with better formatting options and proper image handling
    pandoc "$temp_file" -o "$pdf_file" \
        --pdf-engine=xelatex \
        --variable geometry:margin=1in \
        --variable fontsize=11pt \
        --variable colorlinks=true \
        --toc \
        --resource-path="$md_dir" \
        2>/dev/null || {
        # Fallback to basic conversion if advanced options fail
        echo "⚠️  Advanced formatting failed, using basic conversion..."
        pandoc "$temp_file" -o "$pdf_file" --resource-path="$md_dir" 2>/dev/null
    }
    
    # Clean up temporary file
    rm "$temp_file"
done

echo "✅ All Markdown files converted to PDF."