# -*- coding: utf-8 -*-
"""0.56.53 Fused Glass List view (FG_V510_View): the chevron that says Left opens a film's versions / a set's films
(sets_05648) sat on the poster's right edge, a dark circle on a dark poster, so it went unseen (user, 2026-11-19:
"missing a left chevron between poster and list to signal several versions available"). It now sits in the gap
between the poster card (ends 683) and the list card (starts 723): a 36 circle, light glass, white chevron.
Repeatable."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Fused.xml')
OLD = ('<control type="image"><left>623</left><top>576</top><width>48</width><height>48</height>'
       '<texture colordiffuse="%s">fg/circle.png</texture></control><control type="image"><left>635</left><top>588</top>'
       '<width>24</width><height>24</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/chevron_left.png</texture></control>')
NEW = ('<!-- 0.56.53 chevron in the gap -->'
       '<control type="image"><left>685</left><top>582</top><width>36</width><height>36</height>'
       '<texture colordiffuse="59ffffff">fg/circle.png</texture></control><control type="image"><left>693</left><top>590</top>'
       '<width>20</width><height>20</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/chevron_left.png</texture></control>')


def main():
    s = io.open(P, encoding='utf-8').read()
    if '0.56.53 chevron in the gap' in s:
        print('chevron: already there')
        return
    a = s.index('<include name="FG_V510_View">')
    i = s.index('aeon/icons/chevron_left.png', a)
    st = s.rfind('<control type="image"><left>623</left>', a, i)
    e = s.index('</control>', i) + len('</control>')
    old = s[st:e]
    import re
    col = re.search(r'colordiffuse="([^"]*)">fg/circle.png', old).group(1)
    assert old == OLD % col, old
    s = s[:st] + NEW + s[e:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('chevron: moved into the gap (circle was %s)' % col)


if __name__ == '__main__':
    main()
