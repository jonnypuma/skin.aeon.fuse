# -*- coding: utf-8 -*-
"""0.56.45 View settings (library views) after the user's notes of 2026-11-18:
- "menu backdrop strength ... was only going to apply for menus, not the fanart in library views? it kinda fights with
  library fanart opacity": the library fanart no longer reads Backdrop strength (Skin settings aeon.backdrop.dim or the
  view's own); its opacity is Library fanart opacity alone (five steps around the old Medium). The Backdrop strength row
  leaves View settings (menus keep it).
- "a lot of settings do not show the default value": every option that follows Skin settings reads "Default (<value>)".
- "the library fanart tint setting does not work": its layers were drawn for the Frosted fanart look only (under the
  Dimmed look's picture) and coloured with Fanart.Color1, which most films do not have. Light and Strong now draw in
  both looks, in the fanart's colour or else a frosted blue-grey; Default stays as it was.
- "library fanart blur ... from -2 to 2 ... where default is 0=mild (default) and that is the current light": Off, -2,
  -1, 0, +1, +2 (helper radii 1 / 2 / 4 / 9 / 16; 0 = the old Light and the new default), here and in Skin settings.
- "In view settings we are missing the options for panel shadow, panel opacity, panel blur and panel tint": four rows
  (aeon.vo.<view>.pshadow / pop / pblur / ptint, helper publishes aeon.vo.pshadow ...); every place that reads the
  Skin settings value of Panel shadow / opacity / tint reads "the view's value, else Skin settings'" (view_aware, a
  post-pass: run it again after fg_material.py / fg_expert.py), the helper the view's Panel blur.
Run from the skin folder. Repeatable."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
VO = 'Window(Home).Property(aeon.vo.%s)'
BASE = '$INFO[Window(Home).Property(aeon.vo.base)]'
L = '$LOCALIZE[%d]'
A = '$ADDON[skin.aeon.fuse %d]'
DEF = L % 31546
STEPS = [('m2', '-2'), ('m1', '-1'), ('z', '$NUMBER[0]'), ('p1', '+1'), ('p2', '+2')]


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(os.path.join(D, name))


def var(name, values):
    """values: [(condition or None, label)]"""
    o = ['\t<variable name="%s">' % name]
    for c, v in values:
        o.append('\t\t<value condition="%s">%s</value>' % (c, v) if c else '\t\t<value>%s</value>' % v)
    return '\n'.join(o + ['\t</variable>'])


def eq(info, v):
    return 'String.IsEqual(%s,%s)' % (info, v)


def vos(opt, explicit, defaults):
    """the View settings value: the view's own, else Default (Skin settings')"""
    vals = [(eq(VO % opt, tok), lab) for tok, lab in explicit]
    vals += [(c, '%s (%s)' % (DEF, lab)) for c, lab in defaults]
    return vals


def cycle(opt, toks):
    """OK steps: follow Skin settings -> each value -> follow"""
    seq = [''] + toks
    out = []
    for i, tok in enumerate(seq):
        nxt = seq[(i + 1) % len(seq)]
        c = 'String.IsEmpty(%s)' % (VO % opt) if not tok else eq(VO % opt, tok)
        act = 'Skin.Reset(%s%s)' % (BASE, opt) if not nxt else 'Skin.SetString(%s%s,%s)' % (BASE, opt, nxt)
        out.append('\t\t\t\t\t\t<onclick condition="%s">%s</onclick>' % (c, act))
    return '\n'.join(out)


def item(label, opt, icon, toks, visible):
    return ('\t\t\t\t\t<item>\n\t\t\t\t\t\t<label>%s</label>\n\t\t\t\t\t\t<label2>$VAR[Aeon_VOS_%s]</label2>\n'
            '\t\t\t\t\t\t<icon>%s</icon>\n%s\n\t\t\t\t\t\t<visible>%s</visible>\n\t\t\t\t\t</item>\n'
            % (label, opt, icon, cycle(opt, toks), visible))


# -------------------------------------------------------------------------- what each View settings value shows
SK = 'Skin.String(aeon.%s)'
G_STEP = lambda key: [(eq(SK % key, t), lab) for t, lab in STEPS if t != 'z'] + [(None, '$NUMBER[0]')]   # noqa: E731
VOS = {
    'ratings': ([('on', L % 31547), ('off', L % 31548)], [(None, L % 31547)]),
    'mediainfo': ([('on', L % 31547), ('off', L % 31548)], [(None, L % 31547)]),
    'plot': ([('on', L % 31547), ('off', L % 31548)], [(None, L % 31547)]),
    'boxbg': ([('colors', L % 31551), ('neutral', L % 31549), ('fanart', L % 31550), ('follow', L % 31543)],
              [(eq(SK % 'boxbg', 'neutral'), L % 31549), (eq(SK % 'boxbg', 'fanart'), L % 31550),
               (eq(SK % 'boxbg', 'follow'), L % 31543), (None, L % 31551)]),
    'strip': ([('on', L % 31802), ('off', L % 31801)], [('Skin.HasSetting(aeon.strip.perm)', L % 31802), (None, L % 31801)]),
    'fop': (STEPS, G_STEP('x.fop')),
    'fblur': ([('off', L % 31548)] + STEPS + [('light', '$NUMBER[0]'), ('medium', '+1'), ('strong', '+2')],
              [(eq(SK % 'x.fblur', 'off'), L % 31548)] + [(eq(SK % 'x.fblur', t), lab) for t, lab in STEPS if t != 'z'] +
              [(eq(SK % 'x.fblur', 'medium'), '+1'), (eq(SK % 'x.fblur', 'strong'), '+2'), (None, '$NUMBER[0]')]),
    'ftint': ([('off', L % 31548), ('light', L % 31672), ('def', L % 31071), ('strong', L % 31673)],
              [(eq(SK % 'x.ftint', 'off'), L % 31548), (eq(SK % 'x.ftint', 'light'), L % 31672),
               (eq(SK % 'x.ftint', 'strong'), L % 31673), (None, L % 31071)]),
    'pshadow': ([('mild', A % 32670), ('medium', L % 31071), ('strong', L % 31673), ('heavy', A % 32671)],
                [(eq(SK % 'fgshadow', 'mild'), A % 32670), (eq(SK % 'fgshadow', 'strong'), L % 31673),
                 (eq(SK % 'fgshadow', 'heavy'), A % 32671), (None, L % 31071)]),
    'pop': (STEPS, G_STEP('x.pop')),
    'pblur': ([('off', L % 31548), ('light', L % 31672), ('medium', L % 31071), ('strong', L % 31673)],
              [(eq(SK % 'fgmat', 'clear'), L % 31548), (eq(SK % 'x.pblur', 'off'), L % 31548), (eq(SK % 'x.pblur', 'light'), L % 31672),
               (eq(SK % 'x.pblur', 'strong'), L % 31673), (None, L % 31071)]),
    'ptint': (STEPS, G_STEP('x.ptint')),
}


def library_alpha(t):
    """Includes_Aeon_Glass.xml: the library fanart's alpha variables lose the Backdrop strength lines"""
    n = 0
    for name in ('Aeon_VFanAlpha', 'Aeon_VFanAlphaG', 'Aeon_VFanAlphaX', 'Aeon_VFanAlphaGX', 'Aeon_VWashAlpha', 'Aeon_FlixFanAlpha'):
        s = t.index('<variable name="%s">' % name)
        e = t.index('</variable>', s)
        blk = t[s:e]
        new = re.sub(r'\t\t<value condition="[^"]*(?:aeon\.vo\.bgs|aeon\.backdrop\.dim)[^"]*">[^<]*</value>\n', '', blk)
        n += blk.count('<value') - new.count('<value')
        t = t[:s] + new + t[e:]
    t = t.replace('<expression name="AX_FanBlur">[[!String.IsEmpty(Window(Home).Property(aeon.vo.fblur)) + !String.IsEqual(Window(Home).Property(aeon.vo.fblur),off)] | [String.IsEmpty(Window(Home).Property(aeon.vo.fblur)) + !String.IsEmpty(Skin.String(aeon.x.fblur))]]',
                  '<expression name="AX_FanBlur">[[!String.IsEmpty(Window(Home).Property(aeon.vo.fblur)) + !String.IsEqual(Window(Home).Property(aeon.vo.fblur),off)] | [String.IsEmpty(Window(Home).Property(aeon.vo.fblur)) + !String.IsEqual(Skin.String(aeon.x.fblur),off)]]')
    if 'name="AX_TintCol"' not in t:
        i = t.index('\t<expression name="AXT_def">')
        t = t[:i] + ('\t<!-- 0.56.45 viewset: the tint\'s colour, the fanart\'s own or else a frosted blue-grey -->\n'
                     '\t<variable name="AX_TintCol">\n\t\t<value condition="!String.IsEmpty(Fanart.Color1)">$INFO[Fanart.Color1]</value>\n'
                     '\t\t<value>ffb0c4de</value>\n\t</variable>\n') + t[i:]
    print('  library fanart alpha: %d Backdrop strength lines out' % n)
    return t


def tint_layers(t):
    """Includes_Aeon_Views2.xml: Light / Strong tint in both fanart looks"""
    if 'AX_TintCol' in t:
        return t
    for tag, end in (('AXT_light', '7'), ('AXT_strong', '28')):
        old = re.search(r'<control type="image"><width>1920</width><height>1080</height><texture colordiffuse="\$INFO\[Fanart.Color1\]">common/white.png</texture>'
                        r'<animation effect="fade" end="%s" time="0" condition="true">Conditional</animation><visible>\$EXP\[Aeon_FanShown\] \+ \$EXP\[Aeon_FanFrosted\] \+ \$EXP\[%s\]</visible></control>' % (end, tag), t)
        assert old, tag
        t = t.replace(old.group(0), old.group(0).replace('$INFO[Fanart.Color1]', '$VAR[AX_TintCol]'))
    # the Dimmed look: its picture comes later; the same two layers after it (and its blurred copy)
    anchor = re.search(r'\n(\t+)<control type="image"><!-- 0.56.28 expert_05628 --><width>1920</width><height>1080</height><aspectratio>stretch</aspectratio>'
                       r'<fadetime>400</fadetime><texture background="true" colordiffuse="\$VAR\[Aeon_VFanAlpha\]">\$INFO\[Window\(Home\).Property\(aeon.fanblur\)\]</texture>'
                       r'<visible>\$EXP\[Aeon_FanShown\] \+ !\$EXP\[Aeon_FanFrosted\] \+ \$EXP\[AX_FanBlur\]</visible></control>', t)
    assert anchor, 'dimmed blur layer'
    ind = anchor.group(1)
    add = ''.join('\n%s<control type="image"><!-- 0.56.45 viewset --><width>1920</width><height>1080</height><texture colordiffuse="$VAR[AX_TintCol]">common/white.png</texture>'
                  '<animation effect="fade" end="%s" time="0" condition="true">Conditional</animation><visible>$EXP[Aeon_FanShown] + !$EXP[Aeon_FanFrosted] + $EXP[%s]</visible></control>'
                  % (ind, end, tag) for tag, end in (('AXT_light', '7'), ('AXT_strong', '28')))
    return t[:anchor.end()] + add + t[anchor.end():]


def view_items(t):
    """Includes_LibraryPanel.xml ViewSet_Items: Backdrop strength out, Fanart blur's new steps, the four panel rows"""
    s = t.index('<include name="ViewSet_Items">')
    e = t.index('</include>', s)
    blk = t[s:e]
    blk = re.sub(r'\t*<item>(?:(?!</item>).)*Aeon_VOS_bgs(?:(?!</item>).)*</item>\n', '', blk, flags=re.S)
    m = re.search(r'(<item>(?:(?!</item>).)*Aeon_VOS_fblur(?:(?!</item>|<onclick).)*)(\t*<onclick(?:(?!</item>).)*</onclick>\n)((?:(?!</item>).)*</item>)', blk, re.S)
    assert m, 'fblur item'
    blk = blk[:m.start(2)] + cycle('fblur', ['off', 'm2', 'm1', 'z', 'p1', 'p2']) + '\n' + blk[m.end(2):]
    if 'Aeon_VOS_pshadow' not in blk:
        m = re.search(r'<item>(?:(?!</item>).)*Aeon_VOS_ftint(?:(?!</item>).)*</item>\n', blk, re.S)
        assert m, 'ftint item'
        add = (item(A % 32668, 'pshadow', 'aeon/icons/layers.png', ['mild', 'medium', 'strong', 'heavy'], 'Skin.HasSetting(aeon.vglass)') +
               item(A % 32674, 'pop', 'aeon/icons/layers.png', ['m2', 'm1', 'z', 'p1', 'p2'], 'Skin.HasSetting(aeon.vglass)') +
               item(A % 32676, 'pblur', 'aeon/icons/blur.png', ['off', 'light', 'medium', 'strong'],
                    'Skin.HasSetting(aeon.fglass)') +      # 0.56.48: also in Clear (Default = Off there)
               item(A % 32678, 'ptint', 'aeon/icons/sparkle.png', ['m2', 'm1', 'z', 'p1', 'p2'], 'Skin.HasSetting(aeon.vglass)'))
        blk = blk[:m.end()] + add + blk[m.end():]
    return t[:s] + blk + t[e:]


def vos_vars(t):
    """Includes_Aeon_Sub.xml: the value labels"""
    for opt, (explicit, defaults) in VOS.items():
        new = var('Aeon_VOS_%s' % opt, vos(opt, explicit, defaults))
        m = re.search(r'\t<variable name="Aeon_VOS_%s">.*?</variable>' % opt, t, re.S)
        if m:
            t = t[:m.start()] + new + t[m.end():]
        else:
            i = t.index('\t<variable name="Aeon_VOS_ratings">')
            t = t[:i] + new + '\n' + t[i:]
    return t


# -------------------------------------------------------------------------- the panels follow the view's values
PANEL = (('x.pop', 'pop', 'z'), ('x.ptint', 'ptint', 'z'), ('fgshadow', 'pshadow', 'medium'))


def view_aware(t):
    """Skin.String(aeon.<key>) tests -> the view's value, else Skin settings' (not inside an already rewritten test)"""
    n = 0
    for key, opt, zero in PANEL:
        v = VO % opt
        k = re.escape('Skin.String(aeon.%s)' % key)

        def is_eq(m, v=v, key=key):
            return '[%s | [String.IsEmpty(%s) + String.IsEqual(Skin.String(aeon.%s),%s)]]' % (eq(v, m.group(1)), v, key, m.group(1))

        def is_empty(_m, v=v, key=key, zero=zero):
            return '[%s | [String.IsEmpty(%s) + String.IsEmpty(Skin.String(aeon.%s))]]' % (eq(v, zero), v, key)
        mine = r'(?<!String\.IsEmpty\(%s\) \+ )' % re.escape(v)      # not the Skin settings half of a rewritten test
        t, a = re.subn(mine + r'String\.IsEqual\(%s,(\w+)\)' % k, is_eq, t)
        t, b = re.subn(mine + r'String\.IsEmpty\(%s\)' % k, is_empty, t)
        n += a + b
    return t, n


def main():
    g = library_alpha(rd('Includes_Aeon_Glass.xml'))
    wr('Includes_Aeon_Glass.xml', g)
    wr('Includes_Aeon_Views2.xml', tint_layers(rd('Includes_Aeon_Views2.xml')))
    wr('Includes_LibraryPanel.xml', view_items(rd('Includes_LibraryPanel.xml')))
    wr('Includes_Aeon_Sub.xml', vos_vars(rd('Includes_Aeon_Sub.xml')))
    total = 0
    for name in ('Includes_Aeon.xml', 'Includes_Aeon_Glass.xml', 'Includes_Fused.xml'):
        t, n = view_aware(rd(name))
        total += n
        wr(name, t)
    print('  panel tests made view-aware: %d' % total)
    print('viewset_05645 done')



def fg_vos():
    """the Fused Glass rows of View settings (FG_VOS block): Watched status and Logos instead of titles say their
    Skin settings value too (box shot 2026-11-18: they read only "Default")"""
    p = os.path.join(D, 'Includes_Fused.xml')
    t = io.open(p, encoding='utf-8').read()
    for name, rule in (('FG_VOS_watched', ('String.IsEqual(Skin.String(aeon.watchedmarkers),off)', L % 31548, L % 31547)),
                       ('FG_VOS_logos', ('Skin.HasSetting(aeon.nologos)', L % 31548, L % 31547))):
        s = t.index('<variable name="%s">' % name)
        e = t.index('</variable>', s)
        blk = t[s:e]
        if DEF in blk:
            continue
        cond, when, other = rule
        blk = blk.replace('\t\t<value>$LOCALIZE[571]</value>\n',
                          '\t\t<value condition="%s">%s (%s)</value>\n\t\t<value>%s (%s)</value>\n' % (cond, DEF, when, DEF, other))
        t = t[:s] + blk + t[e:]
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(p)


if __name__ == '__main__':
    main()
    fg_vos()
