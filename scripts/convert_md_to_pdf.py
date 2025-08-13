#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile
import re
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    """Remove emojis and convert markdown links to GitHub URLs.

    Expanded emoji removal to a broader unicode set to eliminate color glyphs in PDFs.
    """
    # Broad (still conservative) emoji pattern: common pictographs, symbols, transport, flags
    emoji_pattern = (
        r"[\U0001F300-\U0001F6FF]"  # Misc symbols & pictographs, transport & map
        r"|[\U0001F700-\U0001F77F]"  # Alchemical
        r"|[\U0001F780-\U0001F7FF]"  # Geometric extended
        r"|[\U0001F800-\U0001F8FF]"  # Supplemental arrows-C
        r"|[\U0001F900-\U0001F9FF]"  # Supplemental symbols & pictographs
        r"|[\U0001FA00-\U0001FAFF]"  # Chess etc.
        r"|[\U00002700-\U000027BF]"  # Dingbats
        r"|[\U00002600-\U000026FF]"  # Misc symbols
    )
    try:
        content = re.sub(emoji_pattern, '', content)
    except re.error:
        # Narrow fallback for environments without wide unicode
        content = re.sub(r'[🧠🔄🗂️🎯🧪🏋️📦🧾🤖🚀🏅🏗️📱📉⚡📊🤔📌📐]', '', content)
    
    # Convert only markdown file links to GitHub URLs (leave images and anchor links unchanged)
    link_pattern = r'\]\(([^#h)][^)]*\.md)\)'
    content = re.sub(link_pattern, r'](https://github.com/brandon-benge/InterviewPrep/blob/main/\1)', content)
    
    return content

def needs_update(md_file_path, pdf_file_path):
    """Check if PDF needs to be updated based on modification times"""
    md_file = Path(md_file_path)
    pdf_file = Path(pdf_file_path)
    
    # If PDF doesn't exist, we need to create it
    if not pdf_file.exists():
        return True
    
    # If MD file is newer than PDF, we need to update
    return md_file.stat().st_mtime > pdf_file.stat().st_mtime

def convert_markdown_to_pdf(md_file_path, force=False):
    """Convert a single markdown file to PDF"""
    start_time = time.time()
    md_file = Path(md_file_path)
    pdf_file = md_file.with_suffix('.pdf')
    md_dir = md_file.parent
    
    # Check if update is needed
    if not force and not needs_update(md_file_path, pdf_file):
        elapsed = time.time() - start_time
        return md_file, True, f"Skipped (up-to-date) in {elapsed:.3f}s"
    
    # Read and process the markdown content
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return md_file, False, f"Could not read {md_file} as UTF-8"
    
    # Process content
    processed_content = remove_emojis_and_convert_links(content)
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(processed_content)
        temp_file_path = temp_file.name
    
    try:
        # Try advanced conversion with full formatting options
        advanced_cmd = [
            'pandoc', temp_file_path, '-o', str(pdf_file),
            '--pdf-engine=xelatex',
            '--variable', 'geometry:margin=1in',
            '--variable', 'fontsize=11pt',
            # Force monochrome link styling (no colors)
            '-V', 'colorlinks=false',
            '-V', 'linkcolor=black',
            '-V', 'urlcolor=black',
            '-V', 'citecolor=black',
            '--toc',
            '--resource-path=' + str(md_dir)
        ]
        
        result = subprocess.run(advanced_cmd, 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
        
        if result.returncode != 0:
            # Fallback to basic conversion without TOC/colorlinks
            basic_cmd = [
                'pandoc', temp_file_path, '-o', str(pdf_file),
                '--pdf-engine=xelatex',
                '--variable', 'geometry:margin=1in',
                '--variable', 'fontsize=11pt',
                '-V', 'colorlinks=false',
                '-V', 'linkcolor=black',
                '--resource-path=' + str(md_dir)
            ]
            result = subprocess.run(basic_cmd, 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
            
            if result.returncode != 0:
                # Final fallback to minimal conversion
                minimal_cmd = ['pandoc', temp_file_path, '-o', str(pdf_file)]
                result = subprocess.run(minimal_cmd, 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.DEVNULL)
                
                if result.returncode != 0:
                    return md_file, False, f"Failed to convert {md_file}"
        
        elapsed = time.time() - start_time
        return md_file, True, f"Converted in {elapsed:.2f}s"
        
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)

def main():
    """Main function to convert all markdown files to PDF"""
    parser = argparse.ArgumentParser(description='Convert Markdown to monochrome PDFs')
    parser.add_argument('--force', action='store_true', help='Force regeneration of all PDFs')
    args = parser.parse_args()
    
    # Check if pandoc is installed
    if not check_pandoc():
        print("❌ Error: pandoc is not installed. Please install it first:")
        print("   brew install pandoc  # macOS")
        print("   sudo apt-get install pandoc  # Ubuntu/Debian")
        sys.exit(1)
    
    # Find all .md files
    print("🔍 Finding Markdown files...")
    start_time = time.time()
    
    md_files = list(Path('.').rglob('*.md'))
    
    if not md_files:
        print("No markdown files found.")
        return
    
    print(f"📄 Found {len(md_files)} markdown files")
    
    # Determine optimal number of workers based on CPU count and target speed
    import multiprocessing
    max_workers = min(multiprocessing.cpu_count() * 2, len(md_files), 3)  # Cap at 3 for memory
    
    print(f"🚀 Starting conversion with {max_workers} parallel workers...")
    
    # Convert files in parallel
    success_count = 0
    total_count = len(md_files)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all jobs
        future_to_file = {
            executor.submit(convert_markdown_to_pdf, md_file, args.force): md_file 
            for md_file in md_files
        }
        
        # Process completed jobs
        for future in as_completed(future_to_file):
            md_file, success, message = future.result()
            
            if success:
                success_count += 1
                print(f"✅ {md_file} → {md_file.with_suffix('.pdf')} ({message})")
            else:
                print(f"❌ {md_file}: {message}")
    
    total_time = time.time() - start_time
    avg_time_per_file = total_time / total_count if total_count > 0 else 0
    
    print(f"\n📊 Conversion Summary:")
    print(f"   ✅ Success: {success_count}/{total_count} files")
    print(f"   ⏱️  Total time: {total_time:.2f}s")
    print(f"   📈 Average: {avg_time_per_file:.2f}s per file")
    print(f"   🎯 Target met: {'Yes' if avg_time_per_file < 1.0 else 'No'} (sub-1 second target)")

if __name__ == "__main__":
    main()
