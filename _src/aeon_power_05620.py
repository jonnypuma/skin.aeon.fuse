# -*- coding: utf-8 -*-
"""0.56.20: Home > Power in Aeon and Aeon Glass becomes the Fused Glass Power page in Aeon dress (canvas "Aeon Power,
Pictures and splash", QGCfFk4L8RfaXGRipeK7ga, approved 2026-11-17; the user's notes: the page sits on the Power item's
own fanart, nothing drawn over it but the text).

- Aeon_H_PowerPage_Aeon (Includes_Fused.xml) is a copy of FG_H_PowerPage (fg_home_power.py): the date, the big clock,
  the uptimes and what plays, the shutdown timer row (9341) and Fused Glass's round actions under the menu (9342, the
  same ids: the two pages are chosen when the skin loads). The timer row is Aeon's option picker: one track, no gaps,
  the running choice an accent block (Kodi does not say which length runs: the row keeps it in
  Window(Home).Property(aeon.pw.timer)); Aeon Glass draws the blocks as pills and the clock on a rounded glass card.
- Aeon's Power item: OK and Up go to the round actions (were the Power list 9338), Down too (was the old timer row).
Runs once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

FUSED = os.path.join('1080i', 'Includes_Fused.xml')
HOME = os.path.join('1080i', 'Includes_Aeon_Home.xml')
MARK = '0.56.20 aeon_power'
KEYS = {'93411': 'off', '93412': '30', '93413': '60', '93414': '90', '93415': '120', '93416': 'end'}

TEX = '''	<!-- %(m)s: the Aeon / Aeon Glass Power page's timer row, Aeon's option picker -->
	<include name="Aeon_PwTimerTex">
		<param name="key"/>
		<definition>
			<!-- the shape is picked when the skin loads: a $VAR in a button's texture path draws nothing -->
			<include condition="Skin.HasSetting(aeon.vglass)" content="Aeon_PwTimerShape"><param name="file" value="fg/r28.png"/><param name="key" value="$PARAM[key]"/></include>
			<include condition="!Skin.HasSetting(aeon.vglass)" content="Aeon_PwTimerShape"><param name="file" value="common/white.png"/><param name="key" value="$PARAM[key]"/></include>
			<textcolor>$VAR[Aeon_PwTimerInk_$PARAM[key]]</textcolor>
		</definition>
	</include>
	<include name="Aeon_PwTimerShape">
		<param name="file"/><param name="key"/>
		<definition>
			<texturefocus border="28" colordiffuse="aeon_white">$PARAM[file]</texturefocus>
			<texturenofocus border="28" colordiffuse="$VAR[Aeon_PwTimerCol_$PARAM[key]]">$PARAM[file]</texturenofocus>
		</definition>
	</include>
''' % {'m': MARK}
ON = {'off': '!System.HasAlarm(shutdowntimer)',
      'end': 'System.HasAlarm(shutdowntimer) + String.IsEqual(Window(Home).Property(aeon.pw.timer),end)'}
for k in ('30', '60', '90', '120'):
    ON[k] = 'System.HasAlarm(shutdowntimer) + String.IsEqual(Window(Home).Property(aeon.pw.timer),%s)' % k
for k, cond in ON.items():
    TEX += ('\t<variable name="Aeon_PwTimerCol_%s"><value condition="%s">$VAR[Aeon_Accent]</value><value>1fffffff</value></variable>\n'
            '\t<variable name="Aeon_PwTimerInk_%s"><value condition="%s">$VAR[Aeon_AccentText]</value><value>d9ffffff</value></variable>\n'
            % (k, cond, k, cond))
CARD = ('\t\t\t<!-- %s: Aeon Glass draws the clock block on a rounded glass card -->\n'
        '\t\t\t<control type="image"><left>80</left><top>84</top><width>820</width><height>432</height><texture border="28" colordiffuse="99101014">fg/r28.png</texture><visible>Skin.HasSetting(aeon.vglass)</visible></control>\n') % MARK


def main():
    f = io.open(FUSED, encoding='utf-8').read()
    if MARK in f:
        print('already')
        return
    a = f.index('\t<include name="FG_H_PowerPage">')
    b = f.index('\n\t</include>', a) + len('\n\t</include>')
    page = f[a:b].replace('<include name="FG_H_PowerPage">', '<include name="Aeon_H_PowerPage_Aeon"><!-- %s: FG_H_PowerPage in Aeon dress -->' % MARK, 1)
    g = page.index('<control type="grouplist" id="9341">')
    h = page.index('</control>\n\t\t</control>', g)
    row = page[g:h].replace('<itemgap>12</itemgap>', '<itemgap>0</itemgap>')
    for bid, key in KEYS.items():
        m = re.search(r'(<control type="button" id="%s">.*?)<textcolor>ffffffff</textcolor>(.*?)<include>FG_PillBtnTex</include>(.*?)<onclick>' % bid, row)
        assert m, bid
        store = '<onclick>ClearProperty(aeon.pw.timer,home)</onclick>' if key == 'off' else '<onclick>SetProperty(aeon.pw.timer,%s,home)</onclick>' % key
        row = row[:m.start()] + m.group(1) + m.group(2) + '<include content="Aeon_PwTimerTex"><param name="key" value="%s"/></include>' % key + m.group(3) + store + '<onclick>' + row[m.end():]
    page = page[:g] + row + page[h:]
    first = page.index('<include>Aeon_LowBand</include>') + len('<include>Aeon_LowBand</include>')
    vis = page.index('</visible>', first) + len('</visible>')
    page = page[:vis] + '\n' + CARD + page[vis:]
    i = f.index('\t<include name="Aeon_H_PowerPage_Classic">')
    f = f[:i] + page.lstrip('\t').join(['\t', '\n']) + TEX + f[i:]
    f = f.replace('<include condition="!Skin.HasSetting(aeon.fglass)">Aeon_H_PowerPage_Classic</include>',
                  '<include condition="!Skin.HasSetting(aeon.fglass)">Aeon_H_PowerPage_Aeon</include><!-- %s (was Aeon_H_PowerPage_Classic) -->' % MARK, 1)
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
    ET.parse(FUSED)
    t = io.open(HOME, encoding='utf-8').read()
    n1 = t.count('<onclick condition="!$EXP[Aeon_FGlass]">SetFocus(9338)</onclick>')
    t = t.replace('<onclick condition="!$EXP[Aeon_FGlass]">SetFocus(9338)</onclick>', '<onclick condition="!$EXP[Aeon_FGlass]">SetFocus(93421)</onclick>')
    up = '<onup condition="String.IsEqual(Container(9000).ListItem.Label2,power) + $EXP[Aeon_SubOn1] + !$EXP[Aeon_FGlass]">SetFocus(9338)</onup>'
    n2 = t.count(up)
    t = t.replace(up, up.replace('SetFocus(9338)', 'SetFocus(93421)').replace(' + $EXP[Aeon_SubOn1]', ''))
    down = '<ondown condition="$EXP[Aeon_H_PowerSec] + !$EXP[Aeon_H_SpotAny] + !Skin.HasSetting(aeon.fglass)">SetFocus(93081)</ondown>'
    n3 = t.count(down)
    t = t.replace(down, down.replace('SetFocus(93081)', 'SetFocus(93421)'))
    assert n1 == 24 and n2 == 1 and n3 == 1, (n1, n2, n3)
    io.open(HOME, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(HOME)
    print('ok', n1, n2, n3)


if __name__ == '__main__':
    main()
