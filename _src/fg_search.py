"""0.42.0 Fused Glass Search (mockup boards Search and SearchResults). Run from the skin folder. Writes into
1080i/Includes_Fused.xml (between FG_SEARCH markers):
  FG_SearchWindow   the Search window (Custom_1150) in Fused Glass: the query in a field at the top, a keyboard of its own
                    on the left (a-z, 0-9, Space / Delete / Clear) typing into Window(Home).Property(aeon.q), and beside
                    it the library's shows (9101, wide cards; the card in focus says "You're on S3 E1") and films (9102),
                    then Also search (9105: Music, People, TMDb, YouTube). OK on the field opens Kodi's keyboard.
  FG_H_SearchPage   Home > Search in Fused Glass: a search field and the recent searches over the picture; under the
                    menu Last search / Online: TMDb / YouTube tabs (9383) over a row of results (9384 / 9385 / 9386).
It also moves the classic window's controls into Search_WindowClassic (Includes_Search.xml), makes Custom_1150 and
Aeon_H_SearchRecent load-time variants, and sets Up / Down from the Search menu item in Fused Glass."""
import io
import re

FUSED = '1080i/Includes_Fused.xml'
SEARCH = '1080i/Includes_Search.xml'
WINDOW = '1080i/Custom_1150_Search.xml'
HOME = '1080i/Includes_Aeon_Home.xml'
A = '$ADDON[skin.aeon.fuse %d]'
Q = 'Window(Home).Property(aeon.q)'
HASQ = '!String.IsEmpty(%s)' % Q
KEYS = list('abcdefghijklmnopqrstuvwxyz1234567890')

src = io.open(SEARCH, encoding='utf-8').read()
paths = {}
for name in ('Search_PathMovies', 'Search_PathTV'):
    found = re.search(r'<variable name="%s">\s*<value condition="[^"]+">(.*?)</value>' % name, src, re.S)
    paths[name] = found.group(1)

READY = '%s + !String.IsEmpty(Window(Home).Property(Aeon.Search.Encoded))' % HASQ
VARS = ('\t<variable name="FG_SearchEncoder">\n\t\t<value condition="' + HASQ + '">plugin://script.skinvariables/?info=get_encoded_string&amp;'
        'unencoded_paths=true&amp;esc=%25&amp;window_prop=Aeon.Search.Encoded&amp;window_id=home&amp;&amp;$ESCINFO[' + Q + ']</value>\n\t</variable>\n'
        '\t<variable name="FG_SearchMovies">\n\t\t<value condition="' + READY + '">' + paths['Search_PathMovies'] + '</value>\n\t</variable>\n'
        '\t<variable name="FG_SearchTV">\n\t\t<value condition="' + READY + '">' + paths['Search_PathTV'] + '</value>\n\t</variable>\n'
        '\t<variable name="FG_SearchField">\n\t\t<value condition="' + HASQ + '">$INFO[' + Q + '][COLOR fg_mark]|[/COLOR]</value>\n'
        '\t\t<value>[COLOR 80ffffff]' + A % 32517 + '[/COLOR]</value>\n\t</variable>\n')


def key_item(ch):
    label = '$NUMBER[%s]' % ch if ch.isdigit() else ch          # a bare number would be read as a string id
    return ('\t\t\t\t\t\t<item><label>%s</label><onclick>SetProperty(aeon.q,"$INFO[%s]%s",home)</onclick></item>\n' % (label, Q, ch))


RESULTS_RIGHT = ('<onright condition="Integer.IsGreater(Container(9111).NumItems,0)">SetFocus(9101)</onright>'
                 '<onright condition="!Integer.IsGreater(Container(9111).NumItems,0) + Integer.IsGreater(Container(9112).NumItems,0)">SetFocus(9102)</onright>'
                 '<onright condition="!Integer.IsGreater(Container(9111).NumItems,0) + !Integer.IsGreater(Container(9112).NumItems,0) + ' + HASQ + '">SetFocus(9105)</onright>')

WINDOW_BODY = '''	<include name="FG_SearchWindow">
		<!-- the query encoder (script.skinvariables) for the library paths: never shown -->
		<control type="list" id="9710">
			<left>-20</left><top>-20</top><width>1</width><height>1</height>
			<itemlayout width="1" height="1"/><focusedlayout width="1" height="1"/>
			<content target="programs">$VAR[FG_SearchEncoder]</content>
		</control>
		<!-- probes: 1 px lists that always load (a list hidden by its own count never would); the rows follow them -->
		<control type="list" id="9111">
			<left>-20</left><top>-20</top><width>1</width><height>1</height>
			<itemlayout width="1" height="1"/><focusedlayout width="1" height="1"/>
			<content target="videos" limit="30" browse="never">$VAR[FG_SearchTV]</content>
		</control>
		<control type="list" id="9112">
			<left>-20</left><top>-20</top><width>1</width><height>1</height>
			<itemlayout width="1" height="1"/><focusedlayout width="1" height="1"/>
			<content target="videos" limit="30" browse="never">$VAR[FG_SearchMovies]</content>
		</control>
		<control type="button" id="9099">
			<left>-100</left><top>-100</top><width>1</width><height>1</height><texturefocus/><texturenofocus/>
			<onfocus>SetFocus(9120)</onfocus>
			<visible allowhiddenfocus="true">false</visible>
		</control>
		<include>AG_Background</include>
		<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="99000000">common/white.png</texture></control>
		<!-- the field: OK opens Kodi's keyboard for any text -->
		<control type="button" id="9130">
			<left>120</left><top>40</top><width>1200</width><height>80</height>
			<label>$VAR[FG_SearchField]</label><font>hm_ui_30_semibold</font><textoffsetx>82</textoffsetx><aligny>center</aligny>
			<textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor>
			<texturenofocus border="40" colordiffuse="fg_frost">fg/r40.png</texturenofocus><texturefocus border="40" colordiffuse="ffffffff">fg/r40.png</texturefocus>
			<onclick>RunScript(script.aeon.helper,searchkey,kodi)</onclick>
			<onup>noop</onup><ondown>9120</ondown><onleft>noop</onleft><onright>noop</onright>
		</control>
		<control type="image"><left>120</left><top>40</top><width>1200</width><height>80</height><texture border="40" colordiffuse="fg_edge">fg/e40.png</texture><visible>!Control.HasFocus(9130)</visible></control>
		<control type="image"><left>152</left><top>62</top><width>36</width><height>36</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/search.png</texture><visible>!Control.HasFocus(9130)</visible></control>
		<control type="image"><left>152</left><top>62</top><width>36</width><height>36</height><aspectratio>keep</aspectratio><texture colordiffuse="aeon_onbar">aeon/icons/search.png</texture><visible>Control.HasFocus(9130)</visible></control>
		<!-- the keyboard -->
		<control type="image"><left>120</left><top>152</top><width>520</width><height>626</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture></control>
		<control type="image"><left>120</left><top>152</top><width>520</width><height>626</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture></control>
		<control type="panel" id="9120">
			<left>140</left><top>172</top><width>492</width><height>456</height>
			<orientation>vertical</orientation>
			<onup>9130</onup><ondown>9121</ondown><onleft>noop</onleft>@@RIGHT@@
			<itemlayout width="82" height="76">
				<control type="image"><left>0</left><top>0</top><width>74</width><height>66</height><texture border="14" colordiffuse="1fffffff">fg/r14.png</texture></control>
				<control type="label"><left>0</left><top>0</top><width>74</width><height>66</height><align>center</align><aligny>center</aligny><font>hm_ui_28_semibold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>$INFO[ListItem.Label]</label></control>
			</itemlayout>
			<focusedlayout width="82" height="76">
				<control type="image"><left>0</left><top>0</top><width>74</width><height>66</height><texture border="14" colordiffuse="1fffffff">fg/r14.png</texture><visible>!Control.HasFocus(9120)</visible></control>
				<control type="image"><left>0</left><top>0</top><width>74</width><height>66</height><texture border="14" colordiffuse="ffffffff">fg/r14.png</texture><visible>Control.HasFocus(9120)</visible></control>
				<control type="label"><left>0</left><top>0</top><width>74</width><height>66</height><align>center</align><aligny>center</aligny><font>hm_ui_28_semibold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><label>$INFO[ListItem.Label]</label><visible>!Control.HasFocus(9120)</visible></control>
				<control type="label"><left>0</left><top>0</top><width>74</width><height>66</height><align>center</align><aligny>center</aligny><font>hm_ui_28_semibold</font><textcolor>aeon_onbar</textcolor><selectedcolor>aeon_onbar</selectedcolor><label>$INFO[ListItem.Label]</label><visible>Control.HasFocus(9120)</visible></control>
			</focusedlayout>
			<content>
@@KEYS@@			</content>
		</control>
		<control type="grouplist" id="9121">
			<left>140</left><top>636</top><width>492</width><height>66</height>
			<orientation>horizontal</orientation><itemgap>12</itemgap>
			<onup>9120</onup><ondown>noop</ondown>@@RIGHT@@
			<control type="button"><width>156</width><height>66</height><label>$LOCALIZE[20182]</label><font>hm_ui_24_semibold</font><align>center</align><aligny>center</aligny><textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor><texturenofocus border="14" colordiffuse="1fffffff">fg/r14.png</texturenofocus><texturefocus border="14" colordiffuse="ffffffff">fg/r14.png</texturefocus><onclick>RunScript(script.aeon.helper,searchkey,space)</onclick></control>
			<control type="button"><width>156</width><height>66</height><label>$LOCALIZE[117]</label><font>hm_ui_24_semibold</font><align>center</align><aligny>center</aligny><textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor><texturenofocus border="14" colordiffuse="1fffffff">fg/r14.png</texturenofocus><texturefocus border="14" colordiffuse="ffffffff">fg/r14.png</texturefocus><onclick>RunScript(script.aeon.helper,searchkey,del)</onclick></control>
			<control type="button"><width>156</width><height>66</height><label>$LOCALIZE[192]</label><font>hm_ui_24_semibold</font><align>center</align><aligny>center</aligny><textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor><texturenofocus border="14" colordiffuse="1fffffff">fg/r14.png</texturenofocus><texturefocus border="14" colordiffuse="ffffffff">fg/r14.png</texturefocus><onclick>ClearProperty(aeon.q,home)</onclick></control>
		</control>
		<!-- results: a vertical grouplist, so empty parts take no room -->
		<control type="label"><left>700</left><top>148</top><width>1100</width><height>40</height><aligny>center</aligny><font>hm_ui_24</font><textcolor>99ffffff</textcolor><label>$LOCALIZE[31239]</label><visible>@@HASQ@@ + [Container(9111).IsUpdating | Container(9112).IsUpdating | String.IsEmpty(Window(Home).Property(Aeon.Search.Encoded))]</visible></control>
		<control type="label"><left>700</left><top>148</top><width>1100</width><height>40</height><aligny>center</aligny><font>hm_ui_24</font><textcolor>99ffffff</textcolor><label>$LOCALIZE[31238]</label><visible>@@HASQ@@ + !Container(9111).IsUpdating + !Container(9112).IsUpdating + !String.IsEmpty(Window(Home).Property(Aeon.Search.Encoded)) + !Integer.IsGreater(Container(9111).NumItems,0) + !Integer.IsGreater(Container(9112).NumItems,0)</visible></control>
		<control type="grouplist" id="9100">
			<left>690</left><top>140</top><width>1230</width><height>930</height>
			<orientation>vertical</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>
			<onup>9130</onup><onleft>9120</onleft>
			<control type="group">
				<width>1230</width><height>248</height>
				<visible>Integer.IsGreater(Container(9111).NumItems,0)</visible>
				<control type="label"><left>10</left><top>0</top><width>1100</width><height>34</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$LOCALIZE[20343]$INFO[Container(9111).NumItems, · ,][/UPPERCASE]</label></control>
				<control type="list" id="9101">
					<top>48</top><width>1230</width><height>200</height>
					<orientation>horizontal</orientation>
					<scrolltime tween="cubic" easing="out">200</scrolltime>
					<onleft>9120</onleft><onup>9130</onup>
					<ondown condition="Integer.IsGreater(Container(9112).NumItems,0)">9102</ondown><ondown condition="!Integer.IsGreater(Container(9112).NumItems,0)">9105</ondown>
					<onback>9120</onback>
					<visible>Integer.IsGreater(Container(9111).NumItems,0)</visible>
					<itemlayout width="884" height="200">
	@@CARD_N@@				</itemlayout>
					<focusedlayout width="884" height="200">
	@@CARD_F@@				</focusedlayout>
					<content target="videos" limit="30" browse="never">$VAR[FG_SearchTV]</content>
				</control>
			</control>
			<control type="group">
				<width>1230</width><height>348</height>
				<visible>Integer.IsGreater(Container(9112).NumItems,0)</visible>
				<control type="label"><left>10</left><top>0</top><width>1100</width><height>34</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]@@FILMS@@$INFO[Container(9112).NumItems, · ,][/UPPERCASE]</label></control>
				<control type="list" id="9102">
					<top>48</top><width>1230</width><height>300</height>
					<orientation>horizontal</orientation>
					<scrolltime tween="cubic" easing="out">200</scrolltime>
					<onleft>9120</onleft>
					<onup condition="Integer.IsGreater(Container(9111).NumItems,0)">9101</onup><onup condition="!Integer.IsGreater(Container(9111).NumItems,0)">9130</onup><ondown>9105</ondown>
					<onback>9120</onback>
					<visible>Integer.IsGreater(Container(9112).NumItems,0)</visible>
					<itemlayout width="143" height="300">
	@@POSTER_N@@				</itemlayout>
					<focusedlayout width="143" height="300">
	@@POSTER_F@@				</focusedlayout>
					<content target="videos" limit="30" browse="never">$VAR[FG_SearchMovies]</content>
				</control>
			</control>
			<control type="group">
				<width>1230</width><height>106</height>
				<visible>@@HASQ@@</visible>
				<control type="label"><left>10</left><top>0</top><width>1100</width><height>34</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]@@ALSO@@[/UPPERCASE]</label></control>
				<control type="grouplist" id="9105">
					<left>8</left><top>48</top><width>1220</width><height>58</height>
					<orientation>horizontal</orientation><itemgap>12</itemgap>
					<onleft>9120</onleft><ondown>noop</ondown><onback>9120</onback>
					<onup condition="Integer.IsGreater(Container(9112).NumItems,0)">9102</onup><onup condition="!Integer.IsGreater(Container(9112).NumItems,0) + Integer.IsGreater(Container(9111).NumItems,0)">9101</onup><onup condition="!Integer.IsGreater(Container(9112).NumItems,0) + !Integer.IsGreater(Container(9111).NumItems,0)">9130</onup>
					<visible>@@HASQ@@</visible>
	@@ALSO_BTNS@@			</control>
			</control>
		</control>
	</include>
'''


def also(ident, label, action, visible=''):
    return ('\t\t\t\t<control type="button" id="%d"><width min="80" max="600">auto</width><height>56</height><label>%s</label>'
            '<font>hm_ui_24_semibold</font><align>center</align><aligny>center</aligny><textoffsetx>26</textoffsetx>'
            '<textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor><include>FG_PillBtnTex</include>'
            '<onclick>%s</onclick><onback>9120</onback>%s</control>\n' % (ident, label, action, '<visible>%s</visible>' % visible if visible else ''))


ALSO_BTNS = (also(91051, '$LOCALIZE[2]', 'ActivateWindow(Music,"musicsearch://$INFO[%s]/",return)' % Q) +
             also(91052, A % 32522, 'ActivateWindow(Videos,"plugin://script.aeon.helper/?info=searchlib&amp;type=people&amp;q=$INFO[%s]",return)' % Q) +
             also(91053, A % 32521, 'ActivateWindow(Videos,"plugin://plugin.video.themoviedb.helper/?info=search&amp;tmdb_type=movie&amp;query=$INFO[%s]",return)' % Q,
                  'System.HasAddon(plugin.video.themoviedb.helper)') +
             also(91054, 'YouTube', 'ActivateWindow(Videos,"plugin://plugin.video.youtube/kodion/search/query/?q=$INFO[%s]",return)' % Q,
                  'System.HasAddon(plugin.video.youtube)'))


def card(focused):
    """A show: landscape at the left, title, year · network · seasons · rating; in focus a white card and the helper's
    "You're on S3 E1" pill with the next airing."""
    if focused:
        bg = ('<control type="image"><left>8</left><top>8</top><width>860</width><height>178</height><texture border="24" colordiffuse="ffffffff">fg/r24.png</texture><visible>Control.HasFocus(9101)</visible></control>'
              '<control type="image"><left>8</left><top>8</top><width>860</width><height>178</height><texture border="24" colordiffuse="fg_frost">fg/r24.png</texture><visible>!Control.HasFocus(9101)</visible></control>')
        ink, ink2 = '$VAR[FG_SearchInk]', '$VAR[FG_SearchInk2]'
    else:
        bg = '<control type="image"><left>8</left><top>8</top><width>860</width><height>178</height><texture border="24" colordiffuse="fg_frost">fg/r24.png</texture></control>'
        ink, ink2 = 'ffffffff', 'b3ffffff'
    out = ('\t\t\t\t\t' + bg +
           '<control type="image"><left>8</left><top>8</top><width>860</width><height>178</height><texture border="24" colordiffuse="fg_edge">fg/e24.png</texture></control>'
           '<control type="image"><left>22</left><top>22</top><width>268</width><height>150</height><aspectratio scalediffuse="false">scale</aspectratio>'
           '<texture background="true" diffuse="fg/m280x158.png">$INFO[ListItem.Art(landscape)]</texture><visible>!String.IsEmpty(ListItem.Art(landscape))</visible></control>'
           '<control type="image"><left>22</left><top>22</top><width>268</width><height>150</height><aspectratio scalediffuse="false">scale</aspectratio>'
           '<texture background="true" diffuse="fg/m280x158.png">$INFO[ListItem.Art(fanart)]</texture><visible>String.IsEmpty(ListItem.Art(landscape))</visible></control>'
           '<control type="label"><left>314</left><top>34</top><width>532</width><height>40</height><aligny>center</aligny><font>hm_ui_28_bold</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><scroll>%s</scroll><label>$INFO[ListItem.Label]</label><visible>%s</visible></control>'
           '<control type="label"><left>314</left><top>34</top><width>532</width><height>40</height><aligny>center</aligny><font>hm_ui_28_bold</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>$INFO[ListItem.Label]</label><visible>%s</visible></control>'
           '<control type="label"><left>314</left><top>74</top><width>532</width><height>32</height><aligny>center</aligny><font>hm_ui_22</font><textcolor>%s</textcolor><selectedcolor>%s</selectedcolor>'
           '<label>$INFO[ListItem.Year]$INFO[ListItem.Studio, · ,]$INFO[ListItem.Property(TotalSeasons), · , $LOCALIZE[33054]]$INFO[ListItem.MPAA, · ,]</label></control>'
           % (ink, ink, 'true' if focused else 'false', 'Control.HasFocus(9101)' if focused else 'false',
              ink, ink, '!Control.HasFocus(9101)' if focused else 'true', ink2, ink2))
    if focused:
        out += ('<control type="grouplist"><left>314</left><top>116</top><width>540</width><height>36</height><orientation>horizontal</orientation><itemgap>12</itemgap><usecontrolcoords>true</usecontrolcoords>'
                '<visible>Control.HasFocus(9101)</visible>'
                '<control type="button"><width min="20" max="300">auto</width><height>36</height><label>$INFO[Window(Home).Property(aeon.show.on)]</label><font>hm_small_20_bold</font><textoffsetx>14</textoffsetx><aligny>center</aligny>'
                '<textcolor>ff1a1405</textcolor><focusedcolor>ff1a1405</focusedcolor><texturenofocus border="18" colordiffuse="fg_mark">fg/r18.png</texturenofocus><texturefocus border="18" colordiffuse="fg_mark">fg/r18.png</texturefocus>'
                '<visible>!String.IsEmpty(Window(Home).Property(aeon.show.on))</visible></control>'
                '<control type="label"><width>auto</width><height>36</height><aligny>center</aligny><font>hm_small_20</font><textcolor>$VAR[FG_SearchInk2]</textcolor><label>$INFO[Window(Home).Property(aeon.show.next)]</label></control>'
                '</control>')
    return out + '\n'


def poster(focused):
    ring = ('<control type="image"><left>5</left><top>5</top><width>132</width><height>196</height><texture border="19" colordiffuse="ffffffff">fg/ring16.png</texture><visible>Control.HasFocus(9102)</visible></control>'
            if focused else '')
    return ('\t\t\t\t\t<control type="image"><left>8</left><top>8</top><width>126</width><height>190</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture></control>'
            '<control type="image"><left>8</left><top>8</top><width>126</width><height>190</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m126x190.png">$INFO[ListItem.Art(poster)]</texture></control>' + ring +
            '<control type="textbox"><left>8</left><top>206</top><width>134</width><height>50</height><font>hm_small_20_bold</font><textcolor>ffffffff</textcolor><label>$INFO[ListItem.Label]</label></control>'
            '<control type="label"><left>8</left><top>258</top><width>130</width><height>26</height><aligny>center</aligny><font>hm_small_20</font><textcolor>99ffffff</textcolor><label>$INFO[ListItem.Year]</label></control>\n')


INK_VARS = ('\t<variable name="FG_SearchInk">\n\t\t<value condition="Control.HasFocus(9101)">aeon_onbar</value>\n\t\t<value>ffffffff</value>\n\t</variable>\n'
            '\t<variable name="FG_SearchInk2">\n\t\t<value condition="Control.HasFocus(9101)">b3000000</value>\n\t\t<value>b3ffffff</value>\n\t</variable>\n')

window = (WINDOW_BODY.replace('@@RIGHT@@', RESULTS_RIGHT).replace('@@KEYS@@', ''.join(key_item(c) for c in KEYS))
          .replace('@@HASQ@@', HASQ).replace('@@CARD_N@@', card(False)).replace('@@CARD_F@@', card(True))
          .replace('@@POSTER_N@@', poster(False)).replace('@@POSTER_F@@', poster(True)).replace('@@FILMS@@', A % 31331)
          .replace('@@ALSO@@', A % 32520).replace('@@ALSO_BTNS@@', ALSO_BTNS))

# ------------------------------------------------------------------ Home > Search
TAB = 'Window(Home).Property(aeon.searchtab)'
S1 = 'Window(Home).Property(aeon.search.1)'
HOME_TABS = (('', 93831, 9384, A % 32519 + ' $INFO[%s]$VAR[FG_HSearchCount]' % S1, ''),
             ('tmdb', 93832, 9385, A % 32523 + ': TMDb', 'System.HasAddon(plugin.video.themoviedb.helper)'),
             ('yt', 93833, 9386, 'YouTube', 'System.HasAddon(plugin.video.youtube)'))


def tab_is(value):
    return 'String.IsEmpty(%s)' % TAB if not value else 'String.IsEqual(%s,%s)' % (TAB, value)


def home_tab(value, ident, lst, label, vis):
    return ('\t\t\t\t\t<control type="button" id="%d"><width min="60" max="700">auto</width><height>44</height><label>%s</label>'
            '<font>hm_ui_22_semibold</font><align>center</align><aligny>center</aligny><textoffsetx>22</textoffsetx>'
            '<textcolor>$VAR[FG_HSearchInk%d]</textcolor><focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>'
            '<texturenofocus border="22" colordiffuse="$VAR[FG_HSearchBg%d]">fg/r22.png</texturenofocus>'
            '<texturefocus border="22" colordiffuse="$VAR[FG_SysTabFocus]">fg/r22.png</texturefocus>'
            '<onfocus>%s</onfocus><ondown>SetFocus(%d)</ondown><onup>9000</onup><onback>9000</onback>%s</control>\n'
            % (ident, label, ident, ident, ('SetProperty(aeon.searchtab,%s,home)' % value) if value else 'ClearProperty(aeon.searchtab,home)',
               lst, '<visible>%s</visible>' % vis if vis else ''))


HOME_VARS = ''.join('''	<variable name="FG_HSearchBg%(b)d">
		<value condition="%(sel)s">fg_sel</value>
		<value>00ffffff</value>
	</variable>
	<variable name="FG_HSearchInk%(b)d">
		<value condition="%(sel)s">ffffffff</value>
		<value>99ffffff</value>
	</variable>
''' % {'b': b, 'sel': tab_is(v)} for v, b, l, label, vis in HOME_TABS)
HOME_VARS += ('\t<variable name="FG_HSearchCount">\n\t\t<value condition="Integer.IsGreater(Container(9384).NumItems,0)">$INFO[Container(9384).NumItems, · ,]</value>\n\t</variable>\n')


def home_list(value, tab, ident, path, w, h, art):
    pitch = w + 20
    tile = ('<control type="image"><left>0</left><top>0</top><width>%d</width><height>%d</height><texture border="16" colordiffuse="fg_frost">fg/r16.png</texture></control>'
            '<control type="image"><left>0</left><top>0</top><width>%d</width><height>%d</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m%dx%d.png">%s</texture></control>' % (w, h, w, h, w, h, art))
    ring = ('<control type="image"><left>-3</left><top>-3</top><width>%d</width><height>%d</height><texture border="19" colordiffuse="fg_mark">fg/ring16.png</texture>'
            '<visible>Control.HasFocus(%d)</visible></control>' % (w + 6, h + 6, ident))
    # posters carry their own title (and a caption would run off the screen); video thumbs get one line
    caption = ('<control type="label"><left>0</left><top>%d</top><width>%d</width><height>30</height><aligny>center</aligny><font>hm_small_20_bold</font>'
               '<textcolor>ffffffff</textcolor><label>$INFO[ListItem.Label]</label></control>' % (h + 8, w)) if w > h else ''
    return '''				<control type="list" id="%(id)d">
					<left>110</left><top>828</top><width>1710</width><height>%(lh)d</height>
					<orientation>horizontal</orientation>
					<scrolltime tween="cubic" easing="out">220</scrolltime>
					<visible>%(vis)s</visible>
					<onup>SetFocus(%(tab)d)</onup><ondown>noop</ondown><onback>9000</onback>
					<itemlayout width="%(pitch)d" height="%(lh)d"><control type="group"><left>10</left><top>10</top>%(tile)s%(caption)s</control></itemlayout>
					<focusedlayout width="%(pitch)d" height="%(lh)d"><control type="group"><left>10</left><top>10</top><animation effect="zoom" start="100" end="104" center="auto" time="160" tween="cubic" easing="out" condition="Control.HasFocus(%(id)d)">Conditional</animation>%(tile)s%(ring)s%(caption)s</control></focusedlayout>
					<content target="videos" limit="20" browse="never">%(path)s</content>
				</control>
''' % {'id': ident, 'lh': h + 60, 'vis': tab_is(value), 'tab': tab, 'pitch': pitch, 'tile': tile, 'caption': caption, 'ring': ring, 'path': path}


HOME_LISTS = (home_list('', 93831, 9384, '$VAR[FG_HSearchPath9384]', 120, 180, '$INFO[ListItem.Art(poster)]') +
              home_list('tmdb', 93832, 9385, '$VAR[FG_HSearchPath9385]', 120, 180, '$INFO[ListItem.Art(poster)]') +
              home_list('yt', 93833, 9386, '$VAR[FG_HSearchPath9386]', 256, 144, '$INFO[ListItem.Art(thumb)]'))
# a path only while the row's tab is chosen and Search is the menu item: a hidden list still loads its path when Home opens
ON_ROW = '$EXP[Aeon_H_SearchSec] + Integer.IsGreater(Window(Home).Property(aeon.search.count),0)'
for _value, _ident, _path in (('', 9384, 'plugin://script.aeon.helper/?info=searchlib&amp;type=all&amp;q=$INFO[%s]' % S1),
                              ('tmdb', 9385, 'plugin://plugin.video.themoviedb.helper/?info=search&amp;tmdb_type=movie&amp;query=$INFO[%s]' % S1),
                              ('yt', 9386, 'plugin://plugin.video.youtube/kodion/search/query/?q=$INFO[%s]' % S1)):
    HOME_VARS += ('\t<variable name="FG_HSearchPath%d">\n\t\t<value condition="%s + %s">%s</value>\n\t</variable>\n'
                  % (_ident, ON_ROW, tab_is(_value), _path))


def recent(n):
    return ('\t\t\t\t\t<control type="button" id="%d"><width min="96" max="560">auto</width><height>52</height><label>$INFO[Window(Home).Property(aeon.search.%d)]</label>'
            '<font>hm_ui_24_semibold</font><align>center</align><aligny>center</aligny><textoffsetx>26</textoffsetx>'
            '<textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor><include>FG_PillBtnTex</include>'
            '<onclick>RunScript(script.aeon.helper,search,%d)</onclick><onup>9381</onup><ondown>9000</ondown><onback>9000</onback>'
            '<visible>!String.IsEmpty(Window(Home).Property(aeon.search.%d))</visible></control>\n' % (93070 + n, n, n, n))


ON_SEARCH = '[Control.HasFocus(9000) | Control.HasFocus(9381) | ControlGroup(9307).HasFocus() | ControlGroup(9383).HasFocus() | Control.HasFocus(9384) | Control.HasFocus(9385) | Control.HasFocus(9386)]'
HAS_RECENT = 'Integer.IsGreater(Window(Home).Property(aeon.search.count),0)'
HOME_BODY = '''	<include name="FG_H_SearchPage">
		<control type="group">
			<include>Aeon_LowBand</include>
			<visible>$EXP[Aeon_H_SearchSec] + !$EXP[Aeon_H_SpotAny] + @@ON@@</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/><effect type="slide" start="0,24" end="0,0" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<control type="label"><left>120</left><top>110</top><width>1000</width><height>36</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]@@CAPTION@@[/UPPERCASE]</label></control>
			<control type="button" id="9381">
				<left>120</left><top>164</top><width>1000</width><height>96</height>
				<label>@@PLACEHOLDER@@</label><font>hm_ui_30_semibold</font><textoffsetx>94</textoffsetx><aligny>center</aligny>
				<textcolor>b3ffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor>
				<texturenofocus border="48" colordiffuse="fg_frost">fg/r48.png</texturenofocus><texturefocus border="48" colordiffuse="ffffffff">fg/r48.png</texturefocus>
				<onclick>ActivateWindow(1150)</onclick>
				<onup>noop</onup><onleft>noop</onleft><onright>noop</onright><onback>9000</onback>
				<ondown condition="@@HASRECENT@@">9307</ondown><ondown condition="!@@HASRECENT@@">9000</ondown>
			</control>
			<control type="image"><left>120</left><top>164</top><width>1000</width><height>96</height><texture border="48" colordiffuse="fg_edge">fg/e48.png</texture><visible>!Control.HasFocus(9381)</visible></control>
			<control type="image"><left>158</left><top>194</top><width>36</width><height>36</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/search.png</texture><visible>!Control.HasFocus(9381)</visible></control>
			<control type="image"><left>158</left><top>194</top><width>36</width><height>36</height><aspectratio>keep</aspectratio><texture colordiffuse="aeon_onbar">aeon/icons/search.png</texture><visible>Control.HasFocus(9381)</visible></control>
			<control type="label"><left>120</left><top>284</top><width>1000</width><height>34</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>[UPPERCASE]$ADDON[skin.aeon.fuse 32406][/UPPERCASE]</label><visible>@@HASRECENT@@</visible></control>
			<control type="grouplist" id="9307">
				<left>112</left><top>326</top><width>1300</width><height>56</height>
				<orientation>horizontal</orientation><itemgap>12</itemgap>
				<onup>9381</onup><ondown>9000</ondown>
				<visible>@@HASRECENT@@</visible>
@@RECENTS@@					<control type="button" id="93079"><width min="96" max="400">auto</width><height>52</height><label>$LOCALIZE[192]</label>
					<font>hm_ui_24</font><align>center</align><aligny>center</aligny><textoffsetx>26</textoffsetx>
					<textcolor>b3ffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor>
					<texturenofocus border="26" colordiffuse="66ffffff">fg/e26.png</texturenofocus><texturefocus border="26" colordiffuse="ffffffff">fg/r26.png</texturefocus>
					<onclick>RunScript(script.aeon.helper,search,clear)</onclick><onclick>SetFocus(9381)</onclick><onup>9381</onup><ondown>9000</ondown><onback>9000</onback></control>
			</control>
		</control>
		<control type="group">
			<include>Aeon_LowSubSlide</include>
			<visible>$EXP[Aeon_H_SearchSec] + !$EXP[Aeon_H_SpotAny] + @@HASRECENT@@ + @@ON@@</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<control type="group">
				<include>Aeon_LowSubZoom</include>
				<control type="grouplist" id="9383">
					<left>112</left><top>778</top><width>1500</width><height>44</height>
					<orientation>horizontal</orientation><itemgap>6</itemgap>
					<onup>9000</onup>
@@TABS@@				</control>
@@LISTS@@			</control>
		</control>
	</include>
'''
home = (HOME_BODY.replace('@@ON@@', ON_SEARCH).replace('@@HASRECENT@@', HAS_RECENT).replace('@@CAPTION@@', A % 32516)
        .replace('@@PLACEHOLDER@@', A % 32517).replace('@@RECENTS@@', ''.join(recent(n) for n in range(1, 9)))
        .replace('@@TABS@@', ''.join(home_tab(*t) for t in HOME_TABS)).replace('@@LISTS@@', HOME_LISTS))

BODY = ('\t<!-- FG_SEARCH:begin (written by _src/fg_search.py) ======================== Search, Fused Glass (0.42.0) -->\n' +
        VARS + INK_VARS + HOME_VARS + window + home + '\t<!-- FG_SEARCH:end -->\n')

t = io.open(FUSED, encoding='utf-8').read()
t = re.sub(r'\t<!-- FG_SEARCH:begin.*?<!-- FG_SEARCH:end -->\n', '', t, flags=re.S)
if 'Aeon_H_SearchRecent_Classic' not in t:
    a = '\t<include name="Aeon_H_SearchRecent">\n'
    assert t.count(a) == 1
    t = t.replace(a, '\t<include name="Aeon_H_SearchRecent">\n'
                     '\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_H_SearchPage</include>\n'
                     '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">Aeon_H_SearchRecent_Classic</include>\n'
                     '\t</include>\n'
                     '\t<include name="Aeon_H_SearchRecent_Classic">\n')
t = t.replace('</includes>', BODY + '</includes>')
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)

# the classic window's controls become Search_WindowClassic; the window picks a variant at load time
w = io.open(WINDOW, encoding='utf-8').read()
if 'Search_WindowClassic' not in w:
    found = re.search(r'(\t<controls>\n)(.*?)(\t</controls>)', w, re.S)
    classic = found.group(2)
    w = w[:found.start(2)] + ('\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_SearchWindow</include>\n'
                              '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">Search_WindowClassic</include>\n') + w[found.end(2):]
    w = w.replace('\t<onunload>ClearProperty(Aeon.Search.Encoded,home)</onunload>\n',
                  '\t<onunload>ClearProperty(Aeon.Search.Encoded,home)</onunload>\n'
                  '\t<!-- Fused Glass (0.42.0): the query lives in aeon.q; a fresh window starts empty unless the helper opened it\n'
                  '\t     with a recent search (aeon.q.keep) -->\n'
                  '\t<onload condition="Skin.HasSetting(aeon.fglass) + String.IsEmpty(Window(Home).Property(aeon.q.keep))">ClearProperty(aeon.q,home)</onload>\n'
                  '\t<onload>ClearProperty(aeon.q.keep,home)</onload>\n')
    io.open(WINDOW, 'w', encoding='utf-8', newline='\n').write(w)
    s = io.open(SEARCH, encoding='utf-8').read()
    s = s.replace('</includes>', '\t<!-- the window\'s controls outside Fused Glass (Custom_1150 picks FG_SearchWindow there; 0.42.0) -->\n'
                                 '\t<include name="Search_WindowClassic">\n' + classic.replace('\n\t\t', '\n\t\t') + '\t</include>\n</includes>')
    io.open(SEARCH, 'w', encoding='utf-8', newline='\n').write(s)

h = io.open(HOME, encoding='utf-8').read()
old = '<ondown condition="$EXP[Aeon_H_SearchRecent] + !$EXP[Aeon_H_SpotAny]">SetFocus(9307)</ondown>'
if old in h:
    h = h.replace(old, '<ondown condition="$EXP[Aeon_H_SearchRecent] + !$EXP[Aeon_H_SpotAny] + !Skin.HasSetting(aeon.fglass)">SetFocus(9307)</ondown>'
                       '<ondown condition="$EXP[Aeon_H_SearchRecent] + !$EXP[Aeon_H_SpotAny] + Skin.HasSetting(aeon.fglass) + String.IsEmpty(Window(Home).Property(aeon.searchtab))">SetFocus(9384)</ondown>'
                       '<ondown condition="$EXP[Aeon_H_SearchRecent] + !$EXP[Aeon_H_SpotAny] + Skin.HasSetting(aeon.fglass) + String.IsEqual(Window(Home).Property(aeon.searchtab),tmdb)">SetFocus(9385)</ondown>'
                       '<ondown condition="$EXP[Aeon_H_SearchRecent] + !$EXP[Aeon_H_SpotAny] + Skin.HasSetting(aeon.fglass) + String.IsEqual(Window(Home).Property(aeon.searchtab),yt)">SetFocus(9386)</ondown>')
fallback = '<onup condition="!$EXP[Aeon_H_LiveTV] + !$EXP[Aeon_H_RowSec] + !$EXP[Aeon_H_PowerSec] + '
if 'SetFocus(9381)' not in h:
    assert h.count(fallback) == 1
    h = h.replace(fallback, '<onup condition="$EXP[Aeon_H_SearchSec] + Skin.HasSetting(aeon.fglass) + %s">SetFocus(9307)</onup>'
                            '<onup condition="$EXP[Aeon_H_SearchSec] + Skin.HasSetting(aeon.fglass) + !%s">SetFocus(9381)</onup>\n\t\t\t' % (HAS_RECENT, HAS_RECENT)
                  + fallback + '![$EXP[Aeon_H_SearchSec] + Skin.HasSetting(aeon.fglass)] + ')
io.open(HOME, 'w', encoding='utf-8', newline='\n').write(h)
import xml.etree.ElementTree as ET
for f in (FUSED, SEARCH, WINDOW, HOME):
    ET.parse(f)
print('ok')
