"""Home background for Favourites (0.32.0), from bg_system.py: rose glow, a neon heart.
Old docstring: Home background for Live TV in the style of aeon_bg_power / aeon_bg_search: dark field, a coloured radial glow on the
right with thin rings, a neon line icon (a TV set with an antenna, broadcast waves on its screen)."""
import math
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
CX, CY = 1400, 540
GLOW = (196, 56, 92)         # rose
NEON = (255, 170, 196)
Z = 2                         # supersampling for the lines

# 1. field: dark at the left, glow around the icon
bg = Image.new('RGB', (W, H), (22, 8, 12))
glow = Image.new('L', (W, H), 0)
d = ImageDraw.Draw(glow)
for r in range(1100, 0, -10):
    v = int(255 * (1 - r / 1100.0) ** 1.6)
    d.ellipse((CX - r, CY - r, CX + r, CY + r), fill=v)
glow = glow.filter(ImageFilter.GaussianBlur(30))
colour = Image.new('RGB', (W, H), GLOW)
bg = Image.composite(colour, bg, glow.point(lambda p: int(p * 0.82)))
# darker to the left (as the other two)
shade = Image.new('L', (W, H), 0)
ds = ImageDraw.Draw(shade)
for x in range(W):
    ds.line([(x, 0), (x, H)], fill=int(200 * max(0.0, 1 - x / 1100.0) ** 1.4))
bg = Image.composite(Image.new('RGB', (W, H), (14, 5, 8)), bg, shade)

# 2. thin rings
rings = Image.new('RGBA', (W * Z, H * Z), (0, 0, 0, 0))
dr = ImageDraw.Draw(rings)
for r in (300, 370, 450, 545, 660, 800):
    dr.ellipse(((CX - r) * Z, (CY - r) * Z, (CX + r) * Z, (CY + r) * Z), outline=(250, 190, 205, 34), width=2 * Z)
rings = rings.resize((W, H), Image.LANCZOS)
bg = bg.convert('RGBA')
bg.alpha_composite(rings)

# 3. the neon icon
line = Image.new('L', (W * Z, H * Z), 0)
dl = ImageDraw.Draw(line)
S = 11 * Z                                   # stroke
# a heart: the classic parametric curve, about 470 px wide
pts = []
for i in range(0, 721):
    t = math.pi * 2 * i / 720
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    pts.append(((CX + x * 14.5) * Z, (CY - 20 - y * 14.5) * Z))
dl.line(pts, fill=255, width=S, joint='curve')
line = line.resize((W, H), Image.LANCZOS)
halo = line.filter(ImageFilter.GaussianBlur(18))
halo2 = line.filter(ImageFilter.GaussianBlur(6))
for mask, col, k in ((halo, GLOW, 0.9), (halo2, NEON, 0.8), (line, NEON, 1.0)):
    layer = Image.new('RGBA', (W, H), col + (0,))
    layer.putalpha(mask.point(lambda p, k=k: int(min(255, p * k * (1.6 if mask is halo else 1)))))
    bg.alpha_composite(layer)
# a white core on the line for the neon look
core = line.filter(ImageFilter.GaussianBlur(1)).point(lambda p: int(p * 0.55))
layer = Image.new('RGBA', (W, H), (235, 250, 255, 0))
layer.putalpha(core)
bg.alpha_composite(layer)
out = 'C:/Users/gideo/AppData/Roaming/Kodi/addons/skin.aeon.fuse/media/common/aeon_bg_favourites.jpg'
bg.convert('RGB').save(out, quality=90, optimize=True, progressive=True)
bg.convert('RGB').resize((960, 540)).save('C:/Users/gideo/AppData/Local/Temp/claude/c0246abe73422812/be2282f1-eeb2-4abe-aa52-a2bae6fb30f8/scratchpad/bg_fav_small.png')
print('ok')
