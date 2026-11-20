# -*- coding: utf-8 -*-
"""0.56.15 the library side strip in a music view (the user: "Music sidestrip shall have an option to choose between
Artists, Albums, Songs and Genre like the top menu for quicker navigation"): four rows at the top of LibPanel_Items
(every theme and menu style uses that list), Artists / Albums / Songs / Genres with the top menu's icons and actions;
the one on screen says Current. Runs once."""
import io
import os
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Includes_LibraryPanel.xml')
MARK = '0.56.15 libpanel_music'
ROWS = (('31298', 'common/aeon_ic_person.png', 'musicdb://artists/', 'Container.Content(artists)'),
        ('31299', 'common/aeon_ic_disc.png', 'musicdb://albums/', 'Container.Content(albums)'),
        ('31343', 'common/aeon_ic_note.png', 'musicdb://songs/', 'Container.Content(songs)'),
        ('31344', 'common/aeon_ic_genre.png', 'musicdb://genres/', 'Container.Content(genres)'))


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('already done')
        return
    anchor = '\t<include name="LibPanel_Items">\n'
    assert t.count(anchor) == 1
    items = '\t\t\t\t\t<!-- %s: music sections, as the top menu -->\n' % MARK
    for label, icon, path, now in ROWS:
        items += ('\t\t\t\t\t<item>\n'
                  '\t\t\t\t\t\t<label>$LOCALIZE[%s]</label>\n'
                  '\t\t\t\t\t\t<label2>$VAR[LibPanel_MusicNow_%s]</label2>\n'
                  '\t\t\t\t\t\t<icon>%s</icon>\n'
                  '\t\t\t\t\t\t<onclick>Dialog.Close(1160,true)</onclick>\n'
                  '\t\t\t\t\t\t<onclick>Container.Update(%s)</onclick>\n'
                  '\t\t\t\t\t\t<visible>String.IsEmpty(Window(Home).Property(aeon.libmode)) + Window.IsActive(music)</visible>\n'
                  '\t\t\t\t\t</item>\n' % (label, label, icon, path))
    t = t.replace(anchor, anchor + items, 1)
    defs = ''
    for label, icon, path, now in ROWS:
        defs += '\t<variable name="LibPanel_MusicNow_%s"><value condition="%s + String.StartsWith(Container.FolderPath,%s)">$ADDON[skin.aeon.fuse 32290]</value></variable>\n' % (label, now, path)
    t = t.replace(anchor, '\t<!-- %s: the music section on screen -->\n%s' % (MARK, defs) + anchor, 1)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    print('ok')


if __name__ == '__main__':
    main()
