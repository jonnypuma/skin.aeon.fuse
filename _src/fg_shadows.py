"""0.45.1 soft shadows without visible steps: fg/sh16, sh24, sh28, sh32 rebuilt from a float Gaussian (the same size
and 9-slice border as before: margin 40, border = 40 + radius) with a little random dither in the alpha, so an 8-bit
gradient shows no bands on a close screen. Run from the skin folder."""
import math
import os
import random

from PIL import Image

OUT = os.path.join('media', 'fg')
random.seed(7)


def rounded_mask(n, r):
    rows = []
    for yy in range(n):
        y = yy + 0.5
        row = []
        for xx in range(n):
            x = xx + 0.5
            cx = min(max(x, r), n - r)
            cy = min(max(y, r), n - r)
            d = math.hypot(x - cx, y - cy)
            row.append(min(max(r - d + 0.5, 0.0), 1.0))
        rows.append(row)
    return rows


def blur1d(v, g, k):
    n = len(v)
    out = [0.0] * n
    for i in range(n):
        s = 0.0
        for j in range(-k, k + 1):
            t = i + j
            if 0 <= t < n:
                s += v[t] * g[j + k]
        out[i] = s
    return out


def blur(a, sigma):
    k = int(sigma * 3)
    g = [math.exp(-(x * x) / (2 * sigma * sigma)) for x in range(-k, k + 1)]
    total = sum(g)
    g = [x / total for x in g]
    a = [blur1d(row, g, k) for row in a]
    cols = [blur1d([a[y][x] for y in range(len(a))], g, k) for x in range(len(a[0]))]
    return [[cols[x][y] for x in range(len(cols))] for y in range(len(a))]


for r in (16, 24, 28, 32):
    m = 40
    n = 2 * r + 16
    size = n + 2 * m
    big = [[0.0] * size for _ in range(size)]
    mask = rounded_mask(n, r)
    for y in range(n):
        big[m + y][m:m + n] = mask[y]
    a = blur(big, 15.0)
    data = []
    for row in a:
        for v in row:
            v = v * v * (3 - 2 * v) * 0.5 + v * 0.5        # a softer start of the fall-off
            v = v * 255.0 + random.random() - 0.5          # dither: breaks the 8-bit steps into a fine grain
            data.append(int(min(max(round(v), 0), 255)))
    alpha = Image.new('L', (size, size))
    alpha.putdata(data)
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    im.putalpha(alpha)
    im.save(os.path.join(OUT, 'sh%d.png' % r), optimize=True)
print('shadows rebuilt')
