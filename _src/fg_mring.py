"""0.42.0 Fused Home > System: the memory ring, fg/mring/0..100.png (white arc from 12 o'clock clockwise, 144 px,
12 px stroke) and fg/mring/track.png (the full ring, tinted faint in the skin). Run from the skin folder."""
import os
from PIL import Image, ImageDraw

OUT = os.path.join('media', 'fg', 'mring')
SS = 4
SIZE, STROKE, INSET = 144, 12, 2
if not os.path.isdir(OUT):
    os.makedirs(OUT)
S = SIZE * SS
box = [INSET * SS, INSET * SS, S - INSET * SS - 1, S - INSET * SS - 1]
for pct in list(range(0, 101)) + ['track']:
    alpha = Image.new('L', (S, S), 0)
    d = ImageDraw.Draw(alpha)
    if pct == 'track':
        d.ellipse(box, outline=255, width=STROKE * SS)
    elif pct > 0:
        d.arc(box, -90, -90 + 360 * pct / 100.0, fill=255, width=STROKE * SS)
    alpha = alpha.resize((SIZE, SIZE), Image.LANCZOS)
    im = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))
    im.putalpha(alpha)
    im.save(os.path.join(OUT, '%s.png' % pct), optimize=True)
print('mring: 102 textures')
