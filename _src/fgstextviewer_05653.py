# -*- coding: utf-8 -*-
"""0.56.53 Kodi's text viewer (changelogs, logs, long texts) in Fused Glass style (the standard-window pass, user
2026-11-20). TV_Classic (the centred dialog, as it was) and FGS_TextViewer: the style's dialog ground and header (the
heading 1), then the page spec:
- frame 120-1820 x 108-960; title band: the page position at the right;
- the text (5) 24 px inside the frame, 191-960 (21 lines), the square bar 3000 in the gutter 1800-1820;
- the focus holder 1000: Up / Down page, OK closes, Right reaches the bar (Left back);
- the hint (OK closes) under the frame.
Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgsfilemanager_05653 as fm  # noqa: E402

P = os.path.join(fm.D, 'DialogTextViewer.xml')


def page():
    L, R, T, B, BAND, GUT = fm.L, fm.R, fm.T, fm.B, fm.BAND, fm.GUT
    out = ['<!-- 0.56.53 fgstextviewer -->', '<include>FGS_DlgBack</include>', '<include>Aeon_ClockBox</include>',
           '<control type="label" id="1"><visible>false</visible></control>',
           '<include content="FGS_DlgHeader"><param name="label" value="$INFO[Control.GetLabel(1)]"/></include>']
    out += [fm.rule(L, T, R - L + 1, 1), fm.rule(L, B, R - L + 1, 1), fm.rule(L + 1, BAND, R - L - 1, 1)]
    out += [fm.rule(x, T, 1, B - T) for x in (L, R - GUT, R)]
    out.append('<control type="label"><left>%d</left><top>120</top><width>400</width><height>60</height><align>right</align><aligny>center</aligny>'
               '<font>st_small_20</font><textcolor>80ffffff</textcolor><label>$INFO[Container(5).CurrentPage]$INFO[Container(5).NumPages,  /  ,]</label><visible>Integer.IsGreater(Container(5).NumPages,0)</visible></control>'
               % (R - GUT - 24 - 400))
    out.append('<control type="textbox" id="5"><left>%d</left><top>%d</top><width>%d</width><height>740</height>'
               '<font>body_24</font><monofont>Mono26</monofont><textcolor>ddffffff</textcolor><pagecontrol>3000</pagecontrol></control>'
               % (L + 25, BAND + 16, R - GUT - L - 49))
    out.append('<control type="scrollbar" id="3000"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>'
               '<include>FGS_SBTex</include><textureslidernib /><textureslidernibfocus /><orientation>vertical</orientation>'
               '<showonepage>false</showonepage><onup>3000</onup><ondown>3000</ondown><onleft>1000</onleft><onright>1000</onright></control>'
               % (R - GUT + 1, BAND + 1, GUT - 1, B - BAND - 1))
    out.append('<control type="label"><left>%d</left><top>975</top><width>900</width><height>40</height><font>st_small_20</font>'
               '<textcolor>80ffffff</textcolor><label>$LOCALIZE[31014]</label></control>' % (L + 24))
    out.append('<control type="button" id="1000"><description>focus holder: up/down page, OK closes, Right the bar</description>'
               '<include>AG_Hidden</include><onclick>Action(Close)</onclick><onup>PageUp(3000)</onup><ondown>PageDown(3000)</ondown>'
               '<onleft>noop</onleft><onright>3000</onright></control>')
    return '\n\t\t'.join(out)


def main():
    s = io.open(P, encoding='utf-8').read()
    t = io.open(fm.FUSED, encoding='utf-8').read()
    a = s.index('<controls>') + len('<controls>')
    e = s.rindex('</controls>')
    if '<include name="TV_Classic">' in t:
        i = t.index('<include name="TV_Classic">')
        classic = t[i + len('<include name="TV_Classic">'):t.index('</include>\n\t<!-- end TV_Classic -->', i)].strip('\n\t')
    else:
        classic = s[a:e].strip('\n\t')
    t = fm.put(t, 'TV_Classic', classic)
    t = fm.put(t, 'FGS_TextViewer', page())
    io.open(fm.FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    s = (s[:a] + '\n\t\t<include condition="!$EXP[FGS]">TV_Classic</include>'
         '\n\t\t<include condition="$EXP[FGS]">FGS_TextViewer</include><!-- 0.56.53 fgstextviewer -->\n\t' + s[e:])
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('text viewer: classic + style layouts')


if __name__ == '__main__':
    main()
