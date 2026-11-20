# -*- coding: utf-8 -*-
"""0.56.53 the Fused Glass wall views' info strip (Poster wall 520, Landscape wall 521, Showcase 523, Square wall 525,
Cards 526), user 2026-11-19: "move the clearlogo to the top right of the panel and the studio logo beneath it in the
lower right corner".
- clear logo: 230 x 100 at the strip's top right (right edge 1776, top = the kicker's), right / top aligned;
- with a clear logo the left column no longer makes room for it: its kicker and meta lines (320 wide beside the logo)
  are the full 560 again, the kicker on the first line;
- studio logo (and its text fallback): the strip's lower right corner (bottom 24 px in from the strip's 1040);
- the plot / tagline end 24 px before the clear logo (806 wide from 716; the Showcase's centred variant 616 from 906);
- the chip lines under the column (1656 wide, chipline2 widen_strips) end 24 px before the studio logo (1452).
The same for the Aeon / Aeon Glass wall views (one panel, Aeon_V_Info in Includes_Aeon_Views2.xml): the clear logo
(380 x 92, logos on) takes the panel's top right where the studio logo was, the studio logo (and its text) goes beneath
it, and the title / ratings / media line / plot end at 1280, before the logos (the title stays: the Aeon look).
Run after chipline2_05653.py (and after the view generators). Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Fused.xml')
VIEWS = ('520', '521', '523', '525', '526')
MARK = '<!-- 0.56.53 walls: clear logo top right, studio logo lower right -->'
RIGHT = 1776
LOGO_W, LOGO_H = 230, 100
STUDIO_W, STUDIO_H, STRIP_BOTTOM, PAD = 180, 84, 1040, 24


def one(seg, c):
    k = re.search(r'<control type="label"><left>120</left><top>(\d+)</top><width>560</width><height>26</height>', seg)
    top = int(k.group(1))                                   # the kicker's top: the strip's first line
    n = 0
    # clear logo -> top right
    def logo(m):
        x = m.group(0)
        x = re.sub(r'<left>450</left><top>\d+</top>', '<left>%d</left><top>%d</top>' % (RIGHT - LOGO_W, top), x, count=1)
        if '<aspectratio' in x:
            x = re.sub(r'<aspectratio[^>]*>', '<aspectratio align="right" aligny="top">', x, count=1)
        else:
            x = x.replace('<texture', '<aspectratio align="right" aligny="top">keep</aspectratio><texture', 1)
        return x
    seg, k1 = re.subn(r'<control type="image"><left>450</left><top>\d+</top><width>230</width><height>100</height>'
                      r'(?:(?!<control).)*?Art\(clearlogo\)(?:(?!<control).)*?</control>', logo, seg, flags=re.S)
    n += k1
    # the left column's 320-wide lines (beside the old logo place) -> full width; the kicker on the first line
    seg, k2 = re.subn(r'<control type="label"><left>120</left><top>(\d+)</top><width>320</width>',
                      lambda m: '<control type="label"><left>120</left><top>%s</top><width>560</width>'
                      % (top if int(m.group(1)) < top + 40 else m.group(1)), seg)
    n += k2
    # studio logo + text -> lower right corner
    st = STRIP_BOTTOM - PAD - STUDIO_H
    seg, k3 = re.subn(r'<control type="image"><left>1596</left><top>\d+</top><width>180</width><height>84</height>',
                      '<control type="image"><left>1596</left><top>%d</top><width>180</width><height>84</height>' % st, seg)
    seg, k4 = re.subn(r'<control type="label"><left>1576</left><top>\d+</top><width>200</width><height>84</height>',
                      '<control type="label"><left>1576</left><top>%d</top><width>200</width><height>84</height>' % st, seg)
    n += k3 + k4
    # plot / tagline end before the logo
    pw = RIGHT - LOGO_W - PAD - 716
    seg, k5 = re.subn(r'<control type="(label|textbox)"><left>716</left><top>(\d+)</top><width>(?:1060|844)</width>',
                      lambda m: '<control type="%s"><left>716</left><top>%s</top><width>%d</width>' % (m.group(1), m.group(2), pw), seg)
    cw = RIGHT - LOGO_W - PAD - 906
    seg, k6 = re.subn(r'<control type="(label|textbox)"><left>906</left><top>(\d+)</top><width>(?:870|654)</width>',
                      lambda m: '<control type="%s"><left>906</left><top>%s</top><width>%d</width>' % (m.group(1), m.group(2), cw), seg)
    n += k5 + k6
    # chip lines end before the studio logo
    seg, k7 = re.subn(r'<control type="grouplist"><left>120</left><top>(\d+)</top><width>1656</width>',
                      lambda m: '<control type="grouplist"><left>120</left><top>%s</top><width>%d</width>'
                      % (m.group(1), 1596 - PAD - 120), seg)
    n += k7
    return seg, (k1, k2, k3 + k4, k5 + k6, k7)


AEON = os.path.join(os.path.dirname(P), 'Includes_Aeon_Views2.xml')


def aeon():
    s = io.open(AEON, encoding='utf-8').read()
    if MARK in s:
        return 'aeon walls: already there'
    a = s.index('<include name="Aeon_V_Info">')
    b = s.index('<include name=', a + 10)
    seg = s[a:b]
    st = '<control type="image"><left>1300</left><top>4</top><width>380</width><height>92</height>'
    assert seg.count(st) == 1, 'studio logo not found'
    logo = ('%s<control type="image"><left>1300</left><top>4</top><width>380</width><height>92</height>'
            '<aspectratio align="right" aligny="top">keep</aspectratio><texture background="true">'
            '$INFO[ListItem.Art(clearlogo)]</texture><visible>$EXP[FG_L_LogosOn] + !String.IsEmpty(ListItem.Art(clearlogo)) + '
            '!String.IsEqual(ListItem.DBType,season) + !String.IsEqual(ListItem.DBType,episode)</visible></control>' % MARK)
    seg = seg.replace(st, logo + st.replace('<top>4</top>', '<top>120</top>'), 1)
    seg = seg.replace('<control type="label"><left>1080</left><top>10</top><width>600</width><height>28</height>',
                      '<control type="label"><left>1080</left><top>152</top><width>600</width><height>28</height>', 1)
    seg = seg.replace('<control type="label"><left>0</left><top>36</top><width>1340</width>',
                      '<control type="label"><left>0</left><top>36</top><width>1280</width>', 1)
    seg = seg.replace('<control type="label"><left>0</left><top>10</top><width>1320</width>',
                      '<control type="label"><left>0</left><top>10</top><width>1280</width>', 1)
    seg = re.sub(r'<control type="(grouplist|textbox)"><left>0</left><top>(\d+)</top><width>1680</width>',
                 lambda m: '<control type="%s"><left>0</left><top>%s</top><width>1280</width>' % (m.group(1), m.group(2)), seg)
    io.open(AEON, 'w', encoding='utf-8', newline='\n').write(s[:a] + seg + s[b:])
    return 'aeon walls: clear logo top right, studio logo beneath, lines to 1280'


def main():
    print(aeon())
    s = io.open(P, encoding='utf-8').read()
    if MARK in s:
        print('walls: already there')
        return
    for c in VIEWS:
        a = s.index('<include name="FG_V%s_View">' % c)
        b = s.find('<include name=', a + 10)
        b = len(s) if b < 0 else b
        seg, counts = one(s[a:b], c)
        print('view %s: logo %d, column lines %d, studio %d, plot %d, chip lines %d' % ((c,) + counts))
        s = s[:a] + seg + s[b:]
    i = s.index('<include name="FG_V520_View">')
    s = s[:i] + MARK + '\n\t' + s[i:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)


if __name__ == '__main__':
    main()
