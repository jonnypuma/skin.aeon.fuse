# -*- coding: utf-8 -*-
"""0.56.15 view names (the user: "rename the Music fanart list views to Compact list, same view name for artists,
albums and track views"; "Music albums: The fanart list and fanart wall are identical ... remove the Fanart Wall view";
"Rule for changing view names: always update the picker names too. review all picker names and check if they are the
same as the names displayed in the view"):
- music List (513): Compact list (string 31142, the video Compact list's) in the picker and the view's heading, for
  artists, albums, songs and genres; its picker line (31084) reads "Rows with A-Z keys" (strings_05615.py);
- Fanart wall (534) no longer offered for albums (picker item gone, the view hidden for albums in all themes);
- the review: the Aeon / Glass heading of a video view now uses the names the picker gives per content (Fused Glass's
  FG_L_ViewName: Show posters, Season posters, Episode wall, Season poster wall combined); before, it showed the view's
  own name (Poster wall, Landscape wall, Combined).
Runs once."""
import io
import os
import re
import xml.etree.ElementTree as ET

MARK = '0.56.15 views_05615'
D = '1080i'


def patch(fn, pairs):
    p = os.path.join(D, fn)
    t = io.open(p, encoding='utf-8').read()
    for old, new, n in pairs:
        assert t.count(old) == n, (fn, old[:80], t.count(old))
        t = t.replace(old, new)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(p)


def main():
    # each file is patched once (its own marker), so the Aeon view generator chain can restore Sub / Views2 and run
    # this again
    pick = io.open(os.path.join(D, 'Custom_1164_MusicViews.xml'), encoding='utf-8').read()
    if MARK not in pick:
        item534 = re.search(r'\n[ \t]*<item>[^\n]*?<icon>534</icon>[^\n]*?<visible>Container\.Content\(albums\)</visible></item>', pick)
        assert item534
        patch('Custom_1164_MusicViews.xml', [
            ('<item><label>$LOCALIZE[31083]</label><label2>$LOCALIZE[31084]</label2><icon>513</icon>',
             '<!-- %s: Compact list for every music content; no Fanart wall for albums -->\n\t\t\t\t<item><label>$LOCALIZE[31142]</label><label2>$LOCALIZE[31084]</label2><icon>513</icon>' % MARK, 1),
            (item534.group(0), '', 1)])
    if MARK not in io.open(os.path.join(D, 'Includes_Aeon_Sub.xml'), encoding='utf-8').read():
        patch('Includes_Aeon_Sub.xml', [
        ('.List.)">$LOCALIZE[31083]</value>', '.List.)">$LOCALIZE[31142]</value>', 4),
        ('\t\t<value condition="String.IsEqual(Window(Home).Property(aeon.vo.base),aeon.vo.albums.$LOCALIZE[31088].)">$LOCALIZE[31109]</value>\n\t\t<value>$INFO[Container.Viewmode]</value>',
         '\t\t<value condition="String.IsEqual(Window(Home).Property(aeon.vo.base),aeon.vo.albums.$LOCALIZE[31088].)">$LOCALIZE[31109]</value>\n'
         '\t\t<!-- %s: video views by the picker\'s names per content (Show posters, Episode wall ...) -->\n\t\t<value>$VAR[FG_L_ViewName]</value>' % MARK, 1)])
    v2 = io.open(os.path.join(D, 'Includes_Aeon_Views2.xml'), encoding='utf-8').read()
    a = v2.index('<control type="panel" id="534">')
    seg = v2[a:v2.index('</visible>', a) + 10]
    if 'Container.Content(albums)' in seg:
        patch('Includes_Aeon_Views2.xml', [(seg, seg.replace('<visible>Container.Content(artists) | Container.Content(albums)</visible>', '<visible>Container.Content(artists)</visible>'), 1)])
    fu = io.open(os.path.join(D, 'Includes_Fused.xml'), encoding='utf-8').read()
    a = fu.index('<control type="panel" id="534">')
    m = re.search(r'<visible>([^<]*)</visible>', fu[a:a + 3000])
    if 'Container.Content(albums)' not in m.group(1):      # Fused Glass's Fanart wall never took albums (Kodi fell back
        print('ok')                                         # to the list, hence "identical")
        return
    new =re.sub(r'\s*\|\s*Container\.Content\(albums\)|Container\.Content\(albums\)\s*\|\s*', '', m.group(1))
    seg = fu[a:a + m.end()]
    patch('Includes_Fused.xml', [(seg, seg.replace(m.group(0), '<visible>%s</visible>' % new), 1)])
    print('ok')


if __name__ == '__main__':
    main()
