# -*- coding: utf-8 -*-
"""0.56.6 Skin settings rows that only the Aeon and Glass themes use are hidden in Fused Glass (the user, 2026-11-16:
"the corner boxes setting for colors neutral fanart, backdrop - they're only used for Aeon theme aren't they?
shouldn't even be available to Fused Glass. Same with the Library side strip (Dark/White)").
  - Look > Library side strip (9524, Dark / White): Fused Glass draws its strip in FG_MenuPanel.
  - Appearance > Corner boxes (9747): the clock / weather boxes of the Aeon theme; Fused Glass has its clock rail.
Each row (and its focus bar) hides in Fused Glass; the rows under it (and their bars) move up a row there, and Up /
Down go round it. Same way as _src/fg_nostrip_perm.py (0.56.1, the permanent strip row 9525).
Run from the skin folder after _src/fg_nostrip_perm.py; safe to run again."""
import io
import os
import re

SS = os.path.join('1080i', 'SkinSettings.xml')
FG = '$EXP[Aeon_FGlass]'
UP = '<animation effect="slide" start="0,0" end="0,-70" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation>'
MARK = '<!-- 0.56.6 not in Fused Glass (_src/fg_aeon_only_rows.py) -->'
# hidden row: (rows under it that move up in Fused Glass, [(row, tag, old target, Fused Glass target)])
ROWS = {9524: ((9526, 9527, 9542, 9546, 9528, 9529), [(9523, 'ondown', 9524, 9526), (9526, 'onup', 9524, 9523)]),
        9747: ((9749, 9759, 9760), [(9746, 'ondown', 9747, 9749), (9749, 'onup', 9747, 9746)])}


def row_group(t, cid):
    i = t.find('<control type="button" id="%d">' % cid)
    return t.rfind('<control type="group">', 0, i)


def bar_visible(t, cid):
    """the <visible> of the row's focus bar group (left -119, drawn under the rows)"""
    for m in re.finditer(r'<visible>Control\.HasFocus\(%d\)[^<]*</visible>' % cid, t):
        if '<left>-119</left>' in t[max(0, m.start() - 400):m.start()]:
            return m
    return None


def run():
    t = io.open(SS, encoding='utf-8').read()
    for cid, (below, nav) in ROWS.items():
        g = row_group(t, cid)
        if MARK in t[g:g + 200]:
            print('row %d already hidden in Fused Glass' % cid)
            continue
        head = t[g:t.find('<control type="button" id="%d">' % cid, g)]
        assert '<visible>' not in head.split('<include')[0], cid
        t = t[:g] + '<control type="group">%s\n\t\t\t\t<visible>!%s</visible>' % (MARK, FG) + t[g + len('<control type="group">'):]
        m = bar_visible(t, cid)
        assert m, ('bar', cid)
        t = t[:m.start()] + m.group(0).replace('</visible>', ' + !%s</visible>' % FG) + t[m.end():]
        for b in below:
            g = row_group(t, b)
            t = t[:g] + '<control type="group">' + UP + t[g + len('<control type="group">'):]
            m = bar_visible(t, b)
            assert m, ('bar', b)
            t = t[:m.start()] + UP + t[m.start():]
        for rid, tag, old, to in nav:
            i = t.find('<control type="button" id="%d">' % rid)
            e = t.find('</control>', i)
            blk = t[i:e]
            o = '<%s>%d</%s>' % (tag, old, tag)
            if o in blk:
                blk = blk.replace(o, '<%s condition="%s">%d</%s><%s condition="!%s">%d</%s>' % (tag, FG, to, tag, tag, FG, old, tag), 1)
            else:                                   # already conditional: the Fused Glass branch goes round the row
                o = '<%s condition="%s">%d</%s>' % (tag, FG, old, tag)
                assert o in blk, (rid, tag)
                blk = blk.replace(o, '<%s condition="%s">%d</%s>' % (tag, FG, to, tag), 1)
            t = t[:i] + blk + t[e:]
        print('row %d hidden in Fused Glass; %s up a row there' % (cid, ', '.join(map(str, below))))
    io.open(SS, 'w', encoding='utf-8', newline='\n').write(t)


if __name__ == '__main__':
    run()
