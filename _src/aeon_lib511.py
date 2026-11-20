# -*- coding: utf-8 -*-
"""0.56.13 the Aeon theme's Episode list (511) and Season list combined 3 episodes (5121) to the Fused Glass list row
and info panel rules, in Aeon dress (the mockup "Episode list (511) with the rules" on canvas HJTtCDChVWkaZZAyt76wJA and
the user's notes on it: the watched mark right before the run time, in one column on every list; the episode picture
filling its box; the network logo under the poster and the next episode under it; "Season 1 | Episode 1 | Air date |
Duration"; ratings).
Aeon and Glass only; Fused Glass keeps its own views and this panel as it was.
Rows (Aeon_Ep5121Row, 740 x 88): the name on line 1; line 2 the grey line "EPISODE 4 · date" and the media chips
(Aeon's two-part resolution pill, audio, aspect), right-aligned before the mark; the mark (eye, or the progress ring
while in progress) in its column right before the run time; while in progress the time left in the accent colour.
Panel (Aeon_EpInfo): the picture (filling the column in 511), name, facts line, ratings and certificate, the status line,
the chips (resolution, audio as one chip, aspect, HDR with the profile; no codec), the plot.
Left column of 511: the network logo under the poster, the next episode (helper 0.3.94: aeon.next.*) under it.
Run from the skin folder; runs once (stops when its marker is there)."""
import io
import os
import re
import xml.etree.ElementTree as ET


def add_vis(xml, extra):
    """the control's first condition AND extra (bracketed: in Kodi + binds tighter than |)"""
    return re.sub(r'<visible>(.*?)</visible>', lambda m: '<visible>[%s] + %s</visible>' % (m.group(1), extra), xml, count=1)

VID = os.path.join('1080i', 'Includes_Aeon_Video.xml')
MARK = '0.56.13 aeon_lib511'
NFG = '!$EXP[Aeon_FGlass]'
PROG = 'Integer.IsGreater(ListItem.PercentPlayed,0)'
FOC = '[$PARAM[focused] + Control.HasFocus($PARAM[id])]'
UNF = '![$PARAM[focused] + Control.HasFocus($PARAM[id])]'
MARK_X, CHIPS_END = 632, 616
W_RES, W_AUD, W_ASP, GAP = 92, 112, 60, 6


def lbl(x, y, w, h, label, font, col, vis, extra=''):
    return ('<control type="label"><left>%d</left><top>%d</top><width>%d</width><height>%d</height>%s<font>%s</font>'
            '<textcolor>%s</textcolor><selectedcolor>%s</selectedcolor><label>%s</label><visible>%s</visible></control>\n'
            % (x, y, w, h, extra, font, col, col, label, vis))


def img(x, y, w, h, tex, col, vis, border=''):
    b = ' border="%s"' % border if border else ''
    return ('<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><texture%s colordiffuse="%s">%s</texture>'
            '<visible>%s</visible></control>\n' % (x, y, w, h, b, col, tex, vis))


def row_parts():
    out = '\t\t\t<!-- %s: line 2 (grey line, chips), the mark column, the time left (Aeon, Glass) -->\n' % MARK
    grey = '$INFO[ListItem.Premiered]'          # the number column already says which episode (the long line was cut)
    out += '\t\t\t' + lbl(110, 48, CHIPS_END - W_RES - W_AUD - W_ASP - 2 * GAP - 16 - 110, 30, grey, 'lb_small_20', '99ffffff', '%s + %s' % (NFG, UNF))
    out += '\t\t\t' + lbl(110, 48, CHIPS_END - W_RES - W_AUD - W_ASP - 2 * GAP - 16 - 110, 30, grey, 'lb_small_20', '$VAR[Aeon_OnBarInk3_L]', '%s + %s' % (NFG, FOC))
    media = '%s + !String.IsEmpty(ListItem.VideoResolution)' % NFG
    for focused in (False, True):
        f = FOC if focused else UNF
        line = '$VAR[Aeon_OnBarLine]' if focused else '88ffffff'
        ink = '$VAR[Aeon_OnBarInk2_L]' if focused else 'ccffffff'
        fill = '$VAR[Aeon_OnBarFill_L]' if focused else 'lib_aeon_white'
        inv = '$VAR[Aeon_OnBarInv]' if focused else 'lib_aeon_onbar'
        # the user, on the built rows: "resolution pill shall be on the far right always": audio, aspect, then the pill
        xa = CHIPS_END - W_RES - GAP - W_ASP
        out += '\t\t\t' + img(xa, 50, W_ASP, 28, '$VAR[Aeon_TexOutline]', line, '%s + %s + !String.IsEmpty(ListItem.VideoAspect)' % (media, f), '8')
        out += '\t\t\t' + lbl(xa + 4, 50, W_ASP - 8, 28, '$INFO[ListItem.VideoAspect]:1', 'lb_cap_14', ink, '%s + %s + !String.IsEmpty(ListItem.VideoAspect)' % (media, f), '<align>center</align><aligny>center</aligny>')
        xa -= GAP + W_AUD
        out += '\t\t\t' + img(xa, 50, W_AUD, 28, '$VAR[Aeon_TexOutline]', line, '%s + %s + !String.IsEmpty(ListItem.AudioCodec)' % (media, f), '8')
        out += '\t\t\t' + lbl(xa + 4, 50, W_AUD - 8, 28, '[UPPERCASE]$VAR[FG_EcAudio][/UPPERCASE]', 'lb_cap_14', ink, '%s + %s + !String.IsEmpty(ListItem.AudioCodec)' % (media, f), '<align>center</align><aligny>center</aligny>')
        x = CHIPS_END - W_RES
        # Aeon's two-part pill, small: the word in the outline, the solid HD block on the right
        two = '%s + %s + $EXP[Aeon_HasResL]' % (media, f)
        out += '\t\t\t' + img(x, 50, W_RES, 28, '$VAR[Aeon_TexOutline]', line, two, '8')
        out += '\t\t\t' + img(x + W_RES - 36, 50, 36, 28, 'common/white.png', fill, '%s + %s' % (media, f))
        out += '\t\t\t' + lbl(x, 50, W_RES - 36, 28, '$VAR[Aeon_ResL]', 'lb_cap_14', ink, two, '<align>center</align><aligny>center</aligny>')
        out += '\t\t\t' + lbl(x + W_RES - 36, 50, 36, 28, '$VAR[Aeon_ResR]', 'lb_cap_14', inv, '%s + %s' % (media, f), '<align>center</align><aligny>center</aligny>')
        # in progress: the ring in the mark column, the time left over the run time
        ring = '$VAR[Aeon_OnBarInk3_L]' if focused else 'fg_mark'
        out += '\t\t\t' + img(MARK_X, 30, 26, 26, 'fg/pring/$INFO[ListItem.PercentPlayed].png', ring, '%s + %s + %s' % (NFG, PROG, f))
        out += '\t\t\t' + lbl(590, 0, 130, 88, '$VAR[Aeon_RowLeft]', 'lb_small_20_bold', ring, '%s + %s + %s' % (NFG, PROG, f), '<align>right</align><aligny>center</aligny>')
    return out


def info_new(fill):
    """the panel for Aeon / Glass; fill: 511's picture fills the column (1180..1820, 360 high)"""
    if fill:
        tx, ty, tw, th, x, w, y = 1180, 0, 640, 360, 1212, 576, 384
    else:
        tx, ty, tw, th, x, w, y = 1214, 56, 572, 322, 1214, 572, 400
    C = 'Container($PARAM[id]).ListItem'
    o = ('\t\t\t<control type="group"><visible>%s + %s</visible>\n' % (NFG, '$PARAM[fill]' if fill else '![$PARAM[fill]]'))
    o += ('\t\t\t\t<control type="image"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><aspectratio>scale</aspectratio>'
          '<texture background="true">$VAR[Aeon_Ep$PARAM[id]Thumb]</texture></control>\n' % (tx, ty, tw, th))
    # the user, on the built panel: "missing yellow progress strip": Aeon's progress line along the picture's foot
    o += ('\t\t\t\t<control type="group"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><visible>Skin.HasSetting(aeon.progressline) + Integer.IsGreater(Container($PARAM[id]).ListItem.PercentPlayed,0)</visible><control type="image"><left>0</left><right>0</right><bottom>0</bottom><height>6</height><texture colordiffuse="b0000000">common/white.png</texture></control><control type="progress"><left>0</left><right>0</right><bottom>0</bottom><height>6</height><texturebg colordiffuse="00ffffff">common/aeon_line_6.png</texturebg><midtexture colordiffuse="fg_mark">common/aeon_line_6.png</midtexture><info>Container($PARAM[id]).ListItem.PercentPlayed</info></control></control>\n'
          % (tx, ty, tw, th))
    o += '\t\t\t\t' + lbl(x, y, w, 46, '[UPPERCASE]$INFO[%s.Title][/UPPERCASE]' % C, 'lb_ui_28_semibold', 'ffffffff', 'true')
    o += '\t\t\t\t' + lbl(x, y + 50, w, 30, '$VAR[Aeon_EpFacts$PARAM[id]]', 'lb_small_20', 'd9ffffff', 'true')
    # a button's texture takes no $VAR (the outline did not draw on the box): one button per theme, square in Aeon,
    # round 8 in Glass, as Aeon_TexOutline picks for images
    one = ('<control type="button"><width min="46" max="300">auto</width><height>34</height><label>%%s</label><font>lb_small_20_bold</font>'
           '<textcolor>ffffffff</textcolor><selectedcolor>ffffffff</selectedcolor><focusedcolor>ffffffff</focusedcolor><disabledcolor>ffffffff</disabledcolor>'
           '<align>center</align><aligny>center</aligny><textoffsetx>12</textoffsetx>'
           '<texturefocus border="8" colordiffuse="ccffffff">%s</texturefocus><texturenofocus border="8" colordiffuse="ccffffff">%s</texturenofocus>'
           '<visible>%s + [%%s]</visible></control>\n')

    class Btn(object):
        def __mod__(self, args):
            label, vis = args
            return ((one % ('common/aeon_outline_sq.png', 'common/aeon_outline_sq.png', '!Skin.HasSetting(aeon.vglass)')) % (label, vis) +
                    '\t\t\t\t\t' + (one % ('common/rect_outline_1_round8.png', 'common/rect_outline_1_round8.png', 'Skin.HasSetting(aeon.vglass)')) % (label, vis))
    btn = Btn()
    # the user, on the built panel: "watched status next to certification": ratings, certificate, then the status
    o += ('\t\t\t\t<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>34</height><orientation>horizontal</orientation><itemgap>10</itemgap>\n'
          '\t\t\t\t\t<include content="Aeon_RatingIcons"><param name="li" value="%s"/></include>\n'
          '\t\t\t\t\t%s'
          '\t\t\t\t\t<control type="label"><width>8</width><height>34</height><label></label></control>\n'
          % (x, y + 92, w, C, btn % ('$VAR[Aeon_LVRated]', '!String.IsEmpty(%s.MPAA)' % C)))
    o += ('\t\t\t\t\t<control type="image"><width>30</width><height>34</height><aspectratio>keep</aspectratio><texture>common/aeon_eye_off.png</texture><visible>$EXP[FG_L$PARAM[id]_Dot]</visible></control>\n'
          '\t\t\t\t\t<control type="image"><width>30</width><height>34</height><aspectratio>keep</aspectratio><texture>common/aeon_eye.png</texture><visible>$EXP[FG_L$PARAM[id]_Tick]</visible></control>\n'
          '\t\t\t\t\t<control type="image"><width>28</width><height>34</height><aspectratio>keep</aspectratio><texture colordiffuse="fg_mark">fg/pring/$INFO[%s.PercentPlayed].png</texture><visible>$EXP[FG_L$PARAM[id]_Ring]</visible></control>\n'
          '\t\t\t\t\t<control type="label"><width min="10" max="500">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>ffffffff</textcolor><label>[UPPERCASE]$VAR[FG_L$PARAM[id]_Status][/UPPERCASE]</label><visible>!$EXP[FG_L$PARAM[id]_Ring]</visible></control>\n'
          '\t\t\t\t\t<control type="label"><width min="10" max="500">auto</width><height>34</height><aligny>center</aligny><font>lb_small_20_bold</font><textcolor>fg_mark</textcolor><label>[UPPERCASE]$VAR[FG_L$PARAM[id]_Status][/UPPERCASE]</label><visible>$EXP[FG_L$PARAM[id]_Ring]</visible></control>\n'
          '\t\t\t\t</control>\n' % C)
    # the chips: audio, aspect, HDR, then the resolution (the user: "resolution pill shall be on the far right always")
    o += ('\t\t\t\t<control type="grouplist"><left>%d</left><top>%d</top><width>%d</width><height>34</height><orientation>horizontal</orientation><itemgap>6</itemgap>\n'
          '\t\t\t\t\t%s\t\t\t\t\t%s\t\t\t\t\t%s\t\t\t\t\t%s'
          '\t\t\t\t</control>\n' % (x, y + 136, w,
                                    btn % ('[UPPERCASE]$VAR[FG_L$PARAM[id]_Audio][/UPPERCASE]', '!String.IsEmpty(%s.AudioCodec)' % C),
                                    btn % ('$INFO[%s.VideoAspect,,:1]' % C, '!String.IsEmpty(%s.VideoAspect)' % C),
                                    btn % ('$VAR[FG_L$PARAM[id]_Hdr]', '!String.IsEmpty(%s.HdrType)' % C),
                                    btn % ('$VAR[Aeon_Ep$PARAM[id]Res]', '!String.IsEmpty(%s.VideoResolution)' % C)))
    o += ('\t\t\t\t<control type="textbox"><left>%d</left><top>%d</top><width>%d</width><height>%d</height><font>lb_body_24</font><textcolor>ccffffff</textcolor>'
          '<label>$INFO[%s.Plot]</label><autoscroll delay="8000" time="3000" repeat="10000">true</autoscroll></control>\n' % (x, y + 186, w, 956 - (y + 186), C))
    # the network logo at the panel's bottom right, as tall as the clock / count box at most (972..1080; the user:
    # "network logo" there, "studio logo, max height = clock dock height")
    o += ('\t\t\t\t<control type="image"><left>%d</left><top>972</top><width>%d</width><height>108</height><aspectratio align="right" aligny="center">keep</aspectratio>'
          '<texture background="true">resource://resource.images.studios.white/$INFO[%s.Studio].png</texture><visible>!Skin.HasSetting(aeon.nostudio)</visible></control>\n'
          % (x, w, C))
    o += '\t\t\t</control>\n'
    return o


def facts_var(cid):
    C = 'Container(%s).ListItem' % cid
    return ('\t<variable name="Aeon_EpFacts%s">\n'
            '\t\t<value>[UPPERCASE]$INFO[%s.Season,$LOCALIZE[20373] ,]$INFO[%s.Episode, | $LOCALIZE[20359] ,]$INFO[%s.Premiered, | ,]'
            '$INFO[%s.Duration(mins), | , $ADDON[skin.aeon.fuse 32220]]$INFO[%s.EndTimeResume, | $LOCALIZE[31030] ,][/UPPERCASE]</value>\n'
            '\t</variable>\n' % (cid, C, C, C, C, C))


def main():
    t = io.open(VID, encoding='utf-8').read()
    if MARK in t:
        print('already done')
        return
    # rows
    a = t.index('<include name="Aeon_Ep5121Row">')
    b = t.index('\t</include>', a)
    row = t[a:b]
    # the name moves to line 1 (Aeon / Glass): its labels get a twin at the top; the old ones stay for Fused Glass
    def name_twin(m):
        lab = m.group(0)
        old = add_vis(lab, '$EXP[Aeon_FGlass]')
        new = lab.replace('<top>0</top><width>470</width><height>88</height>', '<top>10</top><width>%d</width><height>40</height>' % (MARK_X - 12 - 110), 1)
        new = add_vis(new, NFG)
        return old + '\n\t\t\t' + new
    row, n = re.subn(r'<control type="label"><left>110</left><top>0</top><width>470</width><height>88</height>.*?</control>', name_twin, row)
    assert n == 2, n
    # the run time: right-aligned at 720 (Aeon / Glass), hidden while in progress; Fused Glass keeps 560..690
    def dur_twin(m):
        lab = m.group(0)
        old = add_vis(lab, '$EXP[Aeon_FGlass]')
        new = lab.replace('<left>560</left><top>0</top><width>130</width>', '<left>590</left><top>0</top><width>130</width>', 1)
        new = add_vis(new, '%s + !%s' % (NFG, PROG))
        return old + '\n\t\t\t' + new
    row, n = re.subn(r'<control type="label"><left>560</left><top>0</top><width>130</width><height>88</height>.*?</control>', dur_twin, row)
    assert n == 2, n
    # the eye: before the run time (Aeon / Glass), not while in progress
    def eye(m):
        g = m.group(0)
        old = add_vis(g, '$EXP[Aeon_FGlass]')
        new = g.replace('<param name="left">698</param>', '<param name="left">%d</param>' % MARK_X, 1)
        new = add_vis(new, '%s + !%s' % (NFG, PROG))
        return old + '\n\t\t\t' + new
    row, n = re.subn(r'<control type="group"><visible>[^<]*</visible><include content="Aeon_WatchMark"><param name="left">698</param>.*?</control>', eye, row)
    assert n == 2, n
    d = row.rindex('\t\t</definition>')
    row = row[:d] + row_parts() + row[d:]
    t = t[:a] + row + t[b:]

    # panel: the old definition is Fused Glass's now; Aeon / Glass get the rule's panel
    a = t.index('<include name="Aeon_EpInfo">')
    b = t.index('\t</include>', a)
    info = t[a:b]
    ds = info.index('<definition>') + len('<definition>')
    de = info.rindex('\t\t</definition>')
    body = info[ds:de]
    info = (info[:ds].replace('<param name="id">5121</param>', '<param name="id">5121</param>\n\t\t<param name="fill">false</param>') +
            '\n\t\t\t<!-- %s: Fused Glass keeps this panel; Aeon / Glass draw the rule\'s panel below -->\n'
            '\t\t\t<control type="group"><visible>$EXP[Aeon_FGlass]</visible>%s\t\t\t</control>\n' % (MARK, body) +
            info_new(True) + info_new(False) + info[de:])
    t = t[:a] + info + t[b:]
    old = '<include content="Aeon_EpInfo"><param name="id" value="511"/></include>'
    assert t.count(old) == 1
    t = t.replace(old, '<include content="Aeon_EpInfo"><param name="id" value="511"/><param name="fill" value="true"/></include>')

    # 511's left column: the network logo under the poster, the next episode under it (Aeon / Glass)
    old = '<include content="Aeon_StudioBlock"><param name="left">120</param><param name="top">900</param>'
    assert t.count(old) == 1
    i = t.index(old)
    e = t.index('</include>', i) + len('</include>')
    call = t[i:e]
    fg_call = call.replace('</include>', '<param name="vis" value="$EXP[Aeon_FGlass]"/></include>') if 'name="vis"' not in call else call
    NX = 'String.IsEqual(Window(Home).Property(aeon.next.of),ListItem.TVShowTitle) + !String.IsEmpty(Window(Home).Property(aeon.next.code))'
    # the next episode under the poster; the network logo is at the panel's bottom right (the user's later note)
    new = (fg_call + '\n\t\t\t<!-- %s: the next episode under the poster -->\n' % MARK +
           '\t\t\t' + lbl(120, 500, 280, 26, '[UPPERCASE]$ADDON[skin.aeon.fuse 32605][/UPPERCASE]', 'lb_cap_16', '$VAR[Aeon_Accent]', '%s + %s' % (NFG, NX), '<align>center</align>') +
           '\t\t\t' + lbl(120, 526, 280, 34, '[UPPERCASE]$INFO[Window(Home).Property(aeon.next.code)]  ·  $INFO[Window(Home).Property(aeon.next.day)][/UPPERCASE]', 'lb_ui_24_bold', 'ffffffff', '%s + %s' % (NFG, NX), '<align>center</align>'))
    t = t[:i] + new + t[e:]

    # variables
    t = t.replace('</includes>', '\t<!-- %s: the Episode list panels\' facts line -->\n' % MARK + facts_var('511') + facts_var('5121') + '</includes>')
    io.open(VID, 'w', encoding='utf-8', newline='\n').write(t)
    ET.parse(VID)
    print('ok')


if __name__ == '__main__':
    main()
