# -*- coding: utf-8 -*-
"""0.56.53 a scroll bar with the focus turns the accent colour, everywhere (user, 2026-11-19: "you have given scrollbar a
yellow highlight. nowhere else have you done that. i like it though but you have not done that consistently" ->
"Yes, all of them").

Aeon_SBFocus: Fused Glass fg_mark (the yellow), Aeon Glass its time-of-day accent (AG_Accent), the other themes
aeon_accent. Library windows read Aeon_SBFocus_L (lib_ colours, palette scope 0.40.4). Every texturesliderbarfocus that
is not already fg_mark takes one of them. Repeatable."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
LIB = ('Includes_Aeon_MusicLib.xml', 'Includes_Aeon_Video.xml', 'Includes_Aeon_Views2.xml', 'Includes_Views.xml',
       'Includes_Aeon_Pics.xml', 'Includes_Fused.xml')
VARS = ('\t<!-- 0.56.53 a focused scroll bar: the accent colour in every theme (_L: library windows) -->\n'
        '\t<variable name="Aeon_SBFocus">\n'
        '\t\t<value condition="Skin.HasSetting(aeon.fglass)">fg_mark</value>\n'
        '\t\t<value condition="Skin.HasSetting(aeon.vglass)">$VAR[AG_Accent]</value>\n'
        '\t\t<value>aeon_accent</value>\n'
        '\t</variable>\n'
        '\t<variable name="Aeon_SBFocus_L">\n'
        '\t\t<value condition="Skin.HasSetting(aeon.fglass)">fg_mark</value>\n'
        '\t\t<value condition="Skin.HasSetting(aeon.vglass)">$VAR[AG_Accent_L]</value>\n'
        '\t\t<value>lib_aeon_accent</value>\n'
        '\t</variable>\n')
PAT = re.compile(r'(<texturesliderbarfocus[^>]*colordiffuse=")([^"]*)(")')


def main():
    total = 0
    for name in sorted(os.listdir(D)):
        if not name.endswith('.xml'):
            continue
        p = os.path.join(D, name)
        t = io.open(p, encoding='utf-8').read()
        var = '$VAR[Aeon_SBFocus_L]' if name in LIB else '$VAR[Aeon_SBFocus]'
        n = [0]

        def sub(m):
            if m.group(2) in ('fg_mark', '$VAR[Aeon_SBFocus]', '$VAR[Aeon_SBFocus_L]'):
                return m.group(0)
            n[0] += 1
            return m.group(1) + var + m.group(3)
        t2 = PAT.sub(sub, t)
        if name == 'Includes_Aeon_Sub.xml' and '<variable name="Aeon_SBFocus">' not in t2:
            i = t2.index('\t<variable name="Aeon_SBBarFocus">')
            t2 = t2[:i] + VARS + t2[i:]
            print('variables added')
        if t2 != t:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(t2)
        if n[0]:
            print('%-32s %d' % (name, n[0]))
        total += n[0]
    print('scroll bars now accent on focus: %d' % total)


if __name__ == '__main__':
    main()
