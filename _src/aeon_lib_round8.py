# -*- coding: utf-8 -*-
"""0.56.20 chain step 17 (after aeon_lib_round7.py). The user (2026-11-17), on the List view after the new Kodi build:
"Can't artwork be loaded progressively, at least show the 100 first items from where you land". Kodi 22's art loader
(nightly 20261116) fills a list from the top, about 9 ms a film on this MariaDB library, so a film half-way down a list
of 6128 waits about 30 s for its poster; Kodi offers no way to change that order. The films' posters are local files in
their own folders (poster.jpg or <file>-poster.jpg, the same URLs Kodi has cached), and ListItem.Path is known at once:
the List view's poster pane (Aeon and Fused Glass) shows those two files under its own picture while ListItem.Art(poster)
is still empty (a file that is not there draws nothing). Shows: <folder>/poster.jpg. <file>-poster.jpg is drawn over
poster.jpg: Kodi's own local art takes it first, and a folder can hold both (Lawrence of Arabia: a different poster.jpg).
Runs once (marker)."""
import io
import os
import xml.etree.ElementTree as ET

VID = os.path.join('1080i', 'Includes_Aeon_Video.xml')
MARK = '0.56.20 aeon_lib_round8'
WAIT = 'String.IsEmpty(ListItem.Art(poster))'
MOVIE = 'String.IsEqual(ListItem.DBType,movie)'
FOLDER = '[String.IsEqual(ListItem.DBType,movie) | String.IsEqual(ListItem.DBType,tvshow)]'
STEM = '$INFO[ListItem.Path]$INFO[ListItem.FileNameNoExtension]-poster.jpg'
PLAIN = '$INFO[ListItem.Path]poster.jpg'


def main():
    t = io.open(VID, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    a = t.index('<include name="Aeon_510_ViewAeon">')
    # Fused Glass's card in the List view
    old_fg = ('<control type="image"><left>92</left><top>111</top><width>572</width><height>858</height><aspectratio scalediffuse="false">scale</aspectratio>'
              '<fadetime>350</fadetime><texture background="true" diffuse="fg/m572x858.png">$VAR[Aeon_Poster]</texture>')
    i = t.index(old_fg, a)
    lay = ''
    for src, cond in ((PLAIN, FOLDER), (STEM, MOVIE)):        # <file>-poster.jpg on top: Kodi takes it before poster.jpg
        lay += ('<control type="image"><left>92</left><top>111</top><width>572</width><height>858</height><aspectratio scalediffuse="false">scale</aspectratio>'
                '<texture background="true" diffuse="fg/m572x858.png">%s</texture><visible>%s + %s</visible></control>' % (src, WAIT, cond))
    t = t[:i] + '<!-- %s: the local poster at once, while Kodi loads the art from the top of the list -->' % MARK + lay + '\n\t\t\t\t' + t[i:]
    # Aeon's pane
    old_aeon = ('\t\t\t\t<control type="image">\n\t\t\t\t\t<width>727</width>\n\t\t\t\t\t<height>1080</height>\n\t\t\t\t\t<aspectratio>scale</aspectratio>\n'
                '\t\t\t\t\t<fadetime>350</fadetime>\n\t\t\t\t\t<texture background="true">$VAR[Aeon_Poster]</texture>\n\t\t\t\t</control>')
    j = t.index(old_aeon, a)
    lay = ''
    for src, cond in ((PLAIN, FOLDER), (STEM, MOVIE)):        # <file>-poster.jpg on top: Kodi takes it before poster.jpg
        lay += ('\t\t\t\t<control type="image"><width>727</width><height>1080</height><aspectratio>scale</aspectratio>'
                '<texture background="true">%s</texture><visible>%s + %s</visible></control>\n' % (src, WAIT, cond))
    t = t[:j] + '\t\t\t\t<!-- %s: the local poster at once (see above) -->\n' % MARK + lay + t[j:]
    io.open(VID, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(VID)
    print('ok')


if __name__ == '__main__':
    main()
