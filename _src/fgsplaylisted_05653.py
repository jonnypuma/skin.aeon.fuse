# -*- coding: utf-8 -*-
"""0.56.53 the music playlist editor in Fused Glass style (the standard-window pass, user 2026-11-20; box shot: pill
buttons, the white bar, thin bars of the other looks). Built with the File manager's two panes
(fgsfilemanager_05653.py): MPE_Classic (as it was) and FGS_PlaylistEditor:
- frame 120-1820 x 108-960, title band: LIBRARY + Kodi's file count (12) | PLAYLIST + its count (101);
- Open / Save / Clear (6, 7, 8 in menucontrol 9000) as a strip of cells under the band (191-261, the sub-nav look);
- the library (50) and the playlist (100) as 70 rows from 261 with the square bars 60 / 61 in their gutters;
  Up from either list to the strip, Down from the strip to the library; the empty playlist's note in its pane.
Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgsfilemanager_05653 as fm  # noqa: E402

P = os.path.join(fm.D, 'MyMusicPlaylistEditor.xml')
TOP = fm.BAND + fm.ROW


def page():
    L, R, T, B, BAND, GUT, MID = fm.L, fm.R, fm.T, fm.B, fm.BAND, fm.GUT, fm.MID
    out = ['<!-- 0.56.53 fgsplaylisted: the Skin settings page spec, two panes under a strip -->']
    out += [fm.rule(L, T, R - L + 1, 1), fm.rule(L, B, R - L + 1, 1), fm.rule(L + 1, BAND, R - L - 1, 1), fm.rule(L + 1, TOP, R - L - 1, 1)]
    out += [fm.rule(x, T, 1, B - T) for x in (L, R)] + [fm.rule(x, TOP, 1, B - TOP) for x in (MID, MID + GUT, R - GUT)]
    out.append(fm.rule(MID, T, 1, BAND - T))
    btn = ('<include content="AG_SubNavButton"><param name="fgs" value="true"/><param name="id" value="%s"/>'
           '<param name="label" value="$LOCALIZE[%s]"/></include>')
    out.append('<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>70</height>'
               '<orientation>horizontal</orientation><itemgap>0</itemgap><onup>noop</onup><ondown>50</ondown>'
               '<onleft>noop</onleft><onright>noop</onright><onback>50</onback>%s</control>'
               % (L + 1, BAND + 1, R - L - 1, ''.join(btn % (i, s) for i, s in (('6', '502'), ('7', '190'), ('8', '192')))))
    lnav = ('<onleft>noop</onleft><onright condition="Integer.IsGreater(Container(100).NumItems,0)">100</onright>'
            '<onright condition="!Integer.IsGreater(Container(100).NumItems,0)">noop</onright>')
    lnav = lnav.replace('<onleft>', '<onup>9000</onup><onleft>', 1)
    rnav = '<onup>9000</onup><onleft>50</onleft><onright>61</onright>'
    a = fm.pane(L + 1, MID, '50', '60', fm.HEAD_TXT % '$LOCALIZE[31204]', fm.COUNT_ID % '12', lnav,
                '<onleft>50</onleft><onright>100</onright>', TOP, '<viewtype label="535">list</viewtype>')
    b = fm.pane(MID + GUT + 1, R - GUT, '100', '61', fm.HEAD_TXT % '$LOCALIZE[31249]', fm.COUNT_ID % '101', rnav,
                '<onleft>100</onleft><onright>noop</onright>', TOP)
    # pane() puts Up / Down as wraps; Up goes to the strip here
    a = a.replace('<onup>50</onup>', '', 1)
    b = b.replace('<onup>100</onup>', '', 1)
    out += [a, b]
    out.append('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>70</height><aligny>center</aligny>'
               '<font>st_ui_24_semibold</font><textcolor>66ffffff</textcolor><label>$LOCALIZE[31250]</label>'
               '<visible>Integer.IsEqual(Container(100).NumItems,0)</visible></control>' % (MID + GUT + 25, TOP, R - GUT - MID - GUT - 48))
    return '\n\t\t'.join(out)


def main():
    s = io.open(P, encoding='utf-8').read()
    t = io.open(fm.FUSED, encoding='utf-8').read()
    a = s.index('</include>', s.index('<include content="AG_TopBar">')) + len('</include>')
    e = s.rindex('</controls>')
    if '<include name="MPE_Classic">' in t:
        i = t.index('<include name="MPE_Classic">')
        classic = t[i + len('<include name="MPE_Classic">'):t.index('</include>\n\t<!-- end MPE_Classic -->', i)].strip('\n\t')
    else:
        classic = s[a:e].strip('\n\t')
    t = fm.put(t, 'MPE_Classic', classic)
    t = fm.put(t, 'FGS_PlaylistEditor', page())
    io.open(fm.FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    s = (s[:a] + '\n\t\t<include condition="!$EXP[FGS]">MPE_Classic</include>'
         '\n\t\t<include condition="$EXP[FGS]">FGS_PlaylistEditor</include><!-- 0.56.53 fgsplaylisted -->\n\t' + s[e:])
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('playlist editor: classic + style layouts')


if __name__ == '__main__':
    main()
