"""0.42.0 Fused Glass Home > Favourites textures. Run from the skin folder.
fg/m300x168.png, fg/m112x168.png, fg/m168x168.png  rounded masks (radius 16) for the wide / poster / square tiles
fg/m126x190.png, fg/m148x222.png  Search window / Home > Search posters
fg/dash168.png    the "Add favourite" tile: a dashed rounded outline (radius 16), drawn 1:1
fg/btninfo_n.png  the spotlight's info button: a faint disc, a thin rim and a white "i" (56 px)
fg/btninfo_f.png  the same in focus: a white disc with the "i" cut out (the backdrop shows through it)"""
import math
import os
from PIL import Image, ImageDraw

OUT = os.path.join('media', 'fg')
SS = 4


def rounded(w, h, r):
    im = Image.new('L', (w * SS, h * SS), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], r * SS, fill=255)
    return im.resize((w, h), Image.LANCZOS)


def save(alpha, name, rgb=(255, 255, 255)):
    im = Image.new('RGBA', alpha.size, rgb + (0,))
    im.putalpha(alpha)
    im.save(os.path.join(OUT, name), optimize=True)


for w, h in ((300, 168), (112, 168), (168, 168), (126, 190), (148, 222)):   # the last two: Search (0.42.0)
    save(rounded(w, h, 16), 'm%dx%d.png' % (w, h))

# dashed outline: walk the rounded rectangle's centre line and draw short arcs / lines
S = 168 * SS
dash = Image.new('L', (S, S), 0)
d = ImageDraw.Draw(dash)
stroke, r, inset = 2 * SS, 16 * SS, 1 * SS
x0, y0, x1, y1 = inset, inset, S - inset, S - inset
points = []
step = 1.0 * SS
# perimeter points in order (top edge, top-right arc, right edge, ...)
def edge(ax, ay, bx, by):
    n = int(math.hypot(bx - ax, by - ay) / step)
    return [(ax + (bx - ax) * i / n, ay + (by - ay) * i / n) for i in range(n)]
def arc(cx, cy, a0, a1):
    n = int(abs(a1 - a0) * r / step)
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n)]
points += edge(x0 + r, y0, x1 - r, y0) + arc(x1 - r, y0 + r, -math.pi / 2, 0)
points += edge(x1, y0 + r, x1, y1 - r) + arc(x1 - r, y1 - r, 0, math.pi / 2)
points += edge(x1 - r, y1, x0 + r, y1) + arc(x0 + r, y1 - r, math.pi / 2, math.pi)
points += edge(x0, y1 - r, x0, y0 + r) + arc(x0 + r, y0 + r, math.pi, 1.5 * math.pi)
on, off = 9 * SS, 7 * SS
period = on + off
for i, (x, y) in enumerate(points):
    if (i * step) % period < on:
        d.ellipse([x - stroke / 2, y - stroke / 2, x + stroke / 2, y + stroke / 2], fill=255)
save(dash.resize((168, 168), Image.LANCZOS), 'dash168.png')

# info buttons, 56 px
B = 56 * SS
def glyph(draw, fill):
    cx = B / 2
    draw.ellipse([cx - 3.2 * SS, 15 * SS, cx + 3.2 * SS, 21.4 * SS], fill=fill)
    draw.rounded_rectangle([cx - 2.6 * SS, 25 * SS, cx + 2.6 * SS, 41 * SS], 2.6 * SS, fill=fill)
alpha = Image.new('L', (B, B), 0)
d = ImageDraw.Draw(alpha)
d.ellipse([0, 0, B - 1, B - 1], fill=46)                      # faint disc (about 18 %)
d.ellipse([0, 0, B - 1, B - 1], outline=72, width=int(1.5 * SS))
glyph(d, 255)
save(alpha.resize((56, 56), Image.LANCZOS), 'btninfo_n.png')
alpha = Image.new('L', (B, B), 0)
d = ImageDraw.Draw(alpha)
d.ellipse([0, 0, B - 1, B - 1], fill=255)
glyph(d, 0)
save(alpha.resize((56, 56), Image.LANCZOS), 'btninfo_f.png')
print('favourites textures written')
