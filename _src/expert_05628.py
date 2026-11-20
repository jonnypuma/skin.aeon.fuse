# -*- coding: utf-8 -*-
"""0.56.28 Panel shadow and Expert settings (the user, 2026-11-17: "I want opacity, blur, frost tint controls for both
Theme style and Fanart look under Expert settings ... Instead of Raised as a style, we could have 'Panel shadow' setting
(default as set currently). Setting Mild, Medium (Default), Strong, Heavy ... Applies universally to menus, library
views etc."). Idempotent; run from the skin folder, then skin_previews.py, fg_material.py, ok_only.py.

Skin settings > Appearance:
- Fused Glass: row 9529 (where Library view theme was) is Panel shadow: Mild | Medium | Strong | Heavy
  (Skin.String(aeon.fgshadow); '' = Medium). fg_material.py turns it into FG_PanelSh_xx (every panel shadow, menus and
  library alike) and Heavy's lit rim (FG_Edge / FG_EdgeM).
- All themes, at the end: heading Expert settings, row 9790 Expert settings (switch, Skin.HasSetting(aeon.expert)); while
  it is on, rows 9791-9797:
    9791 Panel opacity  -2 | -1 | Default | +1 | +2       aeon.x.pop     (Fused Glass)
    9792 Panel blur     Off | Light | Default | Strong     aeon.x.pblur   (Fused Glass; the helper's blur radius)
    9793 Panel tint     -2 | -1 | Default | +1 | +2       aeon.x.ptint   (Fused Glass)
    9794 Fanart opacity -2 | -1 | Default | +1 | +2       aeon.x.fop     (library views' fanart alpha)
    9795 Fanart blur    Off | Light | Medium | Strong      aeon.x.fblur   (the helper's blurred copy, aeon.fanblur)
    9796 Fanart tint    Off | Light | Default | Strong     aeon.x.ftint   (the Frosted look's colour tint)
    9797 Reset expert settings
- Library views: fanart alpha steps (Aeon_VFanAlpha / Aeon_VFanAlphaG twins), the tint's three strengths, the blurred
  fanart instead of the sharp one while Fanart blur is on.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fg_expert                       # noqa: E402
import expert_strings_05628 as S       # noqa: E402

D = '1080i'
L = 'language'
SET = os.path.join(D, 'SkinSettings.xml')
HELP = os.path.join(D, 'Includes_Settings.xml')
MARK = '0.56.28 expert_05628'
A = lambda i: '$ADDON[skin.aeon.fuse %d]' % i          # noqa: E731
EXPERT = 'Skin.HasSetting(aeon.expert)'
FG = '$EXP[Aeon_FGlass]'
OFF, ON, LIGHT, MEDIUM, STRONG, DEFAULT = '$LOCALIZE[31072]', '$LOCALIZE[31547]', '$LOCALIZE[31672]', '$LOCALIZE[31071]', '$LOCALIZE[31673]', '$LOCALIZE[571]'
STEPS5 = [('m2', '-2', 70), ('m1', '-1', 70), ('', DEFAULT, 130), ('p1', '+1', 70), ('p2', '+2', 70)]


def rd(p):
    return io.open(p, encoding='utf-8').read()


def wr(p, t):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)


# ------------------------------------------------------------------------------------------------- strings
def strings():
    for d in sorted(os.listdir(L)):
        code = d.replace('resource.language.', '')
        p = os.path.join(L, d, 'strings.po')
        t = rd(p)
        if 'msgctxt "#32668"' in t:
            continue
        m = re.search(r'msgctxt "#32667"\nmsgid "[^\n]*"\nmsgstr "[^\n]*"\n', t)
        assert m, code
        tr = [''] * len(S.IDS) if code == 'en_gb' else S.T[code]
        add = ''.join('\nmsgctxt "#%d"\nmsgid "%s"\nmsgstr "%s"\n' % (sid, S.EN[i].replace('"', '\\"'), tr[i].replace('"', '\\"'))
                      for i, sid in enumerate(S.IDS))
        wr(p, t[:m.end()] + add + t[m.end():])
    print('strings 32668-32688 in 23 languages')


# ------------------------------------------------------------------------------------------------- rows
def sel(setting, v):
    return 'String.IsEmpty(Skin.String(%s))' % setting if not v else 'String.IsEqual(Skin.String(%s),%s)' % (setting, v)


def pills(rid, setting, options):
    """the segmented value at the row's end (as Backdrop strength draws it): options [(value, label, width)]"""
    total = sum(w for _v, _l, w in options)
    x0 = 860 - total
    o = ('\t\t\t\t<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="22ffffff">$VAR[Aeon_MenuTexPill]</texture><visible>!Control.HasFocus(%d)</visible></control>\n'
         '\t\t\t\t<control type="image"><left>%d</left><top>13</top><width>%d</width><height>44</height><texture border="22,0,22,0" colordiffuse="26000000">$VAR[Aeon_MenuTexPill]</texture><visible>Control.HasFocus(%d)</visible></control>\n'
         % (x0, total, rid, x0, total, rid))
    x = x0
    for v, label, w in options:
        c = sel(setting, v)
        geo = '<left>%d</left><top>13</top><width>%d</width><height>44</height>' % (x, w)
        o += ('\t\t\t\t<control type="image">%s<texture border="22,0,22,0" colordiffuse="$VAR[Aeon_Accent]">$VAR[Aeon_MenuTexPill]</texture><visible>[%s] + !Control.HasFocus(%d)</visible></control>\n' % (geo, c, rid) +
              '\t\t\t\t<control type="image">%s<texture border="22,0,22,0" colordiffuse="$VAR[Aeon_OnBarFill]">$VAR[Aeon_MenuTexPill]</texture><visible>[%s] + Control.HasFocus(%d)</visible></control>\n' % (geo, c, rid) +
              '\t\t\t\t<control type="label">%s<align>center</align><font>st_ui_22_bold</font><textcolor>$VAR[Aeon_AccentText]</textcolor><label>%s</label><visible>[%s] + !Control.HasFocus(%d)</visible></control>\n' % (geo, label, c, rid) +
              '\t\t\t\t<control type="label">%s<align>center</align><font>st_ui_22_bold</font><textcolor>$VAR[Aeon_SegSelTxt]</textcolor><label>%s</label><visible>[%s] + Control.HasFocus(%d)</visible></control>\n' % (geo, label, c, rid) +
              '\t\t\t\t<control type="label">%s<align>center</align><font>st_ui_22</font><textcolor>99ffffff</textcolor><label>%s</label><visible>![%s] + !Control.HasFocus(%d)</visible></control>\n' % (geo, label, c, rid) +
              '\t\t\t\t<control type="label">%s<align>center</align><font>st_ui_22</font><textcolor>$VAR[Aeon_SegUnselF]</textcolor><label>%s</label><visible>![%s] + Control.HasFocus(%d)</visible></control>\n' % (geo, label, c, rid))
        x += w
    return o


def cycle(setting, options):
    """OK steps to the next value (the last back to the first)"""
    vals = [v for v, _l, _w in options]
    o = ''
    for i, v in enumerate(vals):
        nxt = vals[(i + 1) % len(vals)]
        act = 'Skin.SetString(%s,%s)' % (setting, nxt) if nxt else 'Skin.Reset(%s)' % setting
        o += '\t\t\t\t\t<onclick condition="%s">%s</onclick>\n' % (sel(setting, v), act)
    return o


def nav(ups, downs):
    """[(id, condition or None)] in order: Kodi takes the first whose condition is true"""
    f = lambda tag, items: ''.join('<%s condition="%s">%d</%s>' % (tag, c, i, tag) if c else '<%s>%d</%s>' % (tag, i, tag) for i, c in items)  # noqa: E731
    return f('onup', ups) + f('ondown', downs)


def bar(t, rid):
    """the focus bar group of Backdrop strength (9742), for another row"""
    i = t.index('<control type="group"><left>41</left><top>0</top><visible>Control.HasFocus(9742)</visible>')
    j = t.index('\n\t\t\t</control>', i) + len('\n\t\t\t</control>')
    return t[i:j].replace('9742', str(rid))


def row(t, rid, label, icon, namew, navs, clicks, value, vis=None):
    return ('\t<control type="group"><!-- row %d (%s) -->\n\t\t<width>1100</width><height>70</height>\n%s%s\n'
            '<control type="group"><left>160</left><top>0</top>\n'
            '\t\t\t\t<animation type="Visible" delay="80" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/><effect type="slide" start="26,0" end="0,0" time="200" tween="cubic" easing="out"/></animation>\n'
            '\t\t\t\t<include content="Dlg_SkinRowChrome">\n'
            '\t\t\t\t\t<param name="id" value="%d"/><param name="namew" value="%d"/><param name="label" value="%s"/><param name="hint" value=""/><param name="labelTop" value="0"/><param name="labelH" value="70"/><param name="icon" value="%s"/><param name="labelx" value="46"/>\n'
            '\t\t\t\t</include>\n'
            '\t\t\t\t<control type="button" id="%d">\n\t\t\t\t\t%s\n\t\t\t\t\t<include>Dlg_SkinRowButton</include>\n'
            '\t\t\t\t\t<onback>9600</onback>\n\t\t\t\t\t<onleft>SetFocus(9600)</onleft>\n%s\t\t\t\t</control>\n%s\t\t\t</control>\n\t</control>\n'
            % (rid, MARK, ('\t\t<visible>%s</visible>\n' % vis) if vis else '', bar(t, rid), rid, namew, label, icon, rid, navs, clicks, value))


def switch(t, rid, setting):
    """the On / Off switch of Toasts from the clock pill (9528), for another row and setting"""
    i = t.index('<control type="button" id="9528">')
    i = t.index('</control>', i) + len('</control>\n')
    j = t.index('\n\t\t\t</control>', i)
    s = t[i:j].replace('aeon.toastpill', setting).replace('9528', str(rid))
    assert 'Skin.HasSetting(%s)' % setting in s
    return s + '\n'


SHADOW = [('mild', A(32670), 116), ('', MEDIUM, 136), ('strong', STRONG, 128), ('heavy', A(32671), 120)]
ROWS = [  # id, label, icon, setting, options, visibility
    (9791, A(32674), 'aeon/icons/layers.png', 'aeon.x.pop', STEPS5, '%s + %s' % (EXPERT, FG)),
    (9792, A(32676), 'aeon/icons/blur.png', 'aeon.x.pblur', [('off', OFF, 100), ('light', LIGHT, 110), ('', DEFAULT, 130), ('strong', STRONG, 120)], '%s + %s' % (EXPERT, FG)),
    (9793, A(32678), 'aeon/icons/sparkle.png', 'aeon.x.ptint', STEPS5, '%s + %s' % (EXPERT, FG)),
    (9794, A(32680), 'aeon/icons/image.png', 'aeon.x.fop', STEPS5, EXPERT),
    (9795, A(32682), 'aeon/icons/blur.png', 'aeon.x.fblur', [('', OFF, 100), ('light', LIGHT, 110), ('medium', MEDIUM, 130), ('strong', STRONG, 120)], EXPERT),
    (9796, A(32684), 'aeon/icons/sparkle.png', 'aeon.x.ftint', [('off', OFF, 100), ('light', LIGHT, 110), ('', DEFAULT, 130), ('strong', STRONG, 120)], EXPERT),
]
RESET = ['aeon.x.pop', 'aeon.x.pblur', 'aeon.x.ptint', 'aeon.x.fop', 'aeon.x.fblur', 'aeon.x.ftint']


def rows():
    t = rd(SET)
    if MARK in t:
        print('rows: already')
        return
    # --- 9529 Panel shadow, in place of Library view theme (its navigation kept)
    a = t.index('<control type="group"><!-- row 9529 -->')
    b = t.index('\n\t</control>', t.index('<control type="button" id="9529">', a)) + len('\n\t</control>')
    old = t[a:b]
    navs = re.search(r'<control type="button" id="9529">\s*(<on(?:up|down).*?)\n', old).group(1).strip()
    new = row(t, 9529, A(32668), 'aeon/icons/layers.png', 300, navs, cycle('aeon.fgshadow', SHADOW), pills(9529, 'aeon.fgshadow', SHADOW),
              FG).strip('\n').lstrip('\t')
    t = t[:a] + new + t[b:]
    # --- the expert rows after 9746 (the last row of the list)
    a = t.index('<control type="group"><!-- row 9746 -->')
    b = t.index('\n\t</control>', t.index('<control type="button" id="9746">', a)) + len('\n\t</control>')
    r9746 = t[a:b]
    assert '<ondown>9744</ondown>' in r9746
    t = t[:a] + r9746.replace('<ondown>9744</ondown>', '<ondown>9790</ondown>', 1) + t[b:]
    b = t.index('\n\t</control>', t.index('<control type="button" id="9746">', a)) + len('\n\t</control>')
    head = ('\n\t<control type="group"><width>1100</width><height>70</height><control type="label"><left>162</left><top>28</top><width>840</width>'
            '<height>40</height><aligny>center</aligny><font>st_cap_20</font><textcolor>$VAR[Aeon_Accent]</textcolor>'
            '<label>[UPPERCASE]%s[/UPPERCASE]</label></control></control>\n' % A(32672))
    ids = [9790] + [r[0] for r in ROWS] + [9797]
    visc = {9790: None, 9797: EXPERT}
    visc.update((r[0], r[5]) for r in ROWS)
    order = [(i, visc[i]) for i in ids]

    def around(rid):
        k = ids.index(rid)
        before = list(reversed(order[:k])) + [(9746, None)]
        after = order[k + 1:] + [(9744, None)]
        return nav(before, after)
    out = head
    out += row(t, 9790, A(32672), 'aeon/icons/settings.png', 300, around(9790), '\t\t\t\t\t<onclick>Skin.ToggleSetting(aeon.expert)</onclick>\n',
               switch(t, 9790, 'aeon.expert'))
    for rid, label, icon, setting, options, vis in ROWS:
        out += row(t, rid, label, icon, 300, around(rid), cycle(setting, options), pills(rid, setting, options), vis)
    clicks = ''.join('\t\t\t\t\t<onclick>Skin.Reset(%s)</onclick>\n' % s for s in RESET)
    clicks += '\t\t\t\t\t<onclick>Notification($ADDON[skin.aeon.fuse 32686],$ADDON[skin.aeon.fuse 32688],3000)</onclick>\n'
    value = ('\t\t\t\t<control type="image"><left>812</left><top>17</top><width>36</width><height>36</height><aspectratio>keep</aspectratio>'
             '<texture colordiffuse="99ffffff">icons/af3/arrow-rotate-left.png</texture><visible>!Control.HasFocus(9797)</visible></control>\n'
             '\t\t\t\t<control type="image"><left>812</left><top>17</top><width>36</width><height>36</height><aspectratio>keep</aspectratio>'
             '<texture colordiffuse="$VAR[Aeon_OnBarIcon]">icons/af3/arrow-rotate-left.png</texture><visible>Control.HasFocus(9797)</visible></control>\n')
    out += row(t, 9797, A(32686), 'icons/af3/arrow-rotate-left.png', 420, around(9797), clicks, value, EXPERT)
    t = t[:b] + out.rstrip('\n') + t[b:]
    # 9744 (the first row): up goes to the last row shown
    i = t.index('<control type="button" id="9744">')
    j = t.index('<onup>9746</onup>', i)
    assert j - i < 300
    t = t[:j] + '<onup condition="%s">9797</onup><onup>9790</onup>' % EXPERT + t[j + len('<onup>9746</onup>'):]
    wr(SET, t)
    import xml.etree.ElementTree as ET
    ET.parse(SET)
    print('rows written')


def help_texts():
    h = rd(HELP)
    if 'Control.HasFocus(9790)' in h:
        return
    old = '<value condition="Control.HasFocus(9529)">$ADDON[skin.aeon.fuse 32551]</value>'
    assert h.count(old) == 1
    new = '<value condition="Control.HasFocus(9529)">%s</value>' % A(32669)
    for rid, sid in ((9790, 32673), (9791, 32675), (9792, 32677), (9793, 32679), (9794, 32681), (9795, 32683), (9796, 32685), (9797, 32687)):
        new += '\n\t\t<value condition="Control.HasFocus(%d)">%s</value>' % (rid, A(sid))
    wr(HELP, h.replace(old, new))
    print('help texts written')


# ------------------------------------------------------------------------------------------------- library fanart
def fanart():
    g = os.path.join(D, 'Includes_Aeon_Glass.xml')
    t = rd(g)
    if 'AXF_On' not in t:
        exps, combos = fg_expert.expressions('AXF', 'aeon.x.fop')
        t, twins = fg_expert.expand(t, ('Aeon_VFanAlpha', 'Aeon_VFanAlphaG'), 'AXF', combos)
        i = t.index('\t<variable name="Aeon_VFanAlpha">')
        t = t[:i] + ('\t<!-- %s: Expert settings > Fanart opacity (aeon.x.fop), five steps around the fanart alpha -->\n' % MARK) + exps + twins + t[i:]
        t = t.replace('\t<!-- 0.56.15 aeon_lib_round2b -->',
                      '\t<!-- %s: Expert settings > Fanart blur: the helper\'s blurred copy (aeon.fanblur) in place of the sharp fanart -->\n'
                      '\t<expression name="AX_FanBlur">!String.IsEmpty(Skin.String(aeon.x.fblur)) + !String.IsEmpty(Window(Home).Property(aeon.fanblur))</expression>\n'
                      '\t<!-- 0.56.15 aeon_lib_round2b -->' % MARK, 1)
        assert 'AX_FanBlur' in t
        wr(g, t)
    v = os.path.join(D, 'Includes_Aeon_Views2.xml')
    t = rd(v)
    if MARK in t:
        print('fanart: already')
        return
    lines = t.split('\n')
    out = []
    n_sharp = n_tint = 0
    for l in lines:
        if '<texture background="true" colordiffuse="$VAR[Aeon_VFanAlpha' in l and '$VAR[Aeon_V_Fan]</texture>' in l and '<visible>$EXP[Aeon_FanShown]' in l:
            sharp = l.replace('</visible>', ' + !$EXP[AX_FanBlur]</visible>', 1)
            blurred = (l.replace('<aspectratio>scale</aspectratio>', '<aspectratio>stretch</aspectratio>')
                       .replace('$VAR[Aeon_V_Fan]</texture>', '$INFO[Window(Home).Property(aeon.fanblur)]</texture>')
                       .replace('</visible>', ' + $EXP[AX_FanBlur]</visible>', 1))
            out += [sharp, blurred.replace('<control type="image">', '<control type="image"><!-- %s -->' % MARK, 1)]
            n_sharp += 1
            continue
        if 'colordiffuse="$INFO[Fanart.Color1]"' in l and 'end="14"' in l:
            base = l.replace('</visible>', ' + String.IsEmpty(Skin.String(aeon.x.ftint))</visible>', 1)
            out.append(base)
            for name, end in (('light', 7), ('strong', 28)):
                out.append(l.replace('end="14"', 'end="%d"' % end).replace('</visible>', ' + String.IsEqual(Skin.String(aeon.x.ftint),%s)</visible>' % name, 1))
            n_tint += 1
            continue
        out.append(l)
    assert n_sharp == 2 and n_tint == 1, (n_sharp, n_tint)
    wr(v, '\n'.join(out))
    print('library fanart written')


# ------------------------------------------------------------------------------------------------- dialog panels
# the dialog / context menu panel is one baked picture (shadow, fill and edge), so Panel shadow gets its own copies of
# the three Skin style panels: panel_fg (Dark), panel_fgg (Clear), panel_fgf (Frost), each _shmild / _shstrong / _shheavy
PANELS = {'panel_fg': ((26, 29, 36), 0.94, 0.227), 'panel_fgg': ((23, 26, 32), 0xc8 / 255.0, 0.20),
          'panel_fgf': ((30, 33, 41), 0xb3 / 255.0, 0.30)}
SHADES = {'mild': (0.5, None), 'strong': (1.6, None), 'heavy': (2.0, None)}   # 0.56.39: drawn again by shadow_lift_05639 (size, not darkness)


def panels():
    from PIL import Image
    base = Image.open(os.path.join('media', 'dialogs', 'panel_fg.png')).convert('RGBA')
    bp = base.load()
    for name, (fill, alpha, edge) in PANELS.items():
        for shname, (shade, rim) in SHADES.items():
            out = Image.new('RGBA', base.size)
            op = out.load()
            e = rim if rim is not None else edge
            for y in range(base.size[1]):
                for x in range(base.size[0]):
                    r, g, b, a = bp[x, y]
                    if (r, g, b) == (0, 0, 0):
                        op[x, y] = (0, 0, 0, min(255, int(round(a * shade))))
                    elif (r, g, b) == (26, 29, 36):
                        op[x, y] = fill + (int(round(a / 0.94 * alpha)),)
                    else:
                        lit = tuple(int(round(c + (255 - c) * e)) for c in fill)
                        op[x, y] = lit + (int(round(a / 0.94 * max(alpha, 0.5))),)
            out.save(os.path.join('media', 'dialogs', '%s_sh%s.png' % (name, shname)), optimize=True)
    g = os.path.join(D, 'Includes_Aeon.xml')
    t = rd(g)
    if '_shheavy.png' not in t:
        for cond, name in (('$EXP[FG_FrostMenus]', 'panel_fgf'), ('$EXP[FG_GlassMenus]', 'panel_fgg'), ('Skin.HasSetting(aeon.fglass)', 'panel_fg')):
            line = '\t\t<value condition="%s">dialogs/%s.png</value>\n' % (cond, name)
            assert t.count(line) == 1, line
            add = ''.join('\t\t<value condition="%s + String.IsEqual(Skin.String(aeon.fgshadow),%s)">dialogs/%s_sh%s.png</value>\n'
                          % (cond, s, name, s) for s in ('mild', 'strong', 'heavy'))
            t = t.replace(line, add + line)
        wr(g, t)
    print('dialog panels written')


if __name__ == '__main__':
    strings()
    rows()
    help_texts()
    fanart()
    panels()
