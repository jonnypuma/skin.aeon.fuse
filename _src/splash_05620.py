# -*- coding: utf-8 -*-
"""0.56.20: the start-up splash (canvas "Aeon Power, Pictures and splash", approved 2026-11-17), Aeon, Aeon Glass and
Fused Glass. It is a layer of Home, not a dialog: Aeon Fuse Helper's Home preload reads Home's lists and stops while
another window has the focus, so a dialog would hold up the loading it waits for. A hidden button (9999) holds the focus
while the layer shows; OK or Back go to the menu at once.

Startup.xml sets Window(Home) aeon.splash and a 20 s alarm (aeon.splash.to). Four steps tick off: Library (Kodi's
library has content), Weather (fetched, or no weather add-on), Home rows (the focused section's strip has items; the helper's preload starts too late for this),
Live TV guide (channels in, or no PVR). Timers.xml aeonsplashend ends it when the library, the row and the channels are in (weather is not waited for) or 20 s after Home opened.
Skin reload: not covered (Kodi does not run Startup.xml again). Runs once (marker)."""
import io
import os
import xml.etree.ElementTree as ET

MARK = '0.56.20 splash'
FUSED = os.path.join('1080i', 'Includes_Fused.xml')
HOME = os.path.join('1080i', 'Home.xml')
START = os.path.join('1080i', 'Startup.xml')
TIMERS = os.path.join('1080i', 'Timers.xml')
P = 'Window(Home).Property(%s)'
L, W, R, T = ('Library.HasContent(movies) | Library.HasContent(tvshows) | Library.HasContent(music)',
              'Weather.IsFetched | String.IsEmpty(Weather.Plugin)',
              '[String.IsEqual(Container(9000).ListItem.Label2,movies) + Integer.IsGreater(Container(9301).NumItems,0)] | [String.IsEqual(Container(9000).ListItem.Label2,tv) + Integer.IsGreater(Container(9302).NumItems,0)] | [String.IsEqual(Container(9000).ListItem.Label2,music) + Integer.IsGreater(Container(9303).NumItems,0)] | ![String.IsEqual(Container(9000).ListItem.Label2,movies) | String.IsEqual(Container(9000).ListItem.Label2,tv) | String.IsEqual(Container(9000).ListItem.Label2,music)]',
              '!System.HasPVRAddon | PVR.HasTVChannels')
EXPR = {'Lib': L, 'Wx': W, 'Rows': R, 'Tv': T}


def e(name):
    return '[$EXP[Aeon_Spl%s]]' % name


N = {1: '%s | %s | %s | %s' % (e('Lib'), e('Wx'), e('Rows'), e('Tv')),
     2: '[%s + [%s | %s | %s]] | [%s + [%s | %s]] | [%s + %s]' % (e('Lib'), e('Wx'), e('Rows'), e('Tv'), e('Wx'), e('Rows'), e('Tv'), e('Rows'), e('Tv')),
     3: '[%s + %s + [%s | %s]] | [[%s | %s] + %s + %s]' % (e('Lib'), e('Wx'), e('Rows'), e('Tv'), e('Lib'), e('Wx'), e('Rows'), e('Tv')),
     4: '%s + %s + %s + %s' % (e('Lib'), e('Wx'), e('Rows'), e('Tv'))}
CUR = {'Lib': '!%s' % e('Lib'), 'Wx': '%s + !%s' % (e('Lib'), e('Wx')),
       'Rows': '%s + %s + !%s' % (e('Lib'), e('Wx'), e('Rows')), 'Tv': '%s + %s + %s + !%s' % (e('Lib'), e('Wx'), e('Rows'), e('Tv'))}
STEPS = (('Lib', '$LOCALIZE[14022]'), ('Wx', '$LOCALIZE[8]'), ('Rows', '$ADDON[skin.aeon.fuse 32623]'), ('Tv', '$ADDON[skin.aeon.fuse 32625]'))


def progress(left, top, width, height, tex, border, track, fill):
    out = '\t\t\t\t<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><texture border="%s" colordiffuse="%s">%s</texture></control>\n' % (left, top, width, height, border, track, tex)
    for k in (1, 2, 3, 4):
        out += ('\t\t\t\t<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><texture border="%s" colordiffuse="%s">%s</texture>'
                '<visible>[%s]%s</visible></control>\n' % (left, top, width * k // 4, height, border, fill, tex, N[k], '' if k == 4 else ' + ![%s]' % N[k + 1]))
    return out


def steps_text(top):
    """Aeon: the steps as text, a check before each one done, the current one bright."""
    out = '\t\t\t\t<control type="grouplist"><left>0</left><top>%d</top><width>1920</width><height>40</height><orientation>horizontal</orientation><align>center</align><itemgap>14</itemgap>\n' % top
    for key, label in STEPS:
        out += ('\t\t\t\t\t<control type="image"><width>22</width><height>40</height><aspectratio>keep</aspectratio><texture colordiffuse="d9ffffff">aeon/icons/check.png</texture><visible>%s</visible></control>\n'
                '\t\t\t\t\t<control type="label"><width max="400">auto</width><height>40</height><aligny>center</aligny><font>hm_ui_22</font><textcolor>d9ffffff</textcolor><label>%s</label><visible>%s</visible></control>\n'
                '\t\t\t\t\t<control type="label"><width max="400">auto</width><height>40</height><aligny>center</aligny><font>hm_ui_22_bold</font><textcolor>ffffffff</textcolor><label>%s</label><visible>%s</visible></control>\n'
                '\t\t\t\t\t<control type="label"><width max="400">auto</width><height>40</height><aligny>center</aligny><font>hm_ui_22</font><textcolor>8cffffff</textcolor><label>%s</label><visible>!%s + ![%s]</visible></control>\n'
                '\t\t\t\t\t<control type="image"><width>20</width><height>40</height><texture></texture></control>\n'
                % (e(key), label, e(key), label, CUR[key], label, e(key), CUR[key]))
    return out + '\t\t\t\t</control>\n'


def steps_pills(top):
    """Aeon Glass / Fused Glass: the steps as pills: done filled, the current one white, the rest outlined."""
    out = '\t\t\t\t<control type="grouplist"><left>0</left><top>%d</top><width>1920</width><height>44</height><orientation>horizontal</orientation><align>center</align><itemgap>14</itemgap>\n' % top
    for key, label in STEPS:
        for cond, tex, col, ink, font in ((e(key), 'fg/p44.png', '1affffff', 'd9ffffff', 'hm_ui_22'),
                                         (CUR[key], 'fg/p44.png', 'ffffffff', 'ff111111', 'hm_ui_22_bold'),
                                         ('!%s + ![%s]' % (e(key), CUR[key]), 'fg/pe44.png', '33ffffff', '8cffffff', 'hm_ui_22')):
            out += ('\t\t\t\t\t<control type="button"><width min="120" max="420">auto</width><height>44</height><label>%s</label><font>%s</font>'
                    '<textcolor>%s</textcolor><disabledcolor>%s</disabledcolor><align>center</align><aligny>center</aligny><textoffsetx>22</textoffsetx>'
                    '<texturenofocus border="22,0,22,0" colordiffuse="%s">%s</texturenofocus><texturefocus border="22,0,22,0" colordiffuse="%s">%s</texturefocus>'
                    '<enable>false</enable><visible>%s</visible></control>\n' % (label, font, ink, ink, col, tex, col, tex, cond))
    return out + '\t\t\t\t</control>\n'


def wordmark(top, fuse_col):
    return ('\t\t\t\t<control type="grouplist"><left>0</left><top>%d</top><width>1920</width><height>130</height><orientation>horizontal</orientation><align>center</align><itemgap>28</itemgap>\n'
            '\t\t\t\t\t<control type="label"><width max="900">auto</width><height>130</height><aligny>center</aligny><font>hm_display_84</font><textcolor>ffffffff</textcolor><label>AEON</label></control>\n'
            '\t\t\t\t\t<control type="label"><width max="900">auto</width><height>130</height><aligny>center</aligny><font>hm_display_84</font><textcolor>%s</textcolor><label>FUSE</label></control>\n'
            '\t\t\t\t</control>\n' % (top, fuse_col))


def status(top):
    return ('\t\t\t\t<control type="label"><left>0</left><top>%d</top><width>1920</width><height>40</height><align>center</align><aligny>center</aligny>'
            '<font>hm_ui_24</font><textcolor>c7ffffff</textcolor><label>$ADDON[skin.aeon.fuse 32622]</label></control>\n' % top)


def hint():
    return ('\t\t\t\t<control type="label"><left>120</left><top>1000</top><width>1680</width><height>34</height><aligny>center</aligny>'
            '<font>hm_ui_20</font><textcolor>73ffffff</textcolor><label>$ADDON[skin.aeon.fuse 32624]</label></control>\n')


def build():
    x = '\t<!-- %s: the start-up splash, a layer of Home (see _src/splash_05620.py) -->\n' % MARK
    for k, v in EXPR.items():
        x += '\t<expression name="Aeon_Spl%s">%s</expression>\n' % (k, v)
    x += '\t<include name="Aeon_Splash">\n'
    x += ('\t\t<control type="button" id="9999"><left>0</left><top>0</top><width>1</width><height>1</height><label></label>'
          '<texturefocus></texturefocus><texturenofocus></texturenofocus><onup>noop</onup><ondown>noop</ondown><onleft>noop</onleft>'
          '<onright>noop</onright><onclick>SetFocus(9000)</onclick><onback>9000</onback>'
          '<visible>!String.IsEmpty(%s)</visible></control>\n' % (P % 'aeon.splash'))
    x += ('\t\t<control type="group">\n\t\t\t<visible>!String.IsEmpty(%s) + Control.HasFocus(9999)</visible>\n'
          '\t\t\t<animation type="Hidden"><effect type="fade" start="100" end="0" time="450"/></animation>\n' % (P % 'aeon.splash'))
    # Aeon: flat, the accent on FUSE, a square line
    x += '\t\t\t<control type="group">\n\t\t\t\t<visible>!Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)</visible>\n'
    x += '\t\t\t\t<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="ff0a0a0c">common/white.png</texture></control>\n'
    x += wordmark(370, '$VAR[Aeon_Accent]') + progress(640, 540, 640, 6, 'common/white.png', '0', '1fffffff', '$VAR[Aeon_Accent]') + status(576) + steps_text(636) + hint()
    x += '\t\t\t</control>\n'
    # Aeon Glass: one rounded glass card, a pill line, pill steps
    x += '\t\t\t<control type="group">\n\t\t\t\t<visible>Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)</visible>\n'
    x += ('\t\t\t\t<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="ff121019">common/white.png</texture></control>\n'
          '\t\t\t\t<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="99000000">common/aeon_vignette.png</texture></control>\n'
          '\t\t\t\t<control type="image"><left>520</left><top>300</top><width>880</width><height>440</height><texture border="28" colordiffuse="10ffffff">fg/r28.png</texture></control>\n'
          '\t\t\t\t<control type="image"><left>520</left><top>300</top><width>880</width><height>440</height><texture border="28" colordiffuse="33ffffff">fg/e28.png</texture></control>\n')
    x += wordmark(352, 'bfffffff') + progress(680, 512, 560, 8, 'fg/pill8.png', '4,0,4,0', '24ffffff', 'ffffffff') + status(552) + steps_pills(790) + hint()
    x += '\t\t\t</control>\n'
    # Fused Glass: frosted card with a soft shadow, the mark's yellow on the line, pill steps
    x += '\t\t\t<control type="group">\n\t\t\t\t<visible>Skin.HasSetting(aeon.fglass)</visible>\n'
    x += ('\t\t\t\t<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="ff0d0c12">common/white.png</texture></control>\n'
          '\t\t\t\t<control type="image"><left>520</left><top>286</top><width>880</width><height>468</height><texture border="56" colordiffuse="73000000">fg/sh16.png</texture></control>\n'
          '\t\t\t\t<control type="image"><left>560</left><top>320</top><width>800</width><height>400</height><texture border="28" colordiffuse="14ffffff">fg/r28.png</texture></control>\n'
          '\t\t\t\t<control type="image"><left>560</left><top>320</top><width>800</width><height>400</height><texture border="28" colordiffuse="29ffffff">fg/e28.png</texture></control>\n')
    x += wordmark(366, 'fg_mark') + progress(700, 520, 520, 10, 'fg/pill10.png', '5,0,5,0', '24ffffff', 'fg_mark') + status(560) + steps_pills(770) + hint()
    x += '\t\t\t</control>\n\t\t</control>\n\t</include>\n'
    return x


TIMER = '''	<timer>
		<name>aeonsplashend</name>
		<description>%(m)s: the start-up splash ends when the library, the focused Home row and the TV channels are in (weather is not waited for) or 20 s after Home opened (_src/splash_05620.py)</description>
		<start>!String.IsEmpty(Window(Home).Property(aeon.splash)) + String.IsEmpty(Window(Home).Property(aeon.splash.hold)) + [[%(ready)s] | !String.IsEmpty(Window(Home).Property(aeon.splash.to))]</start>
		<stop>true</stop>
		<onstart condition="Window.IsActive(home) + Control.HasFocus(9999)">SetFocus(9000)</onstart>
		<onstart>ClearProperty(aeon.splash,home)</onstart>
		<onstart>ClearProperty(aeon.splash.to,home)</onstart>
	</timer>
''' % {'m': MARK, 'ready': '[%s] + [%s] + [%s]' % (L, R, T)}


def main():
    f = io.open(FUSED, encoding='utf-8').read()
    if MARK in f:
        print('already')
        return
    i = f.rindex('</includes>')
    f = f[:i] + build() + f[i:]
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(f)
    ET.parse(FUSED)
    h = io.open(HOME, encoding='utf-8').read()
    old = '\t<include>Anim_WindowOpenClose</include>\n\t<controls>\n\t\t<include>Aeon_Home</include>\n\t</controls>'
    assert h.count(old) == 1
    h = h.replace(old, ('\t<!-- %s: while the start-up splash shows, its button holds the focus (OK / Back: the menu) -->\n'
                        '\t<onload condition="!String.IsEmpty(Window(Home).Property(aeon.splash))">SetFocus(9999)</onload>\n'
                        '\t<onunload>ClearProperty(aeon.splash,home)</onunload>\n' % MARK) + old.replace(
                            '<include>Aeon_Home</include>\n', '<include>Aeon_Home</include>\n\t\t<include>Aeon_Splash</include>\n'))
    io.open(HOME, 'w', encoding='utf-8', newline='\n').write(h)
    ET.parse(HOME)
    s = io.open(START, encoding='utf-8').read()
    old = '\t<onload>ReplaceWindow($INFO[System.StartupWindow])</onload>'
    assert s.count(old) == 1
    s = s.replace(old, ('\t<!-- %s: the splash over Home while it loads, 20 s at the most -->\n'
                        '\t<onload>SetProperty(aeon.splash,1,home)</onload>\n'
                        '\t<onload>AlarmClock(aeonsplashto,SetProperty(aeon.splash.to,1,home),00:20,silent)</onload>\n' % MARK) + old)
    io.open(START, 'w', encoding='utf-8', newline='\n').write(s)
    ET.parse(START)
    t = io.open(TIMERS, encoding='utf-8').read()
    i = t.rindex('</timers>')
    t = t[:i] + TIMER + t[i:]
    io.open(TIMERS, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(TIMERS)
    print('ok')


if __name__ == '__main__':
    main()
