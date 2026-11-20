# -*- coding: utf-8 -*-
"""0.56.53 round 3 of the Fused Glass style windows (canvas round 3, user 2026-11-20: "go ahead building the last
mockups, they all look good"). New pages next to the first style pass; each window now loads the round-3 include:
- Play queue (MyPlaylist): FGS_Playlist3 - the record player at the left (cover, record for music, title, progress,
  times; the focused song when nothing plays), Shuffle / Repeat / Save / Clear as cells under it; the queue as a rail
  of dots (gold = playing) with art, title, artist and length; bar 60 in the gutter.
- File browser (FileBrowser): FGS_FileBrowser3 - the path as crumbs (helper aeon.fb.c1-6), the files (450) in the
  middle, at the right a peek inside the folder in focus (helper ?info=peek) and its counts, OK / Cancel / New folder /
  Mirror (413-416) as rows.
- Text viewer (DialogTextViewer): FGS_TextViewer3 - a reader: the heading and the reading time at the left (helper
  aeon.tv.mins), the text (5) in a serif column of comfortable measure, bar 3000 as a page rail in the gutter.
- Media source (DialogMediaSource): FGS_MediaSource3 - all sources at the left (helper ?info=sources, the one being
  edited lit), the three steps in the band, the paths (10) with the room, Browse / Add / Remove as rows, a peek inside
  the path in focus, the name row and OK / Cancel.
- Settings, centred: the PVR timer dialog gets the left column that says what will happen (title, channel, day,
  begin - end on a bar).
- Settings, side panel: the subtitles tab shows the film's subtitles as cards with round flags (helper
  ?info=substreams; your language first, OK picks it: RunScript(script.aeon.helper,setsub,<index>)).
Run after fgsplaylist / fgsfilebrowser / fgstextviewer / fgsmediasource / fgssettingsdlg. Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

LINE = fw.LINE
FOC = ('<control type="image"><left>-40</left><top>-34</top><width>%d</width><height>150</height>' + fw.SHADOW +
       '<visible>Control.HasFocus(%s) + $EXP[FGS_ShadowOn]</visible></control>'
       '<control type="image"><left>0</left><top>0</top><width>%d</width><height>70</height>' + fw.BAR + '<visible>Control.HasFocus(%s)</visible></control>')


def frame(cols, top=191):
    return (fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + fw.line(121, top, 1699) +
            ''.join(fw.line(x, 108, 1, 852) for x in cols))


def swap(window, old, new):
    p = os.path.join(fw.D, window)
    s = io.open(p, encoding='utf-8').read()
    if '>%s</include>' % new not in s:
        a = '<include condition="$EXP[FGS]">%s</include>' % old
        assert a in s, (window, old)
        s = s.replace(a, '<include condition="$EXP[FGS]">%s</include>' % new, 1)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


# ---------------------------------------------------------------- play queue
def queue_row(focused):
    w = 1179
    out = (FOC % (w + 80, '50', w, '50')) if focused else ''
    out += fw.img(0, 69, w, 1, 'common/white.png', '12ffffff')
    out += fw.img(40, 0, 2, 70, 'common/white.png', '1fffffff')
    out += fw.img(35, 29, 12, 12, 'fg/circle.png', 'fg_mark', 'ListItem.IsPlaying')
    out += fw.img(36, 30, 10, 10, 'fg/circle.png', '59ffffff', '!ListItem.IsPlaying')
    out += ('<control type="image"><left>70</left><top>11</top><width>48</width><height>48</height><aspectratio>scale</aspectratio>'
            '<texture background="true" diffuse="fg/m48x48.png">$INFO[ListItem.Icon]</texture></control>')
    ink = 'ffffffff' if focused else 'd9ffffff'
    out += fw.label(136, 8, 900, 32, '$INFO[ListItem.Title]', 'st_ui_24_semibold', ink, vis='!String.IsEmpty(ListItem.Title)')
    out += fw.label(136, 0, 900, 70, '$INFO[ListItem.Label]', 'st_ui_24_semibold', ink, vis='String.IsEmpty(ListItem.Title)')
    out += fw.label(136, 38, 900, 26, '$INFO[ListItem.Artist]$INFO[ListItem.Album,  ·  ,]', 'st_small_20', '80ffffff', vis='!String.IsEmpty(ListItem.Title)')
    out += fw.label(1050, 0, 105, 70, '$INFO[ListItem.Duration]', 'st_small_20', '99ffffff', 'right')
    return out


def playlist():
    nav = '<onup>50</onup><ondown>50</ondown>'
    playing = 'Player.HasMedia'
    left = (
        # the record player: what plays now
        '<control type="group"><visible>%s</visible>' % playing +
        fw.img(210, 216, 400, 400, 'fg/fgs_vinyl.png', vis='Player.HasAudio') +
        fw.img(110, 176, 480, 480, 'fg/sh16.png', '$VAR[FG_ShadowColM]').replace('<texture colordiffuse', '<texture border="56" colordiffuse') +
        '<control type="image"><left>150</left><top>216</top><width>400</width><height>400</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m404x404.png">$INFO[Player.Art(thumb)]</texture></control>' +
        fw.label(150, 640, 450, 44, '[UPPERCASE]$INFO[Player.Title][/UPPERCASE]', 'st_ui_28_bold', 'ffffffff') +
        fw.label(150, 684, 450, 30, '$INFO[MusicPlayer.Artist]$INFO[MusicPlayer.Album,  ·  ,]$INFO[VideoPlayer.TVShowTitle]', 'st_small_20', 'a6ffffff') +
        '<control type="progress"><left>150</left><top>750</top><width>440</width><height>6</height><texturebg border="2,0,2,0" colordiffuse="2effffff">fg/pillh.png</texturebg>'
        '<midtexture border="2,0,2,0" colordiffuse="fg_mark">fg/pillh.png</midtexture><info>Player.Progress</info></control>' +
        fw.label(150, 762, 200, 30, '$INFO[Player.Time]', 'st_small_20', '99ffffff') + fw.label(390, 764, 200, 30, '$INFO[Player.Duration]', 'st_small_20', '99ffffff', 'right') +
        '</control>'
        # nothing plays: the song in focus
        '<control type="group"><visible>!%s + Integer.IsGreater(Container(50).NumItems,0)</visible>' % playing +
        '<control type="image"><left>150</left><top>216</top><width>400</width><height>400</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m404x404.png">$INFO[Container(50).ListItem.Icon]</texture></control>' +
        fw.label(150, 640, 450, 44, '[UPPERCASE]$INFO[Container(50).ListItem.Title][/UPPERCASE]', 'st_ui_28_bold', 'ffffffff') +
        fw.label(150, 684, 450, 30, '$INFO[Container(50).ListItem.Artist]', 'st_small_20', 'a6ffffff') +
        '</control>')
    nav1 = '<onup>50</onup><ondown>9002</ondown>'
    nav2 = '<onup>9000</onup><ondown>50</ondown>'
    cells = fw.cell('20', 250, '$VAR[Music_QueueShuffleLabel]', nav1) + fw.cell('26', 249, '$LOCALIZE[595]', nav1)
    cells2 = (fw.cell('21', 250, '$LOCALIZE[190]', nav2, vis='Integer.IsGreater(Container.NumItems,0)') +
              fw.cell('22', 249, '$LOCALIZE[192]', nav2, vis='Integer.IsGreater(Container.NumItems,0)'))
    return (
        '<include name="FGS_Playlist3">'
        '' +
        frame((120, 620, 1800, 1820)) +
        fw.label(144, 120, 470, 60, '[UPPERCASE]$ADDON[skin.aeon.fuse 31017][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        fw.label(644, 120, 700, 60, '[UPPERCASE]$VAR[Music_QueueTitle][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        fw.label(1300, 120, 476, 60, '$VAR[PL_Container_NumItems_Item]$INFO[Container.TotalTime,  ·  ,]', 'st_small_20', '8cffffff', 'right') +
        left + fw.line(120, 820, 500) + fw.line(120, 890, 500) +
        '<control type="grouplist" id="9000"><left>121</left><top>821</top><width>499</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onup>50</onup><ondown>9002</ondown><onleft>noop</onleft><onright>50</onright><onback>50</onback>%s</control>' % cells +
        '<control type="grouplist" id="9002"><left>121</left><top>891</top><width>499</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onup>9000</onup><ondown>50</ondown><onleft>noop</onleft><onright>50</onright><onback>50</onback>%s</control>' % cells2 +
        '<control type="list" id="50"><left>621</left><top>191</top><width>1179</width><height>770</height><orientation>vertical</orientation>'
        '<onup>50</onup><ondown>50</ondown><onleft>9000</onleft><onright>60</onright><pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
        '<viewtype label="535">list</viewtype>'
        '<itemlayout width="1179" height="70">%s</itemlayout><focusedlayout width="1179" height="70">%s</focusedlayout></control>' % (queue_row(False), queue_row(True)) +
        fw.gutter_bar('60', 1801, 192, 768, '50', 'noop') +
        fw.label(645, 191, 1130, 70, '$LOCALIZE[31251]', 'st_ui_24_semibold', '66ffffff', vis='Integer.IsEqual(Container.NumItems,0) + !Container.IsUpdating') +
        '<include>Music_NowPlayingBar</include>'
        '</include>')


# ---------------------------------------------------------------- file browser
def fb_row(focused):
    w = 919
    out = (FOC % (w + 80, '450', w, '450')) if focused else ''
    out += fw.img(0, 69, w, 1, 'common/white.png', '12ffffff')
    out += fw.img(24, 21, 28, 28, 'icons/af3/folder-closed.png', 'fg_mark', 'ListItem.IsFolder')
    out += ('<control type="image"><left>22</left><top>17</top><width>36</width><height>36</height><aspectratio>keep</aspectratio>'
            '<texture background="true">$INFO[ListItem.Icon]</texture><visible>!ListItem.IsFolder</visible></control>')
    out += fw.label(76, 0, 640, 70, '$INFO[ListItem.Label]', 'st_ui_24_semibold', 'ffffffff' if focused else 'd9ffffff')
    out += fw.label(720, 0, 175, 70, '$INFO[ListItem.Label2]', 'st_small_20', '80ffffff', 'right')
    return out


def filebrowser():
    crumbs = ''.join(
        '<control type="button"><width min="40" max="300">auto</width><height>40</height><font>st_small_20_semibold</font><textcolor>%s</textcolor>'
        '<focusedcolor>%s</focusedcolor><disabledcolor>%s</disabledcolor><textoffsetx>16</textoffsetx><aligny>center</aligny><enable>false</enable>'
        '<label>$INFO[Window(Home).Property(aeon.fb.c%d)]</label>'
        '<texturenofocus border="20,0,20,0" colordiffuse="%s">fg/btn56n.png</texturenofocus><texturefocus border="20,0,20,0" colordiffuse="%s">fg/btn56n.png</texturefocus>'
        '<visible>!String.IsEmpty(Window(Home).Property(aeon.fb.c%d))</visible></control>'
        % (('ffffffff', 'ffffffff', 'ffffffff', i, '40ffffff', '40ffffff', i) if False else
           ('b3ffffff', 'b3ffffff', 'b3ffffff', i, '26ffffff', '26ffffff', i)) for i in range(1, 7))
    btn = ('<control type="button" id="%s"><width>299</width><height>70</height><font>uc_st_ui_24_semibold</font><textcolor>ccffffff</textcolor>'
           '<focusedcolor>ffffffff</focusedcolor><disabledcolor>44ffffff</disabledcolor><textoffsetx>24</textoffsetx><aligny>center</aligny>'
           '<label>$LOCALIZE[%s]</label><texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>'
           '<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>%s</control>')
    return (
        '<include name="FGS_FileBrowser3">'
        '<include content="FGS_DlgBack"/>'
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[5][/UPPERCASE]</label></control>'
        '<control type="label" id="411"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor></control>'
        '</control><include>Aeon_ClockBox</include>'
        + frame((120, 1040, 1060, 1820)) +
        # the path as crumbs (Kodi writes 412; the helper splits it)
        '<control type="label" id="412"><visible>false</visible></control>'
        '<control type="grouplist"><left>144</left><top>130</top><width>880</width><height>40</height><orientation>horizontal</orientation><itemgap>10</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords>%s</control>' % crumbs +
        '<control type="list" id="450"><left>121</left><top>191</top><width>919</width><height>770</height><orientation>vertical</orientation>'
        '<onup>450</onup><ondown>450</ondown><onleft>noop</onleft><onright>60</onright><pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
        '<itemlayout width="919" height="70">%s</itemlayout><focusedlayout width="919" height="70">%s</focusedlayout></control>' % (fb_row(False), fb_row(True)) +
        fw.gutter_bar('60', 1041, 192, 768, '450', '9000') +
        # a peek inside the folder in focus
        fw.label(1084, 120, 712, 60, '[UPPERCASE]$INFO[Container(450).ListItem.Label][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff', vis='Container(450).ListItem.IsFolder') +
        '<control type="panel"><left>1084</left><top>210</top><width>712</width><height>420</height><orientation>vertical</orientation>'
        '<itemlayout width="237" height="210"><control type="image"><left>0</left><top>0</top><width>225</width><height>198</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m225x198.png">$INFO[ListItem.Art(thumb)]</texture></control></itemlayout>'
        '<focusedlayout width="237" height="210"><control type="image"><left>0</left><top>0</top><width>225</width><height>198</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m225x198.png">$INFO[ListItem.Art(thumb)]</texture></control></focusedlayout>'
        '<content>plugin://script.aeon.helper/?info=peek&amp;n=$INFO[Window(Home).Property(aeon.peek.stamp)]</content>'
        '<visible>Container(450).ListItem.IsFolder</visible></control>' +
        '<control type="group"><left>1084</left><top>640</top><visible>Container(450).ListItem.IsFolder + !String.IsEmpty(Window(Home).Property(aeon.peek.dirs))</visible>' +
        fw.img(0, 7, 20, 20, 'icons/af3/folder-closed.png', 'b3ffffff') + fw.label(30, 0, 90, 34, '$INFO[Window(Home).Property(aeon.peek.dirs)]', 'st_small_20_semibold', 'ffffffff') +
        fw.img(120, 7, 20, 20, 'icons/af3/file.png', 'b3ffffff') + fw.label(150, 0, 100, 34, '$INFO[Window(Home).Property(aeon.peek.files)]', 'st_small_20_semibold', 'ffffffff') +
        '</control>' +
        fw.line(1060, 680, 760) +
        fw.img(1061, 681, 5, 70, 'common/white.png', 'fg_mark', '!Control.HasFocus(413)') +
        '<control type="grouplist" id="9000"><left>1061</left><top>681</top><width>759</width><height>280</height><orientation>vertical</orientation><itemgap>0</itemgap>'
        '<onleft>60</onleft><onright>noop</onright><onup>9000</onup><ondown>9000</ondown>%s</control>'
        % (((btn % ('413', '186', '')).replace('<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>', '<texturenofocus colordiffuse="24e8b04b">common/white.png</texturenofocus>') + btn % ('415', '119', '<visible>Control.IsEnabled(415)</visible>') + btn % ('414', '222', '')
            + btn % ('416', '749', '<visible>Control.IsEnabled(416)</visible>')).replace('<width>299</width>', '<width>759</width>')) +
        '</include>')


# ---------------------------------------------------------------- text viewer
def textviewer():
    return (
        '<include name="FGS_TextViewer3">'
        '<include content="FGS_DlgBack"/>'
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
                '<control type="label" id="1"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor></control>'
        '</control><include>Aeon_ClockBox</include>'
        + frame((120, 480, 1780, 1800, 1820)) +
        # left: what it is, how long it reads, where you are
        fw.label(144, 120, 320, 60, '[UPPERCASE]$INFO[Control.GetLabel(1)][/UPPERCASE]', 'st_ui_24_bold', 'ffffffff', extra='<scroll>true</scroll>') +
        fw.img(144, 210, 30, 30, 'icons/af3/clock.png', 'fg_mark', '!String.IsEmpty(Window(Home).Property(aeon.tv.mins))') +
        fw.label(186, 200, 278, 50, '$INFO[Window(Home).Property(aeon.tv.mins)] $LOCALIZE[12391]', 'st_ui_28_semibold', 'fg_mark', vis='!String.IsEmpty(Window(Home).Property(aeon.tv.mins))') +
        fw.label(144, 880, 320, 60, '$LOCALIZE[31234]', 'st_small_20', '73ffffff', extra='<wrapmultiline>true</wrapmultiline>') +
        # the text, set for reading
        '<control type="textbox" id="5"><left>640</left><top>220</top><width>980</width><height>720</height><font>st_body_26</font><textcolor>e6ffffff</textcolor>'
        '<pagecontrol>3000</pagecontrol></control>'
        '<control type="scrollbar" id="3000"><left>1781</left><top>192</top><width>19</width><height>768</height>'
        '<texturesliderbackground colordiffuse="0dffffff">common/white.png</texturesliderbackground>'
        '<texturesliderbar colordiffuse="fg_mark">common/white.png</texturesliderbar><texturesliderbarfocus colordiffuse="fg_mark">common/white.png</texturesliderbarfocus>'
        '<orientation>vertical</orientation><showonepage>false</showonepage><onleft>1000</onleft><onright>1000</onright></control>'
        '<control type="button" id="1000"><description>focus holder: up/down page, OK closes, Right the bar</description><left>0</left><top>0</top><width>1</width><height>1</height>'
        '<texturefocus /><texturenofocus /><onup>PageUp(3000)</onup><ondown>PageDown(3000)</ondown><onright>3000</onright><onleft>noop</onleft><onclick>Dialog.Close(textviewer)</onclick></control>'
        '</include>')


# ---------------------------------------------------------------- media source
def ms_path_row(focused):
    w = 919
    out = (FOC % (w + 80, '10', w, '10')) if focused else ''
    out += fw.img(0, 69, w, 1, 'common/white.png', '12ffffff')
    out += fw.label(24, 0, 870, 70, '$INFO[ListItem.Label]', 'st_ui_24_semibold', 'ffffffff' if focused else 'd9ffffff')
    return out


def src_row(focused):
    out = fw.img(0, 69, 359, 1, 'common/white.png', '12ffffff')
    out += fw.img(0, 0, 359, 70, 'common/white.png', '1fe8b04b', '!String.IsEmpty(ListItem.Property(aeon.current))')
    out += fw.img(0, 0, 5, 70, 'common/white.png', 'fg_mark', '!String.IsEmpty(ListItem.Property(aeon.current))')
    out += fw.label(24, 8, 320, 32, '$INFO[ListItem.Label]', 'st_ui_24_semibold', 'ffffffff')
    out += fw.label(24, 38, 320, 26, '$INFO[ListItem.Label2]', 'st_cap_14', '73ffffff')
    return out


def mediasource():
    btn = ('<control type="button" id="%s"><width>299</width><height>70</height><font>uc_st_ui_24_semibold</font><textcolor>ccffffff</textcolor>'
           '<focusedcolor>ffffffff</focusedcolor><disabledcolor>44ffffff</disabledcolor><textoffsetx>24</textoffsetx><aligny>center</aligny>'
           '<label>$LOCALIZE[%s]</label><texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus>'
           '<texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus></control>')
    step = lambda i, x, label, lit: (
        '<control type="group"><left>%d</left><top>109</top>' % x +
        fw.img(22, 23, 36, 36, 'fg/circle.png', 'fg_mark', lit) + fw.img(22, 23, 36, 36, 'fg/circle.png', '26ffffff', '!' + lit) +
        fw.label(22, 23, 36, 36, '$NUMBER[%d]' % i, 'st_ui_22_bold', 'ff000000', 'center', vis=lit) + fw.label(22, 23, 36, 36, '$NUMBER[%d]' % i, 'st_ui_22_bold', 'ffffffff', 'center', vis='!' + lit) +
        fw.label(72, 0, 250, 82, '[UPPERCASE]%s[/UPPERCASE]' % label, 'st_ui_24_bold', 'ffffffff') +
        fw.img(0, 78, 339, 4, 'common/white.png', 'fg_mark', lit) + fw.img(339, 0, 1, 82, 'common/white.png', LINE) + '</control>')
    on_paths = 'ControlGroup(9000).HasFocus() | Control.HasFocus(10)'
    return (
        '<include name="FGS_MediaSource3">'
        '<include content="FGS_DlgBack"/>'
        '<control type="grouplist"><left>60</left><top>44</top><width>1500</width><height>48</height><orientation>horizontal</orientation><itemgap>14</itemgap><usecontrolcoords>true</usecontrolcoords>'
        '<control type="label"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28</font><textcolor>$VAR[Aeon_MenuLeadCol]</textcolor><label>[UPPERCASE]$LOCALIZE[39031][/UPPERCASE]</label></control>'
        '<control type="label" id="2"><width>auto</width><height>48</height><aligny>center</aligny><font>st_ui_28_bold</font><textcolor>ffffffff</textcolor></control>'
        '</control><include>Aeon_ClockBox</include>'
        + frame((120, 480, 1500, 1520, 1820)) +
        # all sources
        fw.label(144, 120, 320, 60, '[UPPERCASE]$LOCALIZE[39031][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
        '<control type="list"><left>121</left><top>191</top><width>359</width><height>770</height><orientation>vertical</orientation>'
        '<itemlayout width="359" height="70">%s</itemlayout><focusedlayout width="359" height="70">%s</focusedlayout>'
        '<content>plugin://script.aeon.helper/?info=sources&amp;media=video&amp;n=$INFO[Window(Home).Property(aeon.ms.name)]</content></control>' % (src_row(False), src_row(True)) +
        # the steps
        step(1, 481, '$LOCALIZE[744]', on_paths) + step(2, 820, '$LOCALIZE[551]', 'Control.HasFocus(12)') + step(3, 1159, '$LOCALIZE[186]', 'ControlGroup(9001).HasFocus()') +
        # the paths get the room
        fw.label(505, 196, 970, 30, '[UPPERCASE]$LOCALIZE[1021][/UPPERCASE]', 'st_cap_14', '73ffffff') +
        '<control type="list" id="10"><left>481</left><top>231</top><width>1019</width><height>490</height><orientation>vertical</orientation>'
        '<onup>10</onup><ondown>12</ondown><onleft>noop</onleft><onright>60</onright><pagecontrol>60</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime>'
        '<itemlayout width="1019" height="70">%s</itemlayout><focusedlayout width="1019" height="70">%s</focusedlayout></control>'
        % (ms_path_row(False).replace('919', '1019'), ms_path_row(True).replace('919', '1019').replace('999', '1099')) +
        fw.gutter_bar('60', 1501, 232, 488, '10', '9000') +
        fw.line(481, 720, 1019) +
        fw.label(505, 726, 400, 30, '[UPPERCASE]$LOCALIZE[551][/UPPERCASE]', 'st_cap_14', '73ffffff') +
        '<control type="edit" id="12"><left>481</left><top>760</top><width>1019</width><height>70</height><font>st_ui_24_semibold</font><textcolor>ddffffff</textcolor>'
        '<focusedcolor>ffffffff</focusedcolor><textoffsetx>24</textoffsetx><aligny>center</aligny>'
        '<texturefocus border="20" colordiffuse="ffffffff">fg/fgs_bar_dk.png</texturefocus><texturenofocus border="0,2,0,0" colordiffuse="12ffffff">fg/fgs_rule_top.png</texturenofocus>'
        '<onup>10</onup><ondown>9001</ondown><onleft>noop</onleft><onright>9000</onright></control>' +
        fw.line(481, 890, 1019) +
        '<control type="grouplist" id="9001"><left>481</left><top>891</top><width>1019</width><height>70</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
        '<usecontrolcoords>true</usecontrolcoords><onup>12</onup><ondown>10</ondown><onleft>noop</onleft><onright>9000</onright>%s</control>'
        % (fw.cell('18', 510, '$LOCALIZE[186]', '<onup>12</onup><ondown>10</ondown>') + fw.cell('19', 509, '$LOCALIZE[222]', '<onup>12</onup><ondown>10</ondown>')) +
        # right: a look inside the path in focus, then the path buttons
        '<control type="panel"><left>1544</left><top>206</top><width>256</width><height>264</height><orientation>vertical</orientation>'
        '<itemlayout width="86" height="132"><control type="image"><left>0</left><top>0</top><width>80</width><height>120</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m80x120.png">$INFO[ListItem.Art(thumb)]</texture></control></itemlayout>'
        '<focusedlayout width="86" height="132"><control type="image"><left>0</left><top>0</top><width>80</width><height>120</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m80x120.png">$INFO[ListItem.Art(thumb)]</texture></control></focusedlayout>'
        '<content>plugin://script.aeon.helper/?info=peek&amp;n=$INFO[Window(Home).Property(aeon.peek.stamp)]</content></control>' +
        fw.label(1544, 476, 256, 30, '$INFO[Window(Home).Property(aeon.peek.count)]', 'st_small_20', '99ffffff') +
        fw.line(1520, 680, 300) +
        '<control type="grouplist" id="9000"><left>1521</left><top>681</top><width>299</width><height>210</height><orientation>vertical</orientation><itemgap>0</itemgap>'
        '<onleft>60</onleft><onright>noop</onright><onup>9000</onup><ondown>9000</ondown>%s</control>'
        % (btn % ('11', '1024') + btn % ('13', '15019') + btn % ('14', '15015')) +
        '</include>')


# ---------------------------------------------------------------- settings: timer column, subtitle cards
TIMER = 'Window.IsActive(pvrtimersetting)'


def timer_column():
    return ('<control type="group"><visible>%s</visible>' % TIMER +
            fw.label(144, 120, 320, 60, '[UPPERCASE]$LOCALIZE[19040][/UPPERCASE]', 'st_ui_28_semibold', 'ffffffff') +
            '<control type="group"><visible>!String.IsEmpty(ListItem.ChannelName)</visible>'
            '<control type="image"><left>144</left><top>220</top><width>160</width><height>90</height><aspectratio align="left">keep</aspectratio>'
            '<texture background="true">$INFO[ListItem.Icon]</texture></control>' +
            '<control type="textbox"><left>144</left><top>330</top><width>312</width><height>120</height><font>st_ui_30_semibold</font><textcolor>ffffffff</textcolor>'
            '<label>$INFO[ListItem.Title]$INFO[ListItem.Label]</label></control>' +
            '<control type="textbox"><left>144</left><top>460</top><width>312</width><height>180</height><font>st_small_20</font><textcolor>bfffffff</textcolor>'
            '<label>$INFO[ListItem.ChannelName,[B],[/B][CR]]$INFO[ListItem.Date,,[CR]]$INFO[ListItem.StartTime,[COLOR fg_mark],[/COLOR]]$INFO[ListItem.EndTime, – [COLOR fg_mark],[/COLOR]]</label></control>' +
            '<control type="progress"><left>144</left><top>660</top><width>312</width><height>10</height><texturebg border="2,0,2,0" colordiffuse="1affffff">fg/pillh.png</texturebg>'
            '<midtexture border="2,0,2,0" colordiffuse="fg_mark">fg/pillh.png</midtexture><info>ListItem.Progress</info></control></control>' +
            '</control>')


def sub_card(focused):
    out = ''
    if focused:
        out += ('<control type="image"><left>-30</left><top>-24</top><width>290</width><height>122</height>%s<visible>Control.HasFocus(9310) + $EXP[FGS_ShadowOn]</visible></control>' % fw.SHADOW)
    out += fw.img(0, 0, 230, 74, 'fg/r12.png', '0dffffff').replace('<texture colordiffuse', '<texture border="12" colordiffuse')
    out += fw.img(0, 0, 230, 74, 'fg/r12.png', '66000000', '!String.IsEmpty(ListItem.Property(aeon.current))').replace('<texture colordiffuse', '<texture border="12" colordiffuse')
    out += fw.img(0, 0, 230, 74, 'fg/e12.png', 'ccffffff', '!String.IsEmpty(ListItem.Property(aeon.current))').replace('<texture colordiffuse', '<texture border="12" colordiffuse')
    out += ('<control type="image"><left>14</left><top>17</top><width>40</width><height>40</height><aspectratio>scale</aspectratio>'
            '<texture background="true">$INFO[ListItem.Property(code),resource://resource.images.languageflags.rounded/,.png]</texture></control>')
    out += fw.label(66, 10, 156, 30, '$INFO[ListItem.Label]', 'st_ui_22_semibold', 'ffffffff')
    out += fw.label(66, 40, 156, 24, '$INFO[ListItem.Label2]', 'st_cap_14', '80ffffff')
    if focused:
        out += fw.img(-3, -3, 236, 80, 'fg/ring12.png', 'ffffffff', 'Control.HasFocus(9310)').replace('<texture colordiffuse', '<texture border="15" colordiffuse')
    return out


def sub_cards():
    s = 'Window.IsActive(osdsubtitlesettings)'
    return ('<control type="group"><visible>%s</visible>' % s +
            fw.label(1065, 196, 711, 30, '[UPPERCASE]$LOCALIZE[287][/UPPERCASE]', 'st_cap_14', '80ffffff') +
            fw.label(1500, 196, 276, 30, '$INFO[Container(9310).NumItems]', 'st_cap_14', 'fg_mark', 'right') +
            '<control type="panel" id="9310"><left>1065</left><top>230</top><width>735</width><height>206</height><orientation>vertical</orientation>'
            '<onup>9102</onup><ondown>5</ondown><onleft>noop</onleft><onright>noop</onright><scrolltime tween="cubic" easing="out">200</scrolltime>'
            '<onclick>RunScript(script.aeon.helper,setsub,$INFO[Container(9310).ListItem.Property(index)])</onclick>'
            '<itemlayout width="242" height="103">%s</itemlayout><focusedlayout width="242" height="103">%s</focusedlayout>'
            '<content>plugin://script.aeon.helper/?info=substreams&amp;s=$INFO[VideoPlayer.SubtitlesLanguage]</content></control>' % (sub_card(False), sub_card(True)) +
            '</control>')


def settings():
    """the round-3 parts into the two settings pages (fgssettingsdlg wrote them)"""
    p = fw.FILE
    s = io.open(p, encoding='utf-8').read()
    # the timer column in the centred dialog: the timer dialog uses the profile geometry
    a = s.index('<include name="FGS_SettingsCentred">')
    e = s.index('</include>', s.index('<include name="FGS_SetArea_Profile">') - 20)
    seg = s[a:e]
    if 'pvrtimersetting' not in seg:
        seg = seg.replace('<include condition="Window.IsActive(profilesettings)">FGS_SetArea_Profile</include><include condition="!Window.IsActive(profilesettings)">FGS_SetArea_Wide</include>',
                          '<include condition="Window.IsActive(profilesettings) | %s">FGS_SetArea_Profile</include><include condition="!Window.IsActive(profilesettings) + !%s">FGS_SetArea_Wide</include>' % (TIMER, TIMER))
        seg = seg.replace('<visible>Window.IsActive(profilesettings)</visible></control>', '<visible>Window.IsActive(profilesettings) | %s</visible></control>' % TIMER, 1)
        seg = seg.replace('<visible>!Window.IsActive(profilesettings)</visible>', '<visible>!Window.IsActive(profilesettings) + !%s</visible>' % TIMER)
        seg = seg.replace('<visible>Window.IsActive(profilesettings)</visible><control type="label"><left>505</left>', '<visible>Window.IsActive(profilesettings) | %s</visible><control type="label"><left>505</left>' % TIMER)
        s = s[:a] + seg + s[e:]
    # the timer column goes over the page's background (after the clock); an earlier run put it first, under it
    a = s.index('<include name="FGS_SettingsCentred">')
    col = timer_column()
    head = '<include name="FGS_SettingsCentred">' + col
    if s.startswith(head, a):
        s = s[:a] + '<include name="FGS_SettingsCentred">' + s[a + len(head):]
    if col not in s[a:s.index('<include name="FGS_SetArea_Profile">')]:
        k = s.index('<include>Aeon_ClockBox</include>', a) + len('<include>Aeon_ClockBox</include>')
        s = s[:k] + col + s[k:]
    # the subtitle cards in the side panel: above the offset card on the subtitle tab
    if 'id="9310"' in s:            # the cards block from an earlier run: out, then in again as it is now
        i = s.index('<control type="group"><visible>Window.IsActive(osdsubtitlesettings)</visible>')
        j = s.index('<control type="grouplist" id="5">', i)
        s = s[:i] + s[j:]
    if 'id="9310"' not in s:
        k = s.index('<include name="FGS_SettingsPanel">')
        m = s.index('<control type="grouplist" id="5">', k)
        s = s[:m] + sub_cards() + s[m:]
        k = s.index('<include name="FGS_SettingsPanel">')
        card = '<control type="group"><visible>Window.IsActive(osdaudiosettings) | Window.IsActive(osdsubtitlesettings)</visible><control type="image"><left>1041</left><top>192</top>'
        i = s.find(card, k)
        if i >= 0:                  # the first run only: the offset card to the audio tab
            s = s[:i] + card.replace('Window.IsActive(osdaudiosettings) | Window.IsActive(osdsubtitlesettings)', 'Window.IsActive(osdaudiosettings)') + s[i + len(card):]
        s = s.replace('<onup condition="Window.IsActive(osdsubtitlesettings)">9102</onup>', '<onup condition="Window.IsActive(osdsubtitlesettings)">9310</onup>', 1)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def main():
    from PIL import Image, ImageDraw
    for w, h, r in ((48, 48, 6), (225, 198, 10), (80, 120, 6)):
        f = os.path.join(fw.SKIN, 'media', 'fg', 'm%dx%d.png' % (w, h))
        if not os.path.exists(f):
            im = Image.new('RGBA', (w, h), (255, 255, 255, 0))
            ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=(255, 255, 255, 255))
            im.save(f)
    fw.put('Round3', playlist() + filebrowser() + textviewer() + mediasource())
    swap('MyPlaylist.xml', 'FGS_Playlist', 'FGS_Playlist3')
    swap('FileBrowser.xml', 'FGS_FileBrowser', 'FGS_FileBrowser3')
    swap('DialogTextViewer.xml', 'FGS_TextViewer', 'FGS_TextViewer3')
    swap('DialogMediaSource.xml', 'FGS_MediaSource', 'FGS_MediaSource3')
    settings()
    print('fgs round 3: pages written')


if __name__ == '__main__':
    main()
