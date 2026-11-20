# -*- coding: utf-8 -*-
"""0.56.20 (screensaver.aeon.fuse 1.2.2): the screensaver's pager stands for the sections of the rotation (films, shows,
albums, in cinemas, airing today, airing tomorrow), not the items of one list. The user saw "missing dots" on Airing
today, which held one episode: its pager was a lone ring. The screensaver publishes Window(Home).Property(aeon.ss.pages)
(how many sections) and aeon.ss.page (the one on show, 1-based); the 40 pager images of Custom_1156_Screensaver.xml (Aeon:
ring / dot, Fused Glass: bar / circle) read those, and the pager hides while the rotation has a single section.
Replaces 0.56.20's aeon.ss.dots fallback. Runs once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Custom_1156_Screensaver.xml')
MARK = '0.56.20 ss_pager'
PAGE = 'Window(Home).Property(aeon.ss.page)'
PAGES = 'Window(Home).Property(aeon.ss.pages)'


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    n = 0
    out = []
    for line in t.split('\n'):
        m = re.search(r'<visible>(!?)Integer\.IsEqual\(Container\(9701\)\.CurrentItem,(\d+)\) \+ .*</visible>', line)
        if m and any(k in line for k in ('aeon_ring.png', 'aeon_dot.png', 'fg/circle.png', 'fg/bar.png')):
            k = m.group(2)
            if m.group(1):
                vis = '!String.IsEqual(%s,%s) + Integer.IsGreaterOrEqual(%s,%s)' % (PAGE, k, PAGES, k)
            else:
                vis = 'String.IsEqual(%s,%s)' % (PAGE, k)
            line = line[:m.start()] + '<visible>%s + Integer.IsGreater(%s,1)</visible>' % (vis, PAGES) + line[m.end():]
            n += 1
        out.append(line)
    assert n == 40, n
    t = '\n'.join(out)
    old = '<!-- pager dots (0.56.20: while the list reloads they stay, from the screensaver\'s aeon.ss.dots) -->'
    assert t.count(old) == 1
    t = t.replace(old, '<!-- pager dots (%s): one per section of the rotation (screensaver.aeon.fuse 1.2.2 aeon.ss.pages / aeon.ss.page), '
                       'the one on show ringed; hidden with a single section -->' % MARK)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    print('ok', n)


if __name__ == '__main__':
    main()
