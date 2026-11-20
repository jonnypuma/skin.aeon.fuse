"""Fused Glass, player overlays (0.31.0). Run once from 1080i.
- Video OSD: the bottom scrim gives way to a floating frosted card (36,744 1848 x 300, radius 28) behind the poster, the
  ends-at ring, the times, the seek line and the controls; the poster rounded.
- Top bar of the player overlays (Video OSD, information, chapters): no black band, a soft top scrim; the clock box and
  weather box become the clock capsule of Home; Skippy's next episode moves left of the capsule.
- OSD buttons (video and music OSD): the focus is a white circle (icon buttons) or a white pill (text buttons), inset in
  the 90 px cell (fg/btn90.png, fg/pill90.png); no dark square behind the others.
- Seek marker: a round knob with a soft halo (fg/knob40.png) instead of the square."""
import io

F = '$EXP[Aeon_FGlass]'
FS = 'Skin.HasSetting(aeon.fglass)'


def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:100], s.count(a))
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


TEX = '''
	<!-- ===================================================== player overlays (0.31.0, _src/fg_osd.py) -->
	<include name="FG_OSDIconTex_fg"><texturefocus colordiffuse="ffffffff">fg/btn90.png</texturefocus><texturenofocus /></include>
	<include name="FG_OSDIconTex_old"><texturefocus colordiffuse="aeon_white">common/white.png</texturefocus><texturenofocus colordiffuse="40000000">common/white.png</texturenofocus></include>
	<include name="FG_OSDIconTex">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_OSDIconTex_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">FG_OSDIconTex_old</include>
	</include>
	<include name="FG_OSDPillTex_fg"><texturefocus border="45" colordiffuse="ffffffff">fg/pill90.png</texturefocus><texturenofocus /></include>
	<include name="FG_OSDPillTex">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_OSDPillTex_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">FG_OSDIconTex_old</include>
	</include>
	<include name="FG_SeekNib_fg"><textureslidernib>fg/knob40.png</textureslidernib><textureslidernibfocus>fg/knob40.png</textureslidernibfocus></include>
	<include name="FG_SeekNib_old"><textureslidernib>aeon/seek_mark40.png</textureslidernib><textureslidernibfocus>aeon/seek_mark40.png</textureslidernibfocus></include>
	<include name="FG_SeekNib">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_SeekNib_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">FG_SeekNib_old</include>
	</include>
	<!-- the floating card of the Video OSD -->
	<include name="FG_OSDCard">
		<control type="group">
			<visible>$EXP[Aeon_FGlass]</visible>
			<control type="image"><left>0</left><top>560</top><width>1920</width><height>520</height><texture colordiffuse="b3000000">fg/scrim_b.png</texture></control>
			<control type="image"><left>-4</left><top>704</top><width>1928</width><height>380</height><texture border="68" colordiffuse="99000000">fg/sh28.png</texture></control>
			<control type="image"><left>36</left><top>744</top><width>1848</width><height>300</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture></control>
			<control type="image"><left>36</left><top>744</top><width>1848</width><height>300</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture></control>
		</control>
	</include>
'''

if __name__ == '__main__':
    s = io.open('Includes_Fused.xml', encoding='utf-8').read()
    if 'FG_OSDIconTex' not in s:
        i = s.rindex('</includes>')
        s = s[:i] + TEX + s[i:]
        io.open('Includes_Fused.xml', 'w', encoding='utf-8', newline='').write(s)

    o = 'Includes_Aeon_OSD.xml'
    patch(o, [
        # icon button textures
        ('''					<label></label>
					<texturefocus colordiffuse="aeon_white">common/white.png</texturefocus>
					<texturenofocus colordiffuse="40000000">common/white.png</texturenofocus>''',
         '''					<label></label>
					<include>FG_OSDIconTex</include>'''),
        # text button textures
        ('''					<focusedcolor>aeon_onbar</focusedcolor>
					<texturefocus colordiffuse="aeon_white">common/white.png</texturefocus>
					<texturenofocus colordiffuse="40000000">common/white.png</texturenofocus>''',
         '''					<focusedcolor>aeon_onbar</focusedcolor>
					<include>FG_OSDPillTex</include>'''),
        # seek marker
        ('''					<textureslidernib>aeon/seek_mark40.png</textureslidernib>
					<textureslidernibfocus>aeon/seek_mark40.png</textureslidernibfocus>''',
         '''					<include>FG_SeekNib</include>'''),
        # top bar: band, clock box, weather box only in Aeon / Glass; the clock capsule in Fused Glass
        ('''		<control type="image"><left>0</left><top>0</top><width>1920</width><height>108</height><texture colordiffuse="e6000000">common/white.png</texture></control>
		<control type="group">
			<visible>!Skin.HasSetting(aeon.osd.noclock)</visible>
			<include>Aeon_ClockBox</include>
		</control>''',
         '''		<control type="image"><left>0</left><top>0</top><width>1920</width><height>108</height><texture colordiffuse="e6000000">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>
		<control type="image"><left>0</left><top>0</top><width>1920</width><height>260</height><texture colordiffuse="cc000000">fg/scrim_t.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>
		<control type="group">
			<visible>!Skin.HasSetting(aeon.osd.noclock) + !$EXP[Aeon_FGlass]</visible>
			<include>Aeon_ClockBox</include>
		</control>
		<control type="group">
			<visible>!Skin.HasSetting(aeon.osd.noclock) + $EXP[Aeon_FGlass]</visible>
			<include>FG_ClockCapsule</include>
		</control>'''),
        ('''			<visible>!Skin.HasSetting(aeon.osd.noweather) + !String.IsEmpty(Weather.Temperature)</visible>
			<animation effect="slide" end="0,-108" time="0" condition="Skin.HasSetting(aeon.osd.noclock)">Conditional</animation>''',
         '''			<visible>!Skin.HasSetting(aeon.osd.noweather) + !String.IsEmpty(Weather.Temperature) + !$EXP[Aeon_FGlass]</visible>
			<animation effect="slide" end="0,-108" time="0" condition="Skin.HasSetting(aeon.osd.noclock)">Conditional</animation>'''),
        ('''			<animation effect="slide" end="100,0" time="0" condition="Skin.HasSetting(aeon.osd.noclock) + [Skin.HasSetting(aeon.osd.noweather) | String.IsEmpty(Weather.Temperature)]">Conditional</animation>''',
         '''			<animation effect="slide" end="100,0" time="0" condition="Skin.HasSetting(aeon.osd.noclock) + [Skin.HasSetting(aeon.osd.noweather) | String.IsEmpty(Weather.Temperature)] + !$EXP[Aeon_FGlass]">Conditional</animation>
			<animation effect="slide" end="-236,0" time="0" condition="!Skin.HasSetting(aeon.osd.noclock) + $EXP[Aeon_FGlass]">Conditional</animation>
			<animation effect="slide" end="100,0" time="0" condition="Skin.HasSetting(aeon.osd.noclock) + $EXP[Aeon_FGlass]">Conditional</animation>'''),
        # Video OSD: card instead of the bottom scrim
        ('''			<texture colordiffuse="f0000000">aeon/osd_scrim_bottom.png</texture>
		</control>
		<include>Aeon_OSD_TopBar</include>''',
         '''			<texture colordiffuse="f0000000">aeon/osd_scrim_bottom.png</texture>
			<visible>!$EXP[Aeon_FGlass]</visible>
		</control>
		<include>FG_OSDCard</include>
		<include>Aeon_OSD_TopBar</include>'''),
        # rounded poster
        ('''			<texture background="true">$VAR[Aeon_OSD_Poster]</texture>
			<visible>!Skin.HasSetting(aeon.osd.noposter) | [Skin.HasSetting(aeon.osd.disc) + [!String.IsEmpty(Player.Art(discart)) | !String.IsEmpty(Player.Art(album.discart))]]</visible>
		</control>''',
         '''			<texture background="true">$VAR[Aeon_OSD_Poster]</texture>
			<visible>[!Skin.HasSetting(aeon.osd.noposter) | [Skin.HasSetting(aeon.osd.disc) + [!String.IsEmpty(Player.Art(discart)) | !String.IsEmpty(Player.Art(album.discart))]]] + !$EXP[Aeon_FGlass]</visible>
		</control>
		<control type="image">
			<left>60</left><top>780</top><width>127</width><height>190</height>
			<aspectratio>scale</aspectratio>
			<texture background="true" diffuse="fg/m127x190.png">$VAR[Aeon_OSD_Poster]</texture>
			<visible>[!Skin.HasSetting(aeon.osd.noposter) | [Skin.HasSetting(aeon.osd.disc) + [!String.IsEmpty(Player.Art(discart)) | !String.IsEmpty(Player.Art(album.discart))]]] + $EXP[Aeon_FGlass]</visible>
		</control>'''),
    ])
    print('osd ok')
