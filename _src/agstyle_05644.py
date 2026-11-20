"""0.56.44 Aeon Glass gets Fused Glass's panel and focus options (the user's review of 2026-11-18, round 2: "where are
the panel blur, opacity, tint options? where are the options for focus highlight type for Aeon Glass?").

- Panel opacity / Panel tint (aeon.x.pop / aeon.x.ptint, shared with Fused Glass: '' Default, m2 m1 p1 p2): the two
  frosted fills of every Aeon Glass card (Aeon_Glass, Aeon_Glass_L, the full-height panel of Aeon_Views2) come from
  AG_FillD / AG_FillL. Opacity scales both alphas (x0.5 .. x2: the fills are light, so Fused Glass's x0.6 .. x1.4
  would hardly show); tint - darkens the dark fill and thins the white one, + moves the dark fill towards frosted grey
  (fg_expert.FROSTED) and thickens the white one.
- Panel shadow (aeon.fgshadow, shared): the cards' shadow alpha AG_Shadow (mild / medium / strong / heavy) and the
  shadow picture of Fused Glass (FG_Sh_sho28).
- Panel blur (aeon.agblur, Aeon Glass only: '' Off = today, light / medium / strong): the menus' backdrop
  (Aeon_Backdrop) shows the helper's blurred copy (blurcache.frost, as Fused Glass's Frost style does).
- Focus highlight (aeon.agfocus, Aeon Glass + its own style, not Fuse: '' Glass = today's accent bar, pill, frost,
  outline, tight = Fused Glass's pictures): Aeon_MenuFocusTex and the button focus includes (Aeon_TexRowFocus,
  Aeon_TexCatFocus); text, icons and switches on a white focus (pill, tight) turn dark (AG_FocusDark in the ink
  variables). Library rows keep the glass bar with its pointer tips (the _L copies stay as they are).
Run from the skin folder; repeatable (checks its own marks).
"""
import io
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
D = os.path.join(ROOT, '1080i')
STEPS = ('m2', 'm1', '', 'p1', 'p2')
OPACITY = {'m2': 0.5, 'm1': 0.75, '': 1.0, 'p1': 1.5, 'p2': 2.0}
FROSTED = (214, 220, 232)
DARK = (0x3a, (16, 16, 16))
LIGHT = (0x0f, (255, 255, 255))
SHADOW = {'mild': 0x33, '': 0x55, 'strong': 0x80, 'heavy': 0xaa}
AG = 'Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)'
AGOWN = AG + ' + !String.IsEqual(Skin.String(aeon.menutheme),fused)'
MARK = '<!-- 0.56.44 agstyle_05644'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)


def once(text, old, new, count=1):
    assert text.count(old) == count, (old[:100], text.count(old))
    return text.replace(old, new)


def cond(key, step):
    return 'String.IsEmpty(Skin.String(%s))' % key if not step else 'String.IsEqual(Skin.String(%s),%s)' % (key, step)


def fill(base, op, tint, dark):
    alpha, rgb = base
    a = alpha * OPACITY[op]
    if dark:
        if tint == 'm2':
            rgb = (0, 0, 0)
        elif tint == 'm1':
            rgb = tuple(int(round(c * 0.5)) for c in rgb)
        elif tint in ('p1', 'p2'):
            k = 0.18 if tint == 'p1' else 0.36
            rgb = tuple(int(round(c + (f - c) * k)) for c, f in zip(rgb, FROSTED))
    else:
        a *= {'m2': 0.3, 'm1': 0.6, '': 1.0, 'p1': 1.4, 'p2': 1.8}[tint]
    a = max(1, min(255, int(round(a))))
    return '%02x%02x%02x%02x' % ((a,) + tuple(rgb))


def fill_var(name, base, dark):
    lines = ['\t<variable name="%s">' % name]
    for op in STEPS:
        for tint in STEPS:
            if not op and not tint:
                continue
            lines.append('\t\t<value condition="%s + %s">%s</value>'
                         % (cond('aeon.x.pop', op), cond('aeon.x.ptint', tint), fill(base, op, tint, dark)))
    lines.append('\t\t<value>%s</value>' % fill(base, '', '', dark))
    lines.append('\t</variable>')
    return '\n'.join(lines)


def defs():
    out = [MARK + ': Aeon Glass panel opacity / tint / shadow / blur + focus highlight -->']
    out.append(fill_var('AG_FillD', DARK, True))
    out.append(fill_var('AG_FillL', LIGHT, False))
    sh = ['\t<variable name="AG_Shadow">']
    for k in ('heavy', 'strong', 'mild'):
        sh.append('\t\t<value condition="String.IsEqual(Skin.String(aeon.fgshadow),%s)">%02x000000</value>' % (k, SHADOW[k]))
    sh.append('\t\t<value>%02x000000</value>' % SHADOW[''])
    sh.append('\t</variable>')
    out.append('\n'.join(sh))
    out.append('\t<expression name="AG_BlurMenus">%s + !String.IsEmpty(Skin.String(aeon.agblur))</expression>' % AG)
    out.append('\t<expression name="AG_FocusOn">%s + !String.IsEmpty(Skin.String(aeon.agfocus))</expression>' % AGOWN)
    out.append('\t<expression name="AG_FocusDark">%s + [String.IsEqual(Skin.String(aeon.agfocus),pill) | '
               'String.IsEqual(Skin.String(aeon.agfocus),tight)]</expression>' % AGOWN)
    out.append('\t<variable name="AG_FocusTex">\n'
               '\t\t<value condition="String.IsEqual(Skin.String(aeon.agfocus),frost)">fg/fx_frost.png</value>\n'
               '\t\t<value condition="String.IsEqual(Skin.String(aeon.agfocus),outline)">fg/fx_outline.png</value>\n'
               '\t\t<value condition="String.IsEqual(Skin.String(aeon.agfocus),tight)">fg/fx_tight.png</value>\n'
               '\t\t<value>fg/fx_pill.png</value>\n'
               '\t</variable>')
    # buttons cannot read $VAR in their textures: picked while the window loads (the row reloads the skin)
    own = AGOWN
    out.append('\t<include name="AG_BtnFocusTex">\n'
               '\t\t<include condition="%s + String.IsEqual(Skin.String(aeon.agfocus),frost)">FG_BtnFocusTex_frost</include>\n'
               '\t\t<include condition="%s + String.IsEqual(Skin.String(aeon.agfocus),outline)">FG_BtnFocusTex_outline</include>\n'
               '\t\t<include condition="%s + String.IsEqual(Skin.String(aeon.agfocus),tight)">FG_BtnFocusTex_tight</include>\n'
               '\t\t<include condition="%s + String.IsEqual(Skin.String(aeon.agfocus),pill)">FG_BtnFocusTex_pill</include>\n'
               '\t</include>' % (own, own, own, own))
    return '\n'.join(out) + '\n'


def glass(t):
    # the cards: fills + shadow
    old_d = 'colordiffuse="3a101010">fg/r28.png</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible>'
    t = once(t, old_d, old_d.replace('3a101010', '$VAR[AG_FillD]'))
    old_l = 'colordiffuse="0fffffff">fg/r28.png</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible>'
    t = once(t, old_l, old_l.replace('0fffffff', '$VAR[AG_FillL]'))
    old_s = 'colordiffuse="55000000">fg/sho28.png</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible>'
    t = once(t, old_s, 'colordiffuse="$VAR[AG_Shadow]">$VAR[FG_Sh_sho28]</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible>')
    # the library copy (square fills)
    old_d = 'colordiffuse="3a101010">common/white.png</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible>'
    t = once(t, old_d, old_d.replace('3a101010', '$VAR[AG_FillD]'))
    old_l = 'colordiffuse="0fffffff">common/white.png</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible>'
    t = once(t, old_l, old_l.replace('0fffffff', '$VAR[AG_FillL]'))
    old_s = 'colordiffuse="55000000">aeon/card_shadow.png</texture><visible>$EXP[Aeon_VGlass] + !$EXP[Aeon_FGlass]</visible>'
    t = once(t, old_s, old_s.replace('55000000', '$VAR[AG_Shadow]'))
    # the menus' backdrop: the blurred copy for Aeon Glass's Panel blur too
    t = once(t, '![$EXP[FG_FrostMenus] + !String.IsEmpty(Window(Home).Property(aeon.bgfan.blur))',
             '![[$EXP[FG_FrostMenus] | $EXP[AG_BlurMenus]] + !String.IsEmpty(Window(Home).Property(aeon.bgfan.blur))')
    t = once(t, '!Skin.HasSetting(aeon.nobackdrop) + $EXP[FG_FrostMenus] + !String.IsEmpty(Window(Home).Property(aeon.bgfan.blur))',
             '!Skin.HasSetting(aeon.nobackdrop) + [$EXP[FG_FrostMenus] | $EXP[AG_BlurMenus]] + !String.IsEmpty(Window(Home).Property(aeon.bgfan.blur))')
    # the focus picture and its colour
    t = once(t, '\t\t<value condition="Skin.HasSetting(aeon.fglass)">$VAR[FG_FocusTex]</value>\n'
                '\t\t<value condition="Skin.HasSetting(aeon.vglass)">common/aeon_row_glass64.png</value>',
             '\t\t<value condition="Skin.HasSetting(aeon.fglass)">$VAR[FG_FocusTex]</value>\n'
             '\t\t<value condition="$EXP[AG_FocusOn]">$VAR[AG_FocusTex]</value>\n'
             '\t\t<value condition="Skin.HasSetting(aeon.vglass)">common/aeon_row_glass64.png</value>')
    for name in ('Aeon_MenuFocusCol', 'Aeon_MenuFocusColR'):
        s = t.index('<variable name="%s">' % name)
        e = t.index('</variable>', s)
        blk = t[s:e]
        first = blk.index('<value')
        blk = blk[:first] + '<value condition="$EXP[AG_FocusOn]">ffffffff</value>\n\t\t' + blk[first:]
        t = t[:s] + blk + t[e:]
    # the ink on the focus: dark on Pill / Tight, as Fused Glass's (not the library _L copies)
    n = 0
    for m in list(re.finditer(r'<variable name="([A-Za-z0-9_]+)">(.*?)</variable>', t, re.S))[::-1]:
        name, body = m.group(1), m.group(2)
        if name.endswith('_L') or 'AG_FocusDark' in body:
            continue
        x = re.search(r'(\t\t<value condition="Skin.HasSetting\(aeon.fglass\) \+ \$EXP\[FG_FocusLight\]">[^<]*</value>\n)'
                      r'(\t\t<value condition="Skin.HasSetting\(aeon.fglass\)">([^<]*)</value>\n)', body)
        if not x:
            continue
        add = '\t\t<value condition="$EXP[AG_FocusDark]">%s</value>\n' % x.group(3)
        nb = body[:x.end()] + add + body[x.end():]
        t = t[:m.start(2)] + nb + t[m.end(2):]
        n += 1
    print('  ink variables with AG_FocusDark:', n)
    # the button focus (menus, Home lists, dialogs; not the library copy)
    for inc in ('Aeon_TexRowFocus', 'Aeon_TexCatFocus'):
        s = t.index('<include name="%s">' % inc)
        e = t.index('\n\t</include>', s)
        blk = t[s:e]
        g = '!String.IsEqual(Skin.String(aeon.menutheme),fused) + Skin.HasSetting(aeon.vglass) + !Skin.HasSetting(aeon.fglass)">'
        assert blk.count(g) == 1, inc
        blk = blk.replace(g, g[:-2] + ' + String.IsEmpty(Skin.String(aeon.agfocus))">')
        blk = blk + '\n\t\t<include condition="%s + !String.IsEmpty(Skin.String(aeon.agfocus))">AG_BtnFocusTex</include>' % AGOWN
        t = t[:s] + blk + t[e:]
    return t


def main():
    t = rd('Includes_Aeon_Glass.xml')
    if MARK in t:
        print('agstyle_05644: already done')
        return
    t = glass(t)
    i = t.index('\t<include name="Aeon_Glass">')
    t = t[:i] + defs() + t[i:]
    wr('Includes_Aeon_Glass.xml', t)
    v = rd('Includes_Aeon_Views2.xml')
    old = '<texture colordiffuse="3a101010">common/white.png</texture><visible>$EXP[Aeon_VGlass]</visible>'
    v = once(v, old, old.replace('3a101010', '$VAR[AG_FillD]'))
    wr('Includes_Aeon_Views2.xml', v)
    print('agstyle_05644: Aeon Glass fills, shadow, blur, focus done')


if __name__ == '__main__':
    main()
