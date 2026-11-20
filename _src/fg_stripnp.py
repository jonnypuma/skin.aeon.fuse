"""0.39.3 library settings strip (dialog 1160), Fused Glass: music playing becomes a section of the open panel, at its
bottom, shown as soon as the strip opens (was the Aeon white bar, only while the bottom box had focus): a lighter
rounded card, the cover with rounded corners, artist and title, the moving bars, and the song's progress filling the
card from the left. Down from the last setting focuses it (brighter edge); OK opens the visualisation as before.
The rail's own circle and bars at the bottom hide while the section shows. Other themes keep the Aeon bar.
Run in 1080i."""
import io

p = 'Custom_1160_LibraryPanel.xml'
s = io.open(p, encoding='utf-8').read()
assert 'FG_StripNP' not in s
# the button draws no white block in Fused Glass
old = '''				<texturefocus colordiffuse="aeon_white">common/white.png</texturefocus>
				<texturenofocus />
				<onup>100</onup><ondown>noop</ondown>'''
assert old in s
s = s.replace(old, '''				<include>FG_StripNPBtnFocus</include>
				<texturenofocus />
				<onup>100</onup><ondown>noop</ondown>''', 1)
# the Aeon bar: other themes only
old = '''			<control type="group">
				<visible>Control.HasFocus(300)</visible>'''
assert old in s
s = s.replace(old, '''			<control type="group">
				<visible>Control.HasFocus(300) + !$EXP[Aeon_FGlass]</visible>''', 1)
old = '''			<!-- Clean library: ask first ("No" is focused) -->'''
assert old in s
s = s.replace(old, '''			<!-- 0.39.3 Fused Glass: music playing as a section of the open panel -->
			<include>FG_StripNP</include>
''' + old, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'Includes_Aeon_Menu.xml'
s = io.open(p, encoding='utf-8').read()
old = '<texture colordiffuse="fg_sel">fg/circle.png</texture><visible>$EXP[Aeon_FGlass] + Player.HasAudio</visible></control>'
assert s.count(old) == 1
s = s.replace(old, '<texture colordiffuse="fg_sel">fg/circle.png</texture><visible>$EXP[Aeon_FGlass] + Player.HasAudio + !Window.IsActive(1160)</visible></control>')
old = '<param name="vis" value="$EXP[Aeon_FGlass] + Player.HasAudio"/></include>'
assert s.count(old) == 1
s = s.replace(old, '<param name="vis" value="$EXP[Aeon_FGlass] + Player.HasAudio + !Window.IsActive(1160)"/></include>')
io.open(p, 'w', encoding='utf-8', newline='').write(s)

p = 'Includes_Fused.xml'
t = io.open(p, encoding='utf-8').read()
assert 'name="FG_StripNP"' not in t
t = t.replace('</includes>', '''	<!-- 0.39.3 library settings strip (1160), Fused Glass: music playing as the panel's bottom section. The song's progress
	     fills the card (fill and background are the same 72 px image: Kodi sizes the fill from the background's height). -->
	<include name="FG_StripNPBtnFocus">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_StripNPBtnFocus_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">FG_StripNPBtnFocus_old</include>
	</include>
	<include name="FG_StripNPBtnFocus_fg"><texturefocus /></include>
	<include name="FG_StripNPBtnFocus_old"><texturefocus colordiffuse="aeon_white">common/white.png</texturefocus></include>
	<include name="FG_StripNP">
		<control type="group">
			<visible>$EXP[Aeon_FGlass] + Player.HasAudio + String.IsEmpty(Window(Home).Property(aeon.libclean))</visible>
			<include>Anim_FadeVisible</include>
			<control type="progress"><left>16</left><top>980</top><width>428</width><height>80</height><texturebg border="28" colordiffuse="14ffffff">fg/r28.png</texturebg><midtexture border="28" colordiffuse="24ffffff">fg/r28.png</midtexture><info>Player.Progress</info></control>
			<control type="image"><left>16</left><top>980</top><width>428</width><height>80</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture><visible>!Control.HasFocus(300)</visible></control>
			<control type="image"><left>16</left><top>980</top><width>428</width><height>80</height><texture border="28" colordiffuse="14ffffff">fg/r28.png</texture><visible>Control.HasFocus(300)</visible></control>
			<control type="image"><left>16</left><top>980</top><width>428</width><height>80</height><texture border="28" colordiffuse="d9ffffff">fg/e28.png</texture><visible>Control.HasFocus(300)</visible></control>
			<control type="image"><left>24</left><top>988</top><width>64</width><height>64</height><aspectratio scalediffuse="false">scale</aspectratio><texture background="true" diffuse="fg/m72x72.png">$VAR[Aeon_NP_Cover]</texture></control>
			<control type="label"><left>104</left><top>992</top><width>284</width><height>24</height><aligny>center</aligny><font>lb_cap_20</font><textcolor>9effffff</textcolor><label>[UPPERCASE]$INFO[MusicPlayer.Artist][/UPPERCASE]</label></control>
			<control type="label"><left>104</left><top>1016</top><width>326</width><height>32</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><label>$INFO[MusicPlayer.Title]</label></control>
			<include content="FG_EqBarsM"><param name="left" value="400"/><param name="top" value="993"/><param name="col" value="fg_mark"/><param name="vis" value="Player.Playing + !Player.Paused"/></include>
		</control>
	</include>
</includes>''')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('ok')
