# -*- coding: utf-8 -*-
"""0.56.53 PVR channel manager and group manager in the Fused Glass style (canvas round 2: PVRChannelManager2 and
PVRGroupManager2, "so good. build that"; round 1 note "needs channel logos").

Channel manager (DialogPVRChannelManager): the frame 120-1820 x 108-960, title band with the counts; the channels
(list 20) as 70 px rows at the left with number, logo, name and Kodi's flags, inactive ones dimmed, the style's bar and
shadow, the square bar 60 in the gutter 1080-1100; at the right the focused channel's logo in the title band, its
switches (grouplist 9002: 7 active, 8 name, 9 logo, 12 guide, 13 guide source, 14 lock) and the tools (9003: 35 logos,
31 new, 30 groups, 34 TV / radio) as rows, OK / Apply / Cancel (9000: 4, 5, 6) as one row of cells at the foot.

Group manager (DialogPVRGroupManager): the groups (list 13) as rows at the left, bar 73; at the right the channels in
the group (list 12, Kodi's heading 22) and not in it (list 11, heading 21) as logo tiles, the members marked in the
accent, OK on a tile moves it across (Kodi); bars 72 / 71; the buttons (9000: 29 OK, 26 add, 27 rename, 25 hide,
28 delete, 35 thumbnail, 34 TV / radio) as one row of cells at the foot. Hidden label 20 kept. Repeatable."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

ROWLOOK = '<width>%d</width><include>FGS_DlgRow</include>'
RADIO = '<radioposx>%d</radioposx><include>FGS_RadioTex</include>'


def frame(cols):
    return (fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + fw.line(121, 191, 1699) +
            ''.join(fw.line(x, 108, 1, 852) for x in cols))


def chan_row(focused):
    out = ''
    if focused:
        out += ('<control type="image"><left>-40</left><top>-34</top><width>1039</width><height>150</height>%s<visible>Control.HasFocus(20) + $EXP[FGS_ShadowOn]</visible></control>'
                '<control type="image"><left>0</left><top>0</top><width>959</width><height>70</height>%s<visible>Control.HasFocus(20)</visible></control>' % (fw.SHADOW, fw.BAR))
    out += fw.img(0, 69, 959, 1, 'common/white.png', '14ffffff')
    out += ('<control type="group"><animation effect="fade" start="100" end="45" time="0" condition="!ListItem.Property(ActiveChannel)">Conditional</animation>'
            + fw.label(14, 0, 64, 70, '$INFO[ListItem.Property(Number)]', 'st_small_20_semibold', '8cffffff', 'right') +
            fw.img(96, 9, 96, 52, 'fg/r8.png', '0fffffff').replace('<texture colordiffuse', '<texture border="8" colordiffuse') +
            '<control type="image"><left>104</left><top>13</top><width>80</width><height>44</height><aspectratio>keep</aspectratio>'
            '<texture background="true">$INFO[ListItem.Property(icon)]</texture></control>'
            + fw.label(214, 0, 560, 70, '$INFO[ListItem.Property(Name)]', 'st_ui_24_semibold', 'ffffffff' if focused else 'd9ffffff',
                       extra='<scroll>true</scroll>' if focused else '') +
            fw.label(780, 0, 155, 70, '[UPPERCASE]$VAR[Misc_ChannelMgrFlags][/UPPERCASE]', 'st_cap_14', 'fg_mark', 'right') + '</control>')
    return out


def channel_manager():
    opts = (('radiobutton', 7, '$LOCALIZE[19074]'), ('edit', 8, '$LOCALIZE[19201]'), ('button', 9, '$LOCALIZE[19202]'),
            ('radiobutton', 12, '$LOCALIZE[19206]'), ('spincontrolex', 13, '$LOCALIZE[19200]'), ('radiobutton', 14, '$LOCALIZE[19267]'))
    rows = ''
    for kind, cid, lab in opts:
        extra = RADIO % 632 if kind == 'radiobutton' else ('<include>FGS_SpinTex</include>' if kind == 'spincontrolex' else '')
        rows += '<control type="%s" id="%d">%s%s<label>%s</label></control>' % (kind, cid, ROWLOOK % 719, extra, lab)
    tools = ('<control type="button" id="35">%s<label>$LOCALIZE[19041]</label></control>'
             '<control type="button" id="31">%s<label>$LOCALIZE[19204]</label></control>'
             '<control type="button" id="30">%s<label>$LOCALIZE[19205]</label></control>'
             '<control type="togglebutton" id="34">%s<label>$LOCALIZE[19024]</label><altlabel>$LOCALIZE[19023]</altlabel>'
             '<usealttexture>!String.IsEmpty(Window.Property(IsRadio))</usealttexture>'
             '<alttexturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</alttexturefocus><alttexturenofocus />'
             '</control>' % ((ROWLOOK % 719,) * 4))
    btn_nav = '<onup>34</onup><ondown>7</ondown>'
    return (
        '<include name="PVRChMgr_PageFGS">'
        '<include content="FGS_DlgBack"/>'
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[19020][/UPPERCASE]</label></control>'
        '<control type="label" id="2"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[19199]</label></control>'
        '</control><include>Aeon_ClockBox</include>'
        + frame((120, 1080, 1100, 1820)) +
        fw.label(144, 120, 920, 60, '[UPPERCASE]$LOCALIZE[19199][/UPPERCASE]$INFO[Container(20).NumItems,  ·  ,]', 'st_ui_28_semibold', 'ffffffff') +
        fw.label(1124, 120, 520, 60, '[UPPERCASE]$INFO[Container(20).ListItem.Property(Name)][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff', extra='<scroll>true</scroll>') +
        '<control type="image"><left>1660</left><top>116</top><width>140</width><height>68</height><aspectratio align="right">keep</aspectratio>'
        '<texture background="true">$INFO[Container(20).ListItem.Property(icon)]</texture></control>'
        '<control type="list" id="20"><left>121</left><top>191</top><width>959</width><height>770</height><orientation>vertical</orientation>'
        '<onup>20</onup><ondown>20</ondown><onleft>noop</onleft><onright>60</onright><pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
        '<itemlayout width="959" height="70">%s</itemlayout><focusedlayout width="959" height="70">%s</focusedlayout></control>' % (chan_row(False), chan_row(True)) +
        fw.gutter_bar('60', 1081, 192, 768, '20', '9002') +
        '<control type="grouplist" id="9002"><left>1101</left><top>191</top><width>719</width><height>420</height><orientation>vertical</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onleft>20</onleft><onright>noop</onright><onup>9000</onup><ondown>35</ondown>%s</control>' % rows +
        '<control type="grouplist" id="9003"><left>1101</left><top>611</top><width>719</width><height>280</height><orientation>vertical</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onleft>20</onleft><onright>noop</onright><onup>14</onup><ondown>9000</ondown>%s</control>' % tools +
        fw.line(1100, 890, 720) +
        '<control type="grouplist" id="9000"><left>1101</left><top>891</top><width>719</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onleft>20</onleft><onright>noop</onright><onup>34</onup><ondown>7</ondown>%s</control>'
        % (fw.cell('4', 180, '$LOCALIZE[186]', btn_nav) + fw.cell('5', 359, '$LOCALIZE[14070]', btn_nav) + fw.cell('6', 180, '$LOCALIZE[222]', btn_nav)) +
        fw.label(144, 975, 1600, 40, '$INFO[Container(20).ListItem.Property(ClientName),$LOCALIZE[19210]  ,]', 'st_small_20', '73ffffff') +
        '</include>')


def group_row(focused):
    out = ''
    if focused:
        out += ('<control type="image"><left>-40</left><top>-34</top><width>499</width><height>150</height>%s<visible>Control.HasFocus(13) + $EXP[FGS_ShadowOn]</visible></control>'
                '<control type="image"><left>0</left><top>0</top><width>419</width><height>70</height>%s<visible>Control.HasFocus(13)</visible></control>' % (fw.SHADOW, fw.BAR))
    return out + fw.img(0, 69, 419, 1, 'common/white.png', '14ffffff') + fw.label(24, 0, 380, 70, '$INFO[ListItem.Label]', 'st_ui_24_semibold', 'ffffffff' if focused else 'd9ffffff')


def tile(lid, focused, member):
    out = ''
    bg = '1ae8b04b' if member else '0affffff'
    if focused:
        out += ('<control type="image"><left>-30</left><top>-24</top><width>230</width><height>196</height>%s<visible>Control.HasFocus(%s) + $EXP[FGS_ShadowOn]</visible></control>'
                % (fw.SHADOW, lid))
    out += fw.img(0, 0, 170, 136, 'fg/r16.png', bg).replace('<texture colordiffuse', '<texture border="16" colordiffuse')
    out += fw.img(0, 0, 170, 136, 'fg/e16.png', '8ce8b04b' if member else '14ffffff').replace('<texture colordiffuse', '<texture border="16" colordiffuse')
    out += ('<control type="image"><left>25</left><top>18</top><width>120</width><height>62</height><aspectratio>keep</aspectratio>'
            '<texture background="true">$INFO[ListItem.Icon]</texture></control>')
    out += fw.label(8, 92, 154, 32, '$INFO[ListItem.ChannelNumberLabel,,  ]$INFO[ListItem.ChannelName]', 'st_cap_14', 'd9ffffff', 'center')
    if member:
        out += (fw.img(134, 8, 28, 28, 'fg/circle.png', 'fg_mark') +
                fw.img(140, 14, 16, 16, 'aeon/icons/check.png', 'ff000000'))
    if focused:
        out += fw.img(-3, -3, 176, 142, 'fg/ring16.png', 'ffffffff', 'Control.HasFocus(%s)' % lid).replace('<texture colordiffuse', '<texture border="19" colordiffuse')
    return out


def group_manager():
    btns = (('button', 29, '$LOCALIZE[186]'), ('button', 26, '$LOCALIZE[31211]'), ('button', 27, '$LOCALIZE[31212]'),
            ('radiobutton', 25, '$LOCALIZE[19289]'), ('button', 28, '$LOCALIZE[31213]'), ('button', 35, '$LOCALIZE[13315]'), ('togglebutton', 34, '$LOCALIZE[19174]'))
    widths = {29: 80, 26: 150, 27: 170, 25: 180, 28: 160, 35: 249, 34: 270}
    row = ''
    for kind, cid, lab in btns:
        if kind == 'button':
            row += fw.cell(str(cid), widths[cid], lab, '<onup>11</onup><ondown>13</ondown>', font='st_cap_14')
        else:
            extra = (RADIO % 112 + '<textoffsetx>16</textoffsetx>') if kind == 'radiobutton' else \
                    ('<altlabel>$LOCALIZE[19173]</altlabel><usealttexture>!String.IsEmpty(Window.Property(IsRadio))</usealttexture>'
                     '<alttexturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</alttexturefocus><alttexturenofocus />')
            row += ('<control type="%s" id="%d"><width>%d</width><height>70</height><font>st_cap_14</font><textcolor>ccffffff</textcolor><focusedcolor>ffffffff</focusedcolor>'
                    '<align>%s</align><aligny>center</aligny><label>[UPPERCASE]%s[/UPPERCASE]</label><texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus />'
                    '%s<onup>11</onup><ondown>13</ondown><include>FGS_RowAnim</include></control>'
                    % (kind, cid, widths[cid], 'left' if kind == 'radiobutton' else 'center', lab, extra))
    def panel(lid, top, h, sid, up, down):
        return ('<control type="panel" id="%d"><left>571</left><top>%d</top><width>1220</width><height>%d</height><orientation>vertical</orientation>'
                '<onup>%s</onup><ondown>%s</ondown><onleft>13</onleft><onright>%d</onright><pagecontrol>%d</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
                '<itemlayout width="174" height="150">%s</itemlayout><focusedlayout width="174" height="150">%s</focusedlayout></control>'
                % (lid, top, h, up, down, sid, sid, tile(lid, False, lid == 12), tile(lid, True, lid == 12)) +
                fw.gutter_bar(str(sid), 1801, top, h, str(lid), 'noop'))
    return (
        '<include name="PVRGrpMgr_PageFGS">'
        '<include content="FGS_DlgBack"/>'
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[19020][/UPPERCASE]</label></control>'
        '<control type="label" id="1"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[19048]</label></control>'
        '</control><include>Aeon_ClockBox</include>'
        + frame((120, 540, 560, 1800, 1820)) +
        fw.label(144, 120, 380, 60, '[UPPERCASE]$LOCALIZE[19048][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        fw.label(584, 120, 1000, 60, '[UPPERCASE]$INFO[Container(13).ListItem.Label][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        '<control type="image"><left>1600</left><top>116</top><width>190</width><height>68</height><aspectratio align="right">keep</aspectratio>'
        '<texture background="true">$INFO[Container(13).ListItem.Icon]</texture></control>'
        '<control type="list" id="13"><left>121</left><top>191</top><width>419</width><height>770</height><orientation>vertical</orientation>'
        '<onup>13</onup><ondown>13</ondown><onleft>noop</onleft><onright>12</onright><pagecontrol>73</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
        '<itemlayout width="419" height="70">%s</itemlayout><focusedlayout width="419" height="70">%s</focusedlayout></control>' % (group_row(False), group_row(True)) +
        fw.gutter_bar('73', 541, 192, 768, '13', '12') +
        '<control type="label" id="22"><left>584</left><top>196</top><width>900</width><height>40</height><aligny>center</aligny><font>st_cap_16</font><textcolor>a6ffffff</textcolor></control>'
        + fw.label(1500, 196, 290, 40, '$INFO[Container(12).NumItems]', 'st_cap_16', 'fg_mark', 'right') +
        panel(12, 240, 300, 72, '12', '11') +
        fw.line(561, 545, 1240) +
        '<control type="label" id="21"><left>584</left><top>550</top><width>900</width><height>40</height><aligny>center</aligny><font>st_cap_16</font><textcolor>a6ffffff</textcolor></control>'
        + fw.label(1500, 550, 290, 40, '$INFO[Container(11).NumItems]', 'st_cap_16', '8cffffff', 'right') +
        panel(11, 594, 296, 71, '12', '9000') +
        fw.line(560, 890, 1260) +
        '<control type="grouplist" id="9000"><left>561</left><top>891</top><width>1259</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onleft>13</onleft><onright>noop</onright><onup>11</onup><ondown>13</ondown>%s</control>' % row +
        fw.label(144, 975, 1600, 40, '$INFO[Container(13).ListItem.Property(ClientName)]', 'st_small_20', '73ffffff') +
        '<control type="label" id="20"><visible>false</visible></control>' +
        '</include>')


def main():
    fw.wrap('DialogPVRChannelManager.xml', 'PVRChMgr')
    fw.put('PVRChMgr', channel_manager())
    fw.wrap('DialogPVRGroupManager.xml', 'PVRGrpMgr')
    fw.put('PVRGrpMgr', group_manager())
    print('fgs pvr managers: pages written')


if __name__ == '__main__':
    main()
