# -*- coding: utf-8 -*-
"""0.56.53 scroll bars of the Fused Glass library views that scroll sideways (user, 2026-11-20: "in movies Flix view
the scrollbar does not work because there is nothing to scroll down to, it's all horizontal. check for scrolling for
all library views").

Checked every library view's list against its bar (the list's <pagecontrol>):
- Flix (528): its bar 5280050 belonged to no list; 529 (5290050) and the 518 strip 5181 (5180051) scroll sideways
  with an upright bar. Each gets a level bar under its row (the row's left and width, 10 below it), the list's
  pagecontrol where it had none, Up back to the list.
- Showcase (523) and the music Showcase (531) are wrap lists (they go round, no first or last): their bars
  (5230050, 5310050) belonged to no list and stood still; they go.
- The upright views (510-536 lists and panels) keep their bars; each is its list's pagecontrol.
Run after the fg_lib* generators. Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Fused.xml')
LEVEL = (('528', '5280050', '5280001'), ('529', '5290050', '5290001'), ('5181', '5180051', '5181'))
GONE = ('5230050', '5310050')


def main():
    s = io.open(P, encoding='utf-8').read()
    n = 0
    for cid, bar, back in LEVEL:
        m = re.search(r'<control type="(\w+)" id="%s">' % cid, s)
        head = s[m.end():m.end() + 400]
        geo = re.match(r'\s*(?:<pagecontrol>\d+</pagecontrol>)?<left>(-?\d+)</left><top>(-?\d+)</top><width>(\d+)</width><height>(\d+)</height>', head)
        left, top, width, height = (int(g) for g in geo.groups())
        if '<pagecontrol>' not in s[m.end():s.index('<itemlayout', m.end())]:
            s = s[:m.end()] + '<pagecontrol>%s</pagecontrol>' % bar + s[m.end():]
        i = s.index('<control type="scrollbar" id="%s">' % bar)
        e = s.index('</control>', i)
        x = s[i:e]
        if '<orientation>horizontal</orientation>' in x:
            x2 = x.replace('<texturesliderbackground colordiffuse="00ffffff">', '<texturesliderbackground colordiffuse="1affffff">', 1)
            s = s[:i] + x2 + s[e:]
            continue
        x = re.sub(r'<left>-?\d+</left><top>-?\d+</top><width>\d+</width><height>\d+</height>',
                   '<left>%d</left><top>%d</top><width>%d</width><height>5</height>' % (left, top + height + 10, width), x, count=1)
        x = x.replace('<orientation>vertical</orientation>', '<orientation>horizontal</orientation>', 1)
        x = x.replace('<texturesliderbackground colordiffuse="00ffffff">', '<texturesliderbackground colordiffuse="1affffff">', 1)   # the track shows: a big library's bar is a few px
        x = re.sub(r'<onleft>[^<]*</onleft><onright>[^<]*</onright>', '<onup>%s</onup><ondown>noop</ondown>' % back, x, count=1)
        s = s[:i] + x + s[e:]
        n += 1
    for bar in GONE:
        i = s.index('<control type="scrollbar" id="%s">' % bar)
        e = s.index('</control>', i)
        if '<visible>false</visible>' not in s[i:e]:
            s = s[:e] + '<visible>false</visible>' + s[e:]
            n += 1
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('library bars changed: %d' % n)


if __name__ == '__main__':
    main()
