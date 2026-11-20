# -*- coding: utf-8 -*-
"""0.56.53 language flags in the player (user, 2026-11-19). Repeatable.
- Fused Glass player information page (FG_FullInfo in Includes_FusedPlayer.xml, written by fg_fullinfo.py: RE-RUN
  after it): the flags of the audio and of the subtitles shown, in a row under the Audio line (the Aeon page,
  FullInfo_Classic, had them; this one only the text). Rounded pack first, then the colour pack.
- The Audio / Subtitles OSD settings panel (Dlg_SettingsPanel, Includes_Settings.xml): the rounded flag of its language
  at the right end of its heading.
- The player controls' audio button (70049, written by fg_osdrow.py: RE-RUN after it too): the rounded flag of the
  playing audio in its circle while it has focus, in place of the speaker icon.
All off with Skin.HasSetting(aeon.osd.noflags)."""
import io
import os
import re

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '1080i')
P = os.path.join(D, 'Includes_FusedPlayer.xml')
SET = os.path.join(D, 'Includes_Settings.xml')
MARK = '0.56.53 language flags'
PACK = '[System.AddonIsEnabled(resource.images.languageflags.rounded) | System.AddonIsEnabled(resource.images.languageflags.colour)]'
RND = 'System.AddonIsEnabled(resource.images.languageflags.rounded)'
ON = '!Skin.HasSetting(aeon.osd.noflags) + %s' % RND
AC = '!String.IsEmpty(VideoPlayer.AudioLanguage)'
SC = 'VideoPlayer.SubtitlesEnabled + !String.IsEmpty(VideoPlayer.SubtitlesLanguage)'
NL = '\n'


def write(path, text):
    io.open(path, 'w', encoding='utf-8', newline=NL).write(text)


def flag(info, cond):
    return ('<control type="image"><width>30</width><height>30</height><aspectratio>keep</aspectratio>'
            '<texture>$INFO[%s,resource://resource.images.languageflags.rounded/,.png]</texture>'
            '<visible>%s + %s</visible></control>'
            '<control type="image"><width>40</width><height>30</height><aspectratio>keep</aspectratio>'
            '<texture>$INFO[%s,resource://resource.images.languageflags.colour/,.png]</texture>'
            '<visible>%s + System.AddonIsEnabled(resource.images.languageflags.colour) + !%s</visible></control>'
            % (info, cond, RND, info, cond, RND))


def icon(name, cond):
    return ('<control type="image"><width>26</width><height>30</height><aspectratio>keep</aspectratio>'
            '<texture colordiffuse="99ffffff">aeon/icons/%s.png</texture><visible>%s</visible></control>' % (name, cond))


def row(top):
    return (NL + '\t\t\t<!-- %s of the audio and the subtitles shown (the Aeon info page had them, this one only the text) -->' % MARK
            + NL + '\t\t\t<control type="grouplist"><left>1420</left><top>%d</top><width>364</width><height>30</height>'
            '<orientation>horizontal</orientation><itemgap>8</itemgap><visible>!Skin.HasSetting(aeon.osd.noflags) + %s</visible>'
            '%s%s%s%s</control>' % (top, PACK, icon('audio', AC), flag('VideoPlayer.AudioLanguage', AC),
                                   icon('subtitles', SC), flag('VideoPlayer.SubtitlesLanguage', SC)))


def info_page(s):
    b = s.index('<include name="FG_FullInfo">')
    e = s.find('<include name=', b + 10)
    e = len(s) if e < 0 else e
    seg = s[b:e]
    if MARK in seg:
        return s, 'info page: already there'
    seg, n = re.subn(r'<control type="label"><left>1570</left><top>(\d+)</top>[^\n]*?aeon\.pf\.audio\)\]</label></control>',
                     lambda m: m.group(0) + row(int(m.group(1)) + 36), seg)
    return s[:b] + seg + s[e:], 'info page: %d rows' % n


def button(s):
    if '0.56.53 audio button flag' in s:
        return s, 'button: already there'
    old = ('<control type="image"><left>23</left><top>21</top><width>34</width><height>34</height><aspectratio>keep</aspectratio>'
           '<texture colordiffuse="aeon_onbar">aeon/icons/audio.png</texture><visible>Control.HasFocus(70049)</visible></control>')
    if s.count(old) != 1:
        return s, 'button: focused icon not found (%d)' % s.count(old)
    cond = '%s + %s' % (ON, AC)
    new = (old.replace('<visible>Control.HasFocus(70049)</visible>', '<visible>Control.HasFocus(70049) + ![%s]</visible>' % cond)
           + '<!-- 0.56.53 audio button flag: the rounded flag of the playing audio while the button has focus -->'
           '<control type="image"><left>18</left><top>16</top><width>44</width><height>44</height><aspectratio>keep</aspectratio>'
           '<texture>$INFO[VideoPlayer.AudioLanguage,resource://resource.images.languageflags.rounded/,.png]</texture>'
           '<visible>Control.HasFocus(70049) + %s</visible></control>' % cond)
    return s.replace(old, new), 'button: flag added'


def panel():
    t = io.open(SET, encoding='utf-8').read()
    if '0.56.53 panel flag' in t:
        return 'panel: already there'
    b = t.index('<include name="Dlg_SettingsPanel">')
    i = t.index('<control type="label" id="2">', b)
    e = t.index('</control>', i) + len('</control>')
    add = (NL + '\t\t\t\t<!-- 0.56.53 panel flag: the flag of the audio / subtitle language at the right end of the heading -->'
           + NL + '\t\t\t\t<control type="grouplist"><include condition="Skin.HasSetting(aeon.fglass)">Dlg_PanelCol_fg</include>'
           '<include condition="!Skin.HasSetting(aeon.fglass)">Dlg_PanelCol</include><top>134</top><height>44</height>'
           '<orientation>horizontal</orientation><align>right</align><visible>%s</visible>'
           '<control type="image"><width>44</width><height>44</height><aspectratio>keep</aspectratio>'
           '<texture>$INFO[VideoPlayer.AudioLanguage,resource://resource.images.languageflags.rounded/,.png]</texture>'
           '<visible>Window.IsActive(osdaudiosettings) + %s</visible></control>'
           '<control type="image"><width>44</width><height>44</height><aspectratio>keep</aspectratio>'
           '<texture>$INFO[VideoPlayer.SubtitlesLanguage,resource://resource.images.languageflags.rounded/,.png]</texture>'
           '<visible>Window.IsActive(osdsubtitlesettings) + %s</visible></control>'
           '</control>' % (ON, AC, SC))
    write(SET, t[:e] + add + t[e:])
    return 'panel: flag added'


def osd_video(s):
    """the player (helper PlayerSidecar, 0.3.114): Dolby Vision with its profile ("DV P8.1") wherever FG_ChipHDR draws
    the HDR (the "In this file" Video line, the chips), and the sidecar's source format and bitrate after it on the
    Video line"""
    if '0.56.53 player sidecar' in s:
        return s, 'osd video: already there'
    old = '<variable name="FG_ChipHDR">'
    cond = ('[String.IsEqual(VideoPlayer.HdrType,dolbyvision) | String.IsEqual(VideoPlayer.HdrType,dv) | '
            'String.IsEqual(VideoPlayer.HdrType,dovi)] + !String.IsEmpty(Window(Home).Property(aeon.pf.dvp)) + '
            'String.IsEqual(Window(Home).Property(aeon.pf.mi.path),Player.FilenameAndPath)')
    s = s.replace(old, '<!-- 0.56.53 player sidecar -->' + old + '\n\t\t<value condition="%s">DV $INFO[Window(Home).Property(aeon.pf.dvp)]</value>' % cond, 1)
    line = '$VAR[OSD_FlagVideoCodec]$VAR[OSD_FlagResolution,  ·  ,]$INFO[VideoPlayer.VideoAspect,  ·  ,:1]$VAR[FG_ChipHDR,  ·  ,]'
    n = s.count(line)
    s = s.replace(line, line + '$INFO[Window(Home).Property(aeon.pf.mi.format),  ·  ,]$INFO[Window(Home).Property(aeon.pf.mi.bitrate),  ·  ,]')
    return s, 'osd video: DV profile, %d Video lines with source format and bitrate' % n


def main():
    print(panel())
    s = io.open(P, encoding='utf-8').read()
    s, m1 = info_page(s)
    s, m2 = button(s)
    s, m3 = osd_video(s)
    print(m3)
    write(P, s)
    print(m1)
    print(m2)


if __name__ == '__main__':
    main()
