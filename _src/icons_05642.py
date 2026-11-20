# -*- coding: utf-8 -*-
"""0.56.42 icons for Skin settings > System > Export / Import skin settings: a tray with an arrow out / in, drawn like
media/aeon/icons (white, 96 px, 9 px strokes with round ends). Run from the skin folder."""
from PIL import Image, ImageDraw

S = 8                      # drawn 8x, then scaled down (smooth edges)
W = 9


def polyline(d, pts):
    pts = [(x * S, y * S) for x, y in pts]
    d.line(pts, fill=255, width=W * S, joint='curve')
    r = W * S / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)


def icon(path, up):
    a = Image.new('L', (96 * S, 96 * S), 0)
    d = ImageDraw.Draw(a)
    # the tray: the lower half of a rounded box (corners like home.png), round ends at the top
    tray = Image.new('L', a.size, 0)
    t = ImageDraw.Draw(tray)
    h = W / 2
    t.rounded_rectangle(((14 - h) * S, 20 * S, (82 + h) * S, (80 + h) * S), radius=16 * S, outline=255, width=W * S)
    t.rectangle((0, 0, 96 * S, 58 * S), fill=0)
    for x in (14, 82):
        t.ellipse(((x - h) * S, (58 - h) * S, (x + h) * S, (58 + h) * S), fill=255)
    a.paste(255, mask=tray)
    if up:
        polyline(d, [(48, 64), (48, 15)])
        polyline(d, [(29, 34), (48, 15), (67, 34)])
    else:
        polyline(d, [(48, 15), (48, 62)])
        polyline(d, [(29, 43), (48, 62), (67, 43)])
    a = a.resize((96, 96), Image.LANCZOS)
    im = Image.new('RGBA', (96, 96), (255, 255, 255, 0))
    im.putalpha(a)
    im.save(path)


def person(path):
    """the artist button of the strip's Now playing overlay (0.56.42): a head and shoulders"""
    a = Image.new('L', (96 * S, 96 * S), 0)
    d = ImageDraw.Draw(a)
    h = W / 2
    d.ellipse(((48 - 16 - h) * S, (16 - h) * S, (48 + 16 + h) * S, (48 + h) * S), outline=255, width=W * S)
    d.arc(((14 - h) * S, (58 - h) * S, (82 + h) * S, (126 + h) * S), 180, 360, fill=255, width=W * S)
    for x in (14, 82):
        d.ellipse(((x - h) * S, (88 - h) * S, (x + h) * S, (88 + h) * S), fill=255)
    a.paste(0, (0, (88 + 1) * S, 96 * S, 96 * S))
    for x in (14, 82):
        d.ellipse(((x - h) * S, (88 - h) * S, (x + h) * S, (88 + h) * S), fill=255)
    a = a.resize((96, 96), Image.LANCZOS)
    im = Image.new('RGBA', (96, 96), (255, 255, 255, 0))
    im.putalpha(a)
    im.save(path)


if __name__ == '__main__':
    icon('media/aeon/icons/export.png', True)
    icon('media/aeon/icons/import.png', False)
    person('media/aeon/icons/artist.png')
    print('ok')
