# -*- coding: utf-8 -*-
"""0.56.2 the frost masks of the library views (fg/bm*.png), redrawn for the Fused Glass views of 0.47+.

The skin lays the helper's blurred backdrop (Window(Home).Property(aeon.blur)) under the frosted panels through these
masks (Aeon_V_Bg, Material Frost and Dark; Clear shows the fanart sharp). The masks still had the shapes of the views
before the redesign, so the blur showed where the old panels were: a clear glass panel above and round the List view's
card (the user, 2026-11-15: "it has a clear glass panel above the dark panel"), and the same in the Episode list and
the open seasons view. Now:
  bm510  List (510): the list card 723,160 1077 x 880 (r28)
  bm511  Episode list (511): the card 432,160 640 x 880
  bm512  Season list combined 3 with the episodes open (512): the seasons card 96,160 540 x 880, the episodes card
         676,160 600 x 880
  bmrail the A-Z rail of every view: 1836,24 64 x 1032 (r32; it was 1832 / 76 wide / r24)
Same drawing as _src/fg_textures.py (4x supersampled rounded rectangles). Run from the skin folder."""
import os

from PIL import Image, ImageDraw

OUT = os.path.join('media', 'fg')
SS = 4


def rounded(size, radius):
    w, h = size
    im = Image.new('L', (w * SS, h * SS), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], radius=radius * SS, fill=255)
    return im.resize((w, h), Image.LANCZOS)


def blur_mask(name, rects):
    im = Image.new('L', (1920, 1080), 0)
    for x, y, w, h, r in rects:
        im.paste(255, (x, y), rounded((w, h), r))
    out = Image.new('RGBA', im.size, (255, 255, 255, 0))
    out.putalpha(im)
    out.save(os.path.join(OUT, name), optimize=True)
    print('wrote', name, im.getbbox())


RAIL = (1836, 24, 64, 1032, 32)
MASKS = {'bm510.png': [(723, 160, 1077, 880, 28), RAIL],
         'bm511.png': [(432, 160, 640, 880, 28), RAIL],
         'bm512.png': [(96, 160, 540, 880, 28), (676, 160, 600, 880, 28), RAIL],
         'bmrail.png': [RAIL]}

if __name__ == '__main__':
    for n, r in MASKS.items():
        blur_mask(n, r)
