# -*- coding: utf-8 -*-
"""0.56.53 the focus shadow under every Fused Glass style button bar (user, 2026-11-20: "the focus highlight bar has
gotten dark overlay on it. and some shadow. that is really nice looking actually and i want that everywhere too").

Rows draw their shadow as an image (fg/sh16.png, FG_ShadowColM, 40 px out at the sides, 34 above, 46 below) and
FGS_ShadowOn now lets it show in the style. Buttons draw their bar as a texture (FGS_BtnFocus), so each one whose
parent is a plain group (an image in a grouplist would take a slot) gets that image just before it, shown while it
has the focus in the style. Run after the generators that write such buttons (homeedit, fgeditors, fgspot).
Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
TAG = re.compile(r'<control type="(\w+)"(?: id="(\d+)")?>|</control>|<include>FGS_BtnFocus</include>|<include condition="\$EXP\[FGS\]">FGS_BtnFocus</include>')
VAL = {'FGS_W319': 319, 'FGS_W1019': 1019, 'FGS_H70': 70, 'FGS_H770': 770}
MARK = '<!-- btnshadow %s -->'


def geometry(x):
    out = {}
    for k in ('left', 'top', 'width', 'height'):
        m = re.search(r'<%s>(-?\d+)</%s>' % (k, k), x)
        if m:
            out[k] = int(m.group(1))
    for name, v in VAL.items():
        if '<include condition="$EXP[FGS]">%s</include>' % name in x:
            out['width' if name.startswith('FGS_W') else 'height'] = v
    return out


def run(t):
    stack, hits = [], []
    for m in TAG.finditer(t):
        g = m.group(0)
        if g == '</control>':
            if stack:
                stack.pop()
        elif g.startswith('<control'):
            stack.append((m.group(1), m.group(2), m.start()))
        elif stack and stack[-1][0] == 'button':
            parent = stack[-2][0] if len(stack) > 1 else 'root'
            if parent != 'grouplist':
                hits.append(stack[-1])
    n = 0
    for _, bid, at in sorted(hits, key=lambda h: -h[2]):
        if MARK % bid in t[max(0, at - 400):at]:
            continue
        end = t.index('</control>', at)
        g = geometry(t[at:end])
        if 'width' not in g or 'height' not in g:
            continue
        img = ('%s<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
               '<texture border="56" colordiffuse="$VAR[FG_ShadowColM]">fg/sh16.png</texture>'
               '<visible>Control.HasFocus(%s) + $EXP[FGS] + $EXP[FGS_ShadowOn]</visible></control>'
               % (MARK % bid, g.get('left', 0) - 40, g.get('top', 0) - 34, g['width'] + 80, g['height'] + 80, bid))
        t = t[:at] + img + t[at:]
        n += 1
    return t, n


def main():
    for name in sorted(os.listdir(D)):
        if not name.endswith('.xml'):
            continue
        p = os.path.join(D, name)
        t = io.open(p, encoding='utf-8').read()
        if 'FGS_BtnFocus' not in t:
            continue
        t2, n = run(t)
        if n:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t2)
            print('%-28s %d button shadows' % (name, n))


if __name__ == '__main__':
    main()
