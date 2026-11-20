# -*- coding: utf-8 -*-
"""0.56.18: the Glass theme is called Aeon Glass (the user, 2026-11-16: "The Glass theme, Let's rename it Aeon Glass").
Only the name people read changes: Kodi's theme value stays "Glass" (lookandfeel.skintheme, media/Glass.xbt, the
wizard's and swap.py's values), so the setting people have keeps working. String 31679 (theme picker) and the help lines
that name the theme (31579, 32054, 32261, 32457) in every language; the skin's own "Glass" name labels read 31679; the
theme picker and the Aeon Glass menu-theme picker get room for the longer name. Skippy's "Glass" card style (32429) and
the Glass / Frost materials keep their names. Runs once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

MARK = '0.56.18 rename_aeonglass'
IDS = ('31679', '31579', '32054', '32261', '32457')
WORD = re.compile(r'(?<!Fused )(?<!Aeon )(?<!Aeon-)\bGlass\b')


def po(path):
    t = io.open(path, encoding='utf-8').read()
    out, n = [], 0
    blocks = t.split('\n\n')
    for b in blocks:
        m = re.search(r'msgctxt "#(\d+)"', b)
        if m and m.group(1) in IDS:
            new = re.sub(r'^(msgid|msgstr) "(.*)"$', lambda mm: '%s "%s"' % (mm.group(1), WORD.sub('Aeon Glass', mm.group(2))), b, flags=re.M)
            n += new != b
            b = new
        out.append(b)
    io.open(path, 'w', encoding='utf-8', newline='\n').write('\n\n'.join(out))
    return n


def swap(path, old, new, count=1):
    t = io.open(path, encoding='utf-8').read()
    if t.count(old) == 0 and t.count(new) == count:
        return                                   # done on an earlier (interrupted) run
    assert t.count(old) == count, (path, old[:90], t.count(old))
    io.open(path, 'w', encoding='utf-8', newline='\n').write(t.replace(old, new))


def main():
    s = os.path.join('1080i', 'SkinSettings.xml')
    if MARK in io.open(s, encoding='utf-8').read():
        # 0.56.20: the Aeon view chain (rebuild_aeon_chain.py) restores Includes_Aeon_Sub.xml; its label again
        swap(os.path.join('1080i', 'Includes_Aeon_Sub.xml'), '<variable name="Aeon_VSetLabel">\n\t\t<value condition="Skin.HasSetting(aeon.vglass)">Glass</value>',
             '<variable name="Aeon_VSetLabel">\n\t\t<value condition="Skin.HasSetting(aeon.vglass)">$LOCALIZE[31679]</value>')
        print('already')
        return
    langs = sorted(os.listdir('language'))
    changed = {l: po(os.path.join('language', l, 'strings.po')) for l in langs}
    print('strings', changed)
    g = os.path.join('1080i', 'Includes_Aeon_Glass.xml')
    swap(g, '\t\t<value condition="Skin.HasSetting(aeon.vglass)">Glass</value>\n\t\t<value>Aeon</value>\n\t</variable>',
         '\t\t<value condition="Skin.HasSetting(aeon.vglass)">$LOCALIZE[31679]</value>\n\t\t<value>Aeon</value>\n\t</variable>')
    swap(os.path.join('1080i', 'Includes_Aeon_Sub.xml'), '<variable name="Aeon_VSetLabel">\n\t\t<value condition="Skin.HasSetting(aeon.vglass)">Glass</value>',
         '<variable name="Aeon_VSetLabel">\n\t\t<value condition="Skin.HasSetting(aeon.vglass)">$LOCALIZE[31679]</value>')
    swap(os.path.join('1080i', 'Custom_1173_SetupWizard.xml'), '\t\t\t\t\t<label>Glass</label>\n\t\t\t\t\t<label2>$ADDON[skin.aeon.fuse 32050]</label2>',
         '\t\t\t\t\t<label>$LOCALIZE[31679]</label>\n\t\t\t\t\t<label2>$ADDON[skin.aeon.fuse 32050]</label2>')
    # theme picker (Aeon | Aeon Glass | Fused Glass): the middle segment 120 -> 158, the right edge stays
    t = io.open(s, encoding='utf-8').read()
    a = t.index('<!-- Aeon | Glass | Fused Glass: Right / Left step to the neighbour -->')
    b = t.index('</control>\n\t\t\t</control>', a)
    seg = t[a:b]
    seg = seg.replace('<!-- Aeon | Glass | Fused Glass: Right / Left step to the neighbour -->',
                      '<!-- Aeon | Aeon Glass | Fused Glass: Right / Left step to the neighbour (%s: the middle one wider) -->' % MARK, 1)
    for old, new, n in (('<left>444</left><top>13</top><width>412</width>', '<left>406</left><top>13</top><width>450</width>', 2),
                        ('<left>448</left><top>13</top><width>120</width>', '<left>410</left><top>13</top><width>120</width>', 6),
                        ('<left>568</left><top>13</top><width>120</width>', '<left>530</left><top>13</top><width>158</width>', 6)):
        assert seg.count(old) == n, (old, seg.count(old))
        seg = seg.replace(old, new)
    t = t[:a] + seg + t[b:]
    # Aeon Glass menu-theme picker (theme name | Fuse): the first segment 122 -> 162, the right edge stays
    old_track = re.compile(r'<control type="image"><left>612</left><top>13</top><width>252</width><height>44</height>(<texture border="22,0,22,0" colordiffuse="[^"]+">\$VAR\[Aeon_MenuTexPill\]</texture><visible>Skin\.HasSetting\(aeon\.vglass\) \+ !Skin\.HasSetting\(aeon\.fglass\) \+ \[!?Control\.HasFocus\(9748\)\])')
    assert len(old_track.findall(t)) == 2, len(old_track.findall(t))
    t = old_track.sub(lambda m: '<control type="image"><left>572</left><top>13</top><width>292</width><height>44</height>' + m.group(1), t)
    i = t.index('<left>572</left><top>13</top><width>292</width>')
    j = t.index('</control>\n\t\t\t</control>', i)
    seg = t[i:j]
    assert seg.count('<left>616</left><top>13</top><width>122</width>') == 6
    seg = seg.replace('<left>616</left><top>13</top><width>122</width>', '<left>576</left><top>13</top><width>162</width>')
    t = t[:i] + seg + t[j:]
    io.open(s, 'w', encoding='utf-8', newline='\n').write(t)
    for f in ('SkinSettings.xml', 'Includes_Aeon_Glass.xml', 'Includes_Aeon_Sub.xml', 'Custom_1173_SetupWizard.xml'):
        ET.parse(os.path.join('1080i', f))
    swap('addon.xml', 'Three themes (Aeon, Glass, Fused Glass)', 'Three themes (Aeon, Aeon Glass, Fused Glass)')
    print('ok')


if __name__ == '__main__':
    main()
