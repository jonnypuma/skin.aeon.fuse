# -*- coding: utf-8 -*-
"""0.56.53 Kodi's file browser (folder / file picker) in Fused Glass style (the standard-window pass, user
2026-11-20). FB_Classic (the centred dialog, as it was) and FGS_FileBrowser: the style's dialog ground and header (the
heading 411, as Select), then the page spec of Add-on settings:
- frame 120-1820 x 108-960; title band: the path (412, Kodi writes it) over the list, the art type when picking art;
- the files (450) as 70 rows 121-1499 (the File manager's rows) with the square bar 60 in the gutter 1500-1520; Right
  through the bar to the buttons, Left back; Up / Down wrap;
- OK / Cancel / New folder / Mirror image (413-416 in 9000) as 70 rows in the right column 1521-1820, the style's bar
  with the dark fill.
Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgsfilemanager_05653 as fm  # noqa: E402

P = os.path.join(fm.D, 'FileBrowser.xml')
RC = 1500


def page():
    L, R, T, B, BAND, GUT = fm.L, fm.R, fm.T, fm.B, fm.BAND, fm.GUT
    out = ['<!-- 0.56.53 fgsfilebrowser: the dialog ground and header, the page spec -->',
           '<include>FGS_DlgBack</include>', '<include>Aeon_ClockBox</include>',
           '<control type="label" id="411"><visible>false</visible></control>',
           '<include content="FGS_DlgHeader"><param name="label" value="$INFO[Control.GetLabel(411)]"/></include>']
    out += [fm.rule(L, T, R - L + 1, 1), fm.rule(L, B, R - L + 1, 1), fm.rule(L + 1, BAND, R - L - 1, 1)]
    out += [fm.rule(x, T, 1, B - T) for x in (L, RC, RC + GUT, R)]
    head = ('<control type="label" id="412"><left>%d</left><top>120</top><width>%d</width><height>60</height><aligny>center</aligny>'
            '<font>st_ui_24_semibold</font><textcolor>$VAR[AG_Ink]</textcolor></control>')
    nav = ('<onleft>9000</onleft><onright condition="Container(450).HasNext | Container(450).HasPrevious">60</onright>'
           '<onright condition="!Container(450).HasNext + !Container(450).HasPrevious">9000</onright>')
    out.append(fm.pane(L + 1, RC, '450', '60', head, fm.COUNT_POS % ('450', '450'), nav, '<onleft>450</onleft><onright>9000</onright>'))
    btn = ('<control type="button" id="%s"><width>%d</width><height>70</height><font>uc_st_ui_24_semibold</font>'
           '<textcolor>ccffffff</textcolor><focusedcolor>$VAR[FGS_Aeon_OnBarInk]</focusedcolor><disabledcolor>44ffffff</disabledcolor>'
           '<textoffsetx>24</textoffsetx><aligny>center</aligny><pulseonselect>false</pulseonselect>'
           '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>'
           '<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>'
           '<label>$LOCALIZE[%s]</label>%s</control>')
    w = R - RC - GUT - 1
    buttons = (btn % ('413', w, '186', '') + btn % ('414', w, '222', '')
               + btn % ('415', w, '119', '<visible>Control.IsEnabled(415)</visible>')
               + btn % ('416', w, '749', '<visible>Control.IsEnabled(416)</visible>'))
    out.append('<control type="grouplist" id="9000"><left>%d</left><top>%d</top><width>%d</width><height>280</height>'
               '<orientation>vertical</orientation><itemgap>0</itemgap><onleft>450</onleft><onright>450</onright>'
               '<onup>9000</onup><ondown>9000</ondown>%s</control>' % (RC + GUT + 1, BAND, w, buttons))
    out.append('<control type="label"><left>%d</left><top>975</top><width>%d</width><height>40</height><font>st_small_20</font>'
               '<textcolor>99ffffff</textcolor><label>[CAPITALIZE]$INFO[Window(Home).Property(aeon.arttype)][/CAPITALIZE]</label>'
               '<visible>!String.IsEmpty(Window(Home).Property(aeon.arttype))</visible></control>' % (L + 24, 900))
    return '\n\t\t'.join(out)


def main():
    s = io.open(P, encoding='utf-8').read()
    t = io.open(fm.FUSED, encoding='utf-8').read()
    a = s.index('<controls>') + len('<controls>')
    e = s.rindex('</controls>')
    if '<include name="FB_Classic">' in t:
        i = t.index('<include name="FB_Classic">')
        classic = t[i + len('<include name="FB_Classic">'):t.index('</include>\n\t<!-- end FB_Classic -->', i)].strip('\n\t')
    else:
        classic = s[a:e].strip('\n\t')
    t = fm.put(t, 'FB_Classic', classic)
    t = fm.put(t, 'FGS_FileBrowser', page())
    io.open(fm.FUSED, 'w', encoding='utf-8', newline='\n').write(t)
    s = (s[:a] + '\n\t\t<include condition="!$EXP[FGS]">FB_Classic</include>'
         '\n\t\t<include condition="$EXP[FGS]">FGS_FileBrowser</include><!-- 0.56.53 fgsfilebrowser -->\n\t' + s[e:])
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
    print('file browser: classic + style layouts')


if __name__ == '__main__':
    main()
