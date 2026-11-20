"""0.39.6 exact rounded textures (white, anti-aliased by 8x box supersampling - the same coverage as the existing
fg/rNN.png): true circular corners so a 9-slice border that equals the radius keeps the corner tangent-continuous.
  fg/r15.png      46 x 46, r15  (the "In library" pill, 30 px tall)
  fg/pill4.png    12 x 4,  r2   (focus marks 4 px tall; fg/pillh.png is 6 px)
  aeon/pill_36.png 72 x 36, r18 (an Aeon pill drawn 36 px tall)
Run from the skin folder. Checks itself against fg/r16.png (max alpha difference)."""
import os

from PIL import Image, ImageDraw

S = 8


def rounded(w, h, r):
    big = Image.new('L', (w * S, h * S), 0)
    ImageDraw.Draw(big).rounded_rectangle((0, 0, w * S - 1, h * S - 1), radius=r * S, fill=255)
    mask = big.resize((w, h), Image.BOX)
    im = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    im.putalpha(mask)
    return im


def save(path, w, h, r):
    rounded(w, h, r).save(os.path.join('media', path), optimize=True)
    print('wrote', path, w, h, r)


ref = Image.open(os.path.join('media', 'fg', 'r16.png')).convert('RGBA').split()[3]
mine = rounded(48, 48, 16).split()[3]
diff = max(abs(a - b) for a, b in zip(ref.getdata(), mine.getdata()))
print('check against fg/r16.png: max alpha difference', diff)
save('fg/r15.png', 46, 46, 15)
save('fg/pill4.png', 12, 4, 2)
save('aeon/pill_36.png', 72, 36, 18)
