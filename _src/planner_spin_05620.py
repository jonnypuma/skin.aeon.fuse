# -*- coding: utf-8 -*-
"""0.56.20: the Planner's Week view in Aeon / Aeon Glass shows a spinner and "Loading" in each day column while its list
loads (the user: "in Aeon theme there was no loading spinners for the days, like we have in fused glass"). The same
layer and condition as Fused Glass (Includes_Fused.xml, lists 9511-9517): the list updating, or empty while the helper
is busy, past days only when they are shown. Runs once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Includes_Planner.xml')
MARK = '0.56.20 planner_spin'
LAYER = ('<!-- %(m)s --><control type="group"><left>%(x)d</left><top>%(y)d</top>'
         '<visible>[Container(%(id)d).IsUpdating | [Integer.IsEqual(Container(%(id)d).NumItems,0) + !String.IsEmpty(Window(Home).Property(aeon.planner.busy))]] + '
         '[String.IsEmpty(Window(Home).Property(aeon.planner.c%(c)d.past)) | Skin.HasSetting(aeon.planner.past)]</visible>'
         '<animation type="Visible"><effect type="fade" start="0" end="100" delay="150" time="200"/></animation>'
         '<control type="image"><left>0</left><top>6</top><width>22</width><height>22</height><texture colordiffuse="b3ffffff">common/aeon_spinner.gif</texture><visible>!Skin.HasSetting(aeon.reducemotion)</visible></control>'
         '<control type="image"><left>0</left><top>6</top><width>22</width><height>22</height><texture colordiffuse="b3ffffff">common/aeon_spinner_still.png</texture><visible>Skin.HasSetting(aeon.reducemotion)</visible></control>'
         '<control type="label"><left>32</left><top>0</top><width>190</width><height>34</height><aligny>center</aligny><font>lb_small_20</font><textcolor>99ffffff</textcolor><label>$LOCALIZE[31952]</label></control>'
         '</control>\n\t\t\t')


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    n = 0
    for c in range(1, 8):
        lid = 9510 + c
        m = re.search(r'<control type="list" id="%d">\s*<left>(\d+)</left><top>(\d+)</top>' % lid, t)
        assert m, lid
        x, y = int(m.group(1)), int(m.group(2))
        t = t[:m.start()] + LAYER % {'m': MARK, 'x': x + 12, 'y': y + 12, 'id': lid, 'c': c} + t[m.start():]
        n += 1
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    print('ok', n)


if __name__ == '__main__':
    main()
