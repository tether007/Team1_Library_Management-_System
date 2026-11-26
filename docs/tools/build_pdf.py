"""Builds docs/Library_Management_System_Project_Guide.pdf.

Run (from the repository root):
    python docs/tools/diagrams.py     # redraw the diagrams (only needed when they change)
    python docs/tools/build_pdf.py    # build the PDF

Requires: reportlab, matplotlib, Pillow.
Code excerpts are read from the real source files, so rebuild after changing the code.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import part1_overview as p1  # noqa: E402
import part2_tools as p2  # noqa: E402
import part3_backend as p3  # noqa: E402
import part4_frontend as p4  # noqa: E402
import part5_quality as p5  # noqa: E402
from common import ROOT, GuideDoc  # noqa: E402

OUT = ROOT / "docs" / "Library_Management_System_Project_Guide.pdf"


def story():
    s = []
    s += p1.cover()
    s += p1.how_to_read()
    s += p1.overview()
    s += p1.requirements()
    s += p1.architecture()
    s += p2.libraries()
    s += p2.maven()
    s += p2.spring_concepts()
    s += p3.walkthrough()
    s += p3.api_reference()
    s += p3.security()
    s += p3.exception_handling()
    s += p3.collections()
    s += p4.overview()
    s += p4.redux()
    s += p4.axios_layer()
    s += p4.auth_ui()
    s += p4.paging_ui()
    s += p4.cache_ui()
    s += p4.ui_theme()
    s += p5.testing()
    s += p5.oop()
    s += p5.decisions()
    s += p5.sample_io()
    s += p5.limitations()
    s += p5.viva()
    s += p5.appendices()
    return s


def main():
    doc = GuideDoc(str(OUT), "Library Management System - Project Guide")
    doc.multiBuild(story())
    print("wrote", OUT, f"({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
