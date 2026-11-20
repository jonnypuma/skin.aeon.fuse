"""Fused Glass context menu panel (media/dialogs/panel_fg.png, 0.31.0): the night panel's shape and shadow
(dialogs/panel_n.png: 192 x 192, panel inset 40, border 72), filled with the Fused frost colour and a hairline edge.
Kodi resizes only the context menu's image 999, so shadow and fill live in one texture."""
from PIL import Image, ImageFilter

src = Image.open('media/dialogs/panel_n.png').convert('RGBA')
w, h = src.size
out = Image.new('RGBA', (w, h))
mask = Image.new('L', (w, h), 0)
sp, op, mp = src.load(), out.load(), mask.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = sp[x, y]
        if (r, g, b) == (2, 4, 10):                 # shadow
            op[x, y] = (0, 0, 0, a)
        else:                                       # panel (antialiased rim keeps its alpha)
            op[x, y] = (26, 29, 36, int(a * 0.94))
            mp[x, y] = a
inner = mask.filter(ImageFilter.MinFilter(3))
ip = inner.load()
for y in range(h):
    for x in range(w):
        if mp[x, y] > 0 and ip[x, y] < 128:         # outermost panel pixels: the hairline edge
            r, g, b, a = op[x, y]
            op[x, y] = (78, 81, 88, a)
out.save('media/dialogs/panel_fg.png', optimize=True)
print('panel_fg.png', out.size)
