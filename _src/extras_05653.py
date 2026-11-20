# -*- coding: utf-8 -*-
"""0.56.53 Aeon / Aeon Glass List view (Aeon_510_ViewAeon, Includes_Aeon_Video.xml): the sidecar's subtitles, chapters
and commentary move from the bottom media line to the top info panel (user, 2026-11-19: "Can you move the 8 SUBTITLES
• 28 CHAPTERS • COMMENTARY to the top info panel instead?"; the bottom line ran out: "... 28 CHAPTERS • C").
- Aeon_TxSideT (Includes_Aeon_Views2.xml): Aeon_TxSide without them (codec, container, bitrate, source, size, 3D);
  the List view's bar (Aeon_V_Bar510) shows that. The other Aeon views keep the whole line.
- The top panel: while the film in focus has any of the three, its plot is 3 lines (was 4.5) and a line under it
  reads "8 SUBTITLES  •  28 CHAPTERS  •  COMMENTARY" (each switched by its Media info chips switch).
Run after sidetext_05653.py. Repeatable."""
import io
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
V = os.path.join(D, 'Includes_Aeon_Views2.xml')
VID = os.path.join(D, 'Includes_Aeon_Video.xml')
MARK = '<!-- 0.56.53 extras in the top panel -->'
MI = 'Window(Home).Property(aeon.mi.%s)'
GATE = ('Skin.HasSetting(aeon.mi.sidecar) + String.IsEqual(%s,Container(510).ListItem.FileNameAndPath)' % (MI % 'path'))
S = 'Skin.HasSetting(aeon.chip.subs) + !String.IsEmpty(%s)' % (MI % 'subs.count')
C = 'Skin.HasSetting(aeon.chip.chapters) + !String.IsEmpty(%s)' % (MI % 'chapters')
M = 'Skin.HasSetting(aeon.chip.commentary) + !String.IsEmpty(%s)' % (MI % 'commentary')
ANY = '%s + [[%s] | [%s] | [%s]]' % (GATE, S, C, M)


def lab(text, cond, colour='ffffffff'):
    return ('<control type="label"><width min="10" max="600">auto</width><height>30</height><aligny>center</aligny>'
            '<font>lb_small_20_bold</font><textcolor>%s</textcolor><label>%s</label><visible>%s</visible></control>'
            % (colour, text, cond))


def main():
    s = io.open(V, encoding='utf-8').read()
    if '<variable name="Aeon_TxSideT">' not in s:
        i = s.index('\t<variable name="Aeon_TxSide">')
        line = s[i:s.index('\n', i) + 1]
        t = line.replace('name="Aeon_TxSide"', 'name="Aeon_TxSideT"')
        for part in ('subs', 'chapters', 'commentary'):
            t = t.replace('$VAR[Aeon_TxSide_%s]' % part, '')
        s = s[:i] + t + s[i:]
        a = s.index('<include name="Aeon_V_Bar510">')
        b = s.index('<include name=', a + 10)
        seg = s[a:b]
        n = seg.count('$VAR[Aeon_TxMedia]$VAR[Aeon_TxSide]')
        s = s[:a] + seg.replace('$VAR[Aeon_TxMedia]$VAR[Aeon_TxSide]', '$VAR[Aeon_TxMedia]$VAR[Aeon_TxSideT]') + s[b:]
        io.open(V, 'w', encoding='utf-8', newline='\n').write(s)
        print('bar: %d media lines without the extras' % n)
    t = io.open(VID, encoding='utf-8').read()
    if MARK in t:
        print('top panel: already there')
        return
    old = ('<control type="textbox"><left>0</left><top>42</top><width>1010</width><height>108</height><font>lb_small_20</font>'
           '<textcolor>c7ffffff</textcolor><label>$INFO[Container(510).ListItem.Plot]</label>'
           '<autoscroll delay="8000" time="3000" repeat="10000">true</autoscroll></control>')
    assert t.count(old) == 1, t.count(old)
    dot = '  •  '
    line = ('<control type="grouplist"><left>0</left><top>124</top><width>1010</width><height>30</height>'
            '<orientation>horizontal</orientation><itemgap>0</itemgap><visible>%s</visible>%s%s%s%s%s</control>'
            % (ANY,
               lab('[UPPERCASE]$INFO[%s,, $LOCALIZE[287]][/UPPERCASE]' % (MI % 'subs.count'), S),
               lab(dot, '[%s] + [[%s] | [%s]]' % (S, C, M), '99ffffff'),
               lab('[UPPERCASE]$INFO[%s,, $ADDON[skin.aeon.fuse 32661]][/UPPERCASE]' % (MI % 'chapters'), C),
               lab(dot, '[%s] + [%s]' % (C, M), '99ffffff'),
               lab('[UPPERCASE]$ADDON[skin.aeon.fuse 32662][/UPPERCASE]', M)))
    new = (old.replace('</control>', '<visible>![%s]</visible></control>' % ANY)
           + MARK + old.replace('<height>108</height>', '<height>78</height>').replace('</control>', '<visible>%s</visible></control>' % ANY)
           + line)
    t = t.replace(old, new)
    io.open(VID, 'w', encoding='utf-8', newline='\n').write(t)
    print('top panel: extras line added')


if __name__ == '__main__':
    main()
