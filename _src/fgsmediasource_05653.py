# -*- coding: utf-8 -*-
"""0.56.53 Kodi's Add / Edit media source dialog in Fused Glass style (the standard-window pass, user 2026-11-20).
MS_Classic (the centred dialog, as it was) and FGS_MediaSource: the style's dialog ground and header (heading 2), then
the page spec on the 70 grid:
- the paths (10) 121-1499, four rows from 191 (the File manager's rows), the square bar 60 in the gutter 1500-1520;
  Browse / Add path / Remove path (11, 13, 14 in 9000) as rows of the right column 1521-1820; the band says what the
  paths are for (Kodi's line 1021);
- a heading row "Name" (1022), the name (edit 12) as a full-width row, the style's bar with the dark fill;
- OK / Cancel (18, 19 in 9001) as a strip of cells on the frame's last row (890-960).
Up / Down: paths > name > OK / Cancel > paths. Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgsfilemanager_05653 as fm  # noqa: E402

P = os.path.join(fm.D, 'DialogMediaSource.xml')
RC = 1500
LIST_B = fm.BAND + 4 * fm.ROW        # 471
NAME_T = LIST_B + fm.ROW             # 541: the name row
BTN_T = fm.B - fm.ROW                # 890: OK / Cancel


def page():
    L, R, T, B, BAND, GUT = fm.L, fm.R, fm.T, fm.B, fm.BAND, fm.GUT
    out = ['<!-- 0.56.53 fgsmediasource -->', '<include>FGS_DlgBack</include>', '<include>Aeon_ClockBox</include>',
           '<control type="label" id="2"><visible>false</visible></control>',
           '<include content="FGS_DlgHeader"><param name="label" value="$INFO[Control.GetLabel(2)]"/></include>']
    out += [fm.rule(L, T, R - L + 1, 1), fm.rule(L, B, R - L + 1, 1), fm.rule(L + 1, BAND, R - L - 1, 1)]
    out += [fm.rule(x, T, 1, B - T) for x in (L, R)] + [fm.rule(x, BAND, 1, LIST_B - BAND) for x in (RC, RC + GUT)]
    out += [fm.rule(L + 1, LIST_B, R - L - 1, 1), fm.rule(L + 1, NAME_T + fm.ROW, R - L - 1, 1), fm.rule(L + 1, BTN_T, R - L - 1, 1)]
    out.append('<control type="label"><left>%d</left><top>120</top><width>%d</width><height>60</height><aligny>center</aligny>'
               '<font>st_ui_24_semibold</font><textcolor>$VAR[AG_Ink]</textcolor><label>$LOCALIZE[1021]</label></control>' % (L + 24, R - L - 48))
    nav = '<onleft>9000</onleft><onright condition="Container(10).HasNext | Container(10).HasPrevious">60</onright><onright condition="!Container(10).HasNext + !Container(10).HasPrevious">9000</onright>'
    pane = fm.pane(L + 1, RC, '10', '60', '', '', nav, '<onleft>10</onleft><onright>9000</onright>', BAND)
    # four rows tall, Up to OK / Cancel, Down to the name
    pane = pane.replace('<height>%d</height>' % (B - BAND - 1), '<height>%d</height>' % (LIST_B - BAND), 2)
    pane = pane.replace('<onup>10</onup><ondown>10</ondown>', '<onup>9001</onup><ondown>12</ondown>', 1)
    out.append(pane)
    btn = ('<control type="button" id="%s"><width>%d</width><height>70</height><font>uc_st_ui_24_semibold</font>'
           '<textcolor>ccffffff</textcolor><focusedcolor>$VAR[FGS_Aeon_OnBarInk]</focusedcolor><disabledcolor>44ffffff</disabledcolor>'
           '<textoffsetx>24</textoffsetx><aligny>center</aligny><pulseonselect>false</pulseonselect>'
           '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>'
           '<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus><label>$LOCALIZE[%s]</label></control>')
    w = R - RC - GUT - 1
    out.append('<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>210</height>'
               '<orientation>vertical</orientation><itemgap>0</itemgap><onleft>10</onleft><onright>10</onright><onup>9001</onup><ondown>12</ondown>%s</control>'
               % (RC + GUT + 1, BAND, w, btn % ('11', w, '1024') + btn % ('13', w, '15019') + btn % ('14', w, '1210')))
    out.append('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>70</height><aligny>center</aligny>'
               '<font>uc_st_ui_24_semibold</font><textcolor>99ffffff</textcolor><label>$LOCALIZE[1022]</label></control>' % (L + 24, LIST_B, 600))
    out.append('<control type="edit" id="12"><left>%d</left><top>%d</top><width>%d</width><height>70</height>'
               '<font>st_ui_24_semibold</font><textcolor>ddffffff</textcolor><focusedcolor>ffffffff</focusedcolor><textoffsetx>24</textoffsetx><aligny>center</aligny>'
               '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>'
               '<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>'
               '<onup>10</onup><ondown>9001</ondown><onleft>noop</onleft><onright>noop</onright></control>' % (L + 1, NAME_T, R - L - 1))
    cell = ('<include content="AG_SubNavButton"><param name="fgs" value="true"/><param name="id" value="%s"/>'
            '<param name="label" value="$LOCALIZE[%s]"/></include>')
    out.append('<control type="grouplist" id="9001"><left>%d</left><top>%d</top><width>%d</width><height>70</height>'
               '<orientation>horizontal</orientation><itemgap>0</itemgap><onup>12</onup><ondown>10</ondown>%s</control>'
               % (L + 1, BTN_T + 1, R - L - 1, cell % ('18', '186') + cell % ('19', '222')))
    return '\n\t\t'.join(out)


def main():
    s = io.open(P, encoding='utf-8').read()
    t = io.open(fm.FUSED, encoding='utf-8').read()
    a = s.index('<controls>') + len('<controls>')
    e = s.rindex('</controls>')
    if '<include name="MS_Classic">' in t:
        i = t.index('<include name="MS_Classic">')
        classic = t[i + len('<include name="MS_Classic">'):t.index('</include>\n\t<!-- end MS_Classic -->', i)].strip('\n\t')
    else:
        classic = s[a:e].strip('\n\t')
    t = fm.put(t, 'MS_Classic', classic)
    t = fm.put(t, 'FGS_MediaSource', page())
    io.open(fm.FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    s = (s[:a] + '\n\t\t<include condition="!$EXP[FGS]">MS_Classic</include>'
         '\n\t\t<include condition="$EXP[FGS]">FGS_MediaSource</include><!-- 0.56.53 fgsmediasource -->\n\t' + s[e:])
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('media source: classic + style layouts')


if __name__ == '__main__':
    main()
