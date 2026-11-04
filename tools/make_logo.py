"""Render the house mark (infinity + / -) to transparent PNGs for the deck.

The mark is a stroked Gerono lemniscate -- x = a·cos t, y = b·sin t·cos t --
which gives the same fat ribbon with a pointed crossing as the site's SVG.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
INK = (26, 42, 34, 255)
CREAM = (246, 241, 229, 255)
JADE = (14, 107, 79, 255)

SS = 4          # supersampling
W, H = 1600, 800
A, B = 1.0, 1.0
BAND = 0.30     # stroke width in path units


def lemniscate(n: int = 720):
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        pts.append((A * math.cos(t), B * math.sin(t) * math.cos(t)))
    return pts


def render(color) -> Image.Image:
    img = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # path units -> pixels: x spans -1.08..1.08 across W
    scale = (W * SS) / 2.16
    cx, cy = W * SS / 2, H * SS / 2
    to_px = lambda p: (cx + p[0] * scale, cy - p[1] * scale)

    pts = [to_px(p) for p in lemniscate()]
    lw = int(BAND * scale)
    d.line(pts, fill=color, width=lw, joint="curve")
    # round the two ends of the closed loop at t=0/2pi (same point) and the tips
    r = lw / 2
    for p in (pts[0],):
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)

    # plus / minus inside the lobes
    def bar(x0, y0, x1, y1, w=0.085):
        p0, p1 = to_px((x0, y0)), to_px((x1, y1))
        d.line([p0, p1], fill=color, width=int(w * scale))
        for p in (p0, p1):
            rr = w * scale / 2
            d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=color)

    bar(-0.70, 0, -0.44, 0)         # minus on the left lobe? no: plus needs two bars
    bar(-0.57, -0.13, -0.57, 0.13)  # vertical of the plus
    bar(-0.70, 0, -0.44, 0)         # horizontal of the plus (drawn twice is harmless)
    bar(0.44, 0, 0.70, 0)           # minus on the right lobe

    return img.resize((W, H), Image.LANCZOS)


def main() -> None:
    for name, color in (("mark-ink", INK), ("mark-cream", CREAM), ("mark-jade", JADE)):
        im = render(color)
        p = OUT / f"{name}.png"
        im.save(p)
        print(name, im.size, p.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
