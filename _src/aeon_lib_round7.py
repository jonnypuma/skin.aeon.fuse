# -*- coding: utf-8 -*-
"""0.56.20 chain step 16 (after aeon_lib_round6.py): premieres and finales (script.aeon.helper 0.3.97: the Planner's
items carry aeon.epkindtext, the show in an episode / season list aeon.next.kind). The user (2026-11-17): "Make the
helper to also show if next airing episode is a series finale, a season finale, a series premiere, a season premiere.
maybe we could show that in the planner as well somehow."
- Planner (Aeon / Aeon Glass): the item's tag says SEASON FINALE, SERIES PREMIERE ... instead of EPISODE; the Planner
  spotlight's episode line ends with it;
- the next-episode line under the Aeon Episode list / season list: S3 E5 · Wed 18 Nov · Season finale.
Runs once (marker)."""
import io
import os
import xml.etree.ElementTree as ET

V3 = os.path.join('1080i', 'Includes_Aeon_Views3.xml')
VID = os.path.join('1080i', 'Includes_Aeon_Video.xml')
MARK = '0.56.20 epkind'
NEXT = '$INFO[Window(Home).Property(aeon.next.day)][/UPPERCASE]</label>'
NEXT_NEW = '$INFO[Window(Home).Property(aeon.next.day)]$INFO[Window(Home).Property(aeon.next.kind),  ·  ,][/UPPERCASE]</label>'


def main():
    t = io.open(V3, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    old = '\t\t<value condition="!String.IsEmpty(ListItem.TVShowTitle)">[UPPERCASE]$LOCALIZE[20359][/UPPERCASE]</value>'
    assert t.count(old) == 1, t.count(old)
    t = t.replace(old, '\t\t<value condition="!String.IsEmpty(ListItem.Property(aeon.epkindtext))">[UPPERCASE]$INFO[ListItem.Property(aeon.epkindtext)][/UPPERCASE]</value><!-- %s: premiere / finale -->\n' % MARK + old, 1)
    t = t.replace('$INFO[ListItem.Property(aeon.eptitle),  ·  ,]</value>', '$INFO[ListItem.Property(aeon.eptitle),  ·  ,]$INFO[ListItem.Property(aeon.epkindtext),  ·  ,]</value>')
    t = t.replace(NEXT, NEXT_NEW)
    v = io.open(VID, encoding='utf-8').read()
    v = v.replace(NEXT, NEXT_NEW)
    for p, x in ((V3, t), (VID, v)):
        io.open(p, 'w', encoding='utf-8', newline='\n').write(x)
        ET.parse(p)
    print('ok')


if __name__ == '__main__':
    main()
