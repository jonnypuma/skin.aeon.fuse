"""Weather slide of the screensaver (Custom_1156_Screensaver.xml, 0.30.0): the fourth of the ten slides shows today's and
this week's weather when the screensaver's weather switch is on and the weather add-on has a forecast. Run from 1080i."""
import io

F = 'Skin.HasSetting(aeon.fglass)'
ICONS = 'resource://resource.images.weathericons.white/'
SHOW = ('Skin.HasSetting(aeon.ss.weather) + !String.IsEmpty(Weather.Temperature) + '
        '!String.IsEmpty(Window(Weather).Property(Daily.1.ShortDay)) + Integer.IsEqual(Container(9701).CurrentItem,4)')

cols = []
for d in range(1, 8):
    P = 'Window(Weather).Property(Daily.%d.%%s)' % d
    day = '$LOCALIZE[33006]' if d == 1 else '$INFO[%s]' % (P % 'LongDay')
    x = (d - 1) * 242
    cols.append(
        '\t\t\t\t<control type="group"><left>%d</left><top>0</top>\n'
        '\t\t\t\t\t<control type="label"><left>22</left><top>22</top><width>210</width><height>32</height><font>ui_24_semibold</font><textcolor>ffffffff</textcolor><label>%s</label></control>\n'
        '\t\t\t\t\t<control type="image"><left>22</left><top>62</top><width>84</width><height>84</height><aspectratio align="left">keep</aspectratio><texture>%s$INFO[%s]</texture><visible>System.HasAddon(resource.images.weathericons.white)</visible></control>\n'
        '\t\t\t\t\t<control type="image"><left>22</left><top>74</top><width>60</width><height>60</height><aspectratio align="left">keep</aspectratio><texture>aeon/icons/cloud.png</texture><visible>!System.HasAddon(resource.images.weathericons.white)</visible></control>\n'
        '\t\t\t\t\t<control type="label"><left>22</left><top>154</top><width>210</width><height>36</height><font>ui_28_bold</font><textcolor>ffffffff</textcolor><label>$INFO[%s]</label></control>\n'
        '\t\t\t\t\t<control type="label"><left>22</left><top>188</top><width>210</width><height>28</height><font>small_20_semibold</font><textcolor>a3ffffff</textcolor><label>$INFO[%s]</label></control>\n'
        '\t\t\t\t\t<control type="label"><left>22</left><top>214</top><width>210</width><height>24</height><font>cap_16</font><textcolor>8fffffff</textcolor><label>$INFO[%s]</label></control>\n'
        '\t\t\t\t</control>' % (x, day, ICONS, P % 'OutlookIcon', P % 'HighTemperature', P % 'LowTemperature', P % 'Outlook'))

details = [
    '$LOCALIZE[33006] $INFO[Window(Weather).Property(Daily.1.HighTemperature)] / $INFO[Window(Weather).Property(Daily.1.LowTemperature)]',
    '$LOCALIZE[402] $INFO[Window(Weather).Property(Current.FeelsLike)]°',
    '$LOCALIZE[404]: $INFO[Window(Weather).Property(Current.Wind)]',
    '$LOCALIZE[406]: $INFO[Window(Weather).Property(Current.Humidity)]',
    '$LOCALIZE[33027] $INFO[Window(Weather).Property(Today.Sunrise)]',
    '$LOCALIZE[33028] $INFO[Window(Weather).Property(Today.Sunset)]',
]
detail_xml = '\n'.join(
    '\t\t\t\t<control type="label"><width>auto</width><height>34</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>d9ffffff</textcolor><label>%s</label></control>' % d
    for d in details)

block = '''		<!-- weather slide (0.30.0): the fourth slide shows today's and this week's weather, over the weather fanart, while
		     the screensaver's weather switch is on (Skin settings > Backgrounds) and the weather add-on has a forecast.
		     Built by _src/wx_screensaver.py. -->
		<control type="group">
			<visible>{SHOW}</visible>
			<animation type="Visible" tween="cubic" easing="out"><effect type="fade" start="0" end="100" time="700"/></animation>
			<animation type="Hidden" tween="cubic" easing="in"><effect type="fade" start="100" end="0" time="500"/></animation>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="ff0a0a0a">common/white.png</texture></control>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><texture background="true" colordiffuse="e6ffffff">$VAR[Aeon_WxBg]</texture></control>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="fg_scrim">fg/scrim_l.png</texture></control>
			<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="fg_scrim">fg/scrim_b.png</texture></control>
			<control type="label"><left>120</left><top>176</top><width>1200</width><height>30</height><font>cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$INFO[Weather.Location][/UPPERCASE]</label></control>
			<control type="image"><left>112</left><top>212</top><width>200</width><height>200</height><aspectratio>keep</aspectratio><texture>$VAR[Aeon_WxIcon]</texture></control>
			<control type="label"><left>336</left><top>216</top><width>800</width><height>130</height><aligny>center</aligny><font>display_84</font><textcolor>ffffffff</textcolor><label>$INFO[Weather.Temperature]</label></control>
			<control type="label"><left>340</left><top>346</top><width>1000</width><height>48</height><aligny>center</aligny><font>ui_30_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[Weather.Conditions]</label></control>
			<control type="grouplist">
				<left>120</left><top>440</top><width>1680</width><height>34</height><orientation>horizontal</orientation><itemgap>30</itemgap>
{DETAILS}
			</control>
			<control type="label"><left>120</left><top>690</top><width>800</width><height>30</height><font>cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$ADDON[skin.aeon.fuse 32404][/UPPERCASE]</label></control>
			<control type="image"><left>112</left><top>728</top><width>1696</width><height>256</height><texture border="24" colordiffuse="fg_frost">fg/r24.png</texture><visible>{F}</visible></control>
			<control type="image"><left>112</left><top>728</top><width>1696</width><height>256</height><texture border="24" colordiffuse="fg_edge">fg/e24.png</texture><visible>{F}</visible></control>
			<control type="image"><left>112</left><top>728</top><width>1696</width><height>256</height><texture colordiffuse="73000000">common/white.png</texture><visible>!{F}</visible></control>
			<control type="group"><left>112</left><top>728</top>
{COLS}
			</control>
		</control>
'''
block = block.replace('{SHOW}', SHOW).replace('{DETAILS}', detail_xml).replace('{COLS}', '\n'.join(cols)).replace('{F}', F)

p = 'Custom_1156_Screensaver.xml'
s = io.open(p, encoding='utf-8').read()
if 'weather slide (0.30.0)' not in s:
    anchor = '\t\t<!-- clock box and weather box, top right, as on Home'
    assert s.count(anchor) == 1
    s = s.replace(anchor, block + anchor)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('screensaver ok')
