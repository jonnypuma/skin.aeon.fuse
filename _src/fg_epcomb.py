"""0.44.0 Fused Glass library view Episode combined (538; mockup board EpisodeCombined). Run from the skin folder.

The episodes of one season: season pills (5381, the show's seasons from script.aeon.helper ?info=seasons, a tick when
watched, a dot for the season on screen) and a sort pill (5382, Container.SortDirection); at the left the season poster,
the number of episodes, "1 in progress · 3 unwatched" and the next airing; in the middle a card with the episodes (538:
thumb with a yellow progress line, EPISODE 1 · 74 MIN, title, resolution and audio pills, minutes left on the row in
focus, a dot on unwatched ones); at the right the episode in focus: its thumb with "35:44 of 73:34 · 38 min left",
S3 E1 · SEASON PREMIERE, title, minutes · rating · date · Ends, media pills and the plot. Offered for episode lists in
Fused Glass (Kodi falls back to another view elsewhere)."""
import io
import os
import re

from PIL import Image, ImageDraw

from fg_lib import row_chips          # 0.52.0: the media chips of the rows

FUSED = '1080i/Includes_Fused.xml'
VIEWS = '1080i/Includes_Views_Video.xml'
NAV = '1080i/MyVideoNav.xml'
PICK = '1080i/Custom_1165_VideoViews.xml'
CARD = '1080i/Includes_Aeon_Picker.xml'
A = '$ADDON[skin.aeon.fuse %d]'
L = 'Container(538).ListItem'
EP = '[Container.Content(episodes) + Skin.HasSetting(aeon.fglass)]'

# rounded masks: row thumbs and the big thumb
for (w, h, r) in ((178, 100, 12), (580, 326, 16)):
    im = Image.new('L', (w * 4, h * 4), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], r * 4, fill=255)
    out = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    out.putalpha(im.resize((w, h), Image.LANCZOS))
    out.save(os.path.join('media', 'fg', 'm%dx%d.png' % (w, h)), optimize=True)

VARS = '''	<variable name="FG_EcAudio">
		<value condition="String.StartsWith(ListItem.AudioCodec,truehd) + String.Contains(ListItem.AudioCodec,atmos)">TrueHD Atmos</value>
		<value condition="String.StartsWith(ListItem.AudioCodec,eac3) + String.Contains(ListItem.AudioCodec,atmos)">DD+ Atmos</value>
		<value condition="String.IsEqual(ListItem.AudioCodec,ac3) | String.IsEqual(ListItem.AudioCodec,dolbydigital)">DD$VAR[VidInfo_AudioChannels]</value>
		<value condition="!String.IsEmpty(ListItem.AudioCodec)">$VAR[VidInfo_AudioCodec]$VAR[VidInfo_AudioChannels]</value>
	</variable>
	<variable name="FG_EcAudioF">
		<value condition="String.StartsWith(%(L)s.AudioCodec,truehd) + String.Contains(%(L)s.AudioCodec,atmos)">TrueHD Atmos$VAR[FG_EcChanF]</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,eac3) + String.Contains(%(L)s.AudioCodec,atmos)">DD+ Atmos$VAR[FG_EcChanF]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,truehd)">TrueHD$VAR[FG_EcChanF]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,eac3)">DD+$VAR[FG_EcChanF]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,ac3) | String.IsEqual(%(L)s.AudioCodec,dolbydigital)">DD$VAR[FG_EcChanF]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,dtshd_ma_x) | String.IsEqual(%(L)s.AudioCodec,dts-x)">DTS:X$VAR[FG_EcChanF]</value>
		<value condition="String.IsEqual(%(L)s.AudioCodec,dtshd_ma) | String.IsEqual(%(L)s.AudioCodec,dtsma)">DTS-HD MA$VAR[FG_EcChanF]</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,dts) | String.IsEqual(%(L)s.AudioCodec,dca)">DTS$VAR[FG_EcChanF]</value>
		<value condition="String.StartsWith(%(L)s.AudioCodec,aac)">AAC$VAR[FG_EcChanF]</value>
		<value condition="!String.IsEmpty(%(L)s.AudioCodec)">[UPPERCASE]$INFO[%(L)s.AudioCodec][/UPPERCASE]$VAR[FG_EcChanF]</value>
	</variable>
	<variable name="FG_EcChanF">
		<value condition="Integer.IsEqual(%(L)s.AudioChannels,8)"> 7.1</value>
		<value condition="Integer.IsEqual(%(L)s.AudioChannels,6)"> 5.1</value>
		<value condition="Integer.IsEqual(%(L)s.AudioChannels,2)"> 2.0</value>
	</variable>
	<variable name="FG_EcResF">
		<value condition="String.IsEqual(%(L)s.VideoResolution,8K)">8K</value>
		<value condition="String.IsEqual(%(L)s.VideoResolution,4K) | String.IsEqual(%(L)s.VideoResolution,2160)">4K</value>
		<value condition="String.IsEqual(%(L)s.VideoResolution,1080)">1080p</value>
		<value condition="String.IsEqual(%(L)s.VideoResolution,720)">720p</value>
		<value condition="!String.IsEmpty(%(L)s.VideoResolution)">SD</value>
	</variable>
	<variable name="FG_EcHdrF">
		<value condition="String.IsEqual(%(L)s.HdrType,dolbyvision)">DV</value>
		<value condition="String.IsEqual(%(L)s.HdrType,hdr10plus)">HDR10+</value>
		<value condition="String.IsEqual(%(L)s.HdrType,hdr10)">HDR10</value>
		<value condition="String.IsEqual(%(L)s.HdrType,hlg)">HLG</value>
		<value condition="!String.IsEmpty(%(L)s.VideoResolution)">SDR</value>
	</variable>
	<variable name="FG_EcMark">
		<value condition="String.IsEqual(Window(Home).Property(aeon.epm.538),series_premiere)">  ·  $LOCALIZE[31394]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.epm.538),season_premiere)">  ·  $LOCALIZE[31395]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.epm.538),series_finale)">  ·  $LOCALIZE[31396]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.epm.538),season_finale)">  ·  $LOCALIZE[31397]</value>
	</variable>
	<variable name="FG_EcSort">
		<value condition="Container.SortDirection(descending)">$LOCALIZE[20360] $INFO[Container(538).NumItems] → 1</value>
		<value>$LOCALIZE[20360] 1 → $INFO[Container(538).NumItems]</value>
	</variable>
	<variable name="FG_EcPoster">
		<value condition="!String.IsEmpty(%(L)s.Art(season.poster))">$INFO[%(L)s.Art(season.poster)]</value>
		<value>$INFO[%(L)s.Art(tvshow.poster)]</value>
	</variable>
	<variable name="FG_EcThumb">
		<value condition="!String.IsEmpty(ListItem.Art(thumb))">$INFO[ListItem.Art(thumb)]</value>
		<value>$INFO[ListItem.Art(fanart)]</value>
	</variable>
''' % {'L': L}


def row(focused):
    """One episode in the card: 710 x 124 at a 130 px pitch."""
    lit = 'Control.HasFocus(538)'
    ink = '$VAR[FG_EcInk]' if focused else 'ffffffff'
    ink2 = '$VAR[FG_EcInk2]' if focused else 'a6ffffff'
    pill = '$VAR[FG_EcPill]' if focused else '66ffffff'
    out = ''
    if focused:
        # 0.56.2: the bar in the Focus highlight style (Pill, Flat, Frosted, Outline, Tight), _src/fg_lib_focus.py
        import fg_lib_focus
        out += fg_lib_focus.style_bar(0, 0, 710, 124, lit)        # Flat: bars outside the list, fg_lib_focus.apply()
    # 0.56.8 the list row rule, as the other lists: the title, under it the grey line (Episode N · first aired) and the
    # chips, at the right the run time (bold), or the time left of an episode in progress on every row; the mark last
    # (ring, dot, tick). The still keeps its bar. The caps kicker above the title is gone.
    import fg_lib
    out += ('<control type="image"><left>12</left><top>12</top><width>178</width><height>100</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m178x100.png">$VAR[FG_EcThumb]</texture></control>'
            '<control type="progress"><left>22</left><top>99</top><width>158</width><height>6</height><texturebg border="3,0,3,0" colordiffuse="59ffffff">fg/pillh.png</texturebg>'
            '<midtexture border="3,0,3,0" colordiffuse="fg_mark">fg/pillh.png</midtexture><info>ListItem.PercentPlayed</info><visible>Integer.IsGreater(ListItem.PercentPlayed,0)</visible></control>'
            '<control type="label"><left>208</left><top>12</top><width>440</width><height>38</height><aligny>center</aligny><font>lb_ui_26_semibold</font><textcolor>%(ink)s</textcolor><selectedcolor>%(ink)s</selectedcolor><label>$INFO[ListItem.Title]</label></control>'
            '<control type="label"><left>208</left><top>50</top><width>290</width><height>30</height><aligny>center</aligny><font>lb_small_20</font><textcolor>%(ink2)s</textcolor><selectedcolor>%(ink2)s</selectedcolor><label>$VAR[FG_L_RowSub]</label></control>'
            + fg_lib.row_chips_right(652, 86, 26, ink, pill, 208) +      # 0.56.11: right-aligned under the run time
            '<control type="label"><left>502</left><top>43</top><width>150</width><height>38</height><align>right</align><aligny>center</aligny><font>lb_ui_24_semibold</font><textcolor>%(ink)s</textcolor><selectedcolor>%(ink)s</selectedcolor><label>$VAR[FG_L_RowRight]</label></control>')
    out = out.replace('%(ink)s', ink).replace('%(ink2)s', ink2).replace('%(pill)s', pill)
    out += fg_lib.marks('', 664, 48, 28, lit if focused else None)
    return out


def detail_pill(label, vis):
    return ('\t\t\t\t\t<control type="button"><width min="40" max="400">auto</width><height>36</height><label>%s</label><font>lb_small_20_bold</font>'
            '<textoffsetx>14</textoffsetx><align>center</align><aligny>center</aligny><textcolor>ffffffff</textcolor><focusedcolor>ffffffff</focusedcolor>'
            '<texturenofocus border="10" colordiffuse="66ffffff">fg/e12.png</texturenofocus><texturefocus border="10" colordiffuse="66ffffff">fg/e12.png</texturefocus>'
            '<visible>%s</visible></control>\n' % (label, vis))


VIEW = '''	<include name="Aeon_V538_View">
		<control type="group">
			<visible>Control.IsVisible(538)</visible>
			<include>Anim_FadeVisible</include>
			<include>Aeon_V_Bg</include>
			<!-- header: TV SHOWS > the show, and the season (the board's header instead of the views' shared one) -->
			<control type="label"><left>120</left><top>34</top><width>1600</width><height>32</height><aligny>center</aligny><font>lb_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[20343]$INFO[%(L)s.TVShowTitle,  ›  ,][/UPPERCASE]</label></control>
			<control type="label"><left>116</left><top>62</top><width>1600</width><height>84</height><aligny>center</aligny><font>lb_aeon_title_66</font><textcolor>ffffffff</textcolor><label>$VAR[FG_EcSeasonName]</label></control>
			<!-- season pills and the sort pill -->
			<control type="list" id="5381">
				<left>112</left><top>166</top><width>820</width><height>52</height>
				<orientation>horizontal</orientation>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<onup condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onup>
				<ondown>538</ondown><onright>5382</onright><onback>538</onback>
				<onclick>Container.Update($INFO[Container(5381).ListItem.FolderPath],replace)</onclick>
				<itemlayout width="198" height="52">
					<control type="image"><left>0</left><top>2</top><width>188</width><height>48</height><texture border="24" colordiffuse="$VAR[FG_EcSeasonBg]">fg/r24.png</texture></control>
					<control type="label"><left>18</left><top>2</top><width>132</width><height>48</height><aligny>center</aligny><font>lb_ui_22_semibold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>$INFO[ListItem.Label]$INFO[ListItem.Label2, · ,]</label></control>
					<control type="image"><left>152</left><top>16</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="b3ffffff">aeon/icons/check.png</texture><visible>!String.IsEmpty(ListItem.Property(aeon.ec.done))</visible></control>
					<control type="image"><left>156</left><top>21</top><width>10</width><height>10</height><texture colordiffuse="fg_mark">fg/circle.png</texture><visible>String.IsEmpty(ListItem.Property(aeon.ec.done)) + !String.IsEmpty(ListItem.Property(aeon.ec.here))</visible></control>
				</itemlayout>
				<focusedlayout width="198" height="52">
					<control type="image"><left>0</left><top>2</top><width>188</width><height>48</height><texture border="24" colordiffuse="$VAR[FG_EcSeasonBg]">fg/r24.png</texture><visible>!Control.HasFocus(5381)</visible></control>
					<control type="image"><left>0</left><top>2</top><width>188</width><height>48</height><texture border="24" colordiffuse="ffffffff">fg/r24.png</texture><visible>Control.HasFocus(5381)</visible></control>
					<control type="label"><left>18</left><top>2</top><width>132</width><height>48</height><aligny>center</aligny><font>lb_ui_22_semibold</font><textcolor>$VAR[FG_EcPillInk]</textcolor><selectedcolor>$VAR[FG_EcPillInk]</selectedcolor><label>$INFO[ListItem.Label]$INFO[ListItem.Label2, · ,]</label></control>
					<control type="image"><left>152</left><top>16</top><width>18</width><height>18</height><aspectratio>keep</aspectratio><texture colordiffuse="$VAR[FG_EcPillInk]">aeon/icons/check.png</texture><visible>!String.IsEmpty(ListItem.Property(aeon.ec.done))</visible></control>
					<control type="image"><left>156</left><top>21</top><width>10</width><height>10</height><texture colordiffuse="fg_mark">fg/circle.png</texture><visible>String.IsEmpty(ListItem.Property(aeon.ec.done)) + !String.IsEmpty(ListItem.Property(aeon.ec.here))</visible></control>
				</focusedlayout>
				<content target="videos">plugin://script.aeon.helper/?info=seasons&amp;path=$INFO[Container.FolderPath]</content>
			</control>
			<control type="button" id="5382">
				<left>950</left><top>168</top><width min="80" max="400">auto</width><height>48</height>
				<label>$VAR[FG_EcSort]</label><font>lb_ui_22_semibold</font><textoffsetx>22</textoffsetx><aligny>center</aligny>
				<textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor>
				<texturenofocus border="24" colordiffuse="fg_frost">fg/r24.png</texturenofocus><texturefocus border="24" colordiffuse="ffffffff">fg/r24.png</texturefocus>
				<onclick>Container.SortDirection</onclick>
				<onleft>5381</onleft><ondown>538</ondown><onback>538</onback>
				<onup condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onup>
			</control>
			<!-- the season: poster and how far you are -->
			<control type="image"><left>120</left><top>252</top><width>300</width><height>440</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture></control>
			<control type="image"><left>120</left><top>252</top><width>300</width><height>440</height><aspectratio scalediffuse="false">scale</aspectratio><texture background="true" diffuse="fg/m300x440.png">$VAR[FG_EcPoster]</texture></control>
			<control type="label"><left>120</left><top>708</top><width>300</width><height>34</height><aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$INFO[Container(538).NumItems] $LOCALIZE[20360]</label></control>
			<control type="label"><left>120</left><top>742</top><width>320</width><height>30</height><aligny>center</aligny><font>lb_small_20</font><textcolor>b3ffffff</textcolor><label>$INFO[Window(Home).Property(aeon.ec.stats)]</label></control>
			<control type="textbox"><left>120</left><top>772</top><width>320</width><height>60</height><font>lb_small_20</font><textcolor>b3ffffff</textcolor><label>$INFO[Window(Home).Property(aeon.ec.next)]</label></control>
@@STUDIO538@@
			<!-- the episodes -->
			<control type="image"><left>457</left><top>252</top><width>734</width><height>792</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture></control>
			<control type="image"><left>457</left><top>252</top><width>734</width><height>792</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture></control>
			<control type="list" id="538">
				<left>469</left><top>264</top><width>710</width><height>780</height>
				<orientation>vertical</orientation>
				<viewtype label="@@NAME@@">list</viewtype>
				<visible>@@EP@@</visible>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<onback condition="String.IsEqual(Skin.String(aeon.backmode),home)">ActivateWindow(home)</onback>
				<onup>5381</onup>
				<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft>
				<onright>5380001</onright>
				<itemlayout width="710" height="130">@@ROW@@</itemlayout>
				<focusedlayout width="710" height="130">@@FROW@@</focusedlayout>
			</control>
			<!-- the episode in focus -->
			<control type="group">
				<left>1228</left><top>252</top>
				<control type="image"><left>0</left><top>0</top><width>580</width><height>326</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture></control>
				<control type="image"><left>0</left><top>0</top><width>580</width><height>326</height><aspectratio scalediffuse="false">scale</aspectratio><fadetime>200</fadetime><texture background="true" diffuse="fg/m580x326.png">$INFO[%(L)s.Art(thumb)]</texture></control>
				<control type="group">
					<visible>!String.IsEmpty(Window(Home).Property(aeon.ec.resume)) + Integer.IsGreater(%(L)s.PercentPlayed,0)</visible>
					<control type="image"><left>0</left><top>186</top><width>580</width><height>140</height><texture colordiffuse="d9000000" diffuse="fg/m580x326.png">aeon/osd_scrim_bottom.png</texture></control>
					
					<control type="progress"><left>20</left><top>302</top><width>540</width><height>6</height><texturebg border="3,0,3,0" colordiffuse="59ffffff">fg/pillh.png</texturebg><midtexture border="3,0,3,0" colordiffuse="fg_mark">fg/pillh.png</midtexture><info>%(L)s.PercentPlayed</info></control>
				</control>
				<control type="label"><left>0</left><top>344</top><width>580</width><height>30</height><aligny>center</aligny><font>lb_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]S$INFO[%(L)s.Season] E$INFO[%(L)s.Episode]$VAR[FG_EcMark][/UPPERCASE]</label></control>
				<control type="label"><left>0</left><top>374</top><width>580</width><height>56</height><aligny>center</aligny><font>lb_font36_title</font><textcolor>ffffffff</textcolor><label>$INFO[%(L)s.Title]</label></control>
				<control type="label"><left>0</left><top>432</top><width>580</width><height>36</height><aligny>center</aligny><font>lb_ui_22</font><textcolor>e6ffffff</textcolor>
					<label>$VAR[FG_L538_Meta]</label></control>
				<control type="grouplist">
					<left>0</left><top>520</top><width>580</width><height>36</height>
					<orientation>horizontal</orientation><itemgap>8</itemgap><usecontrolcoords>true</usecontrolcoords>
@@PILLS@@				</control>
				@@STATUS@@
				<control type="textbox"><left>0</left><top>572</top><width>580</width><height>156</height><font>lb_body_24</font><textcolor>d9ffffff</textcolor><label>$INFO[%(L)s.Plot]</label><autoscroll delay="8000" time="2000" repeat="8000">true</autoscroll></control>
			</control>
			<include content="Aeon_M_Nav"><param name="icon" value="common/aeon_film.png"/><param name="cid" value="538"/><param name="base" value="53800"/><param name="scroll" value="true"/></include>
		</control>
	</include>
''' % {'L': L}
VARS += '''	<variable name="FG_EcSeasonName">
		<value condition="Integer.IsEqual(Container(538).ListItem.Season,0)">$LOCALIZE[20381]</value>
		<value condition="!String.IsEmpty(Container(538).ListItem.Season)">$LOCALIZE[20373] $INFO[Container(538).ListItem.Season]</value>
		<value>$INFO[Container.FolderName]</value>
	</variable>
	<variable name="FG_EcInk">
		<value condition="Control.HasFocus(538) + !$EXP[FG_FocusLight]">aeon_onbar</value>
		<value>ffffffff</value>
	</variable>
	<variable name="FG_EcInk2">
		<value condition="Control.HasFocus(538) + !$EXP[FG_FocusLight]">99000000</value>
		<value>a6ffffff</value>
	</variable>
	<variable name="FG_EcPill">
		<value condition="Control.HasFocus(538) + !$EXP[FG_FocusLight]">59000000</value>
		<value>66ffffff</value>
	</variable>
	<variable name="FG_EcPillInk">
		<value condition="Control.HasFocus(5381)">aeon_onbar</value>
		<value>ffffffff</value>
	</variable>
	<variable name="FG_EcSeasonBg">
		<value condition="!String.IsEmpty(ListItem.Property(aeon.ec.here))">40ffffff</value>
		<value>fg_frost</value>
	</variable>
'''
# 0.56.9 the info panel rule: the row's chips in the row's order (resolution, audio, aspect ratio, HDR with the Dolby
# Vision profile; no SDR), the facts in the rule's order, the status line with the mark (FG_L538_* from focus_vars)
import fg_lib
import fg_lib_walls
pills = (detail_pill('$VAR[FG_L538_Res]', '!String.IsEmpty(%s.VideoResolution)' % L) +
         detail_pill('$VAR[FG_L538_Audio]', '!String.IsEmpty(%s.AudioCodec)' % L) +
         detail_pill('$INFO[%s.VideoAspect]:1' % L, '!String.IsEmpty(%s.VideoAspect)' % L) +
         detail_pill('$VAR[FG_L538_Hdr]', '!String.IsEmpty(%s.HdrType)' % L))
VARS += fg_lib_walls.focus_vars(538).replace('<variable name="FG_L538_Status">', '<variable name="FG_L538_Status">\n\t\t<value condition="Integer.IsGreater(%s.PercentPlayed,0) + !String.IsEmpty(Window(Home).Property(aeon.ec.resume))">$INFO[Window(Home).Property(aeon.ec.resume)]</value>' % L, 1)
STATUS = fg_lib.status_line('538', 580, 32, 0, 478)
VIEW = (VIEW.replace('@@NAME@@', A % 32544).replace('@@EP@@', EP).replace('@@ROW@@', row(False)).replace('@@FROW@@', row(True))
        .replace('@@PILLS@@', pills).replace('@@STATUS@@', '\t\t\t\t' + STATUS)
        .replace('@@STUDIO538@@', '\t\t\t' + __import__('fg_lib_lists').studio(538, 120, 940, 240, 76, 'left', 'bottom')))

# poster mask 300 x 440
im = Image.new('L', (1200, 1760), 0)
ImageDraw.Draw(im).rounded_rectangle([0, 0, 1199, 1759], 64, fill=255)
out = Image.new('RGBA', (300, 440), (255, 255, 255, 0))
out.putalpha(im.resize((300, 440), Image.LANCZOS))
out.save(os.path.join('media', 'fg', 'm300x440.png'), optimize=True)

BODY = ('\t<!-- FG_EPCOMB:begin (written by _src/fg_epcomb.py) ====================== Episode combined view 538 (0.44.0) -->\n'
        + VARS + VIEW + '\t<!-- FG_EPCOMB:end -->\n')
f = io.open(FUSED, encoding='utf-8').read()
f = re.sub(r'\t<!-- FG_EPCOMB:begin.*?<!-- FG_EPCOMB:end -->\n', '', f, flags=re.S)
f = f.replace('</includes>', BODY + '</includes>')
import fg_lib_focus                     # noqa: E402  0.56.2: Focus highlight styles, the flat bars outside the list
f = fg_lib_focus.apply(f)
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)

v = io.open(VIEWS, encoding='utf-8').read()
if 'Aeon_V538_View' not in v:
    a = '\t\t<include>Aeon_V537_View</include>\n'
    assert v.count(a) == 1
    v = v.replace(a, a + '\t\t<include>Aeon_V538_View</include>\n')
    io.open(VIEWS, 'w', encoding='utf-8', newline='\n').write(v)
n = io.open(NAV, encoding='utf-8').read()
if ',538,' not in n:
    n = n.replace(',536,537,50</views>', ',536,537,538,50</views>')
    assert ',538,' in n
    io.open(NAV, 'w', encoding='utf-8', newline='\n').write(n)
p = io.open(PICK, encoding='utf-8').read()
if '<icon>538</icon>' not in p:
    a = '\t\t\t</content>'
    assert p.count(a) == 1
    p = p.replace(a, '\t\t\t\t<item><label>%s</label><label2>%s</label2><icon>538</icon><onclick>Dialog.Close(1165,true)</onclick><onclick>Container.SetViewMode(538)</onclick><visible>%s</visible></item>\n'
                  % (A % 32544, A % 32545, EP) + a)
    io.open(PICK, 'w', encoding='utf-8', newline='\n').write(p)
c = io.open(CARD, encoding='utf-8').read()
if '32545' not in c and 'ListItem.Icon,538' not in c:          # 0.46.0: the picker mock-up is fg_pick538.py's now
    # the picker card's sketch: pills, a poster, rows in a card, a big thumb with lines
    sketch = ('\t\t\t<control type="group"><visible>String.IsEqual(ListItem.Label2,%s)</visible>'
              '<control type="image"><left>14</left><top>16</top><width>40</width><height>10</height><texture colordiffuse="66ffffff">common/white.png</texture></control>'
              '<control type="image"><left>60</left><top>16</top><width>40</width><height>10</height><texture colordiffuse="66ffffff">common/white.png</texture></control>'
              '<control type="image"><left>106</left><top>16</top><width>40</width><height>10</height><texture colordiffuse="b3ffffff">common/white.png</texture></control>'
              '<control type="image"><left>14</left><top>40</top><width>50</width><height>74</height><texture colordiffuse="59ffffff">common/white.png</texture></control>'
              '<control type="image"><left>72</left><top>40</top><width>100</width><height>22</height><texture colordiffuse="ffffffff">common/white.png</texture></control>'
              '<control type="image"><left>72</left><top>66</top><width>100</width><height>22</height><texture colordiffuse="40ffffff">common/white.png</texture></control>'
              '<control type="image"><left>72</left><top>92</top><width>100</width><height>22</height><texture colordiffuse="40ffffff">common/white.png</texture></control>'
              '<control type="image"><left>180</left><top>40</top><width>76</width><height>44</height><texture colordiffuse="59ffffff">common/white.png</texture></control>'
              '<control type="image"><left>180</left><top>92</top><width>60</width><height>8</height><texture colordiffuse="40ffffff">common/white.png</texture></control>'
              '<control type="image"><left>180</left><top>106</top><width>76</width><height>8</height><texture colordiffuse="40ffffff">common/white.png</texture></control></control>\n'
              % (A % 32545))
    m = re.search(r'(\t<include name="Aeon_Pk_Card">.*?)(\t\t</definition>|\t</include>)', c, re.S)
    assert m
    c = c[:m.start(2)] + sketch + c[m.start(2):]
    io.open(CARD, 'w', encoding='utf-8', newline='\n').write(c)
import xml.etree.ElementTree as ET
for name in (FUSED, VIEWS, NAV, PICK, CARD):
    ET.parse(name)
print('ok')
