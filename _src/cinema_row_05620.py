# -*- coding: utf-8 -*-
"""0.56.20: Skin settings > Spotlight & widgets gets a tenth row, In cinemas now: films from (9779). The user saw
"a lot of" Indian films in In cinemas now: TMDb Helper's list for the United States holds every film with a US release.
OK opens the helper's country list (RunScript(script.aeon.helper,cinemacountry)): Everywhere (the default, as before),
the United States, or the United States with one more country; the helper then asks TMDb's discover for films made
there (resources/lib/online.py). The row shows the choice on the right; help text 32621. Navigation: 9758 -> 9779 ->
9750 (the page wraps). Runs once (marker); run _src/ok_only.py after it."""
import io
import os
import xml.etree.ElementTree as ET

SS = os.path.join('1080i', 'SkinSettings.xml')
INC = os.path.join('1080i', 'Includes_Settings.xml')
MARK = '0.56.20 cinema_row'
VALUE = '$VAR[Aeon_CinemaFrom]'
ROW = '''				<!-- %(mark)s: In cinemas now, films from: Everywhere / the United States / with one more country -->
				<control type="group">
					<left>-119</left>
					<top>821</top>
					<visible>Control.HasFocus(9779)</visible>
					<animation type="Visible"><effect type="fade" start="0" end="100" time="150"/></animation>
					<include>FG_LandVisible</include>
					<animation type="Hidden"><effect type="fade" start="100" end="0" time="100"/></animation>
					<control type="image"><left>-40</left><top>-34</top><width>1099</width><height>150</height><texture border="56" colordiffuse="$VAR[FG_ShadowCol]">fg/sh16.png</texture><visible>$EXP[Aeon_FGlass] + $EXP[FG_FocusShadowOn]</visible></control>
<control type="image"><left>0</left><top>0</top><width>1019</width><height>70</height><texture border="20" colordiffuse="$VAR[Aeon_MenuFocusColR]">$VAR[Aeon_MenuFocusTex]</texture><animation effect="zoom" start="100,100" end="102.355,100.000" center="auto" time="0" condition="$EXP[Aeon_FGlass] + $EXP[FG_FocusFlat]">Conditional</animation></control>
					<control type="image"><left>0</left><top>0</top><width>1019</width><height>1</height><texture colordiffuse="55ffffff">common/white.png</texture><visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_FGlass]</visible></control>
				</control>
				<control type="group">
					<top>821</top>
					<include content="Dlg_SkinRowChrome">
						<param name="id" value="9779"/><param name="namew" value="420"/><param name="label" value="$ADDON[skin.aeon.fuse 32619]"/><param name="hint" value=""/><param name="labelTop" value="0"/><param name="labelH" value="70"/><param name="icon" value="aeon/icons/film.png"/><param name="labelx" value="46"/>
					</include>
					<control type="button" id="9779">
						<include>Dlg_SkinRowButton</include>
						<onup>9758</onup>
						<ondown>9750</ondown>
						<onback>9601</onback>
						<onleft>SetFocus(9601)</onleft>
						<onclick>RunScript(script.aeon.helper,cinemacountry)</onclick>
					</control>
					<control type="label"><left>480</left><top>9</top><width>380</width><height>52</height><align>right</align><font>st_ui_22_bold</font><textcolor>ffffffff</textcolor><label>%(value)s</label><visible>!Control.HasFocus(9779)</visible></control>
					<control type="label"><left>480</left><top>9</top><width>380</width><height>52</height><align>right</align><font>st_ui_22_bold</font><textcolor>$VAR[Aeon_OnBarInk]</textcolor><label>%(value)s</label><visible>Control.HasFocus(9779)</visible></control>
				</control>
''' % {'mark': MARK, 'value': VALUE}
VAR = ('\t<!-- %s: the In cinemas now row\'s value -->\n\t<variable name="Aeon_CinemaFrom">\n'
       '\t\t<value condition="!String.IsEmpty(Skin.String(aeon.cinema.country)) + !String.IsEmpty(Skin.String(aeon.cinema.countryname))">$INFO[Skin.String(aeon.cinema.countryname)]</value>\n'
       '\t\t<value>$ADDON[skin.aeon.fuse 32620]</value>\n\t</variable>\n') % MARK


def main():
    t = io.open(SS, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    a = t.index('<control type="button" id="9758">')
    for old, new in (('<onup>9756</onup>\n\t\t\t\t\t<ondown>9750</ondown>', '<onup>9756</onup>\n\t\t\t\t\t<ondown>9779</ondown>'),):
        i = t.index(old, a)
        t = t[:i] + new + t[i + len(old):]
    b = t.index('<control type="button" id="9750">')
    i = t.index('<onup>9758</onup>', b)
    assert i - b < 300, i - b
    t = t[:i] + '<onup>9779</onup>' + t[i + len('<onup>9758</onup>'):]
    end = t.index('\t\t\t</control>\n\t\t</control>\n\t\t<!-- Context menu: the four context items', a)
    t = t[:end] + '\t\t\t</control>\n' + ROW + t[end + len('\t\t\t</control>\n'):]
    io.open(SS, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(SS)
    s = io.open(INC, encoding='utf-8').read()
    old = '\t\t<value condition="Control.HasFocus(9758)">$ADDON[skin.aeon.fuse 32330]</value>'
    assert s.count(old) == 1
    s = s.replace(old, old + '\n\t\t<value condition="Control.HasFocus(9779)">$ADDON[skin.aeon.fuse 32621]</value><!-- %s -->' % MARK)
    i = s.index('<includes>') + len('<includes>')
    s = s[:i] + '\n' + VAR + s[i:].lstrip('\n')
    io.open(INC, 'w', encoding='utf-8', newline='\n').write(s)
    ET.parse(INC)
    print('ok')


if __name__ == '__main__':
    main()
