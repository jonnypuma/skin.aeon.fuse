# -*- coding: utf-8 -*-
"""0.56.53 Files in the Fused Glass style (canvas round 4, idea A: "A is the more user-friendly", "go ahead").
The plain list 50 that Videos > Files, Music > Files, folders inside a source and untyped add-on folders fall back to
(the Fused Glass library views only cover typed content) gets the page spec:
- frame 120-1820 x 108-960; title band: the path as crumbs (helper aeon.f50.c1-4 after the window's name and Files),
  the count at the right; Music adds Albums / Artists / Songs / Genres as cells in the band (Files lit);
- a 70 px row per item 121-1499: Kodi's icon, the name, the kind as a tag (NFS, SMB, ADD-ONS, …), label2 at the right;
  "Add videos… / Add music…" in the accent; the style's bar and focus shadow; bar 5960 in the gutter 1500-1520;
- the right column 1521-1820: a peek inside the folder in focus (helper ?info=peek) and what it holds.
The page is the windows' top layer while list 50 shows (its own ground, header and clock), so the older music header,
card and art box stay underneath. Navigation as before: Up to the window's menu (9000), Left / Right the Library panel.
Run after the view generators. Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

LINE = fw.LINE
KINDS = (('nfs://', 'NFS'), ('smb://', 'SMB'), ('addons://', 'ADD-ONS'), ('upnp://', 'UPNP'), ('dav://', 'WEBDAV'), ('davs://', 'WEBDAV'),
         ('ftp://', 'FTP'), ('sftp://', 'SFTP'), ('plugin://', 'ADD-ON'), ('zip://', 'ZIP'), ('rar://', 'RAR'))


def row(focused):
    w = 1379
    out = ''
    if focused:
        out += ('<control type="image"><left>-40</left><top>-34</top><width>%d</width><height>150</height>%s<visible>Control.HasFocus(50) + $EXP[FGS_ShadowOn]</visible></control>'
                '<control type="image"><left>0</left><top>0</top><width>%d</width><height>70</height>%s<visible>Control.HasFocus(50)</visible></control>'
                % (w + 80, fw.SHADOW, w, fw.BAR))
    out += fw.img(0, 69, w, 1, 'common/white.png', '12ffffff')
    out += fw.img(24, 15, 40, 40, 'common/white.png', '12ffffff').replace('<texture colordiffuse', '<texture border="10" colordiffuse')
    net = '[String.StartsWith(ListItem.FolderPath,nfs://) | String.StartsWith(ListItem.FolderPath,smb://) | String.StartsWith(ListItem.FolderPath,upnp://) | String.StartsWith(ListItem.FolderPath,dav://) | String.StartsWith(ListItem.FolderPath,davs://) | String.StartsWith(ListItem.FolderPath,ftp://) | String.StartsWith(ListItem.FolderPath,sftp://)]'
    addon = '[String.StartsWith(ListItem.FolderPath,addons://) | String.StartsWith(ListItem.FolderPath,plugin://)]'
    addrow = 'String.EndsWith(ListItem.Label,...)'
    icon = '<control type="image"><left>32</left><top>23</top><width>24</width><height>24</height><aspectratio>keep</aspectratio><texture colordiffuse="%s">%s</texture><visible>%s</visible></control>'
    out += icon % ('fg_mark', 'icons/af3/plus.png', addrow)
    out += icon % ('d9ffffff', 'icons/af3/network-wired.png', '!%s + %s' % (addrow, net))
    out += icon % ('d9ffffff', 'icons/af3/puzzle-piece.png', '!%s + %s' % (addrow, addon))
    out += icon % ('d9ffffff', 'icons/af3/folder-closed.png', '!%s + !%s + !%s + ListItem.IsFolder' % (addrow, net, addon))
    out += ('<control type="image"><left>30</left><top>21</top><width>28</width><height>28</height><aspectratio>keep</aspectratio>'
            '<texture background="true" colordiffuse="d9ffffff">$INFO[ListItem.Icon]</texture><visible>!ListItem.IsFolder + !%s</visible></control>' % addrow)
    add = 'String.StartsWith(ListItem.FolderPath,add://) | String.Contains(ListItem.Label,...)'
    ink = 'ffffffff' if focused else 'd9ffffff'
    out += fw.label(84, 0, 960, 70, '$INFO[ListItem.Label]', 'st_ui_24_semibold', ink, vis='!String.EndsWith(ListItem.Label,...)')
    out += fw.label(84, 0, 960, 70, '$INFO[ListItem.Label]', 'st_ui_24_semibold', 'fg_mark', vis='String.EndsWith(ListItem.Label,...)')
    for prefix, tag in KINDS:
        vis = 'String.StartsWith(ListItem.FolderPath,%s)' % prefix
        out += fw.img(1060, 21, 92, 28, 'fg/e8.png', '66ffffff', vis).replace('<texture colordiffuse', '<texture border="8" colordiffuse')
        out += fw.label(1060, 21, 92, 28, tag, 'st_cap_14', 'b3ffffff', 'center', vis=vis)
    out += fw.label(1160, 0, 195, 70, '$INFO[ListItem.Label2]', 'st_small_20', '80ffffff', 'right')
    return out


def page(music):
    lead = '$LOCALIZE[2]' if music else '$LOCALIZE[3]'
    crumbs = ''.join(
        '<control type="label"><width>auto</width><height>40</height><aligny>center</aligny><font>st_small_20</font><textcolor>59ffffff</textcolor><label>›</label>'
        '<visible>!String.IsEmpty(Window(Home).Property(aeon.f50.c%d))</visible></control>'
        '<control type="label"><width max="300">auto</width><height>40</height><aligny>center</aligny><font>st_small_20_semibold</font><textcolor>%s</textcolor>'
        '<label>$INFO[Window(Home).Property(aeon.f50.c%d)]</label><visible>!String.IsEmpty(Window(Home).Property(aeon.f50.c%d))</visible></control>'
        % (i, 'ffffffff' if i == 4 else 'b3ffffff', i, i) for i in range(1, 5))
    band = ('<control type="grouplist"><left>144</left><top>130</top><width>1100</width><height>40</height><orientation>horizontal</orientation><itemgap>12</itemgap>'
            '<usecontrolcoords>true</usecontrolcoords>'
            '<control type="label"><width>auto</width><height>40</height><aligny>center</aligny><font>st_small_20_semibold</font><textcolor>b3ffffff</textcolor><label>%s</label></control>'
            '<control type="label"><width>auto</width><height>40</height><aligny>center</aligny><font>st_small_20</font><textcolor>59ffffff</textcolor><label>›</label></control>'
            '<control type="label"><width>auto</width><height>40</height><aligny>center</aligny><font>st_small_20_semibold</font><textcolor>ffffffff</textcolor><label>$LOCALIZE[744]</label></control>'
            '%s</control>' % (lead, crumbs))
    if music:
        tabs = (('$LOCALIZE[132]', 'ActivateWindow(Music,musicdb://albums/,return)'), ('$LOCALIZE[133]', 'ActivateWindow(Music,musicdb://artists/,return)'),
                ('$LOCALIZE[134]', 'ActivateWindow(Music,musicdb://songs/,return)'), ('$LOCALIZE[135]', 'ActivateWindow(Music,musicdb://genres/,return)'))
        cells = ''.join(fw.cell(str(9851 + k), 170, lab, '<onup>noop</onup><ondown>50</ondown>', (act,), font='st_cap_16') for k, (lab, act) in enumerate(tabs))
        band = ('<control type="grouplist" id="9850"><left>121</left><top>109</top><width>700</width><height>82</height><orientation>horizontal</orientation><itemgap>0</itemgap>'
                '<usecontrolcoords>true</usecontrolcoords><onleft>noop</onleft><onright>noop</onright><onup>noop</onup><ondown>50</ondown>%s</control>' % cells.replace('<height>70</height>', '<height>82</height>').replace('<height>150</height>', '<height>162</height>') +
                band.replace('<left>144</left><top>130</top><width>1100</width>', '<left>844</left><top>130</top><width>620</width>'))
    return (
        '<control type="group"><visible>Control.IsVisible(50)</visible><include>Anim_FadeVisible</include>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><texture colordiffuse="ff0b0d11">common/white.png</texture></control>'
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><fadetime>400</fadetime>'
        '<texture background="true" colordiffuse="40ffffff">$INFO[Container(50).ListItem.Art(fanart)]</texture></control>'
        + fw.img(0, 0, 1920, 1080, 'fg/fgs_vi_l.png') +
        fw.header(lead, '$LOCALIZE[744]') +
        fw.line(120, 108, 1701) + fw.line(120, 960, 1701) + fw.line(121, 191, 1699) +
        ''.join(fw.line(x, 108, 1, 852) for x in (120, 1500, 1520, 1820)) +
        band +
        fw.label(1300, 120, 176, 60, '$INFO[Container.NumItems]', 'st_small_20', '8cffffff', 'right') +
        '<control type="list" id="50"><left>121</left><top>191</top><width>1379</width><height>770</height><orientation>vertical</orientation>'
        '<onup>%s</onup><ondown>50</ondown>'
        '<onleft condition="!Skin.HasSetting(aeon.kiosk)">ActivateWindow(1160)</onleft><onright>5960</onright>'
        '<pagecontrol>5960</pagecontrol><scrolltime tween="cubic" easing="out">200</scrolltime><viewtype label="535">list</viewtype>'
        '<itemlayout width="1379" height="70">%s</itemlayout><focusedlayout width="1379" height="70">%s</focusedlayout></control>'
        % ('9850' if music else '9000', row(False), row(True)) +
        fw.gutter_bar('5960', 1501, 192, 768, '50', 'noop') +
        # the peek
        fw.label(1544, 120, 256, 60, '[UPPERCASE]$INFO[Container(50).ListItem.Label][/UPPERCASE]', 'st_ui_24_bold', 'ffffffff', extra='<scroll>true</scroll>') +
        '<control type="panel"><left>1544</left><top>206</top><width>264</width><height>396</height><orientation>vertical</orientation>'
        '<itemlayout width="88" height="132"><control type="image"><left>0</left><top>0</top><width>80</width><height>120</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m80x120.png">$INFO[ListItem.Art(thumb)]</texture></control></itemlayout>'
        '<focusedlayout width="88" height="132"><control type="image"><left>0</left><top>0</top><width>80</width><height>120</height><aspectratio scalediffuse="false">scale</aspectratio>'
        '<texture background="true" diffuse="fg/m80x120.png">$INFO[ListItem.Art(thumb)]</texture></control></focusedlayout>'
        '<content>plugin://script.aeon.helper/?info=peek&amp;n=$INFO[Window(Home).Property(aeon.peek.stamp)]</content>'
        '<visible>!String.IsEmpty(Window(Home).Property(aeon.peek.path))</visible></control>' +
        '<control type="group"><left>1544</left><top>612</top><visible>!String.IsEmpty(Window(Home).Property(aeon.peek.dirs))</visible>' +
        fw.img(0, 7, 20, 20, 'icons/af3/folder-closed.png', 'b3ffffff') + fw.label(30, 0, 90, 34, '$INFO[Window(Home).Property(aeon.peek.dirs)]', 'st_small_20_semibold', 'ffffffff') +
        fw.img(120, 7, 20, 20, 'icons/af3/file.png', 'b3ffffff') + fw.label(150, 0, 100, 34, '$INFO[Window(Home).Property(aeon.peek.files)]', 'st_small_20_semibold', 'ffffffff') +
        '</control>' +
        ''.join(fw.label(1544, 648, 256, 34, '[UPPERCASE]%s[/UPPERCASE]' % tag, 'st_cap_14', 'fg_mark', vis='String.StartsWith(Container(50).ListItem.FolderPath,%s)' % prefix) for prefix, tag in KINDS) +
        fw.label(1544, 880, 256, 70, '$LOCALIZE[31234]', 'st_small_20', '59ffffff', vis='false') +
        '</control>')


def wire(window, old, name, end_marker='</controls>'):
    p = os.path.join(fw.D, window)
    s = io.open(p, encoding='utf-8').read()
    changed = False
    if '<include condition="!$EXP[FGS]">%s</include>' % old not in s and old:
        a = '<include>%s</include>' % old
        if a in s:
            s = s.replace(a, '<include condition="!$EXP[FGS]">%s</include>' % old, 1)
            changed = True
    if '>%s</include>' % name not in s:
        k = s.rindex(end_marker)
        s = s[:k] + '\t<include condition="$EXP[FGS]">%s</include><!-- 0.56.53 fgsfiles: the top layer -->\n\t' % name + s[k:]
        changed = True
    if changed:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def main():
    fw.put('Files50', '<include name="FGS_Files50_Video">%s</include><include name="FGS_Files50_Music">%s</include>' % (page(False), page(True)))
    # videos: view 50 sits in VidView_Window (Includes_Views_Video.xml)
    p = os.path.join(fw.D, 'Includes_Views_Video.xml')
    s = io.open(p, encoding='utf-8').read()
    a = '\t\t<include>VidView_50_List</include>'
    if a in s:
        s = s.replace(a, '\t\t<include condition="!$EXP[FGS]">VidView_50_List</include>', 1)
        io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    wire('MyVideoNav.xml', '', 'FGS_Files50_Video')
    wire('MyMusicNav.xml', 'Music_View_50', 'FGS_Files50_Music')
    print('fgs files: Videos / Music Files pages written')


if __name__ == '__main__':
    main()
