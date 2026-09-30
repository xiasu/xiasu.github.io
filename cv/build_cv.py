#!/usr/bin/env python3
"""Build the public three-page CV from content.json using ReportLab.

Run: python3 cv/build_cv.py
Optional: python3 cv/build_cv.py --output /path/to/cv.pdf
Dependency: reportlab (pip install -r cv/requirements.txt)
"""
import argparse
import json
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 612, 792
LEFT, RIGHT = 45, 45
WIDTH = PAGE_W - LEFT - RIGHT
INK = colors.HexColor("#183033")
TEXT = colors.HexColor("#253235")
MUTED = colors.HexColor("#5A6C6D")
ACCENT = colors.HexColor("#147D78")
RULE = colors.HexColor("#CFDEDC")


def style(name, size=10, leading=13, color=TEXT, font="Helvetica", **kwargs):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading,
                          textColor=color, alignment=kwargs.pop("alignment", TA_LEFT), **kwargs)


STYLES = {
    "body": style("body", 10, 13.4),
    "small": style("small", 9.2, 12.0, MUTED),
    "role": style("role", 10.1, 13.0),
    "item": style("item", 10.4, 13.3, INK, "Helvetica-Bold"),
    "date": style("date", 9.1, 13.3, MUTED, alignment=TA_RIGHT),
    "pubtitle": style("pubtitle", 10.15, 12.5, INK, "Helvetica-Bold"),
    "authors": style("authors", 9.1, 11.7),
    "venue": style("venue", 8.8, 11.1, ACCENT),
    "compact": style("compact", 9.4, 12.3),
}


def link(text, url):
    return f'<a href="{escape(url, quote=True)}" color="#147D78">{escape(text)}</a>'


class CV:
    def __init__(self, output, data):
        self.data = data
        self.canvas = canvas.Canvas(str(output), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
        self.canvas.setTitle("Xia Su | Curriculum Vitae")
        self.canvas.setAuthor("Xia Su")
        self.canvas.setSubject("Computer vision, spatial AI, human-computer interaction, and accessibility")
        self.y = 0
        self.page = 0
        self.layout = []

    def para(self, text, kind="body", x=LEFT, width=WIDTH, gap=0):
        p = Paragraph(text, STYLES[kind])
        _, h = p.wrap(width, PAGE_H)
        if self.y - h < 46:
            raise ValueError(f"Page {self.page} overflow: {text[:90]!r} at y={self.y:.1f}")
        p.drawOn(self.canvas, x, self.y - h)
        self.y -= h + gap
        return h

    def pair(self, text, date, gap=0):
        start = self.y
        h = self.para(text, "item", width=WIDTH - 150)
        self.y = start
        dh = self.para(escape(date), "date", x=PAGE_W - RIGHT - 154, width=154)
        self.y = start - max(h, dh) - gap

    def section(self, text, gap_before=13):
        self.y -= gap_before
        self.canvas.setFont("Helvetica-Bold", 9.2)
        self.canvas.setFillColor(ACCENT)
        self.canvas.drawString(LEFT, self.y - 8, text.upper())
        self.canvas.setStrokeColor(RULE)
        self.canvas.setLineWidth(0.55)
        self.canvas.line(LEFT, self.y - 14, PAGE_W - RIGHT, self.y - 14)
        self.y -= 23

    def start_page(self, label):
        self.page += 1
        self.canvas.setFillColor(ACCENT)
        self.canvas.rect(LEFT, PAGE_H - 37, 26, 3, fill=1, stroke=0)
        self.canvas.setFillColor(MUTED)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 36, label.upper())
        self.y = PAGE_H - 51

    def finish_page(self):
        self.layout.append({"page": self.page, "content_bottom": round(self.y, 1)})
        self.canvas.setStrokeColor(RULE)
        self.canvas.setLineWidth(0.55)
        self.canvas.line(LEFT, 35, PAGE_W - RIGHT, 35)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.setFillColor(MUTED)
        self.canvas.drawString(LEFT, 22, "Xia Su  |  xiasu.github.io")
        self.canvas.drawRightString(PAGE_W - RIGHT, 22, f"{self.data['updated']}  /  {self.page}")
        self.canvas.showPage()

    def publication(self, p, gap=8.2):
        self.para(escape(p["title"]), "pubtitle", gap=1.0)
        authors = escape(p["authors"]).replace("Xia Su", "<b>Xia Su</b>")
        self.para(authors, "authors", gap=0.5)
        self.para(link(p["venue"], p["url"]), "venue", gap=gap)

    def build(self):
        d = self.data
        self.start_page("Curriculum vitae")
        self.canvas.setFillColor(INK)
        self.canvas.setFont("Times-Bold", 33)
        self.canvas.drawString(LEFT, self.y - 29, d["name"])
        self.y -= 40
        self.para(escape(d["tagline"]), "item", gap=8)
        self.para(" &nbsp; | &nbsp; ".join([
            link(d["email"], "mailto:" + d["email"]),
            link("xiasu.github.io", d["website"]),
            link("Google Scholar", d["scholar"]),
        ]), "small", gap=12)
        self.para(escape(d["profile"]), "body", gap=0)

        self.section("Experience", 13)
        for e in d["experience"]:
            self.pair(escape(e["organization"]), e["dates"])
            self.para(escape(e["role"]) + (" <font color='#5A6C6D'>| " + escape(e["focus"]) + "</font>" if e.get("focus") else ""), "role", gap=4 if e.get("bullets") else 7)
            for i, b in enumerate(e.get("bullets", [])):
                self.para("<font color='#147D78'>-</font> " + escape(b), "compact", x=LEFT + 5, width=WIDTH - 5, gap=3)
            if e.get("bullets"):
                self.y -= 5

        self.section("Education", 5)
        for e in d["education"]:
            self.pair(escape(e["institution"]), e["dates"], gap=1)
            self.para(e["detail"], "compact", gap=8)

        self.section("Technical expertise", 3)
        for label, detail in d["skills"]:
            self.para(f"<b>{escape(label)}.</b> {escape(detail)}", "compact", gap=5)
        self.finish_page()

        self.start_page("Xia Su / Research")
        self.section("Selected full papers", 0)
        for p in d["papers"]:
            self.publication(p)
        self.section("Selected posters & demos", 1)
        for p in d["posters"]:
            self.publication(p, gap=8.2)
        self.finish_page()

        self.start_page("Xia Su / Community & impact")
        self.section("Patents & inventions", 0)
        for p in d["patents"]:
            self.para(link(p["title"], p["url"]) if p.get("url") else escape(p["title"]), "item", gap=2)
            self.para(p["detail"].replace("Xia Su", "<b>Xia Su</b>"), "compact", gap=9)

        self.section("Academic service", 4)
        for line in d["service"]:
            self.para(escape(line), "compact", gap=4)

        self.section("Press & invited talks", 9)
        for t in d["talks"]:
            title = link(t["title"], t["url"]) if t.get("url") else escape(t["title"])
            self.para(title, "compact", gap=1)
            self.para(f"{escape(t['context'])} &nbsp; | &nbsp; {escape(t['date'])}", "small", gap=7)

        self.section("Teaching", 5)
        for line in d["teaching"]:
            self.para(escape(line), "compact", gap=4)

        self.section("Mentoring", 9)
        for line in d["mentoring"]:
            self.para(escape(line), "compact", gap=4)
        self.finish_page()
        self.canvas.save()
        return self.layout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT.parent / "assets" / "Xia_Su_CV_2026.pdf")
    args = parser.parse_args()
    data = json.loads((ROOT / "content.json").read_text())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    layout = CV(args.output, data).build()
    print(json.dumps({"output": str(args.output), "pages": layout}, indent=2))


if __name__ == "__main__":
    main()
