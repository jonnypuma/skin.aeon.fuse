"""0.42.0 Fused Glass Home > System (mockup board Main): writes include FG_H_SystemPage into 1080i/Includes_Fused.xml
(between FG_SYSTEM markers), puts it in the Home window (Fused Glass only, at load time), hides the old four panels in
Fused Glass and points Down from the System item at the tile row. Run from the skin folder.

Above the menu three cards: This box (Kodi version, OS and device, skin, screen, how long Kodi and the box have run),
Health (memory ring, processor bar, memory in use, CPU / GPU temperature, a status pill "All good" / "Running warm" /
"Memory almost full") and Library (films, shows, episodes with watched counts, songs, albums, artists). Under the menu
three tabs (9345: Shortcuts, Recently used add-ons, Library jobs) over a row of tiles (9343 / 9344 / 9346). The helper
(0.3.73) publishes aeon.sys.*, aeon.mem.*, aeon.cpu.pct, aeon.health and aeon.countg.* (numbers with separators)."""
import io
import re

FUSED = '1080i/Includes_Fused.xml'
HOME = '1080i/Includes_Aeon_Home.xml'
A = '$ADDON[skin.aeon.fuse %d]'
TAB = 'Window(Home).Property(aeon.systab)'
LISTS = (('', 9343, 93451), ('addons', 9344, 93452), ('jobs', 9346, 93453))   # tab property, list, tab button


def tab_is(value):
    return 'String.IsEmpty(%s)' % TAB if not value else 'String.IsEqual(%s,%s)' % (TAB, value)


def card(x, body):
    return '''			<control type="group">
				<left>%d</left><top>120</top>
				<control type="image"><left>-40</left><top>-40</top><width>628</width><height>536</height><texture border="68" colordiffuse="59000000">fg/sh28.png</texture></control>
				<control type="image"><left>0</left><top>0</top><width>548</width><height>456</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture></control>
				<control type="image"><left>0</left><top>0</top><width>548</width><height>456</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture></control>
%s			</control>
''' % (x, body)


def lbl(left, top, width, height, font, color, label, align='left', extra=''):
    return ('\t\t\t\t<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><align>%s</align>'
            '<aligny>center</aligny><font>%s</font><textcolor>%s</textcolor><label>%s</label>%s</control>\n'
            % (left, top, width, height, align, font, color, label, extra))


def row(top, label, value):
    return (lbl(34, top, 250, 34, 'hm_ui_22', 'b3ffffff', label) +
            lbl(214, top, 300, 34, 'hm_ui_22_semibold', 'ffffffff', value, 'right'))


THIS_BOX = (lbl(34, 26, 480, 36, 'hm_cap_20', 'b3ffffff', '[UPPERCASE]%s[/UPPERCASE]' % (A % 31269)) +
            lbl(30, 58, 488, 84, 'hm_aeon_title_66', 'ffffffff', '$VAR[FG_SysKodi]') +
            lbl(34, 146, 480, 34, 'hm_ui_24', 'f2ffffff', '$VAR[FG_SysLine]') +
            lbl(34, 182, 480, 30, 'hm_small_20', '99ffffff', '$VAR[FG_SysOS]') +
            row(256, A % 31649, 'Aeon Fuse $INFO[System.AddonVersion(skin.aeon.fuse)]') +
            row(290, A % 31651, '$VAR[FG_SysScreen]') +
            row(324, A % 31796, '$INFO[Network.IPAddress]') +
            row(358, A % 32489, '$VAR[Aeon_Uptime]') +
            row(392, A % 32490, '$INFO[Window(Home).Property(aeon.boxuptime)]').replace(
                '</control>\n', '<visible>!String.IsEmpty(Window(Home).Property(aeon.boxuptime))</visible></control>\n'))

TEMP_TILE = '''				<control type="group">
					<left>%(x)d</left><top>262</top>
					<visible>!String.IsEmpty(%(info)s)</visible>
					<control type="image"><left>0</left><top>0</top><width>232</width><height>90</height><texture border="16" colordiffuse="17ffffff">fg/r16.png</texture></control>
					<control type="label"><left>20</left><top>12</top><width>200</width><height>26</height><aligny>center</aligny><font>hm_cap_16</font><textcolor>b3ffffff</textcolor><label>%(name)s</label></control>
					<control type="label"><left>20</left><top>38</top><width>200</width><height>42</height><aligny>center</aligny><font>hm_serif_32</font><textcolor>ffffffff</textcolor><label>$INFO[%(info)s]</label></control>
				</control>
'''
HEALTH = (lbl(34, 26, 300, 36, 'hm_cap_20', 'b3ffffff', '[UPPERCASE]%s[/UPPERCASE]' % (A % 32502)) +
          '''				<control type="grouplist">
					<left>34</left><top>28</top><width>480</width><height>32</height>
					<orientation>horizontal</orientation><align>right</align><usecontrolcoords>true</usecontrolcoords>
					<visible>!String.IsEmpty(Window(Home).Property(aeon.health))</visible>
					<control type="button"><width min="40" max="480">auto</width><height>32</height><textoffsetx>14</textoffsetx><aligny>center</aligny><font>hm_small_20_bold</font><textcolor>ffffffff</textcolor><focusedcolor>ffffffff</focusedcolor><label>$VAR[FG_SysStatus]</label><texturenofocus border="16" colordiffuse="fg_sel">fg/r16.png</texturenofocus><texturefocus border="16" colordiffuse="fg_sel">fg/r16.png</texturefocus></control>
				</control>
				<control type="image"><left>32</left><top>92</top><width>144</width><height>144</height><texture colordiffuse="26ffffff">fg/mring/track.png</texture></control>
				<control type="image"><left>32</left><top>92</top><width>144</width><height>144</height><texture colordiffuse="ffffffff">fg/mring/$INFO[Window(Home).Property(aeon.mem.pct)].png</texture><visible>!String.IsEmpty(Window(Home).Property(aeon.mem.pct))</visible></control>
''' + lbl(32, 132, 144, 44, 'hm_font36_title', 'ffffffff', '$VAR[FG_SysMemPct]', 'center') +
          lbl(32, 172, 144, 24, 'hm_cap_16', '99ffffff', A % 32377, 'center') +
          lbl(204, 126, 200, 32, 'hm_ui_22', 'e6ffffff', A % 32506) +
          lbl(334, 126, 180, 32, 'hm_ui_22_semibold', 'ffffffff', '$VAR[FG_SysCpu]', 'right') +
          '''				<control type="progress"><left>204</left><top>164</top><width>310</width><height>6</height><texturebg border="3,0,3,0" colordiffuse="26ffffff">fg/pillh.png</texturebg><midtexture border="3,0,3,0" colordiffuse="ffffffff">fg/pillh.png</midtexture><info>System.CPUUsage</info></control>
''' + lbl(204, 180, 310, 30, 'hm_small_20', '99ffffff', '$INFO[Window(Home).Property(aeon.mem.text)]') +
          TEMP_TILE % {'x': 34, 'info': 'System.CPUTemperature', 'name': 'CPU'} +
          TEMP_TILE % {'x': 282, 'info': 'System.GPUTemperature', 'name': 'GPU'})


def lib(col, top, count, caption):
    x, width = (34, 262) if col == 0 else (300, 214)
    return (lbl(x, top, width, 56, 'hm_font45', 'ffffffff', '$INFO[Window(Home).Property(aeon.countg.%s)]' % count) +
            lbl(x, top + 54, width, 28, 'hm_small_20', 'b3ffffff', caption))


def watched(name, label):
    return '%s$INFO[Window(Home).Property(aeon.countg.%s.watched), · , %s]' % (label, name, A % 32286)


LIBRARY = (lbl(34, 26, 480, 36, 'hm_cap_20', 'b3ffffff', '[UPPERCASE]%s[/UPPERCASE]' % (A % 31204)) +
           lib(0, 70, 'movies', watched('movies', A % 31331)) +
           lib(1, 70, 'tvshows', watched('tvshows', A % 31332)) +
           lib(0, 176, 'episodes', watched('episodes', A % 31314)) +
           lib(1, 176, 'songs', A % 31343) +
           lib(0, 282, 'albums', A % 31299) +
           lib(1, 282, 'artists', A % 31298))

SHORTCUTS = [  # label, icon, action, visible
    ('$LOCALIZE[5]', 'aeon/icons/settings.png', 'ActivateWindow(settings)', ''),
    ('$LOCALIZE[20077]', 'common/aeon_mi_palette.png', 'ActivateWindow(skinsettings)', ''),
    ('$LOCALIZE[24001]', 'common/aeon_mi_box.png', 'ActivateWindow(addonbrowser)', ''),
    ('$LOCALIZE[7]', 'common/aeon_mi_folder.png', 'ActivateWindow(filemanager)', ''),
    ('$LOCALIZE[14111]', 'common/aeon_mi_log.png', 'ActivateWindow(eventlog)', ''),
    ('$LOCALIZE[10007]', 'common/aeon_mi_info.png', 'ActivateWindow(systeminfo)', ''),
    ('$LOCALIZE[13200]', 'common/aeon_mi_person.png', 'ActivateWindow(profiles)', 'Integer.IsGreater(System.ProfileCount,1)'),
]
JOBS = [
    (A % 31203, '$LOCALIZE[3]', 'common/aeon_ic_refresh.png', 'RunScript(script.aeon.helper,lib,update,video)'),
    (A % 31205, '$LOCALIZE[3]', 'common/aeon_ic_clean.png', 'RunScript(script.aeon.helper,lib,clean,video)'),
    (A % 31203, '$LOCALIZE[2]', 'common/aeon_ic_refresh.png', 'RunScript(script.aeon.helper,lib,update,music)'),
    (A % 31205, '$LOCALIZE[2]', 'common/aeon_ic_clean.png', 'RunScript(script.aeon.helper,lib,clean,music)'),
]


def items_static():
    out = {}
    s = ''
    for label, icon, action, vis in SHORTCUTS:
        s += ('\t\t\t\t\t\t<item><label>%s</label><icon>%s</icon><onclick>%s</onclick>%s</item>\n'
              % (label, icon, action, '<visible>%s</visible>' % vis if vis else ''))
    out[9343] = s
    s = ''
    for label, label2, icon, action in JOBS:
        s += '\t\t\t\t\t\t<item><label>%s</label><label2>%s</label2><icon>%s</icon><onclick>%s</onclick></item>\n' % (label, label2, icon, action)
    out[9346] = s
    return out


def tile_layout(ident, focused):
    """186 x 186 tiles at a 208 px pitch. Glyph icons (shortcuts, jobs) turn to the focus ink; add-on icons keep their
    colours in a rounded 72 px mask."""
    addon = ident == 9344
    if addon:
        icon = ('<control type="image"><left>57</left><top>26</top><width>72</width><height>72</height><aspectratio scalediffuse="false">scale</aspectratio>'
                '<texture background="true" diffuse="fg/m72x72.png">$INFO[ListItem.Icon]</texture></control>')
    else:
        icon = ('<control type="image"><left>69</left><top>36</top><width>48</width><height>48</height><aspectratio>keep</aspectratio>'
                '<texture colordiffuse="%s">$INFO[ListItem.Icon]</texture></control>')
    jobs = ident == 9346
    def texts(ink, ink2):
        if jobs:
            return ('<control type="label"><left>12</left><top>96</top><width>162</width><height>40</height><align>center</align><aligny>center</aligny>'
                    '<font>hm_ui_22_semibold</font><textcolor>%s</textcolor><label>$INFO[ListItem.Label]</label></control>'
                    '<control type="label"><left>12</left><top>134</top><width>162</width><height>28</height><align>center</align><aligny>center</aligny>'
                    '<font>hm_small_20</font><textcolor>%s</textcolor><label>$INFO[ListItem.Label2]</label></control>' % (ink, ink2))
        if addon:                        # add-on names can be long: one line, scrolling while the tile has focus
            return ('<control type="label"><left>14</left><top>112</top><width>158</width><height>40</height><align>center</align><aligny>center</aligny>'
                    '<font>hm_ui_22_semibold</font><textcolor>%s</textcolor><scroll>%s</scroll><label>$INFO[ListItem.Label]</label></control>'
                    % (ink, 'true' if ink != 'ffffffff' else 'false'))
        return ('<control type="textbox"><left>10</left><top>96</top><width>166</width><height>66</height><align>center</align><aligny>center</aligny>'
                '<font>hm_ui_22_semibold</font><textcolor>%s</textcolor><label>$INFO[ListItem.Label]</label></control>' % ink)
    plain = ('<control type="image"><left>0</left><top>0</top><width>186</width><height>186</height><texture border="24" colordiffuse="fg_frost">fg/r24.png</texture></control>'
             '<control type="image"><left>0</left><top>0</top><width>186</width><height>186</height><texture border="24" colordiffuse="fg_edge">fg/e24.png</texture></control>'
             + (icon if addon else icon % 'ffffffff') + texts('ffffffff', '99ffffff'))
    if not focused:
        return '\t\t\t\t\t\t' + plain + '\n'
    has = 'Control.HasFocus(%d)' % ident
    lit = ('<control type="image"><left>0</left><top>0</top><width>186</width><height>186</height><texture border="24" colordiffuse="ffffffff">fg/r24.png</texture><visible>!$EXP[FG_FocusLight]</visible></control>'
           '<control type="image"><left>0</left><top>0</top><width>186</width><height>186</height><texture border="24" colordiffuse="4dffffff">fg/r24.png</texture><visible>$EXP[FG_FocusLight]</visible></control>'
           '<control type="image"><left>0</left><top>0</top><width>186</width><height>186</height><texture border="24" colordiffuse="ffffffff">fg/e24.png</texture><visible>$EXP[FG_FocusLight]</visible></control>'
           + (icon if addon else icon % '$VAR[Aeon_OnBarInk]') + texts('$VAR[Aeon_OnBarInk]', '$VAR[Aeon_OnBarInk]'))
    return ('\t\t\t\t\t\t<control type="group"><visible>!%s</visible>%s</control>\n'
            '\t\t\t\t\t\t<control type="group"><visible>%s</visible><include>FG_LandFocus</include>%s</control>\n' % (has, plain, has, lit))


def tile_list(value, ident, button):
    statics = items_static()
    if ident == 9344:
        content = '<content target="programs" sortby="lastused" sortorder="descending" limit="14">addons://sources/executable/</content>'
    else:
        content = '<content>\n%s\t\t\t\t\t</content>' % statics[ident]
    return '''				<control type="list" id="%(id)d">
					<left>120</left><top>846</top><width>1664</width><height>200</height>
					<orientation>horizontal</orientation>
					<scrolltime tween="cubic" easing="out">220</scrolltime>
					<visible>%(vis)s</visible>
					<onup>SetFocus(%(btn)d)</onup>
					<ondown>noop</ondown>
					<onback>9000</onback>
					<itemlayout width="208" height="200">
%(item)s					</itemlayout>
					<focusedlayout width="208" height="200">
%(focus)s					</focusedlayout>
					%(content)s
				</control>
''' % {'id': ident, 'vis': tab_is(value), 'btn': button, 'item': tile_layout(ident, False), 'focus': tile_layout(ident, True), 'content': content}


def tab_button(value, ident, button, label):
    downs = '<ondown>SetFocus(%d)</ondown>' % ident
    return ('\t\t\t\t\t<control type="button" id="%d"><width min="60" max="600">auto</width><height>44</height><label>%s</label>'
            '<font>hm_ui_22_semibold</font><align>center</align><aligny>center</aligny><textoffsetx>22</textoffsetx>'
            '<textcolor>$VAR[FG_SysTabInk%d]</textcolor><focusedcolor>$VAR[Aeon_OnBarInk]</focusedcolor>'
            '<texturenofocus border="22" colordiffuse="$VAR[FG_SysTabBg%d]">fg/r22.png</texturenofocus>'
            '<texturefocus border="22" colordiffuse="$VAR[FG_SysTabFocus]">fg/r22.png</texturefocus>'
            '<onfocus>%s</onfocus>%s<onup>9000</onup><onback>9000</onback></control>\n'
            % (button, label, button, button, ('SetProperty(aeon.systab,%s,home)' % value) if value else 'ClearProperty(aeon.systab,home)', downs))


TABS = [('', 9343, 93451, A % 32507), ('addons', 9344, 93452, A % 32508), ('jobs', 9346, 93453, A % 32509)]
TAB_VARS = ''.join('''	<variable name="FG_SysTabBg%(b)d">
		<value condition="%(sel)s">fg_sel</value>
		<value>00ffffff</value>
	</variable>
	<variable name="FG_SysTabInk%(b)d">
		<value condition="%(sel)s">ffffffff</value>
		<value>99ffffff</value>
	</variable>
''' % {'b': b, 'sel': tab_is(v)} for v, i, b, l in TABS)

FOCUSED = '[Control.HasFocus(9000) | ControlGroup(9345).HasFocus() | Control.HasFocus(9343) | Control.HasFocus(9344) | Control.HasFocus(9346)]'
BODY = '''	<!-- FG_SYSTEM:begin (written by _src/fg_home_system.py) ===================== Home > System, Fused Glass (0.42.0)
	     Three cards over the System picture: This box, Health (memory ring, processor, temperatures, status pill) and
	     Library. Under the menu the tabs Shortcuts / Recently used add-ons / Library jobs (9345) over a row of tiles
	     (9343 / 9344 / 9346); Down from the System item reaches the row, Up from the row the tabs. -->
	<variable name="FG_SysKodi">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.sys.major))">Kodi $INFO[Window(Home).Property(aeon.sys.major)]</value>
		<value>Kodi $INFO[System.BuildVersionShort]</value>
	</variable>
	<variable name="FG_SysLine">
		<value>$INFO[System.BuildVersionShort]$INFO[Window(Home).Property(aeon.sys.osname),  ·  ,]$INFO[Window(Home).Property(aeon.sys.device),  ·  ,]</value>
	</variable>
	<variable name="FG_SysOS">
		<value>$INFO[Window(Home).Property(aeon.sys.osline)]</value>
	</variable>
	<variable name="FG_SysScreen">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.sys.screen))">$INFO[Window(Home).Property(aeon.sys.screen)]</value>
		<value>$INFO[System.ScreenResolution]</value>
	</variable>
	<variable name="FG_SysMemPct">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.mem.pct))">$INFO[Window(Home).Property(aeon.mem.pct)]%%</value>
		<value>$INFO[System.Memory(used.percent)]</value>
	</variable>
	<variable name="FG_SysCpu">
		<value condition="!String.IsEmpty(Window(Home).Property(aeon.cpu.pct))">$INFO[Window(Home).Property(aeon.cpu.pct)]%%</value>
	</variable>
	<variable name="FG_SysStatus">
		<value condition="String.IsEqual(Window(Home).Property(aeon.health),memory)">[COLOR ffe5484d]●[/COLOR]  %(mem)s</value>
		<value condition="String.IsEqual(Window(Home).Property(aeon.health),warm)">[COLOR fff5a524]●[/COLOR]  %(warm)s</value>
		<value>[COLOR ff4ade80]●[/COLOR]  %(good)s</value>
	</variable>
	<variable name="FG_SysTabFocus">
		<value condition="$EXP[FG_FocusLight]">4dffffff</value>
		<value>ffffffff</value>
	</variable>
%(tabvars)s	<include name="FG_H_SystemPage">
		<control type="group">
			<include>Aeon_LowBand</include>
			<visible>$EXP[Aeon_H_SystemSec] + %(focused)s</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/><effect type="slide" start="0,24" end="0,0" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
%(cards)s		</control>
		<control type="group">
			<include>Aeon_LowSubSlide</include>
			<visible>$EXP[Aeon_H_SystemSec] + %(focused)s</visible>
			<animation type="Visible" tween="cubic" easing="out" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" delay="200" time="300"/></animation>
			<animation type="Hidden"><effect type="fade" start="100" end="0" time="150"/></animation>
			<control type="group">
				<include>Aeon_LowSubZoom</include>
				<control type="grouplist" id="9345">
					<left>112</left><top>786</top><width>1400</width><height>44</height>
					<orientation>horizontal</orientation><itemgap>6</itemgap>
					<onup>9000</onup>
%(tabs)s				</control>
%(lists)s			</control>
		</control>
	</include>
	<!-- FG_SYSTEM:end -->
''' % {'mem': A % 32505, 'warm': A % 32504, 'good': A % 32503, 'tabvars': TAB_VARS, 'focused': FOCUSED,
       'cards': card(120, THIS_BOX) + card(698, HEALTH) + card(1276, LIBRARY),
       'tabs': ''.join(tab_button(v, i, b, l) for v, i, b, l in TABS),
       'lists': ''.join(tile_list(v, i, b) for v, i, b, l in TABS)}

t = io.open(FUSED, encoding='utf-8').read()
t = re.sub(r'\t<!-- FG_SYSTEM:begin.*?<!-- FG_SYSTEM:end -->\n', '', t, flags=re.S)
t = t.replace('</includes>', BODY + '</includes>')
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)

h = io.open(HOME, encoding='utf-8').read()
# the page itself (Fused Glass only, chosen at load time)
a = '\t\t<include>Aeon_H_PowerPage</include>\n'
if 'FG_H_SystemPage' not in h:
    assert h.count(a) == 1
    h = h.replace(a, a + '\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_H_SystemPage</include>\n')
# the old four panels: not in Fused Glass
old = '<visible>String.IsEqual(Container(9000).ListItem.Label2,system) + Control.HasFocus(9000)</visible>'
if old in h:
    h = h.replace(old, '<visible>String.IsEqual(Container(9000).ListItem.Label2,system) + Control.HasFocus(9000) + !Skin.HasSetting(aeon.fglass)</visible>')
# Down from the System item: the tiles of the open tab (Fused Glass)
down = '<ondown condition="$EXP[Aeon_H_FavSec] + !$EXP[Aeon_H_SpotAny]">SetFocus(9309)</ondown>'
if 'SetFocus(9343)' not in h:
    assert h.count(down) == 1
    sysdown = ''.join('<ondown condition="$EXP[Aeon_H_SystemSec] + Skin.HasSetting(aeon.fglass) + %s">SetFocus(%d)</ondown>' % (tab_is(v), i)
                      for v, i, b, l in TABS)
    h = h.replace(down, down + '\n\t\t\t' + sysdown)
    # and the general Down (to the rows) leaves the System item alone in Fused Glass
    gen = '<ondown condition="$EXP[Aeon_H_Other] + !$EXP[Aeon_H_SpotAny] + '
    assert h.count(gen) == 1
    h = h.replace(gen, gen + '![$EXP[Aeon_H_SystemSec] + Skin.HasSetting(aeon.fglass)] + ')
io.open(HOME, 'w', encoding='utf-8', newline='\n').write(h)
import xml.etree.ElementTree as ET
ET.parse(FUSED); ET.parse(HOME)
print('ok')
