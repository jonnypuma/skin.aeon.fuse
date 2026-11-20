# -*- coding: utf-8 -*-
"""0.56.24 List view (510): an episode row shows its certificate in the left column, like a film row; the number
stays in the title line only ("01. LA X (1)", a joined row "01-02. LA X"). Kodi keeps no certificate per episode:
ListItem.MPAA of an episode is its show's (the helper's joined rows set the show's too). Before, the column held the
episode code ("6x01") in the certificate's shape, so the number showed twice. Safe to run again."""
import io
import os
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Includes_Aeon_Video.xml')
ZOOM = '\t\t\t\t<animation effect="zoom" start="125" end="125" center="50,54" time="0" condition="String.IsEqual(ListItem.DBType,episode)">Conditional</animation>\n'


def main():
    t = io.open(P, encoding='utf-8').read()
    before = t
    t = t.replace('\t\t<value condition="String.IsEqual(ListItem.DBType,episode)">$VAR[Aeon_EpCode]</value>\n', '', 1)
    old = '<expression name="Aeon_BadgeSxE">[String.IsEqual(ListItem.DBType,episode) + String.IsEqual(Skin.String(aeon.epcode),sxe)]</expression>'
    t = t.replace(old, '<expression name="Aeon_BadgeSxE">false</expression><!-- 0.56.24: the badge is the certificate for episodes too -->')
    t = t.replace(' | String.IsEqual(ListItem.DBType,episode) | String.IsEqual(ListItem.DBType,season)]', ' | String.IsEqual(ListItem.DBType,season)]')
    n = t.count(ZOOM)
    t = t.replace(ZOOM, '')
    if t != before:
        io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
        ET.parse(P)
    print('changed' if t != before else 'already done', 'zooms removed', n)


if __name__ == '__main__':
    main()
