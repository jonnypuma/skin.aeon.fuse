# -*- coding: utf-8 -*-
"""0.56.20 after the box test (Lawrence of Arabia with Curator's sidecar): the chip row was 700 wide and the source chip
was cut off after seven chips, and the second card line ran out of room. The chip row is 1100 wide (it still ends inside
the hero card), the edition is no chip (it is the card's first line), and the card's lines are: source / edition /
size / bitrate; the main audio track, the number of audio tracks and commentaries; subtitles (SDH) and chapters.
Run after mediainfo_skin_05620.py; once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Includes_VideoInfo.xml')
MARK = '0.56.20 mediainfo_skin2'
H = 'Window(Home).Property(aeon.mi.%s)'
ON = 'Skin.HasSetting(aeon.mi.sidecar) + String.IsEqual(Window(Home).Property(aeon.mi.path),ListItem.FileNameAndPath)'


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    old = '<width>700</width><height>34</height><orientation>horizontal</orientation><itemgap>8</itemgap><usecontrolcoords>true</usecontrolcoords>'
    assert t.count(old) == 1, t.count(old)
    t = t.replace(old, old.replace('<width>700</width>', '<width>1100</width>') + '<!-- %s: room for the sidecar\'s source chip -->' % MARK)
    edition = re.findall(r'\t*<control type="button">[^\n]*\$INFO\[Window\(Home\)\.Property\(aeon\.mi\.edition\)\][^\n]*</control>\n', t)
    assert len(edition) == 2, len(edition)
    for e in edition:
        t = t.replace(e, '')
    a = t.index('<!-- 0.56.20 mediainfo_skin: what the mediainfo sidecar says -->')
    b = t.index('\t\t\t</control>', a)
    L1 = '$INFO[%s]$INFO[%s, · ]$INFO[%s, · ]$INFO[%s, · ]$INFO[%s, · ]' % (H % 'source', H % 'edition', H % '3d', H % 'size', H % 'bitrate')
    L2 = '$INFO[%s]$INFO[%s, · $LOCALIZE[292] ]$INFO[%s, · $ADDON[skin.aeon.fuse 32617] ]' % (H % 'audio', H % 'audio.count', H % 'commentary')
    L3 = '$INFO[%s,$LOCALIZE[287] ]$INFO[%s, ]$INFO[%s, · $ADDON[skin.aeon.fuse 32618] ]' % (H % 'subs.count', H % 'sdh', H % 'chapters')
    lines = '<!-- 0.56.20 mediainfo_skin: what the mediainfo sidecar says (%s: three lines that fit) -->\n' % MARK
    for i, (lab, font, col) in enumerate(((L1, 'lb_small_20_bold', '$VAR[AG_Ink]'), (L2, 'lb_small_20', '$VAR[AG_Ink2]'), (L3, 'lb_small_20', '$VAR[AG_Ink2]'))):
        lines += ('\t\t\t\t<control type="label"><left>36</left><top>%d</top><width>552</width><height>30</height><aligny>center</aligny>'
                  '<font>%s</font><textcolor>%s</textcolor><label>%s</label><visible>%s + !String.IsEmpty(%s)</visible></control>\n'
                  % (186 + 32 * i, font, col, lab, ON, H % 'from'))
    t = t[:a] + lines + t[b:]
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    print('ok')


if __name__ == '__main__':
    main()
