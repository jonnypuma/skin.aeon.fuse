# -*- coding: utf-8 -*-
"""0.56.12 Skin settings > Appearance and Look: rows in scrolling lists, the theme's own options together.

The user (2026-11-16): "We need to call the Material option Library view theme and it should really be next to Menu
theme in the options. Create scrollbar if needed due to amount of options. Also try and gather Aeon/Glass theme
specific options together, Fused Glass theme options together and then have a shared subsection."

Before: every row a group at a fixed top (191 + 70 n) with conditional slides to close the gaps of hidden rows, its
focus bar a separate group at the same top, Up / Down chained by hand.
Now both pages are a vertical grouplist (Appearance 9770 with scroll bar 9771, Look 9772 with 9773), each row one
group of the list (its focus bar first, then the row moved 160 right, so the bar's shadow fits in the list), so hidden
rows take no room and the list scrolls when the rows do not fit:
  Appearance:  Skin theme
               <THEME NAME>   Menu theme, Library view theme (was Look > Material) and the other rows that belong to
                              the theme in use (Fused Glass rows, or the Aeon / Glass rows; those moved here from Look)
               ALL THEMES     the rows every theme has
  Look:        the rows every theme has (Watched indicators ... Fonts)
Up / Down: each button names the rows after / before it in order with their visibility as the condition (Kodi takes
the first whose condition is true), so hidden rows are skipped and the ends wrap.
Run from the skin folder, then python _src/skin_previews.py and python _src/ok_only.py. Runs once (it stops when the
lists are there)."""
import io
import os
import re
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'SkinSettings.xml')
HELP = os.path.join('1080i', 'Includes_Settings.xml')
A = '$ADDON[skin.aeon.fuse %d]'
FG = '$EXP[Aeon_FGlass]'
ALL_THEMES = 32604

APPEARANCE = [9744, 'THEME', 9748, 9529, 9749, 9759, 9546, 9528, 9740, 9760, 9747, 9524, 9525, 9547, 9743,
              'ALL', 9741, 9742, 9745, 9746]
LOOK = [9520, 9521, 9522, 9523, 9526, 9527, 9542]
PAGES = (('appearance', 9600, APPEARANCE, 9770, 9771), ('look', 9551, LOOK, 9772, 9773))
# rows whose visibility changes here: Now playing on Home was shown greyed out in Fused Glass, it belongs to the
# Aeon / Glass rows now
SET_VIS = {9743: '!' + FG}
NEVER = {9520}                      # visible false (an old row kept for its id)


def read(p):
    return io.open(p, encoding='utf-8').read()


def masked(t):
    """the text with comments blanked out (same length), so <control in a comment is not counted"""
    return re.sub(r'<!--.*?-->', lambda m: ' ' * len(m.group(0)), t, flags=re.S)


def ctl_end(m, start):
    depth = 0
    for x in re.finditer(r'<control[ >]|</control>', m[start:]):
        depth += -1 if x.group(0) == '</control>' else 1
        if depth == 0:
            return start + x.end()
    raise ValueError('unbalanced at %d' % start)


def children(m, start, end):
    """(start, end) of the direct child controls of the control at start"""
    out = []
    i = m.index('>', start) + 1
    while True:
        x = re.compile(r'<control[ >]').search(m, i, end)
        if not x:
            return out
        e = ctl_end(m, x.start())
        out.append((x.start(), e))
        i = e


def page_span(t, m, page):
    v = m.index('<visible>String.IsEqual(Window(Home).Property(aeon.skincat),%s)</visible>' % page)
    s = m.rfind('<control type="group">', 0, v)
    return s, ctl_end(m, s)


def props(block):
    """the block's own settings: from its opening tag to its first child control"""
    mb = masked(block)
    o = mb.index('>') + 1
    x = re.compile(r'<control[ >]').search(mb, o)
    return o, (x.start() if x else len(block) - len('</control>'))


SLIDE = re.compile(r'<animation effect="slide"[^>]*time="0"[^>]*condition="[^"]*">Conditional</animation>')


def own_visible(block):
    o, c = props(block)
    v = re.search(r'<visible>(.*?)</visible>', block[o:c])
    return v.group(1) if v else None


def strip_props(block, drop_left):
    o, c = props(block)
    p = block[o:c]
    p = re.sub(r'<visible>.*?</visible>', '', p, count=1)
    p = re.sub(r'<top>-?\d+</top>', '', p, count=1)
    if drop_left:
        p = re.sub(r'<left>-?\d+</left>', '', p, count=1)
    p = SLIDE.sub('', p)
    return block[:o], p, block[c:]


def page_of(gid):
    return {9770: 'appearance', 9772: 'look', 9774: 'details 0.56.20'}.get(gid, str(gid))


def main(pages=None, done='id="9770"'):
    """0.56.20: pages / done as parameters, so _src/settings_details_05620.py turns Details into a list too"""
    PAGES_ = pages or PAGES
    t = read(P)
    if done in t:
        print('already done')
        return
    rows, bars = {}, {}
    spans = []
    for page, cat, _, _, _ in PAGES_:
        m = masked(t)
        s, e = page_span(t, m, page)
        spans.append((page, s, e))
        for a, b in children(m, s, e):
            block = t[a:b]
            mb = m[a:b]
            kids = children(mb, 0, len(mb))
            btn = None
            for ka, kb in kids:
                x = re.match(r'<control type="button" id="(\d+)">', mb[ka:kb])
                if x:
                    btn = int(x.group(1))
            vis = own_visible(block) or ''
            fb = re.match(r'Control\.HasFocus\((\d+)\)', vis)
            if btn is not None:
                rows[btn] = (page, a, b, block)
            elif fb and '<left>-119</left>' in block[:props(block)[1]]:
                bars[int(fb.group(1))] = (page, a, b, block)
    want = [r for _, _, order, _, _ in PAGES_ for r in order if isinstance(r, int)]
    missing = [r for r in want if r not in rows]
    assert not missing, ('rows not found', missing)
    have = set(r for r in rows if rows[r][0] in [p[0] for p in PAGES_])
    assert have == set(want), ('rows not placed', sorted(have - set(want)))
    nobar = [r for r in want if r not in bars and r not in NEVER]
    assert not nobar, ('no focus bar', nobar)

    vis = dict((r, SET_VIS.get(r, own_visible(rows[r][3]))) for r in want)
    vis.update((r, 'false') for r in NEVER)

    def nav(order, r, cat):
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

    def heading(label, cond=None):
        return ('<control type="group"><width>1100</width><height>70</height>%s'
                '<control type="label"><left>162</left><top>28</top><width>840</width><height>40</height><aligny>center</aligny>'
                '<font>st_cap_20</font><textcolor>$VAR[Aeon_Accent]</textcolor><label>[UPPERCASE]%s[/UPPERCASE]</label></control>'
                '</control>' % ('<visible>%s</visible>' % cond if cond else '', label))

    def build(order, cat, gid, sid):
        o = ['<!-- 0.56.12 rows in a list that scrolls (_src/settings_sections.py; %s) -->' % page_of(gid),
             '<control type="grouplist" id="%d">' % gid,
             # every item (row or heading) is 70 high and the list 11 of them, so a scrolled list always stops on whole
             # items (a 34 px spacer for the focus shadow left half a heading under the page title on the box)
             '\t<left>-160</left><top>191</top><width>1100</width><height>770</height>',
             '\t<orientation>vertical</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>',
             '\t<scrolltime tween="cubic" easing="out">200</scrolltime><pagecontrol>%d</pagecontrol>' % sid,
             '\t<onleft>%d</onleft>' % cat]
        for r in order:
            if r == 'THEME':
                o.append('\t' + heading('$VAR[Aeon_SetThemeName]'))
                continue
            if r == 'ALL':
                o.append('\t' + heading(A % ALL_THEMES))
                continue
            page, _, _, block = rows[r]
            head, p, rest = strip_props(block, False)
            rowg = head + '<left>160</left><top>0</top>' + p + rest
            # its button: the new Up / Down, Back / Left to this page's category
            b = rowg.index('<control type="button" id="%d">' % r)
            be = rowg.index('</control>', b)
            btn = rowg[b:be]
            btn = re.sub(r'\s*<onup[^>]*>[^<]*</onup>', '', btn)
            btn = re.sub(r'\s*<ondown[^>]*>[^<]*</ondown>', '', btn)
            btn = re.sub(r'<onback>95\d\d</onback>', '<onback>%d</onback>' % cat, btn)
            btn = re.sub(r'<onleft>SetFocus\(95\d\d\)</onleft>', '<onleft>SetFocus(%d)</onleft>' % cat, btn)
            if r not in NEVER:
                k = btn.index('>') + 1
                btn = btn[:k] + '\n\t\t\t\t\t' + nav(order, r, cat) + btn[k:]
            rowg = rowg[:b] + btn + rowg[be:]
            part = ['\t<control type="group"><!-- row %d -->' % r, '\t\t<width>1100</width><height>70</height>']
            if vis[r]:
                part.append('\t\t<visible>%s</visible>' % vis[r])
            if r in bars:
                bh, bp, brest = strip_props(bars[r][3], True)
                bv = own_visible(bars[r][3])
                part.append(bh + '<left>41</left><top>0</top><visible>%s</visible>' % bv + bp + brest)
            part.append(rowg)
            part.append('\t</control>')
            o.append('\n'.join(part))
        o.append('</control>')
        o.append('<control type="scrollbar" id="%d">\n'
                 '\t<left>920</left><top>197</top><width>4</width><height>758</height>\n'
                 '\t<texturesliderbackground border="2" colordiffuse="22ffffff">aeon/track_8.png</texturesliderbackground>\n'
                 '\t<texturesliderbar border="2" colordiffuse="99ffffff">aeon/track_8.png</texturesliderbar>\n'
                 '\t<texturesliderbarfocus border="2" colordiffuse="99ffffff">aeon/track_8.png</texturesliderbarfocus>\n'
                 '\t<textureslidernib /><textureslidernibfocus />\n'
                 '\t<orientation>vertical</orientation><showonepage>false</showonepage>\n'
                 '\t<onleft>%d</onleft>\n'
                 '\t<animation effect="slide" end="-26,0" time="0" condition="!%s">Conditional</animation>\n'
                 '</control>' % (sid, gid, FG))
        return '\n'.join(o)

    # rebuild the pages from the bottom of the file up, so the offsets stay right
    gone = set()
    for r in want:
        gone.add(rows[r][1:3])
        if r in bars:
            gone.add(bars[r][1:3])
    new = {}
    for page, cat, order, gid, sid in PAGES_:
        new[page] = build(order, cat, gid, sid)
    for page, s, e in sorted(spans, key=lambda x: -x[1]):
        seg = t[s:e]
        # take the old rows and bars out (from the back), then the list goes before the page's end
        for a, b in sorted([g for g in gone if s <= g[0] < e], key=lambda x: -x[0]):
            ls = t.rfind('\n', s, a)
            a2 = ls if ls > s and t[ls:a].strip() == '' else a
            seg = seg[:a2 - s] + seg[b - s:]
            # note: offsets inside seg are taken from the back, so the earlier ones stay valid
        end = seg.rindex('</control>')
        seg = seg[:end] + new[page] + '\n\t\t' + seg[end:]
        t = t[:s] + seg + t[e:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)

    h = read(HELP)
    if 'name="Aeon_SetThemeName"' not in h:
        h = h.replace('</includes>', '\t<!-- 0.56.12 Skin settings > Appearance: the heading over the theme\'s own rows -->\n'
                      '\t<variable name="Aeon_SetThemeName">\n'
                      '\t\t<value condition="Skin.HasSetting(aeon.fglass)">%s</value>\n'
                      '\t\t<value condition="Skin.HasSetting(aeon.vglass)">$LOCALIZE[31679]</value>\n'
                      '\t\t<value>$LOCALIZE[31678]</value>\n'
                      '\t</variable>\n</includes>' % (A % 32402))
        io.open(HELP, 'w', encoding='utf-8', newline='\n').write(h)
    ET.parse(P)
    ET.parse(HELP)
    print('ok')


if __name__ == '__main__':
    main()
