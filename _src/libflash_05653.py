# -*- coding: utf-8 -*-
"""0.56.53 the "Flix flash" (review 2026-11-18, open; user 2026-11-20 on the box: "that background is what i have been
talking about has flashed previously movies. It's a Films window which shows hours").

The video library window (VidView_Window) always carries the Aeon Glass library layer: its tab bar
(AG_LibraryTopLine_L: Options / For now / Films / Shows / Music / Search), the card with "Films . title . n of total",
the details line and the views 500-506 (506 "Time": the hour timeline, "Start now and you're done by"). Their
conditions only ask which view is visible; while the window opens and the Fused Glass view is not drawn yet, they hold
for a moment and the layer fades in and out over Flix. In Fused Glass the layer is not loaded at all (conditional
includes, read when the window loads); list 50 stays (it is in the window's <views>). Aeon and Aeon Glass unchanged.
Repeatable."""
import io
import os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i', 'Includes_Views_Video.xml')
CLASSIC = ('VidView_Card', 'VidView_Detail', 'VidView_500_Grid', 'VidView_501_Wall', 'VidView_502_Spotlight',
           'VidView_503_Episodes', 'VidView_509_Rows', 'VidView_505_Wide', 'VidView_506_Time', 'VidView_CardFade',
           'VidView_Empty', 'VidView_CardHeader')


def main():
    t = io.open(P, encoding='utf-8').read()
    i = t.index('<include name="VidView_Window">')
    e = t.index('\n\t</include>', i)
    seg = t[i:e]
    n = 0
    for name in CLASSIC:
        old = '<include>%s</include>' % name
        if old in seg:
            seg = seg.replace(old, '<include condition="!Skin.HasSetting(aeon.fglass)">%s</include>' % name, 1)
            n += 1
    old = '<include content="AG_LibraryTopLine_L">'
    if old in seg:
        seg = seg.replace(old, '<include content="AG_LibraryTopLine_L" condition="!Skin.HasSetting(aeon.fglass)">', 1)
        n += 1
    if n:
        seg = seg.replace('<include name="VidView_Window">', '<include name="VidView_Window"><!-- 0.56.53 libflash: the Aeon Glass layer not in Fused Glass -->', 1)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t[:i] + seg + t[e:])
    print('library window: %d Aeon Glass layers left out in Fused Glass' % n)


if __name__ == '__main__':
    main()
