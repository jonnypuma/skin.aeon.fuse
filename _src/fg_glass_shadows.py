# -*- coding: utf-8 -*-
"""0.56.5 Fused Glass: a panel's drop shadow is an outline round it, never a dark sheet under it.

The user (2026-11-16): library views look like "dark overlay" panels while Episode combined looks like glass; "the
drop shadow should just be a single outline gradient texture. around the panel. glass shall be glass", "the episode
combined looks like i expect glass to look like for all views".
Why: the panel shadows (fg/sh16 / sh24 / sh28 / sh32, colordiffuse FG_PanelSh_xx, up to 8c000000) are a blurred
rounded rectangle that is solid in the middle (alpha ~250), drawn under the see-through frosted panels: every panel
sat on a 55 % black sheet, whatever the material. Episode combined draws no panel shadows, so only it looked like glass.
Now:
  - fg/sho<r>.png (r = the panel's corner radius): the same soft fall-off, but only outside the panel (the panel's
    rounded rectangle is cut out of it), margin 40, 9-slice border 40 + r.
  - every panel shadow (FG_PanelSh_xx) right under a panel picture fg/r<r>.png in the same group is redrawn as that
    outline: the panel's rectangle grown by 40 on every side (it was offset down as a drop shadow; a drop shadow under
    glass shows through it).
Run from the skin folder; safe to run again."""
import io
import math
import os
import random
import re

from PIL import Image

D = '1080i'
OUT = os.path.join('media', 'fg')
M = 40

IMG = re.compile(r'<control type="image">(?:<left>(-?\d+)</left>)?(?:<top>(-?\d+)</top>)?<width>(\d+)</width>'
                 r'<height>(\d+)</height>(<texture[^>]*>)(fg/sh\d+\.png|fg/r(\d+)\.png)</texture>')
LINE_IMAGE = re.compile(r'^\s*(?:<control type="image">[^\n]*?</control>\s*)*$')


def only_images(gap):
    """nothing but single-line pictures between the shadow and the panel (so both sit in the same group)"""
    return len(gap) < 6000 and all(LINE_IMAGE.match(line) for line in gap.split('\n'))


def outline(r):
    """the panel's rounded rectangle (radius r) blurred like fg_shadows.py, with the rectangle itself cut out"""
    random.seed(11 + r)
    n = 2 * r + 16
    size = n + 2 * M
    ss = 4
    # the panel shape at 4x, then down: the antialiased cut-out
    big = Image.new('L', (size * ss, size * ss), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(big).rounded_rectangle([M * ss, M * ss, (M + n) * ss - 1, (M + n) * ss - 1], radius=r * ss, fill=255)
    shape = big.resize((size, size), Image.LANCZOS)
    from PIL import ImageFilter
    soft = shape.filter(ImageFilter.GaussianBlur(15))
    sp, hp = soft.load(), shape.load()
    alpha = Image.new('L', (size, size))
    ap = alpha.load()
    for y in range(size):
        for x in range(size):
            v = sp[x, y] / 255.0
            v = v * v * (3 - 2 * v) * 0.5 + v * 0.5             # the softer start of fg_shadows.py
            v *= 1.0 - hp[x, y] / 255.0                         # nothing under the panel
            v = v * 255.0 + random.random() - 0.5
            ap[x, y] = int(min(max(round(v), 0), 255))
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    im.putalpha(alpha)
    name = 'sho%d.png' % r
    im.save(os.path.join(OUT, name), optimize=True)
    return name


def run():
    made = {}
    total = 0
    for fname in sorted(os.listdir(D)):
        if not fname.endswith('.xml'):
            continue
        p = os.path.join(D, fname)
        t = io.open(p, encoding='utf-8').read()
        out, pos, n = [], 0, 0
        ms = list(IMG.finditer(t))
        for i, m in enumerate(ms):
            if not m.group(6).startswith('fg/sh') or 'FG_PanelSh_' not in m.group(5):
                continue
            # the panel: the next picture fg/r<r>.png, with only single-line pictures in between (same group)
            panel = None
            for nx in ms[i + 1:i + 4]:
                gap = t[t.find('</control>', m.end()) + len('</control>'):nx.start()]
                if not only_images(gap):
                    break
                if nx.group(7):
                    panel = nx
                    break
            if panel is None:
                continue
            px, py, pw, ph = (int(panel.group(k) or 0) for k in (1, 2, 3, 4))
            r = int(panel.group(7))
            if r not in made:
                made[r] = outline(r)
            col = re.search(r'colordiffuse="([^"]+)"', m.group(5)).group(1)
            new = ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
                   '<texture border="%d" colordiffuse="%s">fg/%s</texture>' % (px - M, py - M, pw + 2 * M, ph + 2 * M, M + r, col, made[r]))
            out.append(t[pos:m.start()] + new)
            pos = m.end()
            n += 1
        out.append(t[pos:])
        t2 = ''.join(out)
        # the shared menu / dialog card (Includes_Aeon_Glass): shadow and card sized by right / bottom
        def edges(mm):
            nonlocal n
            r = int(mm.group(3))
            if r not in made:
                made[r] = outline(r)
            n += 1
            return ('<control type="image"><left>-%d</left><top>-%d</top><right>-%d</right><bottom>-%d</bottom>'
                    '<texture border="%d" colordiffuse="%s">fg/%s</texture>%s' % (M, M, M, M, M + r, mm.group(1), made[r], mm.group(2)))
        t2 = re.sub(r'<control type="image"><left>-?\d+</left><top>-?\d+</top><right>-?\d+</right><bottom>-?\d+</bottom>'
                    r'<texture border="\d+" colordiffuse="(\$VAR\[FG_PanelSh_[0-9a-f]+\])">fg/sh\d+\.png</texture>(.*?</control>\s*'
                    r'<control type="image"><left>0</left><top>0</top><right>0</right><bottom>0</bottom><texture border="\d+" '
                    r'colordiffuse="[^"]*">fg/r(\d+)\.png)', edges, t2)
        if n:
            out = [t2]
            io.open(p, 'w', encoding='utf-8', newline='\n').write(''.join(out))
            print('%-34s %d panel shadows -> outlines' % (fname, n))
            total += n
    # the outlines already written (a second run finds them as fg/sho*.png: the pattern above skips them)
    print('total', total, 'outline pictures', sorted(made.values()))


if __name__ == '__main__':
    run()
