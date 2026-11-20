# -*- coding: utf-8 -*-
"""0.56.22 (screensaver.aeon.fuse 1.3.0, helper 0.3.98): the screensaver works in rounds. The user: "every item
displayed is one dot in the sequence and it does 10 items at a time or whatever the user has set it to and then it just
goes back to the first dot and does 10 random more from the sources the user has set to use".
List 9701 now holds one round (helper ?info=ssround: N items mixed from the switched-on sources, in its own order, so no
sortby random); each item carries its kind (ListItem.Property(aeon.ss.kind)), which replaces the window property of
the section on show; the pager's ring follows the list position (Container(9701).CurrentItem), the dots count the round
(Window(Home).Property(aeon.ss.pages), set by the helper, so they stay while a new round loads). Safe to run again."""
import io
import os
import xml.etree.ElementTree as ET

SS = os.path.join('1080i', 'Custom_1156_Screensaver.xml')
SUB = os.path.join('1080i', 'Includes_Aeon_Sub.xml')
KIND_OLD, KIND_NEW = 'Window(Home).Property(aeon.ss.kind)', 'Container(9701).ListItem.Property(aeon.ss.kind)'
PAGE_OLD, PAGE_NEW = 'Window(Home).Property(aeon.ss.page)', 'Container(9701).CurrentItem'


def main():
    t = io.open(SS, encoding='utf-8').read()
    t = t.replace('''	(Settings > Interface > Screensaver: on / off and wait time are Kodi's). The add-on rotates the library section on show:
	Window(Home).Property(aeon.ss.kind) = movies / tvshows / music, aeon.ss.path = its library path.''',
                  '''	(Settings > Interface > Screensaver: on / off and wait time are Kodi's). The add-on asks for one round at a time
	(0.56.22, screensaver 1.3.0): aeon.ss.path = the helper's ?info=ssround list, N items mixed from the switched-on sources,
	each with ListItem.Property(aeon.ss.kind) = movies / tvshows / music / cinema / today / tomorrow.''')
    t = t.replace(KIND_OLD, KIND_NEW).replace(PAGE_OLD, PAGE_NEW)
    t = t.replace('<content limit="10" sortby="random" browse="never">$VAR[Aeon_SSPath]</content>',
                  '<content limit="10" browse="never">$VAR[Aeon_SSPath]</content><!-- 0.56.22: the round keeps the helper\'s mixed order -->')
    t = t.replace('<!-- pager dots (0.56.20 ss_pager): one per section of the rotation (screensaver.aeon.fuse 1.2.2 aeon.ss.pages / aeon.ss.page), the one on show ringed; hidden with a single section -->',
                  '<!-- pager dots (0.56.22 ss_round): one per item of the round (aeon.ss.pages), the one on show ringed (Container(9701).CurrentItem); hidden with a single item -->')
    io.open(SS, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(SS)
    s = io.open(SUB, encoding='utf-8').read()
    a = s.index('<variable name="Aeon_SSKindWord">')
    b = s.index('</variable>', a)
    s = s[:a] + s[a:b].replace(KIND_OLD, KIND_NEW) + s[b:]
    io.open(SUB, 'w', encoding='utf-8', newline='\n').write(s)
    ET.parse(SUB)
    print('kind left', t.count(KIND_OLD), 'page left', t.count(PAGE_OLD), 'sortby random', t.count('sortby="random" browse="never">$VAR[Aeon_SSPath]'))


if __name__ == '__main__':
    main()
