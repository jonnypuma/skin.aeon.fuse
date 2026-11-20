# -*- coding: utf-8 -*-
"""0.56.53 the scroll bar gutter, Fused Glass style (user, 2026-11-20, on the submenu editor: "It has space for a
potential scrollbar between the two lists. I love that idea, but then you need to make the scrollbar square and fit it
inside those two lines. and then you'd need to add that scrollbar column box ... to all menus").

Skin settings window: a 20 px column between the rows (481-1500) and the right column, with lines at 1500 and 1520;
the rows' scroll bars (9771 ... 9799, 9642) fill it, square (common/white.png, 19 px, 1501-1519, from the title band's
rule to the frame's bottom / the list's end); the right column starts at 1521: the Home menu / Context menu options
(299 wide, text 24 px in), Selected item and the preview cards move 20 right. The editors (fgeditors) and the option
dialogs (fgspot) get their gutters in their own generators. Other looks unchanged.
Run after homeedit_05653.py and skin_previews.py; before btnshadow_05653.py. Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
P = os.path.join(D, 'SkinSettings.xml')
FUSED = os.path.join(D, 'Includes_Fused.xml')
DONE = '<!-- 0.56.53 gutter -->'
TEX_OLD = re.compile(r'<texturesliderbackground border="2" colordiffuse="22ffffff">aeon/track_8.png</texturesliderbackground>\s*'
                     r'<texturesliderbar border="2" colordiffuse="99ffffff">aeon/track_8.png</texturesliderbar>\s*'
                     r'<texturesliderbarfocus border="2" colordiffuse="(\$VAR\[Aeon_SBFocus\]|fg_mark)">aeon/track_8.png</texturesliderbarfocus>')
TEX = '<include condition="$EXP[FGS]">FGS_SBTex</include><include condition="!$EXP[FGS]">FGS_SBTex_Else</include>'
INCLUDES = (
    '\t<!-- 0.56.53 the scroll bar gutter (Fused Glass style): a square bar between two lines; elsewhere the round track -->\n'
    '\t<include name="FGS_SBTex"><texturesliderbackground colordiffuse="0dffffff">common/white.png</texturesliderbackground>'
    '<texturesliderbar colordiffuse="59ffffff">common/white.png</texturesliderbar>'
    '<texturesliderbarfocus colordiffuse="$VAR[Aeon_SBFocus]">common/white.png</texturesliderbarfocus></include>'
    '<include name="FGS_SBTex_Else"><texturesliderbackground border="2" colordiffuse="22ffffff">aeon/track_8.png</texturesliderbackground>'
    '<texturesliderbar border="2" colordiffuse="99ffffff">aeon/track_8.png</texturesliderbar>'
    '<texturesliderbarfocus border="2" colordiffuse="$VAR[Aeon_SBFocus]">aeon/track_8.png</texturesliderbarfocus></include>\n'
    '\t<include name="FGS_W19"><width>19</width></include><include name="FGS_W4_Else"><width>4</width></include>'
    '<include name="FGS_H768"><height>768</height></include><include name="FGS_H758_Else"><height>758</height></include>'
    '<include name="FGS_H699"><height>699</height></include><include name="FGS_H690_Else"><height>690</height></include>'
    '<include name="FGS_W299"><width>299</width></include>\n')


def cond(a, b):
    return '<include condition="$EXP[FGS]">%s</include><include condition="!$EXP[FGS]">%s</include>' % (a, b)


def main():
    s = io.open(P, encoding='utf-8').read()
    if DONE not in s:
        n = 0
        for m in list(re.finditer(r'<control type="scrollbar" id="(97\d\d|9642)">.*?</control>', s, re.S))[::-1]:
            x = m.group(0)
            x2, k = TEX_OLD.subn(TEX, x, count=1)
            if not k:
                continue
            h = cond('FGS_H699', 'FGS_H690_Else') if m.group(1) == '9642' else cond('FGS_H768', 'FGS_H758_Else')
            x2 = re.sub(r'<width>4</width><height>(690|758)</height>', cond('FGS_W19', 'FGS_W4_Else') + h, x2, count=1)
            x2 = re.sub(r'<animation effect="slide" end="-24,0" time="0" condition="\$EXP\[FGS\]">Conditional</animation>',
                        '<animation effect="slide" end="-19,-5" time="0" condition="$EXP[FGS]">Conditional</animation>', x2, count=1)
            s = s[:m.start()] + x2 + s[m.end():]
            n += 1
        # the gutter's second line and its piece of the title band's rule
        line = s.index('<control type="image"><left>1500</left><top>108</top><width>1</width><height>852</height>')
        s = (s[:line] + DONE + '<control type="image"><left>1520</left><top>108</top><width>1</width><height>852</height>'
             '<texture colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture><visible>$EXP[FGS]</visible></control>'
             '<control type="image"><left>1501</left><top>191</top><width>19</width><height>1</height>'
             '<texture colordiffuse="$VAR[FGS_FrameCol]">common/white.png</texture><visible>$EXP[FGS]</visible></control>' + s[line:])
        # the right column 20 px right: option columns, their buttons and lines, the preview cards
        k1 = s.count('<animation effect="slide" end="-35,0" time="0" condition="$EXP[FGS]">Conditional</animation>')
        s = s.replace('<animation effect="slide" end="-35,0" time="0" condition="$EXP[FGS]">Conditional</animation>',
                      '<animation effect="slide" end="-15,0" time="0" condition="$EXP[FGS]">Conditional</animation>')
        s = s.replace('<include condition="$EXP[FGS]">FGS_W319</include>', '<include condition="$EXP[FGS]">FGS_W299</include>')
        s = s.replace('<left>0</left><top>0</top><width>319</width><height>1</height><texture colordiffuse="12ffffff">',
                      '<left>0</left><top>0</top><width>299</width><height>1</height><texture colordiffuse="12ffffff">')
        s = re.sub(r'<left>-40</left><top>-34</top><width>399</width>', '<left>-40</left><top>-34</top><width>379</width>', s)
        k2 = s.count('<animation effect="slide" start="0,0" end="-20,0" time="0" condition="$EXP[FGS]">Conditional</animation>')
        s = s.replace('<animation effect="slide" start="0,0" end="-20,0" time="0" condition="$EXP[FGS]">Conditional</animation>', '')
        s = s.replace('<animation effect="slide" end="47,-33" time="0" condition="$EXP[FGS]">', '<animation effect="slide" end="27,-33" time="0" condition="$EXP[FGS]">')
        io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
        print('gutter: %d scroll bars, %d option columns, %d preview cards' % (n, k1, k2))
    t = io.open(FUSED, encoding='utf-8').read()
    if '<include name="FGS_SBTex">' not in t:
        i = t.index('\t<include name="FGS_RowTex">')
        t = t[:i] + INCLUDES + t[i:]
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)


if __name__ == '__main__':
    main()
