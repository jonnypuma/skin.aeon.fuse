# -*- coding: utf-8 -*-
"""0.56.53 Live TV in the Fused Glass style (canvas round 8; user: "Build these windows: recordings, timer rules,
search and put days over EPG as in screenshot"). Every other theme / style keeps today's pages.

- Guide: eight day chips over the grid (helper aeon.gd.d1-8, the day in view gold, a dot where a timer is set; OK
  jumps the grid to that day: PVR.EpgGridControl(CurrentProgramme) then +24 per day). Up from the group pill reaches
  them. The programme's time line gets its day in words (aeon.gd.long) in Fused Glass.
- Recordings: the list becomes cards like the library (art, NEW, how far you got, channel logo, date, channel, length).
- Search: the search as a big field, the results as rows with the day, time, channel logo and a mark when a timer is set.
- Timer rules: each rule as a card with what it catches as a sentence (helper ?info=timerrules); Kodi's list 50 stays
  the focus (its focused rule's card is white); New rule / Edit / Activate-Deactivate / Delete as cells.
Repeatable; run after fg_livetv.py / fgstimers_05653.py."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

ADD = '$ADDON[skin.aeon.fuse %d]'
HP = 'Window(Home).Property(%s)'
RMODE = '$EXP[FGS] + Window.IsActive(TVTimerRules)'
TMODE = '$EXP[FGS] + Window.IsActive(TVTimers)'


def rd(path):
    return io.open(path, encoding='utf-8').read()


def wr(path, s):
    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)


def pill_btn(cid, label, nav, clicks, color_var):
    return ('<control type="button" id="%d"><width min="120" max="420">auto</width><height>44</height><label>%s</label>'
            '<font>st_small_20_semibold</font><textcolor>$VAR[%s]</textcolor><focusedcolor>ff0b0d11</focusedcolor><textoffsetx>22</textoffsetx>'
            '<align>center</align><aligny>center</aligny><texturefocus border="22" colordiffuse="ffffffff">fg/r22.png</texturefocus>'
            '<texturenofocus border="22" colordiffuse="$VAR[%sEdge]">fg/e22.png</texturenofocus>%s%s</control>'
            % (cid, label, color_var, color_var, nav, ''.join('<onclick>%s</onclick>' % c for c in clicks)))


# ---------------------------------------------------------------- guide days
def guide_days():
    btns, vars_ = '', ''
    for n in range(1, 9):
        clicks = ['PVR.EpgGridControl(CurrentProgramme)'] + ['PVR.EpgGridControl(+24)'] * (n - 1) + ['SetFocus(9100)']
        btns += pill_btn(9070 + n, '$INFO[%s]' % (HP % ('aeon.gd.d%d' % n)), '', clicks, 'FGS_GdInk%d' % n)
        cur = 'String.IsEqual(%s,%d)' % (HP % 'aeon.gd.cur', n)
        vars_ += ('<variable name="FGS_GdInk%d"><value condition="%s">fg_mark</value><value>d9ffffff</value></variable>'
                  '<variable name="FGS_GdInk%dEdge"><value condition="%s">ffe8b04b</value><value>33ffffff</value></variable>' % (n, cur, n, cur))
    return ('<include name="FGS_GuideDays"><control type="group"><visible>Window.IsActive(TVGuide) + !$EXP[FG_GuideOSD]</visible>'
            '<control type="grouplist" id="9070"><left>96</left><top>384</top><width>1728</width><height>44</height><orientation>horizontal</orientation>'
            '<itemgap>10</itemgap><onup>SetFocus(101)</onup><ondown>6056</ondown><onleft>9078</onleft><onright>9071</onright>%s</control>'
            '</control></include>' % btns + vars_)


def patch_guide():
    p = os.path.join(fw.D, 'MyPVRGuide.xml')
    s = rd(p)
    if 'FGS_GuideDays' not in s:
        s = s.replace('\t</controls>\n</window>', '\t\t<include condition="$EXP[FGS]">FGS_GuideDays</include>\n\t</controls>\n</window>', 1)
        assert 'FGS_GuideDays' in s
        wr(p, s)
    p = os.path.join(fw.D, 'Includes_Fused.xml')
    s = rd(p)
    i = s.index('<control type="button" id="6056">')
    j = s.index('</control>', i)
    seg = s[i:j]
    if '9070' not in seg:
        seg = seg.replace('<onup condition="!$EXP[FG_GuideOSD]">SetFocus(101)</onup>',
                          '<onup condition="!$EXP[FG_GuideOSD] + $EXP[FGS]">9070</onup><onup condition="!$EXP[FG_GuideOSD] + !$EXP[FGS]">SetFocus(101)</onup>', 1)
        assert '9070' in seg
        s = s[:i] + seg + s[j:]
    old = '<label>$INFO[Container(50).ListItem.StartTime]$INFO[Container(50).ListItem.EndTime,–,]'
    if 'aeon.gd.long' in s:
        s = s.replace('$INFO[Window(Home).Property(aeon.gd.long),,  ·  ]', '$INFO[Container(50).ListItem.StartDate,,  ·  ]')
    while old in s:
        s = s.replace(old, '<label>$INFO[Container(50).ListItem.StartDate,,  ·  ]$INFO[Container(50).ListItem.StartTime]$INFO[Container(50).ListItem.EndTime,–,]', 1)
    wr(p, s)


# ---------------------------------------------------------------- recordings
def rec_card(focused):
    out = ''
    if focused:
        out += '<control type="image"><left>-36</left><top>-30</top><width>472</width><height>297</height>%s<visible>Control.HasFocus(50)</visible></control>' % fw.SHADOW
    out += fw.img(0, 0, 400, 225, 'common/white.png', '14ffffff').replace('<texture colordiffuse', '<texture diffuse="fg/m400x225.png" colordiffuse')
    out += ('<control type="image"><left>0</left><top>0</top><width>400</width><height>225</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m400x225.png">$VAR[FGS_RecArt]</texture></control>')
    out += fw.img(170, 80, 60, 60, 'icons/af3/folder-closed.png', '99ffffff', 'ListItem.IsFolder + String.IsEmpty(ListItem.Art(thumb))')
    out += fw.img(14, 14, 64, 26, 'fg/r12.png', 'fg_mark', '!ListItem.IsFolder + Integer.IsEqual(ListItem.PlayCount,0) + !Integer.IsGreater(ListItem.PercentPlayed,0)').replace('<texture colordiffuse', '<texture border="12" colordiffuse')
    out += fw.label(14, 14, 64, 26, '[UPPERCASE]%s[/UPPERCASE]' % (ADD % 32819), 'st_cap_12', 'ff0b0d11', 'center', '!ListItem.IsFolder + Integer.IsEqual(ListItem.PlayCount,0) + !Integer.IsGreater(ListItem.PercentPlayed,0)')
    out += ('<control type="image"><left>300</left><top>180</top><width>86</width><height>32</height><aspectratio align="right">keep</aspectratio>'
            '<texture background="true">$INFO[ListItem.ChannelLogo]</texture></control>')
    out += ('<control type="progress"><left>0</left><top>220</top><width>400</width><height>5</height><info>ListItem.PercentPlayed</info>'
            '<texturebg colordiffuse="00ffffff">common/white.png</texturebg><lefttexture /><midtexture colordiffuse="fg_mark">common/white.png</midtexture><righttexture />'
            '<visible>Integer.IsGreater(ListItem.PercentPlayed,0)</visible></control>')
    if focused:
        out += fw.img(-3, -3, 406, 231, 'fg/ring14.png', 'ffffffff', 'Control.HasFocus(50)').replace('<texture colordiffuse', '<texture border="17" colordiffuse')
    out += fw.label(0, 236, 400, 34, '$INFO[ListItem.Label]', 'st_ui_22_bold', 'ffffffff', extra='<scroll>%s</scroll>' % ('true' if focused else 'false'))
    out += fw.label(0, 270, 400, 28, '$INFO[ListItem.Date]$INFO[ListItem.ChannelName,  ·  ,]$INFO[ListItem.Duration,  ·  ,]', 'st_small_20', '8cffffff')
    return out


def recordings():
    return ('<include name="FGS_Recordings">'
            '<control type="grouplist"><left>120</left><top>184</top><width>1400</width><height>60</height><orientation>horizontal</orientation><itemgap>16</itemgap><usecontrolcoords>true</usecontrolcoords>'
            '<control type="label"><width>auto</width><height>60</height><aligny>center</aligny><font>st_display_40</font><textcolor>fg_mark</textcolor><label>$INFO[Container(50).NumItems]</label></control>'
            '<control type="label"><width>auto</width><height>60</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor><label>[LOWERCASE]$LOCALIZE[19017][/LOWERCASE]</label></control>'
            '<control type="label"><width>auto</width><height>60</height><aligny>center</aligny><font>st_small_20</font><textcolor>8cffffff</textcolor><label>$INFO[PVR.BackendDiskSpace,·  ,]</label><visible>Integer.IsGreater(Container(50).NumItems,0)</visible></control>'
            '</control>'
            '<control type="group" id="9100"><defaultcontrol always="true">50</defaultcontrol>'
            '<control type="panel" id="50"><left>120</left><top>262</top><width>1680</width><height>700</height><orientation>vertical</orientation>'
            '<visible>Integer.IsGreater(Container(50).NumItems,0)</visible>'
            '<onup>9001</onup><ondown>50</ondown><onleft>noop</onleft><onright>60</onright><pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<viewtype label="535">list</viewtype>'
            '<itemlayout width="420" height="330">%s</itemlayout><focusedlayout width="420" height="330">%s</focusedlayout></control>'
            '<control type="button" id="9099"><left>120</left><top>262</top><width>420</width><height>70</height><label>$LOCALIZE[31231]</label>'
            '<font>st_ui_22_semibold</font><textcolor>ccffffff</textcolor><focusedcolor>ffffffff</focusedcolor><align>center</align><aligny>center</aligny>'
            '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus border="20" colordiffuse="40ffffff">fg/e20.png</texturenofocus>'
            '<onclick>ActivateWindow(pvrsettings)</onclick><onup>9001</onup><visible>Integer.IsEqual(Container(50).NumItems,0) + !Container(50).IsUpdating</visible></control>'
            '</control>' % (rec_card(False), rec_card(True)) +
            fw.gutter_bar('60', 1801, 262, 698, '50') +
            '</include>'
            '<variable name="FGS_RecArt"><value condition="!String.IsEmpty(ListItem.Art(thumb))">$INFO[ListItem.Art(thumb)]</value>'
            '<value condition="!String.IsEmpty(ListItem.Art(fanart))">$INFO[ListItem.Art(fanart)]</value><value>$INFO[ListItem.Icon]</value></variable>')


# ---------------------------------------------------------------- search
def search_row(focused):
    out = (('<control type="image"><left>0</left><top>0</top><width>1680</width><height>84</height><texture border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texture><visible>Control.HasFocus(50)</visible></control>')
           if focused else '')
    out += fw.img(0, 83, 1680, 1, 'common/white.png', '12ffffff')
    out += fw.img(28, 26, 32, 32, 'icons/af3/magnifying-glass.png', '99ffffff', 'String.IsEmpty(ListItem.StartTime)')
    out += fw.label(84, 0, 1500, 84, '$VAR[Misc_PVRSearchLabel]', 'st_ui_24_semibold', 'ffffffff', vis='String.IsEmpty(ListItem.StartTime)')
    out += '<control type="group"><visible>!String.IsEmpty(ListItem.StartTime)</visible>'
    out += fw.label(24, 0, 170, 84, '[UPPERCASE]$INFO[ListItem.StartDate][/UPPERCASE]', 'st_cap_14', 'fg_mark')
    out += fw.label(200, 0, 100, 84, '$INFO[ListItem.StartTime]', 'st_ui_24_bold', 'ffffffff')
    out += fw.img(310, 20, 96, 44, 'fg/r8.png', '14ffffff', '!String.IsEmpty(ListItem.ChannelLogo)').replace('<texture colordiffuse', '<texture border="8" colordiffuse')
    out += ('<control type="image"><left>320</left><top>26</top><width>76</width><height>32</height><aspectratio>keep</aspectratio>'
            '<texture background="true">$INFO[ListItem.ChannelLogo]</texture></control>')
    out += fw.label(430, 0, 840, 84, '$VAR[Misc_PVRSearchLabel]', 'st_ui_24_semibold', 'ffffffff', extra='<scroll>%s</scroll>' % ('true' if focused else 'false'))
    out += fw.label(1280, 0, 220, 84, '$INFO[ListItem.ChannelName]', 'st_small_20', '8cffffff', 'right')
    out += fw.img(1516, 26, 140, 32, 'fg/r16.png', '00ffffff', 'ListItem.HasTimer')
    out += fw.img(1516, 26, 140, 32, 'fg/e16.png', 'ffe8b04b', 'ListItem.HasTimer').replace('<texture colordiffuse', '<texture border="16" colordiffuse')
    out += fw.label(1516, 26, 140, 32, '[UPPERCASE]$LOCALIZE[19040][/UPPERCASE]', 'st_cap_12', 'fg_mark', 'center', 'ListItem.HasTimer')
    return out + '</control>'


def search():
    return ('<include name="FGS_Search">'
            + '<control type="group"><visible>!String.IsEmpty(Control.GetLabel(29)) | !String.IsEmpty(Control.GetLabel(30))</visible>'
            + fw.img(120, 180, 1700, 84, 'fg/r40.png', '12ffffff').replace('<texture colordiffuse', '<texture border="40" colordiffuse')
            + fw.img(120, 180, 1700, 84, 'fg/e40.png', '2effffff').replace('<texture colordiffuse', '<texture border="40" colordiffuse')
            + fw.img(160, 206, 32, 32, 'icons/af3/magnifying-glass.png', '99ffffff')
            + fw.label(214, 180, 1100, 84, '$INFO[Control.GetLabel(29)]$INFO[Control.GetLabel(30),  ·  ,]', 'st_ui_28_bold', 'ffffffff')
            + fw.label(1320, 180, 470, 84, '$INFO[Container(50).NumItems]', 'st_small_20', '8cffffff', 'right') + '</control>' +
            '<control type="group" id="9100"><defaultcontrol always="true">50</defaultcontrol>'
            '<animation effect="slide" end="0,-96" time="0" condition="String.IsEmpty(Control.GetLabel(29)) + String.IsEmpty(Control.GetLabel(30))">Conditional</animation>'
            '<control type="list" id="50"><left>120</left><top>290</top><width>1680</width><height>672</height><orientation>vertical</orientation>'
            '<onup>9001</onup><ondown>50</ondown><onleft>noop</onleft><onright>60</onright><pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<viewtype label="535">list</viewtype>'
            '<itemlayout width="1680" height="84">%s</itemlayout><focusedlayout width="1680" height="84">%s</focusedlayout></control>'
            '<include content="Misc_EmptyStateButton"><param name="top" value="misc_pvr_top"/><param name="label" value="%s"/></include>'
            '</control>' % (search_row(False), search_row(True), ADD % 32358) +
            fw.gutter_bar('60', 1801, 290, 672, '50') +
            '</include>')


def patch_list_window(fname, inc):
    p = os.path.join(fw.D, fname)
    s = rd(p)
    if inc not in s:
        s = s.replace('\t\t<include content="Misc_PVRList">', '\t\t<include content="%s" condition="$EXP[FGS]"/>\n\t\t<include content="Misc_PVRList" condition="!$EXP[FGS]">' % inc, 1)
        assert inc in s
        wr(p, s)


# ---------------------------------------------------------------- timer rules
def rule_card(focused):
    on = 'String.IsEqual(ListItem.Label,Container(50).ListItem.Label) + Control.HasFocus(50)'
    out = '<control type="image"><left>-36</left><top>-30</top><width>1772</width><height>210</height>%s<visible>%s</visible></control>' % (fw.SHADOW, on)
    out += fw.img(0, 0, 1700, 150, 'fg/r16.png', '0fffffff', '![%s]' % on).replace('<texture colordiffuse', '<texture border="16" colordiffuse')
    out += fw.img(0, 0, 1700, 150, 'fg/r16.png', 'ffffffff', on).replace('<texture colordiffuse', '<texture border="16" colordiffuse')
    out += fw.img(30, 43, 110, 64, 'fg/r12.png', 'ff1b1f27').replace('<texture colordiffuse', '<texture border="12" colordiffuse')
    out += ('<control type="image"><left>40</left><top>51</top><width>90</width><height>48</height><aspectratio>keep</aspectratio>'
            '<texture background="true">$INFO[ListItem.Icon]</texture></control>')
    for ink, ink2, vis in (('ffffffff', 'bfffffff', '![%s]' % on), ('ff0b0d11', 'b30b0d11', on)):
        out += fw.label(170, 34, 1480, 44, '$INFO[ListItem.Label]', 'st_ui_28_bold', ink, vis=vis)
        out += fw.label(170, 80, 1480, 36, '$INFO[ListItem.Label2]', 'st_small_20', ink2, vis=vis)
    out += fw.label(1500, 0, 170, 150, '[UPPERCASE]$LOCALIZE[24021][/UPPERCASE]', 'st_cap_14', 'ffe05a4f', 'right', '!String.IsEmpty(ListItem.Property(off))')
    return out


def rules():
    nav = '<onup>50</onup>'
    on = '!String.IsEmpty(Container(50).ListItem.Label) + !String.IsEqual(Container(50).CurrentItem,1)'
    cells = (fw.cell('9061', 425, '[COLOR fg_mark]+[/COLOR]  $LOCALIZE[19056]', nav, ('SetFocus(50,0,absolute)', 'SendClick(50)'), font='st_cap_16')
             + fw.cell('9062', 425, '$LOCALIZE[21435]', nav, ('SendClick(50)',), font='st_cap_16').replace('<onup>50</onup>', '<onup>50</onup><enable>%s</enable>' % on, 1)
             + fw.cell('9063', 425, '$LOCALIZE[844]  /  $LOCALIZE[843]', nav, ('SetFocus(50)', 'Action(ContextMenu)'), font='st_cap_16').replace('<onup>50</onup>', '<onup>50</onup><enable>%s</enable>' % on, 1)
             + fw.cell('9064', 425, '$LOCALIZE[117]', nav, ('RunScript(script.aeon.helper,livetv,delrule)',), font='st_cap_16').replace('<onup>50</onup>', '<onup>50</onup><enable>%s</enable>' % on, 1))
    return ('<include name="FGS_TimerRules"><control type="group"><visible>Window.IsActive(TVTimerRules)</visible>'
            +
            '<control type="grouplist"><left>120</left><top>134</top><width>1700</width><height>60</height><orientation>horizontal</orientation><itemgap>16</itemgap><usecontrolcoords>true</usecontrolcoords>'
            '<control type="label"><width>auto</width><height>60</height><aligny>center</aligny><font>st_display_40</font><textcolor>fg_mark</textcolor><label>$INFO[Container(9069).NumItems]</label>'
            '<visible>Integer.IsGreater(Container(9069).NumItems,0)</visible></control>'
            '<control type="label"><width>auto</width><height>60</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor><label>%s</label></control>'
            '</control>' % (ADD % 32817) +
            '<control type="list" id="9069"><left>120</left><top>220</top><width>1700</width><height>656</height><orientation>vertical</orientation>'
            '<content>plugin://script.aeon.helper/?info=timerrules&amp;n=$INFO[Window(Home).Property(aeon.tr.stamp)]</content>'
            '<itemlayout width="1700" height="164">%s</itemlayout><focusedlayout width="1700" height="164">%s</focusedlayout></control>' % (rule_card(False), rule_card(False)) +
            fw.label(120, 220, 1700, 400, ADD % 32818, 'st_ui_24_semibold', '8cffffff', 'center', 'Integer.IsEqual(Container(9069).NumItems,0) + !Container(9069).IsUpdating') +
            fw.line(120, 889, 1700) + fw.line(120, 960, 1700) + fw.line(120, 890, 1, 70) +
            '<control type="grouplist" id="9060"><left>120</left><top>890</top><width>1700</width><height>70</height><orientation>horizontal</orientation>'
            '<itemgap>0</itemgap><onleft>9064</onleft><onright>9061</onright><onup>50</onup>%s</control>' % cells +
            '</control></include>')


def patch_rules_nav():
    p = os.path.join(fw.D, 'MyPVRTimers.xml')
    s = rd(p)
    if 'FGS_TimerRules' not in s:
        s = s.replace('\t\t<include condition="$EXP[FGS]">FGS_TimersWeek</include>', '\t\t<include condition="$EXP[FGS]">FGS_TimersWeek</include>\n\t\t<include condition="$EXP[FGS]">FGS_TimerRules</include>', 1)
        assert 'FGS_TimerRules' in s
        wr(p, s)
    p = os.path.join(fw.D, 'Includes_Misc.xml')
    s = rd(p)
    a = s.index('<include name="Misc_PVRList">')
    b = s.index('</include>', s.index('<include>Misc_PVRInfoPanel</include>', a))
    seg = s[a:b]
    if 'TVTimerRules' not in seg:
        for act, rule_to, old_to in (('onup', '104', '9001'), ('ondown', '9060', '50'), ('onright', '9060', '60')):
            old = '<%s condition="![%s]">%s</%s>' % (act, TMODE, old_to, act)
            assert old in seg, old
            seg = seg.replace(old, '<%s condition="%s">%s</%s><%s condition="![%s] + ![%s]">%s</%s>' % (act, RMODE, rule_to, act, act, TMODE, RMODE, old_to, act), 1)
        s = s[:a] + seg + s[b:]
        wr(p, s)
    p = os.path.join(fw.D, 'Includes_Fused.xml')
    s = rd(p)
    i = s.index('<control type="button" id="104">')
    j = s.index('</control>', i)
    seg = s[i:j]
    if 'TVTimerRules)">9100' not in seg and '<ondown condition="Control.IsVisible(9001)">9001</ondown>' in seg:
        seg = seg.replace('<ondown condition="Control.IsVisible(9001)">9001</ondown>',
                          '<ondown condition="%s">9100</ondown><ondown condition="Control.IsVisible(9001) + ![%s]">9001</ondown>' % (RMODE, RMODE), 1)
        s = s[:i] + seg + s[j:]
        wr(p, s)


def main():
    patch_guide()
    patch_list_window('MyPVRRecordings.xml', 'FGS_Recordings')
    patch_list_window('MyPVRSearch.xml', 'FGS_Search')
    patch_rules_nav()
    fw.put('LiveTV', guide_days() + recordings() + search() + rules())
    print('fgs live tv: guide days, recordings, search, timer rules written')


if __name__ == '__main__':
    main()
