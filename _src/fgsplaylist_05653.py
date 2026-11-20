# -*- coding: utf-8 -*-
"""0.56.53 the play queue (MyPlaylist: music and video playlists) in Fused Glass style (the standard-window pass,
user 2026-11-20). PL_Classic (as it was) and FGS_Playlist, the Skin settings page spec:
- frame 120-1820 x 108-960; title band: the queue's title | its count and total time;
- Shuffle / Repeat / Save / Clear (20, 26, 21, 22 in menucontrol 9000) as a strip of cells under the band;
- the queue (50) as 70 rows 121-1499 from 261 with the square bar 60 in the gutter 1500-1520 (the File manager's rows:
  the art, the name, label2 at the right), Up to the strip, Down wraps;
- the right column 1521-1820: the focused item's art (square) and its name, as the preview column of Skin settings;
- the empty note in the list, the now-playing bar as before.
Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgsfilemanager_05653 as fm  # noqa: E402

P = os.path.join(fm.D, 'MyPlaylist.xml')
TOP = fm.BAND + fm.ROW
RC = 1500


def page():
    L, R, T, B, BAND, GUT = fm.L, fm.R, fm.T, fm.B, fm.BAND, fm.GUT
    out = ['<!-- 0.56.53 fgsplaylist: the Skin settings page spec -->']
    out += [fm.rule(L, T, R - L + 1, 1), fm.rule(L, B, R - L + 1, 1), fm.rule(L + 1, BAND, R - L - 1, 1), fm.rule(L + 1, TOP, R - L - 1, 1)]
    out += [fm.rule(x, T, 1, B - T) for x in (L, R)] + [fm.rule(x, TOP, 1, B - TOP) for x in (RC, RC + GUT)]
    out.append('<control type="label"><left>%d</left><top>120</top><width>%d</width><height>60</height><aligny>center</aligny>'
               '<font>st_ui_30_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>[UPPERCASE]$VAR[Music_QueueTitle][/UPPERCASE]</label></control>'
               % (L + 24, 900))
    out.append('<control type="label"><left>%d</left><top>120</top><width>600</width><height>60</height><align>right</align><aligny>center</aligny>'
               '<font>st_small_20</font><textcolor>80ffffff</textcolor><label>$VAR[PL_Container_NumItems_Item]$INFO[Container.TotalTime,  ·  ,]</label></control>'
               % (R - 24 - 600))
    btn = ('<include content="AG_SubNavButton"><param name="fgs" value="true"/><param name="id" value="%s"/>'
           '<param name="label" value="%s"/>%s</include>')
    vis = '<param name="visible" value="Integer.IsGreater(Container.NumItems,0)"/>'
    out.append('<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>70</height>'
               '<orientation>horizontal</orientation><itemgap>0</itemgap><onup>noop</onup><ondown>50</ondown>'
               '<onleft>noop</onleft><onright>noop</onright><onback>50</onback>%s</control>'
               % (L + 1, BAND + 1, R - L - 1, btn % ('20', '$VAR[Music_QueueShuffleLabel]', '') + btn % ('26', '$LOCALIZE[595]', '')
                  + btn % ('21', '$LOCALIZE[190]', vis) + btn % ('22', '$LOCALIZE[192]', vis)))
    a = fm.pane(L + 1, RC, '50', '60', '', '', '<onup>9000</onup><onleft>noop</onleft><onright>60</onright>',
                '<onleft>50</onleft><onright>50</onright>', TOP, '<viewtype label="535">list</viewtype>')
    a = a.replace('<onup>50</onup>', '', 1)
    out.append('<control type="group"><visible>Control.IsVisible(50)</visible>%s</control>' % a)
    w = R - RC - GUT - 1
    out.append('<control type="group"><left>%d</left><top>%d</top><visible>Integer.IsGreater(Container(50).NumItems,0)</visible>'
               '<control type="image"><left>24</left><top>24</top><width>%d</width><height>%d</height><aspectratio>keep</aspectratio>'
               '<texture background="true">$INFO[Container(50).ListItem.Icon]</texture></control>'
               '<control type="label"><left>24</left><top>%d</top><width>%d</width><height>34</height><font>st_ui_24_semibold</font>'
               '<textcolor>ffffffff</textcolor><label>$INFO[Container(50).ListItem.Title]</label></control>'
               '<control type="label"><left>24</left><top>%d</top><width>%d</width><height>30</height><font>st_small_20</font>'
               '<textcolor>99ffffff</textcolor><label>$INFO[Container(50).ListItem.Artist]$INFO[Container(50).ListItem.Album, · ,]</label></control>'
               '</control>' % (RC + GUT + 1, TOP, w - 48, w - 48, 24 + w - 48 + 16, w - 48, 24 + w - 48 + 54, w - 48))
    out.append('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>70</height><aligny>center</aligny>'
               '<font>st_ui_24_semibold</font><textcolor>66ffffff</textcolor><label>$LOCALIZE[31251]</label>'
               '<visible>Integer.IsEqual(Container.NumItems,0) + !Container.IsUpdating</visible></control>' % (L + 25, TOP, RC - L - 48))
    out.append('<include>Music_NowPlayingBar</include>')
    return '\n\t\t'.join(out)


def main():
    s = io.open(P, encoding='utf-8').read()
    t = io.open(fm.FUSED, encoding='utf-8').read()
    a = s.index('</include>', s.index('<include content="AG_TopBar">')) + len('</include>')
    e = s.rindex('</controls>')
    if '<include name="PL_Classic">' in t:
        i = t.index('<include name="PL_Classic">')
        classic = t[i + len('<include name="PL_Classic">'):t.index('</include>\n\t<!-- end PL_Classic -->', i)].strip('\n\t')
    else:
        classic = s[a:e].strip('\n\t')
    t = fm.put(t, 'PL_Classic', classic)
    t = fm.put(t, 'FGS_Playlist', page())
    io.open(fm.FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    s = (s[:a] + '\n\t\t<include condition="!$EXP[FGS]">PL_Classic</include>'
         '\n\t\t<include condition="$EXP[FGS]">FGS_Playlist</include><!-- 0.56.53 fgsplaylist -->\n\t' + s[e:])
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('playlist: classic + style layouts')


if __name__ == '__main__':
    main()
