# -*- coding: utf-8 -*-
"""0.56.42 Skin settings in the categories the user approved (2026-11-18):
  Theme & style, Home, Home menu, Libraries, Information, Widget & Spotlight screens, Player, Music player,
  Screensaver & backdrops, System, Context menu.
The user: "regroup Skin settings like proposed but Widget screens <-- shouldn't it be Widget & Spotlight screens??"

Every page with rows (the old Appearance, Look, Details, Ratings, Playback, OSD settings, Backgrounds, Spotlight &
widgets, Motion pages) is taken apart and the rows go into nine scrolling lists (70 px items: focus bar at left 41,
row at left 160, the row's visibility on the item; settings_sections.py explains the layout). Up / Down are written
again from the new order (each button names the rows after / before it with their visibility, first true wins).
Home menu and Context menu stay as they are. The preview cards (skin_previews.py) are split per row and put together
again per new page, so the fgs / shadow generators that changed them do not need to run again.
The category list gets the new order, names, icons and Right targets; long names wrap to two lines.
Run from the skin folder. Runs once (stops when the Libraries list 9777 is there)."""
import io
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings_sections as ss  # noqa: E402

P = ss.P
A = '$ADDON[skin.aeon.fuse %d]'
SOURCE = ['look', 'playback', 'motion', 'appearance', 'details', 'ratings', 'behaviour', 'backgrounds', 'widgets']
NEVER = {9520}                       # visible false (an old row kept for its id)


def H(label):
    return ('H', label)


# key, category id, list id, scroll bar id, rows (H = a heading over the rows after it, hidden when none of them shows)
PAGES = [
    ('appearance', 9600, 9770, 9771, [9744, 9748, H('$VAR[Aeon_SetThemeName]'), 9798, 9529, 9749, 9759, 9528, 9791, 9792, 9793,
                                      9740, 9760, H(A % 32604), 9542, 9790, 9797]),
    ('home', 9551, 9772, 9773, [9746, 9546, 9766, 9764, 9737, 9743, 9755, 9733, 9765]),    # + 9517 after 9743, 9516 after 9765 (rows_05642.py)
    ('libraries', 9567, 9777, 9778, [9745, 9767, 9794, 9795, 9796, 9747, 9524, 9525, 9547, 9521, 9520, 9522, 9523, 9526, 9527,
                                     9781, 9723, 9726]),
    ('details', 9566, 9774, 9775, [9703, 9704, 9705, 9761, 9709, 9707, 9706, 9708, 9700, 9701, 9702, 9780, 9776,
                                   H('$LOCALIZE[31541]'), 9768, 9710, 9711, 9712, 9713, 9714]),
    ('widgets', 9601, 9782, 9783, [9753, 9754, 9757, 9756, 9758, 9750, 9751, 9752, 9779]),
    ('playback', 9552, 9784, 9785, [9530, 9720, 9721, 9722, 9537, 9724, 9725, 9531, 9532, 9533, 9538, 9539,
                                    9727, 9728, 9738, 9739, 9729]),
    ('music', 9568, 9786, 9787, [9534, 9535, 9536, 9762, 9550, 9579, 9763, 9732]),
    ('backgrounds', 9569, 9788, 9789, [9741, 9742, 9736, 9734, 9735, 9730, 9731]),
    ('motion', 9553, 9769, 9799, [9540, 9548, 9549, 9543, 9544, 9545, 9541]),             # + 9513, 9514 after 9545 (rows_05642.py)
]
# the category column, top to bottom: id, key, label, icon, Right goes to
CATS = [
    (9600, 'appearance', '$LOCALIZE[31725]', 'aeon/icons/sun.png', 9744),        # Theme & style
    (9551, 'home', '$LOCALIZE[10000]', 'aeon/icons/home.png', 9746),             # Home (Kodi's string)
    (9558, 'homemenu', '$LOCALIZE[31732]', 'aeon/icons/lines.png', 9641),        # Home menu
    (9567, 'libraries', A % 32722, 'aeon/icons/film.png', 9745),                 # Libraries
    (9566, 'details', A % 32723, 'aeon/icons/info.png', 9703),                   # Information
    (9601, 'widgets', '$LOCALIZE[31730]', 'aeon/icons/tv.png', 9753),            # Widget & Spotlight screens
    (9552, 'playback', '$LOCALIZE[31727]', 'aeon/icons/play.png', 9530),         # Player
    (9568, 'music', '$LOCALIZE[31728]', 'aeon/icons/music.png', 9534),           # Music player
    (9569, 'backgrounds', A % 32724, 'aeon/icons/image.png', 9741),              # Screensaver & backdrops
    (9553, 'motion', '$LOCALIZE[31731]', 'aeon/icons/settings.png', 9540),       # System
    (9559, 'ctxmenu', '$LOCALIZE[10106]', 'aeon/icons/stack.png', 9672),         # Context menu
]
CAT_NAME = [('appearance', '$LOCALIZE[31725]'), ('home', '$LOCALIZE[10000]'), ('libraries', A % 32722),
            ('details', A % 32723), ('playback', '$LOCALIZE[31727]'), ('music', '$LOCALIZE[31728]'),
            ('backgrounds', A % 32724), ('widgets', '$LOCALIZE[31730]'), ('motion', '$LOCALIZE[31731]'),
            ('rows', '$LOCALIZE[31940]'), ('homemenu', '$LOCALIZE[31732]'), ('ctxmenu', '$LOCALIZE[10106]')]
SUB = os.path.join('1080i', 'Includes_Aeon_Sub.xml')
SET = os.path.join('1080i', 'Includes_Settings.xml')
PV_BEGIN, PV_END = '<!-- PREVIEW CARD %s (_src/skin_previews.py) -->', '<!-- /PREVIEW CARD %s -->'


def button_of(mb):
    for ka, kb in ss.children(mb, 0, len(mb)):
        x = re.match(r'<control type="button" id="(\d+)">', mb[ka:kb])
        if x:
            return int(x.group(1))
    return None


def collect(t):
    """rows {id: (item text without nav, visibility)}, previews {id: group text}, the old pages' spans"""
    m = ss.masked(t)
    items, bars, fixed, spans = {}, {}, {}, []
    for page in SOURCE:
        s, e = ss.page_span(t, m, page)
        spans.append((page, s, e))
        for a, b in ss.children(m, s, e):
            blk, mb = t[a:b], m[a:b]
            if re.match(r'<control type="grouplist"', blk):
                for ia, ib in ss.children(m, a, b):
                    it, mit = t[ia:ib], m[ia:ib]
                    btns = re.findall(r'<control type="button" id="(\d+)">', mit)     # item > row group > button
                    if not btns:
                        continue                   # a heading, built again
                    assert len(btns) == 1, btns
                    r = int(btns[0])
                    assert r not in items, r
                    items[r] = (it, ss.own_visible(it))
                continue
            r = button_of(mb)
            vis = ss.own_visible(blk) or ''
            fb = re.match(r'Control\.HasFocus\((\d+)\)', vis)      # the memory rows' bars add + $EXP[Aeon_MemTrimRows]
            if r is not None:
                fixed[r] = blk
            elif fb and '<left>-119</left>' in blk[:ss.props(blk)[1]]:
                bars[int(fb.group(1))] = blk
    for r, blk in fixed.items():
        head, p, rest = ss.strip_props(blk, False)
        assert '<left>' not in p, r
        rowg = head + '<left>160</left><top>0</top>' + p + rest
        part = ['\t<control type="group"><!-- row %d -->' % r, '\t\t<width>1100</width><height>70</height>']
        vis = ss.own_visible(blk)
        if vis:
            part.append('\t\t<visible>%s</visible>' % vis)
        if r in bars:
            bh, bp, brest = ss.strip_props(bars[r], True)
            part.append(bh + '<left>41</left><top>0</top><visible>%s</visible>' % ss.own_visible(bars[r]) + bp + brest)
        elif r not in NEVER:
            raise AssertionError(('no focus bar', r))
        part.append(rowg)
        part.append('\t</control>')
        assert r not in items, r
        items[r] = ('\n'.join(part), vis)
    previews = {}
    for x in re.finditer(r'<!-- PREVIEW CARD (\w+) \(_src/skin_previews.py\) -->(.*?)<!-- /PREVIEW CARD \1 -->', t, re.S):
        if x.group(1) not in SOURCE:
            continue
        body = x.group(2)
        i = body.index('<!-- preview:')
        tail = body.rindex('</control></control>')
        parts = re.split(r'<!-- preview:(\d+) -->\n?', body[i:tail])
        for k in range(1, len(parts), 2):
            previews[int(parts[k])] = parts[k + 1].strip()
    return items, previews, spans


def card_head(t):
    x = re.search(r'<!-- PREVIEW CARD appearance \(_src/skin_previews.py\) -->(.*?)<!-- preview:', t, re.S)
    return x.group(1)


def main():
    t = ss.read(P)
    if 'id="9777"' in t:
        print('already done')
        return
    items, previews, spans = collect(t)
    want = [r for _, _, _, _, order in PAGES for r in order if isinstance(r, int)]
    assert len(want) == len(set(want)), 'a row twice'
    assert set(want) == set(items), ('rows not placed', sorted(set(items) - set(want)), 'unknown', sorted(set(want) - set(items)))
    vis = dict((r, items[r][1]) for r in want)
    vis.update((r, 'false') for r in NEVER)
    head = card_head(t)

    def nav(order, r):
        ids = [x for x in order if isinstance(x, int) and x not in NEVER]
        i = ids.index(r)
        out = []
        for tag, step in (('onup', -1), ('ondown', 1)):
            k = i
            for _ in range(len(ids) - 1):
                k = (k + step) % len(ids)
                c = vis[ids[k]]
                if c:
                    out.append('<%s condition="%s">%d</%s>' % (tag, c, ids[k], tag))
                else:
                    out.append('<%s>%d</%s>' % (tag, ids[k], tag))
                    break
        return ''.join(out)

    def heading(label, cond):
        return ('<control type="group"><width>1100</width><height>70</height>%s'
                # the heading as fgs_grid_05631 left it: a rule above and 101 px left in the Fused Glass style
                '<control type="image"><left>41</left><top>0</top><width>1019</width><height>1</height><texture colordiffuse="12ffffff">common/white.png</texture><visible>$EXP[FGS]</visible></control>'
                '<control type="label"><left>162</left><top>28</top><animation effect="slide" start="0,0" end="-101,0" time="0" condition="$EXP[FGS]">Conditional</animation><width>840</width><height>40</height><aligny>center</aligny>'
                '<font>st_cap_20</font><textcolor>$VAR[Aeon_Accent]</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label></control>'
                '</control>' % ('<visible>%s</visible>' % cond if cond else '', label))

    gl = re.search(r'<control type="grouplist" id="9770">(.*?)<control type="group">', t, re.S).group(0)
    gl_head = gl[:gl.rindex('<control type="group">')]
    sb = re.search(r'<control type="scrollbar" id="9771">.*?</control>', t, re.S).group(0)

    def build(key, cat, gid, sid, order):
        o = []
        rows = [r for r in order if isinstance(r, int)]
        pv = [r for r in rows if r in previews]
        if pv:
            o.append(PV_BEGIN % key)
            cond = ' | '.join('Control.HasFocus(%d)' % r for r in pv)
            o.append(re.sub(r'<visible>[^<]*</visible>', '<visible>%s</visible>' % cond, head.strip('\n'), count=1))
            for r in pv:
                o.append('<!-- preview:%d -->' % r)
                o.append(previews[r])
            o.append('</control></control>')
            o.append(PV_END % key)
        o.append('\t\t\t<include>Aeon_PageIn</include>')
        g = gl_head.replace('id="9770"', 'id="%d"' % gid).replace('<pagecontrol>9771</pagecontrol>', '<pagecontrol>%d</pagecontrol>' % sid)
        g = g.replace('<onleft>9600</onleft>', '<onleft>%d</onleft>' % cat)
        g = g.replace('_src/settings_sections.py; appearance', '_src/regroup_05642.py; %s' % key)
        o.append('<!-- 0.56.42 rows in a list that scrolls (_src/regroup_05642.py; %s) -->' % key)
        o.append(g.rstrip())
        for n, r in enumerate(order):
            if not isinstance(r, int):
                section = []
                for x in order[n + 1:]:
                    if not isinstance(x, int):
                        break
                    section.append(x)
                conds = [vis[x] for x in section if x not in NEVER]
                cond = None if any(not c for c in conds) else ' | '.join('[%s]' % c for c in conds)
                o.append('\t' + heading(r[1], cond))
                continue
            it = items[r][0]
            b = it.index('<control type="button" id="%d">' % r)
            be = it.index('</control>', b)
            btn = it[b:be]
            btn = re.sub(r'\s*<onup[^>]*>[^<]*</onup>', '', btn)
            btn = re.sub(r'\s*<ondown[^>]*>[^<]*</ondown>', '', btn)
            btn = re.sub(r'<onback>9\d\d\d</onback>', '<onback>%d</onback>' % cat, btn)
            btn = re.sub(r'<onleft>SetFocus\(9\d\d\d\)</onleft>', '<onleft>SetFocus(%d)</onleft>' % cat, btn)
            assert '<onback>%d</onback>' % cat in btn and 'SetFocus(%d)' % cat in btn, r
            if r not in NEVER:
                k = btn.index('>') + 1
                btn = btn[:k] + '\n\t\t\t\t\t' + nav(order, r) + btn[k:]
            o.append(it[:b] + btn + it[be:])
        o.append('</control>')
        o.append(sb.replace('id="9771"', 'id="%d"' % sid).replace('<onleft>9770</onleft>', '<onleft>%d</onleft>' % gid))
        return ('<control type="group">\n\t\t\t<left>600</left>\n'
                '\t\t\t<animation effect="slide" start="0,0" end="20,0" time="0" condition="$EXP[Aeon_FGlass] + !$EXP[FGS]">Conditional</animation>\n'
                '\t\t\t<visible>String.IsEqual(Window(Home).Property(aeon.skincat),%s)</visible>\n' % key
                + '\n'.join(o) + '\n\t\t</control>')

    pages = '\n\t\t'.join(build(*p) for p in PAGES)
    # the old pages out (from the back), the new ones where Look was (right after the category column)
    # the newline before the first page taken out: nothing before it changes
    ins = t.rfind('\n', 0, min(s for _, s, _ in spans))
    for _, s, e in sorted(spans, key=lambda x: -x[1]):
        ls = t.rfind('\n', 0, s)
        t = t[:ls] + t[e:]
    t = t[:ins] + '\n\t\t<!-- 0.56.42 the settings pages (_src/regroup_05642.py) -->\n\t\t' + pages + t[ins:]

    # the category column
    for n, (cid, key, label, icon, right) in enumerate(CATS):
        top = 199 + 70 * n
        x = re.search(r'<include content="Dlg_SkinCategory">\s*<param name="id" value="%d"/>.*?</include>' % cid, t, re.S)
        assert x, cid
        up, down = CATS[n - 1][0], CATS[(n + 1) % len(CATS)][0]
        new = ('<include content="Dlg_SkinCategory">\n'
               '\t\t\t\t<param name="id" value="%d"/><param name="top" value="%d"/>%s\n'
               '\t\t\t\t<param name="label" value="%s"/><param name="key" value="%s"/><param name="icon" value="%s"/>\n'
               '\t\t\t\t<param name="onright" value="%d"/><param name="onup" value="%d"/><param name="ondown" value="%d"/>\n'
               '\t\t\t</include>' % (cid, top, '<param name="corner" value="true"/>' if n == len(CATS) - 1 else '',
                                     label, key, icon, right, up, down))
        t = t[:x.start()] + new + t[x.end():]
        y = re.search(r'(<control type="group">\s*<left>0</left>\s*<top>)(\d+)(</top>\s*<visible>Control\.HasFocus\(%d\)</visible>)' % cid, t)
        assert y, ('focus bar', cid)
        t = t[:y.start(2)] + str(top) + t[y.end(2):]
    # the category includes in the order they are drawn (Kodi draws in file order; the list reads top to bottom)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)

    # the title band names
    s = ss.read(SUB)
    x = re.search(r'<variable name="Aeon_SkinCatName">.*?</variable>', s, re.S)
    s = s[:x.start()] + '<variable name="Aeon_SkinCatName">\n' + ''.join(
        '\t\t<value condition="String.IsEqual(Window(Home).Property(aeon.skincat),%s)">%s</value>\n' % kv for kv in CAT_NAME) + '\t</variable>' + s[x.end():]
    io.open(SUB, 'w', encoding='utf-8', newline='\n').write(s)
    ET.parse(SUB)

    # long category names wrap to two lines
    c = ss.read(SET)
    i = c.index('<include name="Dlg_SkinCategory">')
    j = c.index('</include>\n', c.index('</definition>', i))
    blk = c[i:j]
    if '<wrapmultiline>' not in blk:
        blk = blk.replace('<label>$PARAM[label]</label>', '<label>$PARAM[label]</label><wrapmultiline>true</wrapmultiline>')
        c = c[:i] + blk + c[j:]
        io.open(SET, 'w', encoding='utf-8', newline='\n').write(c)
    ET.parse(SET)
    print('ok', dict((p[0], len([r for r in p[4] if isinstance(r, int)])) for p in PAGES))


if __name__ == '__main__':
    main()
