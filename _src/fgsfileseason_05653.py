# -*- coding: utf-8 -*-
"""0.56.53 the player information's File and season page (Up on the OSD seek bar, then Down from the Overview) in the
Fused Glass style (canvas round 6 board FileSeason6, "good to go"): on the fanart with the faded gradient, the show's logo
and the episode in the title band, at the left the file as a spec sheet (picture as chips, every sound stream as a row
with its flag and the one playing marked, the subtitles as round flags with the one showing ringed in gold, the file,
size, length, the screen and the decoder), at the right the season (thumb, title, length, a tick when watched, a gold
bar under the one playing, the focused row white, OK plays). Films: the poster takes the season's column.

Today's page 2 moves unchanged into FG_FullInfoPage2_Classic (every other theme / style); ids 9502 (season list) and 9503
(films' focus, outside the page) keep their jobs. Lists: helper ?info=audiostreams (0.3.121) and ?info=substreams.
Run AFTER _src/fg_fullinfo.py (it rewrites the FG_FULLINFO block). Repeatable."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fgswin_05653 as fw  # noqa: E402

P = os.path.join(fw.D, 'Includes_FusedPlayer.xml')
FLAG = '$INFO[ListItem.Property(code),resource://resource.images.languageflags.rounded/,.png]'
ONUP = ('<onup>ClearProperty(fgpage,fullscreeninfo)</onup><onup condition="Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)">SetFocus(9504)</onup>'
        '<onup condition="![Skin.HasSetting(aeon.osd.castphotos) + Integer.IsGreater(Container(9504).NumItems,0)]">SetFocus(999)</onup>')
CAP = 'st_cap_14'


def cap(x, y, w, text, vis=''):
    return fw.label(x, y, w, 24, '[UPPERCASE]%s[/UPPERCASE]' % text, CAP, '80ffffff', vis=vis)


def chip(text, vis, gold=False):
    return ('<control type="button"><width min="40" max="400">auto</width><height>34</height><label>[UPPERCASE]%s[/UPPERCASE]</label>'
            '<font>st_small_20_bold</font><textoffsetx>12</textoffsetx><aligny>center</aligny><textcolor>%s</textcolor><disabledcolor>%s</disabledcolor>'
            '<texturenofocus border="8" colordiffuse="%s">fg/e8.png</texturenofocus><texturefocus /><enable>false</enable><visible>%s</visible></control>'
            % (text, 'fg_mark' if gold else 'ffffffff', 'fg_mark' if gold else 'ffffffff', 'ffe8b04b' if gold else '4dffffff', vis))


def audio_row(focused):
    return ('<control type="image"><left>0</left><top>2</top><width>860</width><height>52</height><texture border="12" colordiffuse="1affffff">fg/r12.png</texture><visible>String.IsEqual(ListItem.Property(aeon.current),1)</visible></control>'
            '<control type="image"><left>14</left><top>11</top><width>34</width><height>34</height><aspectratio>keep</aspectratio><texture background="true">%s</texture></control>'
            % FLAG +
            fw.label(64, 2, 200, 52, '$INFO[ListItem.Label]', 'st_ui_22_bold', 'ffffffff', extra='<scroll>false</scroll>') +
            fw.label(270, 2, 440, 52, '$INFO[ListItem.Label2]', 'st_small_20', 'a6ffffff') +
            fw.label(700, 2, 140, 52, '[UPPERCASE]$LOCALIZE[31017][/UPPERCASE]', CAP, 'fg_mark', 'right', 'String.IsEqual(ListItem.Property(aeon.current),1)'))


def sub_flag():
    return ('<control type="image"><left>0</left><top>0</top><width>38</width><height>38</height><texture colordiffuse="fg_mark">fg/circle.png</texture><visible>String.IsEqual(ListItem.Property(aeon.current),1)</visible></control>'
            '<control type="image"><left>3</left><top>3</top><width>32</width><height>32</height><aspectratio>keep</aspectratio><texture background="true">%s</texture></control>' % FLAG)


def ep_row(focused):
    f = 'Control.HasFocus(9502)'
    on = ('<visible>%s</visible>' % f) if focused else ''
    ink_f, ink = 'ff0b0d11', 'ffffffff'
    out = ('<control type="image"><left>0</left><top>4</top><width>760</width><height>112</height><texture border="16" colordiffuse="1affffff">fg/r16.png</texture><visible>ListItem.IsPlaying%s</visible></control>'
           % (' + !' + f if focused else ''))
    if focused:
        out += '<control type="image"><left>0</left><top>4</top><width>760</width><height>112</height><texture border="16" colordiffuse="ffffffff">fg/r16.png</texture>%s</control>' % on
    out += ('<control type="image"><left>14</left><top>15</top><width>160</width><height>90</height><aspectratio scalediffuse="false">scale</aspectratio>'
            '<texture background="true" diffuse="fg/m128x72.png">$INFO[ListItem.Art(thumb)]</texture></control>'
            '<control type="image"><left>14</left><top>100</top><width>70</width><height>5</height><texture colordiffuse="fg_mark">common/white.png</texture><visible>ListItem.IsPlaying</visible></control>'
            '<control type="image"><left>144</left><top>21</top><width>24</width><height>24</height><texture colordiffuse="a6000000">fg/circle.png</texture><visible>Integer.IsGreater(ListItem.PlayCount,0)</visible></control>'
            '<control type="label"><left>144</left><top>21</top><width>24</width><height>24</height><align>center</align><aligny>center</aligny><font>st_small_20_bold</font><textcolor>ffffffff</textcolor><label>✓</label><visible>Integer.IsGreater(ListItem.PlayCount,0)</visible></control>')
    for col, vis in ((ink, ('!' + f) if focused else ''), (ink_f, f if focused else 'false')):
        if vis == 'false':
            continue
        out += fw.label(194, 22, 420, 36, '$INFO[ListItem.Episode,E, · ]$INFO[ListItem.Title]', 'st_ui_22_bold', col, vis=vis, extra='<scroll>false</scroll>')
        out += fw.label(194, 60, 420, 32, '$INFO[ListItem.Duration(mins),, min]', 'st_small_20', col.replace('ff', 'b3', 1), vis=vis)
        out += fw.label(600, 22, 140, 76, '[UPPERCASE]$LOCALIZE[31017][/UPPERCASE]', CAP, 'fg_mark' if col == ink else ink_f, 'right', 'ListItem.IsPlaying' + ((' + ' + vis) if vis else ''))
    return out


def page():
    fan = '$VAR[FGS_FSFanart]'
    return (
        '<include name="FGS_FileSeason"><control type="group"><visible>String.IsEqual(Window(fullscreeninfo).Property(fgpage),2)</visible>'
        '<animation type="Visible" condition="!Skin.HasSetting(aeon.reducemotion)"><effect type="fade" start="0" end="100" time="200"/></animation>'
        + fw.img(0, 0, 1920, 1080, 'common/white.png', 'ff000000') +
        '<control type="image"><left>0</left><top>0</top><width>1920</width><height>1080</height><aspectratio>scale</aspectratio><texture background="true">%s</texture></control>' % fan +
        fw.img(0, 0, 1920, 1080, 'fg/fgs_vi_l.png') + fw.img(0, 0, 1920, 1080, 'fg/fgs_vi_l.png') + fw.img(0, 0, 1920, 1080, 'fg/fgs_vi_b.png') +
        # title band: the logo, the kick and the title, the clock
        '<control type="image"><left>120</left><top>40</top><width>360</width><height>68</height><aspectratio align="left">keep</aspectratio><texture background="true">$VAR[FGS_FSLogo]</texture></control>'
        + fw.label(510, 40, 1000, 26, '[UPPERCASE]$VAR[FG_OSDKick][/UPPERCASE]', CAP, '80ffffff') +
        fw.label(510, 66, 1000, 44, '$INFO[Player.Title]', 'st_ui_28_bold', 'ffffffff', extra='<scroll>false</scroll>') +
        '<include>Aeon_ClockBox</include>' + fw.line(120, 132, 1700) +
        # left: the file as a spec sheet
        cap(120, 160, 860, '$LOCALIZE[291]') +
        '<control type="grouplist"><left>120</left><top>194</top><width>860</width><height>34</height><orientation>horizontal</orientation><itemgap>10</itemgap>'
        + chip('$VAR[FG_ChipHDR]', '!String.IsEmpty(VideoPlayer.HdrType)', True) +
        chip('$INFO[VideoPlayer.VideoResolution]', '!String.IsEmpty(VideoPlayer.VideoResolution)') +
        chip('$INFO[VideoPlayer.VideoCodec]', '!String.IsEmpty(VideoPlayer.VideoCodec)') +
        chip('$INFO[VideoPlayer.VideoAspect,, : 1]', '!String.IsEmpty(VideoPlayer.VideoAspect)') +
        '<control type="label"><width max="420">auto</width><height>34</height><aligny>center</aligny><font>st_small_20</font><textcolor>b3ffffff</textcolor>'
        '<label>$INFO[Window(Home).Property(aeon.pf.mi.format),  ,]$INFO[Window(Home).Property(aeon.pf.mi.bitrate),  ·  ,]</label></control></control>' +
        cap(120, 254, 860, '$LOCALIZE[292]$INFO[Window(Home).Property(aeon.pf.audiocount), · ,]') +
        '<control type="list" id="9520"><left>120</left><top>286</top><width>860</width><height>168</height><orientation>vertical</orientation>'
        '<content>plugin://script.aeon.helper/?info=audiostreams&amp;a=$INFO[VideoPlayer.AudioLanguage]$INFO[VideoPlayer.AudioCodec]</content>'
        '<itemlayout width="860" height="56">%s</itemlayout><focusedlayout width="860" height="56">%s</focusedlayout></control>' % (audio_row(False), audio_row(False)) +
        '<control type="group">'
        '<animation effect="slide" end="0,-56" time="0" condition="String.IsEqual(Window(Home).Property(aeon.pf.audiocount),2)">Conditional</animation>'
        '<animation effect="slide" end="0,-112" time="0" condition="String.IsEqual(Window(Home).Property(aeon.pf.audiocount),1)">Conditional</animation>' +
        cap(120, 474, 860, '$LOCALIZE[287]$INFO[Window(Home).Property(aeon.pf.subcount), · ,]$INFO[VideoPlayer.SubtitlesLanguage, · ,]') +
        '<control type="list" id="9521"><left>120</left><top>506</top><width>748</width><height>38</height><orientation>horizontal</orientation>'
        '<content>plugin://script.aeon.helper/?info=substreams&amp;s=$INFO[VideoPlayer.SubtitlesLanguage]</content>'
        '<itemlayout width="44" height="38">%s</itemlayout><focusedlayout width="44" height="38">%s</focusedlayout></control>' % (sub_flag(), sub_flag()) +
        fw.label(876, 506, 104, 38, '$INFO[Window(Home).Property(aeon.pf.submore)]', 'st_small_20_bold', '99ffffff') +
        cap(120, 572, 860, '$ADDON[skin.aeon.fuse 32482]') +
        '<control type="textbox"><left>120</left><top>604</top><width>860</width><height>64</height><font>st_ui_22_semibold</font><textcolor>ffffffff</textcolor>'
        '<label>$INFO[Window(Home).Property(aeon.pf.file)]</label></control>' +
        fw.label(120, 676, 860, 34, '$INFO[Window(Home).Property(aeon.pf.size),[B],[/B] [COLOR 99ffffff][LOWERCASE]$LOCALIZE[289][/LOWERCASE][/COLOR]     ]$INFO[VideoPlayer.Duration,[B],[/B] [COLOR 99ffffff][LOWERCASE]$LOCALIZE[180][/LOWERCASE][/COLOR]     ]$INFO[Window(Home).Property(aeon.pf.mi.format),[B],[/B] [COLOR 99ffffff][LOWERCASE]$LOCALIZE[21870][/LOWERCASE][/COLOR]]', 'st_small_20', 'ffffffff') +
        fw.line(120, 732, 860) +
        cap(120, 752, 400, '$ADDON[skin.aeon.fuse 32484]') +
        fw.label(120, 780, 400, 34, '$INFO[System.ScreenResolution]', 'st_ui_22_bold', 'ffffffff') +
        cap(560, 752, 420, '$LOCALIZE[14200]') +
        fw.label(560, 780, 420, 34, '$INFO[Player.Process(videodecoder)]$INFO[Player.Process(videofps),  ·  , fps]', 'st_ui_22_bold', 'ffffffff') +
        '</control>' +
        # right: the season (episodes) or the poster (films)
        '<control type="group"><visible>!String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))</visible>'
        + cap(1060, 160, 760, '$LOCALIZE[20373] $INFO[VideoPlayer.Season]$INFO[Container(9502).NumItems, · , $LOCALIZE[20360]]') +
        '<control type="list" id="9502"><left>1060</left><top>190</top><width>760</width><height>720</height><orientation>vertical</orientation><preloaditems>1</preloaditems>'
        '<scrolltime tween="cubic" easing="out">200</scrolltime>%s<onleft>noop</onleft><onright>noop</onright><ondown>noop</ondown>'
        '<content target="videos">$VAR[FG_InfoSeasonPath]</content>'
        '<itemlayout width="760" height="120">%s</itemlayout><focusedlayout width="760" height="120">%s</focusedlayout></control></control>' % (ONUP, ep_row(False), ep_row(True)) +
        '<control type="group"><visible>String.IsEmpty(Window(Home).Property(aeon.pf.seasonpath))</visible>'
        '<control type="image"><left>1360</left><top>160</top><width>460</width><height>690</height><aspectratio aligny="top" align="right">keep</aspectratio><texture background="true">$INFO[Player.Art(poster)]</texture></control>'
        '</control>' +
        # foot: where in the episode / film
        fw.label(120, 990, 160, 40, '$INFO[Player.Time]', 'st_small_20', 'ccffffff') +
        '<control type="progress"><left>290</left><top>1008</top><width>1180</width><height>4</height><info>Player.Progress</info>'
        '<texturebg border="2" colordiffuse="33ffffff">fg/pill4.png</texturebg><lefttexture /><midtexture border="2" colordiffuse="fg_mark">fg/pill4.png</midtexture><righttexture /></control>'
        + fw.label(1480, 990, 340, 40, '$INFO[Player.TimeRemaining,-,]$INFO[Player.FinishTime,  ·  $LOCALIZE[31030] ,]', 'st_small_20', 'ccffffff', 'right') +
        '</control></include>'
        '<variable name="FGS_FSFanart"><value condition="!String.IsEmpty(Player.Art(tvshow.fanart))">$INFO[Player.Art(tvshow.fanart)]</value><value>$INFO[Player.Art(fanart)]</value></variable>'
        '<variable name="FGS_FSLogo"><value condition="!String.IsEmpty(Player.Art(tvshow.clearlogo))">$INFO[Player.Art(tvshow.clearlogo)]</value><value>$INFO[Player.Art(clearlogo)]</value></variable>')


def patch():
    s = io.open(P, encoding='utf-8').read()
    if 'FG_FullInfoPage2_Classic' in s:
        return
    a = s.index('\t\t\t<!-- second page: file and season -->\n')
    e = s.index('<!-- FG_FULLINFO:end -->')
    tail = '\t\t</control>\n\t</include>\n\t'
    assert s[e - len(tail):e] == tail
    b = e - len(tail)
    old = s[a:b]
    s = (s[:a] + '\t\t\t<!-- second page: file and season (0.56.53: the Fused Glass style draws its own, _src/fgsfileseason_05653.py) -->\n'
         '\t\t\t<include condition="!$EXP[FGS]">FG_FullInfoPage2_Classic</include>\n'
         '\t\t\t<include condition="$EXP[FGS]">FGS_FileSeason</include>\n' + s[b:])
    s = s.replace('\t<!-- FG_FULLINFO:end -->', '\t<!-- FG_FULLINFO:end -->\n\t<!-- today\'s second page, moved unchanged (0.56.53) -->\n'
                  '\t<include name="FG_FullInfoPage2_Classic">\n%s\t</include>' % old, 1)
    io.open(P, 'w', encoding='utf-8', newline='\n').write(s)


def main():
    patch()
    fw.put('FileSeason', page())
    print('fgs file and season: page written')


if __name__ == '__main__':
    main()
