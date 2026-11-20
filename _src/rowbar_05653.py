# -*- coding: utf-8 -*-
"""0.56.53 Skin settings rows in Fused Glass style (user, 2026-11-20, Libraries: "scrollbar is not flush with the focus
highlight bar top line ... also focus bar is missing the same brightness on it's lower line", "it is not possible to
focus on scrollbar"):
1. the focused row drew an extra 55ffffff rule on its top only (121 rows), over the bar's own outline: in the style it
   goes, so the bar's top and bottom lines are alike, as on every other style bar (Home menu, editors, dialogs);
2. the gutter's bars (9771 ... 9799) start on the title band's rule (191), the focus bar's top line, to the frame's
   bottom (769);
3. Right from a row stops on its page's scroll bar (as on the Home menu page) - not while that row picks a value
   (OK-only choose mode keeps Left/Right); the bar: Left back to the list, Right nowhere.
Run after gutter_05653.py. Repeatable."""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, '..', '1080i', 'SkinSettings.xml')
FUSED = os.path.join(HERE, '..', '1080i', 'Includes_Fused.xml')
LINE_OLD = ('<texture colordiffuse="55ffffff">common/white.png</texture><visible>!$EXP[Aeon_Fused] + [!$EXP[Aeon_FGlass] | $EXP[FGS]]</visible>')
LINE_NEW = ('<texture colordiffuse="55ffffff">common/white.png</texture><visible>!$EXP[Aeon_Fused] + !$EXP[Aeon_FGlass]</visible>')
PAGES = re.compile(r'<control type="grouplist" id="(\d+)">\s*<left>[^<]*</left><top>[^<]*</top><width>[^<]*</width><height>[^<]*</height>'
                   r'\s*<orientation>vertical</orientation><itemgap>0</itemgap><usecontrolcoords>true</usecontrolcoords>'
                   r'\s*<scrolltime[^>]*>\d+</scrolltime><pagecontrol>(\d+)</pagecontrol>')


def main():
    s = io.open(P, encoding='utf-8').read()
    n1 = s.count(LINE_OLD)
    s = s.replace(LINE_OLD, LINE_NEW)
    s = s.replace('<animation effect="slide" end="-19,-5" time="0" condition="$EXP[FGS]">Conditional</animation>',
                  '<animation effect="slide" end="-19,-6" time="0" condition="$EXP[FGS]">Conditional</animation>')
    s = s.replace('<include condition="$EXP[FGS]">FGS_H768</include>', '<include condition="$EXP[FGS]">FGS_H769</include>')
    n3 = 0
    for m in list(PAGES.finditer(s))[::-1]:
        gid, bar = m.group(1), m.group(2)
        e = s.index('<control type="scrollbar" id="%s">' % bar, m.end())
        seg = s[m.end():e]
        if '<!-- rowbar -->' in seg:
            continue

        def right(b):
            rid = b.group(1)
            return b.group(0) + '<onright condition="!String.IsEqual(Window(Home).Property(aeon.pickrow),%s)">%s</onright>' % (rid, bar)
        seg, k = re.subn(r'<control type="button" id="(\d+)">', right, seg)
        n3 += k
        s = s[:m.end()] + '<!-- rowbar -->' + seg + s[e:]
        j = s.index('<control type="scrollbar" id="%s">' % bar)
        end = s.index('</control>', j)
        x = s[j:end]
        if '<onright>' not in x:
            x = x.replace('<onleft>%s</onleft>' % gid, '<onleft>%s</onleft><onright>noop</onright><onback>%s</onback>' % (gid, gid), 1)
            s = s[:j] + x + s[end:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    t = io.open(FUSED, encoding='utf-8').read()
    if '<include name="FGS_H769">' not in t:
        t = t.replace('<include name="FGS_H768"><height>768</height></include>',
                      '<include name="FGS_H768"><height>768</height></include><include name="FGS_H769"><height>769</height></include>', 1)
        io.open(FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    print('extra top rules off: %d; Right to the bar: %d rows' % (n1, n3))


if __name__ == '__main__':
    main()
