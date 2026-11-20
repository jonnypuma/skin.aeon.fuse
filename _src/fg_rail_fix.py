# -*- coding: utf-8 -*-
"""0.56.6 the A-Z rail of every Fused Glass view.

The user (2026-11-16): "Artist wall, the A-Z strip, when standing on the # character, the white circle highlight is
clipping with the clock/weather section on the top."
  - the white focus circle (36 px) is wider than a letter row (26 px) and a list cuts its rows at its own edges, so on
    # (and Z) the circle lost its top (bottom). It is drawn outside the list now, under it: one circle per letter slot
    (1850, 211 + 26 k), shown for the slot of the focused letter (Container(rail).Position).
  - # jumped to the List view's list (SetFocus(510,0,absolute)) in every view; now to the view's own list.
fg_lib.rail() writes the same from now on; this patches the views as they are. Run from the skin folder; safe to run
again."""
import io
import os
import re

FUSED = os.path.join('1080i', 'Includes_Fused.xml')
CIRCLE = ('<control type="image"><left>14</left><top>-5</top><width>36</width><height>36</height><texture colordiffuse="ffffffff">'
          'fg/circle.png</texture><visible>Control.HasFocus(%d)</visible></control>')


def slots(az, n):
    return ''.join('<control type="image"><left>1850</left><top>%d</top><width>36</width><height>36</height><texture colordiffuse="ffffffff">'
                   'fg/circle.png</texture><visible>Control.HasFocus(%d) + Integer.IsEqual(Container(%d).Position,%d)</visible></control>'
                   % (211 + 26 * k, az, az, k) for k in range(n))


def run():
    t = io.open(FUSED, encoding='utf-8').read()
    out, pos, n_c, n_h = [], 0, 0, 0
    for m in re.finditer(r'<include name="FG_V(\d+)_View">', t):
        view = int(m.group(1))
        b = t.find('\n\t</include>', m.end())
        r = re.search(r'<control type="list" id="(\d+)"><left>1836</left><top>216</top><width>64</width><height>702</height>', t[m.end():b])
        if not r:
            continue
        az = int(r.group(1))
        s = m.end() + r.start()
        e = t.find('</control>', t.find('</content>', s)) + len('</control>')
        rail = t[s:e]
        circle = CIRCLE % az
        new = rail
        if circle in new:
            new = new.replace(circle, '')
            n_c += 1
            pre = slots(az, (702 // 26))
        else:
            pre = ''
        if '<item><label>#</label><onclick>SetFocus(510,0,absolute)</onclick>' in new and view != 510:
            new = new.replace('<item><label>#</label><onclick>SetFocus(510,0,absolute)</onclick>',
                              '<item><label>#</label><onclick>SetFocus(%d,0,absolute)</onclick>' % view)
            n_h += 1
        out.append(t[pos:s] + pre + new)
        pos = e
    out.append(t[pos:])
    t = ''.join(out)
    io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    print('rails: %d focus circles outside the list, %d # jumps to the own list' % (n_c, n_h))


if __name__ == '__main__':
    run()
