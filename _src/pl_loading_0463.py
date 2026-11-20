"""0.46.3 Planner: Loading instead of "Nothing planned" while the lists are filled, and holding buttons so the focus
never dead-ends on an empty list (Earlier days). Run from the skin folder, once (it checks).

Custom_1168_Planner.xml (Day view, both looks):
- onload sets Window(Home).Property(aeon.planner.busy) before the helper starts; the helper clears it once the lists
  have their items (plannerwin.py 0.3.78, also for the view / week start / Shows you watch / Earlier days / Show /
  Update now commands).
- Loading (string 31952 "Loading...", in every language already) while the day list is empty and busy, loading
  (Container.IsUpdating) or before the helper has chosen a day: Fused Glass the capsule of the busy dialog (frost,
  edge, spinner disc), the other looks the spinner and the word on a dark box. "Nothing planned" only once it is done.
- 9501 (the stand-in of an empty day) is now the Day view's holding button: always there in the Day view (1 x 1, no
  texture; the faint row shows only on an empty day), so the helper can park the focus on it while the list loads.
Includes_Planner.xml (the classic header / Week view): Down from the options goes to the day list only when it has
items and is not loading, else through the helper (planner,focus); the Week view gets its holding button 9518.
The Fused Glass header / Week view are written by fg_planner.py (same changes)."""
import io

W = '1080i/Custom_1168_Planner.xml'
P = '1080i/Includes_Planner.xml'
DAY = 'String.IsEqual(Window(Home).Property(aeon.planner.mode),day)'
BUSY = '!String.IsEmpty(Window(Home).Property(aeon.planner.busy))'
IDLE = 'String.IsEmpty(Window(Home).Property(aeon.planner.busy))'
NODATE = 'String.IsEmpty(Window(Home).Property(aeon.planner.date))'
EMPTY = 'Integer.IsEqual(Container(9500).NumItems,0)'
UPD = 'Container(9500).IsUpdating'


def once(text, old, new):
    assert text.count(old) == 1, old[:90]
    return text.replace(old, new)


w = io.open(W, encoding='utf-8').read()
if 'aeon.planner.busy' not in w:
    w = once(w, '\t<onload>RunScript(script.aeon.helper,planner,init)</onload>',
             '\t<onload>SetProperty(aeon.planner.busy,1,home)</onload>\n\t<onload>RunScript(script.aeon.helper,planner,init)</onload>')
    w = once(w, '\tNever a day before today. Up reaches the options',
             '\tNever a day before today (Earlier days: this week\'s first day). Up reaches the options')
    w = once(w, '\t\t\t\t<left>85</left><top>290</top><width>1720</width><height>756</height>\n\t\t\t\t<pagecontrol>9580</pagecontrol>',
             '\t\t\t\t<left>85</left><top>290</top><width>1720</width><height>756</height>\n'
             '\t\t\t\t<!-- 0.46.3: Kodi keeps the old day\'s items until the new ones are in: they fade out meanwhile (Loading shows) -->\n'
             '\t\t\t\t<animation effect="fade" start="100" end="0" time="150" condition="%s">Conditional</animation>\n'
             '\t\t\t\t<pagecontrol>9580</pagecontrol>' % UPD)
    old_nothing = ('\t\t\t<control type="label"><left>85</left><top>290</top><width>1720</width><height>104</height><align>center</align>'
                   '<aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>66ffffff</textcolor><label>$LOCALIZE[31893]</label>'
                   '<visible>Integer.IsEqual(Container(9500).NumItems,0)</visible><animation type="Visible"><effect type="fade" start="0" '
                   'end="100" delay="1200" time="200"/></animation></control>')
    # the label stays in the Day view's group; the Loading capsule follows that group, so it also shows right after Kodi
    # starts, before the helper has chosen a view (aeon.planner.mode empty: neither view shows then)
    pill = ('\t\t\t<!-- 0.46.3: "Nothing planned" only once the helper is done and the list has loaded (Loading below until then) -->\n'
            '\t\t\t<control type="label"><left>85</left><top>290</top><width>1720</width><height>104</height><align>center</align>'
            '<aligny>center</aligny><font>lb_ui_24_bold</font><textcolor>66ffffff</textcolor><label>$LOCALIZE[31893]</label>'
            '<visible>%(empty)s + !%(upd)s + %(idle)s + !%(nodate)s</visible><animation type="Visible"><effect type="fade" start="0" '
            'end="100" delay="300" time="200"/></animation></control>\n'
            '\t\t</control>\n'
            '\t\t<!-- 0.46.3: Loading while the helper fills the list or the day list loads, and before the helper has chosen a view\n'
            '\t\t     after Kodi starts (no view shows then); Fused Glass: the capsule of the busy dialog -->\n'
            '\t\t<control type="group">\n'
            '\t\t\t<left>801</left><top>310</top>\n'
            '\t\t\t<visible>[%(day)s + [%(upd)s | [%(empty)s + [%(busy)s | %(nodate)s]]]] | String.IsEmpty(Window(Home).Property(aeon.planner.mode))</visible>\n'
            '\t\t\t<animation type="Visible"><effect type="fade" start="0" end="100" delay="150" time="200"/></animation>\n'
            '\t\t\t<control type="image"><width>288</width><height>64</height><texture border="32" colordiffuse="$VAR[FG_Panel]">fg/r32.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>\n'
            '\t\t\t<control type="image"><width>288</width><height>64</height><texture border="32" colordiffuse="$VAR[FG_Edge]">fg/e32.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>\n'
            '\t\t\t<control type="image"><left>12</left><top>12</top><width>40</width><height>40</height><texture colordiffuse="1fffffff">fg/circle.png</texture><visible>$EXP[Aeon_FGlass]</visible></control>\n'
            '\t\t\t<control type="image"><width>288</width><height>64</height><texture colordiffuse="80000000">common/white.png</texture><visible>!$EXP[Aeon_FGlass]</visible></control>\n'
            '\t\t\t<control type="image"><left>18</left><top>18</top><width>28</width><height>28</height><texture colordiffuse="ffffffff">common/aeon_spinner.gif</texture><visible>!Skin.HasSetting(aeon.reducemotion)</visible></control>\n'
            '\t\t\t<control type="image"><left>18</left><top>18</top><width>28</width><height>28</height><texture colordiffuse="ffffffff">common/aeon_spinner_still.png</texture><visible>Skin.HasSetting(aeon.reducemotion)</visible></control>\n'
            '\t\t\t<control type="label"><left>64</left><top>0</top><width>200</width><height>64</height><aligny>center</aligny><font>ui_22</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[31952]</label></control>\n'
            '\t\t</control>') % {'empty': EMPTY, 'upd': UPD, 'busy': BUSY, 'idle': IDLE, 'nodate': NODATE, 'day': DAY}
    w = once(w, old_nothing + '\n\t\t</control>', pill)
    old_btn = ('''		<!-- an empty day has no list to hold the focus: this invisible button takes Left / Right there -->
		<control type="button" id="9501">
			<left>85</left><top>290</top><width>1720</width><height>104</height><texturefocus colordiffuse="18ffffff">common/white.png</texturefocus><texturenofocus />
			<onleft>RunScript(script.aeon.helper,planner,prev)</onleft><onright>RunScript(script.aeon.helper,planner,next)</onright><onup>9400</onup><ondown>noop</ondown><onclick>noop</onclick>
			<visible>String.IsEqual(Window(Home).Property(aeon.planner.mode),day) + Integer.IsEqual(Container(9500).NumItems,0)</visible>
		</control>''')
    new_btn = ('''		<!-- an empty day has no list to hold the focus: this invisible button takes Left / Right there. 0.46.3: always there
		     in the Day view (1 x 1, so the mouse never lands on it): the helper parks the focus on it while the list loads
		     other items (a focused list that comes back empty hands the focus to the View pill); the faint row shows
		     only on an empty day -->
		<control type="image"><left>85</left><top>290</top><width>1720</width><height>104</height><texture colordiffuse="18ffffff">common/white.png</texture><visible>Control.HasFocus(9501) + %(empty)s + !%(upd)s + !$EXP[Aeon_FGlass]</visible></control>
		<control type="image"><left>85</left><top>290</top><width>1720</width><height>104</height><texture border="16" colordiffuse="18ffffff">fg/r16.png</texture><visible>Control.HasFocus(9501) + %(empty)s + !%(upd)s + $EXP[Aeon_FGlass]</visible></control>
		<control type="button" id="9501">
			<left>85</left><top>290</top><width>1</width><height>1</height><texturefocus /><texturenofocus />
			<onleft>RunScript(script.aeon.helper,planner,prev)</onleft><onright>RunScript(script.aeon.helper,planner,next)</onright><onup>9400</onup><ondown>9500</ondown><onclick>noop</onclick>
			<visible>%(day)s</visible>
		</control>''') % {'empty': EMPTY, 'upd': UPD, 'day': DAY}
    w = once(w, old_btn, new_btn)
    io.open(W, 'w', encoding='utf-8', newline='\n').write(w)

p = io.open(P, encoding='utf-8').read()
if 'id="9518"' not in p:
    old_down = ('<ondown condition="%s">9500</ondown>\n\t\t\t\t\t<ondown condition="String.IsEqual(Window(Home).Property(aeon.planner.mode),week)">'
                'RunScript(script.aeon.helper,planner,focus)</ondown>' % DAY)
    new_down = ('<ondown condition="%s + !%s + !%s">9500</ondown>\n\t\t\t\t\t'
                '<ondown condition="[%s + [%s | %s]] | String.IsEqual(Window(Home).Property(aeon.planner.mode),week)">RunScript(script.aeon.helper,planner,focus)</ondown>'
                % (DAY, EMPTY, UPD, DAY, EMPTY, UPD))
    assert p.count(old_down) == 4, p.count(old_down)
    p = p.replace(old_down, new_down)
    hold = ('\t\t\t<!-- 0.46.3: the Week view\'s holding button (1 x 1, no texture): the helper parks the focus here while the lists\n'
            '\t\t\t     of a new week load, and leaves it here when the selected day\'s list is empty -->\n'
            '\t\t\t<control type="button" id="9518"><left>85</left><top>200</top><width>1</width><height>1</height><texturefocus /><texturenofocus />'
            '<onleft>RunScript(script.aeon.helper,planner,left)</onleft><onright>RunScript(script.aeon.helper,planner,right)</onright>'
            '<onup>9400</onup><ondown>RunScript(script.aeon.helper,planner,focus)</ondown><onclick>noop</onclick></control>\n')
    p = once(p, '\t\t\t\t<content target="videos">$VAR[Aeon_Pl_ColPath7]</content>\n\t\t\t</control>\n\t\t</control>\n\t</include>\n</includes>',
             '\t\t\t\t<content target="videos">$VAR[Aeon_Pl_ColPath7]</content>\n\t\t\t</control>\n' + hold + '\t\t</control>\n\t</include>\n</includes>')
    io.open(P, 'w', encoding='utf-8', newline='\n').write(p)

# the View pill: before the helper has chosen a view (right after Kodi starts) it names the saved one, not Day
V = '1080i/Includes_Aeon_Views3.xml'
v = io.open(V, encoding='utf-8').read()
old_view = '\t\t<value condition="String.IsEqual(Window(Home).Property(aeon.planner.mode),week)">$LOCALIZE[31898]</value>'
if old_view in v:
    v = once(v, old_view, '\t\t<value condition="String.IsEqual(Window(Home).Property(aeon.planner.mode),week) | [String.IsEmpty(Window(Home).Property(aeon.planner.mode)) + '
                          'String.IsEqual(Skin.String(aeon.planner.view),week)]">$LOCALIZE[31898]</value>')
    io.open(V, 'w', encoding='utf-8', newline='\n').write(v)

import xml.etree.ElementTree as ET
for name in (W, P, V):
    ET.parse(name)
print('ok')
