#!/usr/bin/env python3
"""(moved to scripts/pdf/) Convert Markdown files to PDF via pandoc."""

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
    try:
        subprocess.run(['pandoc', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def remove_emojis_and_convert_links(content):
    emoji_pattern = (
        r"[\U0001F300-\U0001F6FF]"
        r"|[\U0001F700-\U0001F77F]"
        r"|[\U0001F780-\U0001F7FF]"
        r"|[\U0001F800-\U0001F8FF]"
        r"|[\U0001F900-\U0001F9FF]"
        r"|[\U0001FA00-\U0001FAFF]"
        r"|[\U00002700-\U000027BF]"
        r"|[\U00002600-\U000026FF]"
    )
    try:
        content = re.sub(emoji_pattern, '', content)
    except re.error:
        content = re.sub(r'[🧠🔄🗂️🎯🧪🏋️📦🧾🤖🚀🏅🏗️📱📉⚡📊🤔📌📐]', '', content)
    link_pattern = r'\]\(([^#h)][^)]*\.md)\)'
    content = re.sub(link_pattern, r'](https://github.com/brandon-benge/InterviewPrep/blob/main/\1)', content)
    return content

def needs_update(md_file_path, pdf_file_path):
    md_file = Path(md_file_path)
    pdf_file = Path(pdf_file_path)
    if not pdf_file.exists():
        return True
    return md_file.stat().st_mtime > pdf_file.stat().st_mtime

def convert_markdown_to_pdf(md_file_path, pdf_dir, force=False):
    start_time = time.time()
    md_file = Path(md_file_path)
    pdf_file = pdf_dir / (md_file.stem + '.pdf')
    md_dir = md_file.parent
    if any(part == '.venv' for part in md_file.parts):
        return md_file, True, "Skipped (.venv directory)"
    if not force and not needs_update(md_file_path, pdf_file):
        elapsed = time.time() - start_time
        return md_file, True, f"Skipped (up-to-date) in {elapsed:.3f}s"
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return md_file, False, f"Could not read {md_file} as UTF-8"
    processed_content = remove_emojis_and_convert_links(content)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(processed_content)
        temp_file_path = temp_file.name
    try:
        advanced_cmd = [
            'pandoc', temp_file_path, '-o', str(pdf_file),
            '--pdf-engine=xelatex',
            '--variable', 'geometry:margin=1in',
            '--variable', 'fontsize=11pt',
            '-V', 'colorlinks=false',
            '-V', 'linkcolor=black',
            '-V', 'urlcolor=black',
            '-V', 'citecolor=black',
            '--toc',
            '--resource-path=' + str(md_dir)
        ]
        result = subprocess.run(advanced_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            basic_cmd = [
                'pandoc', temp_file_path, '-o', str(pdf_file),
                '--pdf-engine=xelatex',
                '--variable', 'geometry:margin=1in',
                '--variable', 'fontsize=11pt',
                '-V', 'colorlinks=false',
                '-V', 'linkcolor=black',
                '--resource-path=' + str(md_dir)
            ]
            result = subprocess.run(basic_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                minimal_cmd = ['pandoc', temp_file_path, '-o', str(pdf_file)]
                result = subprocess.run(minimal_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if result.returncode != 0:
                    return md_file, False, f"Failed to convert {md_file}"
        elapsed = time.time() - start_time
        return md_file, True, f"Converted in {elapsed:.2f}s"
    finally:
        os.unlink(temp_file_path)

def main(argv):
    ap = argparse.ArgumentParser(description='Convert Markdown to monochrome PDFs')
    ap.add_argument('--root', default='.')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--glob', default='*.md')
    args = ap.parse_args(argv)
    if not check_pandoc():
        print("❌ Error: pandoc is not installed. Please install it first:")
        print("   brew install pandoc  # macOS")
        print("   sudo apt-get install pandoc  # Ubuntu/Debian")
        return 1
    root = Path(args.root)
    pdf_dir = Path.cwd() / 'pdfs'
    pdf_dir.mkdir(parents=True, exist_ok=True)
    md_files = [
        md for md in root.rglob(args.glob)
        if (
            md.suffix.lower() == '.md'
            and not md.name.startswith('.')
            and not any(part == '.venv' for part in md.parts)
            and md.parent != root  # Exclude files in the base directory
        )
    ]
    if not md_files:
        print("No markdown files found.")
        return 0
    import multiprocessing
    max_workers = min(multiprocessing.cpu_count() * 2, len(md_files), 3)
    print(f"🚀 Starting conversion with {max_workers} parallel workers...")
    success_count = 0
    total_count = len(md_files)
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(convert_markdown_to_pdf, str(md), pdf_dir, args.force): md
            for md in md_files
        }
        for future in as_completed(future_to_file):
            md_file, success, message = future.result()
            if success:
                success_count += 1
                print(f"✅ {md_file} → {pdf_dir / (md_file.stem + '.pdf')} ({message})")
            else:
                print(f"❌ {md_file}: {message}")
    end_time = time.time()
    total_time = end_time - start_time
    avg_time_per_file = total_time / total_count if total_count > 0 else 0
    print(f"\n📊 Conversion Summary:")
    print(f"   ✅ Success: {success_count}/{total_count} files")
    print(f"   ⏱️  Total time: {total_time:.2f}s")
    print(f"   📈 Average: {avg_time_per_file:.2f}s per file")
    print(f"   🎯 Target met: {'Yes' if avg_time_per_file < 1.0 else 'No'} (sub-1 second target)")
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
