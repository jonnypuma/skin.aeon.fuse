# -*- coding: utf-8 -*-
"""0.40.4: Kodi's own toast icons. Kodi's info / warning / error notifications ask the skin for DefaultIconInfo.png,
DefaultIconWarning.png and DefaultIconError.png; the skin had none, so those toasts showed an empty icon slot.
Rounded tiles with a white glyph (drawn as shapes, no font), 128 x 128, made at 4x and scaled down.
They read on the white Aeon bar, the dark Glass fade and Fused Glass's capsule (cut to a circle there).
Run from the skin folder."""
import os

from PIL import Image, ImageDraw, ImageFilter

S = 4
N = 128 * S
TILES = {
    'DefaultIconInfo.png': ((88, 128, 186), (62, 96, 150), 'i'),
    'DefaultIconWarning.png': ((232, 168, 56), (196, 128, 28), '!'),
    'DefaultIconError.png': ((214, 86, 66), (170, 52, 40), 'x'),
}


def tile(top, bottom):
    grad = Image.new('RGBA', (N, N))
    d = ImageDraw.Draw(grad)
    for y in range(N):
        k = y / (N - 1.0)
        d.line([(0, y), (N, y)], fill=tuple(int(round(a + (b - a) * k)) for a, b in zip(top, bottom)) + (255,))
    mask = Image.new('L', (N, N), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, N - 1, N - 1], radius=28 * S, fill=255)
    out = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out, mask


def glyph(kind):
    g = Image.new('L', (N, N), 0)
    d = ImageDraw.Draw(g)
    c = N // 2
    w = 14 * S
    if kind == 'i':
        d.ellipse([c - 9 * S, 28 * S, c + 9 * S, 46 * S], fill=255)
        d.rounded_rectangle([c - w // 2, 56 * S, c + w // 2, 100 * S], radius=w // 2, fill=255)
    elif kind == '!':
        d.rounded_rectangle([c - w // 2, 26 * S, c + w // 2, 76 * S], radius=w // 2, fill=255)
        d.ellipse([c - 9 * S, 84 * S, c + 9 * S, 102 * S], fill=255)
    else:
        bar = Image.new('L', (N, N), 0)
        ImageDraw.Draw(bar).rounded_rectangle([c - w // 2, 30 * S, c + w // 2, N - 30 * S], radius=w // 2, fill=255)
        g = Image.composite(Image.new('L', (N, N), 255), g, bar.rotate(45, resample=Image.BICUBIC, center=(c, c)))
        g = Image.composite(Image.new('L', (N, N), 255), g, bar.rotate(-45, resample=Image.BICUBIC, center=(c, c)))
    return g


def make(name, top, bottom, kind):
    base, mask = tile(top, bottom)
    gl = glyph(kind)
    shadow = Image.new('L', (N, N), 0)
    shadow.paste(gl, (0, 3 * S))
    shadow = shadow.filter(ImageFilter.GaussianBlur(3 * S))
    dark = Image.new('RGBA', (N, N), (20, 12, 8, 0))
    dark.putalpha(shadow.point(lambda v: int(v * 0.4)))
    base = Image.alpha_composite(base, dark)
    white = Image.new('RGBA', (N, N), (255, 255, 255, 0))
    white.putalpha(gl)
    base = Image.alpha_composite(base, white)
    base.putalpha(Image.composite(base.getchannel('A'), Image.new('L', (N, N), 0), mask))
    path = os.path.join('media', name)
    base.resize((128, 128), Image.LANCZOS).save(path, optimize=True)
    return path


for name, (top, bottom, kind) in TILES.items():
    print('wrote', make(name, top, bottom, kind))
