# -*- coding: utf-8 -*-
"""0.56.14 the user's notes on the Aeon theme's Planner (537) and Flix (528) (canvas HJTtCDChVWkaZZAyt76wJA):
Planner: "no gap between highlight bar and clock/A-Z strip. also highlight bar top right corner shall meet clock box
lower left corner": in Aeon and Glass the list starts at 108 (the header's rule, the clock box's bottom) and is 1730
wide (it meets the strip at 1820); Fused Glass keeps its own spacing (the highlight gap rule).
Flix: "next episode airs info + network logo": NEXT EPISODE / S3 E5 · WED 18 NOV under the plot (helper aeon.next.*),
the network's (studio's) logo beside it on the right (the helper's pick, aeon.studio; its name when the pack has none).
Run from the skin folder after aeon_lib_music.py; runs once."""
import io
import os
import xml.etree.ElementTree as ET

V3 = os.path.join('1080i', 'Includes_Aeon_Views3.xml')
MARK = '0.56.14 aeon_lib_other'


def main():
    v = io.open(V3, encoding='utf-8').read()
    if MARK in v:
        print('already done')
        return
    # ---------------------------------------------------------------- Planner
    a = v.index('<include name="Aeon_V537_View">')
    b = v.index('\n\t</include>', a)
    view = v[a:b]
    old = '<left>90</left><top>124</top><width>1720</width><height>864</height>'
    assert view.count(old) == 1
    view = view.replace(old, '<include condition="Skin.HasSetting(aeon.fglass)">Aeon_V537_GeoFG</include><include condition="!Skin.HasSetting(aeon.fglass)">Aeon_V537_GeoAeon</include>')
    assert view.count('width="1720"') == 2
    view = view.replace('width="1720"', 'width="1730"')
    v = v[:a] + view + v[b:]
    a = v.index('<include name="Aeon_V537_Row">')
    b = v.index('\n\t</include>', a)
    row = v[a:b]
    lines = row.split('\n')
    n = 0
    for i, l in enumerate(lines):
        if '<left>0</left><top>0</top><width>1720</width><height>104</height>' in l and ('!$EXP[Aeon_FGlass]' in l or '70000000' in l):
            lines[i] = l.replace('<width>1720</width>', '<width>1730</width>', 1)
            n += 1
    assert n == 2, n
    v = v[:a] + '\n'.join(lines) + v[b:]
    geo = ('\t<!-- %s: the Planner list meets the clock box and the A-Z strip in Aeon and Glass -->\n'
           '\t<include name="Aeon_V537_GeoAeon"><left>90</left><top>108</top><width>1730</width><height>864</height></include>\n'
           '\t<include name="Aeon_V537_GeoFG"><left>90</left><top>124</top><width>1720</width><height>864</height></include>\n' % MARK)
    v = v.replace('\t<include name="Aeon_V537_Row">', geo + '\t<include name="Aeon_V537_Row">', 1)
    # ---------------------------------------------------------------- Flix
    a = v.index('<include name="Aeon_V528_ViewAeon">')
    b = v.index('\n\t</include>', a)
    view = v[a:b]
    i = view.index('\t\t\t<control type="fixedlist" id="528">')
    NX = 'String.IsEqual(Window(Home).Property(aeon.next.of),ListItem.TVShowTitle) + !String.IsEmpty(Window(Home).Property(aeon.next.code))'
    SO = 'String.IsEqual(Window(Home).Property(aeon.studio.of),ListItem.Studio)'
    add = ('\t\t\t<!-- %s: the next episode and the network\'s logo under the plot -->\n'
           '\t\t\t<control type="label"><left>100</left><top>592</top><width>600</width><height>26</height><aligny>center</aligny><font>lb_cap_16</font><textcolor>$VAR[Aeon_Accent]</textcolor>'
           '<label>[UPPERCASE]$ADDON[skin.aeon.fuse 32605][/UPPERCASE]</label><visible>%s</visible></control>\n'
           '\t\t\t<control type="label"><left>100</left><top>618</top><width>600</width><height>36</height><aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>ffffffff</textcolor>'
           '<label>[UPPERCASE]$INFO[Window(Home).Property(aeon.next.code)]  ·  $INFO[Window(Home).Property(aeon.next.day)][/UPPERCASE]</label><visible>%s</visible></control>\n'
           '\t\t\t<control type="image"><left>720</left><top>590</top><width>280</width><height>70</height><aspectratio align="right" aligny="center">keep</aspectratio>'
           '<texture background="true">resource://resource.images.studios.white/$INFO[Window(Home).Property(aeon.studio)].png</texture>'
           '<visible>!Skin.HasSetting(aeon.nostudio) + !String.IsEmpty(Window(Home).Property(aeon.studio)) + %s</visible></control>\n'
           '\t\t\t<control type="label"><left>700</left><top>590</top><width>300</width><height>70</height><align>right</align><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>d9ffffff</textcolor>'
           '<label>[UPPERCASE]$INFO[Window(Home).Property(aeon.studio.text)][/UPPERCASE]</label>'
           '<visible>!Skin.HasSetting(aeon.nostudio) + String.IsEmpty(Window(Home).Property(aeon.studio)) + !String.IsEmpty(Window(Home).Property(aeon.studio.text)) + %s</visible></control>\n'
           % (MARK, NX, NX, SO, SO))
    view = view[:i] + add + view[i:]
    v = v[:a] + view + v[b:]
    io.open(V3, 'w', encoding='utf-8', newline='\n').write(v)
    ET.parse(V3)
    print('ok')


if __name__ == '__main__':
    main()
