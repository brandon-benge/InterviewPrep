# PDF Generation Guide

This repository includes automated PDF generation for all markdown files using a Python-based workflow.

---
## 🔄 Automated Generation
- **GitHub Actions**: PDFs are automatically generated and uploaded as artifacts on every push.
- **Incremental**: Only changed Markdown files are rebuilt locally by the Python driver.
- **Enhanced Processing**: Emoji removal and relative-to-GitHub link conversion for clean PDFs.

## 🛠️ Manual Local Generation
Ensure you have the required dependencies (macOS examples):
```bash
# Install pandoc
brew install pandoc

# Install LaTeX distribution (large)
brew install --cask mactex

# Generate PDFs (incremental)
./scripts/run_venv.sh scripts/convert_md_to_pdf.py
```
Artifacts are written alongside each source markdown (e.g. `system-design-approach.md` -> `system-design-approach.pdf`).

## ✨ Features
- Cross-platform Python script (falls back gracefully when tools missing).
- Automatic emoji stripping for LaTeX compatibility.
- Relative links rewritten to absolute GitHub URLs so PDFs are navigable.
- Local images preserved.
- UTF-8 safe.

## 🧪 Quick Sanity Check
Regenerate a single file by touching it:
```bash
touch system-design/system-design-approach.md
./scripts/run_venv.sh scripts/convert_md_to_pdf.py
```

## ❓ Troubleshooting
| Issue | Cause | Fix |
|-------|-------|-----|
| Missing `pandoc` | Not installed | `brew install pandoc` |
| LaTeX errors on symbols | Unescaped emoji / unicode | Script strips most emoji; open an issue if missed |
| PDF not updated | File timestamp older | `touch <file>.md` or edit file |

## 🧩 Internals (Brief)
`convert_md_to_pdf.py` scans repo for `.md` files, hashes content to skip unchanged, parallelizes pandoc conversions, and writes PDFs adjacent to sources.

---
Return to main README: [README.md](./README.md)
