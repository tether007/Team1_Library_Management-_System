"""Shared styles and helpers for building the project guide PDF with reportlab.

Text helpers accept light markup:  **bold**  and  `inline code`.  Everything else is escaped,
so '<' and '&' can be typed freely. Keep text ASCII (the built-in PDF fonts are Latin-1).
"""
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[2]
IMAGES = ROOT / "docs" / "images"
PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

BLACK = colors.black
YELLOW = colors.HexColor("#fff6c2")
GREEN = colors.HexColor("#d9f2d9")
RED = colors.HexColor("#f8d7d7")
PAPER = colors.HexColor("#f4f4f0")
BLUE = colors.HexColor("#dbe8f7")

_base = getSampleStyleSheet()
BODY = ParagraphStyle("Body", parent=_base["BodyText"], fontName="Helvetica", fontSize=9.6, leading=13.6, spaceAfter=5, alignment=TA_LEFT)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.2, leading=10.8, spaceAfter=0)
CELL = ParagraphStyle("Cell", parent=BODY, fontSize=8.2, leading=10.6, spaceAfter=0)
CELL_B = ParagraphStyle("CellB", parent=CELL, fontName="Helvetica-Bold")
BULLET = ParagraphStyle("Bullet", parent=BODY, leftIndent=14, bulletIndent=4, spaceAfter=2.5)
H1 = ParagraphStyle("H1", parent=BODY, fontName="Helvetica-Bold", fontSize=19, leading=23, spaceBefore=0, spaceAfter=10, textColor=BLACK)
H2 = ParagraphStyle("H2", parent=BODY, fontName="Helvetica-Bold", fontSize=13, leading=16, spaceBefore=12, spaceAfter=5, textColor=BLACK)
H3 = ParagraphStyle("H3", parent=BODY, fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=8, spaceAfter=3)
CAPTION = ParagraphStyle("Caption", parent=BODY, fontName="Helvetica-Oblique", fontSize=8.2, leading=10.5, alignment=1, spaceAfter=8)
CODE = ParagraphStyle("Code", fontName="Courier", fontSize=7.1, leading=8.7, backColor=PAPER, borderColor=BLACK,
                      borderWidth=0.5, borderPadding=4, leftIndent=4, rightIndent=4, spaceBefore=3, spaceAfter=9)
FILE_LABEL = ParagraphStyle("FileLabel", parent=BODY, fontName="Courier-Bold", fontSize=7.6, leading=9.5, spaceBefore=4, spaceAfter=0)

_UNICODE = {"\u2013": "-", "\u2014": "-", "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u2192": "->", "\u00a0": " "}


def fmt(text):
    """Escape and apply **bold** / `code` markup."""
    for k, v in _UNICODE.items():
        text = text.replace(k, v)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r'<font face="Courier" size="8.4">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


# ----------------------------------------------------------------- flowable builders
def h1(text, page_break=True):
    out = [PageBreak()] if page_break else []
    out.append(Paragraph(fmt(text), H1))
    return out


def h2(text):
    return [Paragraph(fmt(text), H2)]


def h3(text):
    return [Paragraph(fmt(text), H3)]


def p(text):
    return [Paragraph(fmt(text), BODY)]


def bullets(items, style=BULLET):
    return [Paragraph(fmt(i), style, bulletText="-") for i in items]


def numbered(items):
    return [Paragraph(fmt(t), BULLET, bulletText=f"{i}.") for i, t in enumerate(items, 1)]


def spacer(h=6):
    return [Spacer(1, h)]


def code(text, label=None):
    out = []
    if label:
        out.append(Paragraph(fmt(label), FILE_LABEL))
    import textwrap
    lines = []
    for line in text.rstrip("\n").expandtabs(4).splitlines():
        if len(line) > 106:
            indent = line[: len(line) - len(line.lstrip())]
            lines += textwrap.wrap(line, 106, subsequent_indent=indent + "    ", break_long_words=False, break_on_hyphens=False) or [line]
        else:
            lines.append(line)
    out.append(Preformatted("\n".join(lines), CODE))
    return out


def snip(rel, start, end=None, max_lines=45, label=True, skip=0):
    """Excerpt of a real source file: from the first line containing `start` to the first later line
    containing `end` (inclusive), or `max_lines` lines. Keeps the guide in sync with the code."""
    path = ROOT / rel
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        i = next(n for n, l in enumerate(lines) if start in l) + skip
    except StopIteration:
        raise SystemExit(f"snippet start not found in {rel}: {start!r}")
    j = min(len(lines), i + max_lines)
    if end:
        for n in range(i, min(len(lines), i + max_lines)):
            if end in lines[n]:
                j = n + 1
                break
    body = "\n".join(l.rstrip() for l in lines[i:j])
    return code(body, rel.replace("\\", "/") if label else None)


def table(rows, widths, header=True, zebra=True, small=False, head_bg=YELLOW, col_bold0=False):
    """rows: list of lists of strings. widths: relative numbers or points."""
    total = sum(widths)
    cw = [CONTENT_W * w / total for w in widths]
    st = CELL if not small else SMALL
    data = []
    for r, row in enumerate(rows):
        cells = []
        for c, cell in enumerate(row):
            style = CELL_B if (header and r == 0) or (col_bold0 and c == 0) else st
            cells.append(Paragraph(fmt(str(cell)).replace("\n", "<br/>"), style))
        data.append(cells)
    t = Table(data, colWidths=cw, repeatRows=1 if header else 0)
    ts = [("GRID", (0, 0), (-1, -1), 0.6, BLACK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        ts.append(("BACKGROUND", (0, 0), (-1, 0), head_bg))
    if zebra:
        for r in range(1 if header else 0, len(rows)):
            if r % 2 == 0:
                ts.append(("BACKGROUND", (0, r), (-1, r), PAPER))
    t.setStyle(TableStyle(ts))
    return [t, Spacer(1, 8)]


def callout(text, kind="note"):
    bg = {"note": YELLOW, "warn": RED, "ok": GREEN, "info": BLUE}[kind]
    title = {"note": "NOTE", "warn": "LIMITATION", "ok": "TIP", "info": "REMEMBER"}[kind]
    para = Paragraph(f"<b>{title}.</b> " + fmt(text), CELL)
    t = Table([[para]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.0, BLACK), ("BACKGROUND", (0, 0), (-1, -1), bg),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return [t, Spacer(1, 8)]


def qa(question, answer):
    q = Paragraph("<b>Q. " + fmt(question) + "</b>", BODY)
    a = Paragraph(fmt(answer), BODY)
    return [KeepTogether([q, a, Spacer(1, 3)])]


def fig(name, caption, max_h=215 * mm, width=None):
    path = IMAGES / name
    if not path.exists():
        return [Paragraph(f"[missing image {name}]", BODY)]
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        w, h = im.size
    target_w = width or CONTENT_W
    scale = min(target_w / w, max_h / h)
    img = Image(str(path), width=w * scale, height=h * scale)
    img.hAlign = "CENTER"
    return [KeepTogether([img, Paragraph(fmt(caption), CAPTION)])]


def screenshot(name, caption, note="Paste the screenshot here"):
    """Real screenshot docs/images/<name> when present, otherwise a labelled empty frame to paste into."""
    path = IMAGES / name
    if path.exists():
        return fig(name, caption, max_h=150 * mm)
    box = Table([[Paragraph(f"<b>{fmt(note)}</b><br/>({fmt(name)})", CELL)]], colWidths=[CONTENT_W * 0.85], rowHeights=[70 * mm])
    box.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.2, BLACK), ("BACKGROUND", (0, 0), (-1, -1), PAPER),
                             ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    box.hAlign = "CENTER"
    return [KeepTogether([box, Paragraph(fmt(caption), CAPTION)])]


# ----------------------------------------------------------------- document
class GuideDoc(BaseDocTemplate):
    def __init__(self, filename, title):
        super().__init__(filename, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=20 * mm, bottomMargin=18 * mm,
                         title=title, author="Team 1", subject="Library Management System project guide")
        frame = Frame(MARGIN, 18 * mm, CONTENT_W, PAGE_H - 38 * mm, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="first", frames=[frame], onPage=self._cover),
                               PageTemplate(id="rest", frames=[frame], onPage=self._page)])
        self._n = 0

    def _cover(self, canv, doc):
        pass

    def _page(self, canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 8)
        canv.line(MARGIN, PAGE_H - 14 * mm, PAGE_W - MARGIN, PAGE_H - 14 * mm)
        canv.drawString(MARGIN, PAGE_H - 12 * mm, "Library Management System - Project Guide")
        canv.drawRightString(PAGE_W - MARGIN, PAGE_H - 12 * mm, "Team 1")
        canv.line(MARGIN, 14 * mm, PAGE_W - MARGIN, 14 * mm)
        canv.drawCentredString(PAGE_W / 2, 9.5 * mm, f"Page {doc.page}")
        canv.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            if style in ("H1", "H2"):
                text = flowable.getPlainText()
                key = "h_" + re.sub(r"\W+", "_", text)[:60]
                self.canv.bookmarkPage(key)
                level = 0 if style == "H1" else 1
                self.canv.addOutlineEntry(text, key, level=level, closed=level == 0)
                self.notify("TOCEntry", (level, text, self.page, key))


def make_toc():
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC0", fontName="Helvetica-Bold", fontSize=10, leading=14, leftIndent=0, spaceBefore=4),
        ParagraphStyle("TOC1", fontName="Helvetica", fontSize=8.6, leading=11.5, leftIndent=14),
    ]
    return toc
