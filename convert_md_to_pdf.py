#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile
import re
from pathlib import Path

def check_pandoc():
    """Check if pandoc is installed"""
    try:
        subprocess.run(['pandoc', '--version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def remove_emojis_and_convert_links(content):
    """Remove emojis and convert markdown links to GitHub URLs"""
    # Remove emojis for better PDF compatibility
    emoji_pattern = r'[🧠🔄🗂️🎯🧪🏋️‍♂️📦🧾🤖🚀🏅🏗️📱📉⚡📊🤔📌📐]'
    content = re.sub(emoji_pattern, '', content)
    
    # Convert only markdown file links to GitHub URLs (leave images and anchor links unchanged)
    link_pattern = r'\]\(([^#h)][^)]*\.md)\)'
    content = re.sub(link_pattern, r'](https://github.com/brandon-benge/InterviewPrep/blob/main/\1)', content)
    
    return content

def convert_markdown_to_pdf(md_file_path):
    """Convert a single markdown file to PDF"""
    md_file = Path(md_file_path)
    pdf_file = md_file.with_suffix('.pdf')
    md_dir = md_file.parent
    
    print(f"Converting: {md_file} → {pdf_file}")
    
    # Read and process the markdown content
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"⚠️  Warning: Could not read {md_file} as UTF-8, skipping...")
        return False
    
    # Process content
    processed_content = remove_emojis_and_convert_links(content)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(processed_content)
        temp_file_path = temp_file.name
    
    try:
        # Try advanced conversion first
        advanced_cmd = [
            'pandoc', temp_file_path, '-o', str(pdf_file),
            '--pdf-engine=xelatex',
            '--variable', 'geometry:margin=1in',
            '--variable', 'fontsize=11pt',
            '--variable', 'colorlinks=true',
            '--toc',
            '--resource-path=' + str(md_dir)
        ]
        
        result = subprocess.run(advanced_cmd, 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
        
        if result.returncode != 0:
            # Fallback to basic conversion
            print("⚠️  Advanced formatting failed, using basic conversion...")
            basic_cmd = [
                'pandoc', temp_file_path, '-o', str(pdf_file),
                '--resource-path=' + str(md_dir)
            ]
            
            result = subprocess.run(basic_cmd, 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
            
            if result.returncode != 0:
                print(f"❌ Failed to convert {md_file}")
                return False
        
        return True
        
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)

def main():
    """Main function to convert all markdown files to PDF"""
    
    # Check if pandoc is installed
    if not check_pandoc():
        print("❌ Error: pandoc is not installed. Please install it first:")
        print("   brew install pandoc  # macOS")
        print("   sudo apt-get install pandoc  # Ubuntu/Debian")
        sys.exit(1)
    
    # Find all .md files
    print("🔍 Finding Markdown files...")
    
    md_files = list(Path('.').rglob('*.md'))
    
    if not md_files:
        print("No markdown files found.")
        return
    
    # Convert each file
    success_count = 0
    total_count = len(md_files)
    
    for md_file in md_files:
        if convert_markdown_to_pdf(md_file):
            success_count += 1
    
    print(f"✅ Converted {success_count}/{total_count} Markdown files to PDF.")

if __name__ == "__main__":
    main()