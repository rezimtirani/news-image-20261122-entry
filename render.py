#!/usr/bin/env python3
"""Render the 22 November 2026 front page from news.json into entry.png.

Pure PIL + DejaVu. No network. Deterministic: same input, same bytes.
Run: python3 render.py  (writes entry.png next to this file)
"""
import json
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
RED = (178, 34, 34)
GREY = (110, 105, 92)
RULE = (60, 58, 50)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin
    right = W - mx

    # --- masthead -------------------------------------------------------
    y = 28
    title = data["masthead"]
    tf = SERIF_B(62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 78
    hrule(d, mx, right, y, 3)
    y += 10
    df = SANS(15)
    dw = d.textlength(data["date_line"], font=df)
    d.text(((W - dw) / 2, y), data["date_line"], font=df, fill=GREY)
    y += 26
    hrule(d, mx, right, y, 3)
    y += 18

    # --- hero -----------------------------------------------------------
    hero = data["hero"]
    kf = SANS_B(17)
    d.text((mx, y), hero["kicker"], font=kf, fill=RED)
    y += 26
    hf = SERIF_B(46)
    hl = wrap(d, hero["headline"], hf, right - mx)
    y = draw_lines(d, hl, mx, y, hf, INK, 54)
    y += 8
    bf = SANS(18)
    bl = wrap(d, hero["body"], bf, right - mx)
    y = draw_lines(d, bl, mx, y, bf, INK, 25)
    y += 16
    hrule(d, mx, right, y, 2)
    y += 18

    # --- story grid: three rows x two columns ---------------------------
    col_w = (right - mx - 24) // 2
    stories = data["stories"]
    row_h = 152
    for idx, st in enumerate(stories):
        col = idx % 2
        row = idx // 2
        x = mx + col * (col_w + 24)
        top = y + row * row_h
        d.text((x, top), st["tag"], font=SANS_B(14), fill=tuple(st["color"]))
        sf = SERIF_B(24)
        sl = wrap(d, st["headline"], sf, col_w)
        ty = draw_lines(d, sl, x, top + 21, sf, INK, 29)
        bf2 = SANS(14)
        bl2 = wrap(d, st["body"], bf2, col_w)
        draw_lines(d, bl2, x, ty + 3, bf2, INK, 19)
        if col == 0:
            d.line([(x + col_w + 12, top), (x + col_w + 12, top + row_h - 12)],
                   fill=(200, 194, 178), width=1)
    # sixth cell: also today
    ax = mx + col_w + 24
    atop = y + 2 * row_h
    d.text((ax, atop), "ALSO TODAY", font=SANS_B(14), fill=RED)
    af2 = SANS(13)
    al = wrap(d, data["also_today"], af2, col_w)
    draw_lines(d, al, ax, atop + 21, af2, INK, 18)
    y = y + 3 * row_h + 10
    hrule(d, mx, right, y, 2)
    y += 14
    sf2 = SANS(12)
    src = "Sources: AP · Reuters · BBC · Al Jazeera · Yle — reporting from 20–22 November 2026"
    sw = d.textlength(src, font=sf2)
    d.text(((W - sw) / 2, y), src, font=sf2, fill=GREY)

    # --- ticker ----------------------------------------------------------
    ty0 = H - 44
    d.rectangle([0, ty0, W, H], fill=INK)
    tf2 = SANS_B(14)
    tw2 = d.textlength(data["ticker"], font=tf2)
    # shrink to fit if needed
    while tw2 > W - 24 and tf2.size > 10:
        tf2 = SANS_B(tf2.size - 1)
        tw2 = d.textlength(data["ticker"], font=tf2)
    d.text(((W - tw2) / 2, ty0 + 13), data["ticker"], font=tf2, fill=(248, 244, 233))

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
