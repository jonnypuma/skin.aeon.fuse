"""0.39.3: add the two symbols the TV channel names use to the skin's Figtree files (Kodi has no font fallback, so a
missing glyph is drawn as a box): U+2726 BLACK FOUR POINTED STAR and U+25CF BLACK CIRCLE, drawn here as plain shapes
sized to Figtree's cap height. Figtree is SIL OFL without a Reserved Font Name, so the files keep their name.
Run from the skin folder: python _src/fg_figtree_symbols.py   (idempotent: skips a file that has them already)"""
import os

from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

K = 0.5523  # circle by four cubic-like quadratic arcs: control distance for a quadratic approximation is r * 0.4142
WEIGHTS = ('Regular', 'Medium', 'SemiBold', 'Bold')


def circle(pen, cx, cy, r):
    # eight quadratic segments (good enough at UI sizes)
    import math
    n = 8
    pts = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    ctl = [(cx + r / math.cos(math.pi / n) * math.cos(2 * math.pi * (i + 0.5) / n),
            cy + r / math.cos(math.pi / n) * math.sin(2 * math.pi * (i + 0.5) / n)) for i in range(n)]
    pen.moveTo(pts[0])
    for i in range(n):
        pen.qCurveTo(ctl[i], pts[(i + 1) % n])
    pen.closePath()


def star(pen, cx, cy, r, pinch=0.16):
    # four points (top, left, bottom, right: counter-clockwise for a TrueType outer contour is clockwise... keep
    # the order clockwise: top, right, bottom, left), concave sides through controls near the centre
    top, right, bottom, left = (cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy)
    c = r * pinch
    pen.moveTo(top)
    pen.qCurveTo((cx + c, cy + c), right)
    pen.qCurveTo((cx + c, cy - c), bottom)
    pen.qCurveTo((cx - c, cy - c), left)
    pen.qCurveTo((cx - c, cy + c), top)
    pen.closePath()


def patch(path):
    font = TTFont(path)
    cmap = font.getBestCmap()
    if 0x2726 in cmap and 0x25CF in cmap:
        return False
    upm = font['head'].unitsPerEm
    cap = getattr(font['OS/2'], 'sCapHeight', 0) or int(upm * 0.7)
    glyphs = font.getGlyphSet()
    shapes = {}
    # circle: as tall as a capital, sitting on the baseline's middle of the cap height
    r = cap * 0.40
    side = upm * 0.08
    pen = TTGlyphPen(glyphs)
    circle(pen, side + r, cap / 2.0, r)
    shapes['uni25CF'] = (pen.glyph(), int(2 * side + 2 * r), 0x25CF)
    rs = cap * 0.52
    pen = TTGlyphPen(glyphs)
    star(pen, side + rs, cap / 2.0, rs)
    shapes['uni2726'] = (pen.glyph(), int(2 * side + 2 * rs), 0x2726)
    order = list(font.getGlyphOrder())
    for name, (glyph, adv, code) in shapes.items():
        if name not in order:
            order.append(name)
        font['glyf'][name] = glyph
        glyph.recalcBounds(font['glyf'])
        font['hmtx'][name] = (adv, getattr(glyph, 'xMin', 0))
        for table in font['cmap'].tables:
            if table.isUnicode():
                table.cmap[code] = name
    font.setGlyphOrder(order)
    for tag in ('hdmx', 'LTSH', 'VDMX'):
        if tag in font:
            del font[tag]
    font.save(path + '.tmp')
    os.replace(path + '.tmp', path)
    return True


for w in WEIGHTS:
    p = os.path.join('fonts', 'Figtree-%s.ttf' % w)
    print(p, 'patched' if patch(p) else 'already has them')
