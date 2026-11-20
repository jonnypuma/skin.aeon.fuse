"""0.38.0 Fused Glass textures (media/fg), same drawing as fg_textures.py:
m200x300.png  poster of the player information screen (radius 16); m240x135.png Low list episode thumb (radius 12)
eptag.png     the dark corner behind the season / episode tag on episode thumbs: dark in the top right corner, fading
              to nothing towards the left and down (drawn over the whole thumb through the thumb's own mask)
epgcell.png   TV guide programme cell (inset 3 px, radius 10, border 13)
Run: python _src/fg_tex38.py media/fg"""
import os
import sys

from PIL import Image, ImageDraw

OUT = sys.argv[1]
SS = 4


def rounded(size, radius):
    w, h = size
    im = Image.new('L', (w * SS, h * SS), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w * SS - 1, h * SS - 1], radius=radius * SS, fill=255)
    return im.resize((w, h), Image.LANCZOS)


def save_alpha(alpha, name):
    im = Image.new('RGBA', alpha.size, (255, 255, 255, 0))
    im.putalpha(alpha)
    im.save(os.path.join(OUT, name), optimize=True)


save_alpha(rounded((200, 300), 16), 'm200x300.png')
save_alpha(rounded((240, 135), 12), 'm240x135.png')
save_alpha(rounded((150, 84), 10), 'm150x84.png')          # 0.39.0 Planner day row thumb
save_alpha(rounded((230, 132), 16), 'm230x132.png')        # 0.39.0 Planner week thumb (ri16 ring)        # Low list: episode thumb beside the network logo

# eptag: 400 x 225 (16:9), opaque in the top right, an elliptical falloff to the left and down
W, H = 400, 225
a = Image.new('L', (W, H), 0)
px = a.load()
for y in range(H):
    for x in range(W):
        dx = (W - x) / 300.0          # reaches 0 about 300 px from the right edge
        dy = y / 115.0                # and 115 px down
        d = (dx * dx + dy * dy) ** 0.5
        v = max(0.0, 1.0 - d)
        px[x, y] = int(255 * min(1.0, 1.15 * v) ** 1.1)
save_alpha(a, 'eptag.png')
# epgcell: a TV guide programme cell, a rounded rectangle inset 3 px so neighbouring cells keep a gap (border 13)
im = Image.new('L', (48 * SS, 48 * SS), 0)
d = ImageDraw.Draw(im)
d.rounded_rectangle([3 * SS, 3 * SS, 45 * SS - 1, 45 * SS - 1], radius=10 * SS, fill=255)
save_alpha(im.resize((48, 48), Image.LANCZOS), 'epgcell.png')
print('ok')
