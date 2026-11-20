"""0.56.37 Fused Glass style: the Add-ons window (and the media windows of Misc_MediaWindow: Favourites ...) in the
System screen's grid (the user, 2026-11-17: "Kodi ADD-ONS menu is still not in Fused Glass style"; "there is a dark
panel with rounded corners on the left ..., the buttons are not vertically aligned inside their cell").

- No side card: the detail panel / icon card on the left is hidden in the style.
- One centred grid 360-1560 like the System screen: the toolbar (sort, Hide foreign / incompatible, Check for
  updates, Settings) is the grid's first row, 70 high (181-250), its buttons fill the cell (text centred, capitals,
  the white bar on focus); then the list, rows of 100: the icon in the icon column (add-ons: 72 x 72, favourites:
  128 x 72, rounded), the divider at 810, the name in capitals and a second line (the add-on's summary, else label2),
  the version at the row's end; the focused row outlined with the bar on the divider; the counter above the grid.
- "Repositories checked" goes to the hint line, bottom left.
AG_SubNavButton gains param fgs: the two windows ask for the style's look, every other use keeps its pill.
Run from the skin folder after fgs_round3_05633. Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
MARK = '<!-- 0.56.37 fgs_addons -->'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def once(text, old, new, count=1):
    assert text.count(old) == count, (old[:100], text.count(old))
    return text.replace(old, new)


def rule(left, top, width, alpha='12'):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>1</height>'
            '<texture colordiffuse="%sffffff">common/white.png</texture></control>' % (left, top, width, alpha))


ROW = '''	<include name="FGS_AddonRow">
		<param name="focused">false</param>
		<param name="wide">false</param>
		<definition>
			%(rule)s
			<control type="image"><left>450</left><top>0</top><width>1</width><height>100</height><texture colordiffuse="1affffff">common/white.png</texture></control>
			<control type="group">
				<visible>$PARAM[focused] + Control.HasFocus(50)</visible>
				<include>FGS_RowAnim</include>
				%(ftop)s
				%(fbot)s
				<control type="image"><left>1199</left><top>0</top><width>1</width><height>100</height><texture colordiffuse="44ffffff">common/white.png</texture></control>
				<control type="image"><left>448</left><top>0</top><width>5</width><height>100</height><texture>common/white.png</texture></control>
			</control>
			<!-- the icon: add-ons square, favourites wide; dim unless in focus -->
			<control type="image"><left>322</left><top>14</top><width>72</width><height>72</height><aspectratio>keep</aspectratio><texture background="true" diffuse="fg/m72x72.png" colordiffuse="99ffffff">$INFO[ListItem.Icon]</texture><visible>!$PARAM[wide] + ![$PARAM[focused] + Control.HasFocus(50)]</visible></control>
			<control type="image"><left>322</left><top>14</top><width>72</width><height>72</height><aspectratio>keep</aspectratio><texture background="true" diffuse="fg/m72x72.png">$INFO[ListItem.Icon]</texture><visible>!$PARAM[wide] + $PARAM[focused] + Control.HasFocus(50)</visible><animation type="Focus" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="zoom" start="85" end="100" center="auto" time="220" tween="back" easing="out"/></animation></control>
			<control type="image"><left>286</left><top>14</top><width>128</width><height>72</height><aspectratio>keep</aspectratio><texture background="true" diffuse="fg/m128x72.png" colordiffuse="99ffffff">$INFO[ListItem.Icon]</texture><visible>$PARAM[wide] + ![$PARAM[focused] + Control.HasFocus(50)]</visible></control>
			<control type="image"><left>286</left><top>14</top><width>128</width><height>72</height><aspectratio>keep</aspectratio><texture background="true" diffuse="fg/m128x72.png">$INFO[ListItem.Icon]</texture><visible>$PARAM[wide] + $PARAM[focused] + Control.HasFocus(50)</visible><animation type="Focus" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="zoom" start="88" end="100" center="auto" time="220" tween="back" easing="out"/></animation></control>
			<!-- the name (capitals) with a second line: the summary, else label2; alone in the middle without one -->
			<control type="group">
				<visible>!String.IsEmpty(ListItem.AddonSummary) | !String.IsEmpty(ListItem.Label2)</visible>
				<control type="label"><left>486</left><top>16</top><width>560</width><height>38</height><aligny>center</aligny><font>uc_st_ui_24_semibold</font><textcolor>66ffffff</textcolor><selectedcolor>66ffffff</selectedcolor><label>$INFO[ListItem.Label]</label><visible>!$PARAM[focused] | !Control.HasFocus(50)</visible></control>
				<control type="label"><left>486</left><top>16</top><width>560</width><height>38</height><aligny>center</aligny><font>uc_st_ui_24_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>$INFO[ListItem.Label]</label><scroll>true</scroll><visible>$PARAM[focused] + Control.HasFocus(50)</visible></control>
				<control type="label"><left>486</left><top>54</top><width>660</width><height>30</height><aligny>center</aligny><font>st_small_20</font><textcolor>59ffffff</textcolor><selectedcolor>59ffffff</selectedcolor><label>$INFO[ListItem.AddonSummary]</label><visible>!String.IsEmpty(ListItem.AddonSummary)</visible></control>
				<control type="label"><left>486</left><top>54</top><width>660</width><height>30</height><aligny>center</aligny><font>st_small_20</font><textcolor>59ffffff</textcolor><selectedcolor>59ffffff</selectedcolor><label>$INFO[ListItem.Label2]</label><visible>String.IsEmpty(ListItem.AddonSummary)</visible></control>
			</control>
			<control type="group">
				<visible>String.IsEmpty(ListItem.AddonSummary) + String.IsEmpty(ListItem.Label2)</visible>
				<control type="label"><left>486</left><top>0</top><width>660</width><height>100</height><aligny>center</aligny><font>uc_st_ui_24_semibold</font><textcolor>66ffffff</textcolor><selectedcolor>66ffffff</selectedcolor><label>$INFO[ListItem.Label]</label><visible>!$PARAM[focused] | !Control.HasFocus(50)</visible></control>
				<control type="label"><left>486</left><top>0</top><width>660</width><height>100</height><aligny>center</aligny><font>uc_st_ui_24_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>$INFO[ListItem.Label]</label><scroll>true</scroll><visible>$PARAM[focused] + Control.HasFocus(50)</visible></control>
			</control>
			<control type="label"><left>1050</left><top>16</top><width>114</width><height>38</height><align>right</align><aligny>center</aligny><font>st_small_20</font><textcolor>59ffffff</textcolor><selectedcolor>59ffffff</selectedcolor><label>$INFO[ListItem.AddonVersion]</label></control>
		</definition>
	</include>
	<include name="FGS_View50">
		<param name="wide">false</param>
		<definition>
		%(gridtop)s
		%(toolbar)s
		<control type="image"><left>360</left><top>250</top><width>1200</width><height>1</height><texture colordiffuse="44ffffff">common/white.png</texture><visible>Control.HasFocus(50) + Integer.IsEqual(Container(50).Position,0)</visible></control>
		<control type="label"><left>1160</left><top>128</top><width>400</width><height>40</height><align>right</align><aligny>center</aligny><font>st_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[Container(50).CurrentItem]  /  $INFO[Container(50).NumItems]</label><visible>Integer.IsGreater(Container(50).NumItems,0)</visible></control>
		<control type="group">
			<visible>Control.IsVisible(50)</visible>
			<include>Anim_VisibleFade</include>
			<control type="list" id="50">
				<left>360</left>
				<top>251</top>
				<width>1200</width>
				<height>700</height>
				<onup>9000</onup>
				<ondown>noop</ondown>
				<onleft condition="Window.IsActive(addonbrowser) + $EXP[Aeon_FGlass] + Control.IsVisible(7700)">7700</onleft>
				<onleft>noop</onleft>
				<onright>60</onright>
				<pagecontrol>60</pagecontrol>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<viewtype label="535">list</viewtype>
				<itemlayout width="1200" height="100">
					<include content="FGS_AddonRow"><param name="wide" value="$PARAM[wide]"/></include>
				</itemlayout>
				<focusedlayout width="1200" height="100">
					<include content="FGS_AddonRow"><param name="focused" value="true"/><param name="wide" value="$PARAM[wide]"/></include>
				</focusedlayout>
			</control>
			<control type="scrollbar" id="60">
				<left>1556</left>
				<top>251</top>
				<width>4</width>
				<height>700</height>
				<texturesliderbackground border="2" colordiffuse="1affffff">aeon/track_8.png</texturesliderbackground>
				<texturesliderbar border="2" colordiffuse="80ffffff">aeon/track_8.png</texturesliderbar>
				<texturesliderbarfocus border="2" colordiffuse="ffffffff">aeon/track_8.png</texturesliderbarfocus>
				<textureslidernib /><textureslidernibfocus />
				<orientation>vertical</orientation>
				<showonepage>false</showonepage>
				<onleft>50</onleft>
				<onright>noop</onright>
				<onup>9000</onup>
			</control>
		</control>
		</definition>
	</include>
'''

SUBNAV = '''	<!-- 0.56.37 the sub-nav buttons' looks: the pill (AG_SubNavLook) and, in the Fused Glass style for the windows that
	     ask for it (param fgs), a grid cell: 70 high, capitals, the white bar on focus (FGS_SubNavLook) -->
	<include name="AG_SubNavLook">
		<height>subnav_h</height>
		<font>ui_22_semibold</font>
		<textcolor>$VAR[AG_Ink2]</textcolor>
		<focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>
		<textoffsetx>20</textoffsetx>
		<include>FG_SubNavFocus</include>
		<include>FG_SubNavNoFocus</include>
	</include>
	<include name="FGS_SubNavLook">
		<height>69</height>
		<font>uc_st_small_20_semibold</font>
		<textcolor>66ffffff</textcolor>
		<focusedcolor>ffffffff</focusedcolor>
		<textoffsetx>30</textoffsetx>
		<aligny>center</aligny>
		<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar.png</texturefocus>
		<texturenofocus />
		<include>FGS_RowAnim</include>
	</include>
'''


def views():
    t = rd('Includes_Views.xml')
    if MARK in t:
        return
    s = t.index('\t<include name="FGS_AddonRow">')
    e0 = t.index('<include name="FGS_View50">', s)
    e = t.index('\n\t</include>', e0) + len('\n\t</include>\n')
    block = ROW % {
        'rule': rule(0, 99, 1200),
        'ftop': rule(0, -1, 1200, '44'),
        'fbot': rule(0, 99, 1200, '44'),
        'gridtop': rule(360, 180, 1200, '1a'),
        'toolbar': rule(360, 250, 1200),
    }
    t = t[:s] + '\t' + MARK + '\n' + block + t[e:]
    wr('Includes_Views.xml', t)
    print('Includes_Views.xml done')


def common():
    t = rd('Includes_Common.xml')
    if 'name="FGS_SubNavLook"' in t:
        return
    s = t.index('<include name="AG_SubNavButton">')
    e = t.index('</include>\n', t.index('</definition>', s)) + len('</include>\n')
    b = t[s:e]
    b = once(b, '<param name="align">left</param>', '<param name="align">left</param>\n\t\t<param name="fgs">false</param>')
    old = '''				<height>subnav_h</height>
				<font>ui_22_semibold</font>
				<textcolor>$VAR[AG_Ink2]</textcolor>
				<focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>
				<textoffsetx>20</textoffsetx>
				<include>FG_SubNavFocus</include>
				<include>FG_SubNavNoFocus</include>'''
    b = once(b, old, '''				<include condition="$PARAM[fgs] + $EXP[FGS]">FGS_SubNavLook</include>
				<include condition="![$PARAM[fgs] + $EXP[FGS]]">AG_SubNavLook</include>''')
    t = t[:s] + b + t[e:]
    i = t.rfind('\n', 0, s)
    t = t[:i + 1] + SUBNAV + t[i + 1:]
    wr('Includes_Common.xml', t)
    print('Includes_Common.xml done')


GL_FGS = ('<animation effect="slide" start="0,0" end="-359,-19" time="0" condition="$EXP[FGS]">Conditional</animation>'
          '<include content="Param_H" condition="$EXP[FGS]"><param name="h" value="70"/></include>'
          '<include content="Param_H" condition="!$EXP[FGS]"><param name="h" value="subnav_h"/></include>')


def browser():
    t = rd('AddonBrowser.xml')
    if MARK in t:
        return
    t = once(t, '<visible>$EXP[Aeon_VGlass]</visible>\n\t\t\t<include>AG_GenericDetail</include>',
             '<visible>$EXP[Aeon_VGlass] + !$EXP[FGS]</visible>\n\t\t\t<include>AG_GenericDetail</include>')
    t = once(t, '<visible>![$EXP[Aeon_VGlass]] + Integer.IsGreater(Container.NumItems,0)</visible>',
             '<visible>![$EXP[Aeon_VGlass]] + Integer.IsGreater(Container.NumItems,0) + !$EXP[FGS]</visible>')
    # the toolbar
    s = t.index('<control type="grouplist" id="9000">')
    e = t.index('</control>\n\t\t<control type="button" id="3">', s)
    b = t[s:e]
    b = once(b, '<height>subnav_h</height>', GL_FGS)
    b = b.replace('<include content="AG_SubNavButton">', '<include content="AG_SubNavButton"><param name="fgs" value="true"/>')
    t = t[:s] + b + t[e:]
    # last repository check: the hint line
    t = once(t, '<label>$INFO[Window(AddonBrowser).Property(Updated),$ADDON[skin.aeon.fuse 32015]  ,]</label>',
             '<label>$INFO[Window(AddonBrowser).Property(Updated),$ADDON[skin.aeon.fuse 32015]  ,]</label>\n'
             '\t\t\t<animation effect="slide" start="0,0" end="-60,888" time="0" condition="$EXP[FGS]">Conditional</animation>')
    # empty folder label into the grid
    t = once(t, '<label>$LOCALIZE[31012]</label>', '<label>$LOCALIZE[31012]</label>\n\t\t\t<animation effect="slide" start="0,0" end="126,-49" time="0" condition="$EXP[FGS]">Conditional</animation>')
    t = t.replace('<include condition="$EXP[FGS]">FGS_View50</include><!-- 0.56.30 fgs_round2 -->',
                  '<include condition="$EXP[FGS]">FGS_View50</include><!-- 0.56.30 fgs_round2 -->' + MARK)
    wr('AddonBrowser.xml', t)
    print('AddonBrowser.xml done')


def misc():
    t = rd('Includes_Misc.xml')
    if MARK in t:
        return
    s = t.index('<include name="Misc_MediaWindow">')
    e = t.index('\n\t</include>', s)
    b = t[s:e]
    b = once(b, '\t\t\t<include>AG_GenericDetail</include>', '\t\t\t<include condition="!$EXP[FGS]">AG_GenericDetail</include>')
    b = once(b, '<include condition="$EXP[FGS]">FGS_View50</include>',
             '<include content="FGS_View50" condition="$EXP[FGS]"><param name="wide" value="true"/></include>' + MARK)
    i = b.index('<control type="grouplist" id="9000">')
    j = b.index('</control>', i)
    gl = b[i:j]
    gl = once(gl, '<height>subnav_h</height>', GL_FGS)
    gl = once(gl, '<include>Misc_SortButtons</include>', '<include condition="!$EXP[FGS]">Misc_SortButtons</include><include condition="$EXP[FGS]">FGS_SortButtons</include>')
    b = b[:i] + gl + b[j:]
    # the counter above the grid's right end, the empty label into the grid
    b = once(b, '<label>$INFO[Container.CurrentItem,, $ADDON[skin.aeon.fuse 32285] ]$INFO[Container.NumItems]</label>',
             '<label>$INFO[Container.CurrentItem,, $ADDON[skin.aeon.fuse 32285] ]$INFO[Container.NumItems]</label>\n'
             '\t\t\t\t<visible>!$EXP[FGS]</visible>')
    b = once(b, '<visible>Integer.IsEqual(Container.NumItems,0) + !Container.IsUpdating</visible>',
             '<visible>Integer.IsEqual(Container.NumItems,0) + !Container.IsUpdating</visible>\n'
             '\t\t\t\t<animation effect="slide" start="0,0" end="126,-49" time="0" condition="$EXP[FGS]">Conditional</animation>')
    t = t[:s] + b + t[e:]
    # the style's sort buttons
    k = t.index('\t<include name="Misc_SortButtons">')
    m = t.index('\n\t</include>', k) + len('\n\t</include>')
    sb = t[k:m].replace('<include name="Misc_SortButtons">', '<include name="FGS_SortButtons">')
    sb = sb.replace('<include content="AG_SubNavButton">', '<include content="AG_SubNavButton"><param name="fgs" value="true"/>')
    t = t[:m] + '\n' + sb + t[m:]
    wr('Includes_Misc.xml', t)
    print('Includes_Misc.xml done')


if __name__ == '__main__':
    views()
    common()
    browser()
    misc()
