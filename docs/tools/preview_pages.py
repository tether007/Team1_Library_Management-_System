"""Renders pages of the guide PDF to PNG for a quick visual check.

Usage: python docs/tools/preview_pages.py [first_page last_page] [dpi]
Pictures go to %TEMP%/guide_pages. Requires PyMuPDF (pip install pymupdf).
"""
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
import fitz  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
pdf = fitz.open(ROOT / "docs" / "Library_Management_System_Project_Guide.pdf")
out = Path(os.environ.get("TEMP", ".")) / "guide_pages"
out.mkdir(exist_ok=True)

first = int(sys.argv[1]) if len(sys.argv) > 1 else 1
last = int(sys.argv[2]) if len(sys.argv) > 2 else len(pdf)
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 70
print("pages:", len(pdf))
for i in range(first - 1, min(last, len(pdf))):
    pdf[i].get_pixmap(dpi=dpi).save(out / f"p{i + 1:02d}.png")
print("chapters:")
for level, title, page in pdf.get_toc():
    if level == 1:
        print(f"  p{page}: {title}")
print("output folder:", out)
