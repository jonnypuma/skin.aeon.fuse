# -*- coding: utf-8 -*-
"""0.56.20 after the box test: the Planner's Week view showed no premiere / finale. Its cards (Includes_Planner.xml, seven
day lists) draw line 2 from Aeon_Pl_Sub (2x04   The Boog); the kind only reached Aeon_Pl_Kind, which the list rows use.
The cards get their own line 2, Aeon_Pl_CardSub: the episode code and the kind in place of the episode's title when the
helper names one (3x01   Season premiere; a premiere's title is often just "Episode 1"), else as before. Kept in
Includes_Planner.xml because rebuild_aeon_chain.py restores Includes_Aeon_Views3.xml. Runs once (marker)."""
import io
import os
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Includes_Planner.xml')
MARK = '0.56.20 planner_kind'
VAR = ('\t<!-- %s: the Week cards\' line 2, the premiere / finale in place of the episode title -->\n'
       '\t<variable name="Aeon_Pl_CardSub">\n'
       '\t\t<value condition="!String.IsEmpty(ListItem.TVShowTitle) + !String.IsEmpty(ListItem.Property(aeon.epkindtext))">'
       '$VAR[Aeon_EpCode]$INFO[ListItem.Property(aeon.epkindtext),   ,]</value>\n'
       '\t\t<value>$VAR[Aeon_Pl_Sub]</value>\n'
       '\t</variable>\n') % MARK


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    n = t.count('$VAR[Aeon_Pl_Sub]')
    assert n == 14, n
    t = t.replace('$VAR[Aeon_Pl_Sub]', '$VAR[Aeon_Pl_CardSub]')
    i = t.index('<includes>') + len('<includes>')
    t = t[:i] + '\n' + VAR + t[i:].lstrip('\n')
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    print('ok', n)


if __name__ == '__main__':
    main()
