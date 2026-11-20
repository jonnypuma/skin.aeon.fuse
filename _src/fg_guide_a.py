"""0.39.7 TV / Radio guide, Fused Glass: mockup A "Glass timeline" (skin.glass/mockups/epg-guide) with the chips of B.
One frosted r28 card (102..1818 x 244..1044):
  head section  the selected programme: channel logo, title, chips (Now, start - end, length, channel), plot line
  grid          epggrid 50 below a hairline: 7 channels of 82 px, 2.5 hours (30 blocks), ruler every 30 min
Cells are r12 (16 px inside the r28 card: 28 - 16), 6 px apart; each cell is a progress control (id 2: Kodi stretches
layout controls with ids 1-14 to the programme's width) whose background is the cell and whose fill darkens the part
of the programme that has been shown, so ended programmes are dim and airing ones dim up to now. Airing cells are a
shade lighter. Focus: the white tile with dark text. Now: a gold pin on the ruler (the grid's progress indicator
texture, transparent except its top right corner: fg/epgnow.png), nothing drawn over the programmes.
The channel column shows number and logo; the channel name is a chip of the head section. The ruler's first item
(the long date) is hidden. Other themes keep the guide as it was (Misc_EPGLayouts_old, the old geometry).
Run from the skin folder: python _src/fg_guide_a.py"""
import io
import os

from PIL import Image, ImageDraw

# ---- the now pin: 24 x 50; top 46 rows = the ruler row; only the top right 12 x 46 corner is drawn
S = 8
W, H = 24, 50
big = Image.new('L', (W * S, H * S), 0)
d = ImageDraw.Draw(big)
d.ellipse((13 * S, 31 * S, 23 * S, 41 * S), fill=255)            # dot r5, centred 18 / 36
d.rectangle((22 * S, 36 * S, 24 * S - 1, 46 * S - 1), fill=255)  # tick on the right edge down to the grid
pin = Image.new('RGBA', (W, H), (255, 255, 255, 0))
pin.putalpha(big.resize((W, H), Image.BOX))
pin.save(os.path.join('media', 'fg', 'epgnow.png'), optimize=True)
print('wrote fg/epgnow.png')

X = '1080i'


def rw(name, fn):
    p = os.path.join(X, name)
    s = io.open(p, encoding='utf-8').read()
    t = fn(s)
    assert t != s, name
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


CELL = 'border="12"'
NOWCOND = 'Integer.IsGreater(ListItem.Progress,0) + Integer.IsLess(ListItem.Progress,100)'

LAYOUTS_FG = '''	<!-- 0.39.7 Fused Glass guide (mockup A): ruler / channel / programme layouts, see _src/fg_guide_a.py -->
	<include name="Misc_EPGLayouts_fg">
		<rulerlayout height="46" width="297">
			<control type="image"><left>0</left><top>34</top><width>2</width><height>8</height><texture colordiffuse="38ffffff">common/white.png</texture><visible>String.Contains(ListItem.Label,:)</visible></control>
			<control type="label"><left>10</left><top>0</top><width>280</width><height>46</height><aligny>center</aligny><font>small_20_semibold</font><textcolor>9effffff</textcolor><label>$INFO[ListItem.Label]</label><visible>String.Contains(ListItem.Label,:)</visible></control>
		</rulerlayout>
		<channellayout height="82" width="200">
			<control type="label"><left>0</left><top>0</top><width>44</width><height>82</height><align>right</align><aligny>center</aligny><font>num_22</font><textcolor>8cffffff</textcolor><label>$INFO[ListItem.ChannelNumberLabel]</label></control>
			<control type="image"><left>60</left><top>16</top><width>124</width><height>50</height><aspectratio>keep</aspectratio><texture background="true" colordiffuse="d9ffffff">$INFO[ListItem.Icon]</texture></control>
		</channellayout>
		<focusedchannellayout height="82" width="200">
			<control type="image"><left>52</left><top>8</top><width>140</width><height>66</height><texture %(cell)s colordiffuse="29ffffff">fg/r12.png</texture><visible>Control.HasFocus(50)</visible></control>
			<control type="label"><left>0</left><top>0</top><width>44</width><height>82</height><align>right</align><aligny>center</aligny><font>num_22</font><textcolor>ffffffff</textcolor><label>$INFO[ListItem.ChannelNumberLabel]</label></control>
			<control type="image"><left>60</left><top>16</top><width>124</width><height>50</height><aspectratio>keep</aspectratio><texture background="true">$INFO[ListItem.Icon]</texture></control>
		</focusedchannellayout>
		<itemlayout height="82" width="40">
			<control type="progress" id="2"><left>3</left><top>8</top><width>34</width><height>66</height><reveal>true</reveal><texturebg %(cell)s colordiffuse="17ffffff">fg/r12.png</texturebg><midtexture %(cell)s colordiffuse="47000000">fg/r12.png</midtexture><info>ListItem.Progress</info></control>
			<control type="image" id="3"><left>3</left><top>8</top><width>34</width><height>66</height><texture %(cell)s colordiffuse="0fffffff">fg/r12.png</texture><visible>%(now)s</visible></control>
			<control type="label" id="1"><left>17</left><top>14</top><width>6</width><height>28</height><font>small_20_semibold</font><textcolor>ebffffff</textcolor><label>$INFO[ListItem.Label]</label><visible>!Integer.IsEqual(ListItem.Progress,100)</visible></control>
			<control type="label" id="4"><left>17</left><top>42</top><width>6</width><height>24</height><font>cap_20</font><textcolor>8cffffff</textcolor><label>$INFO[ListItem.StartTime]$INFO[ListItem.EndTime, – ,]</label><visible>!Integer.IsEqual(ListItem.Progress,100)</visible></control>
			<control type="label" id="5"><left>17</left><top>14</top><width>6</width><height>28</height><font>small_20_semibold</font><textcolor>73ffffff</textcolor><label>$INFO[ListItem.Label]</label><visible>Integer.IsEqual(ListItem.Progress,100)</visible></control>
			<control type="label" id="6"><left>17</left><top>42</top><width>6</width><height>24</height><font>cap_20</font><textcolor>52ffffff</textcolor><label>$INFO[ListItem.StartTime]$INFO[ListItem.EndTime, – ,]</label><visible>Integer.IsEqual(ListItem.Progress,100)</visible></control>
		</itemlayout>
		<focusedlayout height="82" width="40">
			<control type="image" id="2"><left>3</left><top>8</top><width>34</width><height>66</height><texture %(cell)s colordiffuse="ffffffff">fg/r12.png</texture><visible>Control.HasFocus(50)</visible></control>
			<control type="progress" id="3"><left>3</left><top>8</top><width>34</width><height>66</height><reveal>true</reveal><texturebg %(cell)s colordiffuse="2effffff">fg/r12.png</texturebg><midtexture %(cell)s colordiffuse="47000000">fg/r12.png</midtexture><info>ListItem.Progress</info><visible>!Control.HasFocus(50)</visible></control>
			<control type="label" id="1"><left>17</left><top>14</top><width>6</width><height>28</height><font>small_20_bold</font><textcolor>fg_ink</textcolor><label>$INFO[ListItem.Label]</label><visible>Control.HasFocus(50)</visible></control>
			<control type="label" id="4"><left>17</left><top>42</top><width>6</width><height>24</height><font>cap_20</font><textcolor>990f1115</textcolor><label>$INFO[ListItem.StartTime]$INFO[ListItem.EndTime, – ,]</label><visible>Control.HasFocus(50)</visible></control>
			<control type="label" id="5"><left>17</left><top>14</top><width>6</width><height>28</height><font>small_20_bold</font><textcolor>ffffffff</textcolor><label>$INFO[ListItem.Label]</label><visible>!Control.HasFocus(50)</visible></control>
			<control type="label" id="6"><left>17</left><top>42</top><width>6</width><height>24</height><font>cap_20</font><textcolor>a6ffffff</textcolor><label>$INFO[ListItem.StartTime]$INFO[ListItem.EndTime, – ,]</label><visible>!Control.HasFocus(50)</visible></control>
		</focusedlayout>
	</include>
	<include name="Misc_EPGLayouts">
		<include condition="Skin.HasSetting(aeon.fglass)">Misc_EPGLayouts_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">Misc_EPGLayouts_old</include>
	</include>
	<!-- the guide grid's place and the now marker: the card of mockup A in Fused Glass, the old full-width grid elsewhere -->
	<include name="FG_EpgGrid">
		<include condition="Skin.HasSetting(aeon.fglass)">FG_EpgGrid_fg</include>
		<include condition="!Skin.HasSetting(aeon.fglass)">FG_EpgGrid_old</include>
	</include>
	<include name="FG_EpgGrid_fg">
		<left>118</left><top>410</top><width>1684</width><height>620</height>
		<timeblocks>30</timeblocks><rulerunit>6</rulerunit>
		<progresstexture border="0,46,12,2" colordiffuse="fg_mark">fg/epgnow.png</progresstexture>
	</include>
	<include name="FG_EpgGrid_old">
		<left>page_margin</left><top>misc_pvr_top</top><width>page_width</width><height>639</height>
		<timeblocks>36</timeblocks><rulerunit>6</rulerunit>
		<progresstexture border="0,0,2,0" colordiffuse="2effffff">misc/epg_now.png</progresstexture>
	</include>
''' % {'cell': CELL, 'now': NOWCOND}


def misc(s):
    assert '<include name="Misc_EPGLayouts_fg">' not in s
    s = s.replace('\t<include name="Misc_EPGLayouts">', '\t<include name="Misc_EPGLayouts_old">', 1)
    a = s.index('\t<include name="Misc_EPGLayouts_old">')
    return s[:a] + LAYOUTS_FG + s[a:]


def chip(label, vis, gold=False):
    col = 'fg_mark' if gold else 'e6ffffff'
    fill = '38e8b04b' if gold else '1fffffff'
    return ('\t\t\t\t\t<control type="button"><width min="44" max="900">auto</width><height>36</height><label>%s</label>'
            '<font>small_20_semibold</font><textcolor>%s</textcolor><focusedcolor>%s</focusedcolor><disabledcolor>%s</disabledcolor>'
            '<align>center</align><aligny>center</aligny><textoffsetx>18</textoffsetx>'
            '<texturenofocus border="18" colordiffuse="%s">fg/r18.png</texturenofocus><texturefocus border="18" colordiffuse="%s">fg/r18.png</texturefocus>'
            '<visible>%s</visible></control>\n' % (label, col, col, col, fill, fill, vis))


C = 'Container(50).ListItem'
HEAD = '''		<!-- Fused Glass (0.39.7, mockup A): one card; its head section shows the selected programme, the grid below a hairline -->
		<control type="group">
			<visible>$EXP[Aeon_FGlass] + Control.IsVisible(50)</visible>
			<control type="image"><left>62</left><top>216</top><width>1796</width><height>880</height><texture border="68" colordiffuse="80000000">fg/sh28.png</texture></control>
			<control type="image"><left>102</left><top>244</top><width>1716</width><height>800</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture></control>
			<control type="image"><left>102</left><top>244</top><width>1716</width><height>800</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture></control>
			<control type="image"><left>103</left><top>404</top><width>1714</width><height>1</height><texture colordiffuse="1affffff">common/white.png</texture></control>
			<control type="group">
				<visible>Integer.IsGreater(Container(50).NumItems,0)</visible>
				<control type="image"><left>130</left><top>262</top><width>96</width><height>64</height><aspectratio>keep</aspectratio><texture background="true">$INFO[%(c)s.Icon]</texture></control>
				<control type="label"><left>250</left><top>258</top><width>1540</width><height>48</height><aligny>center</aligny><font>ui_30_semibold</font><textcolor>ffffffff</textcolor><label>$VAR[FG_EpgHeadTitle]$INFO[%(c)s.EpisodeName,  ·  ,]</label></control>
				<control type="grouplist">
					<left>250</left><top>314</top><width>1540</width><height>36</height>
					<orientation>horizontal</orientation><itemgap>10</itemgap><usecontrolcoords>true</usecontrolcoords>
%(chips)s				</control>
				<control type="label"><left>250</left><top>358</top><width>1540</width><height>32</height><aligny>center</aligny><font>small_20</font><textcolor>8cffffff</textcolor><label>$INFO[%(c)s.Plot]</label></control>
			</control>
		</control>
''' % {'c': C, 'chips': chip('$LOCALIZE[31324]', 'Integer.IsGreater(%s.Progress,0) + Integer.IsLess(%s.Progress,100)' % (C, C), gold=True)
       + chip('$INFO[%s.StartTime]$INFO[%s.EndTime, – ,]' % (C, C), '!String.IsEmpty(%s.StartTime)' % C)
       + chip('$INFO[%s.Duration(mins)] $ADDON[skin.aeon.fuse 32220]' % C, '!String.IsEmpty(%s.Duration(mins))' % C)
       + chip('$INFO[%s.ChannelNumberLabel,,  ·  ]$INFO[%s.ChannelName]' % (C, C), '!String.IsEmpty(%s.ChannelName)' % C)}


def guide(s):
    a = s.index('\t\t<!-- Fused Glass: a frosted card behind the ruler, the channels and the programmes (0.38.0) -->')
    b = s.index('\t\t<!-- ====== grid (focus group 9100', a)
    s = s[:a] + HEAD + s[b:]
    old = '''				<left>page_margin</left>
				<top>misc_pvr_top</top>
				<width>page_width</width>
				<height>639</height>
				<onup>9001</onup>
				<pagecontrol>60</pagecontrol>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<timeblocks>36</timeblocks>
				<rulerunit>6</rulerunit>
				<viewtype label="19069">list</viewtype>
				<progresstexture border="0,0,2,0" colordiffuse="2effffff">misc/epg_now.png</progresstexture>'''
    assert s.count(old) == 1
    s = s.replace(old, '''				<include>FG_EpgGrid</include>
				<onup>9001</onup>
				<pagecontrol>60</pagecontrol>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<viewtype label="19069">list</viewtype>''')
    old = '''		<include content="AG_Scrollbar">
			<param name="id" value="60"/>
			<param name="left" value="1828"/>
			<param name="top" value="295"/>
			<param name="height" value="594"/>'''
    assert s.count(old) == 1
    s = s.replace(old, '''		<include content="AG_Scrollbar" condition="Skin.HasSetting(aeon.fglass)">
			<param name="id" value="60"/>
			<param name="left" value="1804"/>
			<param name="top" value="464"/>
			<param name="height" value="560"/>
			<param name="onleft" value="50"/>
			<param name="onright" value="50"/>
		</include>
		<include content="AG_Scrollbar" condition="!Skin.HasSetting(aeon.fglass)">
			<param name="id" value="60"/>
			<param name="left" value="1828"/>
			<param name="top" value="295"/>
			<param name="height" value="594"/>''')
    old = '<visible>Control.IsVisible(50) + Integer.IsGreater(Container.NumItems,0)</visible>'
    assert s.count(old) == 1
    return s.replace(old, '<visible>Control.IsVisible(50) + Integer.IsGreater(Container.NumItems,0) + !$EXP[Aeon_FGlass]</visible>')


def fused(s):
    assert 'FG_EpgHeadTitle' not in s
    return s.replace('</includes>', '''	<!-- 0.39.7 guide head section: the selected programme's title -->
	<variable name="FG_EpgHeadTitle">
		<value condition="!String.IsEmpty(Container(50).ListItem.EpgEventTitle)">$INFO[Container(50).ListItem.EpgEventTitle]</value>
		<value condition="!String.IsEmpty(Container(50).ListItem.Title)">$INFO[Container(50).ListItem.Title]</value>
		<value>$INFO[Container(50).ListItem.Label]</value>
	</variable>
</includes>''')


rw('Includes_Misc.xml', misc)
rw('MyPVRGuide.xml', guide)
rw('Includes_Fused.xml', fused)
print('ok')
