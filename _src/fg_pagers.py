"""Fused Glass pagers (0.32.0). Run once from 1080i. The pagers of Home (spotlights, Planner) and of the widget screens
(1157) draw a ring on the current item and a dot for each other one, with a pulsing glow circle; in Fused Glass the
current item is a short white pill (fg/pillh.png) and the others small dots, as on the screensaver. Every ring / dot /
glow image keeps its place for Aeon and Glass ("+ !Fused"); the Fused copy sits next to it."""
import io
import re

F = '$EXP[Aeon_FGlass]'
LINE = re.compile(r'^([ \t]*)(<control type="image">.*?</control>)[ \t]*$', re.M)


def geo(c):
    g = dict(re.findall(r'<(left|top|width|height)>(-?\d+)</\1>', c))
    return {k: int(v) for k, v in g.items()}


def vis(c):
    m = re.search(r'<visible>(.*)</visible>', c)
    return m.group(1) if m else ''


def with_vis(c, cond):
    m = re.search(r'<visible>(.*)</visible>', c)
    if m:
        return c.replace(m.group(0), '<visible>[%s] + %s</visible>' % (m.group(1), cond), 1)
    return c.replace('</control>', '<visible>%s</visible></control>' % cond, 1)


def convert(text):
    n = 0

    def one(m):
        nonlocal n
        indent, c = m.group(1), m.group(2)
        if F in c:
            return m.group(0)
        g = geo(c)
        if not all(k in g for k in ('left', 'top', 'width', 'height')):
            return m.group(0)
        v = vis(c)
        if 'common/aeon_ring.png' in c and g['width'] <= 30:
            w = g['width'] - 4
            new = ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>6</height><texture border="3" colordiffuse="ffffffff">fg/pillh.png</texture><visible>[%s] + %s</visible></control>'
                   % (g['left'] + 2, g['top'] + g['height'] // 2 - 3, w, v or 'true', F))
        elif 'common/aeon_dot.png' in c and g['width'] <= 12:
            new = ('<control type="image"><left>%d</left><top>%d</top><width>6</width><height>6</height><texture colordiffuse="73ffffff">fg/circle.png</texture><visible>[%s] + %s</visible></control>'
                   % (g['left'] + g['width'] // 2 - 3, g['top'] + g['height'] // 2 - 3, v or 'true', F))
        elif 'aeon/circle_24.png' in c and g['width'] in (26, 30, 46, 52) and ('38ffffff' in c or '66ffffff' in c):
            new = ''
        else:
            return m.group(0)
        n += 1
        out = indent + with_vis(c, '!' + F)
        return out + ('\n' + indent + new if new else '')
    return LINE.sub(one, text), n


if __name__ == '__main__':
    for path in ('Includes_Aeon_Home.xml', 'Custom_1157_Spotlight.xml'):
        s = io.open(path, encoding='utf-8').read()
        s2, n = convert(s)
        io.open(path, 'w', encoding='utf-8', newline='').write(s2)
        print(path, n)
