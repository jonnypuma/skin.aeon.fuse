"""Fused Glass, Home details (0.31.0). Run once from 1080i.
- Spectrum bars drawn by the skin (FG_EqBars 4 x 22, FG_EqBarsM 5 x 26): four rounded bars on one base line, each
  pulsing on its own cycle while music plays, settling low while paused. Used instead of the GIF in Fused Glass.
- Home now playing: in Fused Glass a frosted capsule left of the clock capsule (round cover, bars, artist, title,
  progress), whatever the placement setting.
- Home strip categories as tabs: the categories of the focused Home item stacked left of the strip, the current one
  in a frosted pill (Up / Down on the strip change it, as before). Replaces the single category label and the caption
  beside the strip in Fused Glass.
- The spotlight heading lines (category, episode code and title) in sentence case in Fused Glass."""
import io
import re

F = '$EXP[Aeon_FGlass]'
PLAYING = 'Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)'


def bars(name, w, h, gap):
    times = (450, 650, 350, 550)
    rest = (45, 70, 30, 55)
    out = []
    for i in range(4):
        x = i * (w + gap)
        c = '%g,%d' % (x + w / 2.0, h)
        out.append(
            '\t\t\t\t<control type="image"><left>%d</left><top>0</top><width>%d</width><height>%d</height>'
            '<texture colordiffuse="$PARAM[col]">fg/bar.png</texture>'
            '<animation effect="zoom" start="100,28" end="100,100" center="%s" time="%d" tween="sine" easing="inout" pulse="true" condition="%s">Conditional</animation>'
            '<animation effect="zoom" start="100,100" end="100,%d" center="%s" time="300" tween="cubic" easing="out" condition="![%s]">Conditional</animation>'
            '</control>' % (x, w, h, c, times[i], PLAYING, rest[i], c, PLAYING))
    return ('\t<include name="%s">\n\t\t<param name="left">0</param>\n\t\t<param name="top">0</param>\n'
            '\t\t<param name="col">ffffffff</param>\n\t\t<param name="vis">true</param>\n\t\t<definition>\n'
            '\t\t\t<control type="group"><left>$PARAM[left]</left><top>$PARAM[top]</top><visible>$PARAM[vis]</visible>\n'
            '%s\n\t\t\t</control>\n\t\t</definition>\n\t</include>\n' % (name, '\n'.join(out)))


def tab_sel(n):
    parts = []
    for sec in ('movies', 'tv', 'music'):
        prop = 'Window(Home).Property(aeon.subsel.%s)' % sec
        cond = 'String.IsEqual(%s,%d)' % (prop, n)
        if n == 1:
            cond = '[String.IsEmpty(%s) | %s]' % (prop, cond)
        parts.append('[String.IsEqual(Container(9000).ListItem.Label2,%s) + %s]' % (sec, cond))
    return '\t<expression name="FG_TabSel%d">[%s]</expression>\n' % (n, ' | '.join(parts))


FUSED_ADD = '''
	<!-- ===================================================== spectrum bars (0.31.0)
	     Four rounded bars on one base line instead of the spectrum GIF: each pulses on its own cycle while music plays
	     (Player.Playing, not paused, motion not reduced) and settles low otherwise. FG_EqBars 4 x 22 (gap 3, 25 wide),
	     FG_EqBarsM 5 x 26 (gap 4, 32 wide). params: left, top (of the bars' box), col, vis. Built by _src/fg_home.py. -->
''' + bars('FG_EqBars', 4, 22, 3) + bars('FG_EqBarsM', 5, 26, 4) + '''
	<!-- Home strip categories as tabs (Fused Glass): FG_TabSelN = the strip of the focused Home item shows its Nth category -->
''' + ''.join(tab_sel(n) for n in range(1, 7)) + '''	<include name="FG_StripTabs">
		<control type="group">
			<visible>[Control.HasFocus(9301) | Control.HasFocus(9302) | Control.HasFocus(9303)] + $EXP[Aeon_FGlass]</visible>
			<include>Anim_FadeVisible</include>
%s
		</control>
	</include>
	<!-- Home now playing (Fused Glass): a frosted capsule left of the clock capsule -->
	<include name="FG_NowPlayingCapsule">
		<control type="group">
			<visible>Player.HasAudio + String.IsEmpty(Window(Home).Property(aeon.theme)) + $EXP[Aeon_FGlass]</visible>
			<include>Anim_FadeVisible</include>
			<left>1112</left><top>40</top>
			<animation effect="slide" end="92,0" time="0" condition="!$EXP[AG_HasWeather]">Conditional</animation>
			<control type="image"><width>460</width><height>64</height><texture border="32" colordiffuse="fg_frost">fg/r32.png</texture></control>
			<control type="image"><width>460</width><height>64</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture></control>
			<control type="image"><left>10</left><top>10</top><width>44</width><height>44</height><aspectratio>scale</aspectratio><texture background="true" diffuse="fg/circle.png">$VAR[Aeon_NP_Cover]</texture></control>
			<include content="FG_EqBars"><param name="left" value="68"/><param name="top" value="21"/><param name="col" value="fg_mark"/></include>
			<control type="label"><left>108</left><top>9</top><width>330</width><height>22</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>9effffff</textcolor><label>[UPPERCASE]$INFO[MusicPlayer.Artist][/UPPERCASE]</label></control>
			<control type="label"><left>108</left><top>30</top><width>330</width><height>26</height><aligny>center</aligny><font>hm_ui_22_bold</font><textcolor>ffffffff</textcolor><label>$INFO[MusicPlayer.Title]</label></control>
			<control type="progress"><left>32</left><top>59</top><width>396</width><height>2</height><texturebg colordiffuse="1fffffff">common/white.png</texturebg><midtexture colordiffuse="d9ffffff">common/white.png</midtexture><info>Player.Progress</info></control>
		</control>
	</include>
'''

TAB_ROW = '''			<control type="grouplist">
				<left>112</left><top>%d</top><width>528</width><height>40</height>
				<orientation>horizontal</orientation><align>right</align><usecontrolcoords>true</usecontrolcoords>
				<visible>$EXP[Aeon_SubOn%d]</visible>
				<control type="button"><width min="0" max="528">auto</width><height>40</height><textoffsetx>20</textoffsetx><aligny>center</aligny><font>hm_ui_22_semibold</font><textcolor>ffffffff</textcolor><focusedcolor>ffffffff</focusedcolor><label>$INFO[Container(9391).ListItemAbsolute(%d).Label]</label><texturenofocus border="20" colordiffuse="fg_sel">fg/r20.png</texturenofocus><texturefocus border="20" colordiffuse="fg_sel">fg/r20.png</texturefocus><visible>$EXP[FG_TabSel%d]</visible></control>
				<control type="button"><width min="0" max="528">auto</width><height>40</height><textoffsetx>20</textoffsetx><aligny>center</aligny><font>hm_ui_22</font><textcolor>94ffffff</textcolor><focusedcolor>94ffffff</focusedcolor><label>$INFO[Container(9391).ListItemAbsolute(%d).Label]</label><texturenofocus /><texturefocus /><visible>!$EXP[FG_TabSel%d]</visible></control>
			</control>'''


def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:90], s.count(a))
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    return s


def add_vis(ctrl, cond):
    m = re.search(r'<visible>(.*?)</visible>', ctrl)
    if m:
        return ctrl.replace(m.group(0), '<visible>[%s] + %s</visible>' % (m.group(1), cond), 1)
    return ctrl.replace('</control>', '<visible>%s</visible></control>' % cond, 1)


if __name__ == '__main__':
    # Includes_Fused.xml: bars, tab expressions and include, capsule
    tabs = '\n'.join(TAB_ROW % (764 + 46 * (n - 1), n, n - 1, n, n - 1, n) for n in range(1, 7))
    s = io.open('Includes_Fused.xml', encoding='utf-8').read()
    if 'FG_EqBars' not in s:
        i = s.rindex('</includes>')
        s = s[:i] + (FUSED_ADD % tabs) + s[i:]
        io.open('Includes_Fused.xml', 'w', encoding='utf-8', newline='').write(s)

    h = 'Includes_Aeon_Home.xml'
    s = io.open(h, encoding='utf-8').read()
    # heading lines in sentence case
    n = 0
    for m in list(re.finditer(r'[^\n]*<control type="label">[^\n]*<top>264</top>[^\n]*\[UPPERCASE\][^\n]*</control>', s)):
        line = m.group(0)
        if F in line:
            continue
        indent = re.match(r'\s*', line).group(0)
        fused = add_vis(line.replace('[UPPERCASE]', '').replace('[/UPPERCASE]', ''), F).strip()
        s = s.replace(line, add_vis(line, '!' + F) + '\n' + indent + fused, 1)
        n += 1
    print('headings', n)
    # category label and caption hidden in Fused; tabs instead
    cat = '''			<visible>[Control.HasFocus(9301) | Control.HasFocus(9302) | Control.HasFocus(9303)]</visible>
		</control>
		</control>
		</control>
		<control type="group">
			<include>Aeon_LowBand</include>
			<include>Aeon_H_SubMenu</include>'''
    assert s.count(cat) == 1
    s = s.replace(cat, cat.replace('Control.HasFocus(9303)]</visible>\n\t\t</control>',
                                   'Control.HasFocus(9303)] + !%s</visible>\n\t\t</control>\n\t\t<include>FG_StripTabs</include>' % F, 1))
    for old in ('<visible>[Control.HasFocus(9301) | Control.HasFocus(9302) | Control.HasFocus(9303)] + $EXP[Aeon_H_CapHasLogo]</visible>',
                '<visible>[Control.HasFocus(9301) | Control.HasFocus(9302) | Control.HasFocus(9303)] + ![$EXP[Aeon_H_CapHasLogo]]</visible>'):
        assert s.count(old) == 1
        s = s.replace(old, old.replace('</visible>', ' + !%s</visible>' % F))
    # now playing: the four placements stay for Aeon / Glass; Fused Glass shows the capsule
    for p in ('[String.IsEmpty(Skin.String(aeon.npplace)) | String.IsEqual(Skin.String(aeon.npplace),a)]</visible>',
              'String.IsEqual(Skin.String(aeon.npplace),b)</visible>',
              'String.IsEqual(Skin.String(aeon.npplace),c)</visible>',
              'String.IsEqual(Skin.String(aeon.npplace),d)</visible>'):
        assert s.count(p) == 1, p
        s = s.replace(p, p.replace('</visible>', ' + !%s</visible>' % F))
    anchor = '\t\t<!-- custom rows (Skin settings > Custom rows) one screen below -->'
    assert s.count(anchor) == 1
    s = s.replace(anchor, '\t\t<include>FG_NowPlayingCapsule</include>\n' + anchor)
    io.open(h, 'w', encoding='utf-8', newline='').write(s)

    # library rail: the bars instead of the GIF
    m = 'Includes_Aeon_Menu.xml'
    patch(m, [
        ('<texture colordiffuse="ffffffff">common/aeon_eq_anim.gif</texture><visible>Player.HasAudio + Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)</visible></control>',
         '<texture colordiffuse="ffffffff">common/aeon_eq_anim.gif</texture><visible>Player.HasAudio + Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion) + !%s</visible></control>' % F),
        ('<texture colordiffuse="ffffffff">common/aeon_eq_still.png</texture><visible>Player.HasAudio + ![Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)]</visible></control>',
         '<texture colordiffuse="ffffffff">common/aeon_eq_still.png</texture><visible>Player.HasAudio + ![Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)] + !%s</visible></control>\n'
         '\t\t<include content="FG_EqBarsM"><param name="left" value="24"/><param name="top" value="1013"/><param name="col" value="ffffffff"/><param name="vis" value="%s + Player.HasAudio"/></include>' % (F, F)),
    ])
    p = 'Custom_1160_LibraryPanel.xml'
    patch(p, [
        ('<texture colordiffuse="aeon_onbar">common/aeon_eq_anim.gif</texture><visible>Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)</visible></control>',
         '<texture colordiffuse="aeon_onbar">common/aeon_eq_anim.gif</texture><visible>Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion) + !%s</visible></control>' % F),
        ('<texture colordiffuse="aeon_onbar">common/aeon_eq_still.png</texture><visible>![Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)]</visible></control>',
         '<texture colordiffuse="aeon_onbar">common/aeon_eq_still.png</texture><visible>![Player.Playing + !Player.Paused + !Skin.HasSetting(aeon.reducemotion)] + !%s</visible></control>\n'
         '\t\t\t\t<include content="FG_EqBarsM"><param name="left" value="24"/><param name="top" value="1013"/><param name="col" value="fg_ink"/><param name="vis" value="%s"/></include>' % (F, F)),
    ])
    print('home ok')
