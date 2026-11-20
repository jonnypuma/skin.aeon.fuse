# -*- coding: utf-8 -*-
"""0.56.20 the mediainfo sidecars on the information page (all themes; script.aeon.helper 0.3.97 reads them, Skin
settings > Details > Media info from sidecars switches them on). The user (2026-11-17): "curator's mediainfo file shall
always be preferred and all that lovely metadata can be displayed on the item's information page or as chips".
- chips after the media chips: the source (UHD Remux, Blu-ray, WEB-DL, DVD ...) and the edition;
- the "Ending at" card, under its lines: three lines - source / edition / bitrate / size; the main audio track, the
  number of audio tracks, commentaries, subtitles (SDH) and chapters; the video (codec, profile, bit depth, frame rate,
  HDR) and where it came from.
Shown only while the setting is on and the helper's aeon.mi.path is the item in focus. Runs once (marker)."""
import io
import os
import re
import xml.etree.ElementTree as ET

P = os.path.join('1080i', 'Includes_VideoInfo.xml')
MARK = '0.56.20 mediainfo_skin'
H = 'Window(Home).Property(aeon.mi.%s)'
ON = 'Skin.HasSetting(aeon.mi.sidecar) + String.IsEqual(Window(Home).Property(aeon.mi.path),ListItem.FileNameAndPath)'


def main():
    t = io.open(P, encoding='utf-8').read()
    if MARK in t:
        print('already')
        return
    # chips: clone the last chip pair (channels, Aeon_LVCh) for the source and the edition
    pair = re.findall(r'\t*<control type="button"><width min="46" max="520">auto</width><height>34</height><label>\$VAR\[Aeon_LVCh\]</label>.*?</control>\n', t)
    assert len(pair) == 2, len(pair)
    end = t.index(pair[1]) + len(pair[1])
    add = '\t\t\t\t\t\t\t<!-- %s: the sidecar\'s source and edition -->\n' % MARK
    for key in ('source', 'edition'):
        for chip in pair:
            c = chip.replace('<label>$VAR[Aeon_LVCh]</label>', '<label>[UPPERCASE]$INFO[%s][/UPPERCASE]</label>' % (H % key))
            c = re.sub(r'<visible>(\$EXP\[Aeon_VGlass\]|!\$EXP\[Aeon_VGlass\])[^<]*</visible>',
                       lambda m: '<visible>%s + %s + !String.IsEmpty(%s)</visible>' % (m.group(1), ON, H % key), c)
            assert ON in c, c[:200]
            add += c
    t = t[:end] + add + t[end:]
    # the Ending at card: three lines under its own
    old = ('\t\t\t\t\t<info>ListItem.Property(WatchedEpisodePercent)</info>\n\t\t\t\t\t<visible>$EXP[VidView_IsTVType]</visible>\n'
           '\t\t\t\t</control>\n\t\t\t</control>')
    assert t.count(old) == 1, t.count(old)
    L1 = '$INFO[%s]$INFO[%s, · ]$INFO[%s, · ]$INFO[%s, · ]$INFO[%s, · ]' % (H % 'source', H % 'edition', H % '3d', H % 'bitrate', H % 'size')
    L2 = ('$INFO[%s]$INFO[%s, · $LOCALIZE[292] ]$INFO[%s, · $ADDON[skin.aeon.fuse 32617] ]$INFO[%s, · $LOCALIZE[287] ]$INFO[%s, ]$INFO[%s, · $ADDON[skin.aeon.fuse 32618] ]'
          % (H % 'audio', H % 'audio.count', H % 'commentary', H % 'subs.count', H % 'sdh', H % 'chapters'))
    L3 = '$INFO[%s]$INFO[%s, · ]' % (H % 'video', H % 'hdr')
    lines = ''
    for i, (lab, font, col) in enumerate(((L1, 'lb_small_20_bold', '$VAR[AG_Ink]'), (L2, 'lb_small_20', '$VAR[AG_Ink2]'), (L3, 'lb_small_20', '$VAR[AG_Ink3]'))):
        lines += ('\t\t\t\t<control type="label"><left>36</left><top>%d</top><width>552</width><height>30</height><aligny>center</aligny>'
                  '<font>%s</font><textcolor>%s</textcolor><scroll>false</scroll><label>%s</label><visible>%s + !String.IsEmpty(%s)</visible></control>\n'
                  % (186 + 32 * i, font, col, lab, ON, H % 'from'))
    t = t.replace(old, old[:-len('\t\t\t</control>')] + '\t\t\t\t<!-- %s: what the mediainfo sidecar says -->\n' % MARK + lines + '\t\t\t</control>', 1)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(P)
    print('ok')


if __name__ == '__main__':
    main()
