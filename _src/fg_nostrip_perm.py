# -*- coding: utf-8 -*-
"""0.56.1 The permanent settings strip is for Aeon and Glass only (the user: "The option to set Settings strip permanent
is an option we cannot use with Fused Glass, the strip in Fused Glass is too wide and cannot permanently cover other
stuff. it's only applicable to Aeon and Glass themes").

- Aeon_StripPerm is never true in Fused Glass, so a "Permanent" chosen in Aeon / Glass (or per view) leaves the Fused
  Glass views alone: the strip slides in over them with Left or the Menu key, as it does by default.
- Skin settings > Look > Settings strip (row 9525) is hidden in Fused Glass; the rows under it (and their focus bars)
  move up a row there, and Up / Down go round it.
- View settings: the per-view "Settings strip" item is hidden in Fused Glass.
Run from the skin folder; safe to run again."""
import io
import os
import re

SS = os.path.join('1080i', 'SkinSettings.xml')
FG = '$EXP[Aeon_FGlass]'
UP = '<animation effect="slide" start="0,0" end="0,-70" time="0" condition="$EXP[Aeon_FGlass]">Conditional</animation>'
BELOW = (9524, 9526, 9527, 9542, 9546, 9528, 9529)


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


def expression():
    p = os.path.join('1080i', 'Includes_Aeon_Sub.xml')
    t = rd(p)
    old = '<expression name="Aeon_StripPerm">[String.IsEqual(Window(Home).Property(aeon.vo.strip),on)'
    if '<expression name="Aeon_StripPerm">!Skin.HasSetting(aeon.fglass) + ' in t:
        return
    assert t.count(old) == 1
    t = t.replace(old, '<expression name="Aeon_StripPerm">!Skin.HasSetting(aeon.fglass) + [String.IsEqual(Window(Home).Property(aeon.vo.strip),on)', 1)
    # close the outer bracket that now wraps the old expression
    i = t.find('<expression name="Aeon_StripPerm">')
    j = t.find('</expression>', i)
    t = t[:j] + ']' + t[j:]
    wr(p, t)
    print('Aeon_StripPerm: off in Fused Glass')


def row_group(t, cid):
    i = t.find('<control type="button" id="%d">' % cid)
    return t.rfind('<control type="group">', 0, i)


def bar_group(t, cid):
    m = re.search(r'<control type="group">\n\t\t\t\t<left>-119</left>\n\t\t\t\t<top>\d+</top>\n\t\t\t\t<visible>Control\.HasFocus\(%d\)[^<]*</visible>' % cid, t)
    return m


def settings():
    t = rd(SS)
    if 'fg_nostrip_perm' in t:
        print('Skin settings already done')
        return
    # the row: hidden in Fused Glass
    g = row_group(t, 9525)
    head = t[g:t.find('<include content="Dlg_SkinRowChrome">', g)]
    assert '<visible>' not in head
    t = t[:g] + '<control type="group"><!-- 0.56.1 not in Fused Glass (_src/fg_nostrip_perm.py) -->\n\t\t\t\t<visible>!%s</visible>' % FG + t[g + len('<control type="group">'):]
    m = bar_group(t, 9525)
    t = t[:m.start()] + m.group(0).replace('<visible>Control.HasFocus(9525)</visible>', '<visible>Control.HasFocus(9525) + !%s</visible>' % FG) + t[m.end():]
    # the rows under it and their bars: up a row in Fused Glass
    for cid in BELOW:
        g = row_group(t, cid)
        t = t[:g] + '<control type="group">' + UP + t[g + len('<control type="group">'):]
        m = bar_group(t, cid)
        assert m, cid
        t = t[:m.start()] + m.group(0).replace('<left>-119</left>', '<left>-119</left>' + UP, 1) + t[m.end():]
    # Up / Down round the hidden row
    for cid, tag, old, fg_to in ((9523, 'ondown', 9525, 9524), (9524, 'onup', 9525, 9523)):
        i = t.find('<control type="button" id="%d">' % cid)
        e = t.find('</control>', i)
        b = t[i:e]
        o = '<%s>%d</%s>' % (tag, old, tag)
        assert b.count(o) == 1, (cid, tag)
        b = b.replace(o, '<%s condition="%s">%d</%s><%s condition="!%s">%d</%s>' % (tag, FG, fg_to, tag, tag, FG, old, tag))
        t = t[:i] + b + t[e:]
    wr(SS, t)
    print('Skin settings: Settings strip hidden in Fused Glass, rows under it moved up')


def view_settings():
    p = os.path.join('1080i', 'Includes_LibraryPanel.xml')
    t = rd(p)
    old = ('<label>$LOCALIZE[31800]</label>\n\t\t\t\t\t\t<label2>$VAR[Aeon_VOS_strip]</label2>')
    assert t.count(old) == 1, 'view settings strip item'
    i = t.find(old)
    e = t.find('</item>', i)
    if '<visible>' in t[i:e]:
        return
    t = t[:e] + '\t<visible>!Skin.HasSetting(aeon.fglass)</visible>\n\t\t\t\t\t' + t[e:]
    wr(p, t)
    print('View settings: strip item hidden in Fused Glass')


if __name__ == '__main__':
    expression()
    settings()
    view_settings()
