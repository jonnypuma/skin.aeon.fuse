# -*- coding: utf-8 -*-
"""0.56.53 Colour picker (DialogColorPicker) in the Fused Glass style (canvas round 2 ColourPicker2, "so good. build
that"): Kodi's colours (panel 6) as 80 px rounded swatches on the frame (the focused one ringed white), its square bar
61 in the gutter, and at the right a live preview of the colour in focus where an accent lands (the focused row's
marker and value, a progress bar, an outlined chip, the unwatched dot, the mark under a Home item) with its name and
hex. Cancel (7, grouplist 9001) as one 70 px cell under the preview. Kodi's heading (1) is the header's bold part.
Not built: the hue families and the contrast numbers (Kodi hands the list in its own order; the skin cannot compute).
Repeatable."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

NAME = 'ColPick'
HEX = '$INFO[Container(6).ListItem.Label2]'


def swatch(focused):
    s = ('<control type="image"><left>8</left><top>8</top><width>80</width><height>80</height><texture border="14">fg/r16.png</texture>'
         '<colordiffuse>$INFO[ListItem.Label2]</colordiffuse></control>')
    if focused:
        s = ('<control type="image"><left>0</left><top>0</top><width>96</width><height>96</height><texture border="19" colordiffuse="ffffffff">fg/ring16.png</texture>'
             '<visible>Control.HasFocus(6)</visible></control>' + s)
    return s


def page():
    pv = (fw.img(1200, 300, 600, 70, 'common/white.png', '57000000') +
          '<control type="image"><left>1200</left><top>300</top><width>600</width><height>70</height><texture border="20">fg/fgs_bar_dk.png</texture></control>'
          '<control type="image"><left>1200</left><top>300</top><width>6</width><height>70</height><texture>common/white.png</texture><colordiffuse>%s</colordiffuse></control>'
          % HEX +
          fw.label(1230, 300, 400, 70, '[UPPERCASE]$LOCALIZE[31206][/UPPERCASE]', 'st_ui_22_bold', 'ffffffff') +
          '<control type="label"><left>1400</left><top>300</top><width>376</width><height>70</height><align>right</align><aligny>center</aligny><font>st_ui_22</font>'
          '<textcolor>%s</textcolor><label>$LOCALIZE[305]</label></control>' % HEX +
          fw.img(1200, 410, 600, 8, 'fg/pillh.png', '2effffff').replace('<texture colordiffuse', '<texture border="2,0,2,0" colordiffuse') +
          '<control type="image"><left>1200</left><top>410</top><width>372</width><height>8</height><texture border="2,0,2,0">fg/pillh.png</texture><colordiffuse>%s</colordiffuse></control>' % HEX +
          '<control type="image"><left>1200</left><top>460</top><width>230</width><height>36</height><texture border="8">fg/e8.png</texture><colordiffuse>%s</colordiffuse></control>' % HEX +
          '<control type="label"><left>1200</left><top>460</top><width>230</width><height>36</height><align>center</align><aligny>center</aligny><font>st_cap_14</font>'
          '<textcolor>%s</textcolor><label>[UPPERCASE]$LOCALIZE[20338][/UPPERCASE]</label></control>' % HEX +
          '<control type="image"><left>1460</left><top>470</top><width>16</width><height>16</height><texture>fg/circle.png</texture><colordiffuse>%s</colordiffuse></control>' % HEX +
          fw.label(1200, 520, 600, 50, '[UPPERCASE]$LOCALIZE[10000][/UPPERCASE]', 'st_ui_28_bold', 'ffffffff') +
          '<control type="image"><left>1200</left><top>572</top><width>120</width><height>6</height><texture border="3,0,3,0">fg/pillh.png</texture><colordiffuse>%s</colordiffuse></control>' % HEX)
    return (
        '<include name="ColPick_PageFGS">'
        '<include content="FGS_DlgBack"/>'
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[5][/UPPERCASE]</label></control>'
        '<control type="label" id="1"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor></control>'
        '</control><include>Aeon_ClockBox</include>'
        + fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + fw.line(121, 191, 1699) +
        ''.join(fw.line(x, 108, 1, 852) for x in (120, 1120, 1140, 1180, 1820)) +
        fw.label(144, 120, 900, 60, '[UPPERCASE]$INFO[Container(6).ListItem.Label][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        fw.label(1204, 120, 600, 60, '$LOCALIZE[31681]', 'st_ui_28_semibold', 'ffffffff') +
        '<control type="panel" id="6"><left>136</left><top>200</top><width>976</width><height>752</height><orientation>vertical</orientation>'
        '<onup>6</onup><ondown>6</ondown><onleft>noop</onleft><onright>61</onright><pagecontrol>61</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
        '<viewtype label="100">icon</viewtype><itemlayout width="96" height="96">%s</itemlayout><focusedlayout width="96" height="96">%s</focusedlayout></control>'
        % (swatch(False), swatch(True)) +
        fw.gutter_bar('61', 1121, 192, 768, '6', '7') +
        fw.label(1204, 220, 600, 40, '[UPPERCASE]$INFO[Container(6).ListItem.Label][/UPPERCASE]', 'st_ui_24_semibold', 'ffffffff') +
        fw.label(1204, 256, 600, 30, '#$INFO[Container(6).ListItem.Label2]', 'st_Mono26', 'a6ffffff') +
        pv +
        # 0.3.117 helper: the colour in focus against white and against the style's dark ground
        fw.img(1200, 640, 290, 70, 'fg/r16.png', 'ffffffff').replace('<texture colordiffuse', '<texture border="16" colordiffuse') +
        '<control type="label"><left>1200</left><top>640</top><width>290</width><height>70</height><align>center</align><aligny>center</aligny><font>st_ui_26_semibold</font>'
        '<textcolor>%s</textcolor><label>Aa  $INFO[Window(Home).Property(aeon.cp.white)]</label></control>' % HEX +
        fw.img(1510, 640, 290, 70, 'fg/r16.png', 'ff08090c').replace('<texture colordiffuse', '<texture border="16" colordiffuse') +
        fw.img(1510, 640, 290, 70, 'fg/e16.png', '33ffffff').replace('<texture colordiffuse', '<texture border="16" colordiffuse') +
        '<control type="label"><left>1510</left><top>640</top><width>290</width><height>70</height><align>center</align><aligny>center</aligny><font>st_ui_26_semibold</font>'
        '<textcolor>%s</textcolor><label>Aa  $INFO[Window(Home).Property(aeon.cp.dark)]</label></control>' % HEX +
        fw.img(1764, 650, 22, 22, 'aeon/icons/check.png', 'fg_mark', '!String.IsEmpty(Window(Home).Property(aeon.cp.ok))') +
        fw.line(1180, 890, 640) +
        '<control type="grouplist" id="9001"><left>1181</left><top>891</top><width>639</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onleft>61</onleft><onright>noop</onright><onup>noop</onup><ondown>noop</ondown>'
        '%s</control>' % fw.cell('7', 639, '$LOCALIZE[222]', '<onleft>61</onleft>') +
        '</include>')


def main():
    fw.wrap('DialogColorPicker.xml', NAME)
    fw.put(NAME, page())
    print('fgs colour picker: page written')


if __name__ == '__main__':
    main()
