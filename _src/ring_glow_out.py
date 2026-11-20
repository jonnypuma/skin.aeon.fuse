# -*- coding: utf-8 -*-
"""0.56.18: the focus glow without its middle. aeon/ring_glow_<r>.png is opaque in the middle, so the glow (AG_Halo,
the mood colour of the time of day) filled the whole focused card - the "frosted" look the user did not like on the
information page's plot card (2026-11-16). ring_glow_out_<r>.png keeps the glow outside the card only: alpha 0 inside
the card's rounded rectangle (44 px in from the texture edge, the card's radius r), a 4 px soft edge. AG_FocusRing
places the glow 44 px outside the card with border 60."""
import os
from PIL import Image

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media', 'aeon')
INSET = 44
SOFT = 4.0


def inside_distance(x, y, w, h, r):
    """distance into the rounded rectangle (inset INSET, radius r); negative outside"""
    left, top, right, bottom = INSET, INSET, w - INSET, h - INSET
    cx = min(max(x, left + r), right - r)
    cy = min(max(y, top + r), bottom - r)
    if left + r <= x <= right - r or top + r <= y <= bottom - r:
        return min(x - left, right - x, y - top, bottom - y)
    return r - ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5


for r in (14, 16, 20, 28):
    src = Image.open(os.path.join(HERE, 'ring_glow_%d.png' % r)).convert('RGBA')
    w, h = src.size
    px = src.load()
    out = Image.new('RGBA', (w, h))
    po = out.load()
    for y in range(h):
        for x in range(w):
            R, G, B, A = px[x, y]
            d = inside_distance(x + 0.5, y + 0.5, w, h, r)
            keep = 1.0 if d <= 0 else max(0.0, 1.0 - d / SOFT)
            po[x, y] = (R, G, B, int(round(A * keep)))
    out.save(os.path.join(HERE, 'ring_glow_out_%d.png' % r))
    print('ring_glow_out_%d.png' % r, (w, h))
