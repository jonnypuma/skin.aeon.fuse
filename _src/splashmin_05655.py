# -*- coding: utf-8 -*-
"""0.56.55 the start-up splash stays until Home is really loaded (user, after a skin switch on the box: "splash screen
only showed for a few seconds", "it took almost a minute though for it to fully load spotlights ... the splash screen
should stay until things are loaded. that is the point of it").

Before: it ended when each section's row had items OR the helper's aeon.pl.<sec>.in was set. That property is set once
per helper run, so after a skin switch / reload it was already there and the splash ended at once; the spotlights were
never waited for. Now each section (movies / tv / music, when the library has it) is done when:
  - its row has items, or the helper saw it empty (aeon.pl.<sec>.in), and neither the row nor its node list is loading;
  - its spotlight (9421 / 9422 / 9423), when on, has items and is not loading.
Plus at least 8 s after Home opened (covers the moment before the lists start loading), and the cap goes from 40 s to
90 s. The step ticks (Aeon_SplMov / Tvs / Mus) use the same tests. Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
MIN = '00:08'
CAP = '01:30'
PROP = 'Window(Home).Property(aeon.splash.min)'
SECS = (('Mov', 'movies', 'movies', 9301, 93911, 9421),
        ('Tvs', 'tvshows', 'tv', 9302, 93912, 9422),
        ('Mus', 'music', 'music', 9303, 93913, 9423))


def sec_test(lib, sec, strip, node, spot):
    return ('[![Library.HasContent({lib})] | [[Integer.IsGreater(Container({strip}).NumItems,0) | '
            '!String.IsEmpty(Window(Home).Property(aeon.pl.{sec}.in))] + !Container({strip}).IsUpdating + '
            '!Container({node}).IsUpdating + [Skin.HasSetting(aeon.nosp2.{sec}) | '
            '[Integer.IsGreater(Container({spot}).NumItems,0) + !Container({spot}).IsUpdating]]]]'
            ).format(lib=lib, sec=sec, strip=strip, node=node, spot=spot)


def edit(name, fn):
    p = os.path.join(D, name)
    s = io.open(p, encoding='utf-8').read()
    t = fn(s)
    if t != s:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
        print('splashmin:', name)


def fused(s):
    for short, lib, sec, strip, node, spot in SECS:
        s = re.sub(r'(<expression name="Aeon_Spl%s">).*?(</expression>)' % short,
                   lambda m: m.group(1) + sec_test(lib, sec, strip, node, spot) + m.group(2), s, count=1)
    return s


def timers(s):
    i = s.index('<name>aeonsplashend</name>')
    j = s.index('<start>', i) + len('<start>')
    k = s.index('</start>', j)
    lib = '[Library.HasContent(movies) | Library.HasContent(tvshows) | Library.HasContent(music)]'
    tests = ' + '.join(sec_test(lib_, sec, strip, node, spot) for _, lib_, sec, strip, node, spot in SECS)
    cond = ('!String.IsEmpty(%s) + !String.IsEmpty(Window(Home).Property(aeon.splash)) + '
            'String.IsEmpty(Window(Home).Property(aeon.splash.ending)) + '
            'String.IsEmpty(Window(Home).Property(aeon.splash.hold)) + '
            '[[%s + %s + [![System.HasPVRAddon] | PVR.HasTVChannels]] | '
            '!String.IsEmpty(Window(Home).Property(aeon.splash.to))]' % (PROP, lib, tests))
    s = s[:j] + cond + s[k:]
    s = s.replace('or 40 s after Home opened (_src/splash_05620.py)',
                  'or 90 s after Home opened (_src/splash_05620.py; 0.56.55 rows and spotlights really loaded, '
                  'at least 8 s: _src/splashmin_05655.py)', 1)
    fin = '<onstart>ClearProperty(aeon.splash.ending,home)</onstart>'
    add = fin + '\n\t\t<onstart>ClearProperty(aeon.splash.min,home)</onstart>'
    if add not in s:
        s = s.replace(fin, add, 1)
    return s


def home(s):
    s = s.replace('SetProperty(aeon.splash.to,1,home),00:40,silent)</onload><!-- 0.56.53 40 s (user: "Wait for 10s more") -->',
                  'SetProperty(aeon.splash.to,1,home),%s,silent)</onload><!-- 0.56.55 90 s cap (rows and spotlights '
                  'can take a minute) -->' % CAP, 1)
    anchor = '<onload condition="!String.IsEmpty(Window(Home).Property(aeon.splash))">SetFocus(9999)</onload>'
    line = ('<onload condition="!String.IsEmpty(Window(Home).Property(aeon.splash))">AlarmClock(aeonsplashmin,'
            'SetProperty(aeon.splash.min,1,home),%s,silent)</onload><!-- 0.56.55 at least 8 s on screen -->' % MIN)
    if 'aeonsplashmin' not in s:
        s = s.replace(anchor, anchor + '\n\t' + line, 1)
    # the helper reloads the skin once after an update (the user's fonts into the fresh Font.xml, fontpick.sync) and
    # sets aeon.splash.keep first: Home's unload keeps the splash, its load starts the waits again
    keep = 'Window(Home).Property(aeon.splash.keep)'
    old = '<onunload>ClearProperty(aeon.splash,home)</onunload>'
    new = '<onunload condition="String.IsEmpty(%s)">ClearProperty(aeon.splash,home)</onunload>' % keep
    s = s.replace(old, new, 1)
    restart = ('<onload condition="!String.IsEmpty(%s)">ClearProperty(aeon.splash.min,home)</onload>'
               '<!-- 0.56.55 back from the helper\'s font reload: wait again -->' % keep)
    if restart not in s:
        s = s.replace(anchor, restart + '\n\t' + anchor, 1)
    clear = '<onload>ClearProperty(aeon.splash.keep,home)</onload>'
    if clear not in s:
        s = s.replace(new, clear + '\n\t' + new, 1)
    return s


def startup(s):
    first = '<onload>SetProperty(aeon.splash,1,home)</onload>'
    line = '<onload>ClearProperty(aeon.splash.min,home)</onload>'
    if line not in s:
        s = s.replace(first, line + '\n\t' + first, 1)
    return s


def main():
    edit('Includes_Fused.xml', fused)
    edit('Timers.xml', timers)
    edit('Home.xml', home)
    edit('Startup.xml', startup)


if __name__ == '__main__':
    main()
