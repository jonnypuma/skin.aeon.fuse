# -*- coding: utf-8 -*-
"""0.56.53 Sort and show only (canvas round 6 board SortFilter6; user: "build the panel with only the 9 sorts Kodi
accepts", then "needs to be fixed for tv shows and music too in the same style"): dialog 1179 replaces Kodi's Select
sort method from the side strip's Sort row in the Fused Glass style for Films, TV shows, Albums and Artists. Two
columns on the frame: Sort by (only the sorts Kodi accepts for that list - tested on the box 2026-11-20; two per line,
the one in use marked, OK again flips the order) and Show only (each filter with how many it leaves; genre / decade /
rating pick lists; clear all), the live count in the column head, the filters in force at the foot.

The strip's row sets Window(Home).Property(aeon.ss.kind) and opens 1179; the window loads that list's block
(include conditions are read at load). The logic is the helper's (resources/lib/sortshow.py, 0.3.121). Every other
list keeps Kodi's own sort list (SendClick(3)). Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

A = '$ADDON[skin.aeon.fuse %d]'
KINDS = [
    ('movies', 'videodb://movies/titles/', '$LOCALIZE[342]',
     [(29, 556), (16, 562), (40, 570), (9, 180), (17, 563), (18, 38018), (31, 20074), (42, 567), (41, 568)],
     [('unwatched', '$LOCALIZE[16101]'), ('inprogress', '$LOCALIZE[575]'), ('watched', '$LOCALIZE[16102]'), ('4k', '4K'),
      ('hdr', 'HDR / Dolby Vision'), ('versions', A % 32807), ('genre', '$LOCALIZE[515]'), ('decade', A % 32808),
      ('mpaa', '$LOCALIZE[20074]'), ('clear', A % 32809)]),
    ('tvshows', 'videodb://tvshows/titles/', '$LOCALIZE[20343]',
     [(29, 556), (16, 562), (40, 570), (17, 563), (18, 38018), (41, 568), (25, 20360)],
     [('unwatched', '$LOCALIZE[16101]'), ('inprogress', '$LOCALIZE[575]'), ('watched', '$LOCALIZE[16102]'),
      ('continuing', A % 32390), ('ended', A % 32391), ('genre', '$LOCALIZE[515]'), ('decade', A % 32808),
      ('mpaa', '$LOCALIZE[20074]'), ('clear', A % 32809)]),
    ('albums', 'musicdb://albums/', '$LOCALIZE[132]',
     [(12, 558), (10, 557), (11, 578), (16, 562), (17, 563), (18, 38018), (40, 570), (41, 568), (42, 567)],
     [('neverplayed', A % 32810), ('played', A % 32811), ('genre', '$LOCALIZE[515]'), ('decade', A % 32808), ('clear', A % 32809)]),
    ('artists', 'musicdb://artists/', '$LOCALIZE[133]',
     [(10, 557), (40, 570)],
     [('genre', '$LOCALIZE[515]'), ('clear', A % 32809)]),
]
PICKED = ('genre', 'decade', 'mpaa')
TOP = 190
H = 70
SX = [121, 545]
SW = [424, 425]
HX, HW = 971, 849


def button(cid, x, y, w, label, label2, nav, click, dot_vis):
    return (
        '<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>%s<visible>Control.HasFocus(%d) + $EXP[FGS_ShadowOn]</visible></control>'
        % (x - 40, y - 34, w + 80, H + 80, fw.SHADOW, cid) +
        '<control type="button" id="%d"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>st_ui_22_semibold</font>'
        '<textcolor>bfffffff</textcolor><focusedcolor>ffffffff</focusedcolor><align>left</align><aligny>center</aligny><textoffsetx>52</textoffsetx>'
        '<label>%s</label><label2>%s</label2><textcolor2>fg_mark</textcolor2>'
        '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus />%s<onclick>%s</onclick></control>'
        % (cid, x, y, w, H, label, label2, nav, click) +
        fw.img(x + 24, y + 30, 10, 10, 'fg/circle.png', 'fg_mark', dot_vis) +
        fw.line(x, y + H - 1, w))


def block(kind, lead, sorts, shows):
    out = ('<include name="SortShow_%s">' % kind +
           '<include content="FGS_DlgBack"/>' + fw.header(lead, A % 32803) +
           fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + ''.join(fw.line(x, 108, 1, 852) for x in (120, 970, 1820)) +
           fw.line(121, 189, 1699) +
           fw.label(145, 109, 400, 80, '[UPPERCASE]%s[/UPPERCASE]' % (A % 32804), 'st_cap_14', '80ffffff') +
           fw.label(545, 109, 400, 80, A % 32806, 'st_small_20', '99ffffff', 'right') +
           fw.label(995, 109, 400, 80, '[UPPERCASE]%s[/UPPERCASE]' % (A % 32805), 'st_cap_14', '80ffffff') +
           fw.label(1300, 109, 496, 80, '$INFO[Container.NumItems][COLOR 99ffffff]$INFO[Window(Home).Property(aeon.ss.total),  /  ][/COLOR]', 'st_ui_28_bold', 'fg_mark', 'right'))
    n, m = len(sorts), len(shows)
    for i, (sid, lab) in enumerate(sorts):
        r, c = divmod(i, 2)
        show_row = 9721 + min(r, m - 1)
        if not c:
            left = show_row
            right = 9711 + i + 1 if i + 1 < n else show_row
        else:
            left = 9711 + i - 1
            right = show_row
        up = 9711 + i - 2 if r else 'noop'
        down = 9711 + i + 2 if i + 2 < n else (9711 + n - 1 if i + 1 < n - 1 else 'noop')
        nav = '<onleft>%s</onleft><onright>%s</onright><onup>%s</onup><ondown>%s</ondown>' % (left, right, up, down)
        out += button(9711 + i, SX[c], TOP + r * H, SW[c], '$LOCALIZE[%d]' % lab, '$VAR[SortShow_Order%d]' % sid, nav,
                      'RunScript(script.aeon.helper,sortshow,sort,%d)' % sid,
                      'String.IsEqual(Window(Home).Property(aeon.ss.sort),%d)' % sid)
    for k, (key, lab) in enumerate(shows):
        srow = min(k, (n - 1) // 2)
        left = 9711 + srow * 2 + 1 if srow * 2 + 1 < n else 9711 + srow * 2
        nav = '<onleft>%d</onleft><onright>noop</onright><onup>%s</onup><ondown>%s</ondown>' % (
            left, 9721 + k - 1 if k else 'noop', 9721 + k + 1 if k + 1 < m else 'noop')
        if key == 'clear':
            label2 = ''
        elif key in PICKED:
            label2 = '$INFO[Window(Home).Property(aeon.ss.v.%s)]' % key
        else:
            label2 = '$INFO[Window(Home).Property(aeon.ss.n.%s)]' % key
        out += button(9721 + k, HX, TOP + k * H, HW, lab, label2, nav, 'RunScript(script.aeon.helper,sortshow,show,%s)' % key,
                      'false' if key == 'clear' else 'String.IsEqual(Window(Home).Property(aeon.ss.on.%s),1)' % key)
    out += fw.label(144, 976, 1660, 48, '$INFO[Window(Home).Property(aeon.ss.chips)]', 'st_ui_22_bold', 'fg_mark',
                    vis='!String.IsEmpty(Window(Home).Property(aeon.ss.chips))')
    return out + '</include>'


def window():
    inc = ''.join('\t\t<include condition="String.IsEqual(Window(Home).Property(aeon.ss.kind),%s)">SortShow_%s</include>\n' % (k[0], k[0]) for k in KINDS)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<!-- GENERATED by _src/sortshow_05653.py: Sort and show only (Films, TV shows, Albums, '
            'Artists; Fused Glass style). -->\n<window type="dialog" id="1179">\n\t<defaultcontrol always="true">9711</defaultcontrol>\n'
            '\t<onload>RunScript(script.aeon.helper,sortshow,open)</onload>\n\t<include>Anim_DialogOpenClose</include>\n\t<controls>\n'
            + inc + '\t</controls>\n</window>\n')


def variables():
    ids = sorted({sid for k in KINDS for sid, _ in k[3]})
    return ''.join('<variable name="SortShow_Order%d"><value condition="String.IsEqual(Window(Home).Property(aeon.ss.sort),%d)">$INFO[Container.SortOrder]</value>'
                   '<value></value></variable>' % (sid, sid) for sid in ids)


def strip():
    p = os.path.join(fw.D, 'Includes_LibraryPanel.xml')
    s = io.open(p, encoding='utf-8').read()
    # today's (or an earlier run's) Sort row clicks -> one per list
    old = re.search(r'(\t+)<onclick>Dialog\.Close\(1160,true\)</onclick>\n(?:\t+<onclick[^\n]*(?:SendClick\(3\)|ActivateWindow\(1179\)|aeon\.ss\.kind)[^\n]*</onclick>\n)+', s)
    assert old, 'sort row not found'
    t = old.group(1)
    conds = ['String.StartsWith(Container.FolderPath,%s)' % k[1] for k in KINDS]
    anyk = '$EXP[FGS] + [%s]' % ' | '.join(conds)
    new = t + '<onclick>Dialog.Close(1160,true)</onclick>\n'
    for k, c in zip(KINDS, conds):
        new += t + '<onclick condition="$EXP[FGS] + %s">SetProperty(aeon.ss.kind,%s,home)</onclick>\n' % (c, k[0])
    new += t + '<onclick condition="%s">ActivateWindow(1179)</onclick>\n' % anyk
    new += t + '<onclick condition="![%s]">SendClick(3)</onclick>\n' % anyk
    s = s[:old.start()] + new + s[old.end():]
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def main():
    io.open(os.path.join(fw.D, 'Custom_1179_SortShow.xml'), 'w', encoding='utf-8', newline='\n').write(window())
    fw.put('SortShow', variables() + ''.join(block(k[0], k[2], k[3], k[4]) for k in KINDS))
    strip()
    print('sort and show: dialog 1179 written (films, shows, albums, artists), strip row patched')


if __name__ == '__main__':
    main()
