# -*- coding: utf-8 -*-
"""0.56.53 Fused Glass info panels: the media chip lines (resolution / audio ... and the sidecar line chipline2 added)
only for a film, an episode or a music video. A grouplist whose chips are all hidden still takes its height in the
panel's vertical grouplist: for a season the two empty lines pushed the plot out of the column, so it was never
drawn (box, 2026-11-19, Banner list). Every grouplist of a FG_V<N>_View that holds media chips (VideoResolution or
the sidecar's aeon.mi.path) and has no type condition of its own gets one. Run after chipline2 / sidechips (and
before seasonplot, any order). Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import settings_sections as ss  # noqa: E402

P = os.path.join(HERE, '..', '1080i', 'Includes_Fused.xml')
MARK = '<!-- 0.56.53 media lines: films / episodes only -->'


def main():
    s = io.open(P, encoding='utf-8').read()
    if MARK in s:
        print('media gate: already there')
        return
    total = []
    for inc in re.finditer(r'<include name="FG_V(\d+)_View">', s):
        pass
    names = re.findall(r'<include name="(FG_V(\d+)_View)">', s)
    for name, n in names:
        a = s.index('<include name="%s">' % name)
        b = s.find('<include name=', a + 10)
        b = len(s) if b < 0 else b
        seg = s[a:b]
        m = ss.masked(seg)
        cond = ('[String.IsEqual(Container(%s).ListItem.DBType,movie) | String.IsEqual(Container(%s).ListItem.DBType,episode) | '
                'String.IsEqual(Container(%s).ListItem.DBType,musicvideo)]' % (n, n, n))
        starts = [x.start() for x in re.finditer(r'<control type="grouplist">', seg)]
        k = 0
        for st in reversed(starts):
            e = ss.ctl_end(m, st)
            x = seg[st:e]
            first = x.find('<control', 10)
            if first < 0:
                continue
            head = x[:first]
            if 'type="grouplist"' in x[10:] and '<orientation>vertical</orientation>' in head:
                continue                                   # a whole column, not a line
            if 'DBType' in head or 'Container(%s).ListItem.VideoResolution' % n not in x and 'aeon.mi.path' not in x:
                continue
            if 'ListItem.Rating' in x or 'FG_Ver_' in x:
                continue                                   # the ratings / status lines hold more than media
            seg = seg[:st + first] + '<visible>%s</visible>' % cond + seg[st + first:]
            k += 1
        if k:
            s = s[:a] + seg + s[b:]
            total.append('%s:%d' % (n, k))
    i = s.rindex('</includes>')
    s = s[:i] + '\t' + MARK + '\n' + s[i:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('media gate: %s' % ' '.join(total))


if __name__ == '__main__':
    main()
