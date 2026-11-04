"""Deck primitives: fonts, hairlines, picture-filled shapes, vector mark."""
from pathlib import Path

from lxml import etree
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsdecls, qn
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"

# ── palette ────────────────────────────────────────────────────
INK       = RGBColor(0x1A, 0x2A, 0x22)
INK_SOFT  = RGBColor(0x55, 0x66, 0x5A)
JADE      = RGBColor(0x0E, 0x6B, 0x4F)
JADE_LT   = RGBColor(0x8F, 0xBB, 0xA8)
CREAM     = RGBColor(0xF6, 0xF1, 0xE5)
PAPER2    = RGBColor(0xEF, 0xE7, 0xD5)
WHITE     = RGBColor(0xFF, 0xFD, 0xF7)
DEEP      = RGBColor(0x0F, 0x23, 0x1B)
LINE      = RGBColor(0xD8, 0xCD, 0xB6)
LINE_DARK = RGBColor(0x3A, 0x4E, 0x43)
OCHRE     = RGBColor(0xA9, 0x6C, 0x2C)
BLUE      = RGBColor(0x3A, 0x58, 0x9E)
SALE_TEAL = RGBColor(0x2C, 0x7A, 0x5C)

SERIF = "Noto Serif SC"
SANS = "Noto Sans SC"

SLIDE_W, SLIDE_H = 13.333, 7.5
MARGIN = 0.9
CONTENT_W = SLIDE_W - 2 * MARGIN


# ── text helpers ───────────────────────────────────────────────
def _set_typefaces(run, name):
    """Set latin + east-asian + complex-script typefaces on one run."""
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", name)


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, wrap=True):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tf


def para(tf, first=False, align=PP_ALIGN.LEFT, space_before=0, space_after=0, line=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    if line:
        p.line_spacing = line
    return p


def run(p, text, size, color=INK, font=SANS, bold=False, italic=False,
        spacing=None, caps=False):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    _set_typefaces(r, font)
    if spacing is not None or caps:
        rPr = r._r.get_or_add_rPr()
        if spacing is not None:
            rPr.set("spc", str(int(spacing * 100)))
        if caps:
            rPr.set("cap", "all")
    return r


def text(slide, s, x, y, w, h, size, color=INK, font=SANS, bold=False,
         italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         spacing=None, caps=False, line=None):
    tf = textbox(slide, x, y, w, h, anchor=anchor)
    p = para(tf, first=True, align=align, line=line)
    run(p, s, size, color, font, bold, italic, spacing, caps)
    return tf


# ── drawing helpers ────────────────────────────────────────────
def _no_shadow(shape):
    """Drop the theme style (its effectRef paints a drop shadow) and add an
    explicit empty effect list so the shape renders flat in every renderer."""
    el = shape._element
    style = el.find(qn("p:style"))
    if style is not None:
        el.remove(style)
    spPr = getattr(el, "spPr", None)
    if spPr is not None and spPr.find(qn("a:effectLst")) is None:
        etree.SubElement(spPr, qn("a:effectLst"))


def rule(slide, x1, y1, x2, y2, color=LINE, width=0.75):
    """Hairline drawn as a filled bar — connectors with a zero dimension get
    stroked as open rectangles by some renderers, a bar never does."""
    t = width / 72.0
    if abs(y2 - y1) < 1e-6:
        return rect(slide, min(x1, x2), y1 - t / 2, abs(x2 - x1), t, fill=color)
    if abs(x2 - x1) < 1e-6:
        return rect(slide, x1 - t / 2, min(y1, y2), t, abs(y2 - y1), fill=color)
    raise ValueError("rule() only draws horizontal or vertical hairlines")


def rect(slide, x, y, w, h, fill=None, line_color=None, line_w=0.75,
         shape=MSO_SHAPE.RECTANGLE, radius=None, alpha=None):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if radius is not None:
        values = radius if isinstance(radius, (tuple, list)) else (radius,)
        for idx, val in enumerate(values):
            try:
                shp.adjustments[idx] = val
            except (IndexError, ValueError):
                pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
        if alpha is not None:
            _set_alpha(shp, alpha)
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(line_w)
    shp.text_frame.word_wrap = True
    _no_shadow(shp)
    return shp


def _set_alpha(shape, pct):
    """pct 0-100 opacity for a solid-filled shape."""
    srgb = shape.fill.fore_color._xFill.find(qn("a:srgbClr"))
    for old in srgb.findall(qn("a:alpha")):
        srgb.remove(old)
    alpha = etree.SubElement(srgb, qn("a:alpha"))
    alpha.set("val", str(int(pct * 1000)))


def cover_crop(img_w, img_h, frame_w, frame_h, anchor_y=0.5):
    """srcRect (l, t, r, b) as fractions for a cover fit."""
    img_ar, frame_ar = img_w / img_h, frame_w / frame_h
    if img_ar > frame_ar:
        keep = frame_ar / img_ar
        side = (1 - keep) / 2
        return side, 0.0, side, 0.0
    keep = img_ar / frame_ar
    excess = 1 - keep
    top = excess * anchor_y
    return 0.0, top, 0.0, excess - top


def picture_fill(slide, path, x, y, w, h, shape=MSO_SHAPE.RECTANGLE,
                 radius=None, anchor_y=0.5, line_color=None, line_w=0.75):
    """Place an image as the fill of a shape (keeps the shape's silhouette)."""
    from PIL import Image

    shp = rect(slide, x, y, w, h, fill=None, line_color=line_color, line_w=line_w,
               shape=shape, radius=radius)
    with Image.open(path) as im:
        iw, ih = im.size
    l, t, r, b = cover_crop(iw, ih, w, h, anchor_y)

    image_part, rId = slide.part.get_or_add_image_part(str(path))
    blip_fill = etree.fromstring(
        f'<a:blipFill {nsdecls("a", "r")} rotWithShape="1">'
        f'  <a:blip r:embed="{rId}"/>'
        f'  <a:srcRect l="{int(l * 100000)}" t="{int(t * 100000)}" '
        f'            r="{int(r * 100000)}" b="{int(b * 100000)}"/>'
        f'  <a:stretch><a:fillRect/></a:stretch>'
        f'</a:blipFill>'
    )
    spPr = shp._element.spPr
    for tag in ("a:solidFill", "a:noFill", "a:gradFill", "a:pattFill"):
        for el in spPr.findall(qn(tag)):
            spPr.remove(el)
    geom = spPr.find(qn("a:prstGeom"))
    geom.addnext(blip_fill)
    return shp


# ── the house mark as a native vector shape ────────────────────
# Path in a 24-unit box: two semicircular lobes joined at a crossing.
MARK_W, MARK_H = 23050, 11050
_MARK_SEGMENTS = [
    # (kind, ((x, y), ...)) in viewBox units
    ("M", ((12, 12),)),
    ("C", ((10, 9.33), (8, 8), (6, 8))),
    ("C", ((3.791, 8), (2, 9.791), (2, 12))),
    ("C", ((2, 14.209), (3.791, 16), (6, 16))),
    ("C", ((8, 16), (10, 14.67), (12, 12))),
    ("C", ((14, 14.67), (16, 16), (18, 16))),
    ("C", ((20.209, 16), (22, 14.209), (22, 12))),
    ("C", ((22, 9.791), (20.209, 8), (18, 8))),
    ("C", ((16, 8), (14, 9.33), (12, 12))),
]


def _pt(x, y):
    # viewBox -> path units, shifted so the stroked mark starts at 0,0
    return round(x * 1000 - 475), round(y * 1000 - 6475)


def add_mark(slide, x, y, width, color=JADE, stroke=3.05):
    """Vector infinity mark; returns (shape, inches_per_mark_unit)."""
    height = width * MARK_H / MARK_W
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                 Inches(width), Inches(height))
    shp.fill.background()
    shp.line.fill.background()

    body = []
    for kind, pts in _MARK_SEGMENTS:
        inner = "".join(
            f'<a:pt x="{_pt(px, py)[0]}" y="{_pt(px, py)[1]}"/>' for px, py in pts
        )
        tag = {"M": "a:moveTo", "C": "a:cubicBezTo"}[kind]
        body.append(f"<{tag}>{inner}</{tag}>")
    path_xml = "".join(body) + "<a:close/>"
    geom_xml = (
        f'<a:custGeom {nsdecls("a")}>'
        f'<a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/>'
        f'<a:rect l="0" t="0" r="r" b="b"/>'
        f'<a:pathLst><a:path w="{MARK_W}" h="{MARK_H}">{path_xml}</a:path></a:pathLst>'
        f'</a:custGeom>'
    )
    spPr = shp._element.spPr
    prst = spPr.find(qn("a:prstGeom"))
    prst.addprevious(etree.fromstring(geom_xml))
    spPr.remove(prst)
    _no_shadow(shp)

    scale = Inches(width) / MARK_W
    shp.line.color.rgb = color
    shp.line.width = Pt(stroke * 1000 * scale / 12700)
    # round caps/joins
    ln = spPr.find(qn("a:ln"))
    ln.set("cap", "rnd")
    for old in ln.findall(qn("a:round")):
        ln.remove(old)
    etree.SubElement(ln, qn("a:round"))

    return shp, scale


def add_mark_bars(slide, x, y, width, color=JADE,
                  plus_center=(6.0, 12.0), minus_center=(18.0, 12.0),
                  length=2.55, thickness=0.92):
    """The + and − that sit inside the lobes (viewBox coordinates)."""
    scale = Inches(width) / MARK_W
    x0, y0 = _pt(*plus_center)

    def to_in(px, py):
        return x + (px - x0 + x0) * scale / 914400, y + py * scale / 914400

    def bar(cx, cy, horizontal=True):
        px, py = _pt(cx, cy)
        bx = x + px * scale / 914400
        by = y + py * scale / 914400
        long_in = length * 1000 * scale / 914400
        thick_in = thickness * 1000 * scale / 914400
        if horizontal:
            left, top, w, h = bx - long_in / 2, by - thick_in / 2, long_in, thick_in
        else:
            left, top, w, h = bx - thick_in / 2, by - long_in / 2, thick_in, long_in
        rect(slide, left, top, w, h, fill=color,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)

    bar(*plus_center, True)
    bar(*plus_center, False)
    bar(*minus_center, True)
