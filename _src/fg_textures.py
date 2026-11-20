"""Fused Glass textures (skin.aeon.fuse/media/fg): white shapes that the skin tints with colordiffuse.
rN.png: rounded rectangle, radius N (9-slice border N). eN.png: its 1 px edge. ringN.png: a 3 px ring around a radius-N
tile, drawn 3 px outside it (border N+3). shN.png: soft shadow of a radius-N panel, 40 px blur margin (border N+40).
circle.png, bar.png (spectrum bar), scrim_l.png / scrim_b.png (left and bottom gradients)."""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter

OUT = sys.argv[1]
SS = 4


def rounded(size, radius, outline=None, inset=0):
    w, h = size
    im = Image.new('L', (w * SS, h * SS), 0)
    d = ImageDraw.Draw(im)
    box = [inset * SS, inset * SS, (w - inset) * SS - 1, (h - inset) * SS - 1]
    if outline:
        d.rounded_rectangle(box, radius=radius * SS, outline=255, width=outline * SS)
    else:
        d.rounded_rectangle(box, radius=radius * SS, fill=255)
    return im.resize((w, h), Image.LANCZOS)


def save_alpha(alpha, name):
    im = Image.new('RGBA', alpha.size, (255, 255, 255, 0))
    im.putalpha(alpha)
    im.save(os.path.join(OUT, name), optimize=True)


for r in (8, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 36, 38, 40, 44, 48):
    n = 2 * r + 16
    save_alpha(rounded((n, n), r), 'r%d.png' % r)
    save_alpha(rounded((n, n), r, outline=1), 'e%d.png' % r)
for r in (12, 14, 16, 18, 20, 24, 28, 30):
    R = r + 3
    n = 2 * R + 16
    save_alpha(rounded((n, n), R, outline=3), 'ring%d.png' % r)
for r in (16, 24, 28, 32):
    m = 40
    n = 2 * r + 16
    big = Image.new('L', (n + 2 * m, n + 2 * m), 0)
    big.paste(rounded((n, n), r), (m, m))
    big = big.filter(ImageFilter.GaussianBlur(16))
    save_alpha(big, 'sh%d.png' % r)
save_alpha(rounded((128, 128), 64), 'circle.png')
save_alpha(rounded((128, 128), 64, outline=2), 'circle_edge.png')
save_alpha(rounded((12, 64), 6), 'bar.png')


def ramp(points, n):
    """points: [(pos 0..1, alpha 0..1)] piecewise linear, smoothed"""
    vals = []
    for i in range(n):
        x = i / (n - 1)
        for (x0, a0), (x1, a1) in zip(points, points[1:]):
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0) if x1 > x0 else 0
                t = t * t * (3 - 2 * t)
                vals.append(a0 + (a1 - a0) * t)
                break
    return vals


left = ramp([(0, 0.9), (0.34, 0.62), (0.62, 0), (1, 0)], 512)
im = Image.new('L', (512, 4))
im.putdata([int(v * 255) for v in left] * 4)
save_alpha(im, 'scrim_l.png')
bottom = ramp([(0, 0), (0.42, 0), (0.66, 0.6), (1, 0.94)], 512)
im = Image.new('L', (4, 512))
im.putdata([int(v * 255) for v in bottom for _ in range(4)])
save_alpha(im, 'scrim_b.png')
top = ramp([(0, 0.55), (0.22, 0), (1, 0)], 256)
im = Image.new('L', (4, 256))
im.putdata([int(v * 255) for v in top for _ in range(4)])
save_alpha(im, 'scrim_t.png')
print(len(os.listdir(OUT)), 'textures')


# tile masks (diffuse) at the exact size of Home's strip tiles: mWxH.png, radius 16
for w, h in ((195, 292), (237, 237), (237, 133)):
    save_alpha(rounded((w, h), 16), 'm%dx%d.png' % (w, h))


# library rails: textures exactly as big as the strip columns (no slicing), a rounded pill inset in each
def rail(w, h, inset, radius, name, yinset=None):
    yinset = inset if yinset is None else yinset
    im = Image.new('L', (w, h), 0)
    im.paste(rounded((w - 2 * inset, h - 2 * yinset), radius), (inset, yinset))
    save_alpha(im, name)


# 0.38.0: the 100 px rail runs 24..1056 like the List view card, corners 24 (38 left the clock and count no room)
rail(100, 1080, 12, 24, 'rail100.png', yinset=24)
rail(80, 1080, 8, 32, 'rail80.png')
rail(60, 1080, 6, 24, 'rail60.png')
save_alpha(Image.new('L', (4, 4), 0), 'clear.png')
# focused letter of the A-Z rail: a 30 px circle in the 66 x 30 row
im = Image.new('L', (66, 30), 0)
im.paste(rounded((30, 30), 15), (18, 0))
save_alpha(im, 'letter66x30.png')
# focused row of the settings rail (420 x 80 row): a pill inset 8 px
im = Image.new('L', (420, 80), 0)
im.paste(rounded((404, 64), 16), (8, 8))
save_alpha(im, 'striprow420x80.png')


# library walls: a 3 px ring INSIDE the tile edge (9-slice, border 16) and masks at the exact tile sizes
save_alpha(rounded((48, 48), 16, outline=3), 'ri16.png')
for w, h in ((205, 308), (195, 293), (410, 231), (266, 238), (266, 266), (543, 305)):
    save_alpha(rounded((w, h), 16), 'm%dx%d.png' % (w, h))


# List view (510): the poster card in the left pane
save_alpha(rounded((572, 858), 24), 'm572x858.png')
# Low list (527): poster and episode still
save_alpha(rounded((197, 296), 16), 'm197x296.png')
save_alpha(rounded((400, 225), 16), 'm400x225.png')


# 0.30.1: Showcase (523), Flix (528), Combined (529), Pictures (516), Episode list (511) and the season view (512):
# radius 16 to match the inner ring ri16.png
for w, h in ((260, 390), (368, 558), (388, 218), (178, 267), (1584, 944), (280, 420), (572, 322), (330, 495)):
    save_alpha(rounded((w, h), 16), 'm%dx%d.png' % (w, h))


# 0.31.0 player overlays: focus circle / pill inset in the 90 px OSD cell, round seek knob with a halo, OSD poster
im = Image.new('L', (90, 90), 0)
im.paste(rounded((76, 76), 38), (7, 7))
save_alpha(im, 'btn90.png')
im = Image.new('L', (140, 90), 0)
im.paste(rounded((126, 76), 38), (7, 7))
save_alpha(im, 'pill90.png')
halo = rounded((34, 34), 17).point(lambda v: int(v * 0.18))
im = Image.new('L', (40, 40), 0)
im.paste(halo, (3, 3))
knob = rounded((22, 22), 11)
im.paste(255, (9, 9), knob)
save_alpha(im, 'knob40.png')
save_alpha(rounded((127, 190), 12), 'm127x190.png')
# Combined (529) seasons / episodes row, season poster of the open seasons view (512)
for w, h in ((156, 238), (328, 184), (320, 480)):
    save_alpha(rounded((w, h), 16), 'm%dx%d.png' % (w, h))


# 0.31.0 real frost: full-screen masks of the frosted panels; the skin lays the helper's blurred backdrop
# (Window(Home).Property(aeon.blur)) under the panels through them. bm510 List view, bm511 Episode list / open seasons
# view, bmrail the A-Z rail of the other views.
def blur_mask(name, rects):
    im = Image.new('L', (1920, 1080), 0)
    for x, y, w, h, r in rects:
        im.paste(255, (x, y), rounded((w, h), r))
    save_alpha(im, name)


# 0.56.2: the shapes of the Fused Glass views of 0.47+ (_src/fg_blur_masks.py draws just these four)
RAIL = (1836, 24, 64, 1032, 32)
blur_mask('bm510.png', [(723, 160, 1077, 880, 28), RAIL])
blur_mask('bm511.png', [(432, 160, 640, 880, 28), RAIL])
blur_mask('bm512.png', [(96, 160, 540, 880, 28), (676, 160, 600, 880, 28), RAIL])
blur_mask('bmrail.png', [RAIL])
# 0.31.0 screensaver: poster card, album cover, now playing cover
save_alpha(rounded((560, 840), 24), 'm560x840.png')
save_alpha(rounded((753, 753), 24), 'm753x753.png')
save_alpha(rounded((112, 112), 14), 'm112x112.png')
# 0.31.0 dialog rows (context menu): a pill inset 6 px left / right and 4 px top / bottom in the row (border 24)
im = Image.new('L', (80, 64), 0)
im.paste(rounded((68, 56), 16), (6, 4))
save_alpha(im, 'rowpill.png')
# 0.32.0 music views: album / song row cover, cover showcase, album list side cover, music List cover
for w, h, r in ((72, 72, 10), (280, 280, 16), (484, 484, 16), (596, 596, 28)):
    save_alpha(rounded((w, h), r), 'm%dx%d.png' % (w, h))
# 0.32.0 Home > Favourites cards
save_alpha(rounded((280, 158), 16), 'm280x158.png')
# 0.32.0 pagers: a horizontal pill for the current item (border 3)
im = Image.new("L", (24, 6), 0)
im.paste(rounded((24, 6), 3), (0, 0))
save_alpha(im, 'pillh.png')
# 0.34.0 information pages: the fanart fades in from the left (no solid fade strip over it, which left a hard line on
# the frosted card), right corners radius 28 like the card. mheroWxH.png at the art's exact size (video 1160, music 1140)
for w in (1160, 1140):
    h = 520
    fade = ramp([(0, 0), (0.06, 0), (0.62, 1), (1, 1)], w)
    im = Image.new('L', (w, h))
    im.putdata([int(v * 255) for v in fade] * h)
    corners = Image.new('L', (w + 28, h), 0)
    corners.paste(rounded((w + 28, h), 28), (0, 0))
    im = Image.composite(im, Image.new('L', (w, h), 0), corners.crop((28, 0, w + 28, h)))
    save_alpha(im, 'mhero%d.png' % w)
# 0.34.0 information pages: Recommended / Similar posters, music info track and similar-artist covers (radius 16)
for w, h in ((158, 241), (180, 180)):
    save_alpha(rounded((w, h), 16), 'm%dx%d.png' % (w, h))
# 0.34.0 settings pages (Settings mockup): Kodi draws the open category with its focus texture at half alpha while the
# list has focus, so selrow16.png is the frosted pill at double strength (fill 32 %, edge 36 % -> 16 % / 18 % shown)
fill = rounded((48, 48), 16)
edge = rounded((48, 48), 16, outline=1)
sel = Image.new('L', (48, 48), 0)
sel.paste(82, (0, 0), fill)
sel.paste(92, (0, 0), edge)
save_alpha(sel, 'selrow16.png')


# on / off switches of Kodi's setting rows (radio buttons), drawn 60 x 34 from 120 x 68 pictures; colours baked in
# (a cloned control cannot tint by variable): accent track + white knob, faint track, and the dark versions for the
# white focus row
def switch(name, track, knob, on):
    w, h = 120, 68
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    t = Image.new('RGBA', (w, h), track)
    im.paste(t, (0, 0), rounded((w, h), h // 2))
    k = Image.new('RGBA', (w, h), knob)
    d = 52
    x = w - 8 - d if on else 8
    mask = Image.new('L', (w, h), 0)
    mask.paste(rounded((d, d), d // 2), (x, 8))
    im.paste(k, (0, 0), mask)
    im.save(os.path.join(OUT, name), optimize=True)


switch('tog_on.png', (0xe8, 0xb0, 0x4b, 255), (255, 255, 255, 255), True)
switch('tog_off.png', (255, 255, 255, 56), (255, 255, 255, 255), False)
switch('tog_on_f.png', (0x0f, 0x11, 0x15, 255), (255, 255, 255, 255), True)
switch('tog_off_f.png', (0x0f, 0x11, 0x15, 64), (0x0f, 0x11, 0x15, 255), False)
# 0.34.0 progress ring on library art (Fused Glass replaces the line under the art, which ran past the rounded corners):
# fg/pring/0..100.png, white arcs from 12 o'clock clockwise (tinted with the accent), fg/pring/track.png the faint ring
from PIL import ImageDraw as _D
ring_dir = os.path.join(OUT, 'pring')
if not os.path.isdir(ring_dir):
    os.makedirs(ring_dir)
S = 80 * SS
for pct in list(range(0, 101)) + ['track']:
    im = Image.new('L', (S, S), 0)
    d = _D.Draw(im)
    box = [9 * SS, 9 * SS, S - 9 * SS - 1, S - 9 * SS - 1]
    if pct == 'track':
        d.ellipse(box, outline=255, width=7 * SS)
    elif pct > 0:
        d.arc(box, -90, -90 + 360 * pct / 100.0, fill=255, width=7 * SS)
    save_alpha(im.resize((80, 80), Image.LANCZOS), os.path.join('pring', '%s.png' % pct))
# 0.34.0 Banner list: banner rows, side pane poster and landscape (radius 16)
for w, h in ((700, 112), (273, 409), (647, 409)):
    save_alpha(rounded((w, h), 16), 'm%dx%d.png' % (w, h))
# 0.35.0 music Fanart list: the cycling album cover at the foot of the list card (radius 16), and that foot: a
# rectangle with only its bottom corners rounded (radius 28, 9-slice border 28,0,28,28)
save_alpha(rounded((256, 256), 16), 'm256x256.png')
save_alpha(rounded((72, 100), 28).crop((0, 28, 72, 100)), 'rb28.png')
# 0.35.0 Neutral backdrop: an elliptical vignette (clear middle, dark corners), drawn full screen over the plain ground
vw, vh = 384, 216
vig = Image.new('L', (vw, vh))
px = []
for y in range(vh):
    for x in range(vw):
        d = (((x + 0.5 - vw / 2) / (vw / 2)) ** 2 + ((y + 0.5 - vh / 2) / (vh / 2)) ** 2) ** 0.5
        t = min(1.0, max(0.0, (d - 0.42) / (1.30 - 0.42)))
        t = t * t * (3 - 2 * t)
        px.append(int(255 * t))
vig.putdata(px)
save_alpha(vig, 'vignette.png')
# 0.35.0 settings: the line between groups of settings (Kodi's separator 11): 1 px in the middle of 17 px, 24 px clear
# at both ends (border 24,0,24,0)
sep = Image.new('L', (64, 17), 0)
sep.paste(255, (24, 8, 40, 9))
save_alpha(sep, 'sepline.png')
# 0.35.0 Trickplay / chapter thumbs in the player's Chapters dialog (radius 16)
save_alpha(rounded((320, 180), 16), 'm320x180.png')
# 0.36.0 the skin's skip button (Custom_1167) in Fused Glass: a white capsule 88 px tall (border 44)
save_alpha(rounded((176, 88), 44), 'pill88.png')


# 0.36.0 focus highlight styles (Skin settings > Focus highlight, Skin.String(aeon.fgfocus)): fx_<style>.png for
# pictures drawn by the skin (64 x 64, 9-slice border 16, no margin; the shadow is a separate picture), fxb_<style>.png
# for buttons, whose texture is the button's own rectangle: 4 px clear at the sides, 2 at the top, 8 at the bottom for
# a baked drop shadow (border 20,18,20,24). Flat is a plain white square (no gap, no shadow).
def fx_shape(style, w, h, ox=0, oy=0, ow=None, oh=None):
    ow = w if ow is None else ow
    oh = h if oh is None else oh
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    radius = 6 if style == 'tight' else 16
    shape = Image.new('L', (w, h), 0)
    shape.paste(rounded((ow, oh), radius), (ox, oy))
    if style in ('pill', 'tight'):
        im.paste(Image.new('RGBA', (w, h), (255, 255, 255, 255)), (0, 0), shape)
    elif style == 'frost':
        fill = Image.new('L', (w, h), 0)
        fill.paste(shape.point(lambda v: v * 46 // 255), (0, 0))
        edge = Image.new('L', (w, h), 0)
        edge.paste(rounded((ow, oh), radius, outline=1), (ox, oy))
        alpha = Image.eval(Image.merge('LA', (fill, edge)).split()[0], lambda v: v)
        alpha = Image.composite(Image.new('L', (w, h), 84), fill, edge)
        im.putalpha(alpha)
        im = Image.merge('RGBA', (Image.new('L', (w, h), 255),) * 3 + (alpha,))
    elif style == 'outline':
        fill = shape.point(lambda v: v * 13 // 255)
        ring = Image.new('L', (w, h), 0)
        ring.paste(rounded((ow, oh), radius, outline=2), (ox, oy))
        alpha = Image.composite(Image.new('L', (w, h), 255), fill, ring)
        im = Image.merge('RGBA', (Image.new('L', (w, h), 255),) * 3 + (alpha,))
    return im, shape


for st in ('pill', 'tight', 'frost', 'outline'):
    im, _ = fx_shape(st, 64, 64)
    im.save(os.path.join(OUT, 'fx_%s.png' % st), optimize=True)
    # button version: shadow baked under the shape, outside it only
    W, H, L, T, B = 96, 96, 4, 2, 8
    im, shape = fx_shape(st, W, H, L, T, W - 2 * L, H - T - B)
    sh = Image.new('L', (W, H), 0)
    sh.paste(rounded((W - 2 * L, H - T - B), 16 if st != 'tight' else 6), (L, T + 4))
    sh = sh.filter(ImageFilter.GaussianBlur(3.2)).point(lambda v: v * 150 // 255)
    sh = Image.composite(Image.new('L', (W, H), 0), sh, shape.point(lambda v: 255 if v > 8 else 0))
    base = Image.merge('RGBA', (Image.new('L', (W, H), 0),) * 3 + (sh,))
    base.alpha_composite(im)
    base.save(os.path.join(OUT, 'fxb_%s.png' % st), optimize=True)
Image.new('RGBA', (16, 16), (255, 255, 255, 255)).save(os.path.join(OUT, 'fx_flat.png'))
Image.new('RGBA', (16, 16), (255, 255, 255, 255)).save(os.path.join(OUT, 'fxb_flat.png'))
