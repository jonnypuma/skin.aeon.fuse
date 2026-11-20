# -*- coding: utf-8 -*-
"""0.56.53 Font picker (script-aeon-fonts, fontpick.py) in the Fused Glass style (canvas round 2 FontsPicker2; user:
"I like the idea but they all look the same!" -> every card is drawn in its OWN fonts): the rows of list 100 become
specimen cards (three across, two rows on screen) on the frame; each card draws its sample in the families it carries
(item properties h = the title's family, b = the rest; fonts pv<n>_h / _t / _s / _b of Font.xml, one set of labels per
family number 0-44, shown by number), the focused card ringed white with the focus shadow, bar 61 in the gutter.
Heading: control 1 (set by the script). Repeatable."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

NAME = 'FontPick'
FAMILIES = 45


def card(focused):
    out = ''
    if focused:
        out += ('<control type="image"><left>-30</left><top>-24</top><width>596</width><height>390</height>%s<visible>Control.HasFocus(100) + $EXP[FGS_ShadowOn]</visible></control>' % fw.SHADOW)
    out += fw.img(0, 0, 536, 326, 'fg/r20.png', '6b000000' if focused else '0dffffff').replace('<texture colordiffuse', '<texture border="20" colordiffuse')
    out += fw.img(0, 0, 536, 326, 'fg/e20.png', '1fffffff').replace('<texture colordiffuse', '<texture border="20" colordiffuse')
    out += fw.label(26, 16, 456, 34, '[UPPERCASE]$INFO[ListItem.Label][/UPPERCASE]', 'st_cap_16', 'a6ffffff', extra='<scroll>%s</scroll>' % ('true' if focused else 'false'))
    out += fw.img(496, 25, 16, 16, 'fg/circle.png', 'fg_mark', 'ListItem.IsSelected')   # the font in use
    for n in range(FAMILIES):
        out += ('<control type="group"><visible>String.IsEqual(ListItem.Property(h),%d)</visible>'
                '<control type="label"><left>26</left><top>56</top><width>484</width><height>70</height><aligny>center</aligny><font>pv%d_h</font>'
                '<textcolor>ffffffff</textcolor><label>$LOCALIZE[31864]</label></control>'
                '<control type="label"><left>26</left><top>252</top><width>200</width><height>56</height><aligny>center</aligny><font>pv%d_h</font>'
                '<textcolor>ffffffff</textcolor><label>$INFO[System.Time]</label></control></control>' % (n, n, n))
        out += ('<control type="group"><visible>String.IsEqual(ListItem.Property(b),%d)</visible>'
                '<control type="label"><left>26</left><top>130</top><width>484</width><height>40</height><aligny>center</aligny><font>pv%d_t</font>'
                '<textcolor>f2ffffff</textcolor><label>$LOCALIZE[31866]</label></control>'
                '<control type="label"><left>26</left><top>170</top><width>484</width><height>32</height><aligny>center</aligny><font>pv%d_s</font>'
                '<textcolor>a6ffffff</textcolor><label>$LOCALIZE[31867]</label></control>'
                '<control type="label"><left>26</left><top>204</top><width>484</width><height>40</height><aligny>center</aligny><font>pv%d_b</font>'
                '<textcolor>b8ffffff</textcolor><label>$LOCALIZE[31868]</label></control></control>' % (n, n, n, n))
    if focused:
        out += fw.img(-3, -3, 542, 332, 'fg/ring20.png', 'ffffffff', 'Control.HasFocus(100)').replace('<texture colordiffuse', '<texture border="23" colordiffuse')
    return out


def page():
    return (
        '<include name="FontPick_PageFGS">'
        '<include content="FGS_DlgBack"/>'
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[5][/UPPERCASE]</label></control>'
        '<control type="label" id="1"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor></control>'
        '</control><include>Aeon_ClockBox</include>'
        + fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + fw.line(121, 191, 1699) +
        ''.join(fw.line(x, 108, 1, 852) for x in (120, 1800, 1820)) +
        fw.label(144, 120, 1300, 60, '[UPPERCASE]$INFO[Window.Property(section)][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        fw.label(1400, 120, 380, 60, '$INFO[Container(100).CurrentItem]$INFO[Container(100).NumItems, / ]', 'st_small_20', '8cffffff', 'right') +
        '<control type="panel" id="100"><left>132</left><top>206</top><width>1668</width><height>744</height><orientation>vertical</orientation>'
        '<onup>100</onup><ondown>100</ondown><onleft>noop</onleft><onright>61</onright><pagecontrol>61</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
        '<itemlayout width="556" height="372">%s</itemlayout><focusedlayout width="556" height="372">%s</focusedlayout></control>' % (card(False), card(True)) +
        fw.gutter_bar('61', 1801, 192, 768, '100', 'noop') +
        '</include>')


def main():
    fw.wrap('script-aeon-fonts.xml', NAME)
    fw.put(NAME, page())
    print('fgs font picker: page written')


if __name__ == '__main__':
    main()
