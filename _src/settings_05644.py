"""0.56.44 Skin settings > Theme & style (the user, 2026-11-18):
- "we don't need the expert settings under theme & style anymore" - the Expert settings switch (9790) and Reset
  expert settings (9797) go; the rows they showed are always there: Panel opacity / tint (9791 / 9793, now Aeon Glass
  too), Fused Glass's Panel blur (9792), Library fanart opacity / blur / tint (9794-9796, with a fanart background).
- Aeon Glass gets Panel shadow (9529), Panel opacity / tint (9791 / 9793), its own Panel blur (9518, aeon.agblur:
  Off / Light / Medium / Strong) and Focus highlight (9515, aeon.agfocus: Glass / Pill / Frosted / Outline / Tight;
  not with the Fuse style, which draws its own focus cards) - _src/agstyle_05644.py draws them.
- "The focus highlight option has no use for style Fused Glass": 9749 hides in the Fused Glass style.
- "the theme & style for Fused glass theme need to be moved to the left like we did earlier": the Fused Glass style's
  101 px shift of the row icons, names and headings (and its wider names) now in every Fused Glass style; the page
  title moves with them.
Run from the skin folder after agstyle_05644.py, then skin_previews.py and ok_only.py. Repeatable."""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings_rows as sr      # noqa: E402
import settings_sections as ss  # noqa: E402

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
SKIN = os.path.join(D, 'SkinSettings.xml')
INC = os.path.join(D, 'Includes_Settings.xml')
PREV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skin_previews.py')
AG = 'Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)'
AGOWN = AG + ' + !String.IsEqual(Skin.String(aeon.menutheme),fused)'
FANART = 'String.IsEqual(Skin.String(aeon.vbg),fanart)'
A = '$ADDON[skin.aeon.fuse %d]'
L = '$LOCALIZE[%d]'
HELP_AGBLUR = 32747


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


def widths(labels, total):
    w = [len(x) * 14 + 44 for x in labels]
    s = float(sum(w))
    out = [int(round(v * total / s)) for v in w]
    out[-1] += total - sum(out)
    return out


def seg(rid, setting, opts, x0, x1):
    """the option pills of a row (as row 9749 draws them): opts = [(value, label, english)]"""
    w = widths([e for _, _, e in opts], x1 - x0)
    o = ['<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="22ffffff">$VAR[Aeon_MenuTexPill]</texture><visible>!Control.HasFocus(%d)</visible></control>' % (x0, x1 - x0, rid),
         '<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="26000000">$VAR[Aeon_MenuTexPill]</texture><visible>Control.HasFocus(%d)</visible></control>' % (x0, x1 - x0, rid)]
    x = x0
    for (v, label, _), ww in zip(opts, w):
        c = '[%s]' % ('String.IsEmpty(Skin.String(%s))' % setting if not v else 'String.IsEqual(Skin.String(%s),%s)' % (setting, v))
        box = '<left>%d</left><top>13</top><width>%d</width><height>44</height>' % (x, ww)
        o.append('<control type="image">%s<texture border="22,0,22,0" colordiffuse="$VAR[FGS_PillOn]">$VAR[Aeon_MenuTexPill]</texture><visible>%s + !Control.HasFocus(%d)</visible></control>' % (box, c, rid))
        o.append('<control type="image">%s<texture border="22,0,22,0" colordiffuse="$VAR[FGS_Aeon_OnBarFill]">$VAR[Aeon_MenuTexPill]</texture><visible>%s + Control.HasFocus(%d)</visible></control>' % (box, c, rid))
        for font, col, neg, foc in (('st_ui_22_bold', '$VAR[Aeon_AccentText]', '', '!'), ('st_ui_22_bold', '$VAR[FGS_Aeon_SegSelTxt]', '', ''),
                                    ('st_ui_22', '$VAR[FGS_Dim99]', '!', '!'), ('st_ui_22', '$VAR[FGS_Aeon_SegUnselF]', '!', '')):
            o.append('<control type="label">%s<align>center</align><font>%s</font><textcolor>%s</textcolor><label>%s</label><visible>%s%s + %sControl.HasFocus(%d)</visible></control>'
                     % (box, font, col, label, neg, c, foc, rid))
        x += ww
    return '\n\t\t\t\t'.join(o)


def cycle(setting, values, reload):
    out = []
    for i, v in enumerate(values):
        nxt = values[(i + 1) % len(values)]
        c = 'String.IsEmpty(Skin.String(%s))' % setting if not v else 'String.IsEqual(Skin.String(%s),%s)' % (setting, v)
        act = 'Skin.Reset(%s)' % setting if not nxt else 'Skin.SetString(%s,%s)' % (setting, nxt)
        out.append('<onclick condition="%s">%s</onclick>' % (c, act))
    if reload:
        out.append('<onclick>ReloadSkin()</onclick>')
    return '\n\t\t\t\t\t'.join(out)


def new_row(t, base, rid, setting, opts, x0, x1, reload, visible):
    x = sr.clone(t, base, rid)
    x = re.sub(r'<!-- row %d(?: \([^)]*\))? -->' % rid, '<!-- row %d (0.56.44 settings_05644) -->' % rid, x, count=1)
    b = x.index('<control type="button" id="%d">' % rid)
    be = x.index('</control>', b)
    btn = re.sub(r'\s*<onclick[^>]*>[^<]*</onclick>', '', x[b:be])
    btn = btn.rstrip() + '\n\t\t\t\t\t' + cycle(setting, [v for v, _, _ in opts], reload) + '\n\t\t\t\t'
    x = x[:b] + btn + x[be:]
    be = x.index('</control>', b) + len('</control>')
    tail = '\n\t\t\t</control>\n\t</control>'
    assert x.endswith(tail), repr(x[-80:])
    x = x[:be] + '\n\t\t\t\t' + seg(rid, setting, opts, x0, x1) + tail
    x = re.sub(r'\s*<visible>[^<]*</visible>', '', x, count=1) if x.index('<visible>') < x.index('<control type="group"><left>41</left>') else x
    i = x.index('<height>70</height>') + len('<height>70</height>')
    x = x[:i] + '\n\t\t<visible>%s</visible>' % visible + x[i:]
    return x


def remove_row(t, rid):
    s, e = sr.item_span(t, rid)
    ls = t.rfind('\n', 0, s)
    return t[:ls] + t[e:]


def headings(t, gid):
    """each heading of list gid shows while one of the rows under it shows"""
    m = ss.masked(t)
    s = t.index('<control type="grouplist" id="%d">' % gid)
    e = ss.ctl_end(m, s)
    kids = ss.children(m, s, e)
    out = []
    for k, (a, b) in enumerate(kids):
        if re.search(r'<control type="button" id="\d+">', m[a:b]):
            continue
        conds = []
        for a2, b2 in kids[k + 1:]:
            if not re.search(r'<control type="button" id="\d+">', m[a2:b2]):
                break
            v = ss.own_visible(t[a2:b2])
            if v == 'false':
                continue
            conds.append(v)
        out.append((a, b, 'true' if (not conds or '' in conds or None in conds) else ' | '.join('[%s]' % c for c in conds)))
    for a, b, c in sorted(out, key=lambda x: -x[0]):
        h = t[a:b]
        o = h.index('<visible>') if '<visible>' in h[:h.index('<control', 10)] else -1
        if c == 'true':
            h2 = re.sub(r'<visible>[^<]*</visible>', '', h, count=1) if o >= 0 else h
        elif o >= 0:
            h2 = h[:o] + re.sub(r'<visible>[^<]*</visible>', '<visible>%s</visible>' % c, h[o:], count=1)
        else:
            i = h.index('<height>70</height>') + len('<height>70</height>')
            h2 = h[:i] + '<visible>%s</visible>' % c + h[i:]
        t = t[:a] + h2 + t[b:]
    return t


def shift(t_skin, t_inc):
    """the Fused Glass style's 101 px shift and wide names in every Fused Glass style"""
    old = 'end="-101,0" time="0" condition="$EXP[FGS]"'
    new = 'end="-101,0" time="0" condition="$EXP[Aeon_FGlass]"'
    n1, n2 = t_inc.count(old), t_skin.count(old)
    t_inc, t_skin = t_inc.replace(old, new), t_skin.replace(old, new)
    a = '<include content="Param_W" condition="$EXP[FGS]"><param name="w" value="$PARAM[namefgs]"/></include><include content="Param_W" condition="!$EXP[FGS]"><param name="w" value="$PARAM[namew]"/></include>'
    b = '<include content="Param_W" condition="$EXP[Aeon_FGlass]"><param name="w" value="$PARAM[namefgs]"/></include><include content="Param_W" condition="!$EXP[Aeon_FGlass]"><param name="w" value="$PARAM[namew]"/></include>'
    n3 = t_inc.count(a)
    t_inc = t_inc.replace(a, b)
    title = '<label>[UPPERCASE]$VAR[Aeon_SkinCatName][/UPPERCASE]</label><animation effect="slide" start="0,0" end="20,0" time="0" condition="$EXP[Aeon_FGlass] + !$EXP[FGS]">Conditional</animation>'
    if title in t_skin:
        t_skin = t_skin.replace(title, title.replace('end="20,0"', 'end="-81,0"'))
    print('  shift: %d chrome + %d heading slides, %d name widths, title %s' % (n1, n2, n3, title in t_skin or 'done'))
    return t_skin, t_inc


def previews():
    p = rd(PREV)
    if 'def p_focus_ag' in p:
        return
    fn = '''

def p_focus_ag():
    """0.56.44 Aeon Glass Focus highlight (Skin.String(aeon.agfocus)): Glass, the accent bar (default), or Fused Glass's
    pictures (Pill and Tight white with dark text, Frosted a wash, Outline a ring)"""
    def sw(tex, col='ffffffff'):
        def draw(x, y):
            return A(x, y, 44, 26, 'cc1a1d24', tex='fg/r8.png', border='4') + A(x + 3, y + 5, 38, 16, col, tex=tex, border='8')
        return draw
    o = A(16, 96, 248, 140, 'ffffffff', tex=pic()) + A(16, 96, 248, 140, '$VAR[AG_FillD]', tex='fg/r8.png', border='8')
    o += A(16, 96, 248, 140, '$VAR[AG_FillL]', tex='fg/r8.png', border='8') + A(16, 96, 248, 140, '38ffffff', tex='fg/e28.png', border='14')
    o += A(28, 108, 224, 36, '$VAR[Aeon_MenuFocusColR]', tex='$VAR[Aeon_MenuFocusTex]', border='12')
    o += T(44, 108, 190, 36, '$LOCALIZE[31683]', '$VAR[Aeon_OnBarInk]', 'st_ui_22_bold', card=True)
    o += T(44, 150, 190, 36, '$LOCALIZE[31684]', W1, 'st_ui_22', card=True) + T(44, 190, 190, 36, '$LOCALIZE[31684]', W2, 'st_ui_22', card=True)
    rows = [('$ADDON[skin.aeon.fuse 32429]', 'String.IsEmpty(Skin.String(aeon.agfocus))', sw('common/aeon_row_glass64.png', '$VAR[Aeon_Accent]'), '', None),
            ('$ADDON[skin.aeon.fuse 32409]', eq('aeon.agfocus', 'pill'), sw('fg/fx_pill.png'), '100 %', None),
            ('$ADDON[skin.aeon.fuse 32411]', eq('aeon.agfocus', 'frost'), sw('fg/fx_frost.png'), '18 %', None),
            ('$ADDON[skin.aeon.fuse 32412]', eq('aeon.agfocus', 'outline'), sw('fg/fx_outline.png'), '5 %', None),
            ('$ADDON[skin.aeon.fuse 32413]', eq('aeon.agfocus', 'tight'), sw('fg/fx_tight.png'), '100 %', None)]
    return o + option_table(TINT, rows)


def p_agblur():
    """0.56.44 Aeon Glass Panel blur (Skin.String(aeon.agblur)): the menus' backdrop sharp (Off, as before) or blurred"""
    def sw(blurred):
        def draw(x, y):
            return A(x, y, 44, 26, 'ffffffff', tex=pic()) + (A(x, y, 44, 26, '66b0c4de', tex='fg/r8.png', border='4') if blurred else '')
        return draw
    o = A(16, 96, 248, 140, 'ffffffff', tex=pic()) + A(16, 96, 248, 140, '55b0c4de', 'Skin.HasSetting(aeon.vglass) + !String.IsEmpty(Skin.String(aeon.agblur))')
    o += A(28, 146, 224, 80, '$VAR[AG_FillD]', tex='fg/r8.png', border='8') + A(28, 146, 224, 80, '38ffffff', tex='fg/e28.png', border='14')
    o += T(42, 154, 200, 32, 'Lawrence of Arabia', W1, 'st_ui_22_bold', card=True)
    rows = [('$LOCALIZE[31072]', 'String.IsEmpty(Skin.String(aeon.agblur))', sw(False), '', None),
            ('$LOCALIZE[31672]', eq('aeon.agblur', 'light'), sw(True), '', None, True),
            ('$LOCALIZE[31071]', eq('aeon.agblur', 'medium'), sw(True), '', None, True),
            ('$LOCALIZE[31673]', eq('aeon.agblur', 'strong'), sw(True), '', None, True)]
    return o + option_table(PICTURE, rows, legend=True)
'''
    i = p.index('\n\ndef p_dlgbg():')
    p = p[:i] + fn + p[i:]
    old = "(9798, 'menu', p_dlgbg), (9791, 'sample', p_xpanel), (9792, 'sample', p_xpanel), (9793, 'sample', p_xpanel),"
    assert old in p
    p = p.replace(old, old + "\n                   (9515, 'sample', p_focus_ag), (9518, 'sample', p_agblur),     # 0.56.44 Aeon Glass")
    # the panel sample in the glass in use: Fused Glass's fill, or Aeon Glass's two fills
    old = "    return sample_panel('$VAR[FG_Frost]', '$VAR[FG_Edge]')\n"
    assert old in p
    p = p.replace(old, "    fg = sample_panel('$VAR[FG_Frost]', '$VAR[FG_Edge]')\n"
                       "    ag = (A(16, 96, 248, 140, 'ffffffff', tex=pic()) + A(28, 146, 224, 80, '$VAR[AG_FillD]', tex='fg/r8.png', border='8') +\n"
                       "          A(28, 146, 224, 80, '$VAR[AG_FillL]', tex='fg/r8.png', border='8') + A(28, 146, 224, 80, '38ffffff', tex='fg/e28.png', border='14') +\n"
                       "          T(42, 154, 200, 32, 'Lawrence of Arabia', W1, 'st_ui_22_bold', card=True) +\n"
                       "          T(42, 186, 200, 28, '1962  \\u00b7  3h 47m', 'b3ffffff', 'st_small_20', card=True))\n"
                       "    # 0.56.44: Aeon Glass's cards too\n"
                       "    return ('<control type=\"group\"><visible>Skin.HasSetting(aeon.fglass)</visible>%s</control>'\n"
                       "            '<control type=\"group\"><visible>!Skin.HasSetting(aeon.fglass)</visible>%s</control>' % (fg, ag))\n")
    wr(PREV, p)
    print('  previews: p_focus_ag, p_agblur, p_xpanel for Aeon Glass')


def main():
    t = rd(SKIN)
    h = rd(INC)
    if '<!-- row 9515 (0.56.44 settings_05644) -->' not in t:
        for rid in (9790, 9797):
            t = remove_row(t, rid)
        focus = [('', A % 32429, 'Glass'), ('pill', A % 32409, 'Pill'), ('frost', A % 32411, 'Frosted'),
                 ('outline', A % 32412, 'Outline'), ('tight', A % 32413, 'Tight')]
        blur = [('', L % 31072, 'Off'), ('light', L % 31672, 'Light'), ('medium', L % 31071, 'Medium'), ('strong', L % 31673, 'Strong')]
        t = sr.insert_after(t, 9749, new_row(t, 9749, 9515, 'aeon.agfocus', focus, 311, 860, True, AGOWN))
        t = sr.insert_after(t, 9792, new_row(t, 9792, 9518, 'aeon.agblur', blur, 400, 860, False, AG))
    for rid, c in ((9749, '$EXP[Aeon_FGlass] + !$EXP[FGS]'), (9529, 'Skin.HasSetting(aeon.vglass)'),
                   (9791, 'Skin.HasSetting(aeon.vglass)'), (9792, '$EXP[Aeon_FGlass]'), (9793, 'Skin.HasSetting(aeon.vglass)'),
                   (9794, FANART), (9795, FANART), (9796, FANART)):
        t = sr.set_item_visible(t, rid, c)
    t = sr.renav(t, 9770)
    t = sr.renav(t, 9777)
    t = headings(t, 9770)
    t, h = shift(t, h)
    h = sr.add_help(h, 9515, 32414)
    h = sr.add_help(h, 9518, HELP_AGBLUR)
    assert 'aeon.expert' not in t.replace('Control.HasFocus(9790)', ''), [m.start() for m in re.finditer('aeon.expert', t)][:5]
    wr(SKIN, t)
    wr(INC, h)
    previews()
    print('settings_05644 done')


if __name__ == '__main__':
    main()
