# -*- coding: utf-8 -*-
"""0.56.42 Library fanart opacity, blur and tint per library view (View settings), on top of Skin settings > Libraries.
The user: "Library fanart opacity, blur and tint need to be options in the view settings which can be stored
individually for each library view."

View settings (ViewSet_Items) gets three rows after Backdrop strength, shown while the view shows fanart. They are kept
like the other view options (skin strings aeon.vo.<content>.<viewmode>.fop / fblur / ftint; the helper publishes the
view's values as Window(Home).Property(aeon.vo.fop / fblur / ftint)); Default (empty) follows Skin settings:
    opacity  '' | m2 | m1 | z (the skin's own, 0) | p1 | p2      Skin settings: '' | m2 | m1 | p1 | p2
    blur     '' | off | light | medium | strong                   Skin settings: '' (off) | light | medium | strong
    tint     '' | off | light | def (the skin's own) | strong     Skin settings: '' | off | light | strong
The places that read the Skin settings values read "the view's value, else Skin settings'" now: expressions AXF_* and
AX_FanBlur (Includes_Aeon_Glass.xml), the tint layers (Includes_Aeon_Views2.xml, new expressions AXT_*), and the helper's
blurred fanart (blurcache.fantick, helper 0.3.108). Repeatable."""
import io
import os
import re
import xml.etree.ElementTree as ET

D = '1080i'
VO = 'Window(Home).Property(aeon.vo.%s)'
SK = 'Skin.String(aeon.x.%s)'


def rd(name):
    return io.open(os.path.join(D, name), encoding='utf-8').read()


def wr(name, text):
    io.open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n').write(text)
    ET.parse(os.path.join(D, name))


def either(opt, value):
    """the view's value is `value`, or the view follows Skin settings and that is `value` ('' = empty)"""
    if value:
        mine, glob = 'String.IsEqual(%s,%s)' % (VO % opt, value), 'String.IsEqual(%s,%s)' % (SK % opt, value)
    else:
        mine, glob = None, 'String.IsEmpty(%s)' % (SK % opt)
    follow = '[String.IsEmpty(%s) + %s]' % (VO % opt, glob)
    return '[%s | %s]' % (mine, follow) if mine else follow


EXPR = {
    'AXF_m2': either('fop', 'm2'), 'AXF_m1': either('fop', 'm1'), 'AXF_p1': either('fop', 'p1'), 'AXF_p2': either('fop', 'p2'),
    'AXF_On': '[$EXP[AXF_m2] | $EXP[AXF_m1] | $EXP[AXF_p1] | $EXP[AXF_p2]]',
    'AX_FanBlur': '[[!String.IsEmpty(%s) + !String.IsEqual(%s,off)] | [String.IsEmpty(%s) + !String.IsEmpty(%s)]] + !String.IsEmpty(Window(Home).Property(aeon.fanblur))'
                  % (VO % 'fblur', VO % 'fblur', VO % 'fblur', SK % 'fblur'),
}
TINT = {
    'AXT_def': '[String.IsEqual(%s,def) | [String.IsEmpty(%s) + String.IsEmpty(%s)]]' % (VO % 'ftint', VO % 'ftint', SK % 'ftint'),
    'AXT_light': either('ftint', 'light'), 'AXT_strong': either('ftint', 'strong'),
}


def expressions():
    t = rd('Includes_Aeon_Glass.xml')
    for name, cond in EXPR.items():
        x = re.search(r'<expression name="%s">.*?</expression>' % name, t)
        assert x, name
        t = t[:x.start()] + '<expression name="%s">%s</expression>' % (name, cond) + t[x.end():]
    if 'name="AXT_def"' not in t:
        i = t.index('<expression name="AX_FanBlur">')
        t = t[:i] + '<!-- 0.56.42 viewfan_05642: Library fanart tint, the view\'s value or Skin settings\' -->\n\t' + ''.join(
            '<expression name="%s">%s</expression>\n\t' % kv for kv in TINT.items()) + t[i:]
    wr('Includes_Aeon_Glass.xml', t)
    v = rd('Includes_Aeon_Views2.xml')
    for old, new in (('String.IsEmpty(Skin.String(aeon.x.ftint))', '$EXP[AXT_def]'),
                     ('String.IsEqual(Skin.String(aeon.x.ftint),light)', '$EXP[AXT_light]'),
                     ('String.IsEqual(Skin.String(aeon.x.ftint),strong)', '$EXP[AXT_strong]')):
        v = v.replace(old, new)
    assert 'aeon.x.ftint' not in v
    wr('Includes_Aeon_Views2.xml', v)


def item(label, opt, icon, cycle):
    base = '$INFO[Window(Home).Property(aeon.vo.base)]'
    clicks = []
    for i, value in enumerate(cycle):
        nxt = cycle[(i + 1) % len(cycle)]
        cond = 'String.IsEmpty(%s)' % (VO % opt) if not value else 'String.IsEqual(%s,%s)' % (VO % opt, value)
        act = 'Skin.SetString(%s%s,%s)' % (base, opt, nxt) if nxt else 'Skin.Reset(%s%s)' % (base, opt)
        clicks.append('\t\t\t\t\t\t<onclick condition="%s">%s</onclick>' % (cond, act))
    return ('\t\t\t\t\t<item>\n\t\t\t\t\t\t<label>%s</label>\n\t\t\t\t\t\t<label2>$VAR[Aeon_VOS_%s]</label2>\n'
            '\t\t\t\t\t\t<icon>%s</icon>\n%s\n\t\t\t\t\t\t<visible>$EXP[Aeon_FanShown]</visible>\n\t\t\t\t\t</item>\n'
            % (label, opt, icon, '\n'.join(clicks)))


def view_settings():
    t = rd('Includes_LibraryPanel.xml')
    if 'aeon.vo.base)]fop' not in t:
        anchor = '<onclick condition="String.IsEqual(Window(Home).Property(aeon.vo.bgs),strong)">Skin.Reset($INFO[Window(Home).Property(aeon.vo.base)]bgs)</onclick>\n\t\t\t\t\t</item>\n'
        assert anchor in t
        new = ('\t\t\t\t\t<!-- 0.56.42 viewfan_05642: the fanart\'s opacity, blur and tint for this view (Default = Skin settings) -->\n'
               + item('$ADDON[skin.aeon.fuse 32680]', 'fop', 'aeon/icons/image.png', ['', 'm2', 'm1', 'z', 'p1', 'p2'])
               + item('$ADDON[skin.aeon.fuse 32682]', 'fblur', 'aeon/icons/blur.png', ['', 'off', 'light', 'medium', 'strong'])
               + item('$ADDON[skin.aeon.fuse 32684]', 'ftint', 'aeon/icons/sparkle.png', ['', 'off', 'light', 'def', 'strong']))
        t = t.replace(anchor, anchor + new, 1)
    wr('Includes_LibraryPanel.xml', t)
    s = rd('Includes_Aeon_Sub.xml')
    if 'name="Aeon_VOS_fop"' not in s:
        def var(opt, pairs):
            return ('\t<variable name="Aeon_VOS_%s">\n' % opt + ''.join(
                '\t\t<value condition="String.IsEqual(%s,%s)">%s</value>\n' % (VO % opt, v, lab) for v, lab in pairs)
                + '\t\t<value>$LOCALIZE[31546]</value>\n\t</variable>\n')
        block = ('\t<!-- 0.56.42 viewfan_05642: View settings > Library fanart opacity / blur / tint (Default = Skin settings) -->\n'
                 + var('fop', [('m2', '-2'), ('m1', '-1'), ('z', '$NUMBER[0]'), ('p1', '+1'), ('p2', '+2')])
                 + var('fblur', [('off', '$LOCALIZE[31548]'), ('light', '$LOCALIZE[31672]'), ('medium', '$LOCALIZE[31071]'), ('strong', '$LOCALIZE[31673]')])
                 + var('ftint', [('off', '$LOCALIZE[31548]'), ('light', '$LOCALIZE[31672]'), ('def', '$LOCALIZE[31071]'), ('strong', '$LOCALIZE[31673]')]))
        i = s.index('\t<variable name="Aeon_VOS_bgs">')
        s = s[:i] + block + s[i:]
    wr('Includes_Aeon_Sub.xml', s)


if __name__ == '__main__':
    expressions()
    view_settings()
    print('ok')
