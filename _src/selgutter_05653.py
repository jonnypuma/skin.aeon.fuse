# -*- coding: utf-8 -*-
"""0.56.53 Select (and the dialogs built on FGS_SelList) in Fused Glass style (user, 2026-11-20: the scroll bar gutter
"for all of Kodi's standard menus too", "and the focus bar dark background there too as well"):
- the list 360-1540 (rows 1180, their texts end 20 sooner), a gutter 1540-1560 between two lines with the square bar
  61 (19 wide), the frame's left line at 360 (it had none);
- the focused row (Select, Add-ons) gets the focus shadow under its lines (fg/sh16.png, FG_ShadowColM): the dark fill.
Repeatable."""
import io
import os
import re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Fused.xml')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Views.xml')
SH = ('<control type="image"><left>-40</left><top>-34</top><width>%d</width><height>150</height>'
      '<texture border="56" colordiffuse="$VAR[FG_ShadowColM]">fg/sh16.png</texture><visible>$EXP[FGS_ShadowOn]</visible></control>')


def block(t, name):
    i = t.index('<include name="%s">' % name)
    e = t.index('\n\t</include>', i)
    return i, e


def main():
    t = io.open(P, encoding='utf-8').read()
    i, e = block(t, 'FGS_SelRow')
    seg = t[i:e]
    if '<!-- selgutter -->' not in seg:
        seg = seg.replace('<width>1200</width>', '<width>1180</width>')
        seg = seg.replace('<left>900</left><top>0</top><width>264</width>', '<left>880</left><top>0</top><width>264</width>')
        seg = seg.replace('<width>678</width>', '<width>658</width>')
        seg = seg.replace('<include>FGS_RowAnim</include>', '<include>FGS_RowAnim</include><!-- selgutter -->' + SH % 1260, 1)
        t = t[:i] + seg + t[e:]
    i, e = block(t, 'FGS_SelList')
    seg = t[i:e]
    if '<!-- selgutter -->' not in seg:
        seg = seg.replace('<left>360</left><top>181</top><width>1200</width><height>700</height>',
                          '<left>360</left><top>181</top><width>1180</width><height>700</height>', 1)
        seg = seg.replace('<itemlayout width="1200"', '<itemlayout width="1180"').replace('<focusedlayout width="1200"', '<focusedlayout width="1180"')
        seg = seg.replace('<left>360</left><top>180</top><width>1200</width><height>1</height><texture colordiffuse="44ffffff">',
                          '<left>360</left><top>180</top><width>1180</width><height>1</height><texture colordiffuse="44ffffff">')
        seg = seg.replace('<definition>', '<definition><!-- selgutter -->', 1)
        t = t[:i] + seg + t[e:]
    i, e = block(t, 'FGS_Select')
    seg = t[i:e]
    if '<!-- selgutter -->' not in seg:
        seg = re.sub(r'<control type="scrollbar" id="61">\s*<left>1556</left><top>181</top><width>4</width><height>700</height>\s*'
                     r'<texturesliderbackground[^>]*>[^<]*</texturesliderbackground>\s*<texturesliderbar [^>]*>[^<]*</texturesliderbar>\s*'
                     r'<texturesliderbarfocus[^>]*>[^<]*</texturesliderbarfocus>',
                     '<!-- selgutter --><control type="image"><left>360</left><top>180</top><width>1</width><height>702</height>'
                     '<texture colordiffuse="1affffff">common/white.png</texture></control>'
                     '<control type="image"><left>1540</left><top>180</top><width>1</width><height>702</height>'
                     '<texture colordiffuse="1affffff">common/white.png</texture></control>'
                     '<control type="image"><left>1560</left><top>180</top><width>1</width><height>702</height>'
                     '<texture colordiffuse="1affffff">common/white.png</texture></control>'
                     '<control type="image"><left>361</left><top>881</top><width>1199</width><height>1</height>'
                     '<texture colordiffuse="1affffff">common/white.png</texture></control>'
                     '<control type="scrollbar" id="61"><left>1541</left><top>181</top><width>19</width><height>700</height>'
                     '<include>FGS_SBTex</include>', seg, count=1)
        t = t[:i] + seg + t[e:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    v = io.open(V, encoding='utf-8').read()
    i, e = block(v, 'FGS_AddonRow')
    seg = v[i:e]
    if '<!-- selgutter -->' not in seg:
        k = seg.index('<include>FGS_RowAnim</include>')
        seg = seg[:k] + '<include>FGS_RowAnim</include><!-- selgutter -->' + SH % 1260 + seg[k + len('<include>FGS_RowAnim</include>'):]
        v = v[:i] + seg + v[e:]
        io.open(V, 'w', encoding='utf-8', newline='\n').write(v)
    print('select gutter + row shadows')


if __name__ == '__main__':
    main()
