"""Fused Glass screensaver (Custom_1156_Screensaver.xml, 0.31.0). Run once from 1080i.
- The poster floats as a rounded card (150,120 560 x 840) with a soft shadow instead of filling the screen's height;
  the album cover is rounded.
- Pager: a column of small dots with the current slide as a short pill (left 48, centred).
- Clock and weather: the clock capsule of Home (FG_ClockCapsule, now with a wx param), or a weather capsule alone when
  only the weather switch is on.
- Now playing: a frosted card under the capsule (cover, artist, title, time, spectrum bars).
Aeon and Glass keep their screensaver as it was."""
import io

F = 'Skin.HasSetting(aeon.fglass)'
CUR = 'Integer.IsEqual(Container(9701).CurrentItem,%d)'


def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:100], s.count(a))
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


pager = []
for n in range(1, 11):
    y = (n - 1) * 24
    pager.append('\t\t\t<control type="image"><left>0</left><top>%d</top><width>6</width><height>6</height><texture colordiffuse="73ffffff">fg/circle.png</texture><visible>!%s</visible></control>' % (y + 9, CUR % n))
    pager.append('\t\t\t<control type="image"><left>0</left><top>%d</top><width>6</width><height>22</height><texture colordiffuse="ffffffff">fg/bar.png</texture><visible>%s</visible></control>' % (y + 1, CUR % n))

FUSED = '''		<!-- Fused Glass (0.31.0, _src/fg_ss.py): pager as dots and a pill, clock capsule, now playing card -->
		<control type="group">
			<left>48</left><top>420</top>
			<visible>{F}</visible>
{PAGER}
		</control>
		<control type="group">
			<visible>{F} + Skin.HasSetting(aeon.ss.clock)</visible>
			<include content="FG_ClockCapsule"><param name="wx" value="Skin.HasSetting(aeon.ss.weather) + $EXP[AG_HasWeather]"/></include>
		</control>
		<control type="group">
			<left>1704</left><top>40</top>
			<visible>{F} + !Skin.HasSetting(aeon.ss.clock) + Skin.HasSetting(aeon.ss.weather) + $EXP[AG_HasWeather]</visible>
			<control type="image"><width>120</width><height>64</height><texture border="32" colordiffuse="fg_frost">fg/r32.png</texture></control>
			<control type="image"><width>120</width><height>64</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture></control>
			<control type="image"><left>18</left><top>16</top><width>32</width><height>32</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">$VAR[AG_WeatherIcon]</texture></control>
			<control type="label"><left>54</left><width>56</width><height>64</height><aligny>center</aligny><align>center</align><font>hm_ui_24</font><textcolor>dbffffff</textcolor><label>$INFO[Weather.Temperature]</label></control>
		</control>
		<control type="group">
			<left>1284</left><top>120</top>
			<visible>{F} + Player.HasAudio</visible>
			<animation effect="slide" end="0,-80" time="0" condition="!Skin.HasSetting(aeon.ss.clock) + ![Skin.HasSetting(aeon.ss.weather) + $EXP[AG_HasWeather]]">Conditional</animation>
			<control type="image"><left>-40</left><top>-40</top><width>620</width><height>228</height><texture border="64" colordiffuse="66000000">fg/sh24.png</texture></control>
			<control type="image"><width>540</width><height>148</height><texture border="24" colordiffuse="fg_frost">fg/r24.png</texture></control>
			<control type="image"><width>540</width><height>148</height><texture border="24" colordiffuse="fg_edge">fg/e24.png</texture></control>
			<control type="image"><left>18</left><top>18</top><width>112</width><height>112</height><aspectratio>scale</aspectratio><fadetime>300</fadetime><texture background="true" diffuse="fg/m112x112.png">$VAR[Aeon_SSCover]</texture></control>
			<control type="label"><left>150</left><top>22</top><width>320</width><height>24</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>9effffff</textcolor><label>[UPPERCASE]$INFO[MusicPlayer.Artist][/UPPERCASE]</label></control>
			<control type="label"><left>150</left><top>48</top><width>320</width><height>40</height><aligny>center</aligny><font>hm_ui_26_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[MusicPlayer.Title]</label></control>
			<control type="label"><left>150</left><top>90</top><width>320</width><height>28</height><aligny>center</aligny><font>hm_small_20</font><textcolor>99ffffff</textcolor><label>$INFO[MusicPlayer.Time]$INFO[MusicPlayer.Duration, / ]</label></control>
			<include content="FG_EqBarsM"><param name="left" value="484"/><param name="top" value="61"/><param name="col" value="ffffffff"/></include>
		</control>
'''.replace('{F}', F).replace('{PAGER}', '\n'.join(pager))

if __name__ == '__main__':
    # the clock capsule takes the weather condition as a param (default: weather is there)
    patch('Includes_Fused.xml', [
        ('''	<include name="FG_ClockCapsule">
		<control type="group">''', '''	<include name="FG_ClockCapsule">
		<param name="wx">$EXP[AG_HasWeather]</param>
		<definition>
		<control type="group">'''),
        ('''				<visible>$EXP[AG_HasWeather]</visible>
				<left>1588</left><top>40</top>''', '''				<visible>$PARAM[wx]</visible>
				<left>1588</left><top>40</top>'''),
        ('''				<visible>!$EXP[AG_HasWeather]</visible>
				<left>1680</left><top>40</top>''', '''				<visible>![$PARAM[wx]]</visible>
				<left>1680</left><top>40</top>'''),
    ])
    s = io.open('Includes_Fused.xml', encoding='utf-8').read()
    a = s.index('<include name="FG_ClockCapsule">')
    b = s.index('\n\t</include>', a)
    assert '</definition>' not in s[a:b]
    s = s[:b] + '\n\t\t</definition>' + s[b:]
    io.open('Includes_Fused.xml', 'w', encoding='utf-8', newline='').write(s)

    p = 'Custom_1156_Screensaver.xml'
    patch(p, [
        # poster: full height in Aeon / Glass, a floating rounded card in Fused Glass
        ('''			<texture background="true">$INFO[Container(9701).ListItem.Art(poster)]</texture>
			<visible>!String.IsEqual(Container(9701).ListItem.DBType,album)</visible>
		</control>''', '''			<texture background="true">$INFO[Container(9701).ListItem.Art(poster)]</texture>
			<visible>!String.IsEqual(Container(9701).ListItem.DBType,album) + !%s</visible>
		</control>
		<control type="image">
			<left>110</left><top>80</top><width>640</width><height>920</height>
			<texture border="64" colordiffuse="99000000">fg/sh24.png</texture>
			<visible>!String.IsEqual(Container(9701).ListItem.DBType,album) + %s + !String.IsEmpty(Container(9701).ListItem.Art(poster))</visible>
		</control>
		<control type="image">
			<left>150</left><top>120</top><width>560</width><height>840</height>
			<aspectratio>scale</aspectratio>
			<fadetime>700</fadetime>
			<texture background="true" diffuse="fg/m560x840.png">$INFO[Container(9701).ListItem.Art(poster)]</texture>
			<visible>!String.IsEqual(Container(9701).ListItem.DBType,album) + %s</visible>
		</control>''' % (F, F, F)),
        # album cover rounded
        ('''			<texture background="true">$INFO[Container(9701).ListItem.Art(thumb)]</texture>
			<visible>String.IsEqual(Container(9701).ListItem.DBType,album)</visible>
		</control>
		<control type="image">
			<left>174</left><top>164</top><width>753</width><height>753</height>
			<texture border="8" colordiffuse="2effffff">common/aeon_outline_sq.png</texture>
			<visible>String.IsEqual(Container(9701).ListItem.DBType,album)</visible>
		</control>''', '''			<texture background="true">$INFO[Container(9701).ListItem.Art(thumb)]</texture>
			<visible>String.IsEqual(Container(9701).ListItem.DBType,album) + !%s</visible>
		</control>
		<control type="image">
			<left>174</left><top>164</top><width>753</width><height>753</height>
			<aspectratio>scale</aspectratio>
			<fadetime>700</fadetime>
			<texture background="true" diffuse="fg/m753x753.png">$INFO[Container(9701).ListItem.Art(thumb)]</texture>
			<visible>String.IsEqual(Container(9701).ListItem.DBType,album) + %s</visible>
		</control>
		<control type="image">
			<left>174</left><top>164</top><width>753</width><height>753</height>
			<texture border="8" colordiffuse="2effffff">common/aeon_outline_sq.png</texture>
			<visible>String.IsEqual(Container(9701).ListItem.DBType,album) + !%s</visible>
		</control>''' % (F, F, F)),
        # old pager hidden in Fused
        ('''		<!-- pager dots -->
		<control type="group">
			<left>62</left>
			<top>300</top>''', '''		<!-- pager dots -->
		<control type="group">
			<left>62</left>
			<top>300</top>
			<visible>!%s</visible>''' % F),
        # old now playing row hidden in Fused
        ('''				<top>200</top>
				<visible>Player.HasAudio</visible>''', '''				<top>200</top>
				<visible>Player.HasAudio + !%s</visible>''' % F),
        # old clock / weather boxes hidden in Fused; the Fused parts after them
        ('''		<control type="group">
			<left>1820</left>
			<top>0</top>
			<control type="group">
				<visible>Skin.HasSetting(aeon.ss.clock)</visible>''', '''		<control type="group">
			<left>1820</left>
			<top>0</top>
			<visible>!%s</visible>
			<control type="group">
				<visible>Skin.HasSetting(aeon.ss.clock)</visible>''' % F),
        ('''	</controls>
</window>''', FUSED + '''	</controls>
</window>'''),
    ])
    print('screensaver ok')
