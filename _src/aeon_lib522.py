# -*- coding: utf-8 -*-
"""0.56.14 the Aeon theme's Banner list (522) rows to the list row rule (canvas HJTtCDChVWkaZZAyt76wJA): a banner row has
no columns, so the status sits on the banner, at its top right, as in Fused Glass: a dark square with the eye, or the
yellow ring while in progress. The versions icon moves left when the status shows.
Run from the skin folder after aeon_lib_lists.py; runs once."""
import io
import os
import xml.etree.ElementTree as ET

V2 = os.path.join('1080i', 'Includes_Aeon_Views2.xml')
MARK = '0.56.14 aeon_lib522'
PROG = 'Integer.IsGreater(ListItem.PercentPlayed,0)'
SHOW = '[$EXP[Aeon_ShowWatch] | %s]' % PROG


def main():
    v = io.open(V2, encoding='utf-8').read()
    if MARK in v:
        print('already done')
        return
    a = v.index('<include name="Aeon_V_BannerRow">')
    b = v.index('\t</include>', a)
    row = v[a:b]
    old = '<control type="image"><left>650</left><top>14</top><width>36</width><height>36</height><aspectratio>keep</aspectratio><texture>common/aeon_layers.png</texture><visible>String.IsEqual(ListItem.DBType,movie) + ListItem.HasVideoVersions</visible></control>'
    assert row.count(old) == 1
    new = (old.replace('</visible>', ' + !%s</visible>' % SHOW) + '\n\t\t\t' +
           old.replace('<left>650</left><top>14</top>', '<left>604</left><top>18</top>').replace('</visible>', ' + %s</visible>' % SHOW))
    row = row.replace(old, new)
    badge = ('\t\t\t<!-- %s: the status at the banner\'s top right: the eye, or the yellow ring while in progress -->\n'
             '\t\t\t<control type="image"><left>652</left><top>12</top><width>48</width><height>48</height><texture colordiffuse="b3080a0e">common/white.png</texture><visible>%s + !$EXP[Aeon_FGlass]</visible></control>\n'
             '\t\t\t<control type="image"><left>662</left><top>22</top><width>28</width><height>28</height><aspectratio>keep</aspectratio><texture colordiffuse="e6ffffff">$VAR[Aeon_WatchIcon]</texture><visible>$EXP[Aeon_ShowWatch] + !%s + !$EXP[Aeon_FGlass]</visible></control>\n'
             '\t\t\t<control type="image"><left>662</left><top>22</top><width>28</width><height>28</height><texture colordiffuse="fg_mark">fg/pring/$INFO[ListItem.PercentPlayed].png</texture><visible>%s + !$EXP[Aeon_FGlass]</visible></control>\n'
             % (MARK, SHOW, PROG, PROG))
    d = row.rindex('\t\t</definition>')
    row = row[:d] + badge + row[d:]
    v = v[:a] + row + v[b:]
    io.open(V2, 'w', encoding='utf-8', newline='\n').write(v)
    ET.parse(V2)
    print('ok')


if __name__ == '__main__':
    main()
