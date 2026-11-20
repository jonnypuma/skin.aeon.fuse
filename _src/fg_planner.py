"""0.43.0 Fused Glass Planner (mockup boards PlannerWeek and PlannerStrip). Run from the skin folder.

Custom_1168_Planner.xml keeps its Day view; its header / options row and its Week view move into Includes_Planner.xml
(Planner_TopClassic, Planner_WeekClassic) and the window picks them or the Fused Glass parts at load time:
  FG_PlannerTop    background (Colors = KarmaMole's colour picture of the title in focus, Neutral, Fanart;
                   Skin.String(aeon.planner.bg)), PLANNER · week caption, the headline (Next 7 days / This week ...)
                   and the pills (9400): Shows you watch, View, Show, View settings
  FG_PlannerWeek   seven glass day cards (lists 9511-9517 as before), the selected day lighter, a yellow ring on the
                   title in focus with "You're on S3 E1" when you are behind on that show
  FG_PlannerStrip  the View settings strip (9450): View, Show, Shows you watch, Background, Week starts, Update every,
                   Update now, Home spotlight, with a help box
The helper (plannerwin.py 0.3.74) publishes aeon.planner.headline / watching / watchname / bgname / summary.
0.46.3 (plannerwin.py 0.3.78, aeon.planner.busy): each day card says Loading (spinner, string 31952) while its list
loads (the list fades out meanwhile: Kodi keeps showing the old week's items until the new ones are in) or, when
empty, while the helper fills the lists; "Nothing out" only after that; Down from the pills reaches an empty or loading day
list through the helper; the holding button 9518 of the Week view. The Day view's part: _src/pl_loading_0463.py.
Run _src/fg_material.py after this script."""
import io
import re

WINDOW = '1080i/Custom_1168_Planner.xml'
PLAN = '1080i/Includes_Planner.xml'
INCLUDES = '1080i/Includes.xml'
FUSED = '1080i/Includes_Fused.xml'
VIEWS = '1080i/Includes_Aeon_Views3.xml'
A = '$ADDON[skin.aeon.fuse %d]'
P = 'Window(Home).Property(aeon.planner.%s)'
WEEK = 'String.IsEqual(%s,week)' % (P % 'mode')
DAY = 'String.IsEqual(%s,day)' % (P % 'mode')

# ------------------------------------------------------------------ move the classic parts into includes
w = io.open(WINDOW, encoding='utf-8').read()
if 'Planner_TopClassic' not in w:
    lines = w.split('\n')
    bg = next(i for i, l in enumerate(lines) if l.strip() == '<include>AG_Background</include>')
    day = next(i for i, l in enumerate(lines) if '<!-- ============================================================ Day -->' in l)
    week = next(i for i, l in enumerate(lines) if '<!-- ============================================================ Week -->' in l)
    strip = next(i for i, l in enumerate(lines) if l.strip().startswith('<!-- right strip'))
    top = lines[bg + 1:day]
    wk = lines[week:strip]
    while top and not top[-1].strip():
        top.pop()
    while wk and not wk[-1].strip():
        wk.pop()
    new = (lines[:bg + 1] +
           ['\t\t<!-- header and options / Week view: Fused Glass or the classic ones (Includes_Planner.xml), chosen at load (0.43.0) -->',
            '\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_PlannerTop</include>',
            '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">Planner_TopClassic</include>', ''] +
           lines[day:week] +
           ['\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_PlannerWeek</include>',
            '\t\t<include condition="!Skin.HasSetting(aeon.fglass)">Planner_WeekClassic</include>', ''] +
           lines[strip:])
    w = '\n'.join(new)
    # the strip goes on top of everything, Fused Glass only
    w = w.replace('\t</controls>\n</window>', '\t\t<include condition="Skin.HasSetting(aeon.fglass)">FG_PlannerStrip</include>\n\t</controls>\n</window>')
    w = w.replace('\t<onload>RunScript(script.aeon.helper,planner,init)</onload>\n',
                  '\t<onload>RunScript(script.aeon.helper,planner,init)</onload>\n\t<onunload>ClearProperty(aeon.planner.strip,home)</onunload>\n')
    io.open(WINDOW, 'w', encoding='utf-8', newline='\n').write(w)
    inc = ('<?xml version="1.0" encoding="UTF-8"?>\n<!-- The Planner window\'s header / options and Week view outside Fused Glass (moved out of\n'
           '     Custom_1168_Planner.xml in 0.43.0; Fused Glass draws FG_PlannerTop / FG_PlannerWeek, _src/fg_planner.py). -->\n<includes>\n'
           '\t<include name="Planner_TopClassic">\n' + '\n'.join(top) + '\n\t</include>\n'
           '\t<include name="Planner_WeekClassic">\n' + '\n'.join(wk) + '\n\t</include>\n</includes>\n')
    io.open(PLAN, 'w', encoding='utf-8', newline='\n').write(inc)
    i = io.open(INCLUDES, encoding='utf-8').read()
    if 'Includes_Planner.xml' not in i:
        i = i.replace('\t<include file="Includes_FusedPlayer.xml"/>\n', '\t<include file="Includes_FusedPlayer.xml"/>\n\t<include file="Includes_Planner.xml"/>\n')
        io.open(INCLUDES, 'w', encoding='utf-8', newline='\n').write(i)

# the lists reload when Shows you watch changes
v = io.open(VIEWS, encoding='utf-8').read()
stamp = '&amp;stamp=$INFO[Window(Home).Property(aeon.planner.updated)]'
if '&amp;w=$INFO[Window(Home).Property(aeon.planner.watching)]' not in v:
    v = v.replace(stamp, stamp + '&amp;w=$INFO[Window(Home).Property(aeon.planner.watching)]')
    io.open(VIEWS, 'w', encoding='utf-8', newline='\n').write(v)

# the classic Week view's slide animations (they follow aeon.planner.flip / dir)
anims = '\n'.join(l for l in io.open(PLAN, encoding='utf-8').read().split('\n')
                  if l.strip().startswith('<animation type="Conditional" reversible="false" condition="') and 'aeon.planner.flip' in l)
anims = anims.replace('aeon.planner.flip', 'aeon.planner.wflip')   # Fused Glass: only a new week slides in (0.45.1)

# ------------------------------------------------------------------ variables
fan = ''.join('\t\t<value condition="Control.HasFocus(%d)">$INFO[Container(%d).ListItem.Art(fanart)]</value>\n' % (9510 + n, 9510 + n) for n in range(1, 8))
fan += '\t\t<value condition="%s">$INFO[Container(9500).ListItem.Art(fanart)]</value>\n' % DAY
fan += ''.join('\t\t<value condition="!String.IsEmpty(%s)">$INFO[Container(%d).ListItem.Art(fanart)]</value>\n' % (P % ('c%d.sel' % n), 9510 + n) for n in range(1, 8))
ROWS = [  # id, icon, label, value, action, help
    (9451, 'aeon/icons/grid.png', '$LOCALIZE[31894]', '$VAR[Aeon_Pl_ViewName]', 'RunScript(script.aeon.helper,planner,view)', 32534),
    (9452, 'common/aeon_ic_filter.png', '$LOCALIZE[31896]', '$INFO[%s]' % (P % 'what'), 'RunScript(script.aeon.helper,planner,what)', 32535),
    (9453, 'aeon/icons/tv.png', A % 32525, '$INFO[%s]' % (P % 'watchname'), 'RunScript(script.aeon.helper,planner,watching)', 32536),
    (9454, 'aeon/icons/image.png', A % 32527, '$INFO[%s]' % (P % 'bgname'), 'RunScript(script.aeon.helper,planner,bg)', 32537),
    (9455, 'aeon/icons/clock.png', '$LOCALIZE[31895]', '$INFO[%s]' % (P % 'weekstart'), 'RunScript(script.aeon.helper,planner,weekstart)', 32538),
    (9459, 'aeon/icons/prev.png', A % 32552, '$INFO[%s]' % (P % 'pastname'), 'RunScript(script.aeon.helper,planner,past)', 32553),
    (9456, 'common/aeon_ic_refresh.png', A % 32028, '$INFO[%s]' % (P % 'refreshname'), 'RunScript(script.aeon.helper,planner,refresh)', 0),
    (9457, 'common/aeon_ic_refresh.png', A % 32029, '$INFO[%s]' % (P % 'updated'), 'RunScript(script.aeon.helper,planner,update)', 0),
    (9458, 'aeon/icons/home.png', '$LOCALIZE[31899]', '', 'ActivateWindow(1169)', 0),
]
helpv = ''.join('\t\t<value condition="Control.HasFocus(%d)">%s</value>\n' % (r[0], A % r[5]) for r in ROWS if r[5])
helpcap = ''.join('\t\t<value condition="Control.HasFocus(%d)">%s</value>\n' % (r[0], r[2]) for r in ROWS if r[5])
VARS = ('\t<variable name="FG_PlFanart">\n' + fan + '\t</variable>\n'
        '\t<variable name="FG_PlWatchLabel">\n'
        '\t\t<value condition="!String.IsEmpty(%s)">[COLOR fg_mark]●[/COLOR]  %s</value>\n'
        '\t\t<value>[COLOR 59ffffff]●[/COLOR]  %s</value>\n\t</variable>\n' % (P % 'watching', A % 32525, A % 32525) +
        '\t<variable name="FG_PlCaps">\n'
        '\t\t<value condition="String.IsEqual(ListItem.Property(kind),movie)">[UPPERCASE]$LOCALIZE[20338][/UPPERCASE]</value>\n'
        '\t\t<value condition="String.IsEqual(ListItem.Property(kind),album)">[UPPERCASE]$INFO[ListItem.Label2][/UPPERCASE]</value>\n'
        '\t\t<value>[UPPERCASE]$INFO[ListItem.TVShowTitle]$INFO[ListItem.Season, · S,]$INFO[ListItem.Episode, E,][/UPPERCASE]</value>\n\t</variable>\n'
        '\t<variable name="FG_PlTitle">\n'
        '\t\t<value condition="!String.IsEmpty(ListItem.Property(aeon.eptitle))">$INFO[ListItem.Property(aeon.eptitle)]</value>\n'
        '\t\t<value>$INFO[ListItem.Label]</value>\n\t</variable>\n'
        '\t<variable name="FG_PlStripHelp">\n' + helpv + '\t</variable>\n'
        '\t<variable name="FG_PlStripHelpCap">\n' + helpcap + '\t</variable>\n'
        '\t<variable name="FG_PlCaption">\n'
        '\t\t<value condition="%s">[UPPERCASE]$LOCALIZE[31294] · $INFO[%s][/UPPERCASE]</value>\n'
        '\t\t<value>[UPPERCASE]$LOCALIZE[31294]$INFO[%s, · ,][/UPPERCASE]</value>\n\t</variable>\n' % (WEEK, P % 'weektitle', P % 'daydate') +
        '\t<variable name="FG_PlHeadline">\n'
        '\t\t<value condition="%s">$INFO[%s]</value>\n'
        '\t\t<value>$INFO[%s]</value>\n\t</variable>\n' % (WEEK, P % 'headline', P % 'dayname') +
        '\t<variable name="FG_PlCardArt">\n'
        '\t\t<value condition="!String.IsEmpty(ListItem.Art(thumb)) + !String.IsEqual(ListItem.Property(kind),movie)">$INFO[ListItem.Art(thumb)]</value>\n'
        '\t\t<value condition="!String.IsEmpty(ListItem.Art(landscape))">$INFO[ListItem.Art(landscape)]</value>\n'
        '\t\t<value condition="!String.IsEmpty(ListItem.Art(fanart))">$INFO[ListItem.Art(fanart)]</value>\n'
        '\t\t<value condition="!String.IsEmpty(ListItem.Art(tvshow.fanart))">$INFO[ListItem.Art(tvshow.fanart)]</value>\n'
        '\t\t<value condition="!String.IsEmpty(ListItem.Art(season.poster))">$INFO[ListItem.Art(season.poster)]</value>\n'
        '\t\t<value condition="!String.IsEmpty(ListItem.Art(poster))">$INFO[ListItem.Art(poster)]</value>\n'
        '\t\t<value>$INFO[ListItem.Art(tvshow.poster)]</value>\n\t</variable>\n')


BUSY = '!String.IsEmpty(%s)' % (P % 'busy')       # 0.46.3: the helper is filling the lists (plannerwin.py 0.3.78)
IDLE = 'String.IsEmpty(%s)' % (P % 'busy')
DAYEMPTY = '[Integer.IsEqual(Container(9500).NumItems,0) | Container(9500).IsUpdating]'


def pill(ident, label, actions, extra=''):
    # 0.46.3: Down goes straight to the day list only when it has items and is not loading; else the helper puts the
    # focus there once it has loaded, or on the holding button (9501) when the day is empty
    downs = ('<ondown condition="%s + !%s">9500</ondown><ondown condition="[%s + %s] | %s">RunScript(script.aeon.helper,planner,focus)</ondown>'
             % (DAY, DAYEMPTY, DAY, DAYEMPTY, WEEK))
    return ('\t\t\t\t<control type="button" id="%d"><width min="60" max="700">auto</width><height>44</height><label>%s</label>'
            '<font>hm_ui_22_semibold</font><align>center</align><aligny>center</aligny><textoffsetx>22</textoffsetx>'
            '<textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor>'
            '<texturenofocus border="22" colordiffuse="fg_sel">fg/r22.png</texturenofocus><texturefocus border="22" colordiffuse="ffffffff">fg/r22.png</texturefocus>'
            '%s%s<onup>noop</onup>%s</control>\n' % (ident, label, ''.join('<onclick>%s</onclick>' % a for a in actions), downs, extra))


TOP = '''	<include name="FG_PlannerTop">
		<!-- background: Colors (default) / Neutral (the plain ground of AG_Background) / Fanart -->
		<control type="group">
			<visible>String.IsEmpty(Skin.String(aeon.planner.bg))</visible>
			<control type="image"><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>500</fadetime><texture background="true" colordiffuse="b3ffffff">$VAR[FG_PlFanart]</texture><visible>String.IsEmpty(Window(Home).Property(Groove.Art.Soft))</visible></control>
			<control type="image"><width>1920</width><height>1080</height><aspectratio>stretch</aspectratio><fadetime>600</fadetime><texture background="true">$INFO[Window(Home).Property(aeon.blur)]</texture><visible>String.IsEmpty(Window(Home).Property(Groove.Art.Soft)) + !String.IsEmpty(Window(Home).Property(aeon.blur))</visible></control>
			<control type="image"><width>1920</width><height>1080</height><aspectratio>stretch</aspectratio><fadetime>600</fadetime><texture background="true">$INFO[Window(Home).Property(Groove.Art.Soft)]</texture><visible>!String.IsEmpty(Window(Home).Property(Groove.Art.Soft))</visible></control>
			<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="66000000">common/white.png</texture></control>
		</control>
		<control type="group">
			<visible>String.IsEqual(Skin.String(aeon.planner.bg),fanart)</visible>
			<control type="image"><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>500</fadetime><texture background="true">$VAR[FG_PlFanart]</texture></control>
			<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="99000000">common/white.png</texture></control>
		</control>
		<control type="label"><left>120</left><top>36</top><width>1000</width><height>32</height><aligny>center</aligny><font>hm_cap_20</font><textcolor>b3ffffff</textcolor><label>$VAR[FG_PlCaption]</label></control>
		<control type="label"><left>116</left><top>62</top><width>760</width><height>80</height><aligny>center</aligny><font>hm_aeon_title_66</font><textcolor>ffffffff</textcolor><label>$VAR[FG_PlHeadline]</label></control>
		<include>FG_ClockCapsule</include>
		<control type="grouplist" id="9400">
			<left>540</left><top>60</top><width>1010</width><height>48</height>
			<orientation>horizontal</orientation><align>right</align><itemgap>12</itemgap>
			<onleft>noop</onleft><onright>noop</onright>
@@PILLS@@		</control>
	</include>
'''
TOP = TOP.replace('@@PILLS@@',
                  pill(9405, '$VAR[FG_PlWatchLabel]', ['RunScript(script.aeon.helper,planner,watching)']) +
                  pill(9401, '$LOCALIZE[31894]: $VAR[Aeon_Pl_ViewName]', ['RunScript(script.aeon.helper,planner,view)']) +
                  pill(9403, '$LOCALIZE[31896]: $INFO[%s]' % (P % 'what'), ['RunScript(script.aeon.helper,planner,what)']) +
                  pill(9406, A % 32526, ['SetProperty(aeon.planner.strip,1,home)', 'SetFocus(9451)'],
                       '<onfocus>ClearProperty(aeon.planner.strip,home)</onfocus>'))


def item(n, focused):
    lid = 9510 + n
    movie = 'String.IsEqual(ListItem.Property(kind),movie)'
    body = ('<control type="image"><left>0</left><top>0</top><width>200</width><height>100</height><texture border="16" colordiffuse="1fffffff">fg/r16.png</texture></control>'
            '<control type="image"><left>0</left><top>0</top><width>200</width><height>100</height><aspectratio scalediffuse="false">scale</aspectratio><texture background="true" colordiffuse="47ffffff" diffuse="fg/m200x100.png">$VAR[FG_PlCardArt]</texture></control>'
            '<control type="image"><left>0</left><top>0</top><width>200</width><height>100</height><texture colordiffuse="66000000" diffuse="fg/m200x100.png">fg/scrim_l.png</texture></control>'
            '<control type="image"><left>10</left><top>17</top><width>44</width><height>66</height><aspectratio>keep</aspectratio><texture background="true">$INFO[ListItem.Art(poster)]</texture><visible>%s</visible></control>'
            '<control type="label"><left>14</left><top>8</top><width>176</width><height>22</height><aligny>center</aligny><font>hm_cap_14</font><textcolor>b3ffffff</textcolor><selectedcolor>b3ffffff</selectedcolor><label>$VAR[FG_PlCaps]</label><visible>!%s</visible></control>'
            '<control type="textbox"><left>14</left><top>30</top><width>176</width><height>48</height><font>hm_small_20_bold</font><textcolor>ffffffff</textcolor><label>$VAR[FG_PlTitle]</label><visible>!%s</visible></control>'
            '<control type="label"><left>64</left><top>14</top><width>126</width><height>22</height><aligny>center</aligny><font>hm_cap_14</font><textcolor>b3ffffff</textcolor><selectedcolor>b3ffffff</selectedcolor><label>$VAR[FG_PlCaps]</label><visible>%s</visible></control>'
            '<control type="textbox"><left>64</left><top>36</top><width>126</width><height>50</height><font>hm_small_20_bold</font><textcolor>ffffffff</textcolor><label>$INFO[ListItem.Label]</label><visible>%s</visible></control>'
            % (movie, movie, movie, movie, movie))
    if focused:
        body += ('<control type="image"><left>-3</left><top>-3</top><width>206</width><height>106</height><texture border="19" colordiffuse="fg_mark">fg/ring16.png</texture><visible>Control.HasFocus(%d)</visible></control>'
                 '<control type="label"><left>14</left><top>76</top><width>176</width><height>22</height><aligny>center</aligny><font>hm_small_20_bold</font><textcolor>fg_mark</textcolor><selectedcolor>fg_mark</selectedcolor><label>$INFO[ListItem.Property(aeon.pl.on)]</label><visible>Control.HasFocus(%d) + !String.IsEmpty(ListItem.Property(aeon.pl.on))</visible></control>'
                 % (lid, lid))
    return '<control type="group"><left>7</left><top>4</top>%s</control>' % body


def column(n):
    x = 120 + (n - 1) * 246
    c = lambda key: P % ('c%d.%s' % (n, key))
    lid = 9510 + n
    return '''			<control type="group">
				<left>%(x)d</left><top>170</top>
				<animation effect="fade" start="100" end="45" time="0" condition="!String.IsEmpty(%(past)s) + !Skin.HasSetting(aeon.planner.past)">Conditional</animation>
				<animation effect="fade" start="100" end="75" time="0" condition="!String.IsEmpty(%(past)s) + Skin.HasSetting(aeon.planner.past)">Conditional</animation>
				<control type="image"><left>0</left><top>0</top><width>230</width><height>860</height><texture border="28" colordiffuse="fg_frost">fg/r28.png</texture></control>
				<control type="image"><left>0</left><top>0</top><width>230</width><height>860</height><texture border="28" colordiffuse="24ffffff">fg/r28.png</texture><visible>!String.IsEmpty(%(sel)s)</visible></control>
				<control type="image"><left>0</left><top>0</top><width>230</width><height>860</height><texture border="28" colordiffuse="fg_edge">fg/e28.png</texture><visible>String.IsEmpty(%(sel)s)</visible></control>
				<control type="image"><left>0</left><top>0</top><width>230</width><height>860</height><texture border="28" colordiffuse="59ffffff">fg/e28.png</texture><visible>!String.IsEmpty(%(sel)s)</visible></control>
				<control type="label"><left>20</left><top>14</top><width>160</width><height>40</height><aligny>center</aligny><font>hm_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$INFO[%(name)s]</label><visible>String.IsEmpty(%(today)s)</visible></control>
				<control type="label"><left>20</left><top>14</top><width>160</width><height>40</height><aligny>center</aligny><font>hm_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[33006]</label><visible>!String.IsEmpty(%(today)s)</visible></control>
				<control type="label"><left>120</left><top>14</top><width>94</width><height>40</height><align>right</align><aligny>center</aligny><font>hm_small_20</font><textcolor>b3ffffff</textcolor><label>$INFO[%(day)s]</label><visible>String.IsEmpty(%(today)s)</visible></control>
				<control type="label"><left>120</left><top>14</top><width>94</width><height>40</height><align>right</align><aligny>center</aligny><font>hm_small_20</font><textcolor>b3ffffff</textcolor><label>$INFO[%(short)s]</label><visible>!String.IsEmpty(%(today)s)</visible></control>
				<control type="label"><left>20</left><top>58</top><width>190</width><height>34</height><aligny>center</aligny><font>hm_small_20</font><textcolor>99ffffff</textcolor><label>%(nothing)s</label><visible>String.IsEqual(%(count)s,0) + String.IsEmpty(%(past)s) + %(idle)s + !Container(%(lid)d).IsUpdating</visible></control>
				<control type="group"><left>20</left><top>58</top>
					<visible>[Container(%(lid)d).IsUpdating | [Integer.IsEqual(Container(%(lid)d).NumItems,0) + %(busy)s]] + [String.IsEmpty(%(past)s) | Skin.HasSetting(aeon.planner.past)]</visible>
					<animation type="Visible"><effect type="fade" start="0" end="100" delay="150" time="200"/></animation>
					<control type="image"><left>0</left><top>6</top><width>22</width><height>22</height><texture colordiffuse="b3ffffff">common/aeon_spinner.gif</texture><visible>!Skin.HasSetting(aeon.reducemotion)</visible></control>
					<control type="image"><left>0</left><top>6</top><width>22</width><height>22</height><texture colordiffuse="b3ffffff">common/aeon_spinner_still.png</texture><visible>Skin.HasSetting(aeon.reducemotion)</visible></control>
					<control type="label"><left>32</left><top>0</top><width>170</width><height>34</height><aligny>center</aligny><font>hm_small_20</font><textcolor>99ffffff</textcolor><label>$LOCALIZE[31952]</label></control>
				</control>
				<control type="list" id="%(lid)d">
					<left>8</left><top>58</top><width>214</width><height>796</height>
					<animation effect="fade" start="100" end="0" time="150" condition="Container(%(lid)d).IsUpdating">Conditional</animation>
					<orientation>vertical</orientation>
					<scrolltime tween="cubic" easing="out">200</scrolltime>
					<onleft>RunScript(script.aeon.helper,planner,left)</onleft>
					<onright>RunScript(script.aeon.helper,planner,right)</onright>
					<onup>9400</onup><ondown>noop</ondown><onclick>Action(Info)</onclick>
					<itemlayout width="214" height="112">%(item)s</itemlayout>
					<focusedlayout width="214" height="112">%(fitem)s</focusedlayout>
					<content target="videos">$VAR[Aeon_Pl_ColPath%(n)d]</content>
				</control>
			</control>
''' % {'x': x, 'past': c('past'), 'sel': c('sel'), 'name': c('name'), 'today': c('today'), 'num': c('num'), 'day': c('day'), 'short': c('short'), 'count': c('count'),
       'nothing': A % 32528, 'lid': lid, 'item': item(n, False), 'fitem': item(n, True), 'n': n, 'busy': BUSY, 'idle': IDLE}


# 0.46.3: the Week view's holding button (1 x 1, no texture): the helper parks the focus here while the lists of a new
# week load (a focused list that comes back empty hands the focus to the View pill), and leaves it here when the
# selected day's list is empty; Left / Right / Up work as on the lists
HOLD = ('\t\t\t<control type="button" id="9518"><left>120</left><top>170</top><width>1</width><height>1</height><texturefocus /><texturenofocus />'
        '<onleft>RunScript(script.aeon.helper,planner,left)</onleft><onright>RunScript(script.aeon.helper,planner,right)</onright>'
        '<onup>9400</onup><ondown>RunScript(script.aeon.helper,planner,focus)</ondown><onclick>noop</onclick></control>\n')
WEEKBODY = ('\t<include name="FG_PlannerWeek">\n\t\t<control type="group">\n\t\t\t<visible>%s</visible>\n' % WEEK +
            anims + '\n' + ''.join(column(n) for n in range(1, 8)) + HOLD + '\t\t</control>\n\t</include>\n')


def row(i, r):
    ident, icon, label, value, action, _help = r
    y = 132 + i * 66
    return (('\t\t\t\t<control type="button" id="%d"><width>448</width><height>64</height><label>%s</label><label2>%s</label2>'
             '<font>hm_ui_24_semibold</font><aligny>center</aligny><textoffsetx>56</textoffsetx>'
             '<textcolor>ffffffff</textcolor><focusedcolor>aeon_onbar</focusedcolor>'
             '<texturefocus border="16" colordiffuse="ffffffff">fg/r16.png</texturefocus><texturenofocus />'
             '<onclick>%s</onclick><onleft>noop</onleft>'
             '<onright>9406</onright><onback>9406</onback></control>\n') % (ident, label, value, action),
            ('\t\t\t<control type="image"><left>56</left><top>%d</top><width>24</width><height>24</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">%s</texture><visible>!Control.HasFocus(%d)</visible></control>\n'
             '\t\t\t<control type="image"><left>56</left><top>%d</top><width>24</width><height>24</height><aspectratio>keep</aspectratio><texture colordiffuse="aeon_onbar">%s</texture><visible>Control.HasFocus(%d)</visible></control>\n')
            % (y + 20, icon, ident, y + 20, icon, ident))


rows = [row(i, r) for i, r in enumerate(ROWS)]
STRIP = '''	<include name="FG_PlannerStrip">
		<control type="group">
			<visible>String.IsEqual(Window(Home).Property(aeon.planner.strip),1)</visible>
			<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="-480,0" end="0,0" time="220" tween="cubic" easing="out"/><effect type="fade" start="0" end="100" time="180"/></animation>
			<animation type="Hidden" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="slide" start="0,0" end="-480,0" time="180" tween="cubic" easing="in"/><effect type="fade" start="100" end="0" time="180"/></animation>
			<control type="image"><left>480</left><width>1440</width><height>1080</height><texture colordiffuse="99000000">common/white.png</texture></control>
			<control type="image"><left>24</left><top>24</top><width>480</width><height>1032</height><texture border="32" colordiffuse="f0121418">fg/r32.png</texture></control>
			<control type="image"><left>24</left><top>24</top><width>480</width><height>1032</height><texture border="32" colordiffuse="fg_edge">fg/e32.png</texture></control>
			<control type="image"><left>40</left><top>46</top><width>56</width><height>56</height><texture colordiffuse="1fffffff">fg/circle.png</texture></control>
			<control type="image"><left>56</left><top>62</top><width>24</width><height>24</height><aspectratio>keep</aspectratio><texture colordiffuse="ffffffff">aeon/icons/clock.png</texture></control>
			<control type="label"><left>112</left><top>44</top><width>380</width><height>36</height><aligny>center</aligny><font>hm_ui_24_bold</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[31294]</label></control>
			<control type="label"><left>112</left><top>78</top><width>380</width><height>28</height><aligny>center</aligny><font>hm_small_20</font><textcolor>b3ffffff</textcolor><label>$INFO[Window(Home).Property(aeon.planner.summary)]</label></control>
			<control type="image"><left>48</left><top>120</top><width>432</width><height>1</height><texture colordiffuse="1fffffff">common/white.png</texture></control>
			<control type="grouplist" id="9450">
				<left>40</left><top>132</top><width>448</width><height>540</height>
				<orientation>vertical</orientation><itemgap>2</itemgap>
@@ROWS@@			</control>
@@ICONS@@			<control type="group">
				<visible>@@HELPVIS@@</visible>
				<control type="image"><left>40</left><top>918</top><width>448</width><height>122</height><texture border="16" colordiffuse="17ffffff">fg/r16.png</texture></control>
				<control type="label"><left>58</left><top>930</top><width>412</width><height>26</height><aligny>center</aligny><font>hm_cap_14</font><textcolor>99ffffff</textcolor><label>[UPPERCASE]$VAR[FG_PlStripHelpCap][/UPPERCASE]</label></control>
				<control type="textbox"><left>58</left><top>958</top><width>412</width><height>76</height><font>hm_small_20</font><textcolor>e6ffffff</textcolor><label>$VAR[FG_PlStripHelp]</label></control>
			</control>
		</control>
	</include>
'''.replace('@@HELPVIS@@', ' | '.join('Control.HasFocus(%d)' % r[0] for r in ROWS if r[5])).replace('@@ROWS@@', ''.join(r[0] for r in rows)).replace('@@ICONS@@', ''.join(r[1] for r in rows))

BODY = ('\t<!-- FG_PLANNER:begin (written by _src/fg_planner.py) ====================== Planner, Fused Glass (0.43.0) -->\n' +
        VARS + TOP + WEEKBODY + STRIP + '\t<!-- FG_PLANNER:end -->\n')
f = io.open(FUSED, encoding='utf-8').read()
f = re.sub(r'\t<!-- FG_PLANNER:begin.*?<!-- FG_PLANNER:end -->\n', '', f, flags=re.S)
f = f.replace('</includes>', BODY + '</includes>')
io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
import xml.etree.ElementTree as ET
for name in (FUSED, PLAN, WINDOW, INCLUDES, VIEWS):
    ET.parse(name)
print('ok')
