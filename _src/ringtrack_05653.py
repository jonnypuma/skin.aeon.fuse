# -*- coding: utf-8 -*-
"""0.56.53 the in-progress rings of the Aeon / Aeon Glass library views (list rows, wall tiles, panes) drew only the
progress arc (fg/pring/<percent>.png), so a film 8 % in showed a small orange sliver and no circle (user,
2026-11-19: "the in progress logo on that row is only showing the progress but not the outline"). Every such arc
without a track gets fg/pring/track.png under it: same place, size and visibility, the arc's own colour at 35 %
(so it reads on the dark rows and on the light focus bar alike). Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
FILES = ('Includes_Aeon_Views2.xml', 'Includes_Aeon_Video.xml', 'Includes_Aeon_Sub.xml', 'Includes_Aeon_Home.xml')
ARC = re.compile(r'<control type="image">((?:(?!<control).)*?)<texture colordiffuse="([^"]*)">fg/pring/\$INFO\[[^\]]*\]\.png</texture>'
                 r'((?:(?!<control).)*?)</control>', re.S)
FADE = '<animation effect="fade" start="100" end="35" time="0" condition="true">Conditional</animation>'
MARK = '<!-- 0.56.53 ring track -->'


def main():
    total = 0
    for f in FILES:
        p = os.path.join(D, f)
        s = io.open(p, encoding='utf-8').read()
        out, last, n = [], 0, 0
        for m in ARC.finditer(s):
            before = s[max(0, m.start() - 6000):m.start()]
            if 'fg/pring/track.png' in before[before.rfind('<control'):] if '<control' in before else False:
                continue
            if MARK in s[max(0, m.start() - len(MARK) - 4):m.start()]:
                continue
            head, colour, tail = m.group(1), m.group(2), m.group(3)
            track = ('%s<control type="image">%s<texture colordiffuse="%s">fg/pring/track.png</texture>%s%s</control>'
                     % (MARK, head, colour, FADE, tail))
            out.append(s[last:m.start()])
            out.append(track)
            last = m.start()
            n += 1
        if n:
            out.append(s[last:])
            io.open(p, 'w', encoding='utf-8', newline='\n').write(''.join(out))
            print('%-28s %d ring tracks' % (f, n))
            total += n
    print('ring tracks added: %d' % total)


if __name__ == '__main__':
    main()
