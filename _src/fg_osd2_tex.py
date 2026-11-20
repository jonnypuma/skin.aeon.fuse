"""Textures for the Fused Glass player card (0.41.0): poster mask, the 12 px seek bar pill and the chapter gap.
Run from the skin folder: python _src/fg_osd2_tex.py"""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media', 'fg')
SS = 8


def alpha_round(w, h, r):
    im = Image.new('L', (w * SS, h * SS), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], radius=r * SS, fill=255)
    return im.resize((w, h), Image.LANCZOS)


def save(alpha, name):
    im = Image.new('RGBA', alpha.size, (255, 255, 255, 0))
    im.putalpha(alpha)
    im.save(os.path.join(OUT, name), optimize=True)


# poster beside the card's text (156 x 234, radius 14, like the 2:3 art masks)
save(alpha_round(156, 234, 14), 'm156x234.png')
# seek bar: a 12 px pill, 9-slice border 6 (the whole arc), stretched to the bar's width
save(alpha_round(28, 12, 6), 'pill12.png')
# chapter gap: drawn at each chapter end over the bar in the card's colour. 18 x 12: the middle 6 px are solid (the
# gap itself), the outer 6 px are the corners outside a 6 px half circle on each side, so both chapter ends look round.
W, H = 18, 12
im = Image.new('L', (W * SS, H * SS), 255)
d = ImageDraw.Draw(im)
r = 6 * SS
d.pieslice([-r, 0, r - 1, 2 * r - 1], 270, 90, fill=0)          # end of the chapter on the left: right half circle at x 0
d.pieslice([W * SS - r, 0, W * SS + r - 1, 2 * r - 1], 90, 270, fill=0)  # start of the next one: left half circle
save(im.resize((W, H), Image.LANCZOS), 'chgap.png')
print('ok')
