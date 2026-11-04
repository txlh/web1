"""Build the redesigned Campus Plant Corner deck (bilingual, 16:9)."""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deck_lib import (  # noqa: E402
    BLUE, CREAM, DEEP, IMG, INK, INK_SOFT, JADE, JADE_LT, LINE, LINE_DARK, OCHRE,
    PAPER2, SALE_TEAL, SANS, SERIF, SLIDE_H, SLIDE_W, WHITE,
    add_mark, add_mark_bars, para, picture_fill, rect, rule, run, text, textbox,
)

OUT = Path(r"D:\deepseek2\Campus_Plant_Corner_校园绿植小店_新版.pptx")
TOTAL = 7


# ── shared chrome ──────────────────────────────────────────────
def background(slide, color=CREAM):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def header(slide, num, cn, en, dark=False):
    ink = CREAM if dark else INK
    soft = JADE_LT if dark else INK_SOFT
    text(slide, num, 0.9, 0.66, 0.6, 0.3, 10.5, soft, SERIF, spacing=1.2)
    tf = textbox(slide, 1.44, 0.55, 10.6, 0.55)
    p = para(tf, first=True)
    run(p, cn, 25, ink, SERIF, spacing=0.6)
    run(p, "   " + en, 15, soft, SERIF, italic=True, spacing=0.4)
    rule(slide, 0.9, 1.34, SLIDE_W - 0.9, 1.34, LINE_DARK if dark else LINE)


def footer(slide, page, dark=False):
    soft = RGBColor(0x8C, 0x9E, 0x91) if dark else INK_SOFT
    text(slide, "Campus Plant Corner · 校园绿植小店", 0.9, 7.04, 6.0, 0.24, 7.5,
         soft, SANS, spacing=1.0)
    text(slide, f"{page:02d} / {TOTAL:02d}", 11.03, 7.04, 1.4, 0.24, 7.5,
         soft, SERIF, align=PP_ALIGN.RIGHT)


def rule_row(slide, y, x1=0.9, x2=SLIDE_W - 0.9, color=LINE):
    rule(slide, x1, y, x2, y, color)


# ── slide 1 · cover ────────────────────────────────────────────
def cover(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s)

    # eyebrow
    tf = textbox(s, 0.9, 1.36, 6.4, 0.3)
    p = para(tf, first=True)
    run(p, "●  ", 9, JADE, SANS, spacing=0)
    run(p, "CAMPUS PLANT CORNER", 9, INK_SOFT, SANS, spacing=3.0)
    run(p, "  ·  校园绿植小店  ·  EST. 2026", 9, INK_SOFT, SANS, spacing=1.6)

    # title
    tf = textbox(s, 0.86, 1.72, 6.6, 2.2)
    p = para(tf, first=True, line=1.02)
    run(p, "小植物，", 62, INK, SERIF, spacing=1.0)
    p = para(tf, line=1.02)
    run(p, "大爱心。", 62, JADE, SERIF, spacing=1.0)

    text(s, "( small plants, big love )", 0.9, 3.88, 6.0, 0.4, 19, JADE_LT, SERIF,
         italic=True)

    tf = textbox(s, 0.9, 4.48, 5.1, 0.9)
    p = para(tf, first=True, line=1.75)
    run(p, "我们把多肉、绿萝和手作花盆搬到校园的角落。你负责喜欢——浇水、换土、"
           "放假托管，都可以交给我们。", 11.5, INK_SOFT, SANS)

    tf = textbox(s, 0.9, 5.28, 5.2, 0.9)
    p = para(tf, first=True, line=1.5)
    run(p, "We bring succulents, pothos and hand-thrown pots to a corner of campus. "
           "You do the loving — watering, repotting and holiday boarding can be ours.",
        9, INK_SOFT, SERIF, italic=True)

    # photo
    picture_fill(s, IMG / "hero-plant.jpg", 7.42, 0.66, 4.55, 5.42,
                 shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE, radius=(0.5, 0.0),
                 anchor_y=0.42, line_color=RGBColor(0xE3, 0xD8, 0xC2), line_w=1.0)
    text(s, "No.01 · 多肉拼盆 · ¥28", 7.42, 6.2, 4.55, 0.25, 8.5, INK_SOFT, SERIF,
         italic=True, align=PP_ALIGN.CENTER)

    rule_row(s, 6.62)
    text(s, "2026.11.01", 0.9, 6.76, 2.0, 0.25, 9, INK, SERIF, spacing=1.2)
    text(s, "每周三 / 周五 12:00  ·  A 座教学楼门口", 3.1, 6.76, 5.4, 0.25, 9,
         INK_SOFT, SANS)
    text(s, "hello@campusplantcorner.cn", 9.2, 6.76, 3.23, 0.25, 9, INK_SOFT, SANS,
         align=PP_ALIGN.RIGHT)
    return s


# ── slide 2 · about ────────────────────────────────────────────
def about(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s)
    header(s, "01", "关于我们", "About Us")

    rows = [
        ("01", "我们卖小盆栽。", "We sell small plants.",
         "多肉、绿萝、小陶盆，都摆在一条长桌上。没有大盆栽，因为宿舍的窗台只有那么宽。",
         "Succulents, pothos and small ceramic pots, all on one long table. "
         "Nothing large — a dorm windowsill is only so wide."),
        ("02", "我们帮学生养植物。", "We help students care for plants.",
         "买走的那天起，它还在我们名单上。每周一条浇水提醒，黄叶了拍张照就行，放假可以寄养在店里。",
         "From the day you take it home, it stays on our list. One reminder a week, "
         "a photo away when a leaf yellows, and boarding at the shop over the holidays."),
    ]

    y = 1.86
    for i, (num, cn, en, body_cn, body_en) in enumerate(rows):
        text(s, num, 0.9, y + 0.08, 0.5, 0.25, 10, JADE, SERIF, spacing=1.2)
        tf = textbox(s, 1.5, y, 5.5, 0.9)
        p = para(tf, first=True, line=1.15)
        run(p, cn, 21, INK, SERIF, spacing=0.4)
        p = para(tf, line=1.1)
        run(p, en, 11.5, INK_SOFT, SERIF, italic=True)

        tf = textbox(s, 1.5, y + 0.92, 5.0, 0.8)
        p = para(tf, first=True, line=1.65)
        run(p, body_cn, 10, INK_SOFT, SANS)
        p = para(tf, space_before=5, line=1.45)
        run(p, body_en, 8.6, INK_SOFT, SERIF, italic=True)

        if i == 0:
            rule_row(s, y + 2.02, 0.9, 7.05)
            y += 2.26
        else:
            y += 2.26

    # photo
    picture_fill(s, IMG / "hands-photo.jpg", 7.5, 1.86, 4.93, 3.86,
                 anchor_y=0.45, line_color=RGBColor(0xE3, 0xD8, 0xC2), line_w=1.0)
    text(s, "第一次出摊 · 周三中午 · 卖出 11 盆", 7.5, 5.8, 4.93, 0.24, 8.5,
         INK_SOFT, SERIF, italic=True, align=PP_ALIGN.CENTER)

    # quiet stat line along the bottom
    rule_row(s, 6.22)
    tf = textbox(s, 0.9, 6.38, 11.53, 0.3)
    p = para(tf, first=True)
    run(p, "1,240", 10.5, JADE, SERIF, spacing=0.5)
    run(p, " 盆植物找到了新主人", 9, INK_SOFT, SANS)
    run(p, "    ·    ", 9, RGBColor(0xB5, 0xA8, 0x8E), SANS)
    run(p, "32", 10.5, JADE, SERIF, spacing=0.5)
    run(p, " 位同学在养护群里", 9, INK_SOFT, SANS)
    run(p, "    ·    ", 9, RGBColor(0xB5, 0xA8, 0x8E), SANS)
    run(p, "14", 10.5, JADE, SERIF, spacing=0.5)
    run(p, " 次免费换盆换土", 9, INK_SOFT, SANS)
    return s


# ── slide 3 · products ─────────────────────────────────────────
def products(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s)
    header(s, "02", "我们的产品", "Our Products")

    items = [
        ("products-succulents.jpg", "¥15 起", "from ¥15", "多肉", "Succulents",
         "两周浇一次也不会死。适合总是忘记浇水的人。",
         "Happy with a drink every two weeks — built for people who forget."),
        ("products-pothos.jpg", "¥18 起", "from ¥18", "绿萝", "Green Radish",
         "长得快，扦插一截就能再活一盆。宿舍北窗也能过。",
         "Grows fast — one cutting becomes another pot. Tolerates a north window."),
        ("products-pots.jpg", "¥25 起", "from ¥25", "花盆", "Flower Pots",
         "手工捏的陶盆，每只都不一样。买盆送一袋颗粒土。",
         "Thrown by hand, so no two are alike. Every pot comes with gritty mix."),
    ]

    x = 0.9
    for img, price, price_en, cn, en, note_cn, note_en in items:
        picture_fill(s, IMG / img, x, 1.86, 3.4, 3.72,
                     shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04, anchor_y=0.5)
        # price chip
        rect(s, x + 0.16, 2.02, 0.86, 0.26, fill=WHITE, alpha=94,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
        text(s, price, x + 0.16, 2.07, 0.86, 0.2, 7.5, INK, SANS,
             align=PP_ALIGN.CENTER, spacing=0.6)

        tf = textbox(s, x, 5.72, 3.4, 0.36)
        p = para(tf, first=True, line=1.1)
        run(p, cn, 16, INK, SERIF, spacing=0.6)
        run(p, "   " + en, 10, INK_SOFT, SERIF, italic=True)

        tf = textbox(s, x, 6.16, 3.2, 0.75)
        p = para(tf, first=True, line=1.5)
        run(p, note_cn, 8.8, INK_SOFT, SANS)
        p = para(tf, space_before=3, line=1.35)
        run(p, note_en, 7.8, INK_SOFT, SERIF, italic=True)

        x += 4.03
    return s


# ── slide 4 · how it works ─────────────────────────────────────
def how_it_works(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s)
    header(s, "03", "怎么买", "How It Works")

    steps = [
        ("01", "逛一逛", "Drop by",
         "每周三、周五中午 12:00，A 座教学楼门口的长桌。下雨就挪到门厅里。",
         "Wednesdays and Fridays at 12:00, a long table outside Building A."),
        ("02", "挑一盆", "Pick one",
         "不知道选哪个就说你的窗朝哪边、多久想起来一次浇水，我们替你挑。",
         "Tell us which way your window faces and how often you water."),
        ("03", "带回去", "Take it home",
         "旧报纸加麻绳捆好，宿舍楼下可送。搬上楼的时候不会撒一车土。",
         "Wrapped in newspaper and twine, delivered to your dorm if you like."),
        ("04", "养下去", "Keep it alive",
         "扫码进养护群。每周一条浇水提醒，出问题随时问，不用自己搜。",
         "A weekly reminder, and a human to ask instead of a search bar."),
    ]

    top, mid, bottom = 1.86, 3.98, 6.10
    left, right = 0.9, SLIDE_W - 0.9
    col = (right - left) / 2
    rule_row(s, mid)
    rule_row(s, bottom)
    rule(s, left + col, top, left + col, bottom)

    cells = [(left, top), (left + col, top), (left, mid), (left + col, mid)]
    for (cx, cy), (num, cn, en, body_cn, body_en) in zip(cells, steps):
        text(s, num, cx + 0.34, cy + 0.3, 0.6, 0.22, 9.5, JADE, SERIF, spacing=1.2)
        tf = textbox(s, cx + 0.34, cy + 0.58, col - 0.7, 0.45)
        p = para(tf, first=True, line=1.1)
        run(p, cn, 19, INK, SERIF, spacing=0.4)
        run(p, "   " + en, 10.5, INK_SOFT, SERIF, italic=True)
        tf = textbox(s, cx + 0.34, cy + 1.2, col - 0.8, 0.85)
        p = para(tf, first=True, line=1.55)
        run(p, body_cn, 9.2, INK_SOFT, SANS)
        p = para(tf, space_before=3, line=1.35)
        run(p, body_en, 8.2, INK_SOFT, SERIF, italic=True)

    tf = textbox(s, 0.9, 6.34, 11.53, 0.3)
    p = para(tf, first=True, align=PP_ALIGN.CENTER)
    run(p, "四步。从看见它，到它在你窗台上活过第一个学期。", 9.5, INK_SOFT, SANS)
    run(p, "   Four steps, from first glance to its first full semester.", 9,
        INK_SOFT, SERIF, italic=True)
    return s


# ── slide 5 · logo ─────────────────────────────────────────────
def logo_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s)
    header(s, "04", "我们的 Logo", "Our Logo")

    add_mark(s, 0.72, 2.58, 5.95, color=INK)
    add_mark_bars(s, 0.72, 2.58, 5.95, color=INK,
                  plus_center=(5.7, 12.0), minus_center=(18.3, 12.0),
                  length=2.45, thickness=0.88)

    rule(s, 7.72, 2.2, 7.72, 5.66, LINE)

    notes = [
        ("01", "外形是一个「无限」符号 ∞。", "Our logo is shaped like the infinity symbol.", 2.2),
        ("02", "象征生命的延续，和无限的可能。", "It symbolises the continuation of life and infinite possibilities.", 4.0),
    ]
    for num, cn, en, y in notes:
        text(s, num, 8.05, y + 0.06, 0.5, 0.24, 10, JADE, SERIF, spacing=1.2)
        tf = textbox(s, 8.62, y, 3.89, 0.9)
        p = para(tf, first=True, line=1.35)
        run(p, cn, 11.5, INK, SANS)
        p = para(tf, space_before=4, line=1.35)
        run(p, en, 8.8, INK_SOFT, SERIF, italic=True)
        rule(s, 8.05, y + 1.55, SLIDE_W - 0.9, y + 1.55, LINE)

    text(s, "左边的 ＋ 是加一点绿，右边的 － 是减一点焦虑。", 0.9, 6.32, 11.53, 0.3,
         10.5, INK_SOFT, SERIF, italic=True, align=PP_ALIGN.CENTER)
    return s


# ── slide 6 · team ─────────────────────────────────────────────
def team(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s)
    header(s, "05", "我们的团队", "Our Team")

    text(s, "一个店长，两个小组。谁决定什么、谁在摊位、谁在群里回消息，都在下面这张图里。",
         0.9, 1.5, 8.6, 0.26, 9, INK_SOFT, SANS)

    # lead card
    lx, ly, lw, lh = 4.36, 1.95, 4.6, 1.32
    card(s, lx, ly, lw, lh, "店长", "Shop Manager", BLUE,
         "店长管店。选品、订货、和学校谈摊位，都是她的事。",
         "Runs the shop: stock, orders, and the stall negotiation.",
         "周一至周五 · 在店里  Mon–Fri · in the shop")

    # connectors
    rule(s, lx + lw / 2, ly + lh, lx + lw / 2, 3.86, LINE)
    rule(s, 3.5, 3.86, 9.86, 3.86, LINE)
    rule(s, 3.5, 3.86, 3.5, 4.08, LINE)
    rule(s, 9.86, 3.86, 9.86, 4.08, LINE)

    card(s, 0.9, 4.08, 5.2, 1.82, "销售组", "Sales Team", SALE_TEAL,
         "销售组卖植物。出摊、介绍品种、帮你挑到合适的那一盆。",
         "Sets up the stall, talks through varieties, finds your plant.",
         "周三 / 周五 · 长桌旁  Wed & Fri · at the table")
    card(s, 7.23, 4.08, 5.2, 1.82, "养护组", "Care Team", OCHRE,
         "养护组浇水。换盆、寄养、回消息，让每一盆都活到下学期。",
         "Watering, repotting, boarding, and answering messages.",
         "每天 · 群里都在  Every day · in the group")
    return s


def card(s, x, y, w, h, tag_cn, tag_en, color, body_cn, body_en, foot):
    rect(s, x, y, w, h, fill=WHITE, line_color=RGBColor(0xE3, 0xD8, 0xC2),
         line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.035)
    # tab
    tag_w = 1.62
    rect(s, x + 0.34, y - 0.17, tag_w, 0.34, fill=color,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    tf = textbox(s, x + 0.34, y - 0.11, tag_w, 0.22)
    p = para(tf, first=True, align=PP_ALIGN.CENTER)
    run(p, tag_cn, 8.5, WHITE, SANS, bold=True)
    run(p, "  " + tag_en, 8, WHITE, SERIF, italic=True)

    tf = textbox(s, x + 0.38, y + 0.34, w - 0.76, 0.8)
    p = para(tf, first=True, line=1.55)
    run(p, body_cn, 10.5, INK, SANS)
    p = para(tf, space_before=4, line=1.35)
    run(p, body_en, 8.4, INK_SOFT, SERIF, italic=True)

    text(s, foot, x + 0.38, y + h - 0.34, w - 0.76, 0.24, 8, INK_SOFT, SERIF,
         italic=True)


# ── slide 7 · closing ──────────────────────────────────────────
def closing(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    background(s, DEEP)

    picture_fill(s, IMG / "forest.jpg", 0, 0, SLIDE_W, SLIDE_H, anchor_y=0.5)
    rect(s, 0, 0, SLIDE_W, SLIDE_H, fill=DEEP, alpha=74)

    text(s, "WE WANT TO SAY  ·  想说的话", 0.9, 0.86, 8.0, 0.26, 9, JADE_LT, SANS,
         spacing=2.4)

    rows = [
        ("01", "植物让校园更绿。", "Plants make campus green.", 1.72),
        ("02", "让我们一起爱护植物和自然。", "Let’s love plants and nature, together.", 3.06),
    ]
    for num, cn, en, y in rows:
        rule(s, 0.9, y - 0.34, 6.4, y - 0.34, LINE_DARK)
        text(s, num, 0.9, y, 0.5, 0.22, 9.5, JADE_LT, SERIF, spacing=1.2)
        tf = textbox(s, 1.5, y - 0.1, 4.9, 0.9)
        p = para(tf, first=True, line=1.4)
        run(p, cn, 15, CREAM, SERIF, spacing=0.4)
        p = para(tf, space_before=3, line=1.3)
        run(p, en, 10, JADE_LT, SERIF, italic=True)

    # big thanks
    tf = textbox(s, 7.55, 2.08, 5.0, 1.3)
    p = para(tf, first=True, line=1.0)
    run(p, "谢谢你！", 62, CREAM, SERIF, spacing=1.0)
    text(s, "Thank you!", 7.6, 3.5, 4.6, 0.5, 26, JADE_LT, SERIF, italic=True)

    rule(s, 7.6, 4.4, 10.6, 4.4, JADE)
    text(s, "Campus Plant Corner · 校园绿植小店\n每周三 / 周五 12:00 · A 座教学楼门口",
         7.6, 4.6, 4.8, 0.8, 9.5, RGBColor(0xB8, 0xC8, 0xBD), SANS, line=1.6)

    # small mark, sitting on the photograph
    add_mark(s, 10.72, 5.62, 1.36, color=CREAM)

    text(s, "07 / 07", 11.03, 7.04, 1.4, 0.24, 7.5, RGBColor(0x7E, 0x91, 0x85),
         SERIF, align=PP_ALIGN.RIGHT)
    return s


def main():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    cover(prs)
    about(prs)
    products(prs)
    how_it_works(prs)
    logo_slide(prs)
    team(prs)
    closing(prs)

    for i, slide in enumerate(prs.slides, 1):
        if i > 1:
            footer(slide, i)

    prs.core_properties.title = "Campus Plant Corner · 校园绿植小店"
    prs.core_properties.author = "Campus Plant Corner"
    prs.core_properties.subject = "校园绿植小店 品牌介绍 / Brand deck"
    prs.save(OUT)
    print("saved", OUT, OUT.stat().st_size // 1024, "KB", len(prs.slides), "slides")


if __name__ == "__main__":
    main()
