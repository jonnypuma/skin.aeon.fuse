"""Home > Favourites (all themes; 0.32.0). Run once from 1080i: adds Aeon_H_FavBg / Aeon_H_Favourites to
Includes_Fused.xml and wires them into Includes_Aeon_Home.xml (background, section layer, Down from the menu).
The heart picture is made by _src/bg_favourites.py, the card mask by fg_textures.py."""
import io

F = '$EXP[Aeon_FGlass]'
SD = '<aspectratio scalediffuse="false">scale</aspectratio>'
KINDS = [('all', '$LOCALIZE[593]'), ('video', '$LOCALIZE[157]'), ('music', '$LOCALIZE[2]'), ('addons', '$LOCALIZE[24001]')]


def sel(k):
    if k == 'all':
        return '[String.IsEmpty(Window(Home).Property(aeon.favkind)) | String.IsEqual(Window(Home).Property(aeon.favkind),all)]'
    return 'String.IsEqual(Window(Home).Property(aeon.favkind),%s)' % k


TAB = '''				<control type="grouplist">
					<left>112</left><top>{top}</top><width>528</width><height>40</height>
					<orientation>horizontal</orientation><align>right</align><usecontrolcoords>true</usecontrolcoords>
					<control type="button"><width min="0" max="528">auto</width><height>40</height><textoffsetx>20</textoffsetx><aligny>center</aligny><font>hm_ui_22_semibold</font><textcolor>ffffffff</textcolor><focusedcolor>ffffffff</focusedcolor><label>{lab}</label><include>FG_TabTex</include><visible>{sel}</visible></control>
					<control type="button"><width min="0" max="528">auto</width><height>40</height><textoffsetx>20</textoffsetx><aligny>center</aligny><font>hm_ui_22</font><textcolor>94ffffff</textcolor><focusedcolor>94ffffff</focusedcolor><label>{lab}</label><texturenofocus /><texturefocus /><visible>!{sel}</visible></control>
				</control>'''

CARD = '''						<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height>{SD}<texture background="true" diffuse="fg/m280x158.png">$VAR[Aeon_FavArtL]</texture><visible>!String.IsEmpty(ListItem.Art(fanart)) | !String.IsEmpty(ListItem.Art(landscape))</visible></control>
						<control type="image"><left>36</left><top>24</top><width>240</width><height>138</height><aspectratio>keep</aspectratio><texture background="true">$VAR[Aeon_FavArtK]</texture><visible>String.IsEmpty(ListItem.Art(fanart)) + String.IsEmpty(ListItem.Art(landscape))</visible></control>'''

BODY = '''
	<!-- ===================================================== Home > Favourites (all themes; 0.32.0)
	     Over the heart picture (common/aeon_bg_favourites.jpg): Kodi's favourites as a row of cards under the menu (list
	     9309, Down from the menu), from script.aeon.helper (?info=favourites&kind=...: a favourite of a library show,
	     film, set, album or artist brings its artwork and plot). Left of the row the groups All / Video / Music /
	     Add-ons; Up / Down on the row change the group (Up from All: back to the menu). The card in focus is the
	     spotlight: its fanart behind, its clearlogo (or title), what it is and its plot at the top left. OK opens it as
	     Kodi's Favourites window does; OK on the menu item still opens that window. Built by _src/fg_fav.py. -->
	<expression name="Aeon_H_FavSec">String.IsEqual(Container(9000).ListItem.Label2,favourites)</expression>
	<variable name="Aeon_FavKind">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.favkind))">$INFO[Window(Home).Property(aeon.favkind)]</value>
		<value>all</value>
	</variable>
	<!-- the whole path in one variable; aeon.fav.stamp (helper) changes with the favourites, so the row reloads -->
	<variable name="Aeon_FavPath">
		<value condition="String.IsEqual(Window(Home).Property(aeon.favkind),video)">plugin://script.aeon.helper/?info=favourites&amp;kind=video$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.favkind),music)">plugin://script.aeon.helper/?info=favourites&amp;kind=music$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.favkind),addons)">plugin://script.aeon.helper/?info=favourites&amp;kind=addons$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
		<value>plugin://script.aeon.helper/?info=favourites&amp;kind=all$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
	</variable>
	<variable name="Aeon_FavKindName">
		<value condition="String.IsEqual(Window(Home).Property(aeon.favkind),video)">$LOCALIZE[157]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.favkind),music)">$LOCALIZE[2]</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.favkind),addons)">$LOCALIZE[24001]</value>
		<value>$LOCALIZE[593]</value>
	</variable>
	<variable name="Aeon_FavArtL">
		<value condition="!String.IsEmpty(ListItem.Art(landscape))">$INFO[ListItem.Art(landscape)]</value>
		<value>$INFO[ListItem.Art(fanart)]</value>
	</variable>
	<variable name="Aeon_FavArtK">
		<value condition="!String.IsEmpty(ListItem.Art(poster))">$INFO[ListItem.Art(poster)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(thumb))">$INFO[ListItem.Art(thumb)]</value>
		<value>$INFO[ListItem.Icon]</value>
	</variable>
	<include name="FG_TabTex_fg"><texturenofocus border="20" colordiffuse="fg_sel">fg/r20.png</texturenofocus><texturefocus border="20" colordiffuse="fg_sel">fg/r20.png</texturefocus></include>
	<include name="FG_TabTex_old"><texturenofocus colordiffuse="73000000">common/white.png</texturenofocus><texturefocus colordiffuse="73000000">common/white.png</texturefocus></include>
	<include name="FG_TabTex">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_TabTex_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">FG_TabTex_old</include>
	</include>
	<include name="Aeon_H_FavBg">
		<control type="group">
			<visible>$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny]</visible>
			<include>Anim_FadeVisible</include>
			<control type="image"><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><texture colordiffuse="c8ffffff">common/aeon_bg_favourites.jpg</texture></control>
			<control type="group">
				<visible>Control.HasFocus(9309) + !String.IsEmpty(Container(9309).ListItem.Art(fanart))</visible>
				<include>Anim_FadeVisible</include>
				<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="ff0a0a0a">common/white.png</texture></control>
				<control type="image"><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>400</fadetime><texture background="true">$INFO[Container(9309).ListItem.Art(fanart)]</texture></control>
				<control type="image"><width>1100</width><height>1080</height><texture colordiffuse="e6000000">common/scrim_left.png</texture></control>
				<control type="image"><left>0</left><top>420</top><width>1920</width><height>660</height><texture colordiffuse="f0000000">aeon/osd_scrim_bottom.png</texture></control>
			</control>
		</control>
	</include>
	<include name="Aeon_H_Favourites">
		<!-- header and the spotlight of the card in focus -->
		<control type="group">
			<visible>$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny] + [Control.HasFocus(9000) | Control.HasFocus(9309)]</visible>
			<include>Anim_FadeVisible</include>
			<control type="label"><left>60</left><top>40</top><width>1300</width><height>44</height><aligny>center</aligny><font>hm_ui_26</font><textcolor>ccffffff</textcolor><label>[UPPERCASE]$LOCALIZE[1036] [B]$VAR[Aeon_FavKindName][/B][/UPPERCASE]</label></control>
			<control type="group">
				<include>Aeon_LowBand</include>
				<visible>Control.HasFocus(9309)</visible>
				<control type="image"><left>120</left><top>116</top><width>640</width><height>150</height><aspectratio align="left" aligny="bottom">keep</aspectratio><texture background="true">$INFO[Container(9309).ListItem.Art(clearlogo)]</texture><visible>!String.IsEmpty(Container(9309).ListItem.Art(clearlogo)) + !Skin.HasSetting(aeon.nologos)</visible></control>
				<control type="label"><left>120</left><top>186</top><width>1240</width><height>80</height><aligny>center</aligny><font>hm_aeon_title_66</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$INFO[Container(9309).ListItem.Label][/UPPERCASE]</label><visible>String.IsEmpty(Container(9309).ListItem.Art(clearlogo)) | Skin.HasSetting(aeon.nologos)</visible></control>
				<control type="label"><left>120</left><top>284</top><width>1300</width><height>34</height><aligny>center</aligny><font>hm_ui_24_bold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$LOCALIZE[1036] · $INFO[Container(9309).ListItem.Label2]$INFO[Container(9309).ListItem.Year,  ·  ,]$INFO[Container(9309).ListItem.Genre,  ·  ,][/UPPERCASE]</label></control>
				<control type="textbox"><left>120</left><top>336</top><width>820</width><height>150</height><font>hm_body_24</font><textcolor>ccffffff</textcolor><label>$INFO[Container(9309).ListItem.Plot]</label></control>
			</control>
		</control>
		<!-- the groups and the row of cards under the menu -->
		<control type="group">
			<include>Aeon_LowSubSlide</include>
			<visible>$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny] + [Control.HasFocus(9000) | Control.HasFocus(9309)]</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<control type="group">
				<include>Aeon_LowSubZoom</include>
{TABS}
				<control type="list" id="9309">
					<left>660</left><top>790</top><width>1260</width><height>290</height>
					<orientation>horizontal</orientation>
					<scrolltime tween="cubic" easing="out">220</scrolltime>
{UPDOWN}
					<onback>9000</onback>
					<itemlayout width="312" height="280">
						<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture><visible>{F}</visible></control>
						<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><texture colordiffuse="73000000">common/white.png</texture><visible>!{F}</visible></control>
{CARD}
						<control type="label"><left>16</left><top>182</top><width>280</width><height>24</height><font>hm_cap_16</font><textcolor>99ffffff</textcolor><label>[UPPERCASE]$INFO[ListItem.Label2][/UPPERCASE]</label></control>
						<control type="label"><left>16</left><top>206</top><width>280</width><height>32</height><font>hm_ui_24_semibold</font><textcolor>e6ffffff</textcolor><label>$INFO[ListItem.Label]</label></control>
					</itemlayout>
					<focusedlayout width="312" height="280">
						<control type="image"><left>12</left><top>10</top><width>288</width><height>166</height><texture colordiffuse="aeon_white">common/white.png</texture><visible>Control.HasFocus(9309) + !{F}</visible></control>
						<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture><visible>{F}</visible></control>
						<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><texture colordiffuse="ff1a1a1a">common/white.png</texture><visible>!{F}</visible></control>
{CARD}
						<control type="image"><left>16</left><top>14</top><width>280</width><height>158</height><texture border="16" colordiffuse="ffffffff">fg/ri16.png</texture><visible>Control.HasFocus(9309) + {F}</visible></control>
						<control type="label"><left>16</left><top>182</top><width>280</width><height>24</height><font>hm_cap_16</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$INFO[ListItem.Label2][/UPPERCASE]</label></control>
						<control type="label"><left>16</left><top>206</top><width>280</width><height>32</height><font>hm_ui_24_semibold</font><textcolor>ffffffff</textcolor><scroll>true</scroll><label>$INFO[ListItem.Label]</label></control>
					</focusedlayout>
					<content target="videos">$VAR[Aeon_FavPath]</content>
				</control>
			</control>
		</control>
	</include>
'''


def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (path, a[:100], s.count(a))
        s = s.replace(a, b)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


if __name__ == '__main__':
    tabs = '\n'.join(TAB.format(top=790 + 46 * n, lab=lab, sel=sel(k)) for n, (k, lab) in enumerate(KINDS))
    updown = '\n'.join('\t\t\t\t\t' + x for x in (
        '<onup condition="%s">SetFocus(9000)</onup>' % sel('all'),
        '<onup condition="%s">SetProperty(aeon.favkind,all,home)</onup>' % sel('video'),
        '<onup condition="%s">SetProperty(aeon.favkind,video,home)</onup>' % sel('music'),
        '<onup condition="%s">SetProperty(aeon.favkind,music,home)</onup>' % sel('addons'),
        '<ondown condition="%s">SetProperty(aeon.favkind,video,home)</ondown>' % sel('all'),
        '<ondown condition="%s">SetProperty(aeon.favkind,music,home)</ondown>' % sel('video'),
        '<ondown condition="%s">SetProperty(aeon.favkind,addons,home)</ondown>' % sel('music')))
    body = BODY.replace('{TABS}', tabs).replace('{UPDOWN}', updown).replace('{CARD}', CARD).replace('{SD}', SD).replace('{F}', F)
    s = io.open('Includes_Fused.xml', encoding='utf-8').read()
    if 'Aeon_H_Favourites' not in s:
        i = s.rindex('</includes>')
        io.open('Includes_Fused.xml', 'w', encoding='utf-8', newline='').write(s[:i] + body + s[i:])
    patch('Includes_Aeon_Home.xml', [
        ('''				<texture colordiffuse="c8ffffff">common/aeon_bg_system.jpg</texture>
			</control>
		</control>
''', '''				<texture colordiffuse="c8ffffff">common/aeon_bg_system.jpg</texture>
			</control>
		</control>
		<include>Aeon_H_FavBg</include>
'''),
        ('!$EXP[Aeon_H_SearchSec] + !$EXP[Aeon_H_LiveTV] + !$EXP[Aeon_H_WeatherSec]]]',
         '!$EXP[Aeon_H_SearchSec] + !$EXP[Aeon_H_LiveTV] + !$EXP[Aeon_H_WeatherSec] + !$EXP[Aeon_H_FavSec]]]'),
        ('\t\t<include>Aeon_H_PlannerWeek</include>\n', '\t\t<include>Aeon_H_PlannerWeek</include>\n\t\t<include>Aeon_H_Favourites</include>\n'),
        ('\t\t\t<ondown condition="$EXP[Aeon_H_PowerSec] + !$EXP[Aeon_H_SpotAny]">SetFocus(93081)</ondown>\n',
         '\t\t\t<ondown condition="$EXP[Aeon_H_PowerSec] + !$EXP[Aeon_H_SpotAny]">SetFocus(93081)</ondown>\n'
         '\t\t\t<ondown condition="$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny] + !Integer.IsGreater(Container(9309).NumItems,0)">SetProperty(aeon.favkind,all,home)</ondown>\n'
         '\t\t\t<ondown condition="$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny]">SetFocus(9309)</ondown>\n'),
        ('+ !$EXP[Aeon_H_SearchRecent] + !$EXP[Aeon_H_PowerSec]">$VAR[Aeon_H_DownToRows]</ondown>',
         '+ !$EXP[Aeon_H_SearchRecent] + !$EXP[Aeon_H_PowerSec] + !$EXP[Aeon_H_FavSec]">$VAR[Aeon_H_DownToRows]</ondown>'),
    ])
    print('favourites ok')
