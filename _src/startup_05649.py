"""0.56.49 the splash from Kodi's first frame (the user, 2026-11-18: "The splash screen starts very late, it should start
as soon as kodi is loading/reloading").

Kodi draws nothing until the start-up window's <onload> has run, and Startup.xml's onload was ReplaceWindow(Home): Home
(the biggest window, KEEP_IN_MEMORY) loaded first, 7.3 s on the box (log: "Loading skin file: Home.xml" 36.04 ->
"initialize done" 43.44), so the screen stayed black and the splash, a layer of Home, came last. Now Startup.xml draws
the splash itself (the same face: dark ground, AEON FUSE, the yellow spinner, the rows) and asks for Home a second
later (AlarmClock, 1 s: Kodi runs it from its loop, after the page has been drawn). While Home loads the screen keeps
that picture; Home's splash then carries on from it (the face fades in only on Startup).

Aeon_Splash is split: Aeon_SplashFront (the shade, vignette, the face and the rows, the hint) is shared; Home keeps the
button, the ground and the drifting fanart (the helper names it once it runs). Run from the skin folder. Repeatable."""
import io
import os
import re

X = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
FUSED = os.path.join(X, 'Includes_Fused.xml')
START = os.path.join(X, 'Startup.xml')
MARK = '<!-- 0.56.49 startup -->'
OVERLAY = '\t\t\t<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="99000000">common/white.png</texture></control>\n'
ANIM = ('\t\t\t\t<animation type="WindowOpen" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="500"/>'
        '<effect type="slide" start="0,24" end="0,0" time="600" tween="cubic" easing="out"/></animation>\n')
STARTUP = """<?xml version="1.0" encoding="UTF-8"?>
<!--
	Startup: the splash from the first frame (0.56.49, _src/startup_05649.py). Kodi draws nothing until this window's
	onload has run, so Home (7 s to load on the box) is asked for a second later, after this page is on screen; the
	screen keeps it while Home loads, and Home's splash carries on from it. Goes to Kodi's configured startup window
	(default Home), like Estuary, so "Settings > Interface > Startup window" keeps working.
-->
<window>
	<onload>SetProperty(aeon.splash,1,home)</onload>
	<onload>AlarmClock(aeonstartup,ReplaceWindow($INFO[System.StartupWindow]),00:01,silent)</onload>
	<controls>
		<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="ff0b0b0e">common/white.png</texture></control>
		<include content="Aeon_SplashFront"><param name="open" value="true"/></include>
	</controls>
</window>
"""


def main():
    t = io.open(FUSED, encoding='utf-8').read()
    if MARK not in t:
        s = t.index('\t<include name="Aeon_Splash">')
        e = t.index('\t</include>\n', s)
        blk = t[s:e]
        a = blk.index(OVERLAY)
        tail = '\t\t</control>\n'
        assert blk.endswith(tail)
        front = blk[a:-len(tail)]
        assert front.count(ANIM) == 1
        front = front.replace(ANIM, ANIM.replace('condition="!Skin.HasSetting(aeon.reducemotion)"',
                                                 'condition="$PARAM[open] + !Skin.HasSetting(aeon.reducemotion)"'))
        # one tab less: the shared part is a direct child of the include, not of the splash group
        front = ''.join(l[1:] if l.startswith('\t') else l for l in front.splitlines(True))
        home = blk[:a] + '\t\t\t<include content="Aeon_SplashFront"><param name="open" value="false"/></include>\n' + tail
        new = (home + '\t</include>\n'
               '\t' + MARK + '<!-- the splash\'s face, shared by Startup.xml (from the first frame) and Home (with the fanart) -->\n'
               '\t<include name="Aeon_SplashFront">\n'
               '\t\t<param name="open" default="false"/>\n'
               '\t\t<definition>\n' + ''.join('\t' + l if l.strip() else l for l in front.splitlines(True)) +
               '\t\t</definition>\n')
        t = t[:s] + new + t[e:]
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    t = rows_out(t)
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    io.open(START, 'w', encoding='utf-8', newline='\n').write(STARTUP)
    print('startup: the splash drawn by Startup.xml, Home follows after 1 s')


def rows_out(t):
    """the box, 22:23: the first window's visibility checks run inside Kodi's start, before it draws anything, and
    Library.HasContent(music) counts every song in the MySQL library there (gdb: CGUIWindow::SetInitialVisibility ->
    CMusicDatabase::GetSongsCount, 7 s). So the rows (Movies / TV shows / Music ... with their Library.HasContent
    checks, Aeon_SplLib too) leave the shared face: Aeon_SplashRows, Home only; Startup.xml checks no library."""
    if 'name="Aeon_SplashRows"' in t:
        return t
    s = t.index('\t<include name="Aeon_SplashFront">')
    e = t.index('\t</include>\n', s)
    a = t.index('<control type="grouplist"><left>0</left><top>660</top>', s, e)
    a = t.rindex('\n', 0, a) + 1
    depth, i = 0, a
    for m in re.finditer(r'<control\b|</control>', t[a:e]):
        depth += 1 if m.group(0) == '<control' else -1
        if depth == 0:
            i = a + m.end()
            break
    assert depth == 0
    i = t.index('\n', i) + 1
    rows = t[a:i]
    assert 'Library.HasContent' in rows or 'Aeon_SplLib' in rows
    t = t[:a] + t[i:]
    home = '\t\t\t<include content="Aeon_SplashFront"><param name="open" value="false"/></include>\n'
    assert t.count(home) == 1
    t = t.replace(home, home + '\t\t\t<include>Aeon_SplashRows</include>\n')
    e = t.index('\t</include>\n', t.index('\t<include name="Aeon_SplashFront">')) + len('\t</include>\n')
    t = (t[:e] + '\t<!-- 0.56.49 the splash\'s rows (Library.HasContent: a library count, so Home only, never the start-up page) -->\n'
         '\t<include name="Aeon_SplashRows">\n' + rows + '\t</include>\n' + t[e:])
    return t


if __name__ == '__main__':
    main()
