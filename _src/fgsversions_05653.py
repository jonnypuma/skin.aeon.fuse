# -*- coding: utf-8 -*-
"""0.56.53 Manage versions / extras (DialogVideoManager) in the Fused Glass style (canvas round 2 VersionManager2,
"so good. build that"): the film's fanart under a dark veil, its clear logo (else the title), the versions as cards side
by side (list 50, horizontal: the art, the version name, the default marked in the accent, the chips and the facts of
that file), Kodi's buttons as one action row under them (grouplist 101: 21 play, 22 add version, 23 add extra, 27 art,
24 set default, 28 rename, 26 remove, 25 version type; Kodi shows / hides them), the file's path at the foot.
Kodi's heading (control 2) is the header's bold part. Repeatable."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

NAME = 'VidMgr'
CHIP = ('<control type="button"><width min="40" max="300">auto</width><height>32</height><label>%s</label><font>st_cap_14</font><textcolor>e6ffffff</textcolor>'
        '<focusedcolor>e6ffffff</focusedcolor><disabledcolor>e6ffffff</disabledcolor><textoffsetx>10</textoffsetx><aligny>center</aligny><enable>false</enable>'
        '<texturenofocus border="8" colordiffuse="b3ffffff">fg/e8.png</texturenofocus><texturefocus border="8" colordiffuse="b3ffffff">fg/e8.png</texturefocus>'
        '<visible>!String.IsEmpty(%s)</visible></control>')


def card(focused):
    f = focused
    out = ''
    if f:
        out += fw.img(-40, -34, 625, 600, 'fg/sh16.png', '$VAR[FG_ShadowColM]', 'Control.HasFocus(50) + $EXP[FGS_ShadowOn]').replace('<texture colordiffuse', '<texture border="56" colordiffuse')
    out += fw.img(0, 0, 545, 520, 'fg/r20.png', '66000000' if f else '0dffffff').replace('<texture colordiffuse', '<texture border="20" colordiffuse')
    out += ('<control type="image"><left>0</left><top>0</top><width>545</width><height>200</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m545x200t.png">$INFO[ListItem.Art(fanart)]</texture><visible>!String.IsEmpty(ListItem.Art(fanart))</visible></control>'
            '<control type="image"><left>0</left><top>0</top><width>545</width><height>200</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m545x200t.png">$INFO[Window(Home).Property(aeon.vm.fanart)]</texture><visible>String.IsEmpty(ListItem.Art(fanart))</visible></control>')
    out += fw.img(0, 80, 545, 120, 'fg/fgs_vi_b.png')
    out += fw.label(24, 140, 400, 50, '[UPPERCASE]$INFO[ListItem.Label][/UPPERCASE]', 'st_ui_30_semibold', 'ffffffff')
    out += ('<control type="group"><visible>ListItem.IsSelected</visible>'
            + fw.img(381, 18, 146, 34, 'fg/r16.png', 'fg_mark').replace('<texture colordiffuse', '<texture border="16" colordiffuse')
            + fw.label(381, 18, 146, 34, '[UPPERCASE]$LOCALIZE[571][/UPPERCASE]', 'st_cap_14', 'ff000000', 'center') + '</control>')
    # the version's file (Kodi hands the version items no runtime / size / streams; a grouplist in a row reads the focused item)
    out += ('<control type="textbox"><left>24</left><top>222</top><width>497</width><height>240</height><font>st_small_20</font>'
            '<textcolor>b3ffffff</textcolor><label>$INFO[ListItem.FileName]</label></control>')
    out += fw.img(24, 470, 497, 1, 'common/white.png', '14ffffff')
    ring = (fw.img(0, 0, 545, 520, 'fg/e20.png', 'ccffffff', 'Control.HasFocus(50)') if f else fw.img(0, 0, 545, 520, 'fg/e20.png', '1fffffff')).replace('<texture colordiffuse', '<texture border="20" colordiffuse')
    return out + ring


def page():
    btns = ((21, '$LOCALIZE[208]', 'true'), (22, '$LOCALIZE[40014]', 'Window.IsVisible(managevideoversions)'),
            (23, '$LOCALIZE[40015]', 'Window.IsVisible(managevideoextras)'), (27, '$LOCALIZE[13511]', 'true'),
            (24, '$LOCALIZE[40004]', 'Window.IsVisible(managevideoversions)'), (28, '$LOCALIZE[118]', 'Window.IsVisible(managevideoextras)'),
            (26, '$LOCALIZE[15015]', 'true'), (25, '$LOCALIZE[40023]', 'Window.IsVisible(managevideoversions)'))
    nav = '<onup condition="Integer.IsGreater(Container(50).NumItems,0)">50</onup><ondown>noop</ondown>'
    row = ''.join(fw.cell(str(i), 270, lab, nav, vis=v) for i, lab, v in btns)
    return (
        '<include name="VidMgr_PageFGS">'
        + fw.img(0, 0, 1920, 1080, 'common/white.png', 'ff08090c') +
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>300</fadetime>'
        '<texture background="true">$INFO[Container(50).ListItem.Art(fanart)]</texture></control>'
        + fw.img(0, 0, 1920, 1080, 'fg/fgs_vi_b.png') + fw.img(0, 0, 1920, 1080, 'common/white.png', 'b008090c') +
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[20338][/UPPERCASE]</label></control>'
        '<control type="label" id="2"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor></control>'
        '</control><include>Aeon_ClockBox</include>'
        '<control type="image"><left>120</left><top>130</top><width>760</width><height>100</height><aspectratio align="left" aligny="center">keep</aspectratio>'
        '<texture background="true">$INFO[Container(50).ListItem.Art(clearlogo)]</texture></control>'
        + fw.label(120, 130, 1700, 100, '[UPPERCASE]$INFO[Window(Home).Property(aeon.vm.title)][/UPPERCASE]', 'st_display_52', 'ffffffff', vis='String.IsEmpty(Container(50).ListItem.Art(clearlogo))')
        + fw.label(120, 240, 1700, 40, '$INFO[Container(50).NumItems]  ·  $INFO[Container(50).ListItem.Label]', 'st_ui_24', 'b8ffffff') +
        '<control type="group" id="100">'
        '<control type="list" id="50"><left>120</left><top>310</top><width>1700</width><height>540</height><orientation>horizontal</orientation>'
        '<onup>noop</onup><ondown>101</ondown><onleft>noop</onleft><onright>noop</onright><scrolltime tween="cubic" easing="out">220</scrolltime>'
        '<itemlayout width="577" height="540">%s</itemlayout><focusedlayout width="577" height="540">%s</focusedlayout></control>'
        '</control>' % (card(False), card(True)) +
        fw.line(120, 880, 1700) + fw.line(120, 950, 1700) + fw.line(120, 880, 1, 71) +
        '<control type="grouplist" id="101"><left>121</left><top>881</top><width>1699</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onup condition="Integer.IsGreater(Container(50).NumItems,0)">50</onup><ondown>noop</ondown><onleft>noop</onleft><onright>noop</onright>'
        '%s</control>' % row
        + fw.label(120, 970, 1700, 40, '$INFO[Container(50).ListItem.FileNameAndPath]', 'st_small_20', '73ffffff', extra='<scroll>true</scroll>') +
        '</include>')


def main():
    from PIL import Image, ImageDraw
    p = os.path.join(fw.SKIN, 'media', 'fg', 'm545x200t.png')
    m = Image.new('RGBA', (545, 200), (255, 255, 255, 0))
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 544, 239), radius=20, fill=(255, 255, 255, 255))
    m.save(p)
    fw.wrap('DialogVideoManager.xml', NAME)
    w = os.path.join(fw.D, 'DialogVideoManager.xml')
    import io
    s = io.open(w, encoding='utf-8').read()
    extra = ('<onload>SetProperty(aeon.vm.fanart,$ESCINFO[ListItem.Art(fanart)],home)</onload>\n\t'
             '<onload>SetProperty(aeon.vm.logo,$ESCINFO[ListItem.Art(clearlogo)],home)</onload>\n\t'
             '<onunload>ClearProperty(aeon.vm.fanart,home)</onunload>\n\t<onunload>ClearProperty(aeon.vm.logo,home)</onunload>\n\t')
    if 'aeon.vm.fanart' not in s:
        s = s.replace('<include>Anim_DialogOpenClose</include>', extra + '<include>Anim_DialogOpenClose</include>', 1)
        io.open(w, 'w', encoding='utf-8', newline='\n').write(s)
    fw.put(NAME, page())
    print('fgs versions: page written')


if __name__ == '__main__':
    main()
