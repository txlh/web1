"""Inspect the source deck: slide size, text, images, fonts."""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

SRC = Path(r"D:\tp\Campus_Plant_Corner_校园绿植小站.pptx")
OUT = Path(r"D:\deepseek2\tools\deck-report.txt")


def main() -> None:
    prs = Presentation(str(SRC))
    lines = []
    w = lambda v: (v / 914400) if v is not None else -1
    lines.append("size: %.2f x %.2f in" % (prs.slide_width / 914400, prs.slide_height / 914400))
    lines.append("slides: %d" % len(prs.slides))
    for i, slide in enumerate(prs.slides, 1):
        lines.append(f"--- slide {i} (layout={slide.slide_layout.name})")
        for sh in slide.shapes:
            pos = "(%5.2f,%5.2f) %5.2fx%5.2f" % (w(sh.left), w(sh.top), w(sh.width), w(sh.height))
            lines.append(f"  {str(sh.shape_type):18s} {pos}  {sh.name!r}")
            if sh.has_text_frame and sh.text_frame.text.strip():
                lines.append("      text: " + sh.text_frame.text.replace("\n", " / ")[:160])
            for p in sh.text_frame.paragraphs if sh.has_text_frame else []:
                for r in p.runs:
                    if r.font.size:
                        lines.append(
                            f"      run: {r.text[:20]!r} size={r.font.size.pt} font={r.font.name} bold={r.font.bold}"
                        )
                        break
            if sh.shape_type == 13:
                lines.append(f"      image: {sh.image.content_type} {sh.image.size}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("written", OUT, len(lines), "lines")


if __name__ == "__main__":
    main()
