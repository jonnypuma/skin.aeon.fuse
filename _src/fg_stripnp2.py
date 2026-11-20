"""0.39.4 library settings strip (dialog 1160), Fused Glass: the music section becomes the bottom band of the panel
itself, as the foot of the List view card (ratings / certificate / duration): a hairline across the panel, under it a
slightly lighter shade with the panel's own rounded bottom corners (fg/rb32.png = r32.png with a flat top). The song's
progress reveals a lighter band from the left with a straight edge (progress <reveal>). Left to right: the cover
(48 px, rounded) centred in the icon column (x 40, like the setting icons), the moving bars, artist and song.
Focused (Down from the last setting): the band turns white with dark ink, like a focused setting; the progress shows as
a darker band on it.
Run in 1080i."""
import io
import re

TOP, H = 972, 100           # the band: 972 .. 1072 (panel bottom)
CY = TOP + H // 2

p = 'Includes_Fused.xml'
t = io.open(p, encoding='utf-8').read()
a = t.index('\t<include name="FG_StripNP">')
b = t.index('\n\t</include>', a) + len('\n\t</include>')
new = '''	<include name="FG_StripNP">
		<control type="group">
			<visible>$EXP[Aeon_FGlass] + Player.HasAudio + String.IsEmpty(Window(Home).Property(aeon.libclean))</visible>
			<include>Anim_FadeVisible</include>
			<!-- the band: the panel's bottom (8..452 x %(top)d..1072), its own shade, the song's progress revealed from the left -->
			<control type="progress"><left>8</left><top>%(top)d</top><width>444</width><height>%(h)d</height><reveal>true</reveal><texturebg border="32" colordiffuse="0dffffff">fg/rb32.png</texturebg><midtexture border="32" colordiffuse="17ffffff">fg/rb32.png</midtexture><info>Player.Progress</info><visible>!Control.HasFocus(300)</visible></control>
			<control type="progress"><left>8</left><top>%(top)d</top><width>444</width><height>%(h)d</height><reveal>true</reveal><texturebg border="32" colordiffuse="ffffffff">fg/rb32.png</texturebg><midtexture border="32" colordiffuse="1f0f1115">fg/rb32.png</midtexture><info>Player.Progress</info><visible>Control.HasFocus(300)</visible></control>
			<control type="image"><left>9</left><top>%(top)d</top><width>442</width><height>1</height><texture colordiffuse="fg_edge">common/white.png</texture><visible>!Control.HasFocus(300)</visible></control>
			<!-- the cover, centred in the icon column (x 40) -->
			<control type="image"><left>16</left><top>%(cy24)d</top><width>48</width><height>48</height><aspectratio scalediffuse="false">scale</aspectratio><texture background="true" diffuse="fg/m72x72.png">$VAR[Aeon_NP_Cover]</texture></control>
			<!-- the moving bars, then artist and song -->
			<include content="FG_EqBarsM"><param name="left" value="84"/><param name="top" value="%(cy13)d"/><param name="col" value="fg_mark"/><param name="vis" value="!Control.HasFocus(300)"/></include>
			<include content="FG_EqBarsM"><param name="left" value="84"/><param name="top" value="%(cy13)d"/><param name="col" value="fg_ink"/><param name="vis" value="Control.HasFocus(300)"/></include>
			<control type="label"><left>132</left><top>%(cy30)d</top><width>300</width><height>26</height><aligny>center</aligny><font>lb_cap_20</font><textcolor>9effffff</textcolor><label>[UPPERCASE]$INFO[MusicPlayer.Artist][/UPPERCASE]</label><visible>!Control.HasFocus(300)</visible></control>
			<control type="label"><left>132</left><top>%(cy6)d</top><width>300</width><height>32</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><label>$INFO[MusicPlayer.Title]</label><visible>!Control.HasFocus(300)</visible></control>
			<control type="label"><left>132</left><top>%(cy30)d</top><width>300</width><height>26</height><aligny>center</aligny><font>lb_cap_20</font><textcolor>990f1115</textcolor><label>[UPPERCASE]$INFO[MusicPlayer.Artist][/UPPERCASE]</label><visible>Control.HasFocus(300)</visible></control>
			<control type="label"><left>132</left><top>%(cy6)d</top><width>300</width><height>32</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>fg_ink</textcolor><label>$INFO[MusicPlayer.Title]</label><visible>Control.HasFocus(300)</visible></control>
		</control>
	</include>''' % {'top': TOP, 'h': H, 'cy24': CY - 24, 'cy13': CY - 13, 'cy30': CY - 30, 'cy6': CY - 4}
t = t[:a] + new + t[b:]
t = t.replace('''	<!-- 0.39.3 library settings strip (1160), Fused Glass: music playing as the panel's bottom section. The song's progress
	     fills the card (fill and background are the same 72 px image: Kodi sizes the fill from the background's height). -->''',
              '''	<!-- 0.39.3 / 0.39.4 library settings strip (1160), Fused Glass: music playing as the panel's bottom band (_src/fg_stripnp2.py).
	     Fill and background are the same image: Kodi sizes the fill from the background image's height. -->''')
io.open(p, 'w', encoding='utf-8', newline='').write(t)
print('ok')
