"""Build the site imagery from the supplied 幻灯片 deck.

Run:  python tools/crop_assets.py
All crops are expressed as fractions of the source slide, so the deck can be
re-exported at a different size without breaking the coordinates.
"""
from pathlib import Path

from PIL import Image, ImageChops

SRC = Path(r"D:\tp\Campus_Plant_Corner_校园绿植小站")
OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)


def trim_white(im: Image.Image, tol: int = 8) -> Image.Image:
    """Crop away a near-uniform white slide margin."""
    rgb = im.convert("RGB")
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, (255, 255, 255)))
    box = diff.convert("L").point(lambda p: 255 if p > tol else 0).getbbox()
    return im.crop(box) if box else im


def crop_fraction(im: Image.Image, box: tuple) -> Image.Image:
    l, t, r, b = box
    w, h = im.size
    return im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))


def crop_aspect(im: Image.Image, aspect: float, anchor_y: float = 0.5) -> Image.Image:
    cw, ch = im.size
    if cw / ch > aspect:
        nw = int(ch * aspect)
        off = (cw - nw) // 2
        return im.crop((off, 0, off + nw, ch))
    nh = int(cw / aspect)
    off = int((ch - nh) * anchor_y)
    return im.crop((0, off, cw, off + nh))


def save(im: Image.Image, name: str, max_edge: int = 1600) -> None:
    if max(im.size) > max_edge:
        s = max_edge / max(im.size)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    dest = OUT / f"{name}.jpg"
    im.convert("RGB").save(dest, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"{dest.name:26s} {im.size[0]:>4}x{im.size[1]:<4} {dest.stat().st_size // 1024:>4} KB")


slide1 = Image.open(SRC / "幻灯片1.JPG").convert("RGB")
slide3 = Image.open(SRC / "幻灯片3.JPG").convert("RGB")
slide4 = Image.open(SRC / "幻灯片4.JPG").convert("RGB")
slide6 = Image.open(SRC / "幻灯片6.JPG").convert("RGB")

# The clean studio photo of hands holding the planter lives on slide 3
# (slide 1 has the title burned in), trim the white margin around it.
photo = trim_white(crop_fraction(slide3, (0.52, 0.30, 0.96, 0.85)))
save(photo, "hands-photo", max_edge=1500)
save(crop_aspect(photo, 4 / 5, anchor_y=0.45), "hero-plant")

# Products: two frames already have a photo, the succulent card is a tighter
# window into the same studio photo so all three cards share one light.
save(crop_aspect(photo.crop((int(photo.width * 0.10), 0,
                             int(photo.width * 0.92), int(photo.height * 0.80))),
                 4 / 5, anchor_y=0.55), "products-succulents")
save(crop_aspect(crop_fraction(slide4, (0.363, 0.255, 0.637, 0.855)), 4 / 5), "products-pothos")
save(crop_aspect(crop_fraction(slide4, (0.652, 0.255, 0.926, 0.855)), 4 / 5), "products-pots")

save(crop_fraction(slide6, (0.066, 0.360, 0.452, 0.812)), "forest")
