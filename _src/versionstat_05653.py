# -*- coding: utf-8 -*-
"""0.56.53 Aeon / Aeon Glass info panels (Aeon_V_Info, Aeon_V_Bar in Includes_Aeon_Views2.xml): the film's version
in front of the watched / progress status in the facts line ("ENDS 17:54  ·  THEATRICAL CUT ◎ UNWATCHED"), as in the
Fused Glass panels (edition_05653.py). The name follows edition_05653's rule (Kodi's version name unless "Standard
Edition", else the sidecar edition of the focused film). Run after edition_05653.py and ringtrack_05653.py. Repeatable."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edition_05653 as ed  # noqa: E402

P = os.path.join(HERE, '..', '1080i', 'Includes_Aeon_Views2.xml')
MARK = '<!-- 0.56.53 version before the status -->'


def main():
    s = io.open(P, encoding='utf-8').read()
    if MARK in s:
        print('version before status: already there')
        return
    names = []
    for m in re.finditer(r'\$VAR\[Aeon_LV_StatusTx\]', s):
        a = s.rfind('<include name="', 0, m.start())
        nm = s[a + 15:s.index('"', a + 15)]
        if nm not in names:
            names.append(nm)
    cond = '[%s] | [String.IsEqual(ListItem.DBType,movie) + %s]' % (ed.kodi_cond('ListItem.'), ed.side_cond('ListItem.'))
    lab = ('%s<control type="label"><width min="10" max="420">auto</width><height>34</height><aligny>center</aligny>'
           '<font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor>'
           '<label>[UPPERCASE]$VAR[Aeon_VerStat][/UPPERCASE]</label><visible>%s</visible></control>' % (MARK, cond))
    for name in names:
        a = s.index('<include name="%s">' % name)
        b = s.index('<include name=', a + 10)
        seg = s[a:b]
        i = seg.index('$VAR[Aeon_LV_StatusTx]')
        cl = [x.start() for x in re.finditer(r'<control type="image">(?:(?!<control).)*?\$EXP\[Aeon_LV_(?:Tick|Ring|Dot|Eye)', seg[:i])]
        cl += [x.start() for x in re.finditer(r'<!-- 0.56.53 ring track -->', seg[:i])]
        first = min(c for c in cl if c > i - 3000)
        s = s[:a] + seg[:first] + lab + seg[first:] + s[b:]
    var = '\t<variable name="Aeon_VerStat">%s</variable>\n' % ed.values('ListItem.')
    i = s.index('\t<variable name="Aeon_TxMedia">')
    s = s[:i] + var + s[i:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('version before status: %s' % ', '.join(names))


if __name__ == '__main__':
    main()
