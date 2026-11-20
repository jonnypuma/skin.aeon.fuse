# -*- coding: utf-8 -*-
"""0.56.42 one start-up splash for every theme (Aeon_Splash, the Home layer while Home gets ready). The user: "make the
splash screen nicer, we only need one splash screen that looks really sleek, we do not need one for each theme. Take
inspiration from Arctic Fuse 3 skin's splash screen. I do like the yellow loading spinner we have and that we should keep."

From Arctic Fuse 3: a picture behind a dark veil and the name in the middle, a status line under it. Here: a random
film's fanart from the library (the helper sets Window(Home).Property(aeon.splash.fan) as it starts, helper 0.3.108)
drifting slowly under a dark veil and vignette; AEON white and FUSE in the yellow (fg_mark, ffe8b04b) in the display
font; the yellow spinner (fg/spin_track + fg/spin_arc, now always the yellow, not the theme's accent); one line naming
what Home still waits for (library, weather, Home rows, Live TV guide, then "Getting Home ready"); four marks for the
four steps (done white, the current one yellow, the rest faint); "OK or Back skips" at the bottom.
The include keeps its focus button 9999 and its visibility / fade-out. Rewrites the include on every run."""
import io
import os
import re
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Includes_Fused.xml')
Y = 'ffe8b04b'
A = '$ADDON[skin.aeon.fuse %d]'
# 0.56.43 the steps in order: (expression name, shown when, done when, label). The user: "splash screen is too static, it
# just says Weather is loading, what about the iptv guide ... it doesn't seem to cycle through what it's loading. can it
# preload movies and tv shows submenus?" The helper loads Home's Movies, TV shows and Music rows one after another while
# Home (and so the splash) is up (service.py HomePreload; aeon.pl.done once all are in); the splash now waits for each.
DONE_ROWS = '!String.IsEmpty(Window(Home).Property(aeon.pl.done))'
STEPS = [
    ('Aeon_SplLib', 'true', 'Library.HasContent(movies) | Library.HasContent(tvshows) | Library.HasContent(music)', '$LOCALIZE[14022]'),
    ('Aeon_SplMov', 'Library.HasContent(movies)', 'Integer.IsGreater(Container(9301).NumItems,0) | ' + DONE_ROWS, '$LOCALIZE[342]'),
    ('Aeon_SplTvs', 'Library.HasContent(tvshows)', 'Integer.IsGreater(Container(9302).NumItems,0) | ' + DONE_ROWS, '$LOCALIZE[20343]'),
    ('Aeon_SplMus', 'Library.HasContent(music)', 'Integer.IsGreater(Container(9303).NumItems,0) | ' + DONE_ROWS, '$LOCALIZE[2]'),
    ('Aeon_SplTv', 'System.HasPVRAddon', 'PVR.HasTVChannels', A % 32625),
    ('Aeon_SplWx', '!String.IsEmpty(Weather.Plugin)', 'Weather.IsFetched', '$LOCALIZE[8]'),
]
WAITED = ('Aeon_SplLib', 'Aeon_SplMov', 'Aeon_SplTvs', 'Aeon_SplMus', 'Aeon_SplTv')   # weather is not waited for


def ready(name):
    """the step is done or not shown (written out: Timers.xml has no $EXP)"""
    _n, vis, done, _l = [x for x in STEPS if x[0] == name][0]
    return '[%s]' % done if vis == 'true' else '[![%s] | %s]' % (vis, done)


def expressions():
    o = ['\t<!-- 0.56.43 splash steps (_src/splash_05642.py): done, or not shown -->']
    for name, _vis, _done, _label in STEPS:
        o.append('\t<expression name="%s">%s</expression>' % (name, ready(name)))
    return '\n'.join(o) + '\n'


def steps_row():
    """the steps side by side, centred: a check when done, a small yellow spinner on the one Home waits for now, a faint
    dot before the rest; the label white / bold / faint the same way"""
    o = ['<control type="grouplist"><left>0</left><top>660</top><width>1920</width><height>40</height><orientation>horizontal</orientation>'
         '<align>center</align><itemgap>10</itemgap>']
    before = []
    for n, (name, vis, _done, label) in enumerate(STEPS):
        shown = '' if vis == 'true' else '[%s] + ' % vis
        done = '$EXP[%s]' % name
        now = '!' + done + ''.join(' + ' + x for x in before)
        later = ('!%s + ![%s]' % (done, ' + '.join(before))) if before else None
        if n:
            o.append('<control type="image"><width>18</width><height>40</height><texture></texture>%s</control>'
                     % ('<visible>%s</visible>' % vis if vis != 'true' else ''))
        o.append('<control type="image"><width>22</width><height>40</height><aspectratio>keep</aspectratio>'
                 '<texture colordiffuse="d9ffffff">aeon/icons/check.png</texture><visible>%s%s</visible></control>' % (shown, done))
        o.append('<control type="group"><width>22</width><height>40</height><visible>%s%s</visible>'
                 '<control type="image"><top>9</top><width>22</width><height>22</height><texture colordiffuse="24ffffff">fg/spin_track.png</texture></control>'
                 '<control type="image"><top>9</top><width>22</width><height>22</height><texture colordiffuse="%s">fg/spin_arc.png</texture>'
                 '<animation effect="rotate" end="-360" center="auto" time="1100" loop="true" reversible="false" condition="!Skin.HasSetting(aeon.reducemotion)">Conditional</animation>'
                 '</control></control>' % (shown, now, Y))
        if later:
            o.append('<control type="group"><width>22</width><height>40</height><visible>%s%s</visible>'
                     '<control type="image"><left>6</left><top>15</top><width>10</width><height>10</height><texture colordiffuse="40ffffff">fg/circle.png</texture></control>'
                     '</control>' % (shown, later))
        o.append('<control type="label"><width max="400">auto</width><height>40</height><aligny>center</aligny><font>hm_ui_22</font>'
                 '<textcolor>d9ffffff</textcolor><label>%s</label><visible>%s%s</visible></control>' % (label, shown, done))
        o.append('<control type="label"><width max="400">auto</width><height>40</height><aligny>center</aligny><font>hm_ui_22_bold</font>'
                 '<textcolor>ffffffff</textcolor><label>%s</label><visible>%s%s</visible></control>' % (label, shown, now))
        if later:
            o.append('<control type="label"><width max="400">auto</width><height>40</height><aligny>center</aligny><font>hm_ui_22</font>'
                     '<textcolor>73ffffff</textcolor><label>%s</label><visible>%s%s</visible></control>' % (label, shown, later))
        before.append(done)
    o.append('</control>')
    return '\n\t\t\t\t'.join(o)


def body():
    return '\n'.join([
        '\t\t<control type="group">',
        '\t\t\t<visible>!String.IsEmpty(Window(Home).Property(aeon.splash)) + Control.HasFocus(9999)</visible>',
        '\t\t\t<animation type="Hidden"><effect type="fade" start="100" end="0" time="450"/></animation>',
        '\t\t\t<!-- 0.56.42 one splash for every theme (_src/splash_05642.py) -->',
        '\t\t\t<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="ff0b0b0e">common/white.png</texture></control>',
        '\t\t\t<control type="image"><left>-60</left><top>-34</top><width>2040</width><height>1148</height><aspectratio>scale</aspectratio><fadetime>900</fadetime>'
        '<texture background="true" colordiffuse="66ffffff">$INFO[Window(Home).Property(aeon.splash.fan)]</texture>'
        '<animation type="Conditional" condition="!Skin.HasSetting(aeon.reducemotion)" reversible="false"><effect type="slide" start="40,0" end="-40,0" time="24000" tween="sine" easing="inout"/></animation></control>',
        '\t\t\t<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="99000000">common/white.png</texture></control>',
        '\t\t\t<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="ff000000">common/aeon_vignette.png</texture></control>',
        '\t\t\t<control type="image"><top>540</top><width>1920</width><height>540</height><texture colordiffuse="cc000000">aeon/osd_scrim_bottom.png</texture></control>',
        '\t\t\t<control type="group">',
        '\t\t\t\t<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="500"/><effect type="slide" start="0,24" end="0,0" time="600" tween="cubic" easing="out"/></animation>',
        '\t\t\t\t<control type="grouplist"><left>0</left><top>380</top><width>1920</width><height>130</height><orientation>horizontal</orientation><align>center</align><itemgap>28</itemgap>',
        '\t\t\t\t\t<control type="label"><width max="900">auto</width><height>130</height><aligny>center</aligny><font>hm_display_84</font><textcolor>ffffffff</textcolor><label>AEON</label></control>',
        '\t\t\t\t\t<control type="label"><width max="900">auto</width><height>130</height><aligny>center</aligny><font>hm_display_84</font><textcolor>%s</textcolor><label>FUSE</label></control>' % Y,
        '\t\t\t\t</control>',
        '\t\t\t\t<!-- the yellow spinner -->',
        '\t\t\t\t<control type="group"><left>938</left><top>534</top><width>44</width><height>44</height>'
        '<control type="image"><width>44</width><height>44</height><texture colordiffuse="24ffffff">fg/spin_track.png</texture></control>'
        '<control type="image"><width>44</width><height>44</height><texture colordiffuse="%s">fg/spin_arc.png</texture>'
        '<animation effect="rotate" end="-360" center="auto" time="1100" loop="true" reversible="false" condition="!Skin.HasSetting(aeon.reducemotion)">Conditional</animation></control></control>' % Y,
        '\t\t\t\t<control type="label"><left>0</left><top>600</top><width>1920</width><height>40</height><align>center</align><aligny>center</aligny>'
        '<font>hm_ui_24</font><textcolor>c7ffffff</textcolor><label>%s</label></control>' % (A % 32622),
        '\t\t\t\t' + steps_row(),
        '\t\t\t</control>',
        '\t\t\t<control type="label"><left>0</left><top>1000</top><width>1920</width><height>34</height><align>center</align><aligny>center</aligny>'
        '<font>hm_ui_20</font><textcolor>66ffffff</textcolor><label>%s</label></control>' % (A % 32624),
        '\t\t</control>'])


def main():
    t = io.open(P, encoding='utf-8').read()
    i = t.index('<include name="Aeon_Splash">')
    j = t.index('\n\t</include>', i)
    blk = t[i:j]
    btn = re.search(r'\n\t\t<control type="button" id="9999">.*?</control>', blk, re.S).group(0)
    t = t[:i] + '<include name="Aeon_Splash">' + btn + '\n' + body() + t[j:]
    # the old step variable and expressions out, the new expressions in
    t = re.sub(r'\t<!-- 0.56.42 splash: the step Home waits for[^\n]*\n\t<variable name="Aeon_SplStep">.*?</variable>\n', '', t, flags=re.S)
    t = re.sub(r'\t<!-- 0.56.43 splash steps[^\n]*\n(?:\t<expression name="Aeon_Spl\w+">[^\n]*\n)+', '', t)
    for name in ('Aeon_SplLib', 'Aeon_SplWx', 'Aeon_SplRows', 'Aeon_SplTv'):
        t = re.sub(r'\t<expression name="%s">[^\n]*\n' % name, '', t)
    i = t.index('<include name="Aeon_Splash">')
    t = t[:i] + expressions().lstrip('\t') + '\t' + t[i:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    # the end: every waited step done (weather is not waited for), or 30 s after Home opened
    tp = os.path.join('1080i', 'Timers.xml')
    x = io.open(tp, encoding='utf-8').read()
    i = x.index('<name>aeonsplashend</name>')
    a, b = x.index('<start>', i), x.index('</start>', i) + len('</start>')
    cond = ('!String.IsEmpty(Window(Home).Property(aeon.splash)) + String.IsEmpty(Window(Home).Property(aeon.splash.hold)) + '
            '[[%s] | !String.IsEmpty(Window(Home).Property(aeon.splash.to))]' % ' + '.join(ready(n) for n in WAITED))
    x = x[:a] + '<start>%s</start>' % cond + x[b:]
    x = x.replace('ends when the library, the focused Home row and the TV channels are in (weather is not waited for) or 20 s',
                  'ends when the library, the Movies / TV shows / Music rows and the TV channels are in (weather is not waited for) or 30 s')
    io.open(tp, 'w', encoding='utf-8', newline='\n').write(x)
    ET.parse(tp)
    hp = os.path.join('1080i', 'Home.xml')
    h = io.open(hp, encoding='utf-8').read()
    h = h.replace('AlarmClock(aeonsplashto,SetProperty(aeon.splash.to,1,home),00:20,silent)',
                  'AlarmClock(aeonsplashto,SetProperty(aeon.splash.to,1,home),00:40,silent)')
    io.open(hp, 'w', encoding='utf-8', newline='\n').write(h)
    ET.parse(hp)
    print('ok')


if __name__ == '__main__':
    main()
