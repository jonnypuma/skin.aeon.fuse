"""Fused Glass variants for the views whose tiles are drawn inline (Showcase 523, Flix 528, Combined 529, Grid 515,
Pictures 516). In each view's layouts: the artwork gets a rounded copy (diffuse mask media/fg/mWxH.png), the dim over it
a rounded copy, the accent / white frame around the focused tile is left out and a 3 px ring (fg/ri16.png) lies inside
the artwork's edge instead. Every original keeps its place with "+ !Fused" added; the copies show with "+ Fused".
Run from 1080i; prints the mask sizes it needs (made by fg_textures.py).
Applied once in 0.30.1; do not run it again. After the run the ring was moved above the artwork in draw order and the
Grid tile (515) got a rounded focus box with the ring at its edge instead of a masked logo (both by hand)."""
import io
import re

F = '$EXP[Aeon_FGlass]'
IMG = re.compile(r'<control type="image">(?:(?!<control ).)*?</control>', re.S)
DIM_COLOURS = ('88000000', '66000000', '99000000', '55000000', '30ffffff')


def geo(ctrl):
    g = dict(re.findall(r'<(left|top|width|height)>(-?\d+)</\1>', ctrl))
    if len(g) != 4:
        return None
    return tuple(int(g[k]) for k in ('left', 'top', 'width', 'height'))


def split_vis(ctrl, cond):
    vis = re.search(r'<visible>(.*?)</visible>', ctrl, re.S)
    if vis:
        return ctrl.replace(vis.group(0), '<visible>[%s] + %s</visible>' % (vis.group(1), cond))
    return ctrl.replace('</control>', '<visible>%s</visible></control>' % cond)


def transform(block, masks):
    ctrls = [(m.start(), m.end(), m.group(0)) for m in IMG.finditer(block)]
    arts = [(geo(c), c) for _, _, c in ctrls if 'background="true"' in c and geo(c)]
    out, pos = [], 0
    for a, b, c in ctrls:
        if 'fg/' in c:
            continue
        g = geo(c)
        tex = re.search(r'<texture([^>]*)>([^<]*)</texture>', c)
        if not g or not tex:
            continue
        attrs, path = tex.group(1), tex.group(2)
        new = None
        if 'background="true"' in attrs:
            masks.add((g[2], g[3]))
            fused = c.replace(tex.group(0), '<texture%s diffuse="fg/m%dx%d.png">%s</texture>' % (attrs, g[2], g[3], path))
            new = split_vis(c, '!' + F) + '\n' + split_vis(fused, F)
        elif path == 'common/white.png' and any('colordiffuse="%s"' % col in attrs for col in DIM_COLOURS) and any(ag == g for ag, _ in arts):
            fused = c.replace(tex.group(0), '<texture border="16"%s>fg/r16.png</texture>' % attrs)
            new = split_vis(c, '!' + F) + '\n' + split_vis(fused, F)
        elif path == 'common/white.png' and ('Aeon_Accent' in attrs or 'aeon_white' in attrs or 'colordiffuse="30ffffff"' in attrs):
            inner = [ag for ag, _ in arts if ag[0] > g[0] and ag[1] > g[1] and ag[0] + ag[2] < g[0] + g[2] and ag[1] + ag[3] < g[1] + g[3]]
            if inner:
                ag = inner[0]
                ring = re.sub(r'<(left|top|width|height)>-?\d+</\1>', lambda m: '<%s>%d</%s>' % (m.group(1), ag[('left', 'top', 'width', 'height').index(m.group(1))], m.group(1)), c)
                ring = ring.replace(tex.group(0), '<texture border="16" colordiffuse="ffffffff">fg/ri16.png</texture>')
                new = split_vis(c, '!' + F) + '\n' + split_vis(ring, F)
            else:
                # a frame without artwork inside (Grid logo tile): a rounded focus box
                fused = c.replace(tex.group(0), '<texture border="16"%s>fg/r16.png</texture>' % attrs)
                new = split_vis(c, '!' + F) + '\n' + split_vis(fused, F)
        if new:
            out.append(block[pos:a])
            out.append(new)
            pos = b
    out.append(block[pos:])
    return ''.join(out)


def region(s, start, end_marker):
    a = s.index(start)
    b = s.index(end_marker, a)
    return a, b


JOBS = [
    ('Includes_Aeon_Views2.xml', '<control type="wraplist" id="523">', '</focusedlayout>'),
    ('Includes_Aeon_Views3.xml', '<control type="fixedlist" id="528">', '</focusedlayout>'),
    ('Includes_Aeon_Views3.xml', '<control type="fixedlist" id="529">', '</focusedlayout>'),
    ('Includes_Aeon_Video.xml', '<include name="Aeon_LogoTile">', '\n\t</include>'),
    ('Includes_Aeon_Pics.xml', '<include name="Aeon_PicCard">', '\n\t</include>'),
]

if __name__ == '__main__':
    masks = set()
    for f, start, end in JOBS:
        s = io.open(f, encoding='utf-8').read()
        a, b = region(s, start, end)
        blk = s[a:b]
        new = transform(blk, masks)
        if new != blk:
            s = s[:a] + new + s[b:]
            io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print(f, start[:40], 'copies:', new.count(F) - blk.count(F))
    print('masks', sorted(masks))
