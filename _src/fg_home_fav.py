"""0.42.0 Fused Glass Home > Favourites (mockup boards Favourites and FavouritesOK): writes FG_H_Favourites and FG_H_FavBg
into 1080i/Includes_Fused.xml (between FG_FAV markers) and makes Aeon_H_Favourites / Aeon_H_FavBg load-time variants
(classic = *_Classic). Run from the skin folder.

Kodi lists draw every item the same size, so the row is a grouplist of slots (9370) fed from the off-screen list 9309
(script.aeon.helper ?info=favourites, 0.3.73): slot k shows item k as a wide (show), poster (film / set) or square tile
(album, channel, add-on, folder ...); a hidden slot takes no room, so the tiles flow. The focused slot is
Window(Home).Property(aeon.favslot); the spotlight above reads that item. OK on a show, film, album or artist moves to
the spotlight's buttons (9360: Resume / Play, Play from the start, All episodes, info); Back returns to the tile. Other
favourites open at once. Filter pills (9361): All · n, Video, Music, Channels, Add-ons."""
import io
import re

FUSED = '1080i/Includes_Fused.xml'
HOME = '1080i/Includes_Aeon_Home.xml'
A = '$ADDON[skin.aeon.fuse %d]'
N = 20                                       # slots
SHAPES = (('wide', 268), ('poster', 100), ('square', 150))   # 0.45.1: a size smaller
SLOT = 'Window(Home).Property(aeon.favslot)'
KIND = 'Window(Home).Property(aeon.favkind)'
ITEM = 'Container(9309).ListItemAbsolute(%d)'
ADD, R_PILL, R_FIRST, R_BACK, R_LAST = 93790, 93791, 93792, 93793, 93794
PILLS = (('all', 93611, '$LOCALIZE[593]'), ('video', 93612, '$LOCALIZE[157]'), ('music', 93613, '$LOCALIZE[2]'),
         ('channels', 93614, '$LOCALIZE[19019]'), ('addons', 93615, '$LOCALIZE[24001]'))


def bid(k, v):
    return 93700 + k * 3 + v


def exists(k):
    return 'Integer.IsGreater(Container(9309).NumItems,%d)' % k


def shape_is(k, v):
    prop = '%s.Property(aeon.favshape)' % (ITEM % k)
    if SHAPES[v][0] == 'square':
        return '%s + !String.IsEqual(%s,wide) + !String.IsEqual(%s,poster)' % (exists(k), prop, prop)
    return '%s + String.IsEqual(%s,%s)' % (exists(k), prop, SHAPES[v][0])


def slot_is(k):
    return ('[String.IsEmpty(%s) | String.IsEqual(%s,0)]' % (SLOT, SLOT)) if k == 0 else 'String.IsEqual(%s,%d)' % (SLOT, k)


def kind_is(kind):
    return ('[String.IsEmpty(%s) | String.IsEqual(%s,all)]' % (KIND, KIND)) if kind == 'all' else 'String.IsEqual(%s,%s)' % (KIND, kind)


def go(tag, k):
    """Conditional moves to the visible tile of slot k (the Add tile when there is no slot k)."""
    if k >= N:
        return '<%s>SetFocus(%d)</%s>' % (tag, ADD, tag)
    out = ''.join('<%s condition="%s">SetFocus(%d)</%s>' % (tag, shape_is(k, v), bid(k, v), tag) for v in range(3))
    return out + '<%s condition="!%s">SetFocus(%d)</%s>' % (tag, exists(k), ADD, tag)


def var(name, field):
    """A variable with the spotlight's item field (slot 0 when nothing is chosen)."""
    rows = ''.join('\t\t<value condition="%s">$INFO[%s.%s]</value>\n' % (slot_is(k), ITEM % k, field) for k in range(N))
    return '\t<variable name="%s">\n%s\t</variable>\n' % (name, rows)


def has(name, field, extra=''):
    """An expression: the spotlight's item has this field (not empty)."""
    terms = ' | '.join('[%s + !String.IsEmpty(%s.%s)%s]' % (slot_is(k), ITEM % k, field, extra % k if extra else '') for k in range(N))
    return '\t<expression name="%s">%s</expression>\n' % (name, terms)


VARS = (var('FG_FavLabel', 'Label') + var('FG_FavKindWord', 'Label2') + var('FG_FavStudio', 'Studio, · ,') +
        var('FG_FavLogo', 'Art(clearlogo)') + var('FG_FavFanart', 'Art(fanart)') + var('FG_FavPlot', 'Plot') +
        var('FG_FavEp', 'Property(aeon.fav.ep)') + var('FG_FavLeft', 'Property(aeon.fav.left)') +
        var('FG_FavNext', 'Property(aeon.fav.next)') + var('FG_FavEpThumb', 'Property(aeon.fav.epthumb)') + has('FG_FavHasEpThumb', 'Property(aeon.fav.epthumb)') +
        var('FG_FavL1', 'Property(aeon.fav.l1)') + var('FG_FavL2', 'Property(aeon.fav.l2)') + var('FG_FavL3', 'Property(aeon.fav.l3)') +
        has('FG_FavHasLogo', 'Art(clearlogo)') + has('FG_FavHasFanart', 'Art(fanart)') + has('FG_FavHasEp', 'Property(aeon.fav.ep)') +
        has('FG_FavStarted', 'Property(aeon.fav.started)') + has('FG_FavHasL2', 'Property(aeon.fav.l2)') +
        has('FG_FavHasL3', 'Property(aeon.fav.l3)') + has('FG_FavHasInfo', 'Property(aeon.fav.info)') +
        has('FG_FavIsSpot', 'Property(aeon.fav.mode)') + has('FG_FavHasItem', 'Label'))

PILL_VARS = ''.join('''	<variable name="FG_FavPillBg%(id)d">
		<value condition="%(sel)s">fg_sel</value>
		<value>00ffffff</value>
	</variable>
	<variable name="FG_FavPillInk%(id)d">
		<value condition="%(sel)s">ffffffff</value>
		<value>99ffffff</value>
	</variable>
''' % {'id': i, 'sel': kind_is(kind)} for kind, i, label in PILLS)
PILL_VARS += '''	<variable name="FG_FavPath">
		<value condition="String.IsEqual(%(k)s,video)">plugin://script.aeon.helper/?info=favourites&amp;kind=video&amp;chan=0$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
		<value condition="String.IsEqual(%(k)s,music)">plugin://script.aeon.helper/?info=favourites&amp;kind=music&amp;chan=0$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
		<value condition="String.IsEqual(%(k)s,channels)">plugin://script.aeon.helper/?info=favourites&amp;kind=channels$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
		<value condition="String.IsEqual(%(k)s,addons)">plugin://script.aeon.helper/?info=favourites&amp;kind=addons$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
		<value>plugin://script.aeon.helper/?info=favourites&amp;kind=all$INFO[Window(Home).Property(aeon.fav.stamp),&amp;r=,]</value>
	</variable>
''' % {'k': KIND}


def pill(kind, ident, label):
    count = '$INFO[Container(9309).NumItems, · ,]'
    return ('\t\t\t\t\t<control type="button" id="%d"><width min="60" max="600">auto</width><height>44</height>'
            '<label>%s$VAR[FG_FavPillCount%d]</label><font>hm_ui_22_semibold</font><align>center</align><aligny>center</aligny>'
            '<textoffsetx>22</textoffsetx><textcolor>$VAR[FG_FavPillInk%d]</textcolor><focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>'
            '<texturenofocus border="22" colordiffuse="$VAR[FG_FavPillBg%d]">fg/r22.png</texturenofocus>'
            '<texturefocus border="22" colordiffuse="$VAR[FG_SysTabFocus]">fg/r22.png</texturefocus>'
            '<onfocus>SetProperty(aeon.favkind,%s,home)</onfocus><onfocus>ClearProperty(aeon.favslot,home)</onfocus>'
            '<ondown>SetFocus(%d)</ondown><onup>9000</onup><onback>9000</onback></control>\n'
            % (ident, label, ident, ident, ident, kind, R_FIRST))


PILL_COUNT = ''.join('''	<variable name="FG_FavPillCount%d">
		<value condition="%s">$INFO[Container(9309).NumItems, · ,]</value>
	</variable>
''' % (i, kind_is(kind)) for kind, i, label in PILLS)


def slot(k, v):
    name, w = SHAPES[v]
    me = bid(k, v)
    it = ITEM % k
    nav = go('onright', k + 1)
    nav += go('onleft', k - 1) if k > 0 else '<onleft>noop</onleft>'
    click = ('<onclick condition="String.IsEqual(%s.Property(aeon.fav.mode),spot)">SetFocus(93601)</onclick>'
             '<onclick condition="!String.IsEqual(%s.Property(aeon.fav.mode),spot)">RunPlugin($INFO[%s.FolderPath])</onclick>' % (it, it, it))
    lw = w + 20
    return '''					<control type="group">
						<top>14</top><width>%(gw)d</width><height>226</height>
						<visible>%(vis)s</visible>
						<control type="group">
							<animation effect="zoom" start="100" end="104" center="auto" time="160" tween="cubic" easing="out" condition="Control.HasFocus(%(id)d)">Conditional</animation>
							<control type="image"><left>0</left><top>0</top><width>%(w)d</width><height>150</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture></control>
							<control type="image"><left>0</left><top>0</top><width>%(w)d</width><height>150</height><aspectratio scalediffuse="false">scale</aspectratio><texture background="true" diffuse="fg/m%(w)dx150.png">$INFO[%(it)s.Property(aeon.favart)]</texture><visible>!String.IsEmpty(%(it)s.Property(aeon.favart)) + !String.IsEqual(%(it)s.Property(aeon.favwhat),channel)</visible></control>
							<control type="image"><left>18</left><top>14</top><width>%(logow)d</width><height>84</height><aspectratio>keep</aspectratio><texture background="true">$INFO[%(it)s.Property(aeon.favart)]</texture><visible>!String.IsEmpty(%(it)s.Property(aeon.favart)) + String.IsEqual(%(it)s.Property(aeon.favwhat),channel)</visible></control>
							<control type="image"><left>%(gx)d</left><top>%(gy)d</top><width>56</width><height>56</height><aspectratio>keep</aspectratio><texture colordiffuse="e6ffffff">$INFO[%(it)s.Property(aeon.favglyph)]</texture><visible>String.IsEmpty(%(it)s.Property(aeon.favart))</visible></control>
							<control type="label"><left>8</left><top>108</top><width>%(iw)d</width><height>32</height><align>center</align><aligny>center</aligny><font>hm_small_20_bold</font><textcolor>ffffffff</textcolor><label>$INFO[%(it)s.Property(aeon.favnow),$LOCALIZE[19030]: ,]</label></control>
							<control type="image"><left>0</left><top>0</top><width>%(w)d</width><height>150</height><texture border="16" colordiffuse="fg_edge">fg/e16.png</texture></control>
							<control type="image"><left>-3</left><top>-3</top><width>%(rw)d</width><height>156</height><texture border="19" colordiffuse="fg_mark">fg/ring16.png</texture><visible>Control.HasFocus(%(id)d)</visible></control>
							<control type="image"><left>-3</left><top>-3</top><width>%(rw)d</width><height>156</height><texture border="19" colordiffuse="fg_mark">fg/ring16.png</texture><visible>ControlGroup(9360).HasFocus() + %(here)s</visible></control>
						</control>
						<control type="button" id="%(id)d">
							<left>0</left><top>0</top><width>%(w)d</width><height>150</height><label></label><texturefocus /><texturenofocus />
							<onfocus>SetProperty(aeon.favslot,%(k)d,home)</onfocus>
							%(click)s
							%(nav)s
							<onup>SetFocus(%(rpill)d)</onup><ondown>noop</ondown><onback>9000</onback>
						</control>
						<control type="label"><left>0</left><top>160</top><width>%(lw)d</width><height>24</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>99ffffff</textcolor><label>[UPPERCASE]$INFO[%(it)s.Label2]$INFO[%(it)s.Property(aeon.favby), · ,][/UPPERCASE]</label></control>
						<control type="label"><left>0</left><top>182</top><width>%(lw)d</width><height>32</height><aligny>center</aligny><font>hm_ui_24_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[%(it)s.Label]</label></control>
					</control>
''' % {'gw': w + 24, 'vis': shape_is(k, v), 'id': me, 'w': w, 'it': it, 'gx': w // 2 - 28, 'gy': 47, 'iw': w - 16, 'logow': w - 36, 'rw': w + 6,
       'k': k, 'here': slot_is(k), 'click': click, 'nav': nav, 'rpill': R_PILL, 'lw': lw}


def router(ident, actions):
    return ('\t\t\t\t<control type="button" id="%d"><left>3000</left><top>0</top><width>2</width><height>2</height><label></label>'
            '<texturefocus /><texturenofocus />%s</control>\n' % (ident, actions))


ROUTERS = (router(R_PILL, ''.join('<onfocus condition="%s">SetFocus(%d)</onfocus>' % (kind_is(kind), i) for kind, i, l in PILLS)) +
           router(R_FIRST, go('onfocus', 0)) +
           router(R_BACK, ''.join('<onfocus condition="%s + %s">SetFocus(%d)</onfocus>' % (slot_is(k), shape_is(k, v), bid(k, v))
                                  for k in range(N) for v in range(3)) + '<onfocus condition="!$EXP[FG_FavHasItem]">SetFocus(%d)</onfocus>' % R_FIRST) +
           router(R_LAST, ''.join('<onfocus condition="%s + %s">SetFocus(%d)</onfocus>' % (shape_is(k, v), '!' + exists(k + 1), bid(k, v))
                                  for k in range(N) for v in range(3)) + '<onfocus condition="!%s">SetFocus(%d)</onfocus>' % (exists(0), ADD)))


def spot_button(ident, label, has_expr, which):
    acts = ''.join('<onclick condition="%s">$INFO[%s.Property(aeon.fav.a%d)]</onclick>' % (slot_is(k), ITEM % k, which) for k in range(N))
    vis = '<visible>$EXP[%s]</visible>' % has_expr if has_expr else ''
    return ('\t\t\t\t\t<control type="button" id="%d"><width min="80" max="700">auto</width><height>56</height><label>%s</label>'
            '<font>hm_ui_24_semibold</font><align>center</align><aligny>center</aligny><textoffsetx>28</textoffsetx>'
            '<textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor><include>FG_PillBtnTex</include>%s%s'
            '<onup>noop</onup><ondown>SetFocus(%d)</ondown><onback>SetFocus(%d)</onback></control>\n'
            % (ident, label, acts, vis, R_BACK, R_BACK))


INFO_BTN = ('\t\t\t\t\t<control type="button" id="93604"><width>56</width><height>56</height><label></label>'
            '<texturenofocus>fg/btninfo_n.png</texturenofocus><texturefocus>fg/btninfo_f.png</texturefocus>%s'
            '<visible>$EXP[FG_FavHasInfo] + ControlGroup(9360).HasFocus()</visible><onup>noop</onup><ondown>SetFocus(%d)</ondown><onback>SetFocus(%d)</onback></control>\n'
            % (''.join('<onclick condition="%s">$INFO[%s.Property(aeon.fav.info)]</onclick>' % (slot_is(k), ITEM % k) for k in range(N)),
               R_BACK, R_BACK))

PERCENT = ''.join('\t\t\t\t\t<control type="progress"><left>0</left><top>0</top><width>560</width><height>6</height>'
                  '<texturebg border="3,0,3,0" colordiffuse="33ffffff">fg/pillh.png</texturebg><midtexture border="3,0,3,0" colordiffuse="fg_mark">fg/pillh.png</midtexture>'
                  '<info>%s.PercentPlayed</info><visible>%s</visible></control>\n' % (ITEM % k, slot_is(k)) for k in range(N))

ON_PAGE = '[ControlGroup(9370).HasFocus() | ControlGroup(9360).HasFocus() | ControlGroup(9361).HasFocus() | ControlGroup(9371).HasFocus()]'
ROW_SHOWN = '[Control.HasFocus(9000) | %s]' % ON_PAGE

BODY = '''	<!-- FG_FAV:begin (written by _src/fg_home_fav.py) ========================== Home > Favourites, Fused Glass (0.42.0)
	     Spotlight of the chosen favourite (Window(Home).Property(aeon.favslot)) over its fanart, filter pills (9361), a
	     row of wide / poster / square tiles (grouplist 9370, slots fed from the off-screen list 9309) and an Add tile.
	     OK on a show, film, album or artist moves to the spotlight's buttons (9360), Back to the tile; other favourites
	     open at once. Hidden routing buttons 93791-93794 pick the right tile / pill. -->
%(vars)s%(pillvars)s%(pillcount)s	<include name="FG_H_FavBg">
		<control type="group">
			<visible>$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny]</visible>
			<include>Anim_FadeVisible</include>
			<control type="image"><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><texture colordiffuse="c8ffffff">common/aeon_bg_favourites.jpg</texture></control>
			<control type="group">
				<visible>%(onpage)s + $EXP[FG_FavHasFanart]</visible>
				<include>Anim_FadeVisible</include>
				<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="ff0a0a0a">common/white.png</texture></control>
				<control type="image"><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>400</fadetime><texture background="true">$VAR[FG_FavFanart]</texture></control>
				<control type="image"><width>1200</width><height>1080</height><texture colordiffuse="e6000000">common/scrim_left.png</texture></control>
				<control type="image"><left>0</left><top>420</top><width>1920</width><height>660</height><texture colordiffuse="f0000000">aeon/osd_scrim_bottom.png</texture></control>
			</control>
		</control>
	</include>
	<include name="FG_H_Favourites">
		<!-- the spotlight -->
		<control type="group">
			<include>Aeon_LowBand</include>
			<visible>$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny] + %(onpage)s + $EXP[FG_FavHasItem]</visible>
			<include>Anim_FadeVisible</include>
			<control type="image"><left>120</left><top>112</top><width>20</width><height>20</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">common/aeon_mi_heart.png</texture></control>
			<control type="label"><left>152</left><top>104</top><width>1200</width><height>36</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>e6ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[1036] · $VAR[FG_FavKindWord]$VAR[FG_FavStudio][/UPPERCASE]</label></control>
			<control type="image"><left>120</left><top>146</top><width>560</width><height>110</height><aspectratio align="left" aligny="bottom">keep</aspectratio><fadetime>200</fadetime><texture background="true">$VAR[FG_FavLogo]</texture><visible>$EXP[FG_FavHasLogo] + !Skin.HasSetting(aeon.nologos)</visible></control>
			<control type="label"><left>120</left><top>160</top><width>1240</width><height>90</height><aligny>center</aligny><font>hm_aeon_title_66</font><textcolor>ffffffff</textcolor><label>$VAR[FG_FavLabel]</label><visible>!$EXP[FG_FavHasLogo] | Skin.HasSetting(aeon.nologos)</visible></control>
			<control type="group">
				<visible>$EXP[FG_FavHasEpThumb]</visible>
				<control type="image"><left>120</left><top>266</top><width>232</width><height>130</height><texture border="12" colordiffuse="$VAR[FG_Frost]">fg/r12.png</texture></control>
				<control type="image"><left>120</left><top>266</top><width>232</width><height>130</height><aspectratio scalediffuse="false">scale</aspectratio><fadetime>200</fadetime><texture background="true" diffuse="fg/m232x130.png">$VAR[FG_FavEpThumb]</texture></control>
				<control type="image"><left>120</left><top>266</top><width>232</width><height>130</height><texture border="12" colordiffuse="$VAR[FG_Edge]">fg/e12.png</texture></control>
			</control>
			<control type="group">
				<visible>$EXP[FG_FavHasEp]</visible>
				<control type="label"><left>120</left><top>406</top><width>560</width><height>40</height><aligny>center</aligny><font>hm_ui_24_semibold</font><textcolor>ffffffff</textcolor><label>$VAR[FG_FavEp]</label></control>
				<control type="label"><left>380</left><top>406</top><width>300</width><height>40</height><align>right</align><aligny>center</aligny><font>hm_ui_24_semibold</font><textcolor>ffffffff</textcolor><label>$VAR[FG_FavLeft]</label><visible>$EXP[FG_FavStarted]</visible></control>
				<control type="group">
					<left>120</left><top>450</top>
					<visible>$EXP[FG_FavStarted]</visible>
%(percent)s				</control>
				<control type="label"><left>120</left><top>462</top><width>1100</width><height>34</height><aligny>center</aligny><font>hm_small_20</font><textcolor>c8ffffff</textcolor><label>$VAR[FG_FavNext]</label></control>
			</control>
			<control type="textbox"><left>120</left><top>380</top><width>820</width><height>96</height><font>hm_body_24</font><textcolor>ccffffff</textcolor><label>$VAR[FG_FavPlot]</label><visible>!$EXP[FG_FavHasEp]</visible></control>
			<control type="grouplist" id="9360">
				<left>112</left><top>514</top><width>1400</width><height>60</height>
				<orientation>horizontal</orientation><itemgap>12</itemgap>
				<visible>$EXP[FG_FavIsSpot]</visible>
%(buttons)s			</control>
			<control type="grouplist">
				<left>120</left><top>590</top><width>800</width><height>30</height>
				<orientation>horizontal</orientation><itemgap>10</itemgap><usecontrolcoords>true</usecontrolcoords>
				<visible>ControlGroup(9360).HasFocus()</visible>
				<control type="button"><width min="40" max="300">auto</width><height>30</height><label>[UPPERCASE]%(back)s[/UPPERCASE]</label><font>hm_cap_14</font><textoffsetx>10</textoffsetx><align>center</align><aligny>center</aligny><textcolor>b3ffffff</textcolor><texturenofocus border="8" colordiffuse="66ffffff">fg/e8.png</texturenofocus><texturefocus border="8" colordiffuse="66ffffff">fg/e8.png</texturefocus></control>
				<control type="label"><width>auto</width><height>30</height><aligny>center</aligny><font>hm_small_20</font><textcolor>b3ffffff</textcolor><label>%(totile)s</label></control>
			</control>
		</control>
		<!-- the pills, the row of tiles and the off-screen data list -->
		<control type="group">
			<include>Aeon_LowSubSlide</include>
			<visible>$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny] + %(rowshown)s</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<control type="group">
				<include>Aeon_LowSubZoom</include>
				<control type="grouplist" id="9361">
					<left>112</left><top>778</top><width>1400</width><height>44</height>
					<orientation>horizontal</orientation><itemgap>6</itemgap>
					<onup>9000</onup>
%(pills)s				</control>
				<control type="grouplist" id="9370">
					<left>106</left><top>824</top><width>1714</width><height>240</height>
					<orientation>horizontal</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
					<control type="group"><width>14</width><height>10</height></control>
					<scrolltime tween="cubic" easing="out">220</scrolltime>
%(slots)s					<control type="group">
						<top>14</top><width>174</width><height>226</height>
						<control type="image"><left>0</left><top>0</top><width>150</width><height>150</height><texture colordiffuse="73ffffff">fg/dash168.png</texture><visible>!Control.HasFocus(%(add)d)</visible></control>
						<control type="image"><left>0</left><top>0</top><width>150</width><height>150</height><texture colordiffuse="ffffffff">fg/dash168.png</texture><visible>Control.HasFocus(%(add)d)</visible></control>
						<control type="label"><left>0</left><top>47</top><width>150</width><height>56</height><align>center</align><aligny>center</aligny><font>hm_display_52</font><textcolor>ccffffff</textcolor><label>+</label></control>
						<control type="button" id="%(add)d">
							<left>0</left><top>0</top><width>150</width><height>150</height><label></label><texturefocus /><texturenofocus />
							<onclick>ActivateWindow(favouritesbrowser)</onclick>
							<onleft>SetFocus(%(rlast)d)</onleft><onright>noop</onright><onup>SetFocus(%(rpill)d)</onup><ondown>noop</ondown><onback>9000</onback>
						</control>
						<control type="label"><left>0</left><top>160</top><width>280</width><height>24</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>99ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[10106][/UPPERCASE]</label></control>
						<control type="label"><left>0</left><top>182</top><width>280</width><height>34</height><aligny>center</aligny><font>hm_ui_24_semibold</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[14076]</label></control>
					</control>
				</control>
				<control type="group" id="9371">
%(routers)s				</control>
				<control type="list" id="9309">
					<left>3000</left><top>0</top><width>10</width><height>10</height>
					<itemlayout width="10" height="10"/><focusedlayout width="10" height="10"/>
					<content target="videos">$VAR[FG_FavPath]</content>
				</control>
			</control>
		</control>
	</include>
	<!-- FG_FAV:end -->
''' % {'vars': VARS, 'pillvars': PILL_VARS, 'pillcount': PILL_COUNT, 'onpage': ON_PAGE, 'rowshown': ROW_SHOWN, 'percent': PERCENT,
       'buttons': spot_button(93601, '$VAR[FG_FavL1]', '', 1) + spot_button(93602, '$VAR[FG_FavL2]', 'FG_FavHasL2] + ControlGroup(9360).HasFocus() + $EXP[FG_FavHasL2', 2) +
                  spot_button(93603, '$VAR[FG_FavL3]', 'FG_FavHasL3', 3) + INFO_BTN,
       'back': A % 31245, 'totile': A % 32511,
       'pills': ''.join(pill(*p) for p in PILLS),
       'slots': ''.join(slot(k, v) for k in range(N) for v in range(3)),
       'add': ADD, 'rlast': R_LAST, 'rpill': R_PILL, 'routers': ROUTERS}

t = io.open(FUSED, encoding='utf-8').read()
t = re.sub(r'\t<!-- FG_FAV:begin.*?<!-- FG_FAV:end -->\n', '', t, flags=re.S)
for name in ('Aeon_H_Favourites', 'Aeon_H_FavBg'):
    if name + '_Classic' not in t:
        a = '\t<include name="%s">\n' % name
        assert t.count(a) == 1, name
        fg = 'FG_H_Favourites' if name == 'Aeon_H_Favourites' else 'FG_H_FavBg'
        t = t.replace(a, '\t<include name="%s">\n'
                         '\t\t<include condition="Skin.HasSetting(aeon.fglass)">%s</include>\n'
                         '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">%s_Classic</include>\n'
                         '\t</include>\n'
                         '\t<include name="%s_Classic">\n' % (name, fg, name, name))
t = t.replace('</includes>', BODY + '</includes>')
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)

h = io.open(HOME, encoding='utf-8').read()
old = '<ondown condition="$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny]">SetFocus(9309)</ondown>'
if old in h:
    h = h.replace(old, '<ondown condition="$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny] + !Skin.HasSetting(aeon.fglass)">SetFocus(9309)</ondown>'
                       '<ondown condition="$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny] + Skin.HasSetting(aeon.fglass)">SetFocus(%d)</ondown>' % R_FIRST)
    io.open(HOME, 'w', encoding='utf-8', newline='\n').write(h)
import xml.etree.ElementTree as ET
ET.parse(FUSED); ET.parse(HOME)
print('ok', len(BODY) // 1024, 'KB')
