"""0.56.32 Fused Glass style: the menus and dialogs in the System grid (canvas EGmWgk5AFMr3yy8fV5DG5j, boards Ctx,
Select, SelectOverlay, Pick, YesNo, Fav; the user's notes there: fanart behind by default, a setting for the dimmed
screen instead; the real item's fanart; favourites of every kind).

The model: full screen, no card; the header top left (light word, bold word); one grid 360-1560: the icon column,
a thin divider at 810, labels in capitals at 846; rows of 70 (the settings grid's height) under a faint rule; the
focus = a white bar on the divider with brighter rules; Back closes (no Cancel button); a key hint bottom left.

- Context menu (DialogContextMenu.xml): Kodi clones button 1000 into grouplist 996, so rows cannot carry icons:
  the item's poster (or thumb) stands in the icon column instead. Header: the item's name + OPTIONS.
- Select (DialogSelect.xml, not the track panel over video, not the skin's palette / icon pickers): list 3 puts the
  number (01, 02 ...) in the icon column, list 6 the picture; label2 at the row's end (list 6: under the label);
  multi-select ticks in gold; buttons 5 / 8 (when Kodi shows them) under the grid; 7 (Cancel) hidden.
- Yes / No (DialogConfirm.xml): the question in the grid's first cell, then the Yes / No / custom rows.
- Favourites and the other media windows of Misc_MediaWindow: the add-on browser's grid list (FGS_View50).
- Background: Skin.String(aeon.fgsdlgbg) '' = Fanart (the item's fanart, else the backdrop, under the settings
  screens' dim), screen = the window behind, dimmed. Row 9798 in Skin settings > Appearance (only in the style).

Run from the skin folder after fgs_grid_05631. Repeatable."""
import io
import os
import sys

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, '1080i')
MARK = '<!-- 0.56.32 fgs_dialogs -->'
MARK_END = '<!-- /0.56.32 fgs_dialogs -->'
SEL_OK = '$EXP[FGS] + String.IsEmpty(Window(Home).Property(aeon.palpick)) + String.IsEmpty(Window(Home).Property(aeon.iconpick))'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def once(text, old, new, count=1):
    assert text.count(old) == count, (old[:100], text.count(old))
    return text.replace(old, new)


def picture():
    """fg/fgs_rowdiv.png: a dialog row's rules: the divider (left column, 10 %) and the rule under it (bottom row, 7 %);
    16 px with a transparent margin inside border 2,0,0,2 (0.56.33: an 8 px picture smeared the lines across the row)"""
    im = Image.new('RGBA', (16, 16), (255, 255, 255, 0))
    for x in range(1, 16):
        im.putpixel((x, 15), (255, 255, 255, 0x12))
    for y in range(16):
        im.putpixel((0, y), (255, 255, 255, 0x1a))
    im.save(os.path.join(ROOT, 'media', 'fg', 'fgs_rowdiv.png'))


def rule(left, top, width, alpha='12'):
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>1</height>'
            '<texture colordiffuse="%sffffff">common/white.png</texture></control>' % (left, top, width, alpha))


def vline(left, top, height, alpha='21'):
    return ('<control type="image"><left>%d</left><top>%d</top><width>1</width><height>%d</height>'
            '<texture colordiffuse="%sffffff">common/white.png</texture></control>' % (left, top, height, alpha))


INCLUDES = '''	%(mark)s
	<!-- the menus' background: Fanart (default) or the screen behind, dimmed (Skin.String(aeon.fgsdlgbg)) -->
	<variable name="FGS_DlgFan">
		<value condition="!String.IsEmpty(ListItem.Art(fanart))">$INFO[ListItem.Art(fanart)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.fanart))">$INFO[ListItem.Art(tvshow.fanart)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(artist.fanart))">$INFO[ListItem.Art(artist.fanart)]</value>
		<value>$INFO[Window(Home).Property(aeon.bgfan)]</value>
	</variable>
	<variable name="FGS_CtxFan">
		<value condition="!String.IsEmpty(ListItem.Art(fanart))">$INFO[ListItem.Art(fanart)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.fanart))">$INFO[ListItem.Art(tvshow.fanart)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(artist.fanart))">$INFO[ListItem.Art(artist.fanart)]</value>
		<value condition="String.IsEmpty(ListItem.Label)">$INFO[Window(Home).Property(aeon.bgfan)]</value>
	</variable>
	<variable name="FGS_CtxArt">
		<value condition="!String.IsEmpty(ListItem.Art(poster))">$INFO[ListItem.Art(poster)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(tvshow.poster))">$INFO[ListItem.Art(tvshow.poster)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(album.thumb))">$INFO[ListItem.Art(album.thumb)]</value>
		<value condition="!String.IsEmpty(ListItem.Art(thumb))">$INFO[ListItem.Art(thumb)]</value>
	</variable>
	<include name="FGS_DlgBack">
		<param name="fan">$VAR[FGS_DlgFan]</param>
		<definition>
		<control type="group">
			<visible>!String.IsEqual(Skin.String(aeon.fgsdlgbg),screen)</visible>
			<control type="image"><left>-40</left><top>-40</top><width>2000</width><height>1160</height><texture colordiffuse="$VAR[AG_Ground]">common/white.png</texture></control>
			<control type="image">
				<left>-40</left><top>-40</top><width>2000</width><height>1160</height>
				<aspectratio>scale</aspectratio><fadetime>300</fadetime>
				<texture background="true" colordiffuse="$VAR[Aeon_BackdropAlpha]">$PARAM[fan]</texture>
				<visible>!Skin.HasSetting(aeon.nobackdrop)</visible>
			</control>
			<control type="image"><left>-40</left><top>-40</top><width>2000</width><height>1160</height><texture colordiffuse="$VAR[FG_BackdropDim]">common/white.png</texture><visible>!Skin.HasSetting(aeon.nobackdrop)</visible></control>
		</control>
		<control type="image">
			<left>-40</left><top>-40</top><width>2000</width><height>1160</height>
			<texture colordiffuse="d906070a">common/white.png</texture>
			<visible>String.IsEqual(Skin.String(aeon.fgsdlgbg),screen)</visible>
		</control>
		</definition>
	</include>
	<include name="FGS_DlgHeader">
		<param name="lead"></param>
		<param name="leadvis">false</param>
		<param name="label"></param>
		<definition>
			<control type="grouplist">
				<left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>
				<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$PARAM[lead][/UPPERCASE]</label><visible>$PARAM[leadvis]</visible></control>
				<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$PARAM[label][/UPPERCASE]</label></control>
			</control>
		</definition>
	</include>
	<include name="FGS_DlgHint">
		<param name="label"></param>
		<definition>
			<control type="label"><left>60</left><top>1012</top><width>1200</width><height>40</height><aligny>center</aligny><font>st_small_20</font><textcolor>73ffffff</textcolor><label>$PARAM[label]</label></control>
		</definition>
	</include>
	<!-- a dialog row (a button): the divider on its left edge and the rule under it; in focus the white bar on the
	     divider and brighter rules; capitals -->
	<include name="FGS_DlgRow">
		<width>750</width>
		<height>70</height>
		<font>uc_st_ui_24_semibold</font>
		<textcolor>66ffffff</textcolor>
		<focusedcolor>ffffffff</focusedcolor>
		<disabledcolor>44ffffff</disabledcolor>
		<textoffsetx>36</textoffsetx>
		<aligny>center</aligny>
		<pulseonselect>false</pulseonselect>
		<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar.png</texturefocus>
		<texturenofocus border="2,0,0,2">fg/fgs_rowdiv.png</texturenofocus>
		<include>FGS_RowAnim</include>
	</include>
	<!-- context menu -->
	<include name="FGS_Ctx">
		<control type="group">
			<include content="FGS_DlgBack"><param name="fan" value="$VAR[FGS_CtxFan]"/></include>
			<include>Aeon_ClockBox</include>
			<include content="FGS_DlgHeader"><param name="lead" value="$INFO[ListItem.Label]"/><param name="leadvis" value="!String.IsEmpty(ListItem.Label)"/><param name="label" value="$LOCALIZE[31272]"/></include>
			<!-- rows cannot carry icons (Kodi clones one button): the item's poster stands in the icon column -->
			<control type="image"><left>450</left><top>181</top><width>324</width><height>486</height><aspectratio align="right" aligny="top">keep</aspectratio><texture background="true">$VAR[FGS_CtxArt]</texture></control>
			<!-- 0.56.34: no poster (Kodi often gives the menu no art) -> the rows stand in the middle of the screen, not
			     beside an empty icon column -->
			<control type="group">
			<animation effect="slide" start="0,0" end="-225,0" time="0" condition="String.IsEmpty(ListItem.Art(poster)) + String.IsEmpty(ListItem.Art(tvshow.poster)) + String.IsEmpty(ListItem.Art(album.thumb)) + String.IsEmpty(ListItem.Art(thumb))">Conditional</animation>
			%(ctxtop)s
			<control type="image" id="999"><left>810</left><top>181</top><width>750</width><height>70</height><texture>common/white.png</texture><visible>false</visible></control>
			<control type="grouplist" id="996">
				<left>810</left><top>181</top><width>750</width><height max="770">auto</height>
				<itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
				<control type="button" id="990">
					<include>FGS_DlgRow</include>
					<label>$LOCALIZE[31342]</label>
					<onclick>Dialog.Close(contextmenu)</onclick>
					<onclick>AlarmClock(aeonopen,ActivateWindow(1160),00:00,silent)</onclick>
					<visible>$EXP[Ctx_ViewRowVis]</visible>
				</control>
			</control>
			</control>
			<include content="FGS_DlgHint"><param name="label" value="$ADDON[skin.aeon.fuse 32692]"/></include>
		</control>
		<control type="button" id="1000">
			<description>button template</description>
			<left>0</left><top>0</top>
			<include>FGS_DlgRow</include>
		</control>
	</include>
	<!-- select: a row of list 3 (number) or list 6 (picture) -->
	<include name="FGS_SelRow">
		<param name="focus">false</param>
		<param name="id">3</param>
		<param name="pic">false</param>
		<definition>
			%(selrule)s
			%(seldiv)s
			<control type="group">
				<visible>$PARAM[focus] + Control.HasFocus($PARAM[id])</visible>
				<include>FGS_RowAnim</include>
				%(selfocus)s
				<control type="image"><left>448</left><top>0</top><width>5</width><height>70</height><texture>common/white.png</texture></control>
			</control>
			<control type="label"><left>308</left><top>0</top><width>100</width><height>70</height><align>center</align><aligny>center</aligny><font>st_ui_26</font><textcolor>59ffffff</textcolor><label>0$INFO[ListItem.CurrentItem]</label><visible>!$PARAM[pic] + Integer.IsLess(ListItem.CurrentItem,10) + ![$PARAM[focus] + Control.HasFocus($PARAM[id])]</visible></control>
			<control type="label"><left>308</left><top>0</top><width>100</width><height>70</height><align>center</align><aligny>center</aligny><font>st_ui_26</font><textcolor>59ffffff</textcolor><label>$INFO[ListItem.CurrentItem]</label><visible>!$PARAM[pic] + !Integer.IsLess(ListItem.CurrentItem,10) + ![$PARAM[focus] + Control.HasFocus($PARAM[id])]</visible></control>
			<control type="label"><left>308</left><top>0</top><width>100</width><height>70</height><align>center</align><aligny>center</aligny><font>st_ui_26_semibold</font><textcolor>ffffffff</textcolor><label>0$INFO[ListItem.CurrentItem]</label><visible>!$PARAM[pic] + Integer.IsLess(ListItem.CurrentItem,10) + $PARAM[focus] + Control.HasFocus($PARAM[id])</visible></control>
			<control type="label"><left>308</left><top>0</top><width>100</width><height>70</height><align>center</align><aligny>center</aligny><font>st_ui_26_semibold</font><textcolor>ffffffff</textcolor><label>$INFO[ListItem.CurrentItem]</label><visible>!$PARAM[pic] + !Integer.IsLess(ListItem.CurrentItem,10) + $PARAM[focus] + Control.HasFocus($PARAM[id])</visible></control>
			<control type="image"><left>300</left><top>6</top><width>130</width><height>58</height><aspectratio align="right">keep</aspectratio><texture background="true">$VAR[FGS_SelArt]</texture><visible>$PARAM[pic]</visible></control><control type="image"><left>333</left><top>12</top><width>91</width><height>46</height><aspectratio>keep</aspectratio><texture background="true">$VAR[FGS_SelLogo]</texture><visible>$PARAM[pic] + String.IsEmpty(ListItem.Art(landscape)) + ![String.IsEqual(ListItem.DBType,episode) + [!String.IsEmpty(ListItem.Art(thumb)) | !String.IsEmpty(ListItem.Art(tvshow.landscape))]] + !String.IsEmpty(ListItem.Art(fanart))</visible></control>
			<control type="image"><left>258</left><top>23</top><width>24</width><height>24</height><texture colordiffuse="fg_mark">markers/check.png</texture><visible>ListItem.IsSelected</visible></control>
			<!-- the label (capitals); list 6 puts label2 under it, list 3 at the row's end -->
			<control type="label"><left>486</left><top>0</top><width>678</width><height>70</height><aligny>center</aligny><font>uc_st_ui_24_semibold</font><textcolor>66ffffff</textcolor><label>$INFO[ListItem.Label]</label><visible>![$PARAM[pic] + !String.IsEmpty(ListItem.Label2)] + ![$PARAM[focus] + Control.HasFocus($PARAM[id])]</visible></control>
			<control type="label"><left>486</left><top>0</top><width>678</width><height>70</height><aligny>center</aligny><font>uc_st_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$INFO[ListItem.Label]</label><scroll>true</scroll><visible>![$PARAM[pic] + !String.IsEmpty(ListItem.Label2)] + $PARAM[focus] + Control.HasFocus($PARAM[id])</visible></control>
			<control type="label"><left>486</left><top>6</top><width>678</width><height>36</height><aligny>center</aligny><font>uc_st_ui_24_semibold</font><textcolor>66ffffff</textcolor><label>$INFO[ListItem.Label]</label><visible>$PARAM[pic] + !String.IsEmpty(ListItem.Label2) + ![$PARAM[focus] + Control.HasFocus($PARAM[id])]</visible></control>
			<control type="label"><left>486</left><top>6</top><width>678</width><height>36</height><aligny>center</aligny><font>uc_st_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$INFO[ListItem.Label]</label><scroll>true</scroll><visible>$PARAM[pic] + !String.IsEmpty(ListItem.Label2) + $PARAM[focus] + Control.HasFocus($PARAM[id])</visible></control>
			<control type="label"><left>486</left><top>40</top><width>678</width><height>24</height><aligny>center</aligny><font>st_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[ListItem.Label2]</label><visible>$PARAM[pic]</visible></control>
			<control type="label"><left>900</left><top>0</top><width>264</width><height>70</height><align>right</align><aligny>center</aligny><font>st_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[ListItem.Label2]</label><visible>!$PARAM[pic]</visible></control>
		</definition>
	</include>
	<include name="FGS_SelList">
		<param name="id">3</param>
		<param name="pic">false</param>
		<definition>
			<control type="list" id="$PARAM[id]">
				<left>360</left><top>181</top><width>1200</width><height>700</height>
				<onup>$PARAM[id]</onup>
				<ondown>$PARAM[id]</ondown>
				<onleft>9001</onleft>
				<onright condition="Control.IsVisible(61)">61</onright><onright condition="!Control.IsVisible(61)">9001</onright>
				<pagecontrol>61</pagecontrol>
				<scrolltime tween="cubic" easing="out">200</scrolltime>
				<itemlayout width="1200" height="70"><include content="FGS_SelRow"><param name="id" value="$PARAM[id]"/><param name="pic" value="$PARAM[pic]"/></include></itemlayout>
				<focusedlayout width="1200" height="70"><include content="FGS_SelRow"><param name="id" value="$PARAM[id]"/><param name="pic" value="$PARAM[pic]"/><param name="focus" value="true"/></include></focusedlayout>
			</control>
			<control type="image"><left>360</left><top>180</top><width>1200</width><height>1</height><texture colordiffuse="44ffffff">common/white.png</texture><visible>Control.HasFocus($PARAM[id]) + Integer.IsEqual(Container($PARAM[id]).Position,0)</visible></control>
			<control type="label"><left>1160</left><top>128</top><width>400</width><height>40</height><align>right</align><aligny>center</aligny><font>st_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[Container($PARAM[id]).CurrentItem]  /  $INFO[Container($PARAM[id]).NumItems]</label><visible>Control.IsVisible($PARAM[id]) + Integer.IsGreater(Container($PARAM[id]).NumItems,0)</visible></control>
		</definition>
	</include>
	<include name="FGS_Select">
		<control type="group">
			<include>FGS_DlgBack</include>
			<include>Aeon_ClockBox</include>
			<control type="label" id="1"><visible>false</visible></control>
			<include content="FGS_DlgHeader"><param name="label" value="$INFO[Control.GetLabel(1)]"/></include>
			%(gridtop)s
			<include content="FGS_SelList"><param name="id" value="3"/></include>
			<include content="FGS_SelList"><param name="id" value="6"/><param name="pic" value="true"/></include>
			<control type="label"><left>846</left><top>181</top><width>678</width><height>70</height><aligny>center</aligny><font>st_cap_20</font><textcolor>80ffffff</textcolor><label>$LOCALIZE[31226]</label><visible>[Control.IsVisible(3) + Integer.IsEqual(Container(3).NumItems,0)] | [Control.IsVisible(6) + Integer.IsEqual(Container(6).NumItems,0)]</visible></control>
			<control type="scrollbar" id="61">
				<left>1556</left><top>181</top><width>4</width><height>700</height>
				<texturesliderbackground border="2" colordiffuse="1affffff">aeon/track_8.png</texturesliderbackground>
				<texturesliderbar border="2" colordiffuse="80ffffff">aeon/track_8.png</texturesliderbar>
				<texturesliderbarfocus border="2" colordiffuse="ffffffff">aeon/track_8.png</texturesliderbarfocus>
				<textureslidernib /><textureslidernibfocus />
				<orientation>vertical</orientation><showonepage>false</showonepage>
				<onleft condition="Control.IsVisible(3)">3</onleft>
				<onleft condition="Control.IsVisible(6)">6</onleft>
				<onright>9001</onright>
			</control>
			<control type="grouplist" id="9001">
				<left>810</left><top>900</top><width>750</width><height>70</height>
				<orientation>horizontal</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
				<onup condition="Control.IsVisible(3)">3</onup><onup condition="Control.IsVisible(6)">6</onup>
				<ondown condition="Control.IsVisible(3)">3</ondown><ondown condition="Control.IsVisible(6)">6</ondown>
				<control type="button" id="5"><width min="200" max="750">auto</width><include>FGS_DlgRow</include></control>
				<control type="button" id="8"><width min="200" max="750">auto</width><include>FGS_DlgRow</include></control>
				<!-- Back closes: no Cancel row (Kodi's id kept) -->
				<control type="button" id="7"><include>FGS_DlgRow</include><label>$LOCALIZE[222]</label><visible>false</visible></control>
			</control>
			<include content="FGS_DlgHint"><param name="label" value="$ADDON[skin.aeon.fuse 32693]"/></include>
		</control>
	</include>
	<!-- yes / no: the question in the grid's first cell, then the rows -->
	<include name="FGS_Confirm">
		<control type="group">
			<include>FGS_DlgBack</include>
			<include>Aeon_ClockBox</include>
			<control type="label" id="1"><visible>false</visible></control>
			<include content="FGS_DlgHeader"><param name="label" value="$INFO[Control.GetLabel(1)]"/></include>
			%(gridtop)s
			%(qdiv)s
			<control type="textbox" id="9">
				<left>846</left><top>196</top><width>678</width><height>180</height>
				<font>st_ui_24</font><textcolor>ddffffff</textcolor><aligny>center</aligny>
				<autoscroll time="3000" delay="4000" repeat="5000">true</autoscroll>
			</control>
			<control type="progress" id="20">
				<left>846</left><top>380</top><width>678</width><height>2</height>
				<info>System.Progressbar</info>
			</control>
			%(qrule)s
			<control type="grouplist" id="9000">
				<left>810</left><top>392</top><width>750</width><height>420</height>
				<orientation>vertical</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>
				<control type="button" id="11"><include>FGS_DlgRow</include><label>$LOCALIZE[107]</label></control>
				<control type="button" id="10"><include>FGS_DlgRow</include><label>$LOCALIZE[106]</label></control>
				<control type="button" id="12"><include>FGS_DlgRow</include></control>
			</control>
		</control>
	</include>
'''


def includes():
    """writes (or rewrites) the block between MARK and MARK_END"""
    t = rd('Includes_Fused.xml')
    block = INCLUDES % {
        'mark': MARK,
        'ctxtop': rule(810, 180, 750),
        'gridtop': rule(360, 180, 1200),
        'selrule': rule(0, 69, 1200),
        'seldiv': vline(450, 0, 70, '1a'),
        'selfocus': rule(0, -1, 1200, '44') + rule(0, 69, 1200, '44') + vline(1199, 0, 70, '44'),
        'qdiv': vline(810, 181, 210, '1a'),
        'qrule': rule(360, 391, 1200),
    }
    block += '\t' + MARK_END + '\n'
    if MARK in t:
        s = t.index('\t' + MARK)
        e = t.index(MARK_END) + len(MARK_END) + 1 if MARK_END in t else t.index('\t<include name="FGS_RowTex">')
        if t[s:e] == block:
            return
        t = t[:s] + block + t[e:]
    else:
        t = once(t, '\t<include name="FGS_RowTex">', block + '\t<include name="FGS_RowTex">')
    wr('Includes_Fused.xml', t)
    print('Includes_Fused.xml done')


def addon_icons():
    """the grid list's icon box (add-on browser, favourites, media windows): 96 x 56, so a landscape thumb or a poster
    reads as well as a square icon"""
    t = rd('Includes_Views.xml')
    s = t.index('<include name="FGS_AddonRow">')
    e = t.index('\n\t</include>', s)
    b = t[s:e]
    old = '<left>33</left><top>13</top><width>44</width><height>44</height><aspectratio>keep</aspectratio>'
    if old in b:
        b = b.replace(old, '<left>7</left><top>7</top><width>96</width><height>56</height><aspectratio>keep</aspectratio>')
        wr('Includes_Views.xml', t[:s] + b + t[e:])
        print('add-on row icons done')


def dialogs():
    t = rd('DialogContextMenu.xml')
    if 'FGS_Ctx' not in t:
        t = once(t, '<include>Anim_DialogOpenClose</include>', '<include>Anim_DialogOpenClose</include>')
        t = once(t, '<include condition="!$EXP[Aeon_MS]">Ctx_Classic</include>',
                 '<include condition="!$EXP[Aeon_MS] + !$EXP[FGS]">Ctx_Classic</include>\n\t\t<include condition="$EXP[FGS]">FGS_Ctx</include>' + MARK)
        wr('DialogContextMenu.xml', t)
    t = rd('DialogSelect.xml')
    if 'FGS_Select' not in t:
        t = once(t, '<include condition="!$EXP[Dlg_IsTrackPanel] + ![$EXP[Aeon_MS] + $EXP[MS_SelPlain]]">Dlg_SelectCentred</include>',
                 '<include condition="!$EXP[Dlg_IsTrackPanel] + ![$EXP[Aeon_MS] + $EXP[MS_SelPlain]] + ![%s]">Dlg_SelectCentred</include>\n'
                 '\t\t<include condition="!$EXP[Dlg_IsTrackPanel] + %s">FGS_Select</include>%s' % (SEL_OK, SEL_OK, MARK))
        wr('DialogSelect.xml', t)
    t = rd('DialogConfirm.xml')
    if 'FGS_Confirm' not in t:
        t = once(t, '<include condition="!$EXP[Aeon_MS]">Confirm_Classic</include>',
                 '<include condition="!$EXP[Aeon_MS] + !$EXP[FGS]">Confirm_Classic</include>\n\t\t\t<include condition="$EXP[FGS]">FGS_Confirm</include>' + MARK)
        wr('DialogConfirm.xml', t)
    t = rd('Includes_Misc.xml')
    s = t.index('<include name="Misc_MediaWindow">')
    e = t.index('\n\t</include>', s)
    b = t[s:e]
    if 'FGS_View50' not in b:
        b = once(b, '<include>View_50_List</include>', '<include condition="!$EXP[FGS]">View_50_List</include><include condition="$EXP[FGS]">FGS_View50</include>' + MARK)
        b = once(b, '<include>AG_CardDense</include>', '<include condition="!$EXP[FGS]">AG_CardDense</include>')
        t = t[:s] + b + t[e:]
        wr('Includes_Misc.xml', t)
    print('dialogs done')


# ---------------------------------------------------------------------------------------- the setting (row 9798)
def setting_row():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.chdir(ROOT)
    import expert_05628 as X
    path = os.path.join(D, 'SkinSettings.xml')
    t = io.open(path, encoding='utf-8').read()
    if 'id="9798"' in t:
        return
    setting = 'aeon.fgsdlgbg'
    opts = [('', '$LOCALIZE[31550]', 150), ('screen', '$ADDON[skin.aeon.fuse 32690]', 150)]
    navs = X.nav([(9748, None)], [(9529, None)])
    body = X.row(t, 9798, '$ADDON[skin.aeon.fuse 32689]', 'aeon/icons/lines.png', 860 - 300 - 46 - 20, navs,
                 X.cycle(setting, opts), X.pills(9798, setting, opts), vis='$EXP[FGS]')
    body = body.replace(X.MARK, '0.56.32 fgs_dialogs')
    namew = 860 - 300 - 46 - 20
    body = body.replace('<include content="Dlg_SkinRowChrome">', '<include content="Dlg_SkinRowChrome"><param name="namefgs" value="%d"/>' % (namew + 101), 1)
    # after Skin style (9748): its group ends where row 9529's group starts
    anchor = '\t<control type="group"><!-- row 9529'
    if anchor not in t:
        anchor = None
    i = t.index('<control type="button" id="9529">')
    start = t.rfind('\n\t<control type="group">', 0, i) + 1
    t = t[:start] + body + t[start:]
    # navigation: Skin style down -> 9798 in the style; Panel shadow up -> 9798 in the style
    i = t.index('<control type="button" id="9748">')
    j = t.index('<ondown', i)
    t = t[:j] + '<ondown condition="$EXP[FGS]">9798</ondown>' + t[j:]
    i = t.index('<control type="button" id="9529">')
    k = t.index('</control>', i)
    j = t.index('<onup', i)
    assert j < k
    t = t[:j] + '<onup condition="$EXP[FGS]">9798</onup>' + t[j:]
    io.open(path, 'w', encoding='utf-8', newline='\n').write(t)
    # help text
    h = rd('Includes_Settings.xml')
    old = '<value condition="Control.HasFocus(9790)">'
    h = once(h, old, '<value condition="Control.HasFocus(9798)">$ADDON[skin.aeon.fuse 32691]</value>\n\t\t' + old)
    wr('Includes_Settings.xml', h)
    print('row 9798 done')


def row_inks():
    """the row's pills use the style's ink twins (FGS_*), as fgs_05629 gave the other rows"""
    t = rd('SkinSettings.xml')
    s = t.index('<!-- row 9798 (')
    e = t.index('\n\t</control>\n', s)
    b = t[s:e]
    nb = b
    for v in ('Aeon_OnBarFill', 'Aeon_SegSelTxt', 'Aeon_SegUnselF'):
        nb = nb.replace('$VAR[%s]' % v, '$VAR[FGS_%s]' % v)
    if nb != b:
        t = t[:s] + nb + t[e:]
        wr('SkinSettings.xml', t)
        print('row 9798 inks done')


if __name__ == '__main__':
    picture()
    includes()
    dialogs()
    addon_icons()
    setting_row()
    row_inks()
