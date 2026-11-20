# -*- coding: utf-8 -*-
"""0.56.53 Game controllers (DialogGameControllers, gamecontrollers variant) in the Fused Glass style (canvas round 2
GameControllers2, "so good. build that", note: "reuse the original gamepad image instead? it just looks better"):
Kodi's own controller picture (gamecontrol 31) large in the middle, the controllers (grouplist 3, rows cloned from
button 10) at the left with bar 62 in the gutter, the features to map (grouplist 5: buttons from 7, group titles 8,
separators 9) at the right with bar 61, Kodi's buttons (9001: 18 OK, 19 reset, 20 get more, 22, 17 help, 21) as one row
of cells under the picture, the controller's description (32) under the frame. The ports and players variants keep
today's look. Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

NAME = 'GameCtl'


def page():
    nav = '<onup>5</onup><ondown>noop</ondown>'
    btns = ((18, '$LOCALIZE[186]'), (19, '$LOCALIZE[13007]'), (20, '$LOCALIZE[21452]'), (22, '$LOCALIZE[35021]'), (17, '$LOCALIZE[10043]'), (21, '$LOCALIZE[35019]'))
    row = ''.join(fw.cell(str(i), 219 if k == 5 else 220, lab, nav) for k, (i, lab) in enumerate(btns))
    return (
        '<include name="GameCtl_PageFGS">'
        '<include content="FGS_DlgBack"/>'
                '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[35050][/UPPERCASE]</label></control>'
        '<control type="label" id="2"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[35058]</label></control>'
        '</control><include>Aeon_ClockBox</include>'
        + fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + fw.line(121, 191, 1699) +
        ''.join(fw.line(x, 108, 1, 852) for x in (120, 480, 500, 1820)) + ''.join(fw.line(x, 108, 1, 782) for x in (1240, 1800)) +
        fw.label(144, 120, 330, 60, '[UPPERCASE]$LOCALIZE[35050][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        fw.label(1264, 120, 530, 60, '[UPPERCASE]$LOCALIZE[35059][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        '<control type="grouplist" id="3"><left>121</left><top>191</top><width>359</width><height>770</height><orientation>vertical</orientation><itemgap>0</itemgap>'
        '<onleft>noop</onleft><onright>62</onright><onup>3</onup><ondown>3</ondown><pagecontrol>62</pagecontrol></control>'
        + fw.gutter_bar('62', 481, 192, 768, '3', '5') +
        '<control type="button" id="10"><left>121</left><top>191</top><width>359</width><include>FGS_DlgRow</include></control>'
        # the original pad picture, large
        '<control type="gamecontroller" id="31"><left>540</left><top>210</top><width>680</width><height>660</height></control>'
        '<control type="grouplist" id="5"><left>1241</left><top>191</top><width>559</width><height>700</height><orientation>vertical</orientation><itemgap>0</itemgap>'
        '<onleft>3</onleft><onright>61</onright><onup>5</onup><ondown>9001</ondown><pagecontrol>61</pagecontrol></control>'
        + fw.gutter_bar('61', 1801, 192, 698, '5', 'noop') +
        '<control type="button" id="7"><left>1241</left><top>191</top><width>559</width><include>FGS_DlgRow</include></control>'
        '<control type="label" id="8"><left>1265</left><top>191</top><width>535</width><height>50</height><aligny>center</aligny><font>st_cap_16</font><textcolor>80ffffff</textcolor></control>'
        '<control type="image" id="9"><left>1241</left><top>191</top><width>559</width><height>1</height><texture colordiffuse="%s">common/white.png</texture></control>' % fw.LINE
        + fw.line(500, 890, 1320) +
        '<control type="grouplist" id="9001"><left>501</left><top>891</top><width>1319</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onleft>3</onleft><onright>5</onright><onup>5</onup><ondown>noop</ondown>%s</control>' % row +
        '<control type="textbox" id="32"><left>144</left><top>972</top><width>1676</width><height>60</height><font>st_small_20</font><textcolor>8cffffff</textcolor></control>'
        '</include>')


def main():
    fw.ensure_file()
    p = os.path.join(fw.D, 'DialogGameControllers.xml')
    w = io.open(p, encoding='utf-8').read()
    old = '<include condition="Window.IsDialogTopMost(gamecontrollers)">Misc_GameControllers</include>'
    if old in w:
        w = w.replace(old, '<include condition="Window.IsDialogTopMost(gamecontrollers) + !$EXP[FGS]">Misc_GameControllers</include>\n\t\t'
                           '<include condition="Window.IsDialogTopMost(gamecontrollers) + $EXP[FGS]">GameCtl_PageFGS</include>')
        io.open(p, 'w', encoding='utf-8', newline='\n').write(w)
    fw.put(NAME, page())
    print('fgs game controllers: page written')


if __name__ == '__main__':
    main()
